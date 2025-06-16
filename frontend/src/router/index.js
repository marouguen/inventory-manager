import { createRouter, createWebHistory } from "vue-router";
import LayoutWrapper from "@/layout/LayoutWrapper.vue";
import DashboardPage from "@/views/DashboardPage.vue";
import HomePage from "@/views/Home.vue";
import ProductListPage from "@/views/ProductListPage.vue";
import ProductEditPage from "@/views/ProductEditPage.vue";
import LoginPage from "@/views/Auth/LoginPage.vue";
import RegisterPage from "@/views/Auth/RegisterPage.vue";
import CategoryPage from "@/views/CategoryPage.vue";
import SupplierListPage from "@/views/SupplierListPage.vue";
import StockLogsPage from "@/views/StockLogsPage.vue";
import MovementPage from "@/views/MovementPage.vue";

import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const routes = [
  // Auth pages (without layout)

  // Pages with layout
  {
    path: "/",
    component: LayoutWrapper,
    children: [
      { path: "", name: "Home", component: HomePage },
      { path: "dashboard", name: "Dashboard", component: DashboardPage },
      { path: "products", name: "Products", component: ProductListPage },
      {
        path: "products/edit/:id",
        name: "EditProduct",
        component: ProductEditPage,
      },
      {
        path: "/products/create",
        name: "ProductCreate",
        component: () => import("@/views/ProductCreatePage.vue"),
        meta: { requiresAuth: true }, // optional protection
      },
      {
        path: "/categories",
        name: "Categories",
        component: CategoryPage,
      },
      {
        path: "/login",
        name: "Login",
        component: LoginPage,
      },
      {
        path: "/register",
        name: "Register",
        component: RegisterPage,
      },
      // src/router/index.js

      {
        path: "/suppliers",
        name: "Suppliers",
        component: SupplierListPage,
      },

      {
        path: "/movements",
        name: "movements",
        component: MovementPage,
      },

      {
        path: "/logs",
        name: "logs",
        component: StockLogsPage,
      },
      {
        path: "/admin/users",
        name: "UserAdmin",
        component: () => import("@/views/userAdmin.vue"),
        meta: { requiresAuth: true, requiresAdmin: true }, // optional route guard
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next("/login");
  } else if ((to.path === "/login" || to.path === "/register") && auth.user) {
    // Prevent logged-in users from accessing login/register
    next("/");
  } else {
    next();
  }
});

export default router;
