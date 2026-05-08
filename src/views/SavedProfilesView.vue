<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const savedProfiles = ref([])
const loading = ref(true)
const error = ref('')

async function loadSavedProfiles() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/favourites', {
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not load saved profiles'
      return
    }

    savedProfiles.value = data.favourites || data.saved || data
  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSavedProfiles()
})
</script>

<template>
  <h2 class="page-title">Saved Profiles</h2>

  <p class="text-muted">
    Profiles you saved for later.
  </p>

  <p v-if="loading" class="alert alert-info">
    Loading saved profiles...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <p
    v-if="!loading && !error && savedProfiles.length === 0"
    class="alert alert-warning"
  >
    No saved profiles yet.
  </p>

  <div class="row">
    <div
      v-for="profile in savedProfiles"
      :key="profile.user_id || profile.id"
      class="col-md-4 mb-4"
    >
      <div class="card h-100">
        <img
          :src="profile.profile_photo || 'https://placehold.co/600x400?text=Profile'"
          class="card-img-top profile-img"
        />

        <div class="card-body">
          <h4>
            {{ profile.name || profile.username || 'Profile' }}
            <span v-if="profile.age">, {{ profile.age }}</span>
          </h4>

          <p class="text-muted">
            {{ profile.location }}
          </p>

          <p>
            {{ profile.bio }}
          </p>

          <RouterLink
            :to="`/chat/${profile.user_id || profile.id}`"
            class="btn btn-primary w-100"
          >
            Message
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>