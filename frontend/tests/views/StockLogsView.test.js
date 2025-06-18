import { mount, flushPromises } from "@vue/test-utils";
import StockLogsPage from "@/views/StockLogsPage.vue";
import { createPinia, setActivePinia } from "pinia";
import { useStockLogStore } from "@/stores/stockLogs";
import { describe, it, vi, expect, beforeEach } from "vitest";

vi.mock("dayjs", () => {
  return {
    default: () => ({
      format: () => "2024-06-01 12:00",
    }),
  };
});

describe("StockLogsPage.vue", () => {
  let store;

  const sampleLogs = [
    {
      id: 1,
      product_id: 101,
      type: "in",
      quantity: 20,
      user_id: 1,
      timestamp: "2024-06-01T12:00:00Z",
    },
    {
      id: 2,
      product_id: 102,
      type: "out",
      quantity: 10,
      user_id: 2,
      timestamp: "2024-06-02T12:00:00Z",
    },
  ];

  beforeEach(() => {
    setActivePinia(createPinia());
    store = useStockLogStore();
    store.logs = sampleLogs;
    store.fetchLogs = vi.fn();
    store.exportCSV = vi.fn();
  });

  it("renders logs correctly", async () => {
    const wrapper = mount(StockLogsPage);
    await flushPromises();

    expect(wrapper.text()).toContain("Stock Logs");
    expect(wrapper.text()).toContain("101");
    expect(wrapper.text()).toContain("in");
    expect(wrapper.text()).toContain("20");
    expect(wrapper.text()).toContain("1");
    expect(wrapper.text()).toContain("2024-06-01 12:00");
  });

  it("calls exportCSV on button click", async () => {
    const wrapper = mount(StockLogsPage);
    await flushPromises();

    const exportBtn = wrapper.find("button");
    await exportBtn.trigger("click");

    expect(store.exportCSV).toHaveBeenCalled();
  });

  it("calls store.fetchLogs on mount", async () => {
    mount(StockLogsPage);
    expect(store.fetchLogs).toHaveBeenCalled();
  });
});
