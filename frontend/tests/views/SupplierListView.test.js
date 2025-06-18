import { mount, flushPromises } from "@vue/test-utils";
import SupplierListPage from "@/views/SupplierListPage.vue";
import api from "@/api";
import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("@/api");

describe("SupplierListPage.vue", () => {
  const sampleSuppliers = [
    {
      id: 1,
      name: "Supplier A",
      email: "a@email.com",
      phone: "123",
      address: "Addr A",
    },
    { id: 2, name: "Supplier B", email: "", phone: "", address: "" },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    api.get.mockResolvedValue({ data: sampleSuppliers });
  });

  it("fetches and renders supplier rows", async () => {
    const wrapper = mount(SupplierListPage);
    await flushPromises();
    expect(wrapper.text()).toContain("Supplier A");
    expect(wrapper.text()).toContain("—");
  });

  it("opens modal when + Add Supplier button is clicked", async () => {
    const wrapper = mount(SupplierListPage);
    await flushPromises();
    await wrapper.find("button.btn-primary").trigger("click");
    expect(wrapper.find(".modal-overlay").exists()).toBe(true);
  });

  it("submits a new supplier", async () => {
    api.post.mockResolvedValue({});
    const wrapper = mount(SupplierListPage);
    await flushPromises();

    await wrapper.find("button.btn-primary").trigger("click");
    await wrapper.find("input.input").setValue("New Supplier");
    await wrapper.find("form").trigger("submit.prevent");
    expect(api.post).toHaveBeenCalled();
  });

  it("deletes a supplier after confirmation", async () => {
    global.confirm = vi.fn(() => true);
    api.delete.mockResolvedValue({});
    const wrapper = mount(SupplierListPage);
    await flushPromises();

    await wrapper.find("button.btn-danger").trigger("click");
    expect(api.delete).toHaveBeenCalledWith("/suppliers/1");
  });
});
