from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ApprovalRequest(BaseModel):
    approver_id: str
    notes: str | None = None

class ApprovalResponse(BaseModel):
    finding_id: str
    approved: bool

@router.post("/{finding_id}/approve")
async def approve_finding(finding_id: str, payload: ApprovalRequest) -> ApprovalResponse:
    # TODO: persist approval and gate intrusive tests
    return ApprovalResponse(finding_id=finding_id, approved=True)