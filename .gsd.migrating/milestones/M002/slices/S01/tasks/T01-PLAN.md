---
estimated_steps: 7
estimated_files: 2
skills_used: []
---

# T01: Enhance SpikeSignal with enriched context fields

1. Enhance SpikeSignal dataclass in models.py with:
   - baseline_1h, baseline_24h (replace single baseline)
   - price_move_1m, price_move_5m, price_move_30m
   - leading_events: list[MarketEvent] (last 5 before spike)
2. Update detector.py to calculate multiple baselines and price move windows
3. Update detector to capture leading events from market window
4. Update SpikeSignal.to_dict() to include new fields

## Inputs

- `app/models.py`
- `app/detector.py`

## Expected Output

- `app/models.py`
- `app/detector.py`
- `tests/test_signal_enrichment.py`

## Verification

python -m pytest tests/test_signal_enrichment.py -k baseline -k price_move
