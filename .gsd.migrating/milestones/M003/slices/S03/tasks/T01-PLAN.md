---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T01: Extend MarketEvent metadata with liquidity fields

1. Update MarketEvent metadata schema to include liquidity fields:
   - bid_price, ask_price (float, optional)
   - bid_size, ask_size (float, optional - contract count)
2. Update Kalshi adapter to extract bid/ask from ticker messages if available
3. Update PolyAlertHub adapter to extract liquidity fields from payload
4. Gracefully handle missing fields - set to None, don't crash
5. Update tests with liquidity metadata

## Inputs

- `app/models.py`
- `app/feeds/kalshi_pykalshi.py`

## Expected Output

- `app/models.py`
- `app/feeds/kalshi_pykalshi.py`
- `app/server.py`

## Verification

python -c 'from app.models import MarketEvent; e = MarketEvent(source="test", platform="test", market_id="TEST", title="Test", metadata={"bid_price": 0.50}); assert e.metadata.get("bid_price") == 0.50'
