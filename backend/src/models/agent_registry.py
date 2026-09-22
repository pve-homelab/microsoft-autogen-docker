"""Registry of editable agent configurations (role, prompt, tools).

Makes the system modular: agents can be reconfigured from the UI, and new
agents can be added, without code changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from threading import Lock

from agents.planner_agent import DEFAULT_PLANNER
from agents.coder_agent import DEFAULT_CODER
from agents.infra_agent import DEFAULT_INFRA
from agents.critic_agent import DEFAULT_CRITIC
from agents.user_agent import DEFAULT_USER


@dataclass
class AgentConfig:
    agent_name: str
    role: str
    prompt: str
    tools_enabled: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class AgentRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._agents: dict[str, AgentConfig] = {}
        for default in (DEFAULT_PLANNER, DEFAULT_CODER, DEFAULT_INFRA, DEFAULT_CRITIC, DEFAULT_USER):
            self._agents[default["agent_name"]] = AgentConfig(**default)

    def list(self) -> list[dict]:
        with self._lock:
            return [a.to_dict() for a in self._agents.values()]

    def get(self, name: str) -> AgentConfig | None:
        with self._lock:
            cfg = self._agents.get(name)
            return AgentConfig(**asdict(cfg)) if cfg else None

    def configure(
        self,
        agent_name: str,
        role: str | None = None,
        prompt: str | None = None,
        tools_enabled: list[str] | None = None,
    ) -> AgentConfig:
        with self._lock:
            existing = self._agents.get(agent_name)
            if existing is None:
                existing = AgentConfig(
                    agent_name=agent_name,
                    role=role or agent_name,
                    prompt=prompt or "",
                    tools_enabled=tools_enabled or [],
                )
            else:
                if role is not None:
                    existing.role = role
                if prompt is not None:
                    existing.prompt = prompt
                if tools_enabled is not None:
                    existing.tools_enabled = tools_enabled
            self._agents[agent_name] = existing
            return AgentConfig(**asdict(existing))

    def remove(self, agent_name: str) -> bool:
        with self._lock:
            return self._agents.pop(agent_name, None) is not None


agent_registry = AgentRegistry()
