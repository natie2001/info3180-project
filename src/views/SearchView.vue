<script setup>
import { ref } from 'vue'

const search = ref('')
const location = ref('')
const minAge = ref('')
const maxAge = ref('')

const profiles = ref([])
const loading = ref(false)
const error = ref('')

async function searchProfiles() {
  loading.value = true
  error.value = ''

  try {
    const params = new URLSearchParams()

    if (search.value) params.append('q', search.value)
    if (location.value) params.append('location', location.value)
    if (minAge.value) params.append('min_age', minAge.value)
    if (maxAge.value) params.append('max_age', maxAge.value)

    const response = await fetch(`/api/search?${params.toString()}`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Search failed'
      return
    }

    profiles.value = data.results || data.profiles || data

  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <h2 class="page-title">Search Profiles</h2>

  <div class="card p-4 mb-4">
    <div class="row">
      <div class="col-md-4 mb-3">
        <label class="form-label">Search</label>
        <input v-model="search" type="text" class="form-control" />
      </div>

      <div class="col-md-3 mb-3">
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

      <div class="col-md-1 d-flex align-items-end">
        <button class="btn btn-primary w-100" @click="searchProfiles">
          Go
        </button>
      </div>
    </div>
  </div>

  <p v-if="loading" class="alert alert-info">
    Searching...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <div
    v-for="profile in profiles"
    :key="profile.id"
    class="card p-3 mb-3"
  >
    <h4>
      {{ profile.name || profile.username || profile.handle }}
      <span v-if="profile.age">, {{ profile.age }}</span>
    </h4>

    <p class="text-muted">
      {{ profile.location }}
    </p>

    <p>
      {{ profile.bio }}
    </p>
  </div>

  <p v-if="!loading && profiles.length === 0" class="alert alert-warning">
    No profiles found.
  </p>
</template>
