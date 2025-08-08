from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        raise NotImplementedError


class LLMConfig:
    def __init__(self, provider: str = "gemini", model: str = "gemini-1.5-flash", api_key: Optional[str] = None) -> None:
        self.provider = provider
        self.model = model
        self.api_key = api_key


def create_llm_adapter(config: LLMConfig) -> LLMAdapter:
    if config.provider == "gemini":
        from .gemini import GeminiAdapter
        if not config.api_key:
            raise ValueError("Gemini API key is not set")
        return GeminiAdapter(model=config.model, api_key=config.api_key)
    if config.provider == "openai":
        from .openai_adapter import OpenAIAdapter
        if not config.api_key:
            raise ValueError("OpenAI API key is not set")
        return OpenAIAdapter(model=config.model, api_key=config.api_key)
    raise ValueError(f"Unsupported LLM provider: {config.provider}")