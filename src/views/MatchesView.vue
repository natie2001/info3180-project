<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const matches = ref([])
const loading = ref(true)
const error = ref('')
const matchCount = ref(0)

async function loadMatches() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/matches', {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not load matches'
      return
    }

    matches.value = data.matches || data.connections || data
    matchCount.value = matches.value.length
  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMatches()
})
</script>

<template>
  <h2 class="page-title">Your Matches</h2>

  <p class="text-muted">
    You have {{ matchCount }} match{{ matchCount === 1 ? '' : 'es' }}.
  </p>

  <p v-if="loading" class="alert alert-info">
    Loading matches...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <p v-if="!loading && !error && matches.length === 0" class="alert alert-warning">
    You do not have any matches yet.
  </p>

  <div class="row">
    <div
      v-for="match in matches"
      :key="match.user_id || match.id"
      class="col-md-6 mb-3"
    >
      <div class="card p-3">
        <h4>
          {{ match.name || match.full_name || match.username || match.handle || 'Match' }}
          <span v-if="match.age">, {{ match.age }}</span>
        </h4>

        <p class="text-muted" v-if="match.location || match.city_area">
          <i class="bi bi-geo-alt"></i>
          {{ match.location || match.city_area }}
        </p>

        <p v-if="match.bio || match.about_me">
          {{ match.bio || match.about_me }}
        </p>

        <RouterLink
          :to="`/chat/${match.user_id || match.id}`"
          class="btn btn-primary"
        >
          Message
        </RouterLink>
      </div>
    </div>
  </div>
</template>