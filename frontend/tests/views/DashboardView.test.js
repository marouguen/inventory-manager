import { mount, flushPromises } from "@vue/test-utils";
import DashboardPage from "@/views/DashboardPage.vue";
import { vi } from "vitest";
import { createTestingPinia } from "@pinia/testing";
import api from "@/api";

// Mock the centralized Axios instance
vi.mock("@/api", () => ({
  default: {
    get: vi.fn(),
  },
}));

vi.mock("vue-chartjs", async () => {
  return await import("../__mocks__/vue-chartjs.js");
});

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
    api.get.mockClear();

    // Match both endpoints, regardless of query params
    api.get
      .mockImplementationOnce(() => Promise.resolve({ data: mockCategoryData }))
      .mockImplementationOnce(() => Promise.resolve({ data: mockTopProducts }));
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

    const doughnutChart = wrapper.findComponent({ name: "DoughnutChart" });
    const barChart = wrapper.findComponent({ name: "BarChart" });

    // ✅ Ensure charts are rendered
    expect(doughnutChart.exists()).toBe(true);
    expect(barChart.exists()).toBe(true);

    // ✅ Validate chart props
    expect(doughnutChart.props("chartData").labels).toEqual([
      "Electronics",
      "Office Supplies",
    ]);
    expect(barChart.props("chartData").labels).toEqual(["Mouse", "Keyboard"]);
  });
});
