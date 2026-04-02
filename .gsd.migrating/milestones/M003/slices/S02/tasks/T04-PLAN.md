---
estimated_steps: 6
estimated_files: 2
skills_used: []
---

# T04: Wire SpreadDetector into event processing pipeline

1. Wire SpreadDetector into service.py
2. On each MarketEvent, pass to both SpikeDetector and SpreadDetector
3. SpreadDetector emits DivergenceSignal when criteria met
4. Store DivergenceSignal in signals table (add divergence-specific columns if needed)
5. Expose divergence signals via /api/signals?type=divergence
6. Add divergence section to spike board view

## Inputs

- `app/spread_detector.py`
- `app/service.py`

## Expected Output

- `app/service.py`
- `app/server.py`

## Verification

curl -s http://127.0.0.1:8765/api/signals?type=divergence | jq -e '.[] | .tier == "cross-venue divergence"'
