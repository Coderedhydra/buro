from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from app.llm.adapter import LLMConfig, create_llm_adapter
from app.llm.prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_PROMPT_TEMPLATE
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


def generate_safe_test_plan(*, method: str, url: str, params: List[Dict[str, Any]], model: Optional[str] = None, provider: str = "gemini") -> Dict[str, Any]:
    if provider == "gemini":
        api_key = secret_store.get_gemini_api_key()
    elif provider == "openai":
        api_key = secret_store.get_openai_api_key()
    else:
        raise RuntimeError(f"Unsupported provider: {provider}")

    if not api_key:
        raise RuntimeError(f"{provider.capitalize()} API key not set")

    adapter = create_llm_adapter(LLMConfig(provider=provider, model=model or ("gemini-1.5-flash" if provider=="gemini" else "gpt-5"), api_key=api_key))

    user_prompt = PLANNER_USER_PROMPT_TEMPLATE.format(method=method, url=url, params_json=json.dumps(params))
    raw = adapter.generate(system_prompt=PLANNER_SYSTEM_PROMPT, user_prompt=user_prompt, temperature=0.1, max_tokens=1024)

    try:
        cleaned = _strip_code_fences(raw)
        plan = json.loads(cleaned)
    except Exception:
        plan = {"test_families": []}

    if not isinstance(plan, dict) or "test_families" not in plan:
        plan = {"test_families": []}

    return plan