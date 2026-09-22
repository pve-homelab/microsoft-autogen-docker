"""Routes: /agents/configure, /agents/list."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from models.agent_registry import agent_registry

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentConfigureRequest(BaseModel):
    agent_name: str
    role: str | None = None
    prompt: str | None = None
    tools_enabled: list[str] | None = None


@router.get("/list")
async def list_agents() -> dict:
    return {"agents": agent_registry.list()}


@router.post("/configure")
async def configure_agent(req: AgentConfigureRequest) -> dict:
    cfg = agent_registry.configure(
        agent_name=req.agent_name,
        role=req.role,
        prompt=req.prompt,
        tools_enabled=req.tools_enabled,
    )
    return {"agent": cfg.to_dict()}


@router.delete("/{agent_name}")
async def delete_agent(agent_name: str) -> dict:
    return {"removed": agent_registry.remove(agent_name), "agent_name": agent_name}
