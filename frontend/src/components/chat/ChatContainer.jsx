import { useEffect, useRef, useState } from "react";
import { RotateCcw } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import { sendMessage, startChat } from "../../services/api";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

const STORAGE_KEY = "welfare-chat-v2";

function loadSaved() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved && Array.isArray(saved.messages) && saved.messages.length > 0) {
      return saved;
    }
  } catch {
    // storage unavailable or corrupted: start fresh
  }
  return null;
}

function errorMessage(error) {
  const status = error?.response?.status;

  if (status === 429) {
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

// Turn a server reply into a chat message.
function toMessage(data) {
  return {
    sender: "assistant",
    message: data.reply || "",
    options: data.options || [],
    sources: data.sources || [],
    checklist: data.checklist || null,
  };
}

export default function ChatContainer() {
  const saved = useRef(loadSaved()).current;

  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState(saved?.messages ?? []);
  const [chatState, setChatState] = useState(saved?.chatState ?? null);
  const bottomRef = useRef(null);
  const started = useRef(false);

  // Persist the conversation (messages + server state) in this browser only.
  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ messages: messages.slice(-40), chatState })
      );
    } catch {
      // ignore storage errors
    }
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, chatState, loading]);

  async function begin() {
    setLoading(true);
    try {
      const data = await startChat();
      setMessages([toMessage(data)]);
      setChatState(data.state);
    } catch (error) {
      setMessages([
        { sender: "assistant", message: errorMessage(error), isError: true, options: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // `value` is what is sent to the server; `shown` is what the user sees as their message.
  async function handleSend(value, shown = value) {
    setMessages((prev) => [
      // Buttons only apply to the latest question; remove them once answered.
      ...prev.map((m) => ({ ...m, options: [] })),
      { sender: "user", message: shown },
    ]);
    setLoading(true);

    try {
      const data = await sendMessage(value, chatState);
      setChatState(data.state);
      setMessages((prev) => [...prev, toMessage(data)]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "assistant", message: errorMessage(error), isError: true, options: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // First visit: ask for the language. Deep link /chat?q=... sends that question once.
  const [searchParams, setSearchParams] = useSearchParams();
  useEffect(() => {
    if (started.current) return;
    started.current = true;

    const q = searchParams.get("q");
    if (q) setSearchParams({}, { replace: true });

    if (messages.length === 0) {
      begin();
    } else if (q) {
      handleSend(q.slice(0, 1000));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function restart() {
    setMessages([]);
    setChatState(null);
    begin();
  }

  const lastIndex = messages.length - 1;
  const options = messages[lastIndex]?.options ?? [];

  return (
    <div className="mx-auto flex h-[80vh] max-w-5xl flex-col rounded-2xl bg-slate-100 shadow-lg">
      <div className="flex items-center justify-end border-b px-4 py-2">
        <button
          onClick={restart}
          disabled={loading}
          className="flex items-center gap-1 text-sm text-slate-500 hover:text-red-600 disabled:opacity-40"
        >
          <RotateCcw size={16} /> Start over
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            sender={msg.sender}
            message={msg.message}
            sources={msg.sources}
            checklist={msg.checklist}
          />
        ))}

        {/* Quick-reply buttons for the latest question */}
        {!loading && options.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2 pl-14">
            {options.map((o) => (
              <button
                key={o.value}
                onClick={() => handleSend(o.value, o.label)}
                className={`rounded-full border px-4 py-2 text-sm hover:bg-teal-50 ${
                  o.kind === "cmd"
                    ? "border-slate-400 text-slate-600"
                    : "border-teal-600 bg-white text-teal-700"
                }`}
              >
                {o.label}
              </button>
            ))}
          </div>
        )}

        {loading && <TypingIndicator />}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={(text) => handleSend(text)} disabled={loading || messages.length === 0} />
    </div>
  );
}
