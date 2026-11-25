import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function ChatMessage({ sender, message, sources }) {

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

          {sources && sources.length > 0 && (
            <div className="mt-3 border-t pt-2 text-xs text-gray-500">
              <p className="mb-1 font-semibold">Related schemes</p>
              <ul className="list-disc pl-4">
                {sources.map((s) => (
                  <li key={`${s.scheme_name}-${s.state}`}>
                    {s.scheme_name}
                    {s.state ? ` (${s.state})` : ""}
                  </li>
                ))}
              </ul>
              <p className="mt-1 italic">
                Please verify details on the official scheme website before applying.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}