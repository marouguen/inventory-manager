<template>
  <div class="p-6 space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-semibold">🚚 Suppliers</h2>
      <button @click="openModal()" class="btn-primary">+ Add Supplier</button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto bg-white shadow rounded border border-gray-200">
      <table class="min-w-full text-sm text-left">
        <thead
          class="bg-gray-100 text-xs uppercase text-gray-600 tracking-wider"
        >
          <tr>
            <th class="px-4 py-3">Name</th>
            <th class="px-4 py-3">Email</th>
            <th class="px-4 py-3">Phone</th>
            <th class="px-4 py-3">Address</th>
            <th class="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="supplier in paginatedSuppliers"
            :key="supplier.id"
            class="border-t hover:bg-gray-50"
          >
            <td class="px-4 py-3">{{ supplier.name }}</td>
            <td class="px-4 py-3">{{ supplier.email || "—" }}</td>
            <td class="px-4 py-3">{{ supplier.phone || "—" }}</td>
            <td class="px-4 py-3">{{ supplier.address || "—" }}</td>
            <td class="px-4 py-3 text-right space-x-2">
              <button @click="openModal(supplier)" class="btn-primary">
                Edit
              </button>
              <button @click="deleteSupplier(supplier.id)" class="btn-danger">
                Delete
              </button>
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

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-lg font-bold mb-4">
          {{ editingSupplier ? "Edit" : "Add" }} Supplier
        </h3>
        <form @submit.prevent="saveSupplier" class="space-y-4">
          <div>
            <label class="block mb-1 font-medium">Name</label>
            <input v-model="form.name" class="input" required />
          </div>
          <div>
            <label class="block mb-1 font-medium">Email</label>
            <input v-model="form.email" type="email" class="input" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Phone</label>
            <input v-model="form.phone" class="input" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Address</label>
            <input v-model="form.address" class="input" />
          </div>

          <div class="flex justify-end gap-2">
            <button type="button" @click="closeModal" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "@/api";

const suppliers = ref([]);
const showModal = ref(false);
const editingSupplier = ref(null);

const form = ref({
  name: "",
  email: "",
  phone: "",
  address: "",
});

// Pagination logic
const currentPage = ref(1);
const pageSize = 10;

const totalPages = computed(() => Math.ceil(suppliers.value.length / pageSize));

const paginatedSuppliers = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return suppliers.value.slice(start, start + pageSize);
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

const fetchSuppliers = async () => {
  const res = await axios.get("/suppliers");
  suppliers.value = res.data;
};

const openModal = (supplier = null) => {
  showModal.value = true;
  if (supplier) {
    editingSupplier.value = supplier;
    form.value = { ...supplier };
  } else {
    editingSupplier.value = null;
    form.value = { name: "", email: "", phone: "", address: "" };
  }
};

const closeModal = () => {
  showModal.value = false;
  editingSupplier.value = null;
  form.value = { name: "", email: "", phone: "", address: "" };
};

const saveSupplier = async () => {
  if (editingSupplier.value) {
    await axios.put(`/suppliers/${editingSupplier.value.id}`, form.value);
  } else {
    await axios.post("/suppliers", form.value);
  }
  await fetchSuppliers();
  closeModal();
};

const deleteSupplier = async (id) => {
  if (confirm("Are you sure you want to delete this supplier?")) {
    await axios.delete(`/suppliers/${id}`);
    await fetchSuppliers();
  }
};

onMounted(fetchSuppliers);
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
