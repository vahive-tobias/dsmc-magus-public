# Changelog

**VaHive Systems Lab**  
Newest entries first.

---

## [1.1.0] — March 2026

### Added
- `dsmc_minimal_sidecar.py` — stdlib HTTP bridge for TypeScript, Node.js, and non-Python agents. Zero dependencies. Wraps `dsmc_minimal.py` and exposes REST endpoints on port 3580.
- `TOKEN_EFFICIENCY.md` — integration guide covering Python and TypeScript examples, phrasing guidance, and `audit_session_overhead()` for measuring correction overhead in existing conversation history.

### Added to `dsmc_minimal.py`
- `audit_session_overhead()` — standalone function, accepts any conversation history in standard LLM messages format, estimates what percentage of tokens were correction overhead
- `get_token_savings_estimate()` — rough estimate of savings given a session token count
- `get_diagnostics()` — session health summary: messages processed, directives captured vs. uncaptured

---

## [1.0.0] — February 2026

### Added
- `dsmc_minimal.py` — initial release
- Heuristic classifier: six categories (DIRECTIVE, REVISION, EXAMPLE, HYPOTHETICAL, QUESTION, THOUGHT), confidence scores, no API call required
- Active state dict with `get_context_block()` for system prompt injection
- `get_diagnostics()` for session health inspection
- `reset()` for clearing session state without re-instantiating
- Self-test via `python3 dsmc_minimal.py`

---

*© 2026 VaHive Systems Lab*
