// src/api/index.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.8.105:8000", // ⬅️ change to your FastAPI backend URL
  withCredentials: false, // Set to true if you're using cookies for auth
});

// Optional: Add auth token automatically if using JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // assumes token is stored in localStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
