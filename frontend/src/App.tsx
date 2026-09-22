import AgentEditor from "./components/AgentEditor";
import ChatInput from "./components/ChatInput";
import ConversationViewer from "./components/ConversationViewer";
import FileViewer from "./components/FileViewer";
import WorkflowControls from "./components/WorkflowControls";
import ModelConfig from "./components/ModelConfig";

// Single-page control panel. Left: model + agents config. Center: chat +
// conversation. Right: generated files. Top bar: workflow controls.
export default function App() {
  return (
    <div className="h-screen flex flex-col p-4 gap-3">
      <header className="flex items-center justify-between">
        <h1 className="text-lg font-bold text-accent">
          Autogen Multi-Agent Builder
        </h1>
        <span className="text-xs text-slate-500">
          Single image · Local model · Autogen v0.7.5
        </span>
      </header>

      <div className="bg-panel border border-slate-700 rounded-lg px-3 py-2">
        <WorkflowControls />
      </div>

      <div className="flex flex-1 gap-3 min-h-0">
        {/* Left column: configuration */}
        <div className="w-1/4 flex flex-col gap-3 overflow-auto">
          <section className="bg-panel border border-slate-700 rounded-lg p-3">
            <ModelConfig />
          </section>
          <section className="bg-panel border border-slate-700 rounded-lg p-3 flex-1 min-h-[300px]">
            <AgentEditor />
          </section>
        </div>

        {/* Center column: chat + conversation */}
        <div className="flex-1 flex flex-col gap-3 min-h-0">
          <section className="bg-panel border border-slate-700 rounded-lg p-3">
            <ChatInput />
          </section>
          <section className="bg-panel border border-slate-700 rounded-lg p-3 flex-1 min-h-0">
            <ConversationViewer />
          </section>
        </div>

        {/* Right column: files */}
        <div className="w-1/3 bg-panel border border-slate-700 rounded-lg p-3 min-h-0">
          <FileViewer />
        </div>
      </div>
    </div>
  );
}
