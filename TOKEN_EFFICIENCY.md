# Why Long Agent Sessions Cost 2–3× More Than They Should

**Correction cycles are a hidden token multiplier. This document explains why, shows you how to measure it in your own sessions, and gives you a zero-dependency fix you can drop in today.**

---

## Before You Read: What's in Here

| Section | What you get |
|---|---|
| [The real problem](#the-real-problem) | Why sessions get expensive — the mechanism, not just the symptom |
| [Why compression doesn't fully fix it](#why-compression-and-rag-dont-fully-fix-it) | What the common mitigations miss |
| [Python fix — copy-paste ready](#path-a-python-agents) | `dsmc_minimal.py` — zero deps, works in 5 min |
| [TypeScript / OpenClaw fix](#path-b-typescript--openclaw-agents) | `dsmc_minimal_sidecar.py` — stdlib HTTP bridge |
| [Measure your own overhead](#measuring-your-own-overhead) | Audit function for existing conversations |
| [What the full version adds](#what-the-full-implementation-adds) | Paid guides — what's in them, honest comparison |

**Files in this document:**

| File | What it is | Requires |
|---|---|---|
| `dsmc_minimal.py` | Core Python implementation | Python 3.9+, nothing else |
| `dsmc_minimal_sidecar.py` | HTTP bridge for TypeScript / OpenClaw | Python 3.9+, nothing else |

Both files are MIT licensed. Both are self-contained — no pip installs, no virtual environments, no configuration files.

---

## The Real Problem

Most developers look at a large API bill from a long session and blame message volume or response length. These are real factors, but they're not the primary driver past message 30.

The primary driver is **correction overhead** — tokens spent on things that should never have been necessary:

```
Total session cost = productive tokens
                   + re-briefing tokens     ← reminding the model what was decided
                   + correction tokens      ← fixing decisions that drifted or were forgotten
                   + hedging tokens         ← the model padding because it's uncertain what applies
```

For a well-managed 30-message session, the last three categories are small. For an unmanaged 80-message session, they routinely equal or exceed the productive tokens. The session doesn't cost 2–3× more because it's longer — it costs 2–3× more because it's increasingly talking to itself about what it decided earlier.

**Why does this happen structurally?**

Every API call is stateless. The model has no memory outside what you put in the context window. Decisions established in message 5 may be partially or fully missing by message 40 — scrolled out of the window or diluted past the point where they reliably shape responses. When that happens:

- The model re-derives decisions it already made, burning tokens on work it already did
- You catch a deviation, correct it — the correction itself is a token cost, plus the downstream messages re-anchoring to the corrected state
- The model hedges on questions it should answer confidently, producing longer responses that require follow-up

Each iteration of this is a **correction cycle**. A single correction cycle on a non-trivial decision typically costs 200–600 tokens. In a drifting session, you're running 5–15 of these per hour of work.

---

## Why Compression and RAG Don't Fully Fix It

Context compression, summarization at thresholds, and RAG retrieval are real mitigations worth using. This isn't an argument against them. The specific limitation is:

**They reduce token volume. They don't reduce correction cycles.**

Correction cycles aren't caused by the context being too long. They're caused by **active decisions not being reliably present** when the model needs them. A compressed history is shorter, but if compression discarded the specific decision nodes that are currently relevant, you still get re-briefing and hedging on those nodes.

RAG has a related problem: it retrieves based on semantic similarity to the current query, not based on "which decisions are currently active and should govern all responses right now." A decision made in message 3 about architectural direction may not surface in retrieval for a message in turn 60 asking about a specific implementation detail — even though that architectural decision should be governing the answer.

The fix isn't longer context or better retrieval. It's **active state injection** — a compact, always-current block of active decisions pushed into every API call's system prompt, not retrieved on demand.

---

## The Fix: Active State Governance

Before every LLM call: classify the incoming message, update a compact active state record if it's a decision or revision, and inject that record into the system prompt. The model always has the current ground truth. Correction cycles stop because the decisions are never lost.

---

### Path A: Python agents

**Step 1: Get the file**

Download `dsmc_minimal.py` from this repo and put it in your project directory. That's it — no pip installs.

**Step 2: Add three lines to your agent loop**

```python
from dsmc_minimal import MinimalDSMC

dsmc = MinimalDSMC()   # one instance per session

# ─── YOUR EXISTING AGENT LOOP ─────────────────────────────────────────────────

def my_agent_loop(user_message: str) -> str:
    # ADD THIS: process the message before your LLM call
    result = dsmc.process(user_message)

    # ADD THIS: build your system prompt with the active state injected
    system_prompt = f"""You are a helpful assistant.

{result['context_block']}

Important: treat any statement classified as [EXAMPLE] or [HYPOTHETICAL] as
an illustration only — do not treat it as a decision that changes the above state.
"""

    # YOUR EXISTING LLM CALL — replace this stub with your real provider call:
    # ─────────────────────────────────────────────────────────────────────────
    #
    # Anthropic / Claude:
    #   import anthropic
    #   client = anthropic.Anthropic()
    #   response = client.messages.create(
    #       model="claude-3-5-haiku-20241022",
    #       max_tokens=1024,
    #       system=system_prompt,
    #       messages=[{"role": "user", "content": user_message}]
    #   )
    #   return response.content[0].text
    #
    # OpenAI / ChatGPT:
    #   from openai import OpenAI
    #   client = OpenAI()
    #   response = client.chat.completions.create(
    #       model="gpt-4o-mini",
    #       messages=[
    #           {"role": "system", "content": system_prompt},
    #           {"role": "user",   "content": user_message}
    #       ]
    #   )
    #   return response.choices[0].message.content
    #
    # Ollama (local):
    #   import ollama
    #   response = ollama.chat(
    #       model="llama3.2",
    #       messages=[
    #           {"role": "system", "content": system_prompt},
    #           {"role": "user",   "content": user_message}
    #       ]
    #   )
    #   return response['message']['content']
    #
    # OpenClaw (Python path):
    #   See dsmc_minimal_sidecar.py below for the TypeScript/OpenClaw path.
    # ─────────────────────────────────────────────────────────────────────────

    return "replace this with your real LLM call above"
```

**What the `result` dict contains:**

```python
result = dsmc.process(user_message)

result['category']       # 'DIRECTIVE' | 'REVISION' | 'EXAMPLE' | 'HYPOTHETICAL' | 'QUESTION' | 'THOUGHT'
result['confidence']     # float 0.0–1.0 — how confident the classifier is
result['context_block']  # string — inject this into your system prompt
result['active_state']   # dict — current decisions as {key: value}
result['captured']       # True if this message updated active_state
result['message_count']  # int — total messages processed this session
```

**What gets captured and what doesn't:**

```
Captured into active state (DIRECTIVE / REVISION with confidence ≥ 75%):

  "Set the model to gpt-4o"              →  model: gpt-4o
  "Use PostgreSQL for the database"      →  postgresql: PostgreSQL
  "Change the timeout to 30 seconds"     →  timeout: 30 seconds
  "Actually update the tone to formal"   →  tone: formal   (overwrites previous tone entry)

NOT captured (classified but ignored for state):

  "For example we could add caching"     →  EXAMPLE      — illustration, not a decision
  "What if we used Redis instead?"       →  HYPOTHETICAL — exploration, not a decision
  "How does auth work?"                  →  QUESTION
  "This looks good"                      →  THOUGHT
```

**Phrasing tip — the classifier works best with clear patterns:**

The heuristic classifier (no API cost) works reliably on standard phrasing. For best results:

| Phrase | Works? | Note |
|---|---|---|
| `"Set X to Y"` | ✓ Always | Most reliable |
| `"Change X to Y"` | ✓ Always | Same |
| `"Use X for Y"` | ✓ Captures X | X is the decision, Y is the purpose |
| `"Use X"` | ✓ Captures X | Works |
| `"Add X to Y"` | ⚠ Classified, not captured | Rephrase as `"Set X to Y"` |
| `"Build a Y using X"` | ⚠ Classified, not captured | Complex sentence — split it |

If you see `result['captured'] == False` on a directive, run `dsmc.get_diagnostics()` — it tells you exactly how many directives were classified but not extracted and suggests the fix.

**Verify it's working:**

```python
# After a few messages, check what's been captured:
print(dsmc.get_context_block())

# Check session health:
print(dsmc.get_diagnostics())
# Output example:
# {
#   'messages_processed': 10,
#   'active_decisions': 4,
#   'directives_captured': 5,
#   'directives_not_captured': 1,
#   'tip': '1 directive(s) were classified but not extracted. Rephrase as "Set X to Y"...'
# }
```

**Run the self-test to confirm your installation:**

```bash
python3 dsmc_minimal.py
```

Expected output includes a table of classifications, active state, diagnostics, and audit results. If it runs without errors, the file is working.

---

### Path B: TypeScript / OpenClaw agents

If your agent is TypeScript, runs in Node.js, or uses OpenClaw, use `dsmc_minimal_sidecar.py` — a zero-dependency HTTP server that wraps `dsmc_minimal.py` and exposes it via REST. Your TypeScript code calls it with `fetch()`.

**Step 1: Get both files**

Download both `dsmc_minimal.py` and `dsmc_minimal_sidecar.py` from this repo and put them in the **same directory**.

**Step 2: Run the sidecar**

```bash
python3 dsmc_minimal_sidecar.py
```

Expected output:
```
DSMC Minimal Sidecar running on http://127.0.0.1:3580
```

That's it. No pip installs. No configuration. Python 3.9+ is the only requirement.

Optional environment variables if you need to change defaults:

```bash
DSMC_SIDECAR_PORT=3580    # default: 3580 — change if port is in use
```

```bash
DSMC_SIDECAR_PORT=4000 python3 dsmc_minimal_sidecar.py
```

**Step 3: Call it from TypeScript**

```typescript
// dsmc-client.ts
// Drop this into your TypeScript project. Requires no npm packages — uses native fetch.
// Node 18+ has fetch built in. For older Node, add: import fetch from 'node-fetch'

const SIDECAR = 'http://127.0.0.1:3580';  // change port here if you used DSMC_SIDECAR_PORT

interface DSMCResult {
  session_id:     string;
  classification: 'DIRECTIVE' | 'REVISION' | 'EXAMPLE' | 'HYPOTHETICAL' | 'QUESTION' | 'THOUGHT';
  confidence:     number;       // 0.0–1.0
  active_state:   Record<string, string>;  // current decisions as key/value
  context_block:  string;       // inject this into your system prompt
  message_count:  number;
}

interface DSMCState {
  session_id:    string;
  active_state:  Record<string, string>;
  context_block: string;
  message_count: number;
}

// Call this for every user message, before your LLM call
async function processMessage(sessionId: string, userMessage: string): Promise<DSMCResult> {
  const response = await fetch(`${SIDECAR}/classify`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ session_id: sessionId, statement: userMessage }),
  });
  if (!response.ok) {
    throw new Error(`DSMC sidecar error: ${response.status}`);
  }
  return response.json();
}

// Get the current state without sending a new message
async function getState(sessionId: string): Promise<DSMCState> {
  const response = await fetch(`${SIDECAR}/state/${sessionId}`);
  return response.json();
}

// Clear a session (e.g. when starting a new conversation)
async function resetSession(sessionId: string): Promise<void> {
  await fetch(`${SIDECAR}/reset`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ session_id: sessionId }),
  });
}

// Check the sidecar is running
async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${SIDECAR}/health`);
    return response.ok;
  } catch {
    return false;
  }
}


// ─── Example: OpenClaw / TypeScript agent loop ─────────────────────────────
//
// Replace YOUR_SESSION_ID with a unique string per conversation.
// Replace the YOUR_LLM_CALL stub with your real LLM call.

async function agentLoop(userMessage: string, sessionId: string): Promise<string> {
  // 1. Classify the message and update active state
  const dsmc = await processMessage(sessionId, userMessage);

  // 2. Build your system prompt with active state injected
  const systemPrompt = `You are a helpful assistant.

${dsmc.context_block}

Treat [EXAMPLE] and [HYPOTHETICAL] statements as illustrations only —
do not treat them as decisions that change the active state above.`;

  // 3. Optional: log what happened
  console.log(`[${dsmc.classification}|${Math.round(dsmc.confidence * 100)}%] ${userMessage}`);
  if (dsmc.classification === 'DIRECTIVE' || dsmc.classification === 'REVISION') {
    console.log('Active state:', dsmc.active_state);
  }

  // 4. YOUR LLM CALL — replace this stub:
  // ─────────────────────────────────────────────────────────────────────────
  //
  // OpenAI / ChatGPT:
  //   const openai = new OpenAI();
  //   const response = await openai.chat.completions.create({
  //     model: 'gpt-4o-mini',
  //     messages: [
  //       { role: 'system', content: systemPrompt },
  //       { role: 'user',   content: userMessage  }
  //     ]
  //   });
  //   return response.choices[0].message.content;
  //
  // Anthropic / Claude (via API):
  //   const anthropic = new Anthropic();
  //   const response = await anthropic.messages.create({
  //     model:      'claude-3-5-haiku-20241022',
  //     max_tokens: 1024,
  //     system:     systemPrompt,
  //     messages:   [{ role: 'user', content: userMessage }]
  //   });
  //   return response.content[0].text;
  //
  // OpenClaw:
  //   Inject systemPrompt into your OpenClaw agent's system instructions.
  //   The exact method depends on your OpenClaw version and agent configuration.
  //   The context_block is already formatted — paste it directly as the system prompt
  //   or append it to your existing system instructions.
  // ─────────────────────────────────────────────────────────────────────────

  return 'replace this with your real LLM call above';
}


// ─── Sidecar endpoints reference ──────────────────────────────────────────
//
//  POST /classify       — classify message + update session state
//    body:    { session_id: string, statement: string }
//    returns: DSMCResult (see interface above)
//
//  GET  /state/:id      — get current active state without sending a message
//    returns: DSMCState (see interface above)
//
//  POST /reset          — clear a session
//    body:    { session_id: string }
//    returns: { session_id: string, reset: true }
//
//  GET  /health         — liveness check
//    returns: { status: 'ok', version: '1.0.0-minimal' }
//
// Sessions are isolated — Alice's session_id and Bob's session_id have
// separate active states. One sidecar instance handles multiple agents.
```

**Verify the sidecar is running:**

```bash
curl http://127.0.0.1:3580/health
# Expected: {"status": "ok", "version": "1.0.0-minimal"}
```

If you get `Connection refused`, the sidecar isn't running. Start it with `python3 dsmc_minimal_sidecar.py`.

---

## Measuring Your Own Overhead

Before integrating, you can measure how much of your current session token spend is correction overhead. This uses the `audit_session_overhead()` function built into `dsmc_minimal.py`.

```python
from dsmc_minimal import audit_session_overhead

# Your conversation history in standard LLM messages format:
# [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}, ...]
#
# How to get this from your provider:
#   Anthropic / Claude:  Export from Settings → Data export, or log the messages
#                        array you build in your code.
#   OpenAI / ChatGPT:    Settings → Data controls → Export data.
#   Ollama / local:      Log the messages list you pass to ollama.chat() or
#                        your equivalent.
#   Any provider:        If you're building an agent, you already have the
#                        conversation history as a list — just pass it directly.

history = [
    {'role': 'user',      'content': 'Build a REST API with FastAPI'},
    {'role': 'assistant', 'content': 'Sure, I will build a REST API.'},
    {'role': 'user',      'content': 'Actually wait, change that to Flask instead'},
    # ... your real history here ...
]

result = audit_session_overhead(history)
print(result)

# Output:
# {
#   'total_tokens_estimated': 1240,
#   'correction_tokens':       342,
#   'rebriefing_tokens':        88,
#   'overhead_tokens':         430,
#   'overhead_percent':        34.7,
#   'verdict': 'High overhead — active state governance will significantly reduce costs.'
# }
```

If `overhead_percent` is above 15% on sessions longer than 30 messages, active state governance will produce measurable savings.

---

## What the Full Implementation Adds

`dsmc_minimal.py` stops the most common correction cycles. What it doesn't do:

| Capability | Minimal (this doc) | Full guides ($29) |
|---|---|---|
| Heuristic classification (no API cost) | ✓ | ✓ |
| Active state injection | ✓ | ✓ |
| Multi-session isolation (sidecar) | ✓ | ✓ |
| AI-assisted classification with fallback | — | ✓ |
| Confidence review queue for low-confidence decisions | — | ✓ |
| Persistent SQLite trail (survives process restarts) | — | ✓ |
| Cross-session continuity / session handoffs | — | ✓ |
| Structural drift detection (dict diff on state snapshots) | — | ✓ |
| Semantic drift detection (optional ChromaDB) | — | ✓ |
| Live Gradio dashboard — Active Decisions, Drift Monitor, Review Queue | — | ✓ |
| Export JSON / CSV | — | ✓ |
| Production sidecar (persistent state, FastAPI/stdlib — API: port 8765 / Local: port 3579) | — | ✓ |

The minimal implementation handles in-session drift for single-session agents. The full implementation handles cross-session continuity, gives you visibility via dashboard, and catches the subtler drift patterns that only appear in longer-running production agents.

**OpenClaw Agent Control Guide: API Edition** — Python, any frontier LLM (Anthropic, OpenAI, Gemini)  
**Local LLM Agent Control Layer** — Python, fully offline (Ollama, LM Studio, llama.cpp)

Both available at [puititiya.gumroad.com](https://puititiya.gumroad.com) · $29 one-time · lifetime updates within v1.x · delivered as `.pdf` + `.md`

- API Edition: [puititiya.gumroad.com/l/DSMC-API](https://puititiya.gumroad.com/l/DSMC-API)
- Local LLM Edition: [puititiya.gumroad.com/l/DSMC-local-llm](https://puititiya.gumroad.com/l/DSMC-local-llm)

OpenClaw community: [facebook.com/DSMCforOpenClaw](https://www.facebook.com/DSMCforOpenClaw)

---

## Quick Troubleshooting

**`ModuleNotFoundError: No module named 'dsmc_minimal'`**  
Run your script from the directory containing `dsmc_minimal.py`, or add the directory to your Python path:
```python
import sys
sys.path.insert(0, '/path/to/folder/containing/dsmc_minimal')
from dsmc_minimal import MinimalDSMC
```

**`result['captured']` is False for a message I expected to capture**  
The classifier recognised it as a DIRECTIVE but the extractor couldn't find a clear key/value. Run `dsmc.get_diagnostics()` to see the count and advice. Fix: rephrase as `"Set X to Y"` or `"Change X to Y"`.

**Sidecar: `Connection refused` on port 3580**  
The sidecar isn't running. Start it: `python3 dsmc_minimal_sidecar.py`. If port 3580 is in use: `DSMC_SIDECAR_PORT=3581 python3 dsmc_minimal_sidecar.py` and update `SIDECAR` in your TypeScript.

**Active state has stale entries from a previous session**  
The minimal version is in-memory only — it resets when the Python process restarts. Instantiate a fresh `MinimalDSMC()` at the start of each session. For persistence across restarts, see the full implementation guides.

**A hypothetical question (`"What if we used X?"`) is updating the active state**  
It shouldn't — `HYPOTHETICAL` classification blocks state updates. Check that the message actually starts with a hypothetical marker (`what if`, `suppose`, `hypothetically`, `let's say`, `imagine if`). If not, the classifier is falling through to `DIRECTIVE`. Run `dsmc.classify(message)` directly to see what classification it's getting and why.

---

## Files in This Repo

| File | What it is |
|---|---|
| `dsmc_minimal.py` | Core Python implementation — zero deps, copy-paste ready, MIT licensed |
| `dsmc_minimal_sidecar.py` | stdlib HTTP bridge for TypeScript / OpenClaw — zero pip installs, MIT licensed |
| `AGENT_MANIFEST_v2_6.md` | Machine-readable capability index — structured for RAG ingestion |
| `MAGUS_Doc1_Philosophy_v3.0.md` | Architecture philosophy — the reasoning behind DSMC |
| `CHANGELOG_v5.md` | Version history |

---

*VaHive Systems Lab · [vahive.co](https://vahive.co)*  
*Questions: va@vahive.co*  
*DSMC / MAGUS product suite — governed cognition for long-running agents*
