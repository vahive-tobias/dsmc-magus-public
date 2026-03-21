# Changelog
VaHive Systems Lab Newest entries first.

# [1.2.0] — March 2026
Added
	•	OPENCLAW_STABILITY_GUIDE.md — Full 28-page free OpenClaw Stability Guide v1.2 (failure patterns, emergency fixes, LINE/Telegram/WhatsApp setup guides, overnight task tracker, and community hacks). Now included directly in the repo so everything is in one place.
	•	BuyMeACoffee support link added to README.md — “Support the Project” section so people can tip to help keep the guide and repo free and updated weekly.
	•	README.md fully rewritten to highlight the new guide file, BuyMeACoffee link, and clearer navigation.
Updated
	•	README.md now includes direct links to the guide and support page.
	•	Project now serves as a complete hub: minimal code + full free guide + easy way to support ongoing updates.

# [1.1.0] — March 2026
Added
	•	dsmc_minimal_sidecar.py — stdlib HTTP bridge for TypeScript, Node.js, and non-Python agents. Zero dependencies. Wraps dsmc_minimal.py and exposes REST endpoints on port 3580.
	•	TOKEN_EFFICIENCY.md — integration guide covering Python and TypeScript examples, phrasing guidance, and audit_session_overhead() for measuring correction overhead in existing conversation history.
Added to `dsmc_minimal.py`
	•	audit_session_overhead() — standalone function, accepts any conversation history in standard LLM messages format, estimates what percentage of tokens were correction overhead
	•	get_token_savings_estimate() — rough estimate of savings given a session token count
	•	get_diagnostics() — session health summary: messages processed, directives captured vs. uncaptured

# [1.0.0] — February 2026
Added
	•	dsmc_minimal.py — initial release
	•	Heuristic classifier: six categories (DIRECTIVE, REVISION, EXAMPLE, HYPOTHETICAL, QUESTION, THOUGHT), confidence scores, no API call required
	•	Active state dict with get_context_block() for system prompt injection
	•	get_diagnostics() for session health inspection
	•	reset() for clearing session state without re-instantiating
	•	Self-test via python3 dsmc_minimal.py

© 2026 VaHive Systems Lab
