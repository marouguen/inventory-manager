import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import CategoriesPage from "@/views/CategoryPage.vue";
import api from "@/api";

vi.mock("@/api");

const mockCategories = [
  { id: 1, name: "Electronics", description: "Gadgets and devices" },
  { id: 2, name: "Office Supplies", description: "Stationery and tools" },
];

describe("CategoriesPage.vue", () => {
  beforeEach(() => {
    api.get.mockResolvedValue({ data: mockCategories });
  });

  it("renders fetched categories in table", async () => {
    const wrapper = mount(CategoriesPage);
    await flushPromises();

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(mockCategories.length);
    expect(wrapper.html()).toContain("Electronics");
    expect(wrapper.html()).toContain("Office Supplies");
  });

  it("opens modal when + New Category is clicked", async () => {
    const wrapper = mount(CategoriesPage);
    await flushPromises();

    expect(wrapper.find(".modal-content").exists()).toBe(false);
    await wrapper.find("button.btn-primary").trigger("click");
    expect(wrapper.find(".modal-content").exists()).toBe(true);
  });

  it("enters edit mode when Edit is clicked", async () => {
    const wrapper = mount(CategoriesPage);
    await flushPromises();

    const editButtons = wrapper.findAll("button.btn-primary");
    await editButtons[1].trigger("click"); // Second is 'Edit'

    expect(wrapper.find(".modal-content").text()).toContain("Edit Category");
    expect(wrapper.find("input").element.value).toBe("Electronics");
  });

  it("shows pagination controls", async () => {
    const wrapper = mount(CategoriesPage);
    await flushPromises();

    expect(wrapper.text()).toContain("Page 1 of");
    expect(wrapper.find("button.btn-light").exists()).toBe(true);
  });
});
