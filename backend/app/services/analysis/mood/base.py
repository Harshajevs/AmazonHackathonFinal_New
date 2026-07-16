"""Mood provider abstraction.

Every mood source (text heuristics, ONNX facial model, local/remote LLMs)
implements the same interface, so providers can be swapped via the
MOOD_PROVIDER env var and paid providers can be added later without
touching callers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class MoodInput:
    text: str | None = None
    emojis: list[str] = field(default_factory=list)
    image_base64: str | None = None


@dataclass
class MoodResult:
    dominant_emotion: str
    emotions: dict[str, float]  # distribution over the 6 core emotions
    provider: str
    confidence: float


class ProviderUnavailable(Exception):
    """Raised when a provider's dependencies or backing service are missing."""


class MoodProvider(ABC):
    name: str = "base"

    @abstractmethod
    def analyze(self, payload: MoodInput) -> MoodResult: ...

    def available(self) -> bool:
        return True
