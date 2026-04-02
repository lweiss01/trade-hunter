---
estimated_steps: 5
estimated_files: 2
skills_used: []
---

# T01: Install pykalshi and test basic WebSocket connection

1. Add pykalshi to dependencies in pyproject.toml under [project.optional-dependencies.integrations]
2. Install locally: `py -m pip install -e .[integrations]`
3. Create test script test_kalshi_connection.py that connects to Kalshi WebSocket and subscribes to one test market
4. Verify connection succeeds and messages arrive
5. Document message schema variations observed

## Inputs

- `pyproject.toml`

## Expected Output

- `test_kalshi_connection.py`
- `output.log`

## Verification

py test_kalshi_connection.py && grep -q 'Connected' output.log

## Observability Impact

Test script logs connection events, message types received, errors
