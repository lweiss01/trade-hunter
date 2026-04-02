---
estimated_steps: 12
estimated_files: 2
skills_used: []
---

# T03: Build detector tuning dashboard UI

1. Create app/templates/detector_tuning.html UI
2. Fetch current config from /api/detector/config
3. Render controls:
   - spike_baseline_points: slider (10-100) + input field
   - spike_min_volume_delta: slider (10-500) + input field
   - spike_min_price_move: slider (0.005-0.05, step 0.001) + input field (percentage)
   - spike_cooldown_seconds: slider (60-600) + input field
   - spike_score_threshold: slider (2.0-10.0, step 0.1) + input field
4. 'Save Changes' button POSTs to /api/detector/config
5. 'Reset to Defaults' button POSTs to /api/detector/config/reset
6. Show last updated timestamp
7. Show signal count last 1h/24h to gauge impact

## Inputs

- None specified.

## Expected Output

- `app/templates/detector_tuning.html`
- `app/static/js/detector_tuning.js`

## Verification

curl -s http://127.0.0.1:8765/dashboard/detector-tuning | grep -q 'detector tuning'
