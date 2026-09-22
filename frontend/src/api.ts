// API client. The frontend is served from the same origin as the backend,
// so all calls use the relative "/api" prefix and the WebSocket derives its
// URL from window.location.

const API_BASE = "/api";

export function wsUrl(path: string): string {
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${window.location.host}${API_BASE}${path}`;
}

export interface AgentConfig {
  agent_name: string;
  role: string;
  prompt: string;
  tools_enabled: string[];
}

export interface WorkflowStatus {
  state: string;
  command: string;
  message_count: number;
}

export interface ConversationMessage {
  source: string;
  content: string;
  state: string;
}

export interface FileEntry {
  name: string;
  size: number;
  modified: number;
}

export interface ModelConfig {
  base_url: string;
  api_key: string;
  model_name: string;
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json() as Promise<T>;
}

export const api = {
  listAgents: () =>
    fetch(`${API_BASE}/agents/list`).then((r) =>
      json<{ agents: AgentConfig[] }>(r)
    ),
  configureAgent: (cfg: Partial<AgentConfig> & { agent_name: string }) =>
    fetch(`${API_BASE}/agents/configure`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cfg),
    }).then((r) => json<{ agent: AgentConfig }>(r)),

  runWorkflow: (command: string) =>
    fetch(`${API_BASE}/workflow/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command }),
    }).then((r) => json<{ started: boolean; reason?: string }>(r)),
  workflowStatus: () =>
    fetch(`${API_BASE}/workflow/status`).then((r) => json<WorkflowStatus>(r)),
  stopWorkflow: () =>
    fetch(`${API_BASE}/workflow/stop`, { method: "POST" }).then((r) =>
      json<WorkflowStatus>(r)
    ),
  restartWorkflow: (command?: string) =>
    fetch(`${API_BASE}/workflow/restart`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: command ?? null }),
    }).then((r) => json<WorkflowStatus>(r)),
  pauseWorkflow: () =>
    fetch(`${API_BASE}/workflow/pause`, { method: "POST" }).then((r) =>
      json<WorkflowStatus>(r)
    ),
  resumeWorkflow: () =>
    fetch(`${API_BASE}/workflow/resume`, { method: "POST" }).then((r) =>
      json<WorkflowStatus>(r)
    ),

  listFiles: () =>
    fetch(`${API_BASE}/files/list`).then((r) =>
      json<{ files: FileEntry[] }>(r)
    ),
  getFile: (name: string) =>
    fetch(`${API_BASE}/files/get?name=${encodeURIComponent(name)}`).then((r) =>
      json<{ filename: string; content: string }>(r)
    ),

  getModel: () =>
    fetch(`${API_BASE}/model/config`).then((r) => json<ModelConfig>(r)),
  configureModel: (cfg: Partial<ModelConfig>) =>
    fetch(`${API_BASE}/model/configure`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cfg),
    }).then((r) => json<{ config: ModelConfig }>(r)),
};
