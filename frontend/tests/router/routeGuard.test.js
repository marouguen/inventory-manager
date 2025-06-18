import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createMemoryHistory } from "vue-router";
import { createTestingPinia } from "@pinia/testing";
import CreateProductView from "@/views/ProductCreatePage.vue";
import ProductForm from "@/components/ProductForm.vue";
import flushPromises from "flush-promises";

// Mock the API
vi.mock("@/api/product", () => ({
  createProduct: vi.fn(),
}));
import { createProduct } from "@/api/product";

// Suppress Vue Router warning messages for unmatched routes
vi.spyOn(console, "warn").mockImplementation((msg) => {
  if (
    typeof msg === "string" &&
    (msg.includes("No match found for location") ||
      msg.includes('Record with path "/products"'))
  ) {
    return;
  }
  console.warn(msg);
});

describe("ProductCreatePage.vue", () => {
  let router;

  beforeEach(async () => {
    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: "/",
          name: "Home",
          component: { template: "<div>Home</div>" },
        },
        {
          path: "/products",
          name: "Products",
          component: { template: "<div>Products</div>" },
        },
      ],
    });

    await router.push("/");
    await router.isReady();
  });

  const mountView = () =>
    mount(CreateProductView, {
      global: {
        plugins: [router, createTestingPinia()],
        stubs: {
          ProductForm,
        },
      },
    });

  it("renders page title", () => {
    const wrapper = mountView();
    expect(wrapper.text()).toContain("➕ Create Product");
  });

  it("opens modal when button is clicked", async () => {
    const wrapper = mountView();
    await wrapper.find("button").trigger("click");
    expect(wrapper.findComponent(ProductForm).exists()).toBe(true);
  });

  it("calls createProduct and redirects after submit", async () => {
    const wrapper = mountView();
    await wrapper.find("button").trigger("click");

    const form = wrapper.findComponent(ProductForm);
    await form.vm.$emit("submit", { name: "New Product", price: 99 });

    expect(createProduct).toHaveBeenCalledWith({
      name: "New Product",
      price: 99,
    });

    // Check final route

    await flushPromises(); // ✅ Wait for navigation to complete
    expect(router.currentRoute.value.fullPath).toBe("/products");
  });

  it("closes modal on close event", async () => {
    const wrapper = mountView();
    await wrapper.find("button").trigger("click");

    const form = wrapper.findComponent(ProductForm);
    await form.vm.$emit("close");
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(ProductForm).exists()).toBe(false);
  });
});
