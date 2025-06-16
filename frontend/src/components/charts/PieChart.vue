<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";

ChartJS.register(Tooltip, Legend, ArcElement);

const props = defineProps({
  chartData: Object,
  chartOptions: Object,
});
</script>

<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>
