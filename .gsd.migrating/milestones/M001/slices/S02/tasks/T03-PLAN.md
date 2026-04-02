---
estimated_steps: 6
estimated_files: 3
skills_used: []
---

# T03: Add optional token validation for PolyAlertHub endpoint

1. Add POLYALERTHUB_TOKEN to config.py Settings (optional, default None)
2. Update .env.example with POLYALERTHUB_TOKEN=
3. In endpoint handler: if token configured, check request.headers.get('Authorization') == f'Bearer {token}'
4. Return 401 Unauthorized if token mismatch
5. Skip validation if token not configured
6. Log validation attempts (success/failure)

## Inputs

- `app/config.py`
- `app/server.py`

## Expected Output

- `app/config.py`
- `.env.example`
- `app/server.py`
- `tests/test_polyalerthub_auth.py`

## Verification

python -m pytest tests/test_polyalerthub_auth.py
