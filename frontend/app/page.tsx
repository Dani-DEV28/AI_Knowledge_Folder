"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import AgentManager from "@/components/AgentManager";
import { Agent, Chat, Message } from "@/types";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [agents, setAgents] = useState<Agent[]>([
    { id: "rcw-navigator", name: "RCW Navigator AI", description: "Washington State law assistant", urls: [], files: [] },
  ]);
  const [selectedAgentId, setSelectedAgentId] = useState("rcw-navigator");
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [adminVisible, setAdminVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [view, setView] = useState<"chat" | "manage">("chat");

  const activeChat = chats.find((c) => c.id === activeChatId) || null;
  const selectedAgent = agents.find((a) => a.id === selectedAgentId)!;

  const handleNewChat = () => {
    const chat: Chat = {
      id: Date.now().toString(),
      title: "New Chat",
      agentId: selectedAgentId,
      messages: [],
      createdAt: Date.now(),
    };
    setChats((prev) => [chat, ...prev]);
    setActiveChatId(chat.id);
    return chat.id;
  };

  const handleSendMessage = async (content: string) => {
    // Create a new chat if none is active
    let chatId = activeChatId;
    if (!chatId) {
      chatId = handleNewChat();
    }

    // Add user message immediately
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: Date.now(),
    };
    setChats((prev) =>
      prev.map((c) => (c.id === chatId ? { ...c, messages: [...c.messages, userMsg] } : c))
    );

    // Call the backend /chat endpoint
    try {
      // Build history from current chat messages
      const currentChat = chats.find((c) => c.id === chatId);
      const history = (currentChat?.messages || []).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ assistant_id: selectedAgentId, question: content, history }),
      });
      const data = await res.json();

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer,
        sources: data.sources?.map((s: { source_title: string; source_url: string }) => ({
          title: s.source_title,
          url: s.source_url,
        })),
        timestamp: Date.now(),
      };
      setChats((prev) =>
        prev.map((c) => (c.id === chatId ? { ...c, messages: [...c.messages, assistantMsg] } : c))
      );
    } catch {
      const errMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I could not reach the backend. Make sure the server is running on port 8000.",
        timestamp: Date.now(),
      };
      setChats((prev) =>
        prev.map((c) => (c.id === chatId ? { ...c, messages: [...c.messages, errMsg] } : c))
      );
    }
  };

  const handleAddAgent = async (name: string) => {
    // Create assistant in backend
    try {
      const res = await fetch(`${API}/assistants`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description: "", folder_name: name.toLowerCase().replace(/\s+/g, "-") }),
      });
      const data = await res.json();
      const agent: Agent = {
        id: data.assistant_id,
        name: data.name,
        description: "",
        urls: [],
        files: [],
      };
      setAgents((prev) => [...prev, agent]);
      setSelectedAgentId(agent.id);
    } catch {
      // Fallback to local only
      const agent: Agent = { id: Date.now().toString(), name, description: "", urls: [], files: [] };
      setAgents((prev) => [...prev, agent]);
      setSelectedAgentId(agent.id);
    }
  };

  const handleAddUrl = (agentId: string, url: string) => {
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, urls: [...a.urls, url] } : a))
    );
  };

  const handleAddUrlWithPrompt = async (agentId: string, url: string, _prompt: string) => {
    // Trigger Apify crawl in backend — waits for completion and auto-ingests
    let result = { pages_ingested: 0, status: "error" };
    try {
      const res = await fetch(`${API}/sources/website`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ assistant_id: agentId, url }),
      });
      result = await res.json();
    } catch {
      throw new Error("Crawl request failed");
    }
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, urls: [...a.urls, url] } : a))
    );
    return result;
  };

  const handleUploadFile = async (agentId: string, file: File) => {
    // Upload file to Box via backend
    const formData = new FormData();
    formData.append("assistant_id", agentId);
    formData.append("file", file);
    const res = await fetch(`${API}/sources/upload`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Upload failed");
    const uploaded = { id: Date.now().toString(), name: file.name, size: file.size, uploadedAt: Date.now() };
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, files: [...a.files, uploaded] } : a))
    );
  };

  const handleDeleteUrl = async (agentId: string, urlIndex: number) => {
    // Find the source in metadata and delete from Box
    const url = agents.find((a) => a.id === agentId)?.urls[urlIndex];
    if (url) {
      try {
        // Get sources to find the matching one
        const res = await fetch(`${API}/sources?assistant_id=${agentId}`);
        const sources = await res.json();
        const match = sources.find((s: { source_url: string }) => s.source_url === url);
        if (match) {
          await fetch(`${API}/sources/${match.id}?assistant_id=${agentId}`, { method: "DELETE" });
        }
      } catch {
        // Continue with UI removal even if backend fails
      }
    }
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, urls: a.urls.filter((_, i) => i !== urlIndex) } : a))
    );
  };

  const handleDeleteFile = async (agentId: string, fileId: string) => {
    try {
      // Get sources to find the matching one by filename
      const file = agents.find((a) => a.id === agentId)?.files.find((f) => f.id === fileId);
      if (file) {
        const res = await fetch(`${API}/sources?assistant_id=${agentId}`);
        const sources = await res.json();
        const match = sources.find((s: { file_name: string }) => s.file_name === file.name);
        if (match) {
          await fetch(`${API}/sources/${match.id}?assistant_id=${agentId}`, { method: "DELETE" });
        }
      }
    } catch {
      // Continue with UI removal even if backend fails
    }
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, files: a.files.filter((f) => f.id !== fileId) } : a))
    );
  };

  return (
    <div className="d-flex vh-100">
      <Sidebar
        agents={agents}
        selectedAgentId={selectedAgentId}
        onSelectAgent={setSelectedAgentId}
        onAddAgent={handleAddAgent}
        chats={chats.filter((c) => c.agentId === selectedAgentId)}
        activeChatId={activeChatId}
        onSelectChat={(id) => { setActiveChatId(id); setView("chat"); }}
        onNewChat={() => { handleNewChat(); setView("chat"); }}
        adminVisible={adminVisible}
        onToggleAdmin={() => setAdminVisible(!adminVisible)}
        onAddUrl={handleAddUrl}
        onUploadFile={handleUploadFile}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onManage={() => { setView("manage"); setSidebarOpen(false); }}
      />
      {view === "manage" ? (
        <AgentManager
          agent={selectedAgent}
          onAddUrl={handleAddUrlWithPrompt}
          onUploadFile={handleUploadFile}
          onDeleteUrl={handleDeleteUrl}
          onDeleteFile={handleDeleteFile}
          onBack={() => setView("chat")}
        />
      ) : (
        <ChatWindow chat={activeChat} onSend={handleSendMessage} onOpenSidebar={() => setSidebarOpen(true)} />
      )}
    </div>
  );
}
