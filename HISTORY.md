# Trade Hunter — Changelog

---

## v0.2.8 — 2026-06-06

**Kalshi Multi-Tier Ticker Architecture**

The biggest feed upgrade since launch. Trade Hunter now correctly handles Kalshi's three-tier market hierarchy — Series, Event, and Market — so broad parent tickers like `KXFED` or `KXTRUMPPARDONS` resolve to all their active child contracts automatically instead of returning 404 and being marked invalid.

**What changed:**

- Series tickers (e.g. `KXFED`) fan out to all open rate-decision contracts across every upcoming Fed meeting — 100 markets from a single configured slug
- Event tickers (e.g. `KXTRUMPPARDONS-29JAN21`) resolve to all open outcome sub-markets under that event
- `closed` markets (past close time, awaiting settlement) are now tracked alongside `open` ones
- Settled markets are automatically excluded — no manual cleanup needed
- Parent ticker association stored in the database; dashboard shows child count per parent (e.g. "KXFED (100 markets)")
- `kalshi_market_hierarchy` exposed in the dashboard API for UI grouping
- Kalshi private key path now resolved relative to the data directory, not the working directory — exe works from any location

**Build system:**

- `scripts/build_release.py` — single command builds commercial exe, sim exe, and commercial zip in the correct order
- Commercial zip (`trade-hunter-v0280-commercial.zip`) ready to upload to Gumroad
- Simulation edition (`trade-hunter-v0280-sim.exe`) — full double-click experience, simulation mode only, free distribution
- Both exes built from clean source trees with dev junk stripped

**Bug fixes:**

- Fixed launcher startup diagnostic sanitizer — sensitive values after `token=` and `webhook=` were not fully redacted
- Fixed detector tier label (`high conviction flow` → `signal`) to match live code and avoid invalid CSS class names
- Dashboard footer links updated to point to GitHub docs (Roadmap, Changelog, User Guide)
- Version display updated throughout (v0.2.7 → v0.2.8)

---

## v0.2.7.5 — 2026-04-13

**Distribution & Security**

- Automated public/commercial edition separation via `scripts/distribute.py`
- Security token auto-generation (ADMIN_TOKEN, INGEST_API_TOKEN) on first launch
- Project-aware data root pathing for frozen (PyInstaller) builds
- Zero-flicker atomic launcher — hides console window before any Python imports
- Single-instance mutex (`TradeHunter_v027_Atomic`) prevents duplicate server launches

---

## v0.2.7.1 — 2026-04-12

**Institutional Gold Master**

- Suppressed all terminal windows via atomic launcher and `CREATE_NO_WINDOW` subprocess flags
- Resolved CSRF-induced read-only Settings states
- Unified branding to v0.2.7.1 throughout dashboard

---

## v0.2.7 — 2026-04-12

**Security Hardening (M014–M016)**

- Admin token authentication for all state-changing endpoints
- CSRF origin validation
- `.env` injection prevention
- Safe port-kill on restart
- Ticker format validation (alphanumeric + dashes, max 64 chars)
- Full security regression test suite

---

## v0.2.6 and earlier

- PolyAlertHub ingest endpoint with Bearer auth
- Dual AI signal analyst (Anthropic Claude primary, Perplexity fallback)
- Autonomous tuning advisor + governor safety layer
- Whale cluster detection (Poisson p < 0.01 on 99th-percentile trade clusters)
- 4-tier signal classification: `watch`, `notable`, `signal`, `whale-cluster`
- Discord webhook routing by topic (crypto, elections, macro, sports, geopolitics)
- SQLite persistence with 7-day rolling retention
- 10-minute freshness window in live mode
- Simulation feed for local testing without API credentials
- Category search for discovering active Kalshi markets
