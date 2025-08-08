from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
async def health_v1() -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "api"})