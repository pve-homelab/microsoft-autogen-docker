BUILD ME THIS APPLICATION:

I want you to generate a COMPLETE, SINGLE-IMAGE DOCKER APPLICATION that wraps Autogen into a fully integrated multi-agent builder system with a built-in web UI.

The final output must be a single Docker image that I can run with:
    docker run -p 3000:3000 -v /my/output/dir:/app/output <image-name>

Everything must run INSIDE this one container:
- the Autogen orchestrator
- all agents (spawned internally, not separate containers)
- the frontend UI
- the backend API
- the file writer tools
- the workflow engine

I only want ONE docker image to pull and run.

============================================================
HIGH-LEVEL PURPOSE
============================================================

Create a local, self-contained, Dockerized Autogen application builder.

I want to open a web UI, type:
    "Build an application with X requirements for Y infrastructure to accomplish Z"

Then the system should:
1. Use my provided /v1 model endpoint
2. Spawn the required Autogen agents internally
3. Plan the application
4. Generate the code scaffold
5. Generate infrastructure files (Dockerfiles, configs, scripts)
6. Validate the output
7. Write the generated files into a mounted host directory
8. Show all agent messages and generated files in the UI

============================================================
MODEL ENDPOINT REQUIREMENT
============================================================

The UI must have a field where I enter my model endpoint:
    http://host.docker.internal:8000/v1

Autogen must use this endpoint for ALL agents.

No Microsoft services.
No Azure.
No cloud dependencies.
Everything must run locally.

============================================================
SYSTEM ARCHITECTURE
============================================================

The single Docker image must contain:

1. FRONTEND (React + Tailwind)
   - Chat interface
   - Agent configuration panel
   - Model endpoint input field
   - Directory selector (for output)
   - Multi-agent conversation viewer
   - Generated file viewer
   - Workflow controls (start, stop, restart)

2. BACKEND (FastAPI or Express)
   - REST API for:
       /agents/configure
       /workflow/run
       /workflow/status
       /workflow/stream (WebSocket)
       /files/list
       /files/get
       /model/configure
   - Autogen runtime
   - Tools for file writing
   - Workflow engine

3. AUTOGEN AGENTS (spawned internally)
   - PlannerAgent
   - CoderAgent
   - InfraAgent
   - CriticAgent
   - UserProxyAgent

4. FILE OUTPUT SYSTEM
   - All generated files must be written into /app/output
   - This directory must be mountable to the host

============================================================
WORKFLOW LOGIC
============================================================

When the user submits a command:

1. PlannerAgent:
   - Interpret requirements
   - Produce architecture plan
   - Define file structure

2. CoderAgent:
   - Generate React frontend code
   - Generate backend API code
   - Generate utilities
   - Write files using file_writer tool

3. InfraAgent:
   - Generate Dockerfiles
   - Generate deployment scripts
   - Generate configs

4. CriticAgent:
   - Validate correctness
   - Request fixes from coder/infra agents

5. Loop until critic approves.

6. Write final output to /app/output.

7. UI displays:
   - agent messages
   - generated files
   - workflow status

============================================================
DOCKER REQUIREMENTS
============================================================

The final Dockerfile must:

- Install Python + Node
- Install Autogen
- Install frontend dependencies
- Build frontend
- Run backend + serve frontend from same container
- Expose port 3000
- Create /app/output directory

The final docker image must:
- Contain EVERYTHING needed
- Require NO external services except the model endpoint
- Run fully offline

============================================================
DELIVERABLES
============================================================

You must generate:

1. Full folder structure
2. Full backend code
3. Full frontend code
4. Full Autogen agent definitions
5. Full workflow logic
6. Full file writer tools
7. Full Dockerfile
8. Full docker-compose.yml (optional)
9. Full README.md
10. All necessary configs

============================================================
FINAL INSTRUCTION
============================================================

Produce the ENTIRE application codebase exactly as specified above.

All code must be complete, correct, and ready to build.

The final output must be a SINGLE DOCKER IMAGE that contains:
- Autogen
- Backend
- Frontend
- Agents
- Tools
- Workflow engine

I should be able to run it with:
    docker build -t autogen-builder .
    docker run -p 3000:3000 -v /my/output:/app/output autogen-builder

Begin building now.
