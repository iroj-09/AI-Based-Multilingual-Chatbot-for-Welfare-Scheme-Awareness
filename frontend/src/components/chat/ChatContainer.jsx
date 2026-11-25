import { useEffect, useRef, useState } from "react";
import { Trash2 } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import { sendMessage } from "../../services/api";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

const STORAGE_KEY = "welfare-chat-history";

const WELCOME = {
  sender: "assistant",
  message:
    "👋 Hello! I am your AI Welfare Assistant. Ask me about any government welfare scheme.",
};

const STARTERS = [
  "What is PM-KISAN?",
  "Schemes for women entrepreneurs",
  "Scholarships for students",
  "किसानों के लिए कौन सी योजनाएं हैं?",
];

function loadMessages() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (Array.isArray(saved) && saved.length > 0) return saved;
  } catch {
    // storage unavailable or corrupted: start fresh
  }
  return [WELCOME];
}

function errorMessage(error) {
  const status = error?.response?.status;

  if (status === 429) {
    // Server explains whether it is the per-user limit or the AI service being busy.
    return (
      error.response.data?.detail ||
      "Too many requests. Please wait a moment and try again."
    );
  }
  if (status === 503) {
    return "The assistant is temporarily unavailable. Please try again shortly.";
  }
  if (!error?.response) {
    return "Cannot reach the server. Please check your connection and try again.";
  }
  return "Sorry, something went wrong. Please try again.";
}

export default function ChatContainer() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState(loadMessages);
  const bottomRef = useRef(null);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.slice(-50)));
    } catch {
      // ignore storage errors
    }
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(userMessage) {
    // Earlier real turns only (skip welcome text and error notices).
    const history = messages
      .filter((m) => m !== WELCOME && !m.isError && m.message !== WELCOME.message)
      .map((m) => ({
        role: m.sender === "user" ? "user" : "assistant",
        content: m.message,
      }));

    setMessages((prev) => [...prev, { sender: "user", message: userMessage }]);
    setLoading(true);

    try {
      const response = await sendMessage(userMessage, history);

      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          message: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "assistant", message: errorMessage(error), isError: true },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function clearChat() {
    setMessages([WELCOME]);
  }

  // Deep link: /chat?q=... sends that question once on first load.
  const [searchParams, setSearchParams] = useSearchParams();
  const autoSent = useRef(false);

  useEffect(() => {
    const q = searchParams.get("q");
    if (q && !autoSent.current) {
      autoSent.current = true;
      setSearchParams({}, { replace: true });
      handleSend(q.slice(0, 1000));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const showStarters = messages.length === 1;

  return (
    <div className="mx-auto flex h-[80vh] max-w-5xl flex-col rounded-2xl bg-slate-100 shadow-lg">
      <div className="flex items-center justify-end border-b px-4 py-2">
        <button
          onClick={clearChat}
          disabled={loading || messages.length === 1}
          className="flex items-center gap-1 text-sm text-slate-500 hover:text-red-600 disabled:opacity-40"
        >
          <Trash2 size={16} /> Clear chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            sender={msg.sender}
            message={msg.message}
            sources={msg.sources}
          />
        ))}

        {showStarters && (
          <div className="flex flex-wrap gap-2">
            {STARTERS.map((s) => (
              <button
                key={s}
                onClick={() => handleSend(s)}
                disabled={loading}
                className="rounded-full border border-teal-600 bg-white px-4 py-2 text-sm text-teal-700 hover:bg-teal-50 disabled:opacity-50"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {loading && <TypingIndicator />}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
