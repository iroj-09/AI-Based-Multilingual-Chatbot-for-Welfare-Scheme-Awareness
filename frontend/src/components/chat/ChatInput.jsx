import { useState } from "react";
import { Send } from "lucide-react";

export default function ChatInput({ onSend }) {

  const [text, setText] = useState("");

  function handleSend() {

    if (!text.trim()) return;

    onSend(text);

    setText("");
  }

  return (

    <div className="border-t bg-white p-4">

      <div className="flex gap-3">

        <input
          type="text"
          placeholder="Ask about any government welfare scheme..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          className="flex-1 rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-teal-600"
        />

        <button
          onClick={handleSend}
          className="rounded-xl bg-teal-700 p-3 text-white hover:bg-teal-800"
        >
          <Send size={22} />
        </button>

      </div>

    </div>
  );
}