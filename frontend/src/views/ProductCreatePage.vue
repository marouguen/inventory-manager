<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">➕ Create Product</h1>

    <button
      @click="createModalOpen = true"
      class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-500"
    >
      + Create Product
    </button>

    <!-- Modal -->
    <ProductForm
      v-if="createModalOpen"
      @submit="handleCreate"
      @close="createModalOpen = false"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createProduct } from "@/api/product";
import ProductForm from "@/components/ProductForm.vue";

const router = useRouter();
const createModalOpen = ref(false);

const handleCreate = async (formData) => {
  await createProduct(formData);
  createModalOpen.value = false;
  router.push("/products");
};
</script>
