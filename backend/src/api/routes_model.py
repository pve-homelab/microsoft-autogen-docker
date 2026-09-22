"""Routes: /model/config, /model/configure."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from models.model_config import model_config_store

router = APIRouter(prefix="/model", tags=["model"])


class ModelConfigureRequest(BaseModel):
    base_url: str | None = None
    api_key: str | None = None
    model_name: str | None = None


@router.get("/config")
async def get_model_config() -> dict:
    return model_config_store.get().to_dict()


@router.post("/configure")
async def configure_model(req: ModelConfigureRequest) -> dict:
    cfg = model_config_store.update(
        base_url=req.base_url,
        api_key=req.api_key,
        model_name=req.model_name,
    )
    return {"config": cfg.to_dict()}
