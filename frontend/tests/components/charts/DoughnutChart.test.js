import { mount } from "@vue/test-utils";
import DoughnutChart from "@/components/charts/DoughnutChart.vue";

// Stub vue-chartjs Doughnut component
vi.mock("vue-chartjs", () => ({
  Doughnut: {
    name: "Doughnut",
    props: ["data", "options"],
    template: "<div class='doughnut-chart-stub'></div>",
  },
}));

describe("DoughnutChart.vue", () => {
  const chartData = {
    labels: ["Electronics", "Office", "Kitchen"],
    datasets: [
      {
        data: [100, 50, 25],
        backgroundColor: ["#6366f1", "#4ade80", "#facc15"],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#000" },
      },
    },
  };

  it("renders stubbed Doughnut chart with correct props", () => {
    const wrapper = mount(DoughnutChart, {
      props: {
        chartData,
        chartOptions,
      },
    });

    const chart = wrapper.findComponent({ name: "Doughnut" });
    expect(chart.exists()).toBe(true);
    expect(chart.props("data")).toEqual(chartData);
    expect(chart.props("options")).toEqual(chartOptions);
  });
});
