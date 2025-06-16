<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Stock Movement</h1>
    <MovementForm />
    <MovementLogTable />
  </div>
</template>

<script setup>
import MovementForm from "@/components/MovementForm.vue";
import MovementLogTable from "@/components/MovementLogTable.vue";
</script>
