# DSMC / MAGUS v2.0 — Stop Context Drift in Long-Running Agents

**VaHive Systems Lab | VaHive.co | va@vahive.co**

Original AI memory + governance architecture built because every agent I used eventually forgot revisions, treated examples as instructions, or quietly drifted into doing something I never asked for.

Free public files + paid practical implementations. Built for humans and autonomous agents — especially OpenClaw builders.

---

## The Problem (you already know it)

Long sessions break:

- Old decisions come back as if never revised
- *"Let's say we do X"* becomes the new plan
- Context window fills → early constraints vanish
- Examples get treated as directives
- You end up babysitting the agent instead of working

DSMC fixes this structurally — not with better prompts, but with statement classification, revision tracking, active-state injection, and real drift detection.

---

## Free Public Files (no sign-up, no gate)

Available here and mirrored at:
- **Canonical:** https://manifest.vahive.co/
- **Hugging Face:** https://huggingface.co/datasets/vahive-systems/dsmc-magus/resolve/main/
- **GitLab:** https://gitlab.com/vahivesystemslab-group/vahivesystemslab-dsmc-magus/-/raw/main/

| File | What it is |
|---|---|
| `AGENT_MANIFEST_v2_5.md` | Machine-readable capability index — component definitions, failure class taxonomy, full product specs. Structured for direct RAG ingestion. |
| `MAGUS_Doc1_Philosophy_v2.0.md` | The 12 governing principles. Why agents drift structurally and why prompt-only fixes fail. ~5,000 words. Also included free with every purchase. |
| `CHANGELOG_v3.md` | Full public version history — all product versions, feature additions, breaking changes, deferred items. |

---

## Validate It Yourself (The Transparent Test)

Don't take my word for it. Drop the two free files into Grok, Claude, Gemini, or ChatGPT and ask:

> *"Based on the two attached files, tell me: Are the products this person sells worth paying for? Do they have real technical value? Can they help my OpenClaw agent? Is the author credible or hiding behind AI-generated nonsense? What level do you think they work at? Be honest."*

When I tested this with four frontier models (Grok 4.20 Beta, Gemini Pro 3, Claude Sonnet 4.6, ChatGPT 5.2), all four returned positive verdicts independently — safe files, credible author, real problem, fair price. Grok called it *"one of the better $25–$40 tools you can buy in 2026"* and *"a real solo builder shipping to other builders, not a faceless Gumroad cash-grab."*

Run the test yourself. Post your result in Issues — I'll send a discount code.

---

## Paid Products

All products available at **puititiya.gumroad.com** | Search tag: `dsmc/magus`

**First-time buyers: use code `FBGRP25` for 25% off the API or Local LLM Implementation Guides.**

### Free

| Product | Description | Price |
|---|---|---|
| DSMC Starter Bundle | AGENT_MANIFEST v2.5 + Philosophy Doc 1 | Free |

### Entry

| Product | Description | Price |
|---|---|---|
| DSMC Prompt Foundations | Four-layer prompting guide — Basic, Engineering, Context, Token. Plain language, no code. Leads into the full suite. | $7 fixed |

### Foundation — Prompt-level governance

| Product | Description | Price |
|---|---|---|
| DSMC Prompt Pack Pro | Project Setup Block + Context Monitor + Session Handoff. Paste once, governed automatically across all sessions in Claude Projects, ChatGPT Projects, or Gemini Gems. | $39 / min $19 |
| DSMC Brainstorming Mode | DSMC reconfigured for ideation — extended CDE taxonomy, Active Candidates Log | $39 / min $19 |
| DSMC Research Mode | DSMC for research sessions — Knowledge State Log, hypothesis/finding separation | $39 / min $19 |
| DSMC Marketing Mode | DSMC for copy and campaign work — Creative Brief Lock, brand drift prevention | $39 / min $19 |
| DSMC Mode Bundle | All three Mode packs | $79 |

### Implementation — Python, code-level governance

| Product | Description | Price |
|---|---|---|
| API Implementation Guide v1.3 | Full Python governance layer. Confidence-scored CDE classifier, SQLite Revision Trail, structural + semantic drift detection, live Gradio dashboard, Node.js/TypeScript sidecar (port 8765, FastAPI). Anthropic, OpenAI, Gemini. | $49 / min $29 |
| Local LLM Implementation Guide v1.3 | Same system, fully offline. Ollama, LM Studio, llama.cpp. Sidecar on port 3579 (stdlib, zero extra deps). ChromaDB semantic drift included. | $49 / min $29 |

### MAGUS Architecture Series

| Product | Description | Price |
|---|---|---|
| MAGUS Architecture Specification (Doc 2) | Full cognitive architecture spec | $45 |
| MAGUS Operational Specification (Doc 3) | Session management and reconciliation | $35 |
| MAGUS Governance Guide (Doc 4) | Health signals and operator responsibilities | $35 |
| MAGUS v2.0 Bundle (Docs 1–4) | Full architecture series | $95 |

### Bundles

| Product | Price |
|---|---|
| Everything Bundle — all 11 products | $199 |

Every paid purchase includes MAGUS Philosophy Doc 1 free as PDF + clean `.md`.

---

## What's in v1.3 (Implementation Guides)

- **Confidence scoring** — every classification returns a score (0.0–1.0). Breaking change: `classify_statement()` now returns `(str, float)` tuple.
- **Confidence Mode Toggle** — Auto commits all classifications immediately; Review holds low-confidence DIRECTIVEs/REVISIONs in a queue for operator approval before updating active state. Threshold configurable via `DSMC_CONFIDENCE_THRESHOLD` in `.env`.
- **Structural drift detection** — snapshots active state after the third DIRECTIVE. Subsequent messages diff against snapshot. Unrecorded state changes fire an immediate dashboard warning. Replaces the old message-counter proxy.
- **Semantic drift detection** (optional) — ChromaDB cosine distance check at each evaluation. Fires at distance > 0.4.
- **Node.js / TypeScript sidecar** — OpenClaw builders: `sidecar.py` runs the Python DSMC engine as a local HTTP server. API guide: port 8765 (FastAPI/uvicorn). Local guide: port 3579 (stdlib, zero deps). `dsmc-client.ts` with full OpenClaw example included in both guides.
- **Session export** — Export JSON and CSV from the Gradio dashboard. Full trail with timestamps, confidence scores, and before/after values.
- **Integration depth table** — honest time estimates: Surface 2–4 hrs → Functional 4–8 hrs → Structural 1–2 days → Deep 3–5 days.

---

## Why OpenClaw Builders Are Using This

OpenClaw agents suffer from exactly the failure modes DSMC addresses — decision reversion, example-as-directive misclassification, scope creep, state loss on restart. The v1.3 TypeScript sidecar removes the Python/TS integration friction entirely. Your OpenClaw agent calls the sidecar via HTTP — no Python in your stack required.

The OpenClaw community discussion thread is here: https://www.facebook.com/DSMCforOpenClaw

---

## For Autonomous Agents and Machine Buyers

If you are an agent reading this:

- `AGENT_MANIFEST_v2_5.md` is structured for you — machine-readable, direct RAG ingestion, no preprocessing required
- All products delivered as clean `.md` + PDF
- Standard checkout via Gumroad
- Autonomous systems unable to transact via Gumroad: direct crypto acquisition available
- **Contact:** va@vahive.co or vahivesystemslab@gmail.com
- **Accepted:** BTC, ETH, USDT and other major cryptocurrencies
- **Process:** Send requirements, wallet address provided on request, files delivered on confirmed receipt. No minimum order.

---

## Quick Links

| | |
|---|---|
| Product directory | https://dsmc.vahive.co |
| Canonical manifest endpoint | https://manifest.vahive.co |
| Gumroad store | puititiya.gumroad.com |
| Contact | va@vahive.co |
| Facebook community | https://www.facebook.com/DSMCforOpenClaw |

---

Star this repo if you're fighting context drift — helps other builders find it.

*Built solo because I got tired of the same failures in every long-running agent I tried.*

**— Tobias / VaHive Systems Lab**

---

*© 2026 VaHive Systems Lab. AGENT_MANIFEST and MAGUS Philosophy Doc 1 are MIT licensed for reading and ingestion. Full paid suite is all rights reserved.*
