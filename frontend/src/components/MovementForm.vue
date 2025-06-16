<template>
  <form @submit.prevent="submit">
    <div class="grid gap-4 grid-cols-1 md:grid-cols-3">
      <select v-model="form.product_id" class="border p-2 rounded">
        <option disabled value="">Select Product</option>
        <option v-for="p in products" :key="p.id" :value="p.id">
          {{ p.name }}
        </option>
      </select>

      <select v-model="form.type" class="border p-2 rounded">
        <option disabled value="">Select Type</option>
        <option value="in">Stock In</option>
        <option value="out">Stock Out</option>
      </select>

      <input
        type="number"
        v-model.number="form.quantity"
        min="1"
        class="border p-2 rounded"
        placeholder="Quantity"
      />
    </div>

    <button
      type="submit"
      class="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-500"
    >
      Submit Movement
    </button>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useMovementStore } from "@/stores/movement";

const form = ref({
  product_id: "",
  type: "",
  quantity: null,
});

const products = ref([]);
const movement = useMovementStore();

const submit = async () => {
  if (!form.value.product_id || !form.value.type || !form.value.quantity)
    return;
  await movement.submitMovement({ ...form.value });
  form.value.quantity = null;
};

onMounted(async () => {
  const res = await axios.get("http://127.0.0.1:8000/products");
  products.value = res.data;
});
</script>
