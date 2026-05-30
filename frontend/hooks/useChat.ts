import { useState } from "react";
import { Message } from "@/types";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (content: string, agentId: string) => {
    const userMsg: Message = { id: Date.now().toString(), role: "user", content, timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      // TODO: Replace with actual API call
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: content, agentId }),
      });
      const data = await res.json();
      const assistantMsg: Message = { id: (Date.now() + 1).toString(), role: "assistant", content: data.answer, sources: data.sources, timestamp: Date.now() };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      // Handle error silently for now
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, sendMessage };
}
