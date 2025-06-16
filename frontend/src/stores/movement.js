// src/stores/movement.js
import { defineStore } from "pinia";
import axios from "axios";

export const useMovementStore = defineStore("movement", {
  state: () => ({
    logs: [],
    loading: false,
  }),
  actions: {
    async fetchLogs() {
      this.loading = true;
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/stock/logs?limit=10"
        );
        this.logs = res.data;
      } catch (e) {
        console.error("Failed to fetch logs", e);
      } finally {
        this.loading = false;
      }
    },
    async submitMovement({ product_id, quantity, type }) {
      const url = `http://127.0.0.1:8000/stock/${type}`;
      await axios.post(url, { product_id, quantity, type });
      await this.fetchLogs();
    },
  },
});
