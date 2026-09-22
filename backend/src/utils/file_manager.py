"""Sandboxed file operations rooted at the mounted output directory (/app/output)."""
from __future__ import annotations

import os
from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/app/output")).resolve()


class FileManager:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or OUTPUT_DIR).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, filename: str) -> Path:
        candidate = (self.root / filename).resolve()
        if not str(candidate).startswith(str(self.root)):
            raise ValueError(f"Path escapes output dir: {filename}")
        return candidate

    def write_file(self, filename: str, content: str) -> str:
        path = self._safe_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        logger.info("Wrote %s (%d bytes)", filename, len(content))
        return str(path.relative_to(self.root)).replace(os.sep, "/")

    def read_file(self, filename: str) -> str:
        path = self._safe_path(filename)
        if not path.is_file():
            raise FileNotFoundError(filename)
        return path.read_text(encoding="utf-8")

    def list_files(self) -> list[dict]:
        results: list[dict] = []
        for path in sorted(self.root.rglob("*")):
            if path.is_file():
                stat = path.stat()
                results.append(
                    {
                        "name": str(path.relative_to(self.root)).replace(os.sep, "/"),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                    }
                )
        return results


file_manager = FileManager()
