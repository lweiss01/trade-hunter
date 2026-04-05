# Trade Hunter

A real-time prediction market monitoring dashboard. Subscribes to live Kalshi WebSocket feeds, detects unusual price and volume activity, and surfaces high-conviction signals for review.

**This app is informational only. It does not place trades.**

---

## What it does

- Live WebSocket subscription to Kalshi markets with automatic series/event resolution
- Custom spike detector with per-market rolling baselines and cooldown
- **Per-signal AI analyst** that labels spikes as `signal`, `noise`, or `uncertain`
- **Tuning advisor** that looks across analysed signals and suggests threshold changes
- Discord webhook notifications on confirmed signals
- PolyAlertHub relay endpoint for third-party alert ingestion
- SQLite persistence — data survives restarts
- Local dashboard at `http://127.0.0.1:8765`

---

## Quick start

```bash
# Windows
.\trade-hunter.cmd

# macOS / Linux
python -m app
```

Open `http://127.0.0.1:8765`.

On Windows, `trade-hunter.cmd` is the repo-supported launcher and uses the guarded single-instance startup path for you.

If Trade Hunter is already running on the configured port, starting it again now requests a scoped shutdown of the old local instance and replaces it with one clean server.

With `ENABLE_SIMULATION=true` (the default), the dashboard fills with synthetic data immediately. No credentials needed.

### Windows launcher

Use the repo-local launcher for normal local work:

```powershell
.\trade-hunter.cmd
```

The launcher forwards arguments to the app entrypoint, so smoke tests still work:

```powershell
.\trade-hunter.cmd --smoke-test
```

Use `py -m app` only if you intentionally need the raw module entrypoint.

---

## Kalshi live feed

Install the feed package:

```bash
py -m pip install .[integrations]
```

Add credentials to `.env`:

```env
ENABLE_KALSHI=true
ENABLE_SIMULATION=false
KALSHI_API_KEY_ID=your-key-id
KALSHI_PRIVATE_KEY_PATH=C:\path\to\kalshi.key
KALSHI_MARKETS=KXBTC15M,KXTOPCHEF-26DEC31,KXTRUMPSAY
```

`KALSHI_MARKETS` accepts three kinds of identifiers — all auto-resolve at startup:

| Type | Example | Resolves to |
|---|---|---|
| Series slug | `KXBTC15M` | Current open market in that series |
| Event ticker | `KXTOPCHEF-26DEC31` | All open sub-markets for that event |
| Specific ticker | `KXBTC15M-26APR030145-45` | That exact contract |

Expired or closed tickers are detected and skipped automatically. The feed status detail in the dashboard shows `N active, M unresolved` so you know what's live.

**Live mode and simulation are mutually exclusive.** When `ENABLE_KALSHI=true`, simulation is suppressed entirely.

---

## Dashboard

The dashboard updates every 3 seconds and shows:

- **Status pills** — mode, freshness window, last event age, Kalshi message counters, ticker count
- **Recent Signals** — spike alerts from the detector, sortable by newest or score, with inline analyst reads
- **Tuning Advisor** — aggregate false-positive pattern analysis and next-step threshold suggestions
- **Live Trade Flow** — compact chronological event stream with T/Q kind badges, prices, volumes, trade sides, and per-market sparklines
- **Market Tape** — latest state per market within the freshness window
- **Tracked Kalshi Tickers** — add/remove tickers live without restarting
- **Category Search** — discover Kalshi markets by category (Crypto, Elections, Sports, etc.) and add them with one click

**Freshness window:** In live mode, only events from the last 10 minutes appear. If panels are empty, the status pills show when the last event arrived and whether the feed is receiving WebSocket traffic.

---

## AI analyst and tuning advisor

Trade Hunter can optionally use cloud LLMs to reduce false positives and help interpret flow.

### Per-signal analyst
When a new spike fires, the analyst reviews:
- current yes price / implied probability
- volume spike vs baseline
- recent price history and trade-side mix
- whether the move looks informed, mechanical, or ambiguous

It returns:
- `noise_or_signal`
- `direction`
- `confidence`
- plain-English rationale
- a one-line detector tuning note

The dashboard shows this inline on each signal card.

### Tuning advisor
A second pass looks across recent analyst-labelled signals and suggests threshold changes to reduce recurring false positives.

Its recommendations are shown in the **Tuning Advisor** panel and also written to the durable backlog file:

- `docs/TUNING-BACKLOG.md`

Use that file as the source of truth for what was suggested, what was applied, and what is still planned.

### Provider order
The analyst stack supports provider fallback:
1. **Anthropic Claude Haiku** (primary)
2. **Perplexity Sonar** (fallback)

If Anthropic is unavailable, Trade Hunter automatically tries Perplexity instead.


```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_ALERT_MODE=all
DISCORD_ANALYST_FOLLOWUP=true
DISCORD_ANALYST_MIN_CONFIDENCE=medium
```

Route different market topics to different channels:

```env
DISCORD_WEBHOOK_ROUTES=crypto=https://...,elections=https://...
```

Discord alert modes:

- `all` — send the detector alert immediately and, when enabled, send an analyst follow-up later
- `detector-only` — send only the immediate detector alert
- `analyst-signals-only` — suppress the raw detector alert and notify Discord only when the analyst labels the spike as a `signal`

`DISCORD_ANALYST_MIN_CONFIDENCE` applies to `analyst-signals-only` mode and accepts `low`, `medium`, or `high`.

---

## PolyAlertHub relay

```env
POLYALERTHUB_TOKEN=your-token
```

Configure PolyAlertHub to POST to:

```
POST http://your-host:8765/api/alerts/polyalerthub
Authorization: Bearer your-token
```

---

## Custom event ingestion

```bash
curl -X POST http://127.0.0.1:8765/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INGEST_API_TOKEN" \
  -d '{
    "source": "my-scraper",
    "platform": "polymarket",
    "market_id": "will-fed-cut-june",
    "title": "Will the Fed cut rates in June?",
    "yes_price": 0.58,
    "volume": 1450
  }'
```

Set `INGEST_API_TOKEN` in `.env` to require authentication. Omit the header to allow unauthenticated ingestion.

---

## Spike detector

Fires when a market shows unusual volume or price movement relative to its recent baseline.

**Score formula:** `(volume_multiple × 0.75) + (price_score × 1.25)`

| Tier | Condition |
|---|---|
| `watch` | Score ≥ 3.0 |
| `notable` | Score ≥ 4.0 |
| `high conviction flow` | Score ≥ 6.0, price ≥ 1.75× threshold, volume ≥ 3× baseline |

Tuning knobs in `.env`:

```env
SPIKE_MIN_VOLUME_DELTA=120    # minimum volume change to consider
SPIKE_MIN_PRICE_MOVE=0.03     # minimum price move (3%)
SPIKE_SCORE_THRESHOLD=3.0     # alert threshold
SPIKE_BASELINE_POINTS=24      # rolling baseline window
SPIKE_COOLDOWN_SECONDS=300    # minimum gap between duplicate alerts
```

---

## Smoke test

```bash
py -m app --smoke-test
```

Injects synthetic events and confirms the detector produces a signal. Safe to run without credentials.

---

## API reference

```
GET  /api/state                          full dashboard state
GET  /api/health                         feed health + retention status
GET  /api/kalshi/markets                 tracked tickers
GET  /api/kalshi/categories?q=Crypto     search markets by category
POST /api/kalshi/markets                 add ticker  { "ticker": "KXBTC15M" }
POST /api/kalshi/markets/remove          remove ticker
POST /api/events                         ingest custom event
POST /api/alerts/polyalerthub            PolyAlertHub relay endpoint
POST /api/demo/spike                     trigger a demo signal
```

---

## Configuration reference

| Variable | Default | Description |
|---|---|---|
| `APP_HOST` | `127.0.0.1` | Dashboard bind address |
| `APP_PORT` | `8765` | Dashboard port |
| `ACTIVE_MODE` | (derived) | `live` or `simulation` |
| `ENABLE_SIMULATION` | `true` | Synthetic data feed |
| `ENABLE_KALSHI` | `false` | Live Kalshi WebSocket feed |
| `KALSHI_API_KEY_ID` | — | Kalshi API key ID |
| `KALSHI_PRIVATE_KEY_PATH` | — | Path to Kalshi private key |
| `KALSHI_MARKETS` | — | Comma-separated tickers/slugs |
| `POLYALERTHUB_TOKEN` | — | PolyAlertHub auth token |
| `INGEST_API_TOKEN` | — | Generic ingest endpoint auth |
| `ANTHROPIC_API_KEY` | — | Enables the signal analyst (primary provider) |
| `PERPLEXITY_API_KEY` | — | Enables analyst fallback and tuning-advisor provider |
| `DISCORD_WEBHOOK_URL` | — | Default Discord webhook |
| `DISCORD_WEBHOOK_ROUTES` | — | Topic-routed webhooks (key=url;...) |
| `DISCORD_ALERT_MODE` | `all` | `all`, `detector-only`, or `analyst-signals-only` Discord delivery policy |
| `DISCORD_ANALYST_FOLLOWUP` | `true` | When `DISCORD_ALERT_MODE=all`, send a second Discord message after analyst completion |
| `DISCORD_ANALYST_MIN_CONFIDENCE` | `medium` | Minimum analyst confidence for `analyst-signals-only` alerts (`low`/`medium`/`high`) |
| `SPIKE_MIN_VOLUME_DELTA` | `120` | Detector volume threshold |
| `SPIKE_MIN_PRICE_MOVE` | `0.03` | Detector price threshold |
| `SPIKE_SCORE_THRESHOLD` | `3.0` | Alert score cutoff |
| `SPIKE_BASELINE_POINTS` | `24` | Baseline rolling window |
| `SPIKE_COOLDOWN_SECONDS` | `300` | Duplicate alert suppression |
| `RETENTION_DAYS` | `7` | Database retention window |
| `QUIET_MODE` | `false` | Suppress console output |

---

## Project layout

```
app/
  __main__.py          entry point
  config.py            settings + .env loader
  service.py           orchestration, ingest, dashboard state
  server.py            HTTP server + API routes
  store.py             SQLite-backed event/signal store
  analyst.py           per-signal analyst + aggregate tuning advisor
  detector.py          spike detection algorithm
  notifiers.py         Discord webhook notifier
  retention.py         automated DB cleanup
  models.py            MarketEvent, SpikeSignal dataclasses
  feeds/
    base.py            FeedAdapter base class
    kalshi_pykalshi.py Kalshi WebSocket adapter (pykalshi)
    simulated.py       synthetic event generator
  static/
    index.html         dashboard shell
    dashboard.js       live polling, rendering, sparklines
    dashboard.css      Command Center-inspired palette
tests/                 pytest suite (63 tests)
```
