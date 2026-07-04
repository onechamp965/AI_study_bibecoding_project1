from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    project_id: str
    folder_id: str | None = None
    topic: str = Field(min_length=1, max_length=100)
    language: str = "zh-CN"
    generate_image: bool = True
    generate_audio: bool = True
    generate_subtitle: bool = True
    render_video: bool = True


class JobResponse(BaseModel):
    id: str
    status: str
    progress: int
    topic: str
