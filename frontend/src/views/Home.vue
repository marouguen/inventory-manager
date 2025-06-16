<template>
  <section
    class="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-6 text-center bg-gray-50"
  >
    <!-- Profile Photo -->
    <div class="mb-6">
      <img
        src="/profile.jpg"
        alt="Profile"
        class="w-32 h-32 rounded-full shadow-lg border-4 border-white object-cover"
      />
    </div>

    <!-- Heading -->
    <div class="max-w-2xl">
      <h1 class="text-4xl md:text-5xl font-extrabold mb-6 leading-tight">
        Welcome to
        <span
          class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600"
        >
          Inventory Manager
        </span>
      </h1>

      <p class="text-lg md:text-xl text-gray-600 mb-8">
        A modern inventory and stock control solution built with Vue.js,
        FastAPI, and PostgreSQL. Designed for performance, reliability, and
        professional use.
      </p>

      <!-- Name & Title -->
      <div class="mb-10">
        <p class="text-gray-700 text-md md:text-lg font-medium">
          👨‍💻 Built by
          <span class="font-semibold text-gray-900"
            >Mohamed Amine Marouguen</span
          >
        </p>
      </div>

      <!-- Call to Action -->
      <RouterLink
        to="/dashboard"
        class="inline-block bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-6 rounded shadow transition"
      >
        Go to Dashboard
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
// No script logic needed
</script>
