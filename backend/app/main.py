from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .api.v1.router import api_router

app = FastAPI(title="LLM-Assisted Security Testing Framework", version="0.1.0")

@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})

app.include_router(api_router, prefix="/api/v1")