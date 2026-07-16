"""Unit tests for context analysis services (PRD 8.3)."""

from datetime import datetime

from app.services.analysis.behavior import classify
from app.services.analysis.emoji import analyze
from app.services.analysis.mood import MoodInput, analyze_mood
from app.services.analysis.time_blocks import current_block


def test_behavior_prototype_rules():
    assert classify(["subtitle_toggle"] * 5 + ["play"] * 5).cluster == "accessibility_user"
    assert classify(["content_switch"] * 7 + ["play"] * 3).cluster == "content_switcher"
    assert classify(["skip_forward"] * 6 + ["play"] * 4).cluster == "quick_browser"
    assert classify(["rewind"] * 8 + ["play"] * 17).cluster == "high_engagement"
    assert classify(["play", "pause"] * 20).cluster == "binge_watcher"
    assert classify(["play", "pause", "skip_forward"]).cluster == "social_viewer"


def test_behavior_determinism():
    events = ["play", "rewind", "pause"] * 10
    assert classify(events).cluster == classify(events).cluster


def _hour_block(hour: int) -> str:
    return current_block(datetime(2026, 7, 16, hour, 0)).key


def test_time_block_boundaries():
    """FR-CTX-01 boundary hours."""
    assert _hour_block(0) == "latenight"
    assert _hour_block(6) == "morning"
    assert _hour_block(10) == "midday"
    assert _hour_block(14) == "afternoon"
    assert _hour_block(18) == "evening"
    assert _hour_block(22) == "prime"
    assert _hour_block(23) == "prime"


def test_emoji_analysis():
    result = analyze(["😂", "😂", "😂", "❤️"])
    assert result.dominant_emotion == "happy"
    assert result.dominant_emoji == "😂"
    assert 0 < result.confidence <= 100
    assert abs(sum(result.emotion_scores.values()) - 1.0) < 1e-3  # values are rounded to 4 dp


def test_emoji_unknown_input():
    result = analyze(["🦖"])
    assert result.dominant_emotion == "neutral"
    assert result.confidence == 0.0


def test_heuristic_mood_text():
    happy = analyze_mood(MoodInput(text="This movie was amazing, I love it!"))
    assert happy.dominant_emotion == "happy"
    sad = analyze_mood(MoodInput(text="feeling really sad and lonely tonight"))
    assert sad.dominant_emotion == "sad"


def test_mood_provider_fallback():
    """Requesting an unavailable provider degrades to heuristic, never raises."""
    result = analyze_mood(MoodInput(text="great fun"), provider_name="ollama")
    assert "heuristic" in result.provider or result.provider == "ollama"


def test_mood_empty_input_is_neutral():
    result = analyze_mood(MoodInput())
    assert result.dominant_emotion in ("neutral", "angry")  # uniform -> first argmax stable
    assert result.provider == "heuristic"
