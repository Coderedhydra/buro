from __future__ import annotations
import os
import io
import zipfile
from typing import Iterator, List, Tuple

TEXT_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php", ".rs", ".cs", ".c", ".h", ".cpp", ".hpp", ".kt", ".m", ".swift", ".json", ".yml", ".yaml", ".toml", ".md", ".env", ".conf"}


def extract_zip_to_tmp(zip_bytes: bytes, tmp_dir: str) -> str:
    os.makedirs(tmp_dir, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        z.extractall(tmp_dir)
    return tmp_dir


def iter_text_files(root: str) -> Iterator[str]:
    for dirpath, _, filenames in os.walk(root):
        # Skip common vendor/build dirs
        if any(part in {"node_modules", ".git", "dist", "build", ".venv"} for part in dirpath.split(os.sep)):
            continue
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in TEXT_EXTS:
                yield os.path.join(dirpath, name)


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def chunk_text(text: str, max_chars: int = 12000) -> List[str]:
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunks.append(text[start:end])
        start = end
    return chunks


def enumerate_chunks(root: str, max_chars: int = 12000) -> Iterator[Tuple[str, int, str]]:
    for path in iter_text_files(root):
        content = read_file(path)
        if not content:
            continue
        parts = chunk_text(content, max_chars=max_chars)
        for idx, part in enumerate(parts):
            yield (path, idx, part)