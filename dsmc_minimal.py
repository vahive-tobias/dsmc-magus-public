# dsmc_minimal.py
# Minimal Active-State Governance — kills correction-cycle token waste
# Zero deps. Works with Ollama, Claude, GPT, Gemini, LM Studio, llama.cpp — anything.
# Python 3.9+  |  No pip installs required
#
# ── Quick start ──────────────────────────────────────────────────────────────
#
#   from dsmc_minimal import MinimalDSMC
#   dsmc = MinimalDSMC()
#
#   In your agent loop, before every LLM call:
#     result = dsmc.process(user_message)
#     system_prompt = f"You are a helpful assistant.\n\n{result['context_block']}"
#     # ... then call your LLM with system_prompt as normal
#
# ── What gets captured into active state ─────────────────────────────────────
#
#   CAPTURED (updates ground truth):
#     "Set the model to gpt-4o"            →  model: gpt-4o
#     "Use PostgreSQL for the database"    →  postgresql: PostgreSQL
#     "Change the timeout to 30s"          →  timeout: 30s
#     "Actually update the tone to formal" →  tone: formal
#
#   NOT CAPTURED (classified but does not pollute state):
#     "For example we could use Redis"     →  EXAMPLE      — illustrations only
#     "What if we used MongoDB?"           →  HYPOTHETICAL — exploration only
#     "How does authentication work?"      →  QUESTION
#     "This looks good"                    →  THOUGHT
#
# ── Phrasing tips for best extraction ────────────────────────────────────────
#
#   Best:  "Set X to Y"         →  clean key/value every time
#          "Change X to Y"      →  same
#          "Use X for Y"        →  captures X as the decision
#
#   Avoid: Compound sentences with multiple decisions in one message.
#          Split them: "Set the DB to Postgres. Set cache to Redis."
#          rather than: "Set the DB to Postgres and cache to Redis."
#
# ─────────────────────────────────────────────────────────────────────────────

from typing import Dict, List, Tuple, Optional
import re
import time


class MinimalDSMC:
    def __init__(self):
        self.active_state: Dict[str, str] = {}   # current ground truth
        self.revision_log: List[dict] = []        # full audit trail
        self.message_count: int = 0
        self._uncaptured_directives: int = 0      # directives classified but not extracted

    # ── Classifier ──────────────────────────────────────────────────────────

    def classify(self, statement: str) -> Tuple[str, float]:
        """
        Classify a statement into one of six categories (no API call, no cost).

        Categories:
          DIRECTIVE    — a decision or instruction that should be remembered
          REVISION     — an update to a previous decision
          EXAMPLE      — illustration (should NOT update active state)
          HYPOTHETICAL — exploration / what-if (should NOT update active state)
          QUESTION     — a question (no state change)
          THOUGHT      — everything else (no state change)
        """
        s = statement.lower().strip()

        # HYPOTHETICAL checked before QUESTION so "What if..." → HYPOTHETICAL not QUESTION
        if any(p in s for p in ['what if', 'suppose', 'hypothetically', "let's say", 'imagine if']):
            return 'HYPOTHETICAL', 0.85

        if any(s.startswith(p) for p in ['actually ', 'change ', 'update ', 'switch ', 'no, ', 'instead ']):
            return 'REVISION', 0.92

        if any(s.startswith(p) for p in ['set ', 'use ', 'make ', 'create ', 'build ',
                                          'add ', 'remove ', 'delete ', 'enable ', 'disable ']):
            return 'DIRECTIVE', 0.88

        if any(p in s for p in ['for example', 'e.g.', 'such as', 'like when', 'as an example']):
            return 'EXAMPLE', 0.90

        if s.endswith('?') or any(s.startswith(p) for p in
                                  ['what ', 'how ', 'why ', 'when ', 'where ', 'who ', 'which ']):
            return 'QUESTION', 0.90

        return 'THOUGHT', 0.55

    # ── Extraction ──────────────────────────────────────────────────────────

    def extract_topic_value(self, statement: str, category: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract a (topic, value) pair from a DIRECTIVE or REVISION.
        Returns (None, None) if no clear key/value can be determined — this is
        normal for complex or compound sentences. Rephrase as "Set X to Y" for
        reliable capture.
        """
        if category not in ('DIRECTIVE', 'REVISION'):
            return None, None

        # Strip common leading filler words
        s = re.sub(r'^(actually|instead|no,|please|ok,|okay,)\s+', '',
                   statement.strip(), flags=re.I)

        def clean_key(k: str) -> str:
            k = k.strip().lower().replace(' ', '_')
            k = re.sub(r'^the_', '', k)            # "the_model" → "model"
            k = re.sub(r'[^a-z0-9_]', '_', k)     # safe characters only
            k = re.sub(r'_+', '_', k).strip('_')   # collapse underscores
            return k

        def clean_value(v: str) -> str:
            # Strip trailing filler words that sneak in from natural phrasing
            filler = r'\s+\b(instead|now|also|too|then|though|please|ok|okay)\b\s*$'
            return re.sub(filler, '', v.strip(), flags=re.I).strip()

        # ── Pattern 1: "set/change/update/switch X to Y" ──────────────────
        match = re.search(r'(?:set|change|update|switch)\s+(.+?)\s+to\s+(.+)', s, re.I)
        if match:
            topic = clean_key(match.group(1))
            value = clean_value(match.group(2))
            if topic and value:
                return topic, value

        # ── Pattern 2: "use X" (strips purpose clause) ────────────────────
        # "Use Python 3.11 for the project"  →  python_3_11: Python 3.11
        # "Use async/await throughout"       →  async:       async/await
        # "Use Redis instead of Postgres"    →  redis:       Redis
        match = re.search(r'^use\s+(.+)', s, re.I)
        if match:
            raw = match.group(1)
            # Strip any "for X", "in X", "throughout", "instead of X", "when X" clauses
            value = re.split(r'\s+(?:for|in|throughout|instead|when)\s+', raw, maxsplit=1)[0]
            value = clean_value(value)
            if value:
                key_word = value.split()[0]
                topic = clean_key(key_word)
                return topic, value

        return None, None

    # ── Core processing ──────────────────────────────────────────────────────

    def process(self, user_message: str) -> dict:
        """
        Main entry point — call this for every user message before your LLM call.

        Returns:
          category      — DIRECTIVE | REVISION | EXAMPLE | HYPOTHETICAL | QUESTION | THOUGHT
          confidence    — float 0.0–1.0
          context_block — formatted string, inject directly into your system prompt
          active_state  — dict of current decisions {topic: value}
          message_count — total messages processed this session
          captured      — True if this message updated active_state
        """
        category, confidence = self.classify(user_message)
        topic, value = self.extract_topic_value(user_message, category)

        captured = False

        if category in ('DIRECTIVE', 'REVISION'):
            if topic and value and confidence >= 0.75:
                self.active_state[topic] = value
                captured = True
            else:
                # Classified as a decision but extraction didn't find a clear key/value.
                # Normal for compound or vague sentences.
                # Fix: rephrase as "Set X to Y" for reliable capture.
                self._uncaptured_directives += 1

        self.message_count += 1
        self.revision_log.append({
            'ts':         time.time(),
            'category':   category,
            'confidence': confidence,
            'statement':  user_message,
            'topic':      topic,
            'value':      value,
            'captured':   captured,
        })

        return {
            'category':      category,
            'confidence':    confidence,
            'context_block': self.get_context_block(),
            'active_state':  dict(self.active_state),
            'message_count': self.message_count,
            'captured':      captured,
        }

    # ── Output helpers ───────────────────────────────────────────────────────

    def get_context_block(self) -> str:
        """
        Returns the active state block, ready to inject into a system prompt.
        Inject this on EVERY API call — it replaces the need to re-brief the model.
        """
        if not self.active_state:
            return "No active decisions recorded yet."
        lines = ["CURRENT ACTIVE DECISIONS (treat as ground truth — do not deviate):"]
        for k, v in self.active_state.items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    def get_diagnostics(self) -> dict:
        """
        Returns a summary of session health.
        Run this if active_state looks wrong — it shows how many directives
        were classified but not captured, and why.
        """
        directives_total = sum(
            1 for e in self.revision_log if e['category'] in ('DIRECTIVE', 'REVISION')
        )
        captured = directives_total - self._uncaptured_directives
        return {
            'messages_processed':      self.message_count,
            'active_decisions':        len(self.active_state),
            'directives_captured':     captured,
            'directives_not_captured': self._uncaptured_directives,
            'tip': (
                'All directives captured successfully.'
                if self._uncaptured_directives == 0
                else (
                    f'{self._uncaptured_directives} directive(s) were classified but not extracted. '
                    'This is normal for compound sentences or vague phrasing. '
                    'Rephrase as "Set X to Y" or "Change X to Y" for reliable extraction.'
                )
            ),
        }

    def reset(self) -> None:
        """
        Clear all session state and start fresh.
        Useful when starting a new conversation mid-script without
        instantiating a new MinimalDSMC object.
        """
        self.active_state.clear()
        self.revision_log.clear()
        self.message_count = 0
        self._uncaptured_directives = 0

    def get_token_savings_estimate(self, session_token_count: int) -> dict:
        """
        Rough estimate of token savings from active state governance.
        Based on observed correction-cycle overhead in unmanaged sessions.

        Pass in the total token count of the current session. If you don't know it,
        estimate it as: len(full_conversation_text) // 4
        """
        reduction = 0.45 if self.message_count > 30 else 0.25
        return {
            'session_tokens':            session_token_count,
            'estimated_savings_percent': round(reduction * 100, 1),
            'estimated_tokens_saved':    int(session_token_count * reduction),
            'note': (
                'Estimate only. Actual savings depend on how decision-heavy your sessions are. '
                'Run audit_session_overhead() on exported history to measure your real baseline.'
            ),
        }


# ── Standalone audit — run against any existing conversation history ─────────

def audit_session_overhead(conversation_history: list) -> dict:
    """
    Estimates how much of an existing conversation's tokens were correction overhead.

    Pass in a list of message dicts in standard LLM format:
      [
        {'role': 'user',      'content': 'Build me a REST API'},
        {'role': 'assistant', 'content': 'Sure, here is the API...'},
        ...
      ]

    Works with exported history from Claude, ChatGPT, Gemini, Ollama, or any
    provider using the standard messages format.

    To get your history:
      Claude:  Settings → Data export, or copy from conversation
      ChatGPT: Settings → Data controls → Export
      Ollama:  Log your messages array as you build it in code
    """
    correction_markers = [
        'actually', 'wait,', 'no,', 'instead', 'i said', 'i meant',
        'change that', 'update that', 'forget that', 'disregard',
        'let me clarify', 'as i mentioned', 'going back to',
        'to clarify', 'correction',
    ]
    rebriefing_markers = [
        'remember that', 'as established', 'we decided', 'you should know',
        'to remind you', 'keep in mind', "don't forget", 'as i told you',
        'as agreed', 'like i said', 'as discussed',
    ]

    total_tokens = correction_tokens = rebriefing_tokens = 0

    for msg in conversation_history:
        content = str(msg.get('content', ''))
        token_estimate = max(1, len(content) // 4)
        total_tokens += token_estimate
        content_lower = content.lower()

        if any(m in content_lower for m in correction_markers):
            correction_tokens += token_estimate
        elif any(m in content_lower for m in rebriefing_markers):
            rebriefing_tokens += token_estimate

    overhead = correction_tokens + rebriefing_tokens
    overhead_pct = round((overhead / total_tokens * 100), 1) if total_tokens else 0.0

    if overhead_pct < 10:
        verdict = 'Low overhead — correction cycles not yet significant. DSMC still prevents future drift.'
    elif overhead_pct < 25:
        verdict = 'Moderate overhead — active state governance will measurably reduce your costs.'
    else:
        verdict = 'High overhead — active state governance will significantly reduce costs in sessions like this.'

    return {
        'total_tokens_estimated': total_tokens,
        'correction_tokens':      correction_tokens,
        'rebriefing_tokens':      rebriefing_tokens,
        'overhead_tokens':        overhead,
        'overhead_percent':       overhead_pct,
        'verdict':                verdict,
    }


# ── Self-test — run: python3 dsmc_minimal.py ─────────────────────────────────

if __name__ == '__main__':
    print('dsmc_minimal.py — self-test\n')

    dsmc = MinimalDSMC()

    test_messages = [
        'Use Python 3.11 for this project',
        'Set the database to PostgreSQL with async support',
        'Actually change the database to MongoDB instead',
        'Set the response tone to professional',
        'For example the bot could handle order tracking',
        'What if we added a FAQ database?',
        'How does authentication work?',
        'This is looking good so far',
        'Add rate limiting to 10 requests per minute',
        'Change the model to claude-3-5-haiku instead',
    ]

    print(f'{"":2} {"CATEGORY":<14} {"CONF":>5}  {"CAPTURED":>8}  STATEMENT')
    print('─' * 78)
    for msg in test_messages:
        r = dsmc.process(msg)
        flag = '✓' if r['captured'] else '·'
        print(f'{flag}  {r["category"]:<14} {r["confidence"]:>4.0%}  '
              f'{"yes" if r["captured"] else "":>8}  {msg[:55]}')

    print()
    print('ACTIVE STATE:')
    print(dsmc.get_context_block())

    print()
    print('DIAGNOSTICS:')
    for k, v in dsmc.get_diagnostics().items():
        print(f'  {k}: {v}')

    print()
    print('TOKEN SAVINGS ESTIMATE (12,400 token session):')
    for k, v in dsmc.get_token_savings_estimate(12400).items():
        print(f'  {k}: {v}')

    print()
    print('AUDIT (sample history):')
    sample_history = [
        {'role': 'user',      'content': 'Build a REST API with FastAPI'},
        {'role': 'assistant', 'content': 'Sure, I will build a REST API.'},
        {'role': 'user',      'content': 'Actually change that to Flask instead'},
        {'role': 'assistant', 'content': 'Switching to Flask.'},
        {'role': 'user',      'content': 'As I mentioned, use PostgreSQL'},
        {'role': 'assistant', 'content': 'Got it, using PostgreSQL.'},
        {'role': 'user',      'content': 'Remember that we want async support'},
        {'role': 'assistant', 'content': 'Yes, adding async support.'},
    ]
    for k, v in audit_session_overhead(sample_history).items():
        print(f'  {k}: {v}')
