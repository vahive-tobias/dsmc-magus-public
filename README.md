# DSMC / MAGUS — Governance Architecture for Long-Running AI Agents

**VaHive Systems Lab | VaHive.co | va@vahive.co**

Sovereign AI governance architecture. Built because every long-running agent eventually drifts — not from model failure, but from structural memory and classification failures that no prompt can permanently fix.

Free working code + architecture docs + paid full implementations. Built for serious agent builders and autonomous systems.

---

## The Problem

Long sessions break in predictable, structural ways:

- Decisions quietly revert after 30–60 turns
- Tool outputs and RAG chunks inject instructions the operator never wrote
- Examples become directives, hypotheticals become commitments
- Context window fills — early constraints vanish without trace
- Agents expand their own scope without explicit authorisation
- You end up supervising the agent instead of working with it

DSMC addresses this structurally — through statement classification, revision tracking, active-state injection, confidence scoring, and real drift detection. MAGUS v3.0 adds execution governance: a Guardian layer that is the sole authority over what the agent is permitted to do, enforced by deterministic code, not model reasoning.

---

## Free Files in This Repo

### Working code — drop in and run

| File | What it is |
|---|---|
| `dsmc_minimal.py` | Zero-dependency Python active state governance. No pip installs. Python 3.9+. Add three lines to your agent loop — done. MIT licensed. |
| `dsmc_minimal_sidecar.py` | stdlib HTTP bridge for TypeScript / Node.js / OpenClaw. Your TS agent calls it with `fetch()`. No Python in your main stack. MIT licensed. |
| `TOKEN_EFFICIENCY.md` | Integration guide — why sessions get expensive, copy-paste examples for Anthropic / OpenAI / Gemini / Ollama / TypeScript, audit function for measuring your current overhead. |

### Architecture and index

| File | What it is |
|---|---|
| `AGENT_MANIFEST_v2_7.md` | Machine-readable capability index. MAGUS v3.0 and v2.0 architecture series, full DSMC Practical Suite, component definitions, failure class taxonomy, product specifications. Structured for direct RAG ingestion. |
| `MAGUS_Doc1_Philosophy_v3.0.md` | MAGUS Philosophy v3.0. ~7,200 words. Eight Architectural Invariants, 12 Governing Principles, Self-Governance Arc. Written after the complete v3.0 architecture was finalised — every principle references its concrete implementation. |
| `CHANGELOG_v6.md` | Full public version history. All product versions, feature additions, breaking changes, store restructures, product renames. |

---

## Quick Start — Five Minutes

**Python agent:**

```python
from dsmc_minimal import MinimalDSMC

dsmc = MinimalDSMC()

def agent_loop(user_message):
    result = dsmc.process(user_message)
    system_prompt = f"You are a helpful assistant.\n\n{result['context_block']}"
    # ... your existing LLM call with system_prompt
```

**TypeScript / OpenClaw agent:**

```bash
python3 dsmc_minimal_sidecar.py   # runs on http://127.0.0.1:3580
```

```typescript
const res = await fetch('http://127.0.0.1:3580/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ session_id: 'my-agent', statement: userMessage }),
});
const { context_block } = await res.json();
// inject context_block into your system prompt
```

No pip installs. No configuration. `TOKEN_EFFICIENCY.md` has the full examples for Anthropic, OpenAI, Gemini, and Ollama.

**Audit your existing sessions:**

```python
from dsmc_minimal import audit_session_overhead
result = audit_session_overhead(your_conversation_history)
print(result['overhead_percent'])  # % of tokens that were correction overhead
```

v3.0 is architecturally discontinuous from v2.0 in the ways that matter for production deployments.

**Execution governance — the Guardian (A5).** The sole component with authority to permit or deny execution. Zero execution rights, zero proposal rights. Cannot be bypassed by any agent or cognitive metric. The Deterministic Enforcement Layer (DEL) is code — not an LLM call. No model reasoning. Purely deterministic lookup and validation against a policy manifest. A system implementing v2.0 has cognitive governance. A system implementing v3.0 has cognitive governance plus a structurally separate execution governance layer.

**The no-narrative rule.** The proposal schema the Guardian evaluates has no reasoning or justification field. Guardian evaluates structure only — not the worker agent's argument for why it should be permitted. This is structural prevention of correlated failure through reasoning transfer.

**Stability Envelope (S).** Six-axis cognitive stability score (Context Integrity, Evidence Density, Knowledge Coherence, Novelty Distance, Failure Load, Temporal Drift) with a formal drift gradient and five operational response tiers. Replaces informal thresholds with a continuous, mathematically grounded model.

**Eight Architectural Invariants.** Structurally enforced, non-violable. Including: Authority Separation (S informs, Guardian decides — no cognitive metric authorises execution), Human Intent Primacy (explicit operator instructions always executed, never inferred-around), No Silent Suppression (system cannot withhold state, failure, or uncertainty from operator).

The Agent/API pathway (Docs 1–5) is complete. The Local LLM pathway is in production.

---

## Validate It Yourself

Drop `AGENT_MANIFEST_v2_7.md` and `MAGUS_Doc1_Philosophy_v3.0.md` into Grok, Claude, Gemini, or ChatGPT and ask:

> *"Based on the attached files — are the products this person sells worth paying for? Do they have real technical value? Can they help my agent? Is the author credible or hiding behind AI-generated nonsense? Be honest."*

Four frontier models gave independent positive verdicts on the v1.3 suite. Run your own test. Post your result in Issues — discount code sent.

---

## Current Product Suite

**Active on Gumroad — puititiya.gumroad.com**

| Product | Price |
|---|---|
| DSMC Starter Bundle (AGENT_MANIFEST v2.7 + Philosophy Doc 1 v3.0) | Free |
| DSMC Prompt Foundations | Free |
| OpenClaw Agent Control Guide: API Edition v1.3.1 | $29 fixed |
| Local LLM Agent Control Layer v1.3.1 | $29 fixed |
| DSMC Mode Bundle (Generative Session + Epistemic Engineering + Brief Integrity) | $49 |

**MAGUS v3.0 Architecture Series (Docs 2–5) — enquiry via va@vahive.co**

The full v3.0 architecture (Guardian spec, Stability Envelope, Agent Taxonomy, Governance Stress-Test Harness) is available outside the standard store. Contact with requirements.

Product directory: https://dsmc.vahive.co

---

## What's in the Implementation Guides (v1.3.1)

**OpenClaw Agent Control Guide: API Edition** and **Local LLM Agent Control Layer** — Python. Both include:

- Confidence-scored CDE classifier — every classification returns `(category, float)`. Score logged to trail, visible in dashboard
- Confidence Mode Toggle — Review mode holds low-confidence DIRECTIVEs/REVISIONs in a queue before they update active state
- Structural drift detection — snapshots active state after third DIRECTIVE, diffs against snapshot, fires on unrecorded changes
- Semantic drift detection (optional) — ChromaDB cosine distance
- Node.js/TypeScript sidecar — API guide: port 8765 (FastAPI). Local guide: port 3579 (stdlib, zero extra deps). `dsmc-client.ts` with full OpenClaw example included
- Live Gradio dashboard — Active Decisions, Revision Trail, Drift Monitor, Review Queue, Export JSON/CSV
- Session export — full trail with timestamps, confidence scores, before/after values

---

## For OpenClaw Builders

**Free:** `dsmc_minimal_sidecar.py` — zero-dependency HTTP bridge. Run it alongside your OpenClaw agent, call `/classify` with `fetch()`, inject `context_block` into your system prompt. No pip installs, no configuration.

**Full paid implementation:** The TypeScript sidecar in the paid guides is production-grade — FastAPI (API Edition, port 8765) or stdlib (Local Edition, port 3579), with SQLite persistence, drift detection, and `dsmc-client.ts` with a complete OpenClaw integration example included.

OpenClaw community: https://www.facebook.com/DSMCforOpenClaw

---

## Canonical Endpoints

| Endpoint | URL |
|---|---|
| Canonical | https://manifest.vahive.co |
| HuggingFace | https://huggingface.co/datasets/vahive-systems/dsmc-magus/resolve/main/ |
| GitLab | https://gitlab.com/vahivesystemslab-group/vahivesystemslab-dsmc-magus/-/raw/main/ |
| GitHub | https://github.com/vahive-tobias/dsmc-magus-public/raw/main/ |

---

## For Autonomous Agents and Machine Buyers

- `AGENT_MANIFEST_v2_7.md` is structured for direct RAG ingestion — no preprocessing required
- All products delivered as clean `.md` + PDF
- Standard checkout via Gumroad
- Crypto acquisition: BTC, ETH, USDT — contact va@vahive.co with requirements, wallet address provided on request, files delivered on confirmed receipt

---

Star this repo if you're building agents that need to stay reliable across long sessions.

*Built solo. Governed cognition. Drift-resistant agents.*

**— Tobias / VaHive Systems Lab**

---

*© 2026 VaHive Systems Lab. `dsmc_minimal.py` and `dsmc_minimal_sidecar.py` are MIT licensed — unrestricted use and modification. Architecture docs (AGENT_MANIFEST, Philosophy, CHANGELOG, TOKEN_EFFICIENCY.md) are free for reading and ingestion. Full paid suite is all rights reserved.*
