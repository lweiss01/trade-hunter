---
estimated_steps: 11
estimated_files: 1
skills_used: []
---

# T05: Test detector tuning end-to-end with signal rate validation

1. Navigate to /dashboard/detector-tuning
2. Record baseline: note current signal count/hour
3. Adjust spike_min_volume_delta to 2x default
4. Save changes, generate test events
5. Verify fewer signals triggered (higher threshold)
6. Adjust spike_score_threshold lower
7. Verify more signals triggered
8. Test 'Reset to Defaults' - verify settings restored
9. Restart app, verify settings persist
10. Check audit log: verify config changes recorded
11. Document impact of each setting on signal rate

## Inputs

- `app/templates/detector_tuning.html`
- `app/server.py`

## Expected Output

- `integration_test_results.md`

## Verification

test -f integration_test_results.md && grep -q 'detector tuning test' integration_test_results.md
