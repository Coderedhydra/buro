from __future__ import annotations
import google.generativeai as genai
from typing import Optional, Any

from .adapter import LLMAdapter


def _extract_text(response: Any) -> str:
    # Try the quick accessor first
    try:
        txt = response.text
        if isinstance(txt, str) and txt.strip():
            return txt.strip()
    except Exception:
        pass

    # Fallback to assembling from candidate parts
    try:
        candidates = getattr(response, "candidates", []) or []
        for cand in candidates:
            content = getattr(cand, "content", None)
            parts = getattr(content, "parts", None) if content else None
            if parts:
                texts = []
                for part in parts:
                    txt = getattr(part, "text", None)
                    if txt:
                        texts.append(txt)
                if texts:
                    return "\n".join(texts).strip()
    except Exception:
        pass

    # If we reach here, assume blocked/empty
    raise RuntimeError("LLM returned no text (possibly safety-blocked). Try a different model or adjust prompt.")


class GeminiAdapter(LLMAdapter):
    def __init__(self, model: str, api_key: str) -> None:
        self.model_name = model
        genai.configure(api_key=api_key)
        self._client = genai.GenerativeModel(model_name=model)

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        prompt = f"System:\n{system_prompt}\n\nUser:\n{user_prompt}"
        response = self._client.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                # Encourage structured JSON to reduce filtering issues
                "response_mime_type": "application/json",
                "candidate_count": 1,
            },
            safety_settings=None,
        )
        return _extract_text(response)