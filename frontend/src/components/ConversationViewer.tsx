import { useEffect, useRef, useState } from "react";
import { ConversationMessage, wsUrl } from "../api";

const AGENT_COLORS: Record<string, string> = {
  planner: "text-sky-400",
  coder: "text-emerald-400",
  infra: "text-amber-400",
  critic: "text-pink-400",
  user: "text-slate-300",
  system: "text-slate-500",
};

// Multi-agent conversation viewer, fed by the /api/workflow/stream WebSocket.
export default function ConversationViewer() {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let closed = false;

    function connect() {
      ws = new WebSocket(wsUrl("/workflow/stream"));
      ws.onopen = () => setConnected(true);
      ws.onclose = () => {
        setConnected(false);
        if (!closed) setTimeout(connect, 2000);
      };
      ws.onmessage = (ev) => {
        const msg = JSON.parse(ev.data) as ConversationMessage;
        if (msg.content === "__STREAM_END__") return;
        setMessages((prev) => [...prev, msg]);
      };
    }
    connect();
    return () => {
      closed = true;
      ws?.close();
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-accent uppercase tracking-wide">
          Conversation
        </h2>
        <span className={`text-xs ${connected ? "text-emerald-400" : "text-slate-500"}`}>
          {connected ? "● live" : "○ offline"}
        </span>
      </div>
      <div className="flex-1 overflow-auto bg-panelalt rounded p-3 space-y-3 text-sm">
        {messages.length === 0 && (
          <p className="text-slate-500">
            No messages yet. Send a build request to watch the agents work.
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i}>
            <span className={`font-semibold ${AGENT_COLORS[m.source] ?? "text-slate-300"}`}>
              {m.source}
            </span>
            <pre className="whitespace-pre-wrap font-mono text-slate-200 mt-1">
              {m.content}
            </pre>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
