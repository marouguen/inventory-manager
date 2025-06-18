<template>
  <header
    class="fixed top-0 left-0 w-full h-16 bg-gray-900 text-white flex items-center justify-between px-4 z-50"
  >
    <!-- Sidebar Toggle -->
    <div class="flex items-center space-x-4">
      <button
        @click="layout.toggleSidebar"
        class="bg-gray-700 hover:bg-gray-600 text-white rounded-full p-2"
        title="Toggle Sidebar"
      >
        <svg
          v-if="layout.isSidebarCollapsed"
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 5l7 7-7 7"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </button>
      <h1 class="text-lg font-bold hidden md:block">Inventory Manager</h1>
    </div>

    <!-- User Info and Logout -->
    <div class="flex items-center space-x-4" v-if="auth.user">
      <span
        data-testid="user-email"
        class="text-sm text-gray-300 hidden sm:block"
      >
        {{ auth.user.email }}
      </span>
      <button
        data-testid="logout-btn"
        @click="logout"
        class="bg-red-600 hover:bg-red-500 px-3 py-1 text-sm rounded"
      >
        Logout
      </button>
    </div>
  </header>
</template>

<script setup>
import { useLayoutStore } from "@/stores/layout";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const layout = useLayoutStore();
const auth = useAuthStore();
const router = useRouter();

const logout = () => {
  auth.logout();
  router.push("/login");
};
</script>
