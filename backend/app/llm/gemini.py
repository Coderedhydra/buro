from __future__ import annotations
import google.generativeai as genai
from typing import Optional

from .adapter import LLMAdapter


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
            },
            safety_settings=None,
        )
        return (response.text or "").strip()