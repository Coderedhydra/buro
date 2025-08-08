from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Any, Dict, List, Optional

from app.services.planner import generate_safe_test_plan

router = APIRouter()

class PlannerRequest(BaseModel):
    method: str
    url: HttpUrl
    params: List[Dict[str, Any]] = []
    model: Optional[str] = None
    provider: str = "gemini"

@router.post("/plan")
async def plan_tests(payload: PlannerRequest) -> Dict[str, Any]:
    try:
        plan = generate_safe_test_plan(method=payload.method.upper(), url=str(payload.url), params=payload.params, model=payload.model, provider=payload.provider)
        return {"plan": plan}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))