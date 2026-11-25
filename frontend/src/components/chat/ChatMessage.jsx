import { useState } from "react";
import { Bot, User, Download, Copy, Check } from "lucide-react";
import ReactMarkdown from "react-markdown";

function Checklist({ checklist }) {
  const [copied, setCopied] = useState(false);

  function download() {
    const blob = new Blob([checklist.text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = checklist.filename;
    link.click();
    URL.revokeObjectURL(url);
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(checklist.sms);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard blocked: the full text is still available via Download
    }
  }

  return (
    <div className="mt-3 flex flex-wrap gap-2">
      <button
        onClick={download}
        className="flex items-center gap-1 rounded-lg bg-teal-700 px-3 py-2 text-sm text-white hover:bg-teal-800"
      >
        <Download size={16} /> {checklist.labels.download}
      </button>
      <button
        onClick={copy}
        className="flex items-center gap-1 rounded-lg border border-teal-700 px-3 py-2 text-sm text-teal-700 hover:bg-teal-50"
      >
        {copied ? <Check size={16} /> : <Copy size={16} />}
        {copied ? checklist.labels.copied : checklist.labels.copy}
      </button>
    </div>
  );
}

export default function ChatMessage({ sender, message, sources, checklist }) {
  const isUser = sender === "user";

  return (
    <div className={`mb-6 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex max-w-3xl gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
        {/* Avatar */}
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
            isUser ? "bg-teal-700 text-white" : "bg-gray-200 text-gray-700"
          }`}
        >
          {isUser ? <User size={20} /> : <Bot size={20} />}
        </div>

        {/* Message */}
        <div
          className={`min-w-0 rounded-2xl px-5 py-4 shadow ${
            isUser ? "bg-teal-700 text-white" : "border bg-white text-gray-800"
          }`}
        >
          {/* dir="auto" lets right-to-left languages such as Urdu display correctly */}
          <div dir="auto" className="whitespace-pre-wrap break-words leading-7">
            <ReactMarkdown>{message}</ReactMarkdown>
          </div>

          {checklist && <Checklist checklist={checklist} />}

          {sources && sources.length > 0 && (
            <div className="mt-3 border-t pt-2 text-xs text-gray-500">
              <ul className="list-disc pl-4">
                {sources.map((s) => (
                  <li key={`${s.scheme_name}-${s.state}`}>
                    {s.scheme_name}
                    {s.state ? ` (${s.state})` : ""}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
