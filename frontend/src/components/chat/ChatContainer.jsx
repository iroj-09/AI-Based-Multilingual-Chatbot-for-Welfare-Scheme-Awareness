import { useState } from "react";

import { sendMessage } from "../../services/api";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

export default function ChatContainer() {

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      message:
        "👋 Hello! I am your AI Welfare Assistant. Ask me about any government welfare scheme.",
    },
  ]);

  async function handleSend(userMessage) {

    // Add user's message immediately
    setMessages((prev) => [
        ...prev,
        {
        sender: "user",
        message: userMessage,
        },
    ]);

    // Show typing indicator
    setLoading(true);

    try {

        const response = await sendMessage(userMessage);

        setMessages((prev) => [
        ...prev,
        {
            sender: "assistant",
            message: response.answer,
        },
        ]);

    } 
    
    catch (error) {

        setMessages((prev) => [
        ...prev,
        {
            sender: "assistant",
            message:
            "Sorry, something went wrong. Please try again.",
        },
        ]);

    } 
    
    finally {

        setLoading(false);

    }

    }

  return (
    <div className="mx-auto flex h-[80vh] max-w-5xl flex-col rounded-2xl bg-slate-100 shadow-lg">

      <div className="flex-1 overflow-y-auto p-6">

        {messages.map((msg, index) => (

          <ChatMessage
            key={index}
            sender={msg.sender}
            message={msg.message}
          />

        ))}

        {loading && <TypingIndicator />}

      </div>

      <ChatInput onSend={handleSend} />

    </div>
  );
}