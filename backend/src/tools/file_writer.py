"""File writing tools exposed to Autogen agents via tool calling."""
from __future__ import annotations

from utils.file_manager import file_manager


async def write_file(filename: str, content: str) -> str:
    """Write a generated file into the output directory (/app/output).

    Args:
        filename: Relative path of the file, e.g. "frontend/src/App.tsx".
        content: Full text content of the file.
    """
    rel = file_manager.write_file(filename, content)
    return f"Wrote file: {rel}"


async def read_file(filename: str) -> str:
    """Read a previously generated file from the output directory.

    Args:
        filename: Relative path of the file to read.
    """
    try:
        return file_manager.read_file(filename)
    except FileNotFoundError:
        return f"ERROR: file not found: {filename}"


async def list_files() -> str:
    """List all files currently in the output directory."""
    files = file_manager.list_files()
    if not files:
        return "(no files yet)"
    return "\n".join(f["name"] for f in files)
