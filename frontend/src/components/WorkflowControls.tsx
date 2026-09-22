import { useEffect, useState } from "react";
import { api, WorkflowStatus } from "../api";

// Workflow controls: stop / restart / pause / resume + live status.
export default function WorkflowControls() {
  const [status, setStatus] = useState<WorkflowStatus | null>(null);

  async function refresh() {
    try {
      setStatus(await api.workflowStatus());
    } catch {
      /* ignore transient errors */
    }
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 2000);
    return () => clearInterval(id);
  }, []);

  const state = status?.state ?? "idle";

  return (
    <div className="flex items-center gap-3 flex-wrap">
      <span className="text-xs text-slate-400">State:</span>
      <span className="text-sm font-mono px-2 py-0.5 rounded bg-panelalt">
        {state}
      </span>
      {status && (
        <span className="text-xs text-slate-500">{status.message_count} msgs</span>
      )}
      <div className="flex gap-2 ml-auto">
        <button
          onClick={() => api.pauseWorkflow().then(setStatus)}
          className="bg-amber-500 text-panel px-3 py-1 rounded text-sm font-medium"
        >
          Pause
        </button>
        <button
          onClick={() => api.resumeWorkflow().then(setStatus)}
          className="bg-emerald-500 text-panel px-3 py-1 rounded text-sm font-medium"
        >
          Resume
        </button>
        <button
          onClick={() => api.restartWorkflow().then(setStatus)}
          className="bg-sky-500 text-panel px-3 py-1 rounded text-sm font-medium"
        >
          Restart
        </button>
        <button
          onClick={() => api.stopWorkflow().then(setStatus)}
          className="bg-pink-600 text-white px-3 py-1 rounded text-sm font-medium"
        >
          Stop
        </button>
      </div>
    </div>
  );
}
