"""LLM mood providers: local Ollama (default) or OpenRouter free models.

Both are free options; a paid provider would implement the same
MoodProvider interface and register in the mood registry.
"""

import json

import httpx

from app.core.config import get_settings
from app.services.analysis.mood.base import MoodInput, MoodProvider, MoodResult, ProviderUnavailable
from app.services.recommendations.matrices import EMOTIONS

_PROMPT = (
    "Classify the emotional tone of this viewer message into exactly one of: "
    f"{', '.join(EMOTIONS)}. Reply with JSON only: "
    '{"emotion": "<label>", "confidence": <0-1>}. Message: '
)


def _parse(reply: str, provider: str) -> MoodResult:
    try:
        start, end = reply.index("{"), reply.rindex("}") + 1
        data = json.loads(reply[start:end])
        emotion = data.get("emotion", "neutral")
        confidence = float(data.get("confidence", 0.5))
    except (ValueError, KeyError):
        emotion, confidence = "neutral", 0.3
    if emotion not in EMOTIONS:
        emotion = "neutral"
    emotions = {e: (confidence if e == emotion else round((1 - confidence) / 5, 4)) for e in EMOTIONS}
    return MoodResult(dominant_emotion=emotion, emotions=emotions, provider=provider, confidence=confidence)


class OllamaMoodProvider(MoodProvider):
    name = "ollama"

    def analyze(self, payload: MoodInput) -> MoodResult:
        if not payload.text:
            raise ProviderUnavailable("ollama provider requires text")
        settings = get_settings()
        try:
            response = httpx.post(
                f"{settings.ollama_base_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": _PROMPT + payload.text, "stream": False},
                timeout=30,
            )
            response.raise_for_status()
            return _parse(response.json().get("response", ""), self.name)
        except httpx.HTTPError as exc:
            raise ProviderUnavailable(f"ollama unreachable: {exc}") from exc


class OpenRouterMoodProvider(MoodProvider):
    name = "openrouter"

    def available(self) -> bool:
        return bool(get_settings().openrouter_api_key)

    def analyze(self, payload: MoodInput) -> MoodResult:
        if not payload.text:
            raise ProviderUnavailable("openrouter provider requires text")
        settings = get_settings()
        if not settings.openrouter_api_key:
            raise ProviderUnavailable("OPENROUTER_API_KEY not configured")
        try:
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
                json={
                    "model": settings.openrouter_model,
                    "messages": [{"role": "user", "content": _PROMPT + payload.text}],
                },
                timeout=30,
            )
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            return _parse(reply, self.name)
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            raise ProviderUnavailable(f"openrouter failed: {exc}") from exc
