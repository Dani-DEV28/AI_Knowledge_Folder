"use client";

import { useState, useRef, useEffect } from "react";
import { Chat } from "@/types";

interface ChatWindowProps {
  chat: Chat | null;
  onSend: (content: string) => void;
  onOpenSidebar: () => void;
}

export default function ChatWindow({ chat, onSend, onOpenSidebar }: ChatWindowProps) {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat?.messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input.trim());
    setInput("");
  };

  return (
    <main className="flex-grow-1 d-flex flex-column bg-dark-900 min-w-0">
      {/* Header with hamburger on mobile */}
      <div className="d-md-none p-3 border-bottom border-dark-700">
        <button
          onClick={onOpenSidebar}
          className="bg-transparent border-0 text-white fs-5"
          aria-label="Open sidebar"
        >
          ☰
        </button>
      </div>

      {/* Messages */}
      <div className="flex-grow-1 overflow-auto p-3 p-md-4">
        {!chat || chat.messages.length === 0 ? (
          <div className="h-100 d-flex align-items-center justify-content-center">
            <p className="text-gray-500 fs-5">Start a conversation</p>
          </div>
        ) : (
          <div className="mx-auto" style={{ maxWidth: "768px" }}>
            {chat.messages.map((msg) => (
              <div
                key={msg.id}
                className={`d-flex mb-3 ${msg.role === "user" ? "justify-content-end" : "justify-content-start"}`}
              >
                <div
                  className={`rounded-3 px-3 py-2 text-sm ${
                    msg.role === "user"
                      ? "bg-cyan-600 text-white"
                      : "bg-dark-700 text-gray-100"
                  }`}
                  style={{ maxWidth: "80%" }}
                >
                  {msg.content}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-top border-dark-500">
                      <p className="text-xs text-gray-400 mb-1">Sources:</p>
                      {msg.sources.map((s, i) => (
                        <p key={i} className="text-xs text-cyan-400 mb-0">{s.title}</p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-3 p-md-4 border-top border-dark-700">
        <div className="mx-auto d-flex gap-2" style={{ maxWidth: "768px" }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-grow-1 bg-dark-700 border border-dark-500 rounded-3 px-3 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
          />
          <button
            type="submit"
            className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-3 border-0 transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </main>
  );
}
