---
estimated_steps: 10
estimated_files: 1
skills_used: []
---

# T01: Define detector_config schema with audit log

1. Add detector_config table to schema.sql:
   - id INTEGER PRIMARY KEY (single row)
   - spike_baseline_points INTEGER
   - spike_min_volume_delta REAL
   - spike_min_price_move REAL
   - spike_cooldown_seconds INTEGER
   - spike_score_threshold REAL
   - updated_at TIMESTAMP
2. Seed with current defaults from config.py
3. Add audit log table: detector_config_history (id, config_snapshot JSON, changed_by, changed_at)

## Inputs

- `app/schema.sql`

## Expected Output

- `app/schema.sql`

## Verification

python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"detector_config\""); assert cursor.fetchone()'
