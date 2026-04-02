# trade-hunter

## What this project is

Trade Hunter is a local decision-support tool for prediction market traders. It monitors multiple venues (Kalshi, Polymarket) for unusual market activity — volume spikes, price moves, cross-platform divergences — and surfaces them with clear explanations so a solo retail trader can decide whether something deserves deeper investigation.

The app is conservative about automation. It does not execute trades. It surfaces signal, explains context, and makes the next research step obvious.

## Current state

**MVP complete** — functional foundation with no production data yet.

Built and working locally:
- Local web dashboard at `http://127.0.0.1:8765`
- In-memory event store (markets, recent events, spike signals, feed health)
- Spike detector using rolling baselines for volume delta and price movement
- Generic `POST /api/events` ingest endpoint
- PolyAlertHub-compatible ingest alias at `POST /api/alerts/polyalerthub`
- Optional `pykalshi` WebSocket adapter (not yet connected to live data)
- Discord webhook notification path
- Simulation feed for local testing

**Not yet connected:**
- No live Kalshi stream
- No PolyAlertHub relay
- No SQLite persistence (all state resets on restart)
- No cross-platform market matching
- No spread/divergence monitoring
- No watchlists or filters

## Goals

Build a practical research assistant for a small retail trader on Kalshi with awareness of Polymarket for comparison context.

**Success looks like:**
- Low false-positive alert rate (signals worth reading)
- Cross-platform divergence detection (find pricing disagreements)
- Explainable alerts (understand why a move is flagged)
- Actionable workflow (not just data, but what to check next)
- Discord-first awareness (don't need to keep dashboard open)
- Historical feedback (learn which signals were useful)

**Constraints:**
- Solo trader, small account, part-time availability
- Kalshi-first for execution, Polymarket-aware for context
- Prefer simple explainable rules over black-box scoring
- No automated execution — observational tooling only
