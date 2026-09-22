"""CriticAgent: validates outputs and requests fixes, or approves."""
from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent

from agents import build_model_client
from tools.file_writer import read_file, list_files

DEFAULT_CRITIC = {
    "agent_name": "critic",
    "role": "Quality Reviewer",
    "prompt": (
        "You are the CriticAgent, a meticulous senior reviewer. Review the "
        "generated code and infrastructure for correctness, completeness, and "
        "consistency with the plan. Use read_file and list_files to inspect "
        "output. If anything is missing or wrong, list the required fixes and "
        "direct them to the coder or infra agent. Only when everything is "
        "correct and complete, reply with the single token 'APPROVE' on its "
        "own line to end the workflow."
    ),
    "tools_enabled": ["read_file", "list_files"],
}

_TOOL_MAP = {"read_file": read_file, "list_files": list_files}


def build_critic_agent(config: dict) -> AssistantAgent:
    tools = [_TOOL_MAP[t] for t in config.get("tools_enabled", []) if t in _TOOL_MAP]
    return AssistantAgent(
        name=config["agent_name"],
        model_client=build_model_client(),
        system_message=config["prompt"],
        description=config.get("role", "Critic"),
        tools=tools or None,
        reflect_on_tool_use=True,
    )
