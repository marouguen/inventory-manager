import { mount, flushPromises } from "@vue/test-utils";
import userAdmin from "@/views/userAdmin.vue";
import { vi } from "vitest";
import api from "@/api";

// Mock API
vi.mock("@/api", () => ({
  default: {
    get: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe("userAdmin.vue", () => {
  const mockUsers = [
    { id: 1, email: "user1@example.com", role: "user", is_active: true },
    { id: 2, email: "admin@example.com", role: "admin", is_active: false },
  ];

  beforeEach(() => {
    api.get.mockResolvedValue({ data: mockUsers });
    api.patch.mockResolvedValue({});
    api.delete.mockResolvedValue({});
  });

  it("renders user table with fetched users", async () => {
    const wrapper = mount(userAdmin);
    await flushPromises();

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(2);
    expect(rows[0].text()).toContain("user1@example.com");
    expect(rows[1].text()).toContain("admin@example.com");
  });

  it("changes user role and sends PATCH request", async () => {
    const wrapper = mount(userAdmin);
    await flushPromises();

    const roleSelects = wrapper.findAll("select");
    await roleSelects[0].setValue("admin"); // change first user's role

    expect(api.patch).toHaveBeenCalledWith("/users/1", { role: "admin" });
  });

  it("deletes a user and updates table", async () => {
    global.confirm = vi.fn(() => true); // simulate confirmation
    const wrapper = mount(userAdmin);
    await flushPromises();

    const deleteButtons = wrapper.findAll("button.btn-danger");
    await deleteButtons[0].trigger("click");

    expect(api.delete).toHaveBeenCalledWith("/users/1");
    await flushPromises();

    // One user left
    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(1);
    expect(rows[0].text()).toContain("admin@example.com");
  });
});
