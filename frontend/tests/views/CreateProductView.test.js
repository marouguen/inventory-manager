import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouter, createMemoryHistory } from "vue-router";
import ProductCreatePage from "@/views/ProductCreatePage.vue";

// Mock ProductForm component
vi.mock("@/components/ProductForm.vue", () => ({
  default: {
    name: "ProductForm",
    template:
      "<div class='mock-form'><button @click=\"$emit('submit', { name: 'Test' })\">Submit</button><button @click=\"$emit('close')\">Close</button></div>",
  },
}));

// Mock API
vi.mock("@/api/product", () => ({
  createProduct: vi.fn(),
}));

import { createProduct } from "@/api/product";

describe("ProductCreatePage.vue", () => {
  let router;

  beforeEach(() => {
    router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: "/products", name: "Products" }],
    });
    router.push("/"); // Set an initial route
  });

  const mountComponent = () =>
    mount(ProductCreatePage, {
      global: {
        plugins: [createTestingPinia(), router],
      },
    });

  it("renders page title", async () => {
    const wrapper = mountComponent();
    expect(wrapper.text()).toContain("➕ Create Product");
  });

  it("opens modal when button is clicked", async () => {
    const wrapper = mountComponent();

    expect(wrapper.find(".mock-form").exists()).toBe(false);
    await wrapper.find("button").trigger("click");
    expect(wrapper.find(".mock-form").exists()).toBe(true);
  });

  it("calls createProduct and redirects after submit", async () => {
    const wrapper = mountComponent();

    // Open modal
    await wrapper.find("button").trigger("click");

    // Simulate submit inside ProductForm
    await wrapper.find(".mock-form button").trigger("click");

    expect(createProduct).toHaveBeenCalledWith({ name: "Test" });

    // Wait for navigation
    await router.isReady();
    expect(router.currentRoute.value.fullPath).toBe("/products");
  });

  it("closes modal on close event", async () => {
    const wrapper = mountComponent();

    // Open modal
    await wrapper.find("button").trigger("click");
    expect(wrapper.find(".mock-form").exists()).toBe(true);

    // Click close button (second button in mock form)
    await wrapper.findAll(".mock-form button")[1].trigger("click");
    expect(wrapper.find(".mock-form").exists()).toBe(false);
  });
});
