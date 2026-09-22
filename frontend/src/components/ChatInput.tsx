import { useState } from "react";
import { api } from "../api";

// Chat interface: type a build request and dispatch it to the agent team.
export default function ChatInput({ onStarted }: { onStarted?: () => void }) {
  const [command, setCommand] = useState("");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function run() {
    if (!command.trim()) return;
    setBusy(true);
    setStatus("Starting...");
    try {
      const res = await api.runWorkflow(command.trim());
      setStatus(res.started ? "Workflow started." : res.reason ?? "Busy.");
      if (res.started) onStarted?.();
    } catch (e) {
      setStatus(String(e));
    } finally {
      setBusy(false);
    }
  }

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) run();
  }

  return (
    <div className="flex flex-col">
      <textarea
        className="bg-panelalt rounded px-3 py-2 text-sm min-h-[70px] resize-none"
        placeholder='e.g. "Build a Flask REST API with a Postgres backend and a Dockerfile"  (Ctrl+Enter to send)'
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        onKeyDown={onKeyDown}
      />
      <div className="flex items-center gap-3 mt-2">
        <button
          onClick={run}
          disabled={busy}
          className="bg-accent text-panel px-4 py-1.5 rounded font-medium disabled:opacity-50"
        >
          Send
        </button>
        <span className="text-xs text-slate-400">{status}</span>
      </div>
    </div>
  );
}
