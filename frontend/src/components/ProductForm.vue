<script setup>
import { ref, onMounted } from "vue";
import { createProduct } from "@/api/product";
const emit = defineEmits(["submit", "close"]);

const name = ref("");
const sku = ref("");
const barcode = ref("");
const quantity = ref(0);
const unit = ref("");
const category_id = ref(null);
const supplier_id = ref(null);

// TODO: Replace with real API call
const categories = ref([
  { id: 1, name: "Electronics" },
  { id: 2, name: "Office Supplies" },
]);

const suppliers = ref([
  { id: 1, name: "ABC Corp" },
  { id: 2, name: "XYZ Ltd" },
]);

const submit = async () => {
  await createProduct({
    name: name.value,
    sku: sku.value,
    barcode: barcode.value,
    quantity: parseFloat(quantity.value),
    unit: unit.value,
    category_id: category_id.value || null,
    supplier_id: supplier_id.value || null,
  });
  emit("close");
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg w-[450px] max-h-[90vh] overflow-y-auto">
      <h3 class="text-xl font-semibold mb-4">New Product</h3>

      <div class="space-y-2">
        <input v-model="name" placeholder="Name" class="w-full border p-2" />
        <input v-model="sku" placeholder="SKU" class="w-full border p-2" />
        <input
          v-model="barcode"
          placeholder="Barcode"
          class="w-full border p-2"
        />
        <input
          v-model="quantity"
          type="number"
          step="any"
          placeholder="Quantity"
          class="w-full border p-2"
        />
        <input
          v-model="unit"
          placeholder="Unit (e.g. pcs, kg)"
          class="w-full border p-2"
        />

        <select v-model="category_id" class="w-full border p-2">
          <option value="">-- Select Category --</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>

        <select v-model="supplier_id" class="w-full border p-2">
          <option value="">-- Select Supplier --</option>
          <option v-for="sup in suppliers" :key="sup.id" :value="sup.id">
            {{ sup.name }}
          </option>
        </select>
      </div>

      <div class="flex justify-end mt-4 space-x-2">
        <button @click="emit('close')" class="px-4 py-2 bg-gray-300 rounded">
          Cancel
        </button>
        <button
          @click="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>
