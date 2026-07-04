from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.gateway import ai_gateway


class ShortsGenerateRequest(BaseModel):
    topic: str
    level: str = "HSK 1"
    duration: str = "20초"
    subtitle_position: str = "하단 중앙"


router = APIRouter(prefix="/shorts", tags=["shorts"])


@router.post("/generate")
async def generate_shorts(payload: ShortsGenerateRequest):
    result = await ai_gateway.generate_chinese_words(payload.topic)

    return {
        "success": True,
        "message": "Shorts content generated successfully.",
        "data": {
            "topic": payload.topic,
            "level": payload.level,
            "duration": payload.duration,
            "subtitle_position": payload.subtitle_position,
            "content": result,
        },
    }