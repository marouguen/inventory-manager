import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createRouter, createMemoryHistory } from "vue-router";
import { createTestingPinia } from "@pinia/testing";
import ProductEditView from "@/views/ProductEditPage.vue";
import ProductForm from "@/components/ProductForm.vue";

// Mock API
vi.mock("@/api/product", () => ({
  getProduct: vi.fn(),
  updateProduct: vi.fn(),
}));

import { getProduct, updateProduct } from "@/api/product";

describe("ProductEditPage.vue", () => {
  let router;

  beforeEach(async () => {
    vi.clearAllMocks();

    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: "/products/:id/edit",
          name: "EditProduct",
          component: ProductEditView,
        },
        {
          path: "/products",
          name: "ProductList",
          component: { template: "<div>Product List</div>" },
        },
      ],
    });

    // mock product response
    getProduct.mockResolvedValue({
      data: {
        id: 1,
        name: "Test Product",
        sku: "T123",
        barcode: "456789",
        quantity: 10,
        unit: "pcs",
        category_id: 2,
        supplier_id: 3,
      },
    });

    await router.push("/products/1/edit");
    await router.isReady();
  });

  const mountView = () =>
    mount(ProductEditView, {
      global: {
        plugins: [router, createTestingPinia()],
        stubs: {
          ProductForm,
        },
      },
    });

  it("renders the product form with fetched product", async () => {
    const wrapper = mountView();
    await flushPromises();

    const form = wrapper.findComponent(ProductForm);
    expect(form.exists()).toBe(true);
    expect(getProduct).toHaveBeenCalledWith("1");
  });

  it("calls updateProduct and navigates on submit", async () => {
    const wrapper = mountView();
    await flushPromises();

    const form = wrapper.findComponent(ProductForm);

    await form.vm.$emit("submit", {
      name: "Updated Product",
      sku: "NEW123",
      quantity: 20,
    });

    // Wait for router push to complete
    await flushPromises();

    expect(updateProduct).toHaveBeenCalledWith("1", {
      name: "Updated Product",
      sku: "NEW123",
      quantity: 20,
    });

    // ✅ Now check route after navigation completes
    expect(wrapper.vm.$router.currentRoute.value.fullPath).toBe("/products");
  });
});
