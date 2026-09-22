import { useEffect, useState } from "react";
import { api } from "../api";

// Model endpoint input field + output directory info.
export default function ModelConfig() {
  const [baseUrl, setBaseUrl] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [modelName, setModelName] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    api
      .getModel()
      .then((c) => {
        setBaseUrl(c.base_url);
        setApiKey(c.api_key);
        setModelName(c.model_name);
      })
      .catch((e) => setStatus(String(e)));
  }, []);

  async function save() {
    setStatus("Saving...");
    try {
      await api.configureModel({
        base_url: baseUrl,
        api_key: apiKey,
        model_name: modelName,
      });
      setStatus("Saved.");
    } catch (e) {
      setStatus(String(e));
    }
  }

  return (
    <div className="flex flex-col">
      <h2 className="text-sm font-semibold text-accent mb-2 uppercase tracking-wide">
        Model Endpoint
      </h2>
      <label className="text-xs text-slate-400">Base URL (/v1)</label>
      <input
        className="bg-panelalt rounded px-2 py-1 mb-2 text-sm"
        placeholder="http://host.docker.internal:8000/v1"
        value={baseUrl}
        onChange={(e) => setBaseUrl(e.target.value)}
      />
      <label className="text-xs text-slate-400">API Key</label>
      <input
        className="bg-panelalt rounded px-2 py-1 mb-2 text-sm"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
      />
      <label className="text-xs text-slate-400">Model Name</label>
      <input
        className="bg-panelalt rounded px-2 py-1 mb-3 text-sm"
        value={modelName}
        onChange={(e) => setModelName(e.target.value)}
      />
      <div className="flex items-center gap-3 mb-2">
        <button
          onClick={save}
          className="bg-accent text-panel px-3 py-1 rounded text-sm font-medium"
        >
          Save Endpoint
        </button>
        <span className="text-xs text-slate-400">{status}</span>
      </div>
      <p className="text-[11px] text-slate-500 leading-snug">
        Output is written to <code>/app/output</code> inside the container.
        Mount it to a host directory:
        <br />
        <code>-v /my/output:/app/output</code>
      </p>
    </div>
  );
}
