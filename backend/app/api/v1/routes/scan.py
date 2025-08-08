from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from typing import Optional

router = APIRouter()

class ScanRequest(BaseModel):
    root_url: HttpUrl
    scope: Optional[list[str]] = None
    creds: Optional[dict] = None
    allowed_hours: Optional[list[int]] = None

class ScanResponse(BaseModel):
    scan_id: str
    status: str

@router.post("/", response_model=ScanResponse)
async def start_scan(payload: ScanRequest) -> ScanResponse:
    # TODO: enqueue a Celery task to start scan
    return ScanResponse(scan_id="demo-scan-1", status="queued")