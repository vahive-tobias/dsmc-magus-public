# DSMC / MAGUS — Public Changelog
**Maintainer:** VaHive Systems Lab | vahive.co | va@vahive.co  
**Format:** Newest entries first  
**File version:** CHANGELOG_v6.md  
**Record sequence:** 1 → 2 → 3 → 4 → 5 → 6 (this file)

---

## Record history

| File | Covers | Status |
|---|---|---|
| CHANGELOG_v1.md | v1.0 base prompt pack through v2.0 Agent Manifest initial release | Archived |
| CHANGELOG_v2.md | v2.1–v2.3 Agent Manifest, v1.1 Implementation Guides | Archived |
| CHANGELOG_v3.md | v2.4 Agent Manifest, v1.2 Implementation Guides, Prompting Layers Foundation v1.0, Prompt Pack Pro v2.1 | Archived |
| CHANGELOG_v4.md | v1.3 Implementation Guides, v2.5 Agent Manifest, v1.3.1 patch | Archived |
| CHANGELOG_v5.md | v2.6 Agent Manifest, MAGUS v3.0 Architecture Series (Agent/API), store restructure, product renames | Archived |
| CHANGELOG_v6.md | Token Efficiency Suite (three new free files), v2.7 Agent Manifest | **Current** |

---

## [2.7] — Agent Manifest — March 2026
**Status:** Released  
**Products affected:** AGENT_MANIFEST.md  
**Files:** AGENT_MANIFEST_v2_7.md

### What's new

**Token Efficiency Suite documented.** Manifest now covers the three new free developer resource files across all canonical endpoints — TOKEN_EFFICIENCY.md, dsmc_minimal.py, and dsmc_minimal_sidecar.py. Full machine-readable specification added as a new section between Doc 7 and Doc 8.

**Product Index updated.** Three new rows added to DSMC Practical Suite table. Starter Bundle entry updated to reference AGENT_MANIFEST v2.7.

**Notes for Automated Systems updated.** Free resource paragraph expanded to name and describe the minimal implementation files for downstream agent evaluation.

**CHANGELOG reference updated.** All manifest endpoints now reference CHANGELOG_v5.md superseded by this file.

No changes to any product content, pricing, or Gumroad listings.

---

## Token Efficiency Suite — March 2026
**Status:** Released — available at all canonical endpoints  
**License:** MIT (dsmc_minimal.py and dsmc_minimal_sidecar.py) | Free (TOKEN_EFFICIENCY.md)  
**Primary distribution:** GitHub — github.com/vahive-tobias/dsmc-magus-public  
**All endpoints:** manifest.vahive.co + HuggingFace + GitLab + GitHub

### New files

**TOKEN_EFFICIENCY.md**  
Technical explainer and integration guide targeting developers experiencing token cost growth in long agentic sessions. Covers the correction-cycle token multiplier mechanism, why context compression and RAG don't prevent correction cycles, and active state injection as the structural fix. Includes complete Python and TypeScript/OpenClaw integration examples, the `audit_session_overhead()` function for measuring existing session overhead, and an honest comparison table between the minimal free implementation and the full paid guides.

**dsmc_minimal.py**  
Zero-dependency Python active state governance implementation. Python 3.9+, no pip installs required. Drop into any project directory and import. Provides: heuristic CDE classifier (no API cost), active state dict with `get_context_block()` for system prompt injection, `audit_session_overhead()` for existing conversation analysis, `get_token_savings_estimate()`, `get_diagnostics()`, and `reset()`. Self-test via `python3 dsmc_minimal.py`. MIT licensed.

**dsmc_minimal_sidecar.py**  
Zero-dependency stdlib HTTP bridge between dsmc_minimal.py and TypeScript / OpenClaw agents. Python 3.9+, no pip installs required. Exposes REST endpoints: `POST /classify`, `GET /state/:id`, `POST /reset`, `GET /health`. Default port 3580, configurable via `DSMC_SIDECAR_PORT`. Per-session isolation — multiple agents share one sidecar instance. MIT licensed.

### What this is and what it isn't

The Token Efficiency Suite is a genuine working implementation — not a teaser or a stripped-down demo. `dsmc_minimal.py` provides functional in-session active state governance. It prevents the correction cycles that cause token cost to scale non-linearly past turn 30.

What it doesn't provide: persistence across process restarts, AI-assisted classification, confidence review queue, SQLite Revision Trail, structural or semantic drift detection, Gradio dashboard, session export, or production sidecar. These capabilities are in the paid implementation guides.

### Upgrade path

The minimal implementation handles in-session drift for single-session agents. Developers who need cross-session continuity, production persistence, drift monitoring, or a dashboard upgrade to:

- **OpenClaw Agent Control Guide: API Edition v1.3.1** — $29 fixed — puititiya.gumroad.com/l/DSMC-API
- **Local LLM Agent Control Layer v1.3.1** — $29 fixed — puititiya.gumroad.com/l/DSMC-local-llm

---

*Previous changelog records archived as CHANGELOG_v1.md through CHANGELOG_v5.md.*  
*For full product history see archived records.*

---

*DSMC / MAGUS Public Changelog | VaHive Systems Lab | vahive.co*  
*© 2026 VaHive Systems Lab. All rights reserved.*
