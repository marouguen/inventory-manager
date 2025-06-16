<template>
  <div class="p-4 space-y-4">
    <div class="flex justify-between items-center">
      <h1 class="text-xl font-bold">Stock Logs</h1>
      <button
        @click="exportCSV"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-500"
      >
        Export CSV
      </button>
    </div>

    <div class="overflow-x-auto bg-white shadow rounded border border-gray-200">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-100 text-xs uppercase text-gray-600">
          <tr>
            <th class="px-4 py-2">Product ID</th>
            <th class="px-4 py-2">Type</th>
            <th class="px-4 py-2">Quantity</th>
            <th class="px-4 py-2">User ID</th>
            <th class="px-4 py-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="log in paginatedLogs"
            :key="log.id"
            class="border-t hover:bg-gray-50 even:bg-gray-50"
          >
            <td class="px-4 py-2">{{ log.product_id }}</td>
            <td class="px-4 py-2 capitalize">{{ log.type }}</td>
            <td class="px-4 py-2">{{ log.quantity }}</td>
            <td class="px-4 py-2">{{ log.user_id }}</td>
            <td class="px-4 py-2">{{ formatDate(log.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div class="flex justify-between items-center pt-4">
      <p class="text-sm text-gray-600">
        Page {{ currentPage }} of {{ totalPages }}
      </p>
      <div class="space-x-2 flex flex-wrap items-center">
        <button
          @click="goToPage(1)"
          :disabled="currentPage === 1"
          class="btn-light"
        >
          ⏮ First
        </button>
        <button
          @click="skipPages(-10)"
          :disabled="currentPage <= 10"
          class="btn-light"
        >
          ⏪ -10
        </button>
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="btn-light"
        >
          ◀ Prev
        </button>
        <span class="px-2 text-sm font-medium">{{ currentPage }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="btn-light"
        >
          Next ▶
        </button>
        <button
          @click="skipPages(10)"
          :disabled="currentPage + 10 > totalPages"
          class="btn-light"
        >
          +10 ⏩
        </button>
        <button
          @click="goToPage(totalPages)"
          :disabled="currentPage === totalPages"
          class="btn-light"
        >
          Last ⏭
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useStockLogStore } from "@/stores/stockLogs";
import dayjs from "dayjs";

const store = useStockLogStore();

const currentPage = ref(1);
const pageSize = 15;

const totalPages = computed(() => Math.ceil(store.logs.length / pageSize));

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return store.logs.slice(start, start + pageSize);
});

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++;
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--;
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const skipPages = (offset) => {
  const newPage = currentPage.value + offset;
  if (newPage >= 1 && newPage <= totalPages.value) {
    currentPage.value = newPage;
  } else if (newPage < 1) {
    currentPage.value = 1;
  } else {
    currentPage.value = totalPages.value;
  }
};

function formatDate(date) {
  return dayjs(date).format("YYYY-MM-DD HH:mm");
}

function exportCSV() {
  store.exportCSV();
}

onMounted(() => {
  store.fetchLogs();
});
</script>
