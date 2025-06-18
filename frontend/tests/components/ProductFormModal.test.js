// tests/components/ProductFormModal.test.js
import { mount } from "@vue/test-utils";
import ProductFormModal from "@/components/ProductForm.vue";
import { vi } from "vitest";
import { createProduct } from "@/api/product";

// Mock the API function
vi.mock("@/api/product", () => ({
  createProduct: vi.fn(() => Promise.resolve()),
}));

describe("ProductFormModal.vue", () => {
  it("renders all input fields", () => {
    const wrapper = mount(ProductFormModal);

    const inputs = wrapper.findAll("input");
    expect(inputs.length).toBe(5); // name, sku, barcode, quantity, unit

    expect(wrapper.find("select").exists()).toBe(true); // at least one select
  });

  it("submits the form and emits close", async () => {
    const wrapper = mount(ProductFormModal);

    // Fill inputs
    await wrapper.find('input[placeholder="Name"]').setValue("Test Product");
    await wrapper.find('input[placeholder="SKU"]').setValue("TP123");
    await wrapper.find('input[placeholder="Barcode"]').setValue("1234567890");
    await wrapper.find('input[placeholder="Quantity"]').setValue("5");
    await wrapper
      .find('input[placeholder="Unit (e.g. pcs, kg)"]')
      .setValue("pcs");

    // Select category & supplier
    await wrapper.findAll("select")[0].setValue("1");
    await wrapper.findAll("select")[1].setValue("2");

    // Click save
    await wrapper.find("button.bg-blue-600").trigger("click");

    expect(createProduct).toHaveBeenCalledWith({
      name: "Test Product",
      sku: "TP123",
      barcode: "1234567890",
      quantity: 5,
      unit: "pcs",
      category_id: 1,
      supplier_id: 2,
    });

    expect(wrapper.emitted("close")).toBeTruthy();
  });
});
