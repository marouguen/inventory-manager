import { defineStore } from "pinia";
import api from "@/api"; // ✅ use centralized axios instance

export const useMovementStore = defineStore("movement", {
  state: () => ({
    logs: [],
    loading: false,
  }),
  actions: {
    async fetchLogs() {
      this.loading = true;
      try {
        const res = await api.get("/stock/logs?limit=10");
        this.logs = res.data;
      } catch (e) {
        console.error("Failed to fetch logs", e);
      } finally {
        this.loading = false;
      }
    },
    async submitMovement({ product_id, quantity, type }) {
      const url = `/stock/${type}`;
      await api.post(url, { product_id, quantity, type });
      await this.fetchLogs();
    },
  },
});
