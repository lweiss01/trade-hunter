---
estimated_steps: 5
estimated_files: 2
skills_used: []
---

# T01: Add checklist_completed JSON field to signals schema

1. Add checklist_completed JSON column to signals table
2. Structure: {"what_changed": true, "cross_platform": false, "news": null, "liquidity": true, "resolution_timing": false, "what_invalidates": null}
3. Default to all null (not started)
4. Update schema migration
5. Add to SpikeSignal model as optional field

## Inputs

- `app/schema.sql`
- `app/models.py`

## Expected Output

- `app/schema.sql`
- `app/models.py`

## Verification

python -c 'import app.db; conn = app.db.connect(":memory:"); cursor = conn.cursor(); cursor.execute("SELECT sql FROM sqlite_master WHERE name=\"signals\""); sql = cursor.fetchone()[0]; assert "checklist_completed" in sql'
