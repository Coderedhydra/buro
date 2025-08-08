from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class ProbeRequest(BaseModel):
    template_id: str
    endpoint_id: str
    param_values: Dict[str, Any] | None = None

class ProbeResponse(BaseModel):
    probe_id: str
    status: str

@router.post("/")
async def run_probe(payload: ProbeRequest) -> ProbeResponse:
    # TODO: enqueue probe task
    return ProbeResponse(probe_id="demo-probe-1", status="queued")