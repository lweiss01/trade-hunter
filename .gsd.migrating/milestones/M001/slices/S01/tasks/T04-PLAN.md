---
estimated_steps: 5
estimated_files: 3
skills_used: []
---

# T04: Add KALSHI_MARKETS env var configuration and subscription logic

1. Add KALSHI_MARKETS to config.py Settings dataclass (comma-separated list)
2. Update .env.example with KALSHI_MARKETS=TICKER1,TICKER2
3. Update KalshiPykalshiFeed to read settings.kalshi_markets and subscribe to each ticker
4. Add validation: if kalshi_markets is empty, publish_status with running=False, detail='no KALSHI_MARKETS configured'
5. Test with real market tickers

## Inputs

- `app/config.py`
- `.env.example`
- `app/feeds/kalshi_pykalshi.py`

## Expected Output

- `app/config.py`
- `.env.example`
- `app/feeds/kalshi_pykalshi.py`

## Verification

grep -q 'KALSHI_MARKETS' .env.example && python -c 'from app.config import Settings; s = Settings(); assert hasattr(s, "kalshi_markets")'
