<script setup>
import { RouterLink, useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <RouterLink class="navbar-brand fw-bold" to="/">
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
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">Home</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
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
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>

          <li class="nav-item">
            <button class="btn btn-outline-light btn-sm ms-2" @click="logout">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>







