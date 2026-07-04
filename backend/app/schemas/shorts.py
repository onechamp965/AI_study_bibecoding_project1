from pydantic import BaseModel, Field


class ShortsGenerateRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=80)
    level: str = "HSK 1"
    duration: str = "20초"
    subtitle_position: str = "하단 중앙"
