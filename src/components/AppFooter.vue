<template>
  <footer class="text-center mt-5 py-4 bg-dark text-white">
    <p class="mb-0">
      Copyright &copy; {{ year }} DriftDater
    </p>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>