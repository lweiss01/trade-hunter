# History - trade-hunter

_Append-only log of every Holistic session. Newest entries at the bottom._

---
## Session `session-2026-04-04T00-43-40-475Z` | 2026-04-12T18:02:47.834Z | unknown

**Branch:** `detached`  
**Status:** handed_off  
**Goal:** Continue work around .bg-shell/manifest.json, .gitattributes, .pytest_cache/v/cache/nodeids  
**Checkpoints:** 17

**Work done:**
✅ Implemented Admin Token Auth
✅ CSRF Protection
✅ .env Injection Prevention
✅ Safe Port-Kill
✅ Ticker Validation
✅ Automated Security Tests

**Recommended next steps:**
- M010: Cross-Platform Whale Flow (Polymarket & Kalshi)

**Files changed:**
- `.gitattributes`
- `ROADMAP.md`
- `app/__main__.py`
- `app/config.py`
- `app/server.py`
- `app/service.py`
- `docs/TUNING-BACKLOG.md`
- `scripts/run_checks.py`
- `tests/test_security_hardening.py`

---

## Session `session-2026-04-12T18-16-52-040Z` | 2026-04-12T22:48:33.365Z | unknown

**Branch:** `main`  
**Status:** handed_off  
**Goal:** M010: Cross-Platform Whale Flow (Polymarket & Kalshi)  
**Checkpoints:** 3

**Work done:**
✅ Unified terminology to WHALE/SIGNAL/NOTABLE/WATCH
✅ Hardened landing page hero card
✅ Styled all tiers in dashboard.css
✅ Synchronized app settings table
✅ Deployed to GitHub Pages

**Recommended next steps:**
- Initiate M017 (Distribution & Licensing) to automate the build-time separation of Public (Simulation) and Commercial (Live) editions using scripts/distribute.py.
- M010: Cross-Platform Whale Flow (Polymarket & Kalshi)

---

## Session `session-2026-04-12T22-51-57-338Z` | 2026-04-13T00:11:53.461Z | unknown

**Branch:** `main`  
**Status:** handed_off  
**Goal:** Initiate M017 (Distribution & Licensing) to automate the build-time separation of Public (Simulation) and Commercial (Live) editions using scripts/distribute.py.  
**Checkpoints:** 1

**Work done:**
✅ Hardened and Unified 4-Tier Signal Standard (WHALE CLUSTER, SIGNAL, NOTABLE, WATCH)
✅ Fixed distribute.py permission issues
✅ Successfully deployed hardened landing page to tradehunter.site
✅ Verified live site status and site cache clearance.

**Recommended next steps:**
- Proceed with M017 (Distribution & Licensing) to automate the build-time separation of Public vs Commercial editions.

---

## Session `session-2026-04-13T00-26-28-982Z` | 2026-04-13T01:45:35.452Z | unknown

**Branch:** `main`  
**Status:** handed_off  
**Goal:** Proceed with M017 (Distribution & Licensing) to automate the build-time separation of Public vs Commercial editions.  
**Checkpoints:** 10

**Work done:**
✅ Delivered Zero-Flicker Institutional Gold Master (v0.2.7.1).
✅ Suppressed all terminal windows via Atomic Launcher hiding and CREATE_NO_WINDOW subprocess flags.
✅ Resolved CSRF-induced 'Read Only' states and synchronized all branding to v0.2.7.1.

**Recommended next steps:**
- 1. Create Inno Setup script for one-click installer. 2. Finalize marketing assets for Gumroad launch. 3. Monitor for any IPv6-specific socket collisions in edge cases.

**Files changed:**
- `app/__main__.py`
- `app/server.py`
- `app/static/index.html`
- `launcher.py`
- `trade-hunter.exe`
- `trade-hunter.spec`

---

## Session `session-2026-04-13T01-57-19-170Z` | 2026-04-13T02:13:47.103Z | unknown

**Branch:** `main`  
**Status:** handed_off  
**Goal:** 1. Create Inno Setup script for one-click installer. 2. Finalize marketing assets for Gumroad launch. 3. Monitor for any IPv6-specific socket collisions in edge cases.  
**Checkpoints:** 2

**Work done:**
✅ Project-aware pathing in config.py
✅ v0.2.7.5 binary build
✅ security token auto-generation

**Recommended next steps:**
- Investigate runtime DATA_ROOT resolution and frontend conditional rendering for settings sections.

**Files changed:**
- `trade-hunter-v0275.exe`

---

## Session `session-2026-05-06T03-26-00-097Z` | 2026-05-08T02:43:24.501Z | cursor

**Branch:** `main`  
**Status:** handed_off  
**Goal:** Execute GSD Phase 1 (packaged runtime reliability) and verify DATA_ROOT, persistence, and settings-section rendering for frozen builds.  
**Checkpoints:** 14

**Work done:**
✅ Created GSD phase directories 01-05 with README index
✅ Moved research docs into phase 01 and 02 as RESEARCH-*.md
✅ Added .planning/research/README.md resolver and updated cross-links

**Recommended next steps:**
- $gsd-discuss-phase 1
- $gsd-plan-phase 1

---

## Session `session-2026-05-09T19-30-18-667Z` | 2026-07-07T19:37:22.424Z | unknown

**Branch:** `main`  
**Status:** active  
**Goal:** $gsd-discuss-phase 1  
**Checkpoints:** 27

**Files changed:**
- `docs/TUNING-BACKLOG.md`

---

## Release summary: v0.3.1 — audit remediation, field-testing fixes & data safety

_26 commits ahead of `origin/main` (from `beb7a47` … `9df80f7`), covering the
end of the 6-phase audit plus the v0.3.1 field-testing round. Newest first.
NOTE: this curated block lives below the Holistic session log; regenerate it
from git if a checkpoint/handoff rewrites the file._

### Data safety — never lose the user's markets (the headline fix)
- **`9df80f7`** Isolate config paths in tests via a session-scoped autouse
  fixture (`tests/conftest.py`) — root cause of the recurring "my saved markets
  vanished after an update" bug. The security suite POSTs to
  `/api/kalshi/markets/remove` against a live server, and tuning tests apply
  rulesets; both resolved write-paths from the real `config.ENV_PATH`, so a
  plain `pytest` run silently emptied the real `data/watchlist.json` (and
  previously the legacy `.env`). Caught with an instrumented stack trace.
- **`7e40c21`** Self-healing watchlist: an empty/missing `data/watchlist.json`
  re-seeds from `.env` instead of treating "empty" as authoritative.
- **`d6fd4cf`** Decouple the watchlist from `.env` into `data/watchlist.json`
  (atomic writes, one-time migration deduping active + legacy `.env`); fix the
  empty-value legacy-`.env` shadow bug where `os.environ.setdefault` let an
  empty active value hide the real value on frozen builds.

### Live-feed & analyst accuracy correctness
- **`f00e39a`** Resolver: Kalshi settles as `finalized`/`determined`, not
  `settled` — fixes "0 outcomes captured" (85 of 160 markets now resolve).
- **`cf4cf35`** Kalshi ticker volume: cumulative → true per-market delta (3.1).
- **`b10e9a2`** Live-feed accuracy fixes and volume probe (3.1–3.3).
- **`bd3c05f`** Fix inverted price trend in the analyst prompt.
- **`beb7a47`** Fix analyst min-confidence setting persisting to the wrong env key.
- **`1ba2506`** Throttle tuning-advisor runs and dedupe identical snapshots.

### UI / settings-page polish (v0.3.1 field testing)
- **`f8b77e7`** Disambiguate the analyst verdict ("AI: real") from the `signal`
  tier pill on cards.
- **`0c5a8e8`** Fix signal-tier pill colors (signal + cross-venue divergence),
  including the slugify fix for the space-containing class name.
- **`6c828ab`** Fix settings status blocks not matching section content indent.
- **`974a3aa`** Fix settings-page padding/alignment (support detail, ruleset, eval).
- **`0447136`** Fix v0.3.1 field-testing bugs: footer version, `/api/state` perf
  (composite index `(market_id, timestamp DESC)`, 2.3s→0.8s), feed writes.
- **`ffb3ffc`** Fix dead `/api/ruleset` endpoint by serving it as a GET route.

### Audit phases & hardening
- **`c275471`** Bump version to v0.3.1.
- **`78e6f7f`** Phase 6 robustness/performance fixes (6.1–6.3, 6.7).
- **`3ee459f`** Add analyst-accuracy evaluation integration (Phase 5).
- **`b59b271`** Make version a single edit; de-version the single-instance mutex.
- **`79084f4`** Fix public-build `.env.example` loss; single-source version (4.1–4.2).
- **`48dbdf9`** Harden origin checks and token handling (2.1–2.3).
- **`6553096`** Harden detector, feed, and ingest paths (1.6–1.9).
- **`12ea984`** Compact `TUNING-BACKLOG.md`: dedupe rejected proposals (6.8).
- **`7514533`** Add explicit discard step to audit item 6.8.
- **`402c488`** Mark audit item 1.4 done; split backlog cleanup to item 6.8.
- **`e4ac90b`** Rewrite corrupted `.gitignore`; track `status.py` eval monitor.

### Housekeeping
- Added `data/watchlist.json` and `.repo-report/` to `.gitignore` (both are
  local-only; watchlist is per-user runtime state).
- Rebuilt `dist/trade-hunter-v0.3.1.exe` with the self-healing watchlist fix;
  full test suite green (312 passing).

