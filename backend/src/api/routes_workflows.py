"""Routes: /workflow/run, /workflow/status, /workflow/stop, /workflow/restart, etc."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from workflows.build_application import workflow_manager, WorkflowState

router = APIRouter(prefix="/workflow", tags=["workflow"])


class WorkflowRunRequest(BaseModel):
    command: str


@router.post("/run")
async def run_workflow(req: WorkflowRunRequest) -> dict:
    started = workflow_manager.start(req.command)
    if not started:
        return {"started": False, "reason": "A workflow is already running."}
    return {"started": True, "command": req.command}


@router.get("/status")
async def workflow_status() -> dict:
    return workflow_manager.status()


@router.post("/stop")
async def stop_workflow() -> dict:
    workflow_manager.stop()
    return workflow_manager.status()


class RestartRequest(BaseModel):
    command: str | None = None


@router.post("/restart")
async def restart_workflow(req: RestartRequest) -> dict:
    workflow_manager.restart(req.command)
    return workflow_manager.status()


@router.post("/pause")
async def pause_workflow() -> dict:
    workflow_manager.pause()
    return workflow_manager.status()


@router.post("/resume")
async def resume_workflow() -> dict:
    workflow_manager.resume()
    return workflow_manager.status()


@router.get("/messages")
async def workflow_messages() -> dict:
    return {"messages": workflow_manager.messages}
