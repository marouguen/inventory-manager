// tests/components/MovementForm.test.js
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import MovementForm from "@/components/MovementForm.vue";
import { useMovementStore } from "@/stores/movement";

// ✅ Mock @/api instead of axios
vi.mock("@/api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    interceptors: { request: { use: vi.fn() } },
  },
}));

import api from "@/api"; // ⬅️ required to use the mock

const mockProducts = [
  { id: 1, name: "Product A" },
  { id: 2, name: "Product B" },
];

beforeEach(() => {
  api.get.mockResolvedValue({ data: mockProducts });
});

describe("MovementForm.vue", () => {
  it("renders form inputs", async () => {
    const wrapper = mount(MovementForm, {
      global: {
        plugins: [createTestingPinia()],
      },
    });

    await flushPromises();

    const selects = wrapper.findAll("select");
    const numberInput = wrapper.find('input[type="number"]');

    expect(selects.length).toBe(2);
    expect(numberInput.exists()).toBe(true);
    expect(selects[0].findAll("option").length).toBeGreaterThan(1);
  });

  it("emits submit event with valid data", async () => {
    const wrapper = mount(MovementForm, {
      global: {
        plugins: [createTestingPinia({ stubActions: false })],
      },
    });

    await flushPromises();

    const productSelect = wrapper.findAll("select")[0];
    const typeSelect = wrapper.findAll("select")[1];
    const quantityInput = wrapper.find('input[type="number"]');

    await productSelect.setValue("1");
    await typeSelect.setValue("in");
    await quantityInput.setValue("10");

    await wrapper.find("form").trigger("submit.prevent");

    const movementStore = useMovementStore();
    expect(movementStore.submitMovement).toHaveBeenCalledOnce();
    expect(movementStore.submitMovement).toHaveBeenCalledWith({
      product_id: 1,
      type: "in",
      quantity: 10,
    });
  });
});
