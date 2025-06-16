<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main -->
    <div
      :class="[
        'flex-1 flex flex-col transition-all duration-300',
        layout.isSidebarCollapsed ? 'ml-16' : 'ml-64',
      ]"
    >
      <!-- ✅ Header with toggle -->
      <Header />

      <!-- Page Content -->
      <main class="pt-16 px-4 flex-1 overflow-auto bg-gray-50">
        <router-view />
      </main>

      <!-- Footer -->
      <Footer />
    </div>
  </div>
</template>

<script setup>
import Sidebar from "./Sidebar.vue";
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import { useLayoutStore } from "@/stores/layout";

const layout = useLayoutStore();
</script>
