from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, SecretStr
from typing import Any, Dict, List, Optional
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from app.core.secrets import secret_store
from app.services.planner import generate_safe_test_plan

router = APIRouter()

class OneClickRequest(BaseModel):
    api_key: SecretStr
    target_url: HttpUrl
    model: Optional[str] = None  # e.g., "gemini-2.0-flash" or "gemini-1.5-flash"

class OneClickResponse(BaseModel):
    target_url: HttpUrl
    model: str
    discovered: List[str]
    plans: Dict[str, Any]

@router.post("/start", response_model=OneClickResponse)
async def oneclick_start(payload: OneClickRequest) -> OneClickResponse:
    key = payload.api_key.get_secret_value().strip()
    if not key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")
    secret_store.set_gemini_api_key(key)

    model = payload.model or "gemini-1.5-flash"

    # Fetch target HTML safely
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            resp = await client.get(str(payload.target_url))
            html = resp.text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch target: {e}")

    # Extract same-origin links (basic)
    parsed_root = urlparse(str(payload.target_url))
    soup = BeautifulSoup(html, "html.parser")
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        abs_url = urljoin(str(payload.target_url), a["href"])
        p = urlparse(abs_url)
        if p.netloc == parsed_root.netloc:
            links.append(abs_url)
    # Deduplicate & limit
    seen = []
    for u in links:
        if u not in seen:
            seen.append(u)
    discovered = seen[:25]

    # Plan safe tests for each discovered link (GET)
    plans: Dict[str, Any] = {}
    for url in discovered:
        plan = generate_safe_test_plan(method="GET", url=url, params=[], model=model)
        plans[url] = plan

    return OneClickResponse(target_url=payload.target_url, model=model, discovered=discovered, plans=plans)