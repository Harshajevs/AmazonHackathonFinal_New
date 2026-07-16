"""Mood provider registry.

Selects the provider named by MOOD_PROVIDER, falling back to the
zero-dependency heuristic provider when the requested one is
unavailable (PRD FR-CTX-05: provider failure degrades, never 5xx).
"""

import logging

from app.core.config import get_settings
from app.services.analysis.mood.base import MoodInput, MoodProvider, MoodResult, ProviderUnavailable
from app.services.analysis.mood.heuristic import HeuristicMoodProvider
from app.services.analysis.mood.llm import OllamaMoodProvider, OpenRouterMoodProvider
from app.services.analysis.mood.onnx_facial import OnnxFacialMoodProvider

logger = logging.getLogger(__name__)

_PROVIDERS: dict[str, type[MoodProvider]] = {
    "heuristic": HeuristicMoodProvider,
    "onnx": OnnxFacialMoodProvider,
    "ollama": OllamaMoodProvider,
    "openrouter": OpenRouterMoodProvider,
}

_fallback = HeuristicMoodProvider()
_instances: dict[str, MoodProvider] = {"heuristic": _fallback}


def get_provider(name: str | None = None) -> MoodProvider:
    key = (name or get_settings().mood_provider).lower()
    if key not in _PROVIDERS:
        logger.warning("Unknown mood provider %r, using heuristic", key)
        return _fallback
    if key not in _instances:
        _instances[key] = _PROVIDERS[key]()
    return _instances[key]


def analyze_mood(payload: MoodInput, provider_name: str | None = None) -> MoodResult:
    provider = get_provider(provider_name)
    try:
        return provider.analyze(payload)
    except ProviderUnavailable as exc:
        logger.info("Mood provider %s unavailable (%s); falling back to heuristic", provider.name, exc)
        result = _fallback.analyze(payload)
        result.provider = f"heuristic (fallback from {provider.name})"
        return result


__all__ = ["MoodInput", "MoodResult", "analyze_mood", "get_provider", "ProviderUnavailable"]
