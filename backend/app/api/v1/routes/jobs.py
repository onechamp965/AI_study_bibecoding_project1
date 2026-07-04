from uuid import uuid4
from fastapi import APIRouter

from app.ai.gateway import ai_gateway
from app.schemas.common import ApiResponse
from app.schemas.job import JobCreateRequest, JobResponse

router = APIRouter()


@router.post("", status_code=202)
async def create_job(payload: JobCreateRequest) -> ApiResponse[JobResponse]:
    # MVP: Queue 연동 전까지는 Job 생성만 반환한다.
    job = JobResponse(id=str(uuid4()), status="PENDING", progress=0, topic=payload.topic)
    return ApiResponse(message="Job accepted.", data=job)


@router.post("/preview")
async def preview_generation(payload: JobCreateRequest) -> ApiResponse[dict]:
    result = await ai_gateway.generate_chinese_words(payload.topic)
    return ApiResponse(data=result)
