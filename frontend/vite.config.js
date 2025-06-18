import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)), // ✅ Ensures @ = src/
    },
  },
  plugins: [vue()],
  test: {
    globals: true,
    environment: "jsdom",
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
