# Regression Watch

Use this before changing existing behavior. It is the short list of fixes and outcomes that future agents should preserve.

## Continue recent repo work

- Goal: M010: Cross-Platform Whale Flow (Polymarket & Kalshi)
- Durable changes:
- Unified terminology to WHALE/SIGNAL/NOTABLE/WATCH
- Hardened landing page hero card
- Styled all tiers in dashboard.css
- Synchronized app settings table
- Deployed to GitHub Pages
- Why this matters:
- Truth-first transparency achieved
- Institutional-grade UI established
- Terminology consistency across all layers
- Hardened marketing page for commercial launch
- Do not regress:
- High flow/Conviction legacy terms
- Top signal strip (wmn-strip) hallucinations
- Mismatched tier names between detector and UI
- Non-commercial terminology leaking into commercial builds
- Source session: session-2026-04-12T18-16-52-040Z

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

