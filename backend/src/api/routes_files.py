"""Routes: /files/list, /files/get."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from utils.file_manager import file_manager

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/list")
async def list_files() -> dict:
    return {"files": file_manager.list_files()}


@router.get("/get")
async def get_file(name: str = Query(..., description="Relative file path")) -> dict:
    try:
        content = file_manager.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {name}")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"filename": name, "content": content}
