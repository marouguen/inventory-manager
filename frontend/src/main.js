// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import "./style.css";
import { setupInterceptors } from "@/api";

const token = localStorage.getItem("token");
if (token) {
  setupInterceptors(token); // ✅ Apply at startup for persisted sessions
}

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");
