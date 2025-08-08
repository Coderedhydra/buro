from __future__ import annotations
from typing import Optional
from openai import OpenAI
from .adapter import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    def __init__(self, model: str, api_key: str) -> None:
        self.model_name = model
        self._client = OpenAI(api_key=api_key)

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        resp = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = resp.choices[0].message.content or ""
        return content.strip()