"""UserProxyAgent: represents the human operator.

In this control panel the human interacts through the web UI, so the user
proxy is non-interactive and carries the initial command into the team.
Defined here so it appears in the registry and is reconfigurable.
"""
from __future__ import annotations

DEFAULT_USER = {
    "agent_name": "user",
    "role": "User Proxy (Human)",
    "prompt": (
        "You represent the human operator. You provide the initial build "
        "command and, when human input is enabled, approve or reject steps."
    ),
    "tools_enabled": [],
}
