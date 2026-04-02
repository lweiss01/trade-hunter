---
estimated_steps: 9
estimated_files: 1
skills_used: []
---

# T03: Define DivergenceSignal model with spread context

1. Create DivergenceSignal dataclass extending SpikeSignal
2. Additional fields:
   - kalshi_event: MarketEvent
   - polymarket_event: MarketEvent
   - spread_cents: float
   - spread_pct: float
   - duration_seconds: float
3. Automatically set tier='cross-venue divergence'
4. Update to_dict() for serialization

## Inputs

- `app/models.py`

## Expected Output

- `app/models.py`
- `tests/test_models.py`

## Verification

python -c 'from app.models import DivergenceSignal; s = DivergenceSignal.__annotations__; assert "spread_pct" in s'
