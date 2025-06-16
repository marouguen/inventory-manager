<template>
  <div class="p-6 space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-semibold">👤 User Management</h1>
    </div>

    <div class="overflow-x-auto bg-white shadow rounded border border-gray-200">
      <table class="min-w-full text-sm text-left">
        <thead class="bg-gray-100 text-gray-700 uppercase tracking-wider">
          <tr>
            <th class="p-3">ID</th>
            <th class="p-3">Email</th>
            <th class="p-3">Role</th>
            <th class="p-3">Active</th>
            <th class="p-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="user in users"
            :key="user.id"
            class="border-t hover:bg-gray-50"
          >
            <td class="p-3">{{ user.id }}</td>
            <td class="p-3">{{ user.email }}</td>
            <td class="p-3">
              <select
                v-model="user.role"
                @change="updateRole(user)"
                class="input"
              >
                <option value="user">user</option>
                <option value="admin">admin</option>
              </select>
            </td>
            <td class="p-3">{{ user.is_active ? "Yes" : "No" }}</td>
            <td class="p-3 text-right">
              <button @click="deleteUser(user.id)" class="btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";
import { useRouter } from "vue-router";

const users = ref([]);
const router = useRouter();

const fetchUsers = async () => {
  try {
    const res = await api.get("/users");
    users.value = res.data;
  } catch (err) {
    if (err.response?.status === 403) {
      alert("Access denied: Admins only.");
      router.push("/");
    } else {
      console.error(err);
    }
  }
};

const updateRole = async (user) => {
  try {
    await api.patch(`/users/${user.id}`, { role: user.role });
  } catch (err) {
    alert("Failed to update role");
    await fetchUsers(); // Reset to original if failed
  }
};

const deleteUser = async (id) => {
  if (!confirm("Are you sure you want to delete this user?")) return;

  try {
    await api.delete(`/users/${id}`);
    users.value = users.value.filter((u) => u.id !== id);
  } catch (err) {
    alert("Failed to delete user.");
  }
};

onMounted(fetchUsers);
</script>

<style scoped>
.input {
  @apply w-full p-2 border rounded;
}
.btn-danger {
  @apply bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700;
}
</style>
