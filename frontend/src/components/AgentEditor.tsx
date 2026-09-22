import { useEffect, useState } from "react";
import { api, AgentConfig } from "../api";

// Agent configuration panel: edit each agent's role, prompt, and tools.
export default function AgentEditor() {
  const [agents, setAgents] = useState<AgentConfig[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [role, setRole] = useState("");
  const [prompt, setPrompt] = useState("");
  const [tools, setTools] = useState("");
  const [status, setStatus] = useState("");

  async function load() {
    const { agents } = await api.listAgents();
    setAgents(agents);
    if (agents.length && !selected) select(agents[0]);
  }

  useEffect(() => {
    load().catch((e) => setStatus(String(e)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function select(a: AgentConfig) {
    setSelected(a.agent_name);
    setRole(a.role);
    setPrompt(a.prompt);
    setTools(a.tools_enabled.join(", "));
  }

  async function save() {
    setStatus("Saving...");
    try {
      await api.configureAgent({
        agent_name: selected,
        role,
        prompt,
        tools_enabled: tools
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      });
      setStatus("Saved.");
      await load();
    } catch (e) {
      setStatus(String(e));
    }
  }

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-sm font-semibold text-accent mb-2 uppercase tracking-wide">
        Agents
      </h2>
      <div className="flex gap-1.5 mb-3 flex-wrap">
        {agents.map((a) => (
          <button
            key={a.agent_name}
            onClick={() => select(a)}
            className={`px-2.5 py-1 rounded text-xs ${
              selected === a.agent_name
                ? "bg-accent text-panel"
                : "bg-panelalt text-slate-200"
            }`}
          >
            {a.agent_name}
          </button>
        ))}
      </div>

      <label className="text-xs text-slate-400">Role</label>
      <input
        className="bg-panelalt rounded px-2 py-1 mb-2 text-sm"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />

      <label className="text-xs text-slate-400">System Prompt</label>
      <textarea
        className="bg-panelalt rounded px-2 py-1 mb-2 text-sm flex-1 min-h-[120px]"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <label className="text-xs text-slate-400">Tools (comma-separated)</label>
      <input
        className="bg-panelalt rounded px-2 py-1 mb-3 text-sm"
        value={tools}
        onChange={(e) => setTools(e.target.value)}
      />

      <div className="flex items-center gap-3">
        <button
          onClick={save}
          disabled={!selected}
          className="bg-accent text-panel px-3 py-1 rounded text-sm font-medium disabled:opacity-50"
        >
          Save
        </button>
        <span className="text-xs text-slate-400">{status}</span>
      </div>
    </div>
  );
}
