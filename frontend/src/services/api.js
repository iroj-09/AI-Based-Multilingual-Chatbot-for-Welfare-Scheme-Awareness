import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:5000",
});

export async function sendMessage(query) {
  const response = await api.post("/chat", {
    question: query,
  });

  return response.data;
}

export default api;

