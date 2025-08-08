from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

router = APIRouter()

class Parameter(BaseModel):
    name: str
    location: str  # query, body, header, cookie, path
    inferred_type: Optional[str] = None

class Endpoint(BaseModel):
    id: str
    method: str
    url: HttpUrl
    params: List[Parameter] = Field(default_factory=list)

@router.get("/")
async def list_inventory() -> List[Endpoint]:
    # TODO: fetch from DB
    return [
        Endpoint(
            id="1",
            method="GET",
            url="https://example.com/api/items",
            params=[Parameter(name="q", location="query", inferred_type="string")],
        )
    ]