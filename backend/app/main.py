from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    Path(settings.STORAGE_PATH).mkdir(parents=True, exist_ok=True)
    app.mount("/outputs", StaticFiles(directory=settings.STORAGE_PATH), name="outputs")
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
