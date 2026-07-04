from fastapi import APIRouter

from app.api.v1.routes import health
from app.api.v1.routes import jobs
from app.api.v1.routes import projects
from app.api.v1.routes import shorts

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(jobs.router)
api_router.include_router(shorts.router)