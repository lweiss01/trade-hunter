---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T01: Implement refined tier assignment logic with composite criteria

1. Update detector.py::_tier() method with refined logic:
   - Cross-venue: if event.metadata.get('cross_venue') return 'cross-venue divergence'
   - High conviction: score >= 6.0 AND price_move >= 1.75 * threshold AND volume_multiple >= 3.0
   - Notable: score >= 4.0 OR (price_move >= 1.2 * threshold AND volume_multiple >= 2.4)
   - Watch: fallback for all other cases
2. Add _tier_explanation() method that returns human-readable reason
3. Update SpikeSignal to include tier_explanation field
4. Write unit tests for tier boundary cases

## Inputs

- `app/detector.py`
- `app/models.py`

## Expected Output

- `app/detector.py`
- `tests/test_tier_refinement.py`

## Verification

python -m pytest tests/test_tier_refinement.py -v
