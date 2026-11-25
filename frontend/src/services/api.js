import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// history: [{ role: "user" | "assistant", content: string }]
export async function sendMessage(query, history = []) {
  const response = await api.post("/chat", {
    question: query,
    history,
  });

  return response.data; // { answer, sources }
}

export async function checkEligibility(user) {
  const response = await api.post("/eligibility", user);

  return response.data;
}
