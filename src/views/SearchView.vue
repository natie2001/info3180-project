<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const location = ref('')
const minAge = ref('')
const maxAge = ref('')

const profiles = ref([
  {
    id: 1,
    name: 'Ashley Brown',
    age: 23,
    location: 'Kingston',
    interests: ['Music', 'Food', 'Travel']
  },
  {
    id: 2,
    name: 'Terrica Smith',
    age: 25,
    location: 'Montego Bay',
    interests: ['Movies', 'Gaming', 'Fitness']
  },
  {
    id: 3,
    name: 'Taylor Green',
    age: 24,
    location: 'Kingston',
    interests: ['Art', 'Coffee', 'Music']
  }
])

const filteredProfiles = computed(() => {
  return profiles.value.filter((profile) => {
    const matchesSearch =
      search.value === '' ||
      profile.name.toLowerCase().includes(search.value.toLowerCase()) ||
      profile.interests.join(' ').toLowerCase().includes(search.value.toLowerCase())

    const matchesLocation =
      location.value === '' ||
      profile.location.toLowerCase().includes(location.value.toLowerCase())

    const matchesMinAge =
      minAge.value === '' || profile.age >= Number(minAge.value)

    const matchesMaxAge =
      maxAge.value === '' || profile.age <= Number(maxAge.value)

    return matchesSearch && matchesLocation && matchesMinAge && matchesMaxAge
  })
})
</script>

<template>
  <h2 class="page-title">Search Profiles</h2>

  <div class="card p-4 mb-4">
    <div class="row">
      <div class="col-md-4 mb-3">
        <label class="form-label">Search by name or interest</label>
        <input v-model="search" type="text" class="form-control" />
      </div>

      <div class="col-md-4 mb-3">
        <label class="form-label">Location</label>
        <input v-model="location" type="text" class="form-control" />
      </div>

      <div class="col-md-2 mb-3">
        <label class="form-label">Min Age</label>
        <input v-model="minAge" type="number" class="form-control" />
      </div>

      <div class="col-md-2 mb-3">
        <label class="form-label">Max Age</label>
        <input v-model="maxAge" type="number" class="form-control" />
      </div>
    </div>
  </div>

  <div
    v-for="profile in filteredProfiles"
    :key="profile.id"
    class="card p-3 mb-3"
  >
    <h4>{{ profile.name }}, {{ profile.age }}</h4>

    <p class="text-muted">
      <i class="bi bi-geo-alt"></i>
      {{ profile.location }}
    </p>

    <p>
      <strong>Interests:</strong>
      {{ profile.interests.join(', ') }}
    </p>
  </div>

  <p v-if="filteredProfiles.length === 0" class="alert alert-warning">
    No profiles found.
  </p>
</template>