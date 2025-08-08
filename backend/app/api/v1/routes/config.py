from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, SecretStr
from app.core.secrets import secret_store

router = APIRouter()

class SetGeminiKeyRequest(BaseModel):
    api_key: SecretStr

class SetGeminiKeyResponse(BaseModel):
    ok: bool

@router.post("/llm/gemini-key", response_model=SetGeminiKeyResponse)
async def set_gemini_key(payload: SetGeminiKeyRequest) -> SetGeminiKeyResponse:
    key = payload.api_key.get_secret_value().strip()
    if not key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")
    secret_store.set_gemini_api_key(key)
    return SetGeminiKeyResponse(ok=True)