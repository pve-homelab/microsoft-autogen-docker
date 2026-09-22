"""Model endpoint configuration (OpenAI-compatible /v1).

Updated at runtime from the UI via /model/configure. All agents read from
this store, so changing the endpoint reconfigures every agent.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from threading import Lock


@dataclass
class ModelConfig:
    base_url: str = os.getenv("MODEL_BASE_URL", "http://host.docker.internal:8000/v1")
    api_key: str = os.getenv("MODEL_API_KEY", "none")
    model_name: str = os.getenv("MODEL_NAME", "local-model")

    def to_dict(self) -> dict:
        return asdict(self)


class ModelConfigStore:
    def __init__(self) -> None:
        self._config = ModelConfig()
        self._lock = Lock()

    def get(self) -> ModelConfig:
        with self._lock:
            return ModelConfig(**asdict(self._config))

    def update(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
    ) -> ModelConfig:
        with self._lock:
            if base_url is not None:
                self._config.base_url = base_url
            if api_key is not None:
                self._config.api_key = api_key
            if model_name is not None:
                self._config.model_name = model_name
            return ModelConfig(**asdict(self._config))


model_config_store = ModelConfigStore()
