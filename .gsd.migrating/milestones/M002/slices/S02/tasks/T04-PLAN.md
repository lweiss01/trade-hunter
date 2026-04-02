---
estimated_steps: 8
estimated_files: 1
skills_used: []
---

# T04: Validate tier assignments against 20+ edge cases

1. Generate 20+ test signals with varying score/volume/price combinations
2. For each tier boundary:
   - Just below threshold (should be lower tier)
   - Just above threshold (should be higher tier)
   - Well above threshold (should be higher tier)
3. Manually review tier assignments - verify conservative high conviction (no false positives)
4. Verify tier explanations are clear and accurate
5. Document any counterintuitive assignments

## Inputs

- `app/detector.py`
- `tests/fixtures/`

## Expected Output

- `integration_test_results.md`

## Verification

python -m pytest tests/test_tier_refinement.py -k edge_cases -v
