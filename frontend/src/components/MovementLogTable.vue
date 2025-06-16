<template>
  <div class="p-6 space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-2xl font-semibold">📦 Recent Stock Movements</h3>
    </div>

    <div class="overflow-x-auto bg-white shadow rounded border border-gray-200">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-100 text-xs uppercase text-gray-600">
          <tr>
            <th class="px-4 py-3">Product ID</th>
            <th class="px-4 py-3">Quantity</th>
            <th class="px-4 py-3">Type</th>
            <th class="px-4 py-3">User ID</th>
            <th class="px-4 py-3">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="log in paginatedLogs"
            :key="log.id"
            class="border-t hover:bg-gray-50 even:bg-gray-50"
          >
            <td class="px-4 py-3">{{ log.product_id }}</td>
            <td class="px-4 py-3">{{ log.quantity }}</td>
            <td class="px-4 py-3 capitalize">{{ log.type }}</td>
            <td class="px-4 py-3">{{ log.user_id }}</td>
            <td class="px-4 py-3">
              {{ new Date(log.timestamp).toLocaleString() }}
            </td>
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
import { useMovementStore } from "@/stores/movement";
import { computed, ref, onMounted } from "vue";

const movement = useMovementStore();
const currentPage = ref(1);
const pageSize = 10;

const totalPages = computed(() => Math.ceil(movement.logs.length / pageSize));

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return movement.logs.slice(start, start + pageSize);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

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

onMounted(() => {
  movement.fetchLogs();
});
</script>

<style scoped>
.input {
  @apply w-full p-2 border rounded;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white p-6 rounded shadow-lg w-full max-w-md;
}

.btn-primary {
  @apply bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700;
}

.btn-danger {
  @apply bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700;
}

.btn-cancel {
  @apply bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400;
}
</style>
