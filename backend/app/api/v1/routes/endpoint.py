from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List

router = APIRouter()

class EndpointDetails(BaseModel):
    id: str
    method: str
    url: HttpUrl
    history: List[str] = []

@router.get("/{endpoint_id}")
async def get_endpoint(endpoint_id: str) -> EndpointDetails:
    if endpoint_id != "1":
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return EndpointDetails(id="1", method="GET", url="https://example.com/api/items", history=["baseline", "probe-1"])