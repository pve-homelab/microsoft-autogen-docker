# =============================================================================
# Autogen Multi-Agent Builder — SINGLE Docker image
#
# Stage 1 builds the React frontend. Stage 2 is a Python runtime that installs
# Autogen from the VENDORED source (fully self-contained, no external autogen
# download), copies the backend and the built frontend, and serves everything
# (REST + WebSocket + static UI) on a single port: 3000.
#
#   docker build -t autogen-builder .
#   docker run -p 3000:3000 -v /my/output:/app/output autogen-builder
# =============================================================================

# ---- Stage 1: build the frontend -------------------------------------------
FROM node:20-alpine AS frontend

WORKDIR /build/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build          # -> /build/frontend/dist


# ---- Stage 2: python runtime that serves everything ------------------------
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    OUTPUT_DIR=/app/output \
    STATIC_DIR=/app/static \
    MODEL_BASE_URL=http://host.docker.internal:8000/v1 \
    MODEL_API_KEY=none \
    MODEL_NAME=local-model

WORKDIR /app

# Build deps for any packages needing compilation.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# --- Install Python deps + Autogen from the vendored fork -------------------
COPY backend/requirements.txt ./requirements.txt
COPY vendor/ ./vendor/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install ./vendor/autogen/python/packages/autogen-core \
    && pip install ./vendor/autogen/python/packages/autogen-agentchat \
    && pip install "./vendor/autogen/python/packages/autogen-ext[openai]"

# --- Application code --------------------------------------------------------
COPY backend/src/ ./src/

# --- Built frontend from stage 1 --------------------------------------------
COPY --from=frontend /build/frontend/dist/ ./static/

# Output directory (mount a host dir here to retrieve generated files).
RUN mkdir -p /app/output

EXPOSE 3000

WORKDIR /app/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
