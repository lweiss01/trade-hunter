# Kalshi WebSocket Message Schema Observations

**Test Date:** 2026-04-02  
**pykalshi Version:** 1.0.2  
**Test Status:** Library verified, connection requires credentials

## Installation Verification

✅ pykalshi 1.0.2 installed successfully  
✅ Imports work correctly  
✅ Client initialization validates credentials before attempting connection

## Connection Requirements

The KalshiClient requires:
1. `KALSHI_API_KEY_ID` environment variable
2. `KALSHI_PRIVATE_KEY_PATH` environment variable (path to private key file)

Without these, the client raises:
```
ValueError: API key ID required. Set KALSHI_API_KEY_ID env var or pass api_key_id.
```

## Message Schema Variations (from adapter code analysis)

The Kalshi WebSocket sends different message types that our adapter handles:

### Common Fields
- `market_ticker` or `ticker` - the market identifier
- Message type determined by `type(message).__name__`

### Ticker Updates (Quote-type messages)
- **price** (int, cents) - current price level
- **volume** or **size** - trading volume
- Event kind: "quote"

### Trade Updates
- **price** (int, cents) - trade execution price
- **count** - number of contracts
- **size** or **volume** - trade size
- **side** - "buy" or "sell"
- Event kind: "trade"

### Adapter Normalization Strategy

The `KalshiPykalshiFeed` adapter (app/feeds/kalshi_pykalshi.py):

1. **Market ID extraction:** Uses `getattr(message, "market_ticker", None) or getattr(message, "ticker", None)`
2. **Price normalization:** Converts cents to decimal: `price_cents / 100.0`
3. **Volume handling:** 
   - Prefers `volume` over `size` over `count`
   - Marks as `volume_kind='delta'` (incremental, not cumulative)
4. **Event classification:** Checks if message type name contains "trade" → `event_kind = "trade"`, else `"quote"`
5. **Defensive field access:** Uses `getattr()` with None defaults since fields vary by message type

### Known Field Variations

Based on the adapter's defensive extraction logic:
- Some messages have `market_ticker`, others have `ticker`
- Some have `volume`, others have `size` or `count`
- Trade messages include `side`, ticker messages may not
- `price` field is always in cents (integer)

## Next Steps for Full Schema Documentation

To document complete message schemas with real examples:
1. Set `KALSHI_API_KEY_ID` and `KALSHI_PRIVATE_KEY_PATH` in environment
2. Run `py test_kalshi_connection.py` with live credentials
3. The script will log all message attributes received from an active market

## References

- pykalshi GitHub: https://github.com/Kalshi/kalshi-python
- Adapter implementation: `app/feeds/kalshi_pykalshi.py`
- Test script: `test_kalshi_connection.py`
