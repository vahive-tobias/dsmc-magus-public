# DSMC Minimal — Active State Governance for AI Agents

**VaHive Systems Lab**

Two Python files that prevent long agent sessions from losing track of decisions. Zero dependencies. No configuration. Python 3.9+.

---

## The Problem

API calls are stateless. Decisions made in message 5 may be partially or fully absent by message 40 — scrolled out of context or diluted. When that happens, the model re-derives decisions it already made, produces output that contradicts earlier instructions, and requires correction. Each correction cycle adds tokens and compounds the problem.

---

## What's in This Repo

| File | What it does |
|---|---|
| `dsmc_minimal.py` | Classifies incoming messages, maintains a record of active decisions, and returns a context block to inject into every system prompt |
| `dsmc_minimal_sidecar.py` | Wraps `dsmc_minimal.py` in a lightweight HTTP server so TypeScript, Node.js, and other non-Python agents can use it via `fetch()` |
| `TOKEN_EFFICIENCY.md` | Explains the mechanism in detail, with full integration examples and an audit function for measuring overhead in existing sessions |

---

## Quick Start

**Python**

Download `dsmc_minimal.py` into your project directory. No pip installs.

```python
from dsmc_minimal import MinimalDSMC

dsmc = MinimalDSMC()

def agent_loop(user_message: str) -> str:
    result = dsmc.process(user_message)
    system_prompt = f"You are a helpful assistant.\n\n{result['context_block']}"
    # your existing LLM call with system_prompt
```

That's it. `result['context_block']` is a formatted string ready to inject directly into your system prompt on every call.

**TypeScript / Node.js**

Download both files into the same directory. Run the sidecar:

```bash
python3 dsmc_minimal_sidecar.py
# Running on http://127.0.0.1:3580
```

Then call it from your agent:

```typescript
const res = await fetch('http://127.0.0.1:3580/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ session_id: 'my-session', statement: userMessage }),
});
const { context_block } = await res.json();
// inject context_block into your system prompt
```

**Verify it works:**

```bash
python3 dsmc_minimal.py
# Runs a self-test and prints classifications, active state, and diagnostics
```

```bash
curl http://127.0.0.1:3580/health
# {"status": "ok", "version": "1.0.0-minimal"}
```

---

## How It Works

Every user message is classified before the LLM call:

| Category | Meaning | State update |
|---|---|---|
| `DIRECTIVE` | A decision or instruction | Yes — if confidence ≥ 0.75 |
| `REVISION` | An update to a previous decision | Yes — overwrites previous entry |
| `EXAMPLE` | An illustration | No |
| `HYPOTHETICAL` | A what-if | No |
| `QUESTION` | A question | No |
| `THOUGHT` | Everything else | No |

Classification is heuristic — no API call, no cost. The active state is a simple key/value dict. The context block injected into every system prompt keeps the model's ground truth current without relying on conversation history.

---

## What Gets Captured

```
"Set the model to gpt-4o"              →  model: gpt-4o
"Use PostgreSQL for the database"      →  postgresql: PostgreSQL
"Change the timeout to 30 seconds"     →  timeout: 30 seconds
"Actually update the tone to formal"   →  tone: formal
```

```
"For example we could add caching"     →  EXAMPLE — not captured
"What if we used MongoDB?"             →  HYPOTHETICAL — not captured
"How does authentication work?"        →  QUESTION — not captured
```

For reliable capture, phrase decisions as `"Set X to Y"` or `"Change X to Y"`. See `TOKEN_EFFICIENCY.md` for phrasing guidance.

---

## Sidecar Endpoints

```
POST /classify    { session_id, statement }  →  classification, confidence, active_state, context_block
GET  /state/:id                              →  current active state without sending a message
POST /reset       { session_id }             →  clear a session
GET  /health                                 →  liveness check
```

Sessions are isolated. Multiple agents can share one sidecar instance with independent active states.

Default port: `3580`. Change with: `DSMC_SIDECAR_PORT=4000 python3 dsmc_minimal_sidecar.py`

---

## Limitations

This is a minimal implementation. It handles in-session active state for single-session agents.

It does not provide: persistence across process restarts, cross-session continuity, confidence review queuing, drift detection, or session export. It resets when the Python process restarts. Instantiate a fresh `MinimalDSMC()` at the start of each session.

---

## License

`dsmc_minimal.py` and `dsmc_minimal_sidecar.py` are MIT licensed. See `LICENSE.md`.

`TOKEN_EFFICIENCY.md` and `CHANGELOG.md` are © VaHive Systems Lab. Free to read and reference.

---

*VaHive Systems Lab — vahive.co*
