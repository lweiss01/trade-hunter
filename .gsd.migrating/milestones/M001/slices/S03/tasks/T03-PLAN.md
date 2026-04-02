---
estimated_steps: 6
estimated_files: 1
skills_used: []
---

# T03: Verify detector baseline calculation behavior unchanged post-migration

1. Create test: generate same event sequence, run through in-memory detector and SQLite detector
2. Compare: volume_deltas deque contents, baseline calculations, signal triggers
3. Verify: detector._baseline() returns same values for both backends
4. Verify: detector._volume_delta() handles cumulative volume correctly
5. Document any differences - fail test if behavior diverges
6. Add regression test with known event sequence and expected baseline/signals

## Inputs

- `app/detector.py`
- `app/store.py`

## Expected Output

- `tests/test_detector_migration.py`

## Verification

python -m pytest tests/test_detector_migration.py -v
