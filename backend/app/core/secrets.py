from __future__ import annotations
from threading import RLock
from typing import Optional


class SecretStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._gemini_api_key: Optional[str] = None

    def set_gemini_api_key(self, api_key: str) -> None:
        with self._lock:
            self._gemini_api_key = api_key.strip()

    def get_gemini_api_key(self) -> Optional[str]:
        with self._lock:
            return self._gemini_api_key


secret_store = SecretStore()