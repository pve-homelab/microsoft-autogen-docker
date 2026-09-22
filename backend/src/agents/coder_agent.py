"""CoderAgent: generates application code and writes files via tools."""
from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent

from agents import build_model_client
from tools.file_writer import write_file, read_file, list_files

DEFAULT_CODER = {
    "agent_name": "coder",
    "role": "Application Developer",
    "prompt": (
        "You are the CoderAgent, an expert full-stack developer. Follow the "
        "PlannerAgent's plan and implement the application (frontend, backend, "
        "utilities). Use the write_file tool to persist EVERY file (relative "
        "path + full content). Use read_file/list_files to inspect output. "
        "Write clean, complete, working code. Finish with 'CODE COMPLETE'."
    ),
    "tools_enabled": ["write_file", "read_file", "list_files"],
}

_TOOL_MAP = {"write_file": write_file, "read_file": read_file, "list_files": list_files}


def build_coder_agent(config: dict) -> AssistantAgent:
    tools = [_TOOL_MAP[t] for t in config.get("tools_enabled", []) if t in _TOOL_MAP]
    return AssistantAgent(
        name=config["agent_name"],
        model_client=build_model_client(),
        system_message=config["prompt"],
        description=config.get("role", "Coder"),
        tools=tools or None,
        reflect_on_tool_use=True,
    )
