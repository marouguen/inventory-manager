import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import MovementLogTable from "@/components/MovementLogTable.vue";

// Fix for dayjs import
vi.mock("dayjs", () => ({
  default: () => ({
    format: () => "2025-06-16 10:00",
  }),
}));

describe("MovementLogTable.vue", () => {
  it("renders stock logs table rows", () => {
    const wrapper = mount(MovementLogTable, {
      global: {
        plugins: [
          createTestingPinia({
            initialState: {
              movement: {
                logs: [
                  {
                    id: 1,
                    product_id: "P001",
                    type: "in",
                    quantity: 10,
                    user_id: 1,
                    timestamp: "2025-06-16T10:00:00Z",
                  },
                ],
              },
            },
            stubActions: false,
          }),
        ],
      },
    });

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(1);
    expect(rows[0].text()).toContain("P001");
    expect(rows[0].text()).toContain("in");
    expect(rows[0].text()).toContain("10");
  });

  it("calls exportCSV when Export CSV button is clicked", async () => {
    const exportCSV = vi.fn();

    const wrapper = mount(MovementLogTable, {
      global: {
        plugins: [
          createTestingPinia({
            initialState: {
              movement: {
                logs: [],
              },
            },
            stubActions: false,
            createSpy: () => exportCSV, // This makes exportCSV get called
          }),
        ],
      },
    });

    await wrapper.find("button").trigger("click");
    expect(exportCSV).toHaveBeenCalled();
  });
});
