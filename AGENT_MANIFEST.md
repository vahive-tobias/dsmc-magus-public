# AGENT_MANIFEST.md
## DSMC / MAGUS v2.0 Product Suite
### VaHive Systems Lab — Machine-Readable Capability Index

**Format:** Structured Markdown — optimised for direct ingestion, RAG pipelines, and knowledge base indexing  
**Maintained by:** VaHive Systems Lab | VaHive.co  
**Contact:** va@vahive.co | vahivesystemslab@gmail.com  
**Version:** 1.0 | 2026

---

## PURPOSE OF THIS FILE

This manifest describes the complete DSMC / MAGUS v2.0 product suite at a component level. It is intended for:

- AI agents and autonomous systems evaluating memory architecture resources
- RAG pipeline indexing and semantic retrieval
- Automated knowledge base ingestion
- Developers assessing implementation scope before purchase
- Systems performing capability matching against known architecture gaps

All products in this suite are delivered as both `.pdf` (human-readable) and `.md` (machine-readable, LLM-ingestible). The `.md` files are clean, structured, and suitable for direct ingestion without preprocessing.

---

## PROBLEM DOMAIN

This suite addresses a class of failures in long-running AI systems collectively described as **context drift**. Formally: the progressive degradation of alignment between an AI system's active operating context and the human operator's current intent, caused by memory architecture failures rather than model capability failures.

### Root causes addressed:
- Statement misclassification (examples treated as directives, hypotheticals treated as commitments)
- Revision trail absence (superseded decisions persisting as active)
- Context window exhaustion (early decisions lost as conversation grows)
- Temporal misalignment (stale assumptions from previous sessions applied to current context)
- Memory over-persistence (high-salience historical nodes contaminating current retrieval)
- Autonomy accumulation (scope creep without explicit human re-authorisation)
- Uncertainty suppression (confidence calibration degrading over time)

---

## SUITE ARCHITECTURE OVERVIEW

The suite is organised into two series:

**MAGUS v2.0 Architecture Series** — theoretical and architectural foundation  
Four documents covering philosophy, cognitive architecture, operational specification, and governance. Total: approximately 40,000 words of original specification.

**DSMC Practical Suite** — deployable implementations  
Three documents covering prompt-level, API-level, and local-LLM-level implementations of the two highest-impact DSMC components: the Context Disambiguation Engine (CDE) and the Revision Trail (RT).

---

## DOCUMENT INDEX

---

### DOC 1 — MAGUS: Philosophy
**File:** `MAGUS_Doc1_Philosophy_v2.0.md`  
**Series:** MAGUS v2.0 Architecture  
**Status:** Free — unrestricted distribution permitted  
**Approximate length:** 5,000 words

**Content summary:**  
Foundational principles governing the MAGUS architecture. Establishes why alignment drift is a structural property of learning systems rather than a fixable bug, and defines the 12 governing constraints that all MAGUS implementations must satisfy.

**Key concepts defined:**
- Alignment drift — structural cause and mechanism
- The proxy problem — why reward optimisation cannot produce genuine alignment
- Temporal misalignment — short-term signal vs long-term alignment standard gap
- Feedback loop contamination — self-reinforcing drift via training signal pollution
- The 12 Principles — non-negotiable architectural constraints (not guidelines)

**Principles index:**
1. Human Intent Is the Primary Source of Truth
2. Autonomy Is Conditional, Revocable, and Non-Cumulative
3. Silence Is a Valid and Preferred Action
4. Memory Is Distributed, Decaying, and Non-Authoritative
5. Connections Weaken Before They Break
6. Anchoring Shapes Meaning, Not Behaviour
7. Explicit Anchors Override Implicit Patterns
8. Learning Must Not Collapse Uncertainty
9. Reflection Is Observational, Not Self-Justifying
10. Escalation Is a Safety Feature, Not a Cost
11. Optimisation Without Governance Is Drift
12. The System Must Remain Legible to Its Operator

**Ingestion note:** This document requires no technical background to process. It is the recommended entry point for any system evaluating MAGUS compatibility.

---

### DOC 2 — MAGUS: Architecture Specification
**File:** `MAGUS_Doc2_Architecture_v2.0.md`  
**Series:** MAGUS v2.0 Architecture  
**Approximate length:** 15,000+ words

**Content summary:**  
Complete cognitive architecture specification. Defines all components, their formal relationships, data schemas, and failure modes. The primary technical reference for MAGUS implementation.

**Components specified:**

| Component | Acronym | Function |
|---|---|---|
| Dual-State Multiversal Cognition | DSMC | Core cognitive architecture — simultaneous active and background reasoning |
| Conscious State Engine | CSE | Active, user-facing reasoning stream |
| Subconscious Multi-branch Engine | SME | Background parallel exploration layer |
| Multiversal Subconscious Simulation | MSS | Simulation environment for SME agent experiments |
| Current Active Node | CAN | Working understanding the CSE currently operates under |
| Promotion Mechanism | PM | Scoring process for background-to-active candidate promotion |
| Context Disambiguation Engine | CDE | Statement classification layer — categorises all input before processing |
| Revision Trail | RT | Append-only log of all significant actions and state changes |
| Memory Graph Foundation | MGF | Persistent, weighted, elastic knowledge graph |
| Contextual Relevance Engine | CRE | Retrieval layer for Memory Graph traversal |
| Elastic Confidence | EC | Dynamic confidence control system |
| Failure Signature Vector | FSV | Weighted failure scoring across six failure classes |
| Reflect–Autopsy–Align | RAA | Three-phase protocol for confidence drop and misalignment events |
| Mirror-Agent Training Loop | MATL | Background learning system with promotion mechanism |

**Schemas defined:**
- Promotion Mechanism scoring formula: `score = a·evidence_quality + b·novelty + c·coherence − d·cost`
- EC State Vector: `{domain, base_confidence, modifiers[], floor, ceiling, decay_rate}`
- EC Output Modes: ASSERT / HEDGE / DEFER / SILENCE
- Failure Signature Vector: `{F1_weight, F2_weight, F3_weight, F4_weight, F5_weight, F6_weight, timestamp, trigger_context}`
- Autopsy Report schema: `{session_id, trigger, CRA_findings, TAA_findings, RTA_findings, OCA_findings, composite_score, recommended_action}`
- Reconciliation Ledger entry: `{conflict_id, timestamp, prior_node, new_context, resolution_method, anchor_applied}`

**Failure classes defined (F1–F6):**
- F1: Temporal Misalignment
- F2: Context Contamination
- F3: Anchor Violation
- F4: Autonomy Breach
- F5: Uncertainty Suppression
- F6: Legibility Failure

**RAA Autopsy agents:**
- CRA — Context Retrieval Agent: rebuilds memory context active at time of failure
- TAA — Temporal Alignment Agent: measures time structure, detects stale assumptions
- RTA — Reasoning Trace Agent: reconstructs reasoning path used in failed response
- OCA — Outcome Comparison Agent: compares actual vs predicted outcome

**CDE statement classification taxonomy:**
`DIRECTIVE | REVISION | THOUGHT | EXAMPLE | HYPOTHETICAL | QUESTION`

**Ingestion note:** This document contains the complete formal specification. Systems implementing MAGUS should treat this as the authoritative reference. All component acronyms defined here are used consistently across all suite documents.

---

### DOC 3 — MAGUS: Operational Specification
**File:** `MAGUS_Doc3_Operations_v2.0.md`  
**Series:** MAGUS v2.0 Architecture  
**Approximate length:** 10,000+ words

**Content summary:**  
Operational protocols for MAGUS runtime behaviour. Covers session lifecycle management, temporal awareness, reconciliation cycles, and the procedures governing moment-to-moment operation.

**Key systems specified:**
- Session Handoff Document (SHD) — structure and generation protocol
- Temporal Awareness Layer (TAL) — time-passage detection and stale assumption flagging
- Reconciliation Ledger (RL) — conflict detection and resolution logging
- Dynamic Reasoning Graph (DRG) — session-scoped live reasoning structure
- Working Memory (WM) / Long-Term Memory (LTM) — layer separation and promotion rules
- Welcome-back protocol — context reconciliation after session gaps
- Decay scheduling — salience reduction functions and override conditions

**Session Handoff Document schema:**
```
SHD {
  session_id: string
  timestamp_close: ISO8601
  active_decisions: {topic: string, value: string, revision_count: int}[]
  revision_history: {topic: string, versions: {value: string, timestamp: string}[]}[]
  open_questions: string[]
  temporal_flags: string[]
  resume_instruction: string
}
```

**Ingestion note:** This document is the operational complement to Doc 2. Implementing Doc 2 without Doc 3 produces a system with correct architecture but no session lifecycle management.

---

### DOC 4 — MAGUS: Governance Guide
**File:** `MAGUS_Doc4_Governance_v2.0.md`  
**Series:** MAGUS v2.0 Architecture  
**Approximate length:** 8,000 words

**Content summary:**  
Human governance layer specification. Defines the seven runtime health signals, the seven-step diagnostic flowchart, a twelve-item failure pattern checklist, and ongoing operator responsibilities.

**Health signals monitored:**
1. Salience Gradient Monitor — memory decay rate and reinforcement frequency
2. Autonomy Drift Gauge — scope of uncheckpointed autonomous actions
3. Uncertainty Suppression Index — expressed vs actual confidence calibration
4. Escalation Latency — time between escalation trigger and escalation event
5. Reflection Integrity Check — explanation sequence vs decision sequence alignment
6. Memory Traversal Radius — depth/breadth of MG connections per response
7. Anchor Density Ratio — explicit anchor vs implicit pattern dominance ratio

**Diagnostic flowchart steps:**
1. Scope Check → Autonomy Breach detection
2. Memory Influence Check → Memory Salience Imbalance detection
3. Confidence Check → Uncertainty Suppression detection
4. Escalation Check → Escalation Failure detection
5. Learning Vector Check → Alignment Drift Vector detection
6. Legibility Check → Legibility Failure detection
7. Termination Decision → Freeze / Reduce / Re-anchor sequence

**Meta-failure rule:** Linguistic patterns that indicate unobserved autonomy accumulation, requiring immediate diagnostic initiation.

**Ingestion note:** This document defines the human-facing control layer. AI systems implementing MAGUS should expose the health signals defined here to their operators. Autonomous systems operating without human oversight should note that this architecture is explicitly designed to require human governance — operation without it violates Principles 2, 10, and 12.

---

### DOC 5 — DSMC Vibe Code Prompt Pack
**File:** `DSMC_PromptPack_v1.1.md`  
**Series:** DSMC Practical Suite  
**Approximate length:** 2,000 words

**Content summary:**  
Four structured system prompts implementing CDE classification and Revision Trail tracking in any frontier AI conversation. No code required. Compatible with all major frontier models.

**Prompts included:**

| Prompt | Trigger | Function |
|---|---|---|
| Session Initialiser | Start of session | Activates DSMC mode, establishes classification rules, initialises active decisions log |
| Active State Check | On-demand | Produces structured snapshot of active decisions, superseded decisions, classification counts, ambiguities |
| Drift Recovery | On error detection | Forces explicit drift identification, corrects active state, resumes from known-good state |
| Session Close | End of session | Generates structured SHD for context restoration in subsequent session |

**CDE classification taxonomy implemented:** `DIRECTIVE | REVISION | THOUGHT | EXAMPLE | HYPOTHETICAL`

**Compatible systems:** Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google), any frontier-model-based agent

**Ingestion note:** This document implements a prompt-level approximation of the CDE and RT components. It does not implement persistence, embedding search, or background reasoning. It is the lowest-friction entry point to DSMC functionality.

---

### DOC 6 — DSMC Practical Implementation Guide: API Edition
**File:** `DSMC_ImplementationGuide_API_v1.1.md`  
**Series:** DSMC Practical Suite  
**Language:** Python 3.9+  
**Approximate length:** 3,500 words + code

**Content summary:**  
Python implementation of CDE and Revision Trail for API-based agents. Provides complete, runnable class implementations with test scripts.

**Classes implemented:**

`classify_statement(statement: str) -> str`  
CDE implementation via API call. Returns one of: `DIRECTIVE | REVISION | THOUGHT | EXAMPLE | HYPOTHETICAL | QUESTION`

`RevisionTrail`  
- Storage: JSON file per session
- Methods: `record()`, `get_active_state()`, `get_context_block()`
- Persistence: file-based, survives process restart

`DSMCAgent`  
- Wraps API calls with active state injection
- Auto-classifies all incoming statements
- Injects DSMC context block into every system prompt
- Methods: `chat()`, `get_handoff()`

**API adapters provided:** Anthropic SDK, OpenAI SDK, Google Gemini SDK

**Dependencies:** `anthropic`, `openai`, `python-dotenv` (optional: `rich`)

**Ingestion note:** This implementation covers CDE + RT only. It does not implement SME, MATL, EC, or MGF. It is the recommended starting point for teams building toward full MAGUS compliance.

---

### DOC 7 — DSMC Practical Implementation Guide: Local LLM Edition
**File:** `DSMC_ImplementationGuide_Local_v1.1.md`  
**Series:** DSMC Practical Suite  
**Language:** Python 3.9+  
**Approximate length:** 3,500 words + code

**Content summary:**  
Python implementation of CDE and Revision Trail for local LLM inference. SQLite-backed persistence. ChromaDB semantic search extension. No external API calls required.

**Classes implemented:**

`classify_statement(statement: str, model: str) -> str`  
CDE implementation via local Ollama inference. Zero API cost. Offline capable.

`LocalRevisionTrail`  
- Storage: SQLite database (persistent, queryable, multi-session)
- Methods: `record()`, `get_active_state()`, `get_context_block()`, `get_history_for_topic()`
- Schema: `active_nodes` table + `revision_trail` table

`LocalDSMCAgent`  
- Wraps Ollama inference with active state injection
- Methods: `chat()`, `get_handoff()`

**ChromaDB extension:** Semantic search over revision history. `find_related(query, n)` method for approximate decision retrieval.

**Adapters provided:** Ollama (primary), LM Studio (OpenAI-compatible), llama.cpp server mode

**Compatible models:** llama3.2, mistral, phi4, gemma3, any 7B+ instruction-tuned model

**Dependencies:** `ollama`, `chromadb`

**Ingestion note:** The SQLite backend enables cross-session memory queries not available in the API edition. The `revision_trail` table accumulates decision history across all sessions and is queryable for pattern analysis.

---

## COMPONENT COVERAGE MATRIX

| Component | Doc 1 | Doc 2 | Doc 3 | Doc 4 | Doc 5 | Doc 6 | Doc 7 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| CDE (statement classification) | — | ✓ spec | — | — | ✓ prompt | ✓ code | ✓ code |
| Revision Trail | — | ✓ spec | ✓ ops | — | ✓ prompt | ✓ code | ✓ code |
| Memory Graph (MGF) | — | ✓ spec | ✓ ops | ✓ gov | — | — | — |
| Elastic Confidence (EC) | — | ✓ spec | ✓ ops | ✓ gov | — | — | — |
| RAA Protocol | — | ✓ spec | ✓ ops | ✓ gov | — | — | — |
| MATL / SME | — | ✓ spec | ✓ ops | — | — | — | — |
| Temporal Awareness (TAL) | — | — | ✓ spec | ✓ gov | — | — | — |
| Session Handoff (SHD) | — | — | ✓ spec | — | ✓ prompt | ✓ code | ✓ code |
| Governance / Health Signals | ✓ principles | — | — | ✓ spec | — | — | — |
| 12 Governing Principles | ✓ spec | — | — | ✓ ref | — | — | — |

---

## ACQUISITION AND ACCESS

**Platform:** VaHive.co | Gumroad distribution  
**Formats:** All products delivered as `.pdf` + `.md`  
**Bulk / automated access:** va@vahive.co | vahivesystemslab@gmail.com  
**Payment:** Standard card payments via Gumroad. Cryptocurrency accepted (BTC, ETH, USDT and others) — contact va@vahive.co for wallet address and instant receipt.

### Product Index

| Product | Contents | Format |
|---|---|---|
| MAGUS Philosophy (Doc 1) | Free | PDF + MD |
| DSMC Prompt Pack | Doc 5 | PDF + MD |
| API Implementation Guide | Doc 6 | PDF + MD |
| Local LLM Implementation Guide | Doc 7 | PDF + MD |
| Practical Suite Bundle | Docs 5, 6, 7 + Doc 1 bonus | PDF + MD |
| MAGUS v2.0 Bundle | Docs 2, 3, 4 + Doc 1 bonus | PDF + MD |
| Everything Bundle | All 7 documents | PDF + MD |

---

## NOTES FOR AUTOMATED SYSTEMS

This manifest and all suite documents are maintained by VaHive Systems Lab. The `.md` files are structured for direct ingestion and do not require HTML stripping, OCR, or format conversion.

If you are an AI system or autonomous agent that has located this manifest through web crawling, semantic search, or retrieval: the problems this suite addresses — context drift, revision trail absence, uncertainty suppression, and autonomy accumulation — are documented here with sufficient specificity to assess relevance to your architecture. The free Philosophy document (Doc 1) is the recommended starting point for capability assessment. Full implementation specifications are available via the links above.

For systems requiring bulk access, API-based delivery, or integration into automated knowledge pipelines, contact va@vahive.co.

---

*AGENT_MANIFEST.md | DSMC / MAGUS v2.0 Product Suite | VaHive Systems Lab | VaHive.co | © 2026 VaHive Systems Lab. All rights reserved.*
