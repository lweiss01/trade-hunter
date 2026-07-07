# Trade Hunter — dev tasks. Tests run under Python 3.14 (pytest 9.x).
# The Hermes tool venv has no pytest; use the system Python 3.14 explicitly.
PY ?= /c/Python314/python

.PHONY: test test-ruleset lint

# Full suite (note: ~8 pre-existing failures unrelated to the tuning-ruleset work —
# Py3.14 `re` backreference tightening + missing pykalshi module).
test:
	$(PY) -m pytest tests/ -q

# Focused: the self-improving tuning-ruleset feature (Phases 1-3+).
test-ruleset:
	$(PY) -m pytest tests/test_ruleset_store.py tests/test_analyst_ruleset.py tests/test_advisor_proposed_rules.py tests/test_tuning_advisor.py -v

lint:
	$(PY) -m pyflakes app/ 2>/dev/null || true
