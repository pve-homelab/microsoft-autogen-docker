"""build_application workflow engine.

Team: planner -> coder -> infra -> critic (RoundRobinGroupChat), looping
until the critic emits 'APPROVE' or a max message cap is hit. Streams every
agent message onto an asyncio.Queue consumed by the WebSocket route.

Controls: start / stop / restart (and pause/resume). Stop is honored between
streamed events via an asyncio flag; the underlying team stream is cancelled.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.base import TaskResult

from agents.planner_agent import build_planner_agent
from agents.coder_agent import build_coder_agent
from agents.infra_agent import build_infra_agent
from agents.critic_agent import build_critic_agent
from models.agent_registry import agent_registry
from utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class WorkflowManager:
    state: WorkflowState = WorkflowState.IDLE
    command: str = ""
    messages: list[dict] = field(default_factory=list)
    _queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    _pause_event: asyncio.Event = field(default_factory=asyncio.Event)
    _stop_flag: bool = False
    _task: Any = None

    def __post_init__(self) -> None:
        self._pause_event.set()

    # ---- controls ------------------------------------------------------
    def pause(self) -> None:
        if self.state == WorkflowState.RUNNING:
            self._pause_event.clear()
            self.state = WorkflowState.PAUSED

    def resume(self) -> None:
        if self.state == WorkflowState.PAUSED:
            self._pause_event.set()
            self.state = WorkflowState.RUNNING

    def stop(self) -> None:
        self._stop_flag = True
        self._pause_event.set()
        if self._task and not self._task.done():
            self._task.cancel()
        self.state = WorkflowState.STOPPED

    def start(self, command: str) -> bool:
        """Start a new workflow run. Returns False if one is already running."""
        if self.state == WorkflowState.RUNNING:
            return False
        self._task = asyncio.create_task(self.run(command))
        return True

    def restart(self, command: str | None = None) -> bool:
        """Stop any current run and start again with the same or new command."""
        cmd = command or self.command
        self.stop()
        self._stop_flag = False
        self.state = WorkflowState.IDLE
        return self.start(cmd)

    def status(self) -> dict:
        return {
            "state": self.state.value,
            "command": self.command,
            "message_count": len(self.messages),
        }

    async def next_message(self) -> dict | None:
        return await self._queue.get()

    # ---- execution -----------------------------------------------------
    def _build_team(self) -> RoundRobinGroupChat:
        planner = build_planner_agent(agent_registry.get("planner").to_dict())
        coder = build_coder_agent(agent_registry.get("coder").to_dict())
        infra = build_infra_agent(agent_registry.get("infra").to_dict())
        critic = build_critic_agent(agent_registry.get("critic").to_dict())
        termination = TextMentionTermination("APPROVE") | MaxMessageTermination(40)
        return RoundRobinGroupChat(
            participants=[planner, coder, infra, critic],
            termination_condition=termination,
        )

    async def run(self, command: str) -> None:
        self.command = command
        self.messages = []
        self._stop_flag = False
        self._pause_event.set()
        self.state = WorkflowState.RUNNING
        await self._emit("system", f"Workflow started for: {command}")
        try:
            team = self._build_team()
            async for event in team.run_stream(task=command):
                await self._pause_event.wait()
                if self._stop_flag:
                    await self._emit("system", "Workflow stopped by user.")
                    return
                if isinstance(event, TaskResult):
                    continue
                source = getattr(event, "source", "agent")
                content = getattr(event, "content", None)
                if content is None:
                    continue
                if not isinstance(content, str):
                    content = str(content)
                await self._emit(source, content)
            if self.state not in (WorkflowState.STOPPED,):
                self.state = WorkflowState.COMPLETED
                await self._emit("system", "Workflow completed.")
        except asyncio.CancelledError:
            self.state = WorkflowState.STOPPED
            await self._emit("system", "Workflow cancelled.")
        except Exception as exc:  # noqa: BLE001
            self.state = WorkflowState.FAILED
            logger.exception("Workflow failed")
            await self._emit("system", f"Workflow failed: {exc}")
        finally:
            await self._queue.put(None)

    async def _emit(self, source: str, content: str) -> None:
        msg = {"source": source, "content": content, "state": self.state.value}
        self.messages.append(msg)
        await self._queue.put(msg)
        logger.info("[%s] %s", source, content[:120].replace("\n", " "))


workflow_manager = WorkflowManager()
