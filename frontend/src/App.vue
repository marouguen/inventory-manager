<!-- src/App.vue -->
<template>
  <router-view />
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
const auth = useAuthStore();

// If token exists, set default header and fetch user
if (auth.token) {
  axios.defaults.headers.common.Authorization = `Bearer ${auth.token}`;
  auth.fetchUser();
}
</script>
