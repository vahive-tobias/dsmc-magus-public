# DSMC / MAGUS — Public Changelog
**Maintainer:** VaHive Systems Lab | vahive.co | va@vahive.co  
**Format:** Newest entries first  
**File version:** CHANGELOG_v4.md  
**Record sequence:** 1 → 2 → 3 → 4 (this file)

---

## Record history

| File | Covers | Status |
|---|---|---|
| CHANGELOG_v1.md | v1.0 base prompt pack through v2.0 Agent Manifest initial release | Archived |
| CHANGELOG_v2.md | v2.1–v2.3 Agent Manifest, v1.1 Implementation Guides | Archived |
| CHANGELOG_v3.md | v2.4 Agent Manifest, v1.2 Implementation Guides, Prompting Layers Foundation v1.0, Prompt Pack Pro v2.1 | Archived |
| CHANGELOG_v4.md | v1.3 Implementation Guides, v2.5 Agent Manifest (pending) | **Current** |

---

## [2.5] — Agent Manifest — In Development
**Status:** Pending — awaiting v1.3 Gumroad listing updates  
**Products affected:** AGENT_MANIFEST.md  
**Changes planned:**
- Add Prompting Layers Foundation v1.0 to product index
- Update API and Local LLM Implementation Guide entries to v1.3
- Update all distribution endpoint references
- Add CHANGELOG.md versioning reference to Notes for Automated Systems section

---

## [v1.3] — API and Local LLM Implementation Guides — February 2026
**Status:** Released  
**Products affected:** DSMC_ImplementationGuide_API, DSMC_ImplementationGuide_Local  
**Price:** $29 minimum / $49 suggested (unchanged from v1.2)  
**Files:** DSMC_ImplementationGuide_API_v1_3.md (99KB) | DSMC_ImplementationGuide_Local_v1_3.md (84KB)

### What's new

**Confidence scoring** — every classification now returns a confidence score (0.0–1.0) alongside the category. Score is logged to the revision trail, visible in the dashboard, and used by the mode toggle to determine handling. Breaking change from v1.2: `classify_statement()` return signature changed from `str` to `(str, float)` tuple.

**Confidence Mode Toggle (Auto / Review)** — new dashboard control. Auto: all classifications committed to active state immediately, confidence score logged for reference. Review: DIRECTIVE and REVISION classifications below the threshold (default 0.70, set via `DSMC_CONFIDENCE_THRESHOLD` in `.env`) are held in a Review Queue for operator approval before updating active state. Operators confirm, override, or dismiss. Mode is toggled in the dashboard Settings panel.

**Structural drift detection** — after the first three DIRECTIVE entries, the system snapshots active state. Every subsequent message performs a dict diff against that snapshot. If a decision has changed without a corresponding REVISION entry, a drift warning fires in the dashboard chat immediately. This replaces the previous message-counter proxy with real detection of unrecorded state changes.

**Semantic drift detection (optional)** — ChromaDB integration. At snapshot time the active state is embedded and stored. Each drift check compares the current state embedding against the snapshot via cosine distance. Fires at distance > 0.4 (configurable). Activated via dashboard Settings or `trail.enable_semantic_drift()`. ChromaDB is optional — system operates without it.

**Node.js / TypeScript sidecar** — `sidecar.py` runs the Python DSMC engine as a lightweight local HTTP server. Default port **8765** (API guide, FastAPI/uvicorn — requires `pip install fastapi uvicorn`); default port **3579** (Local guide, stdlib `http.server` — zero extra dependencies). TypeScript and OpenClaw agents call it via HTTP — no Python integration required on the agent side. Endpoints: `POST /classify`, `POST /record`, `POST /handoff`, `POST /resolve`, `GET /state`, `GET /trail`, `GET /export`. `dsmc-client.ts` TypeScript module with full OpenClaw usage example included in both guides.

**Session export** — Export JSON and Export CSV buttons in dashboard. Full revision trail — all entries, timestamps, confidence scores, before/after values for every revision. JSON export includes session metadata and active state snapshot.

**Review Queue** — low-confidence items accumulate in a dedicated dashboard panel (Review mode). Each entry shows 8-char ID, classification, confidence, and statement. Resolved via Settings → Resolve.

**Integration depth table** — honest, tiered time estimates in both guides: Surface (2–4 hrs), Functional (4–8 hrs), Structural (1–2 days), Deep (3–5 days).

**LM Studio and llama.cpp adaptation sections** — restored from v1.2 and updated for v1.3 classifier signature (Local guide only).

**Enhanced auto-extraction** — handles `Actually change X to Y`, `Use X for Y`, qualifier stripping (`actually`, `instead`, `no,`).

### Technical notes
- All code AST-verified across both guides, 8 Python blocks each
- Trail schema additions: `confidence REAL` and `low_confidence INTEGER` columns added to `revision_trail` table; new `drift_events` table
- `record()` now accepts `confidence` and `low_confidence` keyword arguments
- Low-confidence DIRECTIVE/REVISION entries written to trail but do NOT update `active_nodes` until resolved via `resolve_low_confidence()`
- Local guide (84KB) has 18 sections vs API guide (99KB) 15 sections — Local has 3 additional sections (Adapting for LM Studio, Adapting for llama.cpp, Phase 3 Semantic Drift as standalone); API guide has more code per section due to multi-provider routing

### Deferred to v2.0 (DSMC Advanced)
- **Classifier Option B** — second-pass LLM re-evaluation of ambiguous inputs. Deferred to preserve low latency and allow real-world misclassification data to inform calibration. The Auto/Review toggle in v1.3 provides operator control at the UI layer without adding API latency.
- **Environmental Input Classification Layer (EICL)** — classifies tool outputs, web fetches, and file reads before they re-enter the agent loop. Indirect prompt injection protection.
- **Memory Graph Foundation** — semantic search across full session history, related past decisions surfaced automatically.
- **Multi-agent session coordination** — shared revision trail with authority hierarchy.

---

*Previous changelog records archived as CHANGELOG_v1.md through CHANGELOG_v3.md.*  
*For full product history see archived records.*

---

*DSMC / MAGUS Public Changelog | VaHive Systems Lab | vahive.co*  
*© 2026 VaHive Systems Lab. All rights reserved.*
