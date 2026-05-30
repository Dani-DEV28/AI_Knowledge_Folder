"use client";

import { useState } from "react";
import { Agent, Chat } from "@/types";

interface SidebarProps {
  agents: Agent[];
  selectedAgentId: string;
  onSelectAgent: (id: string) => void;
  onAddAgent: (name: string) => void;
  chats: Chat[];
  activeChatId: string | null;
  onSelectChat: (id: string) => void;
  onNewChat: () => void;
  adminVisible: boolean;
  onToggleAdmin: () => void;
  onAddUrl: (agentId: string, url: string) => void;
  onUploadFile: (agentId: string, file: File) => void;
  open: boolean;
  onClose: () => void;
}

export default function Sidebar({
  agents,
  selectedAgentId,
  onSelectAgent,
  onAddAgent,
  chats,
  activeChatId,
  onSelectChat,
  onNewChat,
  adminVisible,
  onToggleAdmin,
  onAddUrl,
  onUploadFile,
  open,
  onClose,
}: SidebarProps) {
  const [newAgentName, setNewAgentName] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const selectedAgent = agents.find((a) => a.id === selectedAgentId);

  return (
    <>
      {/* Backdrop overlay on mobile */}
      {open && (
        <div
          className="d-md-none position-fixed top-0 start-0 w-100 h-100"
          style={{ background: "rgba(0,0,0,0.6)", zIndex: 40 }}
          onClick={onClose}
        />
      )}

      <aside
        className={`d-flex flex-column bg-dark-800 border-end border-dark-600 position-fixed position-md-relative h-100 ${
          open ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0 transition-transform`}
        style={{ width: "288px", zIndex: 50 }}
      >
        {/* Close button (mobile only) */}
        <button
          onClick={onClose}
          className="d-md-none position-absolute top-0 end-0 mt-2 me-2 text-gray-400 hover:text-white text-lg bg-transparent border-0"
          aria-label="Close sidebar"
        >
          ✕
        </button>

        {/* Model/Agent Selector */}
        <div className="p-3 border-bottom border-dark-600">
          <select
            value={selectedAgentId}
            onChange={(e) => onSelectAgent(e.target.value)}
            className="w-100 bg-dark-700 text-white border border-dark-500 rounded px-3 py-2 text-sm focus:outline-none focus:border-cyan-500"
          >
            {agents.map((agent) => (
              <option key={agent.id} value={agent.id}>
                {agent.name}
              </option>
            ))}
          </select>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <button
            onClick={onNewChat}
            className="w-100 bg-dark-700 hover:bg-dark-600 border border-dark-500 text-white rounded px-3 py-2 text-sm transition-colors"
          >
            + New Chat
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-grow-1 overflow-auto px-3">
          <p className="text-xs text-gray-400 text-uppercase tracking-wide mb-2">History</p>
          {chats.length === 0 && <p className="text-xs text-gray-500">No chats yet</p>}
          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => { onSelectChat(chat.id); onClose(); }}
              className={`w-100 text-start px-3 py-2 rounded text-sm mb-1 border-0 transition-colors ${
                chat.id === activeChatId ? "bg-dark-600 text-cyan-400" : "text-gray-300 hover:bg-dark-700"
              }`}
            >
              {chat.title}
            </button>
          ))}
        </div>

        {/* Admin Toggle */}
        <div className="border-top border-dark-600 p-3">
          <button
            onClick={onToggleAdmin}
            className="d-flex align-items-center gap-2 text-sm text-gray-400 hover:text-cyan-400 transition-colors bg-transparent border-0"
          >
            <span className={`d-inline-block rounded-circle ${adminVisible ? "bg-cyan-500" : "bg-dark-500"}`} style={{ width: 12, height: 12 }} />
            Admin
          </button>
        </div>

        {/* Admin Panel (per-agent) */}
        {adminVisible && selectedAgent && (
          <div className="border-top border-dark-600 p-3 overflow-auto" style={{ maxHeight: "256px" }}>
            <p className="text-xs text-cyan-400 fw-medium mb-2">{selectedAgent.name} Settings</p>

            {/* Add URL */}
            <div className="mb-3">
              <label className="text-xs text-gray-400">Apify Scrape URL</label>
              <div className="d-flex gap-1 mt-1">
                <input
                  type="url"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  placeholder="https://..."
                  className="flex-grow-1 bg-dark-700 border border-dark-500 rounded px-2 py-1 text-xs text-white focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={() => { if (urlInput) { onAddUrl(selectedAgentId, urlInput); setUrlInput(""); } }}
                  className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-2 py-1 rounded border-0"
                >
                  Add
                </button>
              </div>
              {selectedAgent.urls.length > 0 && (
                <ul className="list-unstyled mt-1">
                  {selectedAgent.urls.map((url, i) => (
                    <li key={i} className="text-xs text-gray-400 text-truncate">{url}</li>
                  ))}
                </ul>
              )}
            </div>

            {/* File Upload */}
            <div className="mb-3">
              <label className="text-xs text-gray-400">Upload File</label>
              <input
                type="file"
                onChange={(e) => { const f = e.target.files?.[0]; if (f) onUploadFile(selectedAgentId, f); }}
                className="mt-1 d-block w-100 text-xs text-gray-400"
              />
              {selectedAgent.files.length > 0 && (
                <ul className="list-unstyled mt-1">
                  {selectedAgent.files.map((f) => (
                    <li key={f.id} className="text-xs text-gray-400 text-truncate">{f.name}</li>
                  ))}
                </ul>
              )}
            </div>

            {/* Add New Agent */}
            <div className="border-top border-dark-600 pt-2">
              <label className="text-xs text-gray-400">Add New Agent</label>
              <div className="d-flex gap-1 mt-1">
                <input
                  value={newAgentName}
                  onChange={(e) => setNewAgentName(e.target.value)}
                  placeholder="Agent name"
                  className="flex-grow-1 bg-dark-700 border border-dark-500 rounded px-2 py-1 text-xs text-white focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={() => { if (newAgentName) { onAddAgent(newAgentName); setNewAgentName(""); } }}
                  className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-2 py-1 rounded border-0"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}
