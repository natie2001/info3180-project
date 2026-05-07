<script setup>
import { ref } from 'vue'

const profiles = ref([
  {
    id: 1,
    name: 'Ashley Brown',
    age: 23,
    location: 'Kingston',
    bio: 'Loves music, beach trips, and trying new restaurants.',
    interests: ['Music', 'Travel', 'Food'],
    photo: 'https://placehold.co/600x400?text=Profile+1'
  },
  {
    id: 2,
    name: 'Jordan Smith',
    age: 25,
    location: 'Montego Bay',
    bio: 'Enjoys fitness, movies, gaming, and good conversation.',
    interests: ['Fitness', 'Movies', 'Gaming'],
    photo: 'https://placehold.co/600x400?text=Profile+2'
  },
  {
    id: 3,
    name: 'Taylor Green',
    age: 24,
    location: 'Spanish Town',
    bio: 'Creative person who enjoys art, music, and coffee.',
    interests: ['Art', 'Coffee', 'Music'],
    photo: 'https://placehold.co/600x400?text=Profile+3'
  }
])

function likeProfile(profile) {
  alert(`You liked ${profile.name}`)
}

function passProfile(profile) {
  alert(`You passed on ${profile.name}`)
}
</script>

<template>
  <h2 class="page-title">Dashboard</h2>

  <p class="text-muted">
    Suggested profiles based on your preferences.
  </p>

  <div class="row">
    <div
      v-for="profile in profiles"
      :key="profile.id"
      class="col-md-4 mb-4"
    >
      <div class="card h-100">
        <img :src="profile.photo" class="card-img-top profile-img" />

        <div class="card-body">
          <h4>{{ profile.name }}, {{ profile.age }}</h4>
          <p class="text-muted">
            <i class="bi bi-geo-alt"></i>
            {{ profile.location }}
          </p>

          <p>{{ profile.bio }}</p>

          <div class="mb-3">
            <span
              v-for="interest in profile.interests"
              :key="interest"
              class="badge bg-primary me-1"
            >
              {{ interest }}
            </span>
          </div>

          <button class="btn btn-success me-2" @click="likeProfile(profile)">
            <i class="bi bi-heart-fill"></i>
            Like
          </button>

          <button class="btn btn-outline-secondary" @click="passProfile(profile)">
            Pass
          </button>
        </div>
      </div>
    </div>
  </div>
</template>