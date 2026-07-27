import axios from "axios";


const api = axios.create({
  baseURL: "https://ai-based-multilingual-chatbot-for-welfare-scheme-production.up.railway.app/",
});

export async function sendMessage(query) {
  const response = await api.post("/chat", {
    question: query,
  });

  return response.data;
}

export default api;