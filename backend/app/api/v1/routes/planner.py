from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Any, Dict, List

from app.services.planner import generate_safe_test_plan

router = APIRouter()

class PlannerRequest(BaseModel):
    method: str
    url: HttpUrl
    params: List[Dict[str, Any]] = []

@router.post("/plan")
async def plan_tests(payload: PlannerRequest) -> Dict[str, Any]:
    try:
        plan = generate_safe_test_plan(method=payload.method.upper(), url=str(payload.url), params=payload.params)
        return {"plan": plan}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))