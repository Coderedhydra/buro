from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, List

from app.services.probe_generator import generate_probe_requests

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

class ProbePlanRequest(BaseModel):
    method: str
    url: HttpUrl
    params: List[Dict[str, Any]]
    plan: Dict[str, Any]

@router.post("/generate")
async def generate_probes(payload: ProbePlanRequest) -> Dict[str, Any]:
    requests = generate_probe_requests(method=payload.method.upper(), url=str(payload.url), params=payload.params, plan=payload.plan)
    return {"requests": requests}