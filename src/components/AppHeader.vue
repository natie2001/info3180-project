<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const router = useRouter()
const auth = useAuthStore()

onMounted(() => {
  auth.fetchCurrentUser()
})

async function logout() {
  await fetch('/api/auth/logout', {
    method: 'POST',
    credentials: 'include'
  })

  auth.clearUser()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg app-navbar fixed-top">
    <div class="container">
      <RouterLink class="navbar-brand brand" to="/">
        <i class="bi bi-heart-fill me-2"></i>
        DriftDater
      </RouterLink>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-lg-center">

          <template v-if="auth.user">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/dashboard">Browse</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/search">Search</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/saved">Saved</RouterLink>
            </li>

            <li class="nav-item ms-lg-3">
              <button class="btn btn-light btn-sm rounded-pill px-3" @click="logout">
                Logout
              </button>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item ms-lg-3">
              <RouterLink class="btn btn-light btn-sm rounded-pill px-3" to="/register">
                Join Now
              </RouterLink>
            </li>
          </template>

        </ul>
      </div>
    </div>
  </nav>
</template>