"""Facial mood provider backed by the prototype's YOLO11 ONNX model.

Optional: requires `onnxruntime` and `opencv-python-headless`
(`pip install -r requirements-ml.txt`) plus the best.onnx checkpoint kept
under research/. Falls back cleanly when either is missing.
"""

import base64
from pathlib import Path

import numpy as np

from app.core.config import get_settings
from app.services.analysis.mood.base import MoodInput, MoodProvider, MoodResult, ProviderUnavailable
from app.services.recommendations.matrices import EMOTIONS

_INPUT_SIZE = 640


class OnnxFacialMoodProvider(MoodProvider):
    name = "onnx"

    def __init__(self) -> None:
        self._session = None

    def available(self) -> bool:
        try:
            import cv2  # noqa: F401
            import onnxruntime  # noqa: F401
        except ImportError:
            return False
        return Path(get_settings().onnx_model_path).exists()

    def _load(self):
        if self._session is None:
            if not self.available():
                raise ProviderUnavailable("onnxruntime/opencv or best.onnx not available")
            import onnxruntime

            self._session = onnxruntime.InferenceSession(get_settings().onnx_model_path)
        return self._session

    def analyze(self, payload: MoodInput) -> MoodResult:
        if not payload.image_base64:
            raise ProviderUnavailable("onnx provider requires image_base64")
        import cv2

        session = self._load()
        raw = base64.b64decode(payload.image_base64)
        image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ProviderUnavailable("could not decode image")

        # Match the prototype preprocessing: grayscale replicated to 3 channels.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray3 = cv2.merge([gray, gray, gray])
        resized = cv2.resize(gray3, (_INPUT_SIZE, _INPUT_SIZE))
        blob = resized.transpose(2, 0, 1)[np.newaxis].astype(np.float32) / 255.0

        outputs = session.run(None, {session.get_inputs()[0].name: blob})[0]
        # YOLO11 detect head: (1, 4 + num_classes, anchors)
        class_scores = outputs[0][4:, :]
        best_anchor = int(np.argmax(class_scores.max(axis=0)))
        logits = class_scores[:, best_anchor][: len(EMOTIONS)]
        if logits.sum() <= 0:
            raise ProviderUnavailable("no face detected")
        distribution = logits / logits.sum()
        dominant = int(np.argmax(distribution))
        return MoodResult(
            dominant_emotion=EMOTIONS[dominant],
            emotions={e: round(float(s), 4) for e, s in zip(EMOTIONS, distribution)},
            provider=self.name,
            confidence=round(float(distribution[dominant]), 4),
        )
