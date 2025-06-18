import { createTestingPinia } from "@pinia/testing";

export function mountWithPinia(component, options = {}) {
  return mount(component, {
    global: {
      plugins: [createTestingPinia()],
      ...options?.global,
    },
    ...options,
  });
}
