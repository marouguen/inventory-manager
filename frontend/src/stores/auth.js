import { defineStore } from "pinia";
import api, { setupInterceptors } from "@/api";

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

      const res = await api.post("/login", form);
      this.token = res.data.access_token;
      localStorage.setItem("token", this.token);

      setupInterceptors(this.token); // ✅ Apply after login
      await this.fetchUser();
    },

    async fetchUser() {
      try {
        const res = await api.get("/users/me");
        this.user = res.data;
      } catch (error) {
        console.error("Failed to fetch user", error);
        this.logout();
      }
    },

    async register(email, password) {
      await api.post("/register", {
        email,
        password,
      });
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
    },
  },
});
