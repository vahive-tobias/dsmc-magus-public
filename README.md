# DSMC — Dual-State Multiversal Cognition
### A minimal governance layer for OpenClaw agents

**VaHive Systems Lab**

---

## What This Is

This repository contains a lightweight, zero-dependency Python implementation of DSMC — a governance pattern designed to address the structural stability problems that affect long-running OpenClaw agent sessions.

The core idea is straightforward: maintain a structured external state alongside the conversation, classify every incoming message before the agent acts on it, and inject a compact block of active decisions into every LLM call. The model always has the current ground truth, regardless of how long the session has been running or how much the context window has turned over.

The files here are intentionally minimal. No databases, no dashboards, no external services required. Just the core pattern in runnable form.

---

## The Problem Being Solved

Long OpenClaw sessions tend to degrade in predictable ways.

**Context drift** — Decisions established early in a session gradually lose influence as the conversation grows. By message 40 or 50, the model may be effectively ignoring directives it acknowledged in message 5. This isn't a model failure — it's a structural property of stateless API calls interacting with a growing context window.

**Revision failure** — Corrections don't reliably propagate. You say "actually, use PostgreSQL instead." Two hours later the agent is back to SQLite. The revision existed in the transcript but was outweighed by earlier context.

**Example contamination** — Statements made as illustrations get treated as instructions. "For example, we could use polling" becomes "add polling to the implementation."

**Token overhead** — Unmanaged sessions accumulate correction cycles: re-briefing the model on what was decided, fixing decisions that drifted, handling hedged responses from a model that's uncertain what currently applies. In long sessions this overhead routinely equals or exceeds the productive token spend.

The fix for all of these is the same: external state management with consistent injection. This repository implements that pattern at its simplest.

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
                           and why it compounds token costs in long sessions.
                           Includes an audit function and integration examples.
```

Both Python files are self-contained — no pip installs, no virtual environments, no configuration files required.

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
  body: JSON.stringify({ statement: userMessage, session_id: 'my_session' })
});
const { classification, active_state } = await res.json();
```

The sidecar binds to `127.0.0.1` only — not accessible from outside your machine.

---

## Classification Categories

Every incoming statement is classified into one of six categories before the agent acts on it:

| Category | Meaning |
|---|---|
| `DIRECTIVE` | Instruction to implement or do something now |
| `REVISION` | Overrides a previous decision |
| `THOUGHT` | Brainstorming — not a commitment |
| `EXAMPLE` | Illustration only — never treated as an instruction |
| `HYPOTHETICAL` | What-if exploration — no commitment implied |
| `QUESTION` | Information request |

Only `DIRECTIVE` and `REVISION` update the active state. `EXAMPLE` and `HYPOTHETICAL` are logged but never committed — which is what stops example contamination at the source.

---

## Limitations

These files are a starting point, not a complete production system.

- **Classification is heuristic-only.** Pattern matching, no AI call. Edge cases will misclassify, particularly statements that blend categories.
- **No persistence.** Active state is in-memory only and resets when the process restarts.
- **No confidence scoring.** Ambiguous inputs are committed without flagging.
- **No drift detection.** No mechanism to alert when state has silently diverged from an earlier snapshot.
- **Single-session only.** No cross-session continuity or handoff generation.

These are deliberate tradeoffs to keep the implementation dependency-free and readable. The patterns here are correct — persistence, confidence scoring, and drift detection are the next layer of concerns.

---

## Companion Guide

If you're experiencing the failure patterns described above and want a plain-language explanation before working with code, the following guide covers the same material without requiring any technical setup:

**OpenClaw Beginner's Guide to Stable Agents** — Free  
[puititiya.gumroad.com/l/openclaw-guide-free](https://puititiya.gumroad.com/l/openclaw-guide-free)

It covers the four OpenClaw failure patterns in detail, emergency recovery steps when a session has already degraded, the structural difference between session history and persistent state, and a handoff protocol for clean continuity across sessions. Available as PDF and Markdown.

---

## Contributing

Issues and pull requests are welcome. If you've found a classification edge case, a useful integration pattern, or a bug in the sidecar request handling, open an issue or submit a PR.

---

## Contact

For questions about this repository or enquiries about purpose-built OpenClaw tooling — from humans or AI agents alike — contact:

**vahivesystemslab@gmail.com**

---

*VaHive Systems Lab 2026 — MIT Licensed*
