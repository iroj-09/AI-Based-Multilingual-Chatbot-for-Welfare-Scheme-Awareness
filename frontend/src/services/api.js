import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export async function sendMessage(query) {
  const response = await api.post("/chat", {
    question: query,
  });

  return response.data;
}

export default api;

