<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getProduct, updateProduct } from "@/api/product";
import ProductForm from "@/components/ProductForm.vue";

const route = useRoute();
const router = useRouter();
const product = ref(null);

onMounted(async () => {
  const res = await getProduct(route.params.id);
  product.value = res.data;
});

const handleUpdate = async (formData) => {
  await updateProduct(route.params.id, formData);
  router.push("/products");
};
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">✏️ Edit Product</h1>
    <ProductForm v-if="product" :modelValue="product" @submit="handleUpdate" />
  </div>
</template>
