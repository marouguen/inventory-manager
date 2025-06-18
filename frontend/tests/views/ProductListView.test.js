// tests/views/ProductListView.test.js
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import ProductListView from "@/views/ProductListPage.vue";
import { createTestingPinia } from "@pinia/testing";

// Mock API
vi.mock("@/api", () => ({
  default: {
    get: vi.fn((url) => {
      if (url === "/products") {
        return Promise.resolve({
          data: [
            {
              id: 1,
              name: "Product A",
              sku: "A001",
              barcode: "123",
              quantity: 10,
              unit: "pcs",
              category_id: 1,
              supplier_id: 1,
            },
          ],
        });
      }
      if (url === "/categories") {
        return Promise.resolve({
          data: [{ id: 1, name: "Electronics" }],
        });
      }
      if (url === "/suppliers") {
        return Promise.resolve({
          data: [{ id: 1, name: "ABC Corp" }],
        });
      }
    }),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe("ProductListView.vue", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders product list table with products", async () => {
    const wrapper = mount(ProductListView, {
      global: {
        plugins: [createTestingPinia()],
      },
    });

    await flushPromises();

    expect(wrapper.text()).toContain("📦 Product List");
    expect(wrapper.text()).toContain("Product A");
    expect(wrapper.findAll("tbody tr")).toHaveLength(1);
  });

  it("opens create modal when + Create Product is clicked", async () => {
    const wrapper = mount(ProductListView, {
      global: {
        plugins: [createTestingPinia()],
      },
    });

    await flushPromises();
    await wrapper.find("button").trigger("click"); // "+ Create Product" button

    await flushPromises();

    // Check for modal structure or specific form field
    expect(wrapper.html()).toContain("New Product");
    expect(wrapper.find("input[placeholder='Name']").exists()).toBe(true);
  });
});
