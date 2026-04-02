---
estimated_steps: 6
estimated_files: 1
skills_used: []
---

# T03: Add checklist update API endpoint

1. Add POST /api/signals/<signal_id>/checklist endpoint
2. Accept JSON body: {"item": "what_changed", "checked": true}
3. Update signals.checklist_completed JSON field
4. Return updated checklist state
5. Add GET /api/signals/<signal_id>/checklist to retrieve current state
6. Handle missing signal_id gracefully (404)

## Inputs

- `app/server.py`

## Expected Output

- `app/server.py`
- `tests/test_checklist_api.py`

## Verification

python -m pytest tests/test_checklist_api.py -k update -k get
