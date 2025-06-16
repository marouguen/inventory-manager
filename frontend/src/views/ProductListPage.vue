<template>
  <div class="p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">📦 Product List</h1>
      <button
        @click="createModalOpen = true"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-500"
      >
        + Create Product
      </button>
    </div>

    <!-- Products Table -->
    <div
      class="overflow-x-auto bg-white shadow rounded border border-gray-200 scroll-smooth"
    >
      <table class="min-w-full text-sm text-left">
        <thead class="bg-gray-100 text-gray-700 uppercase tracking-wider">
          <tr>
            <th class="p-3">Name</th>
            <th class="p-3">SKU</th>
            <th class="p-3">Barcode</th>
            <th class="p-3">Qty</th>
            <th class="p-3">Unit</th>
            <th class="p-3">Category</th>
            <th class="p-3">Supplier</th>
            <th class="p-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="product in paginatedProducts"
            :key="product.id"
            class="border-t hover:bg-gray-50"
          >
            <td class="p-3">{{ product.name }}</td>
            <td class="p-3">{{ product.sku }}</td>
            <td class="p-3">{{ product.barcode }}</td>
            <td class="p-3">{{ product.quantity }}</td>
            <td class="p-3">{{ product.unit }}</td>
            <td class="p-3">{{ categoryName(product.category_id) }}</td>
            <td class="p-3">{{ supplierName(product.supplier_id) }}</td>
            <td class="p-3 text-right space-x-2">
              <button @click="openEdit(product)" class="btn-primary">
                Edit
              </button>
              <button @click="openDelete(product)" class="btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div class="flex justify-between items-center pt-4 flex-wrap gap-2">
      <p class="text-sm text-gray-600">
        Page {{ currentPage }} of {{ totalPages }}
      </p>
      <div class="space-x-1 flex flex-wrap">
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
        <span class="px-3 py-2 rounded border bg-gray-100 text-sm">{{
          currentPage
        }}</span>
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

    <!-- Edit Modal -->
    <div v-if="editModalOpen" class="modal-overlay">
      <div class="modal-content">
        <h2 class="text-lg font-semibold mb-4">Edit Product</h2>
        <form @submit.prevent="submitEdit" class="space-y-3">
          <input v-model="editForm.name" class="input" placeholder="Name" />
          <input v-model="editForm.sku" class="input" placeholder="SKU" />
          <input
            v-model="editForm.barcode"
            class="input"
            placeholder="Barcode"
          />
          <input
            v-model.number="editForm.quantity"
            class="input"
            placeholder="Quantity"
          />
          <input v-model="editForm.unit" class="input" placeholder="Unit" />

          <select v-model.number="editForm.category_id" class="input">
            <option disabled value="">Select Category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>

          <select v-model.number="editForm.supplier_id" class="input">
            <option disabled value="">Select Supplier</option>
            <option v-for="sup in suppliers" :key="sup.id" :value="sup.id">
              {{ sup.name }}
            </option>
          </select>

          <div class="flex justify-end gap-3 pt-3">
            <button type="button" @click="closeEdit" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="deleteModalOpen" class="modal-overlay">
      <div class="modal-content">
        <p>
          Are you sure you want to delete
          <strong>{{ selectedProduct.name }}</strong
          >?
        </p>
        <div class="flex justify-end gap-3 mt-4">
          <button @click="closeDelete" class="btn-cancel">Cancel</button>
          <button @click="confirmDelete" class="btn-danger">Delete</button>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <ProductForm
      v-if="createModalOpen"
      @submit="handleCreate"
      @close="createModalOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/api";
import ProductForm from "@/components/ProductForm.vue";

const createModalOpen = ref(false);
const editModalOpen = ref(false);
const deleteModalOpen = ref(false);

const products = ref([]);
const categories = ref([]);
const suppliers = ref([]);
const selectedProduct = ref(null);

const editForm = ref({
  name: "",
  sku: "",
  barcode: "",
  quantity: 0,
  unit: "",
  category_id: null,
  supplier_id: null,
});

// Pagination
const currentPage = ref(1);
const pageSize = 10;

const totalPages = computed(() => Math.ceil(products.value.length / pageSize));
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return products.value.slice(start, start + pageSize);
});

const nextPage = () =>
  currentPage.value < totalPages.value && currentPage.value++;
const prevPage = () => currentPage.value > 1 && currentPage.value--;
const goToPage = (page) =>
  page >= 1 && page <= totalPages.value && (currentPage.value = page);
const skipPages = (offset) => {
  const newPage = currentPage.value + offset;
  currentPage.value = Math.min(Math.max(newPage, 1), totalPages.value);
};

// Fetch
const fetchProducts = async () => {
  const res = await api.get("/products");
  products.value = res.data;
};
const fetchCategories = async () => {
  const res = await api.get("/categories");
  categories.value = res.data;
};
const fetchSuppliers = async () => {
  const res = await api.get("/suppliers");
  suppliers.value = res.data;
};

const categoryName = (id) =>
  categories.value.find((c) => c.id === id)?.name || "";
const supplierName = (id) =>
  suppliers.value.find((s) => s.id === id)?.name || "";

const openEdit = (product) => {
  selectedProduct.value = product;
  editForm.value = { ...product };
  editModalOpen.value = true;
};
const closeEdit = () => (editModalOpen.value = false);
const submitEdit = async () => {
  await api.put(`/products/${selectedProduct.value.id}`, editForm.value);
  await fetchProducts();
  currentPage.value = 1;
  closeEdit();
};

const openDelete = (product) => {
  selectedProduct.value = product;
  deleteModalOpen.value = true;
};
const closeDelete = () => (deleteModalOpen.value = false);
const confirmDelete = async () => {
  await api.delete(`/products/${selectedProduct.value.id}`);
  await fetchProducts();
  currentPage.value = 1;
  closeDelete();
};

const handleCreate = async (formData) => {
  await api.post("/products", formData);
  await fetchProducts();
  createModalOpen.value = false;
  currentPage.value = 1;
};

onMounted(() => {
  fetchProducts();
  fetchCategories();
  fetchSuppliers();
});
</script>

<style scoped>
.input {
  @apply w-full p-2 border rounded max-h-60 overflow-auto;
}
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
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
.btn-cancel {
  @apply bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400;
}
.btn-light {
  @apply bg-gray-100 text-black px-4 py-2 rounded hover:bg-gray-200 disabled:opacity-50;
}
</style>
