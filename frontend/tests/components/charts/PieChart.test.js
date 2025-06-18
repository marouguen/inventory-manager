import { mount } from "@vue/test-utils";
import PieChart from "@/components/charts/PieChart.vue";

// Stub the Pie component from vue-chartjs to avoid canvas errors
vi.mock("vue-chartjs", () => ({
  Pie: {
    name: "Pie",
    props: ["data", "options"],
    template: "<div class='pie-chart-stub'></div>",
  },
}));

describe("PieChart.vue", () => {
  const chartData = {
    labels: ["Apples", "Bananas", "Cherries"],
    datasets: [
      {
        data: [40, 30, 30],
        backgroundColor: ["#f87171", "#60a5fa", "#34d399"],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "right",
        labels: { color: "#000" },
      },
    },
  };

  it("renders stubbed Pie chart with correct props", () => {
    const wrapper = mount(PieChart, {
      props: {
        chartData,
        chartOptions,
      },
    });

    const chart = wrapper.findComponent({ name: "Pie" });
    expect(chart.exists()).toBe(true);
    expect(chart.props("data")).toEqual(chartData);
    expect(chart.props("options")).toEqual(chartOptions);
  });
});
