<template>
  <div class="p-6 space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-semibold">📂 Categories</h2>
      <button @click="openCreateModal" class="btn-primary">
        + New Category
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto bg-white shadow rounded border border-gray-200">
      <table class="min-w-full text-sm text-left">
        <thead class="bg-gray-100 text-gray-700 uppercase tracking-wider">
          <tr>
            <th class="p-3">ID</th>
            <th class="p-3">Name</th>
            <th class="p-3">Description</th>
            <th class="p-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="cat in paginatedCategories"
            :key="cat.id"
            class="border-t hover:bg-gray-50"
          >
            <td class="p-3">{{ cat.id }}</td>
            <td class="p-3">{{ cat.name }}</td>
            <td class="p-3">{{ cat.description }}</td>
            <td class="p-3 text-right space-x-2">
              <button @click="openEditModal(cat)" class="btn-primary">
                Edit
              </button>
              <button @click="deleteCategory(cat.id)" class="btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
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

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-lg font-semibold mb-4">
          {{ editMode ? "Edit" : "Create" }} Category
        </h3>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block mb-1 font-medium">Name</label>
            <input v-model="form.name" class="input" required />
          </div>
          <div>
            <label class="block mb-1 font-medium">Description</label>
            <input v-model="form.description" class="input" />
          </div>
          <div class="flex justify-end gap-3">
            <button type="button" @click="closeModal" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              {{ editMode ? "Update" : "Create" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/api";

const categories = ref([]);
const showModal = ref(false);
const editMode = ref(false);
const form = ref({
  id: null,
  name: "",
  description: "",
});

// Pagination
const currentPage = ref(1);
const pageSize = 10;
const totalPages = computed(() =>
  Math.ceil(categories.value.length / pageSize)
);

const paginatedCategories = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return categories.value.slice(start, start + pageSize);
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

const fetchCategories = async () => {
  const res = await api.get("/categories");
  categories.value = res.data;
};

const openCreateModal = () => {
  editMode.value = false;
  form.value = { id: null, name: "", description: "" };
  showModal.value = true;
};

const openEditModal = (cat) => {
  editMode.value = true;
  form.value = { ...cat };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const submitForm = async () => {
  if (editMode.value) {
    await api.put(`/categories/${form.value.id}`, form.value);
  } else {
    await api.post("/categories", {
      name: form.value.name,
      description: form.value.description,
    });
  }
  closeModal();
  fetchCategories();
};

const deleteCategory = async (id) => {
  if (confirm("Are you sure?")) {
    await api.delete(`/categories/${id}`);
    fetchCategories();
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.input {
  @apply w-full p-2 border rounded;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50;
}

.modal-content {
  @apply bg-white p-6 rounded shadow-lg w-full max-w-md;
}

.btn-primary {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
}

.btn-danger {
  @apply bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700;
}

.btn-light {
  @apply bg-gray-100 text-black px-4 py-2 rounded hover:bg-gray-200;
}

.btn-cancel {
  @apply bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400;
}
</style>
