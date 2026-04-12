# Project History

This archive is the durable memory of what agents changed, why they changed it, and what the project impact was. Review it before revisiting a feature area.

## Continue recent repo work

- Session: session-2026-04-12T18-16-52-040Z
- Agent: unknown
- Status: handed_off
- When: 2026-04-12T22:48:33.365Z
- Goal: M010: Cross-Platform Whale Flow (Polymarket & Kalshi)
- Summary: Detected branch switch; review the new branch context.
- Work done:
- Unified terminology to WHALE/SIGNAL/NOTABLE/WATCH
- Hardened landing page hero card
- Styled all tiers in dashboard.css
- Synchronized app settings table
- Deployed to GitHub Pages
- Why it mattered:
- Truth-first transparency achieved
- Institutional-grade UI established
- Terminology consistency across all layers
- Hardened marketing page for commercial launch
- Regression risks:
- High flow/Conviction legacy terms
- Top signal strip (wmn-strip) hallucinations
- Mismatched tier names between detector and UI
- Non-commercial terminology leaking into commercial builds
- References:
- .holistic/context/regression-watch.md
- docs/index.html
- app/static/index.html
- app/detector.py

## Continue recent repo work

- Session: session-2026-04-04T00-43-40-475Z
- Agent: unknown
- Status: handed_off
- When: 2026-04-12T18:02:47.834Z
- Goal: Continue work around .bg-shell/manifest.json, .gitattributes, .pytest_cache/v/cache/nodeids
- Summary: Detected branch switch; review the new branch context.
- Work done:
- Implemented Admin Token Auth
- CSRF Protection
- .env Injection Prevention
- Safe Port-Kill
- Ticker Validation
- Automated Security Tests
- Why it mattered:
- Significantly higher security posture
- Blocked potential RCE and data poisoning
- Improved operational stability
- Regression risks:
- Ensure ADMIN_TOKEN and INGEST_API_TOKEN remain correctly configured in .env
- Maintain same-origin check
- References:
- ROADMAP.md
- .antigravity_session/walkthrough.md
- scripts/run_checks.py

