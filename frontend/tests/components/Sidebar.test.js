import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";

// Mock vue-router
vi.mock("vue-router", () => ({
  RouterLink: {
    name: "RouterLink",
    props: ["to"],
    template: `<a :href="to"><slot /></a>`,
  },
}));

const mockUser = { email: "admin@example.com", role: "admin" };
const toggleMock = vi.fn();

// Master test suite
describe("Sidebar.vue", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    toggleMock.mockClear();
  });

  describe("Authenticated user", () => {
    beforeEach(() => {
      vi.doMock("@/stores/auth", () => ({
        useAuthStore: () => ({ user: mockUser }),
      }));
      vi.doMock("@/stores/layout", () => ({
        useLayoutStore: () => ({
          isSidebarCollapsed: false,
          toggleSidebar: toggleMock,
        }),
      }));
    });

    it("renders all authenticated links", async () => {
      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);
      expect(wrapper.text()).toContain("🏠 Home");
      expect(wrapper.text()).toContain("📦 Products");
      expect(wrapper.text()).toContain("👤 Users Admin");
    });

    it("calls toggleSidebar when button is clicked", async () => {
      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);
      await wrapper.find("button").trigger("click");
      expect(toggleMock).toHaveBeenCalled();
    });
  });

  describe("Guest user", () => {
    beforeEach(() => {
      vi.resetModules();
      vi.doMock("@/stores/auth", () => ({
        useAuthStore: () => ({ user: null }),
      }));
      vi.doMock("@/stores/layout", () => ({
        useLayoutStore: () => ({
          isSidebarCollapsed: false,
          toggleSidebar: toggleMock,
        }),
      }));
    });

    it("renders only guest links", async () => {
      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);

      expect(wrapper.text()).toContain("🔐 Login");
      expect(wrapper.text()).toContain("📝 Register");
      expect(wrapper.text()).not.toContain("Products");
    });
  });

  describe("Sidebar collapsed", () => {
    beforeEach(() => {
      vi.resetModules(); // 👈 Clear previous modules
      vi.doMock("@/stores/auth", () => ({
        useAuthStore: () => ({ user: mockUser }),
      }));
      vi.doMock("@/stores/layout", () => ({
        useLayoutStore: () => ({
          isSidebarCollapsed: true,
          toggleSidebar: toggleMock,
        }),
      }));
    });

    it("renders icons only", async () => {
      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);
      expect(wrapper.text()).toContain("🏠");
      expect(wrapper.text()).not.toContain("Home");
    });
  });
  describe("Role-based rendering", () => {
    beforeEach(() => {
      vi.resetModules();
    });

    it('shows "Users Admin" link for admin role', async () => {
      vi.doMock("@/stores/auth", () => ({
        useAuthStore: () => ({
          user: { email: "admin@example.com", role: "admin" },
        }),
      }));

      vi.doMock("@/stores/layout", () => ({
        useLayoutStore: () => ({
          isSidebarCollapsed: false,
          toggleSidebar: toggleMock,
        }),
      }));

      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);

      expect(wrapper.text()).toContain("👤 Users Admin");
    });

    it('hides "Users Admin" link for staff role', async () => {
      vi.doMock("@/stores/auth", () => ({
        useAuthStore: () => ({
          user: { email: "staff@example.com", role: "staff" },
        }),
      }));

      vi.doMock("@/stores/layout", () => ({
        useLayoutStore: () => ({
          isSidebarCollapsed: false,
          toggleSidebar: toggleMock,
        }),
      }));

      const { default: Sidebar } = await import("@/layout/Sidebar.vue");
      const wrapper = mount(Sidebar);

      expect(wrapper.text()).not.toContain("👤 Users Admin");
    });
  });
});
