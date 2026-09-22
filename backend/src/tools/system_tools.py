"""System / infra helper tools exposed to Autogen agents.

Deliberately safe: creates directories inside the sandbox and records
deployment commands as documentation rather than executing them.
"""
from __future__ import annotations

from utils.file_manager import file_manager


async def make_directory(path: str) -> str:
    """Create a directory inside the output dir.

    Args:
        path: Relative directory path to create.
    """
    marker = f"{path.rstrip('/')}/.gitkeep"
    file_manager.write_file(marker, "")
    return f"Created directory: {path}"


async def record_command(description: str, command: str) -> str:
    """Record a deployment/build command into DEPLOY_STEPS.md.

    Args:
        description: What the command does.
        command: The shell command string.
    """
    try:
        existing = file_manager.read_file("DEPLOY_STEPS.md")
    except FileNotFoundError:
        existing = "# Deployment Steps\n\n"
    file_manager.write_file(
        "DEPLOY_STEPS.md",
        existing + f"### {description}\n\n```bash\n{command}\n```\n\n",
    )
    return f"Recorded step: {description}"
