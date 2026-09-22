"""PlannerAgent: interprets requirements and produces the architecture plan."""
from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent

from agents import build_model_client

DEFAULT_PLANNER = {
    "agent_name": "planner",
    "role": "Software Architect / Planner",
    "prompt": (
        "You are the PlannerAgent, a senior software architect. Given the "
        "user's build request, interpret the requirements, produce a concise "
        "architecture plan, and define the exact file structure to create. "
        "List which files the CoderAgent should write and which infra files "
        "the InfraAgent should write. Do NOT write code yourself. "
        "Finish with 'PLAN COMPLETE'."
    ),
    "tools_enabled": [],
}


def build_planner_agent(config: dict) -> AssistantAgent:
    return AssistantAgent(
        name=config["agent_name"],
        model_client=build_model_client(),
        system_message=config["prompt"],
        description=config.get("role", "Planner"),
    )
