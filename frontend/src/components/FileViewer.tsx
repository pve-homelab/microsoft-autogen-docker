import { useEffect, useState } from "react";
import { api, FileEntry } from "../api";

// Generated file viewer: lists files in /app/output and shows contents.
export default function FileViewer() {
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [selected, setSelected] = useState("");
  const [content, setContent] = useState("");

  async function refresh() {
    const { files } = await api.listFiles();
    setFiles(files);
  }

  useEffect(() => {
    refresh().catch(() => undefined);
    const id = setInterval(() => refresh().catch(() => undefined), 4000);
    return () => clearInterval(id);
  }, []);

  async function open(name: string) {
    setSelected(name);
    try {
      const { content } = await api.getFile(name);
      setContent(content);
    } catch (e) {
      setContent(String(e));
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-accent uppercase tracking-wide">
          Generated Files
        </h2>
        <button
          onClick={() => refresh()}
          className="text-xs bg-panelalt px-2 py-1 rounded text-slate-300"
        >
          Refresh
        </button>
      </div>
      <div className="flex flex-1 gap-3 min-h-0">
        <ul className="w-2/5 overflow-auto bg-panelalt rounded p-2 text-xs space-y-1">
          {files.length === 0 && <li className="text-slate-500">No files yet.</li>}
          {files.map((f) => (
            <li key={f.name}>
              <button
                onClick={() => open(f.name)}
                className={`text-left w-full truncate px-1 rounded ${
                  selected === f.name
                    ? "bg-accent text-panel"
                    : "text-slate-200 hover:bg-slate-700"
                }`}
                title={f.name}
              >
                {f.name}
              </button>
            </li>
          ))}
        </ul>
        <pre className="flex-1 overflow-auto bg-panelalt rounded p-3 text-xs font-mono whitespace-pre-wrap text-slate-200">
          {content || "Select a file to view its contents."}
        </pre>
      </div>
    </div>
  );
}
