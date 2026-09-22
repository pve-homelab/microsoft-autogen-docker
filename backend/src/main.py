"""FastAPI entrypoint.

Serves EVERYTHING on a single port (3000):
  - REST API under /api/*
  - WebSocket at /api/workflow/stream
  - the built React frontend (static files) for all other paths (SPA)

This is what allows the whole system to run as one Docker image.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import (
    routes_agents,
    routes_workflows,
    routes_files,
    routes_stream,
    routes_model,
)
from utils.logger import get_logger

logger = get_logger(__name__)

# Directory containing the built frontend (populated by the Docker build).
STATIC_DIR = Path(os.getenv("STATIC_DIR", "/app/static")).resolve()

app = FastAPI(
    title="Autogen Multi-Agent Builder",
    description="Single-image Autogen app builder with a built-in web UI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All API + WS routes are served under /api so they never collide with the
# SPA's client-side routes.
api_prefix = "/api"
app.include_router(routes_agents.router, prefix=api_prefix)
app.include_router(routes_workflows.router, prefix=api_prefix)
app.include_router(routes_files.router, prefix=api_prefix)
app.include_router(routes_stream.router, prefix=api_prefix)
app.include_router(routes_model.router, prefix=api_prefix)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "healthy"}


# ---- Static frontend (mounted last so /api takes precedence) --------------
if STATIC_DIR.is_dir():
    # Serve hashed assets etc. directly.
    app.mount(
        "/assets",
        StaticFiles(directory=str(STATIC_DIR / "assets")),
        name="assets",
    )

    index_file = STATIC_DIR / "index.html"

    @app.get("/")
    async def serve_index() -> FileResponse:
        return FileResponse(str(index_file))

    # SPA fallback: any non-API path returns index.html so client routing works.
    @app.exception_handler(StarletteHTTPException)
    async def spa_fallback(request, exc):  # type: ignore[no-untyped-def]
        if exc.status_code == 404 and not request.url.path.startswith("/api"):
            if index_file.is_file():
                return FileResponse(str(index_file))
        # Re-raise as JSON for API paths / other errors.
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
else:
    logger.warning("Static dir %s not found; serving API only.", STATIC_DIR)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Autogen builder started. Static dir: %s", STATIC_DIR)
