import axios from "axios";

console.log("VITE_API_URL:", import.meta.env.VITE_API_URL);

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export async function sendMessage(query) {
  console.log("Base URL:", api.defaults.baseURL);

  const response = await api.post("/chat", {
    question: query,
  });

  return response.data;
}