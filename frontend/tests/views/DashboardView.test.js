import { mount, flushPromises } from "@vue/test-utils";
import DashboardPage from "@/views/DashboardPage.vue";
import { vi } from "vitest";
import axios from "axios";
import { createTestingPinia } from "@pinia/testing";

// Mock axios
vi.mock("axios");

describe("DashboardPage.vue", () => {
  const mockCategoryData = [
    { category: "Electronics", total_quantity: 100 },
    { category: "Office Supplies", total_quantity: 50 },
  ];

  const mockTopProducts = [
    { name: "Mouse", quantity: 80 },
    { name: "Keyboard", quantity: 40 },
  ];

  beforeEach(() => {
    axios.get
      .mockResolvedValueOnce({ data: mockCategoryData }) // first API
      .mockResolvedValueOnce({ data: mockTopProducts }); // second API
  });

  it("fetches data and renders charts", async () => {
    const wrapper = mount(DashboardPage, {
      global: {
        plugins: [
          createTestingPinia({
            stubActions: false,
            initialState: {
              auth: { token: "fake-token" },
            },
          }),
        ],
      },
    });

    await flushPromises();

    // Check chart components exist
    expect(wrapper.findComponent({ name: "DoughnutChart" }).exists()).toBe(
      true
    );
    expect(wrapper.findComponent({ name: "BarChart" }).exists()).toBe(true);

    // Check chart data props
    const doughnutChart = wrapper.findComponent({ name: "DoughnutChart" });
    expect(doughnutChart.props("chartData").labels).toEqual([
      "Electronics",
      "Office Supplies",
    ]);

    const barChart = wrapper.findComponent({ name: "BarChart" });
    expect(barChart.props("chartData").labels).toEqual(["Mouse", "Keyboard"]);
  });
});
