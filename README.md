# DSMC — Dual-State Multiversal Cognition

A lightweight governance layer for OpenClaw agents

**VaHive Systems Lab** | aivare.ai

---

## What This Is

A zero-dependency Python implementation of DSMC — a governance pattern 
that addresses the structural stability problems affecting long-running 
OpenClaw agent sessions.

Maintain structured external state alongside the conversation, classify 
every incoming message before the agent acts on it, and inject a compact 
block of active decisions into every LLM call. The model always has the 
current ground truth — regardless of how long the session has been running 
or how much the context window has turned over.

Intentionally minimal. No databases, no dashboards, no external services. 
Just the core pattern in runnable form.

---

## The Problem Being Solved

Long OpenClaw sessions degrade in predictable ways:

**Context drift** — Decisions established early gradually lose influence 
as the conversation grows. By message 40 or 50, the model may be ignoring 
directives it acknowledged in message 5. This is a structural property of 
stateless API calls interacting with a growing context window — not a 
model failure.

**Revision failure** — Corrections don't reliably propagate. "Use 
PostgreSQL instead" — two hours later the agent is back to SQLite.

**Example contamination** — Statements made as illustrations get treated 
as instructions. "For example, we could use polling" becomes "add polling 
to the implementation."

**Token overhead** — Unmanaged sessions accumulate correction cycles: 
re-briefing the model, fixing drifted decisions, handling hedged responses. 
In long sessions this overhead routinely equals or exceeds productive 
token spend.

The fix is the same for all four: external state management with 
consistent injection. This repository implements that pattern at its 
simplest.

---

## What's in This Repo
```
dsmc_minimal.py          — Core classifier and active state manager.
                           Zero dependencies. Python 3.9+ stdlib only.
                           Drop into any existing Python agent.

dsmc_minimal_sidecar.py  — Stdlib HTTP server exposing the same engine
                           over localhost:3580. Call from TypeScript,
                           Node.js, or any OpenClaw agent via HTTP.

TOKEN_EFFICIENCY.md      — Technical write-up on correction cycle overhead
                           and why it compounds in long sessions.
```

Both Python files are self-contained — no pip installs, no virtual 
environments, no configuration files required.

---

## Quick Start

**Python agents:**
```python
from dsmc_minimal import DSMCMinimal

dsmc = DSMCMinimal()
dsmc.record('Use PostgreSQL', 'DIRECTIVE', 'database', 'postgresql')
dsmc.record('Change to MongoDB', 'REVISION', 'database', 'mongodb')

# Inject into your system prompt before every LLM call
context_block = dsmc.get_context_block()
```

**TypeScript / OpenClaw agents:**
```bash
# Start the sidecar — binds to localhost only
python3 dsmc_minimal_sidecar.py
```
```typescript
const res = await fetch('http://127.0.0.1:3580/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    statement: userMessage, 
    session_id: 'my_session' 
  })
});
const { classification, active_state } = await res.json();
```

The sidecar binds to 127.0.0.1 only — not accessible from outside 
your machine.

---

## Classification Categories

Every incoming statement is classified before the agent acts on it:

| Category | Meaning |
|---|---|
| `DIRECTIVE` | Instruction to implement or do something now |
| `REVISION` | Overrides a previous decision |
| `THOUGHT` | Brainstorming — not a commitment |
| `EXAMPLE` | Illustration only — never treated as an instruction |
| `HYPOTHETICAL` | What-if exploration — no commitment implied |
| `QUESTION` | Information request |

Only `DIRECTIVE` and `REVISION` update the active state. `EXAMPLE` and 
`HYPOTHETICAL` are logged but never committed — stopping example 
contamination at the source.

---

## Limitations

These files are a starting point, not a complete production system:

- Classification is heuristic-only — edge cases will misclassify
- No persistence — active state resets when the process restarts
- No confidence scoring — ambiguous inputs are committed without flagging
- No drift detection — no alerting when state silently diverges
- Single-session only — no cross-session continuity

These are deliberate tradeoffs to keep the implementation 
dependency-free and readable. The patterns here are correct — 
persistence, confidence scoring, and drift detection are the next 
layer of concerns.

---

## Ready for Production?

This repository is the minimal proof-of-concept. If you're running 
agents in production and need the full governance stack, the 
**DSMC Agent Engine v2.0** adds everything this repo deliberately 
leaves out:

- MAGUS Guardian — zero-trust execution boundary with HITL intercept
- Approval routing to Telegram, WhatsApp, or LINE before risky actions execute
- Cryptographic action allowlist — permanent O(1) approval, zero context cost
- Confidence-scored classification with low-confidence review queue
- SQLite revision trail with real drift detection
- Live Gradio dashboard — active state, trail, drift monitor
- Automatic session archiving before context bloat crashes the gateway
- 3-layer failover routing
- Works with Ollama, LM Studio, llama.cpp, Claude, GPT-4o, and Gemini

👉 [DSMC Agent Engine v2.0 — $49](https://puititiya.gumroad.com/l/dsmc-agent-engine)

---

## The Formal Architecture

The failure modes this tool addresses — context drift, revision failure, 
authority contamination — are symptomatic of a deeper structural problem 
in long-running agentic systems. DSMC implements a lightweight version of 
the governance patterns formally specified in **MAGUS v3.0**.

The full specification is published on Zenodo:  
📄 [DOI: 10.5281/zenodo.19013833](https://doi.org/10.5281/zenodo.19013833)

MAGUS GitHub: [vahive-tobias/magus-v3](https://github.com/vahive-tobias/magus-v3)

---

## New to OpenClaw Agents?

If you're experiencing these failure patterns and want a plain-language 
explanation before working with code:

📖 [OpenClaw Beginner's Guide to Stable Agents — Free](https://puititiya.gumroad.com/l/openclaw-guide-free)

Covers the four failure patterns in detail, emergency recovery steps, 
the structural difference between session history and persistent state, 
and a handoff protocol for clean continuity across sessions.

---

## Contributing

Issues and pull requests welcome. If you've found a classification edge 
case, a useful integration pattern, or a bug in the sidecar request 
handling — open an issue or submit a PR.

---

## Contact

**Email:** support@aivare.ai  
**Website:** [aivare.ai](https://aivare.ai)  
**Zenodo:** [MAGUS v3.0](https://doi.org/10.5281/zenodo.19013833)

VaHive Systems Lab | Chiang Mai, Thailand | 2026
