# Autogen Multi-Agent Builder

A **single-image, fully self-contained Docker application** that wraps
[Microsoft Autogen](https://github.com/microsoft/autogen) into a multi-agent
app builder with a built-in web UI.

Type a request like _"Build a Flask REST API with a Postgres backend and a
Dockerfile"_ into the UI, and a team of Autogen agents (Planner, Coder, Infra,
Critic) plans it, generates the code and infrastructure files, validates the
result, and writes everything to a mounted host directory — all inside **one
container**, using **your** local OpenAI-compatible model endpoint.

No Microsoft services. No Azure. No cloud. Everything runs locally.

---

## Quick start

```bash
# Pull and start the published single image
docker compose up -d --pull always
```

Then open <http://localhost:3000>.

The Compose file pulls the published image from GHCR; no local build or
repository checkout is required. To stop it, run `docker compose down`.
The image is rebuilt and published automatically whenever `main` changes.

---

## Using the app

1. **Model Endpoint** (left panel): enter your OpenAI-compatible `/v1` endpoint,
   e.g. `http://host.docker.internal:8000/v1`, an API key (or `none`), and the
   model name. Click **Save Endpoint**. All agents use this endpoint.
2. **Agents** (left panel): optionally edit each agent's role, system prompt,
   and enabled tools. Click **Save**.
3. **Chat** (center): type your build request and press **Send** (or Ctrl+Enter).
4. **Conversation** (center): watch the agents collaborate in real time
   (streamed over a WebSocket).
5. **Generated Files** (right): browse and view files written to `/app/output`.
6. **Workflow Controls** (top bar): Pause / Resume / Restart / Stop.

Generated files appear on your host in the directory you mounted to
`/app/output`.

---

## Architecture (everything in one container)

```
┌─────────────────────────── single Docker image ───────────────────────────┐
│  FastAPI (port 3000)                                                        │
│    ├── /api/*                REST API (agents, workflow, files, model)      │
│    ├── /api/workflow/stream  WebSocket — live agent messages                │
│    └── /                     serves the built React + Tailwind UI (static)  │
│                                                                             │
│  Autogen runtime (autogen-agentchat 0.7.5, installed from vendored source)  │
│    ├── PlannerAgent   interprets the request, produces the plan             │
│    ├── CoderAgent     generates application code (write_file tool)          │
│    ├── InfraAgent     generates Dockerfiles/configs/scripts                 │
│    ├── CriticAgent    reviews & loops until it replies APPROVE              │
│    └── UserProxyAgent represents the human operator                         │
│                                                                             │
│  File output → /app/output  (mount to host to retrieve generated files)     │
└─────────────────────────────────────────────────────────────────────────-─┘
```

The agents run as a `RoundRobinGroupChat`
(planner → coder → infra → critic), looping until the critic emits `APPROVE`
or a message cap is reached.

---

## Project layout

```
.
├── Dockerfile              # single multi-stage image (node build → python runtime)
├── docker-compose.yml      # single-image pull-and-run deployment
├── .env.example            # environment variables
├── backend/
│   ├── requirements.txt    # web deps (autogen installed from vendor/ in Docker)
│   └── src/
│       ├── main.py         # FastAPI: API + WS + static UI on port 3000
│       ├── agents/         # planner, coder, infra, critic, user
│       ├── workflows/      # build_application workflow engine
│       ├── tools/          # file_writer, system_tools
│       ├── models/         # model_config, agent_registry
│       ├── api/            # route modules
│       └── utils/          # logger, file_manager
├── frontend/               # React + TS + Vite + Tailwind UI
│   └── src/components/      # AgentEditor, ChatInput, ConversationViewer,
│                            # FileViewer, WorkflowControls, ModelConfig
└── vendor/
    └── autogen/            # vendored microsoft/autogen fork (v0.7.5)
```

---

## Self-contained / offline

Autogen is **vendored** into `vendor/autogen` (a fork of `microsoft/autogen`)
and installed from that local source during the Docker build. The image
requires **no external services except your model endpoint**, so it is easy to
share with coworkers and build/run all at once.

---

## API reference

| Method | Path                       | Purpose                              |
| ------ | -------------------------- | ------------------------------------ |
| GET    | `/api/agents/list`         | List agents and their configs        |
| POST   | `/api/agents/configure`    | Create/update an agent               |
| POST   | `/api/workflow/run`        | Start a build workflow               |
| GET    | `/api/workflow/status`     | Current workflow state               |
| POST   | `/api/workflow/stop`       | Stop the workflow                    |
| POST   | `/api/workflow/restart`    | Restart the workflow                 |
| POST   | `/api/workflow/pause`      | Pause                                |
| POST   | `/api/workflow/resume`     | Resume                               |
| WS     | `/api/workflow/stream`     | Stream agent messages                |
| GET    | `/api/files/list`          | List generated files                 |
| GET    | `/api/files/get?name=...`  | Get a file's contents                |
| GET    | `/api/model/config`        | Get model endpoint config            |
| POST   | `/api/model/configure`     | Update model endpoint config         |

---

## Local development (without Docker)

Backend:

```bash
cd backend
pip install -r requirements.txt
pip install ./../vendor/autogen/python/packages/autogen-core \
            ./../vendor/autogen/python/packages/autogen-agentchat \
            "./../vendor/autogen/python/packages/autogen-ext[openai]"
cd src
uvicorn main:app --host 0.0.0.0 --port 3000
```

Frontend (dev server proxies `/api` to the backend on port 3000):

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

---

## Environment variables

| Variable          | Default                                    | Description                     |
| ----------------- | ------------------------------------------ | ------------------------------- |
| `MODEL_BASE_URL`  | `http://host.docker.internal:8000/v1`      | OpenAI-compatible endpoint      |
| `MODEL_API_KEY`   | `none`                                     | API key (if your server needs)  |
| `MODEL_NAME`      | `local-model`                              | Model name to request           |
| `OUTPUT_DIR`      | `/app/output`                              | Generated file output directory |
| `STATIC_DIR`      | `/app/static`                              | Built frontend location         |

The model endpoint can also be changed at runtime from the UI.
