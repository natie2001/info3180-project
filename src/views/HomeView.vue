<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="text-center py-5">
    <h1 class="display-1 fw-bold text-primary">
      DriftDater
    </h1>

    <p class="lead mt-3">
      Find meaningful connections near you.
    </p>

    <div class="mt-4">
      <RouterLink to="/register" class="btn btn-primary btn-lg me-3">
        Get Started
      </RouterLink>

      <RouterLink to="/login" class="btn btn-outline-dark btn-lg">
        Login
      </RouterLink>
    </div>
  </section>
</template>


