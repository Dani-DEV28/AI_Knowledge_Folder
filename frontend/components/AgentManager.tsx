"use client";

import { useState } from "react";
import { Agent } from "@/types";

interface AgentManagerProps {
  agent: Agent;
  onAddUrl: (agentId: string, url: string, prompt: string) => Promise<{ pages_ingested?: number; status?: string }>;
  onUploadFile: (agentId: string, file: File) => Promise<void>;
  onDeleteUrl: (agentId: string, urlIndex: number) => void;
  onDeleteFile: (agentId: string, fileId: string) => void;
  onBack: () => void;
}

export default function AgentManager({ agent, onAddUrl, onUploadFile, onDeleteUrl, onDeleteFile, onBack }: AgentManagerProps) {
  const [urlOpen, setUrlOpen] = useState(true);
  const [filesOpen, setFilesOpen] = useState(true);
  const [urlInput, setUrlInput] = useState("");
  const [crawlStatus, setCrawlStatus] = useState<"idle" | "crawling" | "done" | "error">("idle");
  const [crawlMessage, setCrawlMessage] = useState("");
  const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "done" | "error">("idle");
  const [uploadMessage, setUploadMessage] = useState("");

  const handleAddUrl = async () => {
    if (!urlInput.trim()) return;
    setCrawlStatus("crawling");
    setCrawlMessage("Crawling website... this may take 1–2 minutes.");
    try {
      const result = await onAddUrl(agent.id, urlInput.trim(), "");
      const pages = result?.pages_ingested ?? 0;
      setCrawlStatus("done");
      setCrawlMessage(`✓ Crawl complete — ${pages} page${pages !== 1 ? "s" : ""} ingested into knowledge base.`);
      setUrlInput("");
    } catch {
      setCrawlStatus("error");
      setCrawlMessage("✕ Crawl failed. Check the URL and try again.");
    }
  };

  const handleUpload = async (file: File) => {
    setUploadStatus("uploading");
    setUploadMessage(`Uploading ${file.name}...`);
    try {
      await onUploadFile(agent.id, file);
      setUploadStatus("done");
      setUploadMessage(`✓ ${file.name} uploaded to Box.`);
    } catch {
      setUploadStatus("error");
      setUploadMessage(`✕ Upload failed for ${file.name}.`);
    }
  };

  return (
    <main className="flex-grow-1 d-flex flex-column bg-dark-900 min-w-0 overflow-auto">
      {/* Header */}
      <div className="p-3 border-bottom border-dark-700 d-flex align-items-center gap-3">
        <button onClick={onBack} className="bg-transparent border-0 text-cyan-400 text-sm">
          ← Back to Chat
        </button>
        <span className="text-gray-400 text-sm">|</span>
        <span className="text-white text-sm fw-medium">{agent.name} — Knowledge Sources</span>
      </div>

      <div className="p-4 mx-auto w-100" style={{ maxWidth: "700px" }}>

        {/* URL / Website Crawl Section */}
        <div className="mb-4 border border-dark-600 rounded">
          <button
            onClick={() => setUrlOpen(!urlOpen)}
            className="w-100 d-flex justify-content-between align-items-center bg-dark-800 text-white border-0 px-3 py-3 text-start"
          >
            <span className="fw-medium">🌐 Website URLs ({agent.urls.length})</span>
            <span>{urlOpen ? "▾" : "▸"}</span>
          </button>

          {urlOpen && (
            <div className="p-3 bg-dark-700 border-top border-dark-600">
              <p className="text-xs text-gray-400 mb-2">
                Enter a URL to crawl. The content will be ingested into the knowledge base and used to answer questions.
              </p>

              <div className="d-flex gap-2 mb-2">
                <input
                  type="url"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAddUrl()}
                  placeholder="https://app.leg.wa.gov/rcw/..."
                  disabled={crawlStatus === "crawling"}
                  className="flex-grow-1 bg-dark-800 border border-dark-500 rounded px-3 py-2 text-sm text-white"
                />
                <button
                  onClick={handleAddUrl}
                  disabled={crawlStatus === "crawling" || !urlInput.trim()}
                  className="bg-cyan-600 text-white text-sm px-3 py-2 rounded border-0"
                  style={{ minWidth: "100px" }}
                >
                  {crawlStatus === "crawling" ? (
                    <span>⏳ Crawling…</span>
                  ) : (
                    <span>Crawl & Ingest</span>
                  )}
                </button>
              </div>

              {/* Crawl status message */}
              {crawlStatus !== "idle" && (
                <div className={`text-xs px-2 py-2 rounded mb-2 ${
                  crawlStatus === "crawling" ? "text-yellow-400 bg-dark-800" :
                  crawlStatus === "done" ? "text-green-400 bg-dark-800" :
                  "text-red-400 bg-dark-800"
                }`}>
                  {crawlMessage}
                </div>
              )}

              {/* URL list */}
              {agent.urls.length > 0 && (
                <ul className="list-unstyled mt-2 mb-0">
                  {agent.urls.map((url, i) => (
                    <li key={i} className="d-flex justify-content-between align-items-center text-xs text-gray-300 py-1 border-bottom border-dark-600">
                      <span className="text-truncate me-2">{url}</span>
                      <button
                        onClick={() => onDeleteUrl(agent.id, i)}
                        className="bg-transparent border-0 text-danger text-xs flex-shrink-0"
                        aria-label={`Remove ${url}`}
                      >
                        ✕
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        {/* File Upload Section */}
        <div className="mb-4 border border-dark-600 rounded">
          <button
            onClick={() => setFilesOpen(!filesOpen)}
            className="w-100 d-flex justify-content-between align-items-center bg-dark-800 text-white border-0 px-3 py-3 text-start"
          >
            <span className="fw-medium">📄 Documents ({agent.files.length})</span>
            <span>{filesOpen ? "▾" : "▸"}</span>
          </button>

          {filesOpen && (
            <div className="p-3 bg-dark-700 border-top border-dark-600">
              <p className="text-xs text-gray-400 mb-2">
                Upload PDF, DOCX, TXT, or JSON files. They will be stored in Box and added to the knowledge base.
              </p>

              <input
                type="file"
                accept=".pdf,.docx,.txt,.json"
                disabled={uploadStatus === "uploading"}
                onChange={(e) => { const f = e.target.files?.[0]; if (f) handleUpload(f); }}
                className="d-block w-100 text-sm text-gray-400 mb-2"
              />

              {/* Upload status message */}
              {uploadStatus !== "idle" && (
                <div className={`text-xs px-2 py-2 rounded mb-2 ${
                  uploadStatus === "uploading" ? "text-yellow-400 bg-dark-800" :
                  uploadStatus === "done" ? "text-green-400 bg-dark-800" :
                  "text-red-400 bg-dark-800"
                }`}>
                  {uploadMessage}
                </div>
              )}

              {/* File list */}
              {agent.files.length > 0 && (
                <ul className="list-unstyled mt-2 mb-0">
                  {agent.files.map((f) => (
                    <li key={f.id} className="d-flex justify-content-between align-items-center text-xs text-gray-300 py-1 border-bottom border-dark-600">
                      <span>{f.name} <span className="text-gray-500">({(f.size / 1024).toFixed(1)} KB)</span></span>
                      <button
                        onClick={() => onDeleteFile(agent.id, f.id)}
                        className="bg-transparent border-0 text-danger text-xs flex-shrink-0"
                        aria-label={`Remove ${f.name}`}
                      >
                        ✕
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        {/* Legal disclaimer */}
        <p className="text-xs text-gray-500 text-center mt-4">
          RCW Navigator AI summarizes public legal information for educational purposes only. It does not provide legal advice.
        </p>
      </div>
    </main>
  );
}
