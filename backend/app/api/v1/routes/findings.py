from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any, Dict

from app.services.rule_engine import classify_finding

router = APIRouter()

class Finding(BaseModel):
    id: str
    title: str
    confidence: float
    triage: str
    severity: str = "info"
    exploitable: bool = False

@router.get("/")
async def list_findings() -> List[Finding]:
    return [
        Finding(
            id="f1",
            title="Reflected input in error message",
            confidence=0.6,
            triage="pending",
            severity="medium",
            exploitable=False,
        )
    ]

class AnalyzerLikeInput(BaseModel):
    anomalies: List[str] = []
    confidence: float = 0.0
    rationale: str = ""
    exploitable: bool | None = None

@router.post("/classify")
async def classify(payload: AnalyzerLikeInput) -> Dict[str, Any]:
    result = classify_finding(payload.model_dump())
    return result