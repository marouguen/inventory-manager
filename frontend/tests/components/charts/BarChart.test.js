import { mount } from "@vue/test-utils";
import BarChart from "@/components/charts/BarChart.vue";

// Stub the Bar component from vue-chartjs
vi.mock("vue-chartjs", () => ({
  Bar: {
    name: "Bar",
    props: ["data", "options"],
    template: "<div class='bar-chart-stub'></div>",
  },
}));

describe("BarChart.vue", () => {
  const chartData = {
    labels: ["Product A", "Product B"],
    datasets: [
      {
        label: "Quantity",
        data: [100, 50],
        backgroundColor: "#4ade80",
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

  it("renders stubbed Bar chart with correct props", () => {
    const wrapper = mount(BarChart, {
      props: {
        chartData,
        chartOptions,
      },
    });

    const bar = wrapper.findComponent({ name: "Bar" });
    expect(bar.exists()).toBe(true);
    expect(bar.props("data")).toEqual(chartData);
    expect(bar.props("options")).toEqual(chartOptions);
  });
});
