<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="hero-card text-center">
    <h1 class="hero-title">
      DriftDater
    </h1>

    <p class="lead mt-3">
      Find meaningful connections near you.
    </p>

    <div class="mt-4">
      <RouterLink to="/register" class="btn btn-primary btn-lg me-3">
        Get Started
      </RouterLink>

      <RouterLink to="/login" class="btn btn-outline-dark btn-lg rounded-pill px-4">
        Login
      </RouterLink>
    </div>
  </section>

  <section class="row mt-5 g-4">
    <div class="col-md-4">
      <div class="card p-4 text-center h-100 match-card">
        <i class="bi bi-person-heart fs-1 text-danger"></i>
        <h4 class="mt-3">Create Profile</h4>
        <p>Add your bio, interests, photos, and dating preferences.</p>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card p-4 text-center h-100 match-card">
        <i class="bi bi-stars fs-1 text-danger"></i>
        <h4 class="mt-3">Find Matches</h4>
        <p>Discover users based on age, location, and shared interests.</p>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card p-4 text-center h-100 match-card">
        <i class="bi bi-chat-dots fs-1 text-danger"></i>
        <h4 class="mt-3">Start Chatting</h4>
        <p>Message users after a mutual match is created.</p>
      </div>
    </div>
  </section>
</template>