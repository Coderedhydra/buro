from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from app.services.analyzer import analyze_probe_result
from app.services.rule_engine import classify_finding

router = APIRouter()

class AnalyzerRequest(BaseModel):
    baseline_meta: Dict[str, Any]
    probe_meta: Dict[str, Any]
    model: Optional[str] = None
    provider: str = "gemini"

@router.post("/run")
async def run_analyzer(payload: AnalyzerRequest) -> Dict[str, Any]:
    try:
        result = analyze_probe_result(baseline_meta=payload.baseline_meta, probe_meta=payload.probe_meta, model=payload.model, provider=payload.provider)
        classification = classify_finding(result)
        return {"analyzer": result, "classification": classification}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))