from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Finding(BaseModel):
    id: str
    title: str
    confidence: float
    triage: str

@router.get("/")
async def list_findings() -> List[Finding]:
    return [Finding(id="f1", title="Reflected input in error message", confidence=0.6, triage="pending")]