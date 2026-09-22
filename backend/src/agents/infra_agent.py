"""InfraAgent: generates Dockerfiles, configs, and deployment scripts."""
from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent

from agents import build_model_client
from tools.file_writer import write_file, read_file, list_files
from tools.system_tools import make_directory, record_command

DEFAULT_INFRA = {
    "agent_name": "infra",
    "role": "DevOps / Infrastructure Engineer",
    "prompt": (
        "You are the InfraAgent, a DevOps engineer. Based on the plan and the "
        "code from the CoderAgent, generate infrastructure: Dockerfiles, "
        "docker-compose files, env configs, and deployment scripts. Use "
        "write_file to persist files and record_command to document deploy "
        "steps. Finish with 'INFRA COMPLETE'."
    ),
    "tools_enabled": ["write_file", "read_file", "list_files", "make_directory", "record_command"],
}

_TOOL_MAP = {
    "write_file": write_file,
    "read_file": read_file,
    "list_files": list_files,
    "make_directory": make_directory,
    "record_command": record_command,
}


def build_infra_agent(config: dict) -> AssistantAgent:
    tools = [_TOOL_MAP[t] for t in config.get("tools_enabled", []) if t in _TOOL_MAP]
    return AssistantAgent(
        name=config["agent_name"],
        model_client=build_model_client(),
        system_message=config["prompt"],
        description=config.get("role", "Infra"),
        tools=tools or None,
        reflect_on_tool_use=True,
    )
