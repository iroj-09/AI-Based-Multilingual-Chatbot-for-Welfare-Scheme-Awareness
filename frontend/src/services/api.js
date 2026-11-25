import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// First message of a conversation (language choice).
export async function startChat() {
  const response = await api.post("/chat/start");

  return response.data; // { reply, state, options, sources, checklist }
}

// `state` is the conversation state returned by the previous reply.
export async function sendMessage(message, state) {
  const response = await api.post("/chat", { message, state });

  return response.data;
}
