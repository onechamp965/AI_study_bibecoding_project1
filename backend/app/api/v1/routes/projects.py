from uuid import uuid4
from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.project import ProjectCreateRequest, ProjectResponse

router = APIRouter()


@router.get("")
async def list_projects() -> ApiResponse[list[ProjectResponse]]:
    return ApiResponse(data=[])


@router.post("", status_code=201)
async def create_project(payload: ProjectCreateRequest) -> ApiResponse[ProjectResponse]:
    project = ProjectResponse(id=str(uuid4()), title=payload.title, description=payload.description)
    return ApiResponse(message="Project created.", data=project)
