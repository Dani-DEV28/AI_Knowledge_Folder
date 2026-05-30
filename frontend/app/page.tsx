"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import { Agent, Chat, Message } from "@/types";

export default function Home() {
  const [agents, setAgents] = useState<Agent[]>([
    { id: "1", name: "RCW Navigator AI", description: "Washington State law assistant", urls: [], files: [] },
  ]);
  const [selectedAgentId, setSelectedAgentId] = useState("1");
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [adminVisible, setAdminVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeChat = chats.find((c) => c.id === activeChatId) || null;

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
  };

  const handleSendMessage = (content: string) => {
    if (!activeChatId) {
      handleNewChat();
    }
    const chatId = activeChatId || chats[0]?.id;
    if (!chatId) return;

    const userMsg: Message = { id: Date.now().toString(), role: "user", content, timestamp: Date.now() };
    setChats((prev) =>
      prev.map((c) => (c.id === chatId ? { ...c, messages: [...c.messages, userMsg] } : c))
    );
  };

  const handleAddAgent = (name: string) => {
    const agent: Agent = { id: Date.now().toString(), name, description: "", urls: [], files: [] };
    setAgents((prev) => [...prev, agent]);
    setSelectedAgentId(agent.id);
  };

  const handleAddUrl = (agentId: string, url: string) => {
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, urls: [...a.urls, url] } : a))
    );
  };

  const handleUploadFile = (agentId: string, file: File) => {
    const uploaded = { id: Date.now().toString(), name: file.name, size: file.size, uploadedAt: Date.now() };
    setAgents((prev) =>
      prev.map((a) => (a.id === agentId ? { ...a, files: [...a.files, uploaded] } : a))
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
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
        adminVisible={adminVisible}
        onToggleAdmin={() => setAdminVisible(!adminVisible)}
        onAddUrl={handleAddUrl}
        onUploadFile={handleUploadFile}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <ChatWindow chat={activeChat} onSend={handleSendMessage} onOpenSidebar={() => setSidebarOpen(true)} />
    </div>
  );
}
