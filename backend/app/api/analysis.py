from datetime import datetime

from fastapi import APIRouter

from app.schemas.analysis import BehaviorIn, BehaviorOut, EmojiIn, EmojiOut, MoodIn, MoodOut, TimeBlockOut
from app.services.analysis.behavior import classify
from app.services.analysis.emoji import analyze as analyze_emoji
from app.services.analysis.mood import MoodInput, analyze_mood
from app.services.analysis.time_blocks import current_block

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/time-block", response_model=TimeBlockOut)
def time_block(hour: int | None = None) -> TimeBlockOut:
    now = datetime.now()
    if hour is not None:
        now = now.replace(hour=hour % 24)
    block = current_block(now)
    return TimeBlockOut(
        key=block.key,
        label=block.label,
        vibe=block.vibe,
        content_types=block.content_types,
        score=block.score,
        hour=now.hour,
    )


@router.post("/behavior", response_model=BehaviorOut)
def behavior(body: BehaviorIn) -> BehaviorOut:
    result = classify(body.events)
    return BehaviorOut(cluster=result.cluster, rates=result.rates, event_count=result.event_count)


@router.post("/emoji", response_model=EmojiOut)
def emoji(body: EmojiIn) -> EmojiOut:
    result = analyze_emoji(body.emojis)
    return EmojiOut(**result.__dict__)


@router.post("/mood", response_model=MoodOut)
def mood(body: MoodIn) -> MoodOut:
    result = analyze_mood(
        MoodInput(text=body.text, emojis=body.emojis, image_base64=body.image_base64),
        provider_name=body.provider,
    )
    return MoodOut(
        dominant_emotion=result.dominant_emotion,
        emotions=result.emotions,
        provider=result.provider,
        confidence=result.confidence,
    )
