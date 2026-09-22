"""Agents package: shared factory for the OpenAI-compatible model client.

Uses autogen-agentchat v0.7.x:
    autogen_ext.models.openai.OpenAIChatCompletionClient
"""
from __future__ import annotations

from autogen_ext.models.openai import OpenAIChatCompletionClient

from models.model_config import model_config_store


def build_model_client() -> OpenAIChatCompletionClient:
    """Build a chat client for any OpenAI-compatible /v1 endpoint.

    Supplies explicit model_info so local servers (vLLM, LM Studio, Ollama's
    OpenAI shim, etc.) with unknown model names still work.
    """
    cfg = model_config_store.get()
    return OpenAIChatCompletionClient(
        model=cfg.model_name,
        base_url=cfg.base_url,
        api_key=cfg.api_key or "none",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        },
    )
