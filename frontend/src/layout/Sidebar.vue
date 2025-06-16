<script setup>
import { RouterLink } from "vue-router";
import { useLayoutStore } from "@/stores/layout";
import { useAuthStore } from "@/stores/auth";

const layout = useLayoutStore();
const auth = useAuthStore();
</script>

<template>
  <aside
    :class="[
      'h-screen bg-gray-800 text-white fixed top-0 pt-16 transition-all duration-300 z-40',
      layout.isSidebarCollapsed ? 'w-16' : 'w-64',
    ]"
  >
    <button
      @click="layout.toggleSidebar"
      class="absolute top-4 right-[-12px] bg-gray-700 hover:bg-gray-600 text-white rounded-full p-1 z-50"
    >
      <span v-if="layout.isSidebarCollapsed">➡️</span>
      <span v-else>⬅️</span>
    </button>

    <nav class="flex flex-col space-y-2 px-2 mt-8">
      <!-- Authenticated Links -->
      <template v-if="auth.user">
        <RouterLink to="/" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">🏠 Home</span>
          <span v-else>🏠</span>
        </RouterLink>

        <RouterLink to="/dashboard" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">📊 Dashboard</span>
          <span v-else>📊</span>
        </RouterLink>

        <RouterLink to="/products" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">📦 Products</span>
          <span v-else>📦</span>
        </RouterLink>

        <RouterLink
          to="/categories"
          class="hover:bg-gray-700 px-3 py-2 rounded"
        >
          <span v-if="!layout.isSidebarCollapsed">🗃️ Categories</span>
          <span v-else>🗃️</span>
        </RouterLink>

        <RouterLink to="/suppliers" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">🚚 Suppliers</span>
          <span v-else>🚚</span>
        </RouterLink>

        <RouterLink to="/movements" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">🔀 Movements</span>
          <span v-else>🔀</span>
        </RouterLink>

        <RouterLink to="/logs" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">📋 Stock Logs</span>
          <span v-else>📋</span>
        </RouterLink>

        <RouterLink
          to="/admin/users"
          class="hover:bg-gray-700 px-3 py-2 rounded"
        >
          <span v-if="!layout.isSidebarCollapsed">👤 Users Amin</span>
          <span v-else>👤</span>
        </RouterLink>
      </template>

      <!-- Guest Links -->
      <template v-else>
        <RouterLink to="/" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">🏠 Home</span>
          <span v-else>🏠</span>
        </RouterLink>
        <RouterLink to="/login" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">🔐 Login</span>
          <span v-else>🔐</span>
        </RouterLink>

        <RouterLink to="/register" class="hover:bg-gray-700 px-3 py-2 rounded">
          <span v-if="!layout.isSidebarCollapsed">📝 Register</span>
          <span v-else>📝</span>
        </RouterLink>
      </template>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar-link {
  @apply hover:bg-gray-700 px-3 py-2 rounded transition-all duration-200;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
</style>
