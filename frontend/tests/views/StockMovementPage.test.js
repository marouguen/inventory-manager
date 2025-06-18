import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import MovementPage from "@/views/MovementPage.vue";

// Mock the child components
vi.mock("@/components/MovementForm.vue", () => ({
  default: {
    name: "MovementForm",
    template: "<div class='mock-form'>Mocked MovementForm</div>",
  },
}));

vi.mock("@/components/MovementLogTable.vue", () => ({
  default: {
    name: "MovementLogTable",
    template: "<div class='mock-log-table'>Mocked MovementLogTable</div>",
  },
}));

describe("MovementPage.vue", () => {
  it("renders title and child components", () => {
    const wrapper = mount(MovementPage);

    expect(wrapper.text()).toContain("Stock Movement");

    // Check if mocked components are rendered
    expect(wrapper.find(".mock-form").exists()).toBe(true);
    expect(wrapper.find(".mock-log-table").exists()).toBe(true);
  });
});
