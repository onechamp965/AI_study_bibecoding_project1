from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {"success": True, "data": {"status": "healthy"}}
