<template>
  <div class="max-w-md mx-auto mt-24 p-6 border rounded shadow bg-white">
    <h2 class="text-2xl font-semibold mb-4">Register</h2>
    <form @submit.prevent="handleRegister">
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full p-2 border rounded"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-2 border rounded"
          required
        />
      </div>
      <button
        type="submit"
        class="bg-green-600 text-white px-4 py-2 rounded w-full"
      >
        Register
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const email = ref("");
const password = ref("");
const auth = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  try {
    await auth.register(email.value, password.value);
    alert("Registration successful. You can now log in.");
    router.push("/login");
  } catch (error) {
    alert(
      "Registration failed: " +
        (error.response?.data?.detail || "Invalid input")
    );
  }
};
</script>
