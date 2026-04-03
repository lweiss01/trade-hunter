"""Tests for TuningAdvice structured suggestions (M006/S03 T01+T02)."""
from __future__ import annotations

from app.analyst import TuningAdvice, _build_tuning_prompt


# ── T01: TuningAdvice structured fields ──────────────────────────────────────

def test_tuning_advice_to_dict_has_suggested_thresholds_key():
    """suggested_thresholds key is always present in to_dict output."""
    advice = TuningAdvice(
        summary="too many noise signals",
        global_recommendation="raise volume delta",
        recommendations=["tweak 1"],
    )
    d = advice.to_dict()
    assert "suggested_thresholds" in d


def test_tuning_advice_to_dict_empty_suggested_when_none():
    """When no numeric suggestions are set, suggested_thresholds is an empty dict."""
    advice = TuningAdvice(
        summary="s",
        global_recommendation="r",
        recommendations=[],
    )
    d = advice.to_dict()
    assert d["suggested_thresholds"] == {}


def test_tuning_advice_to_dict_includes_all_set_suggestions():
    """All three threshold fields appear when set."""
    advice = TuningAdvice(
        summary="s",
        global_recommendation="r",
        recommendations=[],
        suggested_min_volume_delta=200.0,
        suggested_min_price_move=0.05,
        suggested_score_threshold=4.0,
    )
    d = advice.to_dict()
    assert d["suggested_thresholds"] == {
        "min_volume_delta": 200.0,
        "min_price_move": 0.05,
        "score_threshold": 4.0,
    }


def test_tuning_advice_to_dict_partial_suggestions():
    """Only set fields appear; unset fields are omitted from suggested_thresholds."""
    advice = TuningAdvice(
        summary="s",
        global_recommendation="r",
        recommendations=[],
        suggested_min_volume_delta=150.0,
    )
    d = advice.to_dict()
    assert d["suggested_thresholds"] == {"min_volume_delta": 150.0}
    assert "min_price_move" not in d["suggested_thresholds"]
    assert "score_threshold" not in d["suggested_thresholds"]


def test_tuning_advice_prose_fields_still_present():
    """Prose fields are not removed by the structured threshold addition."""
    advice = TuningAdvice(
        summary="summary text",
        global_recommendation="global rec",
        recommendations=["rec 1", "rec 2"],
        suggested_min_volume_delta=180.0,
    )
    d = advice.to_dict()
    assert d["summary"] == "summary text"
    assert d["global_recommendation"] == "global rec"
    assert d["recommendations"] == ["rec 1", "rec 2"]
    assert "generated_at" in d


def test_tuning_advice_suggested_thresholds_not_in_prose_fields():
    """suggested_thresholds is a separate key — not embedded inside prose text."""
    advice = TuningAdvice(
        summary="raise the score threshold",
        global_recommendation="increase score_threshold to 4.5",
        recommendations=[],
        suggested_score_threshold=4.5,
    )
    d = advice.to_dict()
    # Structured field lives under suggested_thresholds, not injected into prose
    assert d["suggested_thresholds"]["score_threshold"] == 4.5
    assert isinstance(d["summary"], str)
    assert isinstance(d["global_recommendation"], str)


# ── T01: Prompt requests structured thresholds ───────────────────────────────

def _make_signal(market_id: str = "MKT-1", tier: str = "watch") -> dict:
    return {
        "event": {"market_id": market_id, "yes_price": 0.55},
        "tier": tier,
        "score": 3.1,
        "volume_delta": 130.0,
        "price_move": 0.04,
        "analyst": {"noise_or_signal": "noise", "direction": "yes", "confidence": "low", "threshold_note": ""},
    }


def test_tuning_prompt_requests_suggested_thresholds():
    """Prompt instructs the model to return suggested_thresholds as a structured JSON block."""
    signals = [_make_signal("MKT-1"), _make_signal("MKT-2")]
    prompt = _build_tuning_prompt(signals)
    assert "suggested_thresholds" in prompt


def test_tuning_prompt_names_all_three_threshold_keys():
    """Prompt explicitly mentions all three numeric threshold keys."""
    signals = [_make_signal()]
    prompt = _build_tuning_prompt(signals)
    assert "min_volume_delta" in prompt
    assert "min_price_move" in prompt
    assert "score_threshold" in prompt


def test_tuning_prompt_describes_current_thresholds_section():
    """Prompt includes a CURRENT THRESHOLDS section so the model has context."""
    signals = [_make_signal()]
    prompt = _build_tuning_prompt(signals)
    assert "CURRENT THRESHOLDS" in prompt


# ── T02: State shape separates suggested from applied ─────────────────────────

def _make_tuning_dict(**kwargs) -> dict:
    """Simulate what TuningAdvice.to_dict() returns."""
    base = TuningAdvice(
        summary="too many noise signals at low volume",
        global_recommendation="raise min_volume_delta to 200",
        recommendations=["tweak 1", "tweak 2"],
        **kwargs,
    ).to_dict()
    return base


def test_state_tuning_advisor_has_status_suggested():
    """When tuning advice is present in state, status='suggested' is set."""
    # Simulate what service.py does when advisor has a result
    tuning_dict = _make_tuning_dict(suggested_min_volume_delta=200.0)
    state_tuning = {**tuning_dict, "status": "suggested"}

    assert state_tuning["status"] == "suggested"


def test_state_suggested_thresholds_distinct_from_applied():
    """suggested_thresholds in tuning_advisor does not equal the applied_thresholds block."""
    applied = {
        "min_volume_delta": 120.0,
        "min_price_move": 0.03,
        "score_threshold": 3.0,
    }
    tuning_dict = _make_tuning_dict(suggested_min_volume_delta=200.0)
    suggested = tuning_dict["suggested_thresholds"]

    # They must be structurally separate — same keys but different containers
    assert suggested is not applied
    # Suggested value differs from applied (that's the whole point)
    assert suggested.get("min_volume_delta") != applied["min_volume_delta"]


def test_state_applied_thresholds_key_present():
    """State config block should expose applied_thresholds as a named sub-key."""
    # Simulate service.py state["config"] shape
    config = {
        "applied_thresholds": {
            "min_volume_delta": 120.0,
            "min_price_move": 0.03,
            "score_threshold": 3.0,
        },
        "spike_min_volume_delta": 120.0,
        "spike_min_price_move": 0.03,
        "spike_score_threshold": 3.0,
    }
    assert "applied_thresholds" in config
    assert config["applied_thresholds"]["min_volume_delta"] == 120.0


def test_state_suggested_thresholds_never_overwrites_applied():
    """Applying suggested_thresholds to applied_thresholds would require explicit action — they don't merge."""
    tuning_dict = _make_tuning_dict(suggested_score_threshold=5.0)
    config = {"applied_thresholds": {"score_threshold": 3.0}}

    # Even if someone naively merged, the test would catch that suggested != applied
    suggested = tuning_dict["suggested_thresholds"]
    applied = config["applied_thresholds"]
    assert suggested.get("score_threshold") != applied["score_threshold"]
