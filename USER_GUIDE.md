# Trade Hunter — User Guide

**Last updated:** 2026-04-03

---

## Local startup

On Windows, use the repo-local launcher:

```powershell
.\trade-hunter.cmd
```

It runs the guarded single-instance startup path, so starting it again replaces the already-running local Trade Hunter instance on the configured port instead of piling up another server.

The launcher also forwards arguments to the app entrypoint:

```powershell
.\trade-hunter.cmd --smoke-test
```

On macOS/Linux, continue to use:

```bash
python -m app
```

---

## Operating modes

Trade Hunter runs in exactly **one** mode. Live and simulation are mutually exclusive.

| Mode | What runs | How to enable |
|---|---|---|
| **live** | Kalshi WebSocket feed | `ENABLE_KALSHI=true` in `.env` |
| **simulation** | Synthetic event generator | `ENABLE_SIMULATION=true` (default) |

When live mode is active, the simulation feed is suppressed entirely — no data, no pill in the dashboard. When you switch to live mode, set `ENABLE_SIMULATION=false` to be explicit.

---

## Kalshi ticker formats

Kalshi uses a three-level market hierarchy. Trade Hunter accepts all three levels and resolves them automatically at startup.

### Series slug
`KXBTC15M`

Resolves to the current open market in that recurring series. When one window closes and the next opens, restarting the app picks up the new one.

### Event ticker  
`KXTOPCHEF-26DEC31`

A single event that contains multiple outcome sub-markets (e.g. "who wins Top Chef — Sierra? Sheridan? Rhodes?"). Trade Hunter subscribes to **all** open sub-markets under the event, so the full event gets coverage.

### Specific market ticker
`KXBTC15M-26APR030145-45`

One exact contract. Use this when you want a specific window, not just the current one.

### Expired tickers
Tickers that 404 or have no open markets are detected at startup via the Kalshi REST API. The feed status detail reports `N active, M unresolved` — you can see exactly which slugs resolved and which didn't. `KXTRUMPSAY-25DEC08` is an example of a settled event that will never resolve.

### Adding and removing tickers live
You don't need to restart the app to change what you're tracking. Use the **Tracked Kalshi Tickers** panel on the dashboard or the API:

```bash
# Add
curl -X POST http://127.0.0.1:8765/api/kalshi/markets \
  -H "Content-Type: application/json" \
  -d '{"ticker": "KXBTC15M"}'

# Remove
curl -X POST http://127.0.0.1:8765/api/kalshi/markets/remove \
  -H "Content-Type: application/json" \
  -d '{"ticker": "KXBTC15M"}'
```

Changes persist to `.env` automatically (restart-safe).

---

## Discovering markets with Category Search

The **Category Search** panel lets you find active Kalshi markets without knowing the ticker in advance.

1. Type a category — `Crypto`, `Elections`, `Sports`, `World`, `Climate and Weather`, etc.
2. Click Search
3. Results show event titles with their series/event slugs
4. Click `+` on any result to add it to your tracked tickers immediately

Internally this calls `GET /api/kalshi/categories?q=<category>` which queries the Kalshi public `/events` endpoint.

---

## The 10-minute freshness window

In live mode, the dashboard only displays events that arrived in the last 10 minutes. Events older than that are stored in the database but hidden from the live panels.

**Why this exists:** Without it, stale rows from hours ago appear alongside fresh data and are indistinguishable at a glance.

**When panels appear empty in live mode:**
1. Look at the status pills — `last event: Xm ago` shows when the last event arrived
2. If it's within 10 minutes, data is flowing and the current markets are just quiet
3. Check `kalshi seen: Xm ago` — if unknown, the feed hasn't processed a ticker/trade message yet
4. Check the feed detail string in the status pills or via `/api/state`

---

## Reading the status pills

| Pill | Meaning |
|---|---|
| `MODE: LIVE` (teal) | Live mode active |
| `MODE: SIMULATION` | Simulation mode active |
| `WINDOW: 10M` | 10-minute freshness filter in effect |
| `LAST EVENT: Xm ago` | Age of the most recently stored event |
| `KALSHI SEEN: Xm ago` | Age of the last Kalshi message processed by your handler |
| `TICKERS: N` | Number of active subscriptions after resolution |
| `FRESHNESS: Xm` | Age of the most recent event visible in the flow |
| `DISCORD: DEFAULT WEBHOOK` | Discord configured, using default channel |
| `DISCORD: ACTIVE` | Discord configured with topic routing |
| `DISCORD: DISABLED` | No Discord webhook configured |
| `KALSHI-PYKALSHI: RUNNING` | Feed connected and receiving traffic |
| `POLYALERTHUB: RUNNING` | Relay endpoint active |

---

## Reading the feed status detail

The Kalshi feed reports a diagnostic string visible in the status pills and in `/api/state → feeds.kalshi-pykalshi.detail`:

```
44 subscriptions (5 configured, 1 unresolved) markets
(callback-startstop, ws_msgs:1298, since_last:21s,
 ticker:357 trade:886 lifecycle:48 handled:1243)
```

| Field | Meaning |
|---|---|
| `44 subscriptions` | Resolved market tickers actually subscribed |
| `5 configured` | Slugs in `KALSHI_MARKETS` |
| `1 unresolved` | Slugs with no open market found |
| `callback-startstop` | Feed API mode (start/stop with callbacks) |
| `ws_msgs` | Total WebSocket frames received (includes internal acks) |
| `since_last` | Seconds since last WebSocket frame |
| `ticker` | Ticker channel messages dispatched to handler |
| `trade` | Trade channel messages dispatched to handler |
| `lifecycle` | Market state-change probe events (confirms dispatch works) |
| `handled` | Total messages your handler processed |

**If `ws_msgs` is growing but `ticker=0, trade=0`:** The WebSocket connection is alive, but those markets are producing no price or trade events right now. The market may be quiet, halted, or near settlement.

**If `ws_msgs=0`:** The WebSocket connection isn't receiving anything. Check credentials and network.

---

## Live Trade Flow

Each row shows one event in a compact format:

```
T  KXBTC15M-26APR030215-15  0.997  vol 25  yes  ≈≈≈  fresh 0m
Q  KXBTC15M-26APR030215-15  0.996  vol 395k       ~~~  fresh 0m
```

| Element | Meaning |
|---|---|
| `T` (orange) | Trade — actual contract execution |
| `Q` (gray) | Quote — price/orderbook update |
| Market ID | Resolved ticker |
| Price | `yes_price` (0.00–1.00 = 0%–100%) |
| `vol N` | Volume for this event |
| `yes`/`no` | Taker side (trade events only) |
| Sparkline | Per-market yes_price trend over last 20 events |
| Age pill | How long ago this event arrived |

Identical consecutive events are collapsed with `×N`. The sparkline builds up over the first few refresh cycles.

---

## Recent Signals

The detector fires when a market shows unusual volume or price movement.

**Sort options:**
- **Newest** (default) — most recently detected signal first
- **Highest score** — strongest signal first regardless of time

**Latest per market toggle:**  
When on, shows only the single most recent signal per market ID. Useful when one market is firing repeatedly and you want one summary view per ticker rather than a list of duplicates. When off, all signals are shown in order.

**Inline analyst read:**
Each signal can also show an AI read with:
- `signal` / `noise` / `uncertain`
- direction (`yes`, `no`, or `unclear`)
- confidence (`low`, `medium`, `high`)
- plain-English rationale
- threshold note when the analyst sees a recurring false-positive pattern

Provider order:
1. **Anthropic Claude Haiku** (primary)
2. **Perplexity Sonar** (fallback)

If Anthropic fails or is unavailable, the app automatically tries Perplexity so analysis can still land.

**Signal tiers:**
| Tier | Score | Meaning |
|---|---|---|
| `watch` | ≥ 3.0 | Noticeable activity, worth monitoring |
| `notable` | ≥ 4.0 | Significant move, worth investigating |
| `high conviction flow` | ≥ 6.0 | Strong signal with multiple confirmations |

**Score formula:** `(volume_multiple × 0.75) + (price_score × 1.25)`

---

## Tuning Advisor

The tuning advisor is the second AI pass. Instead of reading one signal in isolation, it looks across recent **analyst-labelled** signals and suggests concrete detector changes to reduce false positives.

It returns:
- a short summary of the current false-positive pattern
- one **best next tweak**
- 2–3 concrete tuning recommendations

Examples:
- require minimum price movement before promoting a spike
- tighten rules for ultra-low-price or illiquid markets
- add directional coherence checks between trade flow and price movement

### Durable backlog
Advisor suggestions are not just ephemeral UI text. They are tracked in:

- `docs/TUNING-BACKLOG.md`

Use that file as the durable source of truth for:
- applied recommendations
- planned next tweaks
- rejected ideas
- superseded rules

---

## Spike detector tuning

| Setting | Default | Effect |
|---|---|---|
| `SPIKE_MIN_VOLUME_DELTA` | 120 | Minimum volume change to consider |
| `SPIKE_MIN_PRICE_MOVE` | 0.03 | Minimum price move (3%) |
| `SPIKE_SCORE_THRESHOLD` | 3.0 | Minimum score to fire an alert |
| `SPIKE_BASELINE_POINTS` | 24 | Events used for rolling baseline |
| `SPIKE_COOLDOWN_SECONDS` | 300 | Minimum time between repeat alerts per market |

Current planned tuning work is tracked in the roadmap milestone **M005** and in `docs/TUNING-BACKLOG.md`.

**Too many false positives:** raise `SPIKE_SCORE_THRESHOLD`, raise `SPIKE_MIN_PRICE_MOVE`, or implement one of the backlog heuristics for thin/flat-price markets  
**Missing moves:** lower `SPIKE_MIN_VOLUME_DELTA` (carefully) or lower `SPIKE_SCORE_THRESHOLD`  
**Too many duplicates:** raise `SPIKE_COOLDOWN_SECONDS` (try 600)

---

## Multiple server instances

Trade Hunter now treats the configured host/port as a single-instance local startup target. On Windows, use `trade-hunter.cmd` as the supported launcher. Starting it again will ask the already-running local Trade Hunter instance on that port to shut down cleanly before the new one starts.

If you still see alternating status strings in the feed detail (different ws_msgs counts on successive refreshes), there may be an older pre-guard instance or a manually started stray process outside the supported path. Kill all and start one clean:

```powershell
# Windows
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match "-m app" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
.\trade-hunter.cmd
```

```bash
# macOS / Linux
pkill -f "python -m app"
python -m app
```

---

## Troubleshooting

### Panels empty, all zeros

Check the status pills first:
- `last event: Xm ago` — if > 10m, freshness window is filtering everything out
- `kalshi seen: unknown` — feed hasn't processed a ticker/trade message
- Feed detail shows `N subscriptions ... ticker:0 trade:0` — markets are quiet

This is usually correct behavior, not a bug. The markets may have low activity.

### Feed shows "all configured tickers unresolved"

Every slug in `KALSHI_MARKETS` resolved to nothing. Causes:
- Using specific expired tickers (e.g. `KXTRUMPSAY-25DEC08`) — use the series slug `KXTRUMPSAY` instead
- Market has closed since you last configured it

Use Category Search to find active markets, or check https://kalshi.com/markets.

### No spike alerts appearing

Normal when markets are quiet. To verify the detector is working:
- Click **Trigger Demo Spike** in the dashboard (simulation mode) or `POST /api/demo/spike`
- If a signal appears, the detector is healthy — markets are just below threshold

### Discord not sending

Test the webhook directly:
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test from Trade Hunter"}'
```

If that works but Trade Hunter doesn't send, ensure `DISCORD_WEBHOOK_URL` is set in `.env` and the server was restarted after adding it.

---

## API quick reference

```bash
# Dashboard state (activity, signals, markets, feeds, telemetry)
curl http://127.0.0.1:8765/api/state

# Feed health
curl http://127.0.0.1:8765/api/health

# Tracked tickers
curl http://127.0.0.1:8765/api/kalshi/markets

# Category search
curl "http://127.0.0.1:8765/api/kalshi/categories?q=Crypto&limit=20"

# Add ticker
curl -X POST http://127.0.0.1:8765/api/kalshi/markets \
  -H "Content-Type: application/json" \
  -d '{"ticker": "KXBTC15M"}'

# Remove ticker
curl -X POST http://127.0.0.1:8765/api/kalshi/markets/remove \
  -H "Content-Type: application/json" \
  -d '{"ticker": "KXBTC15M"}'

# Ingest custom event
curl -X POST http://127.0.0.1:8765/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INGEST_API_TOKEN" \
  -d '{"source":"custom","platform":"polymarket","market_id":"m1","title":"Test","yes_price":0.55,"volume":1000}'
```

---

## Database

SQLite at `trade_hunter.db`. Survives restarts. Schema:

| Table | Contents |
|---|---|
| `events` | All ingested market events |
| `markets` | Latest state per market ID |
| `signals` | Detected spike alerts |
| `feed_status` | Feed health snapshots |

Automatic cleanup runs every 24 hours, keeping `RETENTION_DAYS` (default 7) of history.

Manual cleanup:
```python
from app.retention import cleanup_old_events
cleanup_old_events(None, retention_days=7)
```

Back up before major changes:
```bash
cp trade_hunter.db trade_hunter.db.bak-$(date +%Y%m%d)
```
