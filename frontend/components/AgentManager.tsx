"use client";

import { useState } from "react";
import { Agent } from "@/types";

interface AgentManagerProps {
  agent: Agent;
  onAddUrl: (agentId: string, url: string, prompt: string) => void;
  onUploadFile: (agentId: string, file: File) => void;
  onBack: () => void;
}

export default function AgentManager({ agent, onAddUrl, onUploadFile, onBack }: AgentManagerProps) {
  const [urlOpen, setUrlOpen] = useState(false);
  const [filesOpen, setFilesOpen] = useState(false);
  const [urlInput, setUrlInput] = useState("");
  const [promptInput, setPromptInput] = useState("");

  const handleAddUrl = () => {
    if (urlInput) {
      onAddUrl(agent.id, urlInput, promptInput);
      setUrlInput("");
      setPromptInput("");
    }
  };

  return (
    <main className="flex-grow-1 d-flex flex-column bg-dark-900 min-w-0 overflow-auto">
      {/* Back button */}
      <div className="p-3 border-bottom border-dark-700">
        <button onClick={onBack} className="bg-transparent border-0 text-cyan-400 text-sm">
          ← Back to Chat
        </button>
      </div>

      <div className="p-4 mx-auto w-100" style={{ maxWidth: "700px" }}>
        {/* Agent Name */}
        <h2 className="text-white mb-4">{agent.name}</h2>

        {/* URL Section - Collapsible */}
        <div className="mb-3 border border-dark-600 rounded">
          <button
            onClick={() => setUrlOpen(!urlOpen)}
            className="w-100 d-flex justify-content-between align-items-center bg-dark-800 text-white border-0 px-3 py-3 text-start"
          >
            <span>URLs ({agent.urls.length})</span>
            <span>{urlOpen ? "▾" : "▸"}</span>
          </button>
          {urlOpen && (
            <div className="p-3 bg-dark-700 border-top border-dark-600">
              <div className="mb-2">
                <label className="text-xs text-gray-400 d-block mb-1">Website URL</label>
                <input
                  type="url"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  placeholder="https://example.com/page"
                  className="w-100 bg-dark-800 border border-dark-500 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
              <div className="mb-2">
                <label className="text-xs text-gray-400 d-block mb-1">Scrape Prompt</label>
                <textarea
                  value={promptInput}
                  onChange={(e) => setPromptInput(e.target.value)}
                  placeholder="Describe what data to extract from this page..."
                  rows={3}
                  className="w-100 bg-dark-800 border border-dark-500 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
                  style={{ resize: "vertical" }}
                />
              </div>
              <button
                onClick={handleAddUrl}
                className="bg-cyan-600 hover:bg-cyan-500 text-white text-sm px-3 py-2 rounded border-0"
              >
                Add URL
              </button>

              {agent.urls.length > 0 && (
                <ul className="list-unstyled mt-3 mb-0">
                  {agent.urls.map((url, i) => (
                    <li key={i} className="text-sm text-gray-300 py-1 border-bottom border-dark-600">{url}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        {/* Files Section - Collapsible */}
        <div className="mb-3 border border-dark-600 rounded">
          <button
            onClick={() => setFilesOpen(!filesOpen)}
            className="w-100 d-flex justify-content-between align-items-center bg-dark-800 text-white border-0 px-3 py-3 text-start"
          >
            <span>Files ({agent.files.length})</span>
            <span>{filesOpen ? "▾" : "▸"}</span>
          </button>
          {filesOpen && (
            <div className="p-3 bg-dark-700 border-top border-dark-600">
              <input
                type="file"
                onChange={(e) => { const f = e.target.files?.[0]; if (f) onUploadFile(agent.id, f); }}
                className="d-block w-100 text-sm text-gray-400"
              />
              {agent.files.length > 0 && (
                <ul className="list-unstyled mt-3 mb-0">
                  {agent.files.map((f) => (
                    <li key={f.id} className="text-sm text-gray-300 py-1 border-bottom border-dark-600">
                      {f.name} <span className="text-gray-500 text-xs">({(f.size / 1024).toFixed(1)} KB)</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
