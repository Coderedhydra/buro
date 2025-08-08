from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzerResult(BaseModel):
    anomalies: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    rationale: str = ""
    exploitable: Optional[bool] = None
    vuln_type: Optional[str] = None
    cwe: Optional[str] = None


class Classification(BaseModel):
    severity: str
    exploitable: bool
    confidence: float
    triage: str
    vuln_type: Optional[str] = None
    cwe: Optional[str] = None