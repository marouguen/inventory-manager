import { defineStore } from "pinia";
import api from "@/api";

export const useStockLogStore = defineStore("stockLogs", {
  state: () => ({
    logs: [],
    loading: false,
  }),
  actions: {
    async fetchLogs(filters = {}) {
      this.loading = true;
      const res = await api.get("/stock/logs", { params: filters });
      this.logs = res.data;
      this.loading = false;
    },
    async exportCSV(filters = {}) {
      const res = await api.get("/stock/export", {
        params: filters,
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "stock_logs.csv");
      document.body.appendChild(link);
      link.click();
    },
  },
});
