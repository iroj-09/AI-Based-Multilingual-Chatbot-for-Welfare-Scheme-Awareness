import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export async function sendMessage(query) {
  const response = await api.post("/chat", {
    question: query,
  });

  return response.data;
}

export async function checkEligibility(user) {
  const response = await api.post("/eligibility", user);

  return response.data;
}
