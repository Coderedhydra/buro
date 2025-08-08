from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/{finding_id}")
async def download_report(finding_id: str) -> JSONResponse:
    # TODO: generate report
    return JSONResponse({"finding_id": finding_id, "report": {"format": "json", "content": "placeholder"}})