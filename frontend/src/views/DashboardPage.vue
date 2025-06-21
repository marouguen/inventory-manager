<template>
  <div class="space-y-8">
    <!-- Date Filters -->
    <div class="flex items-center space-x-4">
      <div>
        <label class="block text-sm font-medium">Start Date</label>
        <input type="date" v-model="startDate" class="input" />
      </div>
      <div>
        <label class="block text-sm font-medium">End Date</label>
        <input type="date" v-model="endDate" class="input" />
      </div>
    </div>

    <!-- Stock by Category Chart -->
    <div class="bg-white p-4 rounded shadow">
      <h2 class="text-lg font-semibold mb-2">📦 Stock by Category</h2>
      <div class="h-64">
        <DoughnutChart
          v-if="categoryChartData"
          :chartData="categoryChartData"
          :chartOptions="chartOptions"
        />
      </div>
    </div>

    <!-- Top Moved Products Chart -->
    <div class="bg-white p-4 rounded shadow">
      <h2 class="text-lg font-semibold mb-2">🔥 Top Moved Products</h2>
      <div class="h-80">
        <BarChart
          v-if="barChartData"
          :chartData="barChartData"
          :chartOptions="chartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/api"; // ✅ centralized axios
import BarChart from "@/components/charts/BarChart.vue";
import DoughnutChart from "@/components/charts/DoughnutChart.vue";

const auth = useAuthStore();

const startDate = ref("");
const endDate = ref("");
const stockByCategory = ref([]);
const topProducts = ref([]);
const barChartData = ref(null);
const categoryChartData = ref(null);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: "#374151" },
    },
  },
  scales: {
    x: {
      ticks: { color: "#6b7280" },
      grid: { display: false },
    },
    y: {
      ticks: { color: "#6b7280", beginAtZero: true },
      grid: { color: "#e5e7eb" },
    },
  },
};

const fetchDashboard = async () => {
  const params = {};
  if (startDate.value) params.start_date = startDate.value;
  if (endDate.value) params.end_date = endDate.value;

  const [res1, res2] = await Promise.all([
    api.get("/dashboard/by-category", { params }),
    api.get("/dashboard/top-products", { params }),
  ]);

  stockByCategory.value = res1.data;
  topProducts.value = res2.data;

  categoryChartData.value = {
    labels: stockByCategory.value.map((item) => item.category),
    datasets: [
      {
        data: stockByCategory.value.map((item) => item.total_quantity),
        backgroundColor: [
          "#6366f1",
          "#4ade80",
          "#facc15",
          "#f87171",
          "#60a5fa",
        ],
        borderWidth: 1,
      },
    ],
  };

  barChartData.value = {
    labels: topProducts.value.map((item) => item.name),
    datasets: [
      {
        label: "Total Movement",
        data: topProducts.value.map((item) => item.quantity),
        backgroundColor: "#6366f1",
        borderRadius: 6,
        barThickness: 40,
      },
    ],
  };
};

watch([startDate, endDate], fetchDashboard, { immediate: true });
</script>

<style scoped>
.input {
  @apply border px-2 py-1 rounded w-full;
}
</style>
