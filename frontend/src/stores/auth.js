// src/stores/auth.js
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);

      const res = await axios.post("http://127.0.0.1:8000/login", form);
      this.token = res.data.access_token;
      localStorage.setItem("token", this.token);

      // Set default auth header
      axios.defaults.headers.common.Authorization = `Bearer ${this.token}`;

      // Fetch user info immediately after login
      await this.fetchUser();
    },

    async fetchUser() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/users/me");
        this.user = res.data;
      } catch (error) {
        console.error("Failed to fetch user", error);
        this.logout(); // Optional: force logout on failure
      }
    },

    async register(email, password) {
      await axios.post("http://127.0.0.1:8000/register", {
        email,
        password,
      });
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
      delete axios.defaults.headers.common.Authorization;
    },
  },
});
