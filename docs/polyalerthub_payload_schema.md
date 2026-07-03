# PolyAlertHub Webhook Payload Schema

## Overview

This document specifies the expected payload format for webhooks sent by PolyAlertHub to the Trade Hunter `/api/alerts/polyalerthub` endpoint.

PolyAlertHub is a third-party alert service that monitors Polymarket and other prediction markets for price movements, whale trades, trader positions, and market events. When an alert condition triggers, PolyAlertHub sends a webhook to configured endpoints.

## Webhook Delivery

**Method:** `POST`  
**Content-Type:** `application/json`  
**Endpoint:** `/api/alerts/polyalerthub`

### Authentication (Optional)

If `POLYALERTHUB_TOKEN` is configured in `.env`, PolyAlertHub should include:

```
Authorization: Bearer {token}
```

Requests without valid auth when a token is configured will receive `401 Unauthorized`.

## Payload Structure

The webhook payload is a JSON object representing a market event. Fields align with the Trade Hunter `MarketEvent` model.

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `platform` | string | Source platform for the market | `"polymarket"`, `"kalshi"`, `"predictit"` |
| `market_id` | string | Unique market identifier on the platform | `"will-fed-cut-rates-in-june"` |
| `title` | string | Human-readable market title | `"Will the Fed cut rates in June?"` |

### Optional Fields

| Field | Type | Description | Example | Default |
|-------|------|-------------|---------|---------|
| `alert_type` | string | Type of alert that triggered the webhook | `"price_alert"`, `"whale_trade"`, `"trader_position"`, `"market_event"` | — |
| `yes_price` | number | Current probability/price for YES outcome (0.0-1.0) | `0.58` | — |
| `no_price` | number | Current probability/price for NO outcome (0.0-1.0) | `0.42` | — |
| `volume` | number | Trading volume associated with the event | `1450` | — |
| `volume_kind` | string | Whether volume is cumulative or delta | `"cumulative"`, `"delta"` | `"delta"` |
| `event_kind` | string | Type of market event | `"quote"`, `"trade"`, `"alert"` | `"alert"` |
| `trade_size` | number | Size of the specific trade (for whale_trade alerts) | `5000` | — |
| `trade_side` | string | Trade direction | `"buy"`, `"sell"` | — |
| `trader` | string | Trader wallet/identifier (for trader_position alerts) | `"0x1234...abcd"` | — |
| `timestamp` | string | ISO 8601 timestamp of the event | `"2026-04-02T14:05:00Z"` | Server time if missing |
| `live` | boolean | Whether the market is currently live/active | `true` | `true` |
| `topic` | string | Market category/topic | `"crypto"`, `"politics"`, `"sports"` | — |
| `metadata` | object | Additional alert-specific data | `{"threshold": 0.1, "duration": "5m"}` | — |

## Example Payloads

### Price Alert

```json
{
  "alert_type": "price_alert",
  "platform": "polymarket",
  "market_id": "will-fed-cut-rates-in-june",
  "title": "Will the Fed cut rates in June?",
  "yes_price": 0.58,
  "volume": 1450,
  "volume_kind": "cumulative",
  "event_kind": "quote",
  "timestamp": "2026-04-02T14:05:00Z",
  "live": true,
  "topic": "macro",
  "metadata": {
    "price_change": 0.12,
    "threshold_crossed": 0.55,
    "timeframe": "1h"
  }
}
```

### Whale Trade Alert

```json
{
  "alert_type": "whale_trade",
  "platform": "polymarket",
  "market_id": "btc-above-100k-by-eoy",
  "title": "Bitcoin above $100k by end of year?",
  "yes_price": 0.43,
  "volume": 25000,
  "volume_kind": "delta",
  "event_kind": "trade",
  "trade_size": 25000,
  "trade_side": "buy",
  "trader": "0x1234567890abcdef",
  "timestamp": "2026-04-02T15:30:22Z",
  "live": true,
  "topic": "crypto",
  "metadata": {
    "min_trade_size": 10000,
    "trader_pnl": 45000
  }
}
```

### Trader Position Alert

```json
{
  "alert_type": "trader_position",
  "platform": "polymarket",
  "market_id": "presidential-election-2026",
  "title": "Presidential Election 2026 - Winner",
  "yes_price": 0.52,
  "volume": 8500,
  "volume_kind": "delta",
  "event_kind": "trade",
  "trade_size": 8500,
  "trade_side": "sell",
  "trader": "0xabcdef1234567890",
  "timestamp": "2026-04-02T16:45:10Z",
  "live": true,
  "topic": "politics",
  "metadata": {
    "followed_trader": "top_performer_123",
    "position_size_usd": 8500
  }
}
```

### Market Event Alert

```json
{
  "alert_type": "market_event",
  "platform": "kalshi",
  "market_id": "KXBTC-26DEC31-B110000",
  "title": "Bitcoin above $110k by Dec 31?",
  "yes_price": 0.38,
  "volume": 2200,
  "volume_kind": "cumulative",
  "event_kind": "alert",
  "timestamp": "2026-04-02T17:20:00Z",
  "live": true,
  "topic": "crypto",
  "metadata": {
    "market_status": "newly_created",
    "liquidity_added": 50000
  }
}
```

## Transformation to MarketEvent

The endpoint transforms the incoming payload into Trade Hunter's internal `MarketEvent` model:

1. **Source assignment:** Always set to `"polyalerthub"` for webhook ingestion
2. **Platform pass-through:** Use `platform` field directly
3. **Market identification:** Use `market_id` and `title` directly
4. **Price extraction:** Prefer `yes_price` when available
5. **Volume handling:** Use `volume` with `volume_kind` (defaults to `"delta"` if not specified)
6. **Event classification:** Use `event_kind` from payload, default to `"alert"` if missing
7. **Trade details:** Pass through `trade_size`, `trade_side`, `trader` when present
8. **Timestamp:** Use provided `timestamp`, fall back to server time
9. **Metadata preservation:** Store `alert_type` and other custom fields in `metadata`

## Error Handling

| Status Code | Scenario | Response |
|-------------|----------|----------|
| 200 OK | Event ingested successfully | `{"ok": true, "signals_triggered": 1}` |
| 400 Bad Request | Missing required fields (`platform`, `market_id`, `title`) | `{"error": "bad request"}` |
| 401 Unauthorized | Invalid or missing auth token when `POLYALERTHUB_TOKEN` is configured | `{"error": "unauthorized"}` |
| 500 Internal Server Error | Store failure or other server error | `{"error": "internal server error"}` |

## Field Validation

- **platform:** Must be a non-empty string
- **market_id:** Must be a non-empty string
- **title:** Must be a non-empty string
- **yes_price:** If present, must be between 0.0 and 1.0
- **no_price:** If present, must be between 0.0 and 1.0
- **volume:** If present, must be non-negative
- **timestamp:** If present, must be valid ISO 8601 format

Missing optional fields are handled gracefully — the endpoint will not reject payloads with partial data.

## Rate Limiting

Currently no rate limiting is enforced. Future implementations may add per-source rate limits.

## Webhook Testing

Use `curl` to test webhook delivery locally:

```bash
curl -X POST http://127.0.0.1:8765/api/alerts/polyalerthub \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token-here" \
  -d @tests/fixtures/sample_polyalerthub_payload.json
```

Check `/api/state` to verify the event appears in the dashboard:

```bash
curl -s http://127.0.0.1:8765/api/state | jq '.markets[] | select(.source == "polyalerthub")'
```

## Notes

- PolyAlertHub is a third-party service not affiliated with Trade Hunter
- Actual payload structure may vary based on PolyAlertHub's implementation
- This schema is designed to be flexible and handle missing optional fields
- The `alert_type` field helps categorize alerts but is not used for routing
