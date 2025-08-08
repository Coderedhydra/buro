from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import tempfile
import shutil

from app.core.secrets import secret_store
from app.llm.adapter import LLMConfig, create_llm_adapter
from app.services.code_ingest import extract_zip_to_tmp, enumerate_chunks

router = APIRouter()

class AnalyzeZipRequest(BaseModel):
    provider: str = "gemini"  # or "openai"
    model: Optional[str] = None

class AnalyzeZipResponse(BaseModel):
    provider: str
    model: str
    results: List[Dict[str, Any]]

@router.post("/analyze-zip", response_model=AnalyzeZipResponse)
async def analyze_zip(provider: str = "gemini", model: Optional[str] = None, file: UploadFile = File(...)) -> AnalyzeZipResponse:
    # Load API key
    if provider == "gemini":
        api_key = secret_store.get_gemini_api_key()
        default_model = "gemini-1.5-flash"
    elif provider == "openai":
        api_key = secret_store.get_openai_api_key()
        default_model = "gpt-5"
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    if not api_key:
        raise HTTPException(status_code=400, detail=f"{provider.capitalize()} API key not set")

    adapter = create_llm_adapter(LLMConfig(provider=provider, model=model or default_model, api_key=api_key))

    # Save and extract ZIP to temp
    tmp_dir = tempfile.mkdtemp(prefix="code_zip_")
    try:
        zip_bytes = await file.read()
        root = extract_zip_to_tmp(zip_bytes, tmp_dir)

        results: List[Dict[str, Any]] = []
        system = (
            "You are auditing source code for security vulnerabilities. "
            "Read the provided chunk in isolation (stateless). "
            "Call out potential issues (input validation, authz, SSRF, SQLi, XSS, path traversal, deserialization). "
            "Return concise JSON with fields: findings (list of {type, cwe?, severity, snippet}), summary."
        )
        for path, idx, chunk in enumerate_chunks(root):
            user = f"File: {path}\nChunk: {idx}\n\n{chunk}"
            try:
                text = adapter.generate(system_prompt=system, user_prompt=user, temperature=0.2, max_tokens=800)
                results.append({"path": path, "chunk_index": idx, "analysis": text})
            except Exception as e:
                results.append({"path": path, "chunk_index": idx, "error": str(e)})

        return AnalyzeZipResponse(provider=provider, model=model or default_model, results=results)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)