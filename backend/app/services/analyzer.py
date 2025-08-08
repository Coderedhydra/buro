from __future__ import annotations
from typing import Any, Dict, Optional

from app.llm.adapter import LLMConfig, create_llm_adapter
from app.llm.prompts import ANALYZER_SYSTEM_PROMPT, ANALYZER_USER_PROMPT_TEMPLATE
from app.core.secrets import secret_store


def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def analyze_probe_result(*, baseline_meta: Dict[str, Any], probe_meta: Dict[str, Any], model: Optional[str] = None, provider: str = "gemini") -> Dict[str, Any]:
    if provider == "gemini":
        api_key = secret_store.get_gemini_api_key()
    elif provider == "openai":
        api_key = secret_store.get_openai_api_key()
    else:
        raise RuntimeError(f"Unsupported provider: {provider}")

    if not api_key:
        raise RuntimeError(f"{provider.capitalize()} API key not set")

    adapter = create_llm_adapter(LLMConfig(provider=provider, model=model or ("gemini-1.5-flash" if provider=="gemini" else "gpt-5"), api_key=api_key))

    user_prompt = ANALYZER_USER_PROMPT_TEMPLATE.format(baseline_meta=baseline_meta, probe_meta=probe_meta)
    raw = adapter.generate(system_prompt=ANALYZER_SYSTEM_PROMPT, user_prompt=user_prompt, temperature=0.2, max_tokens=768)

    try:
        import json
        cleaned = _strip_code_fences(raw)
        result = json.loads(cleaned)
    except Exception:
        result = {"anomalies": [], "confidence": 0.5, "rationale": raw[:300]}

    return result