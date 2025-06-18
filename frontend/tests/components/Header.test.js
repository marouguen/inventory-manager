import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import Header from "@/layout/Header.vue";

// 🔧 Create a shared mock for logout and router.push
const mockLogout = vi.fn();
const mockPush = vi.fn();

// 🧪 Mock vue-router
vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// 🧪 Mock Pinia store
vi.mock("@/stores/auth", () => ({
  useAuthStore: () => ({
    user: { email: "admin@example.com", role: "admin" },
    logout: mockLogout,
  }),
}));

describe("Header.vue", () => {
  beforeEach(() => {
    // Fresh Pinia for each test
    setActivePinia(createPinia());
    mockLogout.mockClear();
    mockPush.mockClear();
  });

  it("renders the title and user email", () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createPinia()],
      },
    });

    expect(wrapper.text()).toContain("Inventory Manager");
    expect(wrapper.text()).toContain("admin@example.com");
  });

  it("calls logout and redirects to login on logout click", async () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [createPinia()],
      },
    });

    const logoutBtn = wrapper.find('[data-testid="logout-btn"]');
    await logoutBtn.trigger("click");

    expect(mockLogout).toHaveBeenCalled();
    expect(mockPush).toHaveBeenCalledWith("/login");
  });
});
