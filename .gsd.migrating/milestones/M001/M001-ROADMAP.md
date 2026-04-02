# M001: 

## Vision
Replace simulation data with live Kalshi WebSocket stream, PolyAlertHub relay, and SQLite persistence. By the end of this milestone, the dashboard will show real market activity from multiple sources with durable history.

## Slice Overview
| ID | Slice | Risk | Depends | Done | After this |
|----|-------|------|---------|------|------------|
| S01 | Kalshi Live WebSocket Stream | medium | — | ⬜ | Dashboard shows live Kalshi markets with ticker and trade updates. Feed status shows connection state, last event timestamp, and error count. |
| S02 | PolyAlertHub Relay Endpoint | low | S01 | ⬜ | POST /api/alerts/polyalerthub accepts PolyAlertHub payloads, transforms them into MarketEvent, and persists to store. Dashboard shows polyalerthub events in activity stream. |
| S03 | SQLite Persistence Layer | medium | S01, S02 | ⬜ | App restart preserves event history and detector state. SQLite database contains events, signals, and feed health records with retention policy. |
