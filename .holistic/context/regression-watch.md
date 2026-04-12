# Regression Watch

Use this before changing existing behavior. It is the short list of fixes and outcomes that future agents should preserve.

## Continue recent repo work

- Goal: Continue work around .bg-shell/manifest.json, .gitattributes, .pytest_cache/v/cache/nodeids
- Durable changes:
- Implemented Admin Token Auth
- CSRF Protection
- .env Injection Prevention
- Safe Port-Kill
- Ticker Validation
- Automated Security Tests
- Why this matters:
- Significantly higher security posture
- Blocked potential RCE and data poisoning
- Improved operational stability
- Do not regress:
- Ensure ADMIN_TOKEN and INGEST_API_TOKEN remain correctly configured in .env
- Maintain same-origin check
- Source session: session-2026-04-04T00-43-40-475Z

