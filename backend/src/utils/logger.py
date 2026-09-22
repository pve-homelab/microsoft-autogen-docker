"""Application logging."""
from __future__ import annotations

import logging
import sys

_CONFIGURED = False


def get_logger(name: str = "autogen_builder") -> logging.Logger:
    global _CONFIGURED
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root = logging.getLogger("autogen_builder")
        root.setLevel(logging.INFO)
        root.addHandler(handler)
        root.propagate = False
        _CONFIGURED = True
    if name.startswith("autogen_builder"):
        return logging.getLogger(name)
    return logging.getLogger(f"autogen_builder.{name}")
