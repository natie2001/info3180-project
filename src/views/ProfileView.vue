<script setup>
import { RouterLink } from 'vue-router'

const profile = {
  name: 'Demo User',
  age: 24,
  location: 'Kingston',
  bio: 'Friendly, adventurous, and interested in meeting new people.',
  interests: ['Music', 'Travel', 'Movies'],
  occupation: 'Student',
  education: 'University of the West Indies',
  photo: 'https://placehold.co/600x400?text=My+Profile'
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="card">
        <img :src="profile.photo" class="card-img-top profile-img" />

        <div class="card-body">
          <h2>{{ profile.name }}, {{ profile.age }}</h2>

          <p class="text-muted">
            <i class="bi bi-geo-alt"></i>
            {{ profile.location }}
          </p>

          <p>{{ profile.bio }}</p>

          <p>
            <strong>Occupation:</strong>
            {{ profile.occupation }}
          </p>

          <p>
            <strong>Education:</strong>
            {{ profile.education }}
          </p>

          <div class="mb-3">
            <span
              v-for="interest in profile.interests"
              :key="interest"
              class="badge bg-primary me-1"
            >
              {{ interest }}
            </span>
          </div>

          <RouterLink to="/profile/edit" class="btn btn-primary">
            Edit Profile
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>