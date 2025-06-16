// src/api/auth.js
import api from "@/api";

// ✅ Send as application/x-www-form-urlencoded for FastAPI OAuth2PasswordRequestForm
export const login = ({ email, password }) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // FastAPI expects "username"
  formData.append("password", password);

  return api.post("/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export const register = (data) => {
  return api.post("/register", data); // This stays as JSON
};
