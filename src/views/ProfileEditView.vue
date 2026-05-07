<template>
  <div class="card p-4">
    <h2 class="page-title">Edit Profile</h2>
    <p class="text-muted">
      This page will allow users to update their profile details.
    </p>

    <RouterLink to="/profile/create" class="btn btn-primary">
      Edit Profile Form
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>