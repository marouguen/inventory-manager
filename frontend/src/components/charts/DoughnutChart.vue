<script setup>
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from "chart.js";
import { Doughnut } from "vue-chartjs";

ChartJS.register(Title, Tooltip, Legend, ArcElement);

defineProps(["chartData", "chartOptions"]);
</script>

<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>
