DSMC — Dual-State Multiversal Cognition
A lightweight governance layer for OpenClaw agents
VaHive Systems Lab | aivare.ai

What This Is
A zero-dependency Python implementation of DSMC — a governance pattern that addresses the structural stability problems affecting long-running OpenClaw agent sessions.
Maintain structured external state alongside the conversation, classify every incoming message before the agent acts on it, and inject a compact block of active decisions into every LLM call. The model always has the current ground truth — regardless of how long the session has been running or how much the context window has turned over.
Intentionally minimal. No databases, no dashboards, no external services. Just the core pattern in runnable form.

The Problem Being Solved
Long OpenClaw sessions degrade in predictable ways:
Context drift — Decisions established early gradually lose influence as the conversation grows. Revision failure — Corrections don’t reliably propagate. Example contamination — Statements made as illustrations get treated as instructions. Token overhead — Unmanaged sessions accumulate correction cycles that eat into productive work.
The fix for all four is the same: external state management with consistent injection. This repository implements that pattern at its simplest.

What’s in This Repo
dsmc_minimal.py — Core classifier and active state manager. Zero dependencies. Python 3.9+ stdlib only.
dsmc_minimal_sidecar.py — Stdlib HTTP server exposing the engine over localhost:3580 (for TypeScript/OpenClaw).
OPENCLAW_STABILITY_GUIDE.md — Full 28-page free guide (v1.2) with failure patterns, emergency fixes, LINE/Telegram/WhatsApp setup, overnight task tracker, and more.
TOKEN_EFFICIENCY.md — Technical write-up on correction cycle overhead.
All files are self-contained — no pip installs, no virtual environments, no configuration required.

Quick Start
Python agents: from dsmc_minimal import DSMCMinimal
dsmc = DSMCMinimal() dsmc.record(‘Use PostgreSQL’, ‘DIRECTIVE’, ‘database’, ‘postgresql’) dsmc.record(‘Change to MongoDB’, ‘REVISION’, ‘database’, ‘mongodb’)
context_block = dsmc.get_context_block() # Inject this into every LLM call
TypeScript / OpenClaw agents: python3 dsmc_minimal_sidecar.py # Runs on localhost:3580

Classification Categories
Every incoming statement is classified before the agent acts:
Category
Meaning
DIRECTIVE
Instruction to implement now
REVISION
Overrides a previous decision
THOUGHT
Brainstorming — not a commitment
EXAMPLE
Illustration only
HYPOTHETICAL
What-if exploration
QUESTION
Information request
Only DIRECTIVE and REVISION update active state.

Support the Project
If the guide or this repo has helped you, consider buying the maintainer a coffee. Every tip helps keep both the guide and the code 100% free and updated weekly.
☕ https://buymeacoffee.com/pui_titiya

Ready for Production?
This is the minimal, zero-dependency version. For full production governance (MAGUS Guardian with phone approvals, cryptographic allowlist, live dashboard, drift detection, etc.) check:
👉 DSMC Agent Engine v2.0 — https://puititiya.gumroad.com/l/dsmc-agent-engine

The Formal Architecture
The patterns here are a lightweight implementation of MAGUS v3.0 — the full governance specification published on Zenodo:
📄 https://doi.org/10.5281/zenodo.19013833

New to OpenClaw Agents?
Start with the full free guide included in this repo:
📖 OPENCLAW_STABILITY_GUIDE.md
It covers the four failure patterns, emergency recovery steps, LINE/Telegram/WhatsApp setup, overnight task tracking, and more — all written for non-developers.

Contributing
Issues and pull requests welcome. Found a classification edge case or a useful integration pattern? Open an issue or submit a PR.

Contact
Email: support@aivare.ai X: @propelaiva Website: https://aivare.ai
VaHive Systems Lab | Chiang Mai, Thailand | 2026
