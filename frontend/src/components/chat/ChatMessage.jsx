import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function ChatMessage({ sender, message }) {

  const isUser = sender === "user";

  return (

    <div
      className={`mb-6 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >

      <div
        className={`flex max-w-3xl gap-3 ${
          isUser ? "flex-row-reverse" : ""
        }`}
      >

        {/* Avatar */}

        <div
          className={`flex h-10 w-10 items-center justify-center rounded-full
          ${
            isUser
              ? "bg-teal-700 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >

          {isUser ? <User size={20} /> : <Bot size={20} />}

        </div>

        {/* Message */}

        <div
          className={`rounded-2xl px-5 py-4 shadow
          ${
            isUser
              ? "bg-teal-700 text-white"
              : "border bg-white text-gray-800"
          }`}
        >

          <div className="leading-7 whitespace-pre-wrap">
            <ReactMarkdown>
                {message}
            </ReactMarkdown>
          </div>

        </div>

      </div>

    </div>
  );
}