<script setup>
import { ref, onMounted } from 'vue'

const profiles = ref([])
const loading = ref(true)
const error = ref('')

async function loadProfiles() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/browse', {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not load profiles'
      return
    }

    profiles.value = data.profiles || data.users || data
  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

function getTargetId(profile) {
  return profile.user_id || profile.member_id
}

async function saveProfile(profile) {
  const targetId = getTargetId(profile)

  if (!targetId) {
    alert('Could not find user ID for this profile.')
    return
  }

  try {
    const response = await fetch(`/api/favourites/${targetId}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      alert(data.error || data.message || 'Could not save profile')
      return
    }

    alert('Profile saved!')
  } catch (err) {
    alert('Could not connect to backend.')
  }
}

async function likeProfile(profile) {
  const targetId = getTargetId(profile)

  if (!targetId) {
    alert('Could not find user ID for this profile.')
    return
  }

  try {
    const response = await fetch(`/api/like/${targetId}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      alert(data.error || data.message || 'Could not like profile')
      return
    }

    if (data.is_match) {
      alert('It’s a match! You can now message this person.')
    } else {
      alert('Profile liked.')
    }

    profiles.value = profiles.value.filter((p) => getTargetId(p) !== targetId)
  } catch (err) {
    alert('Could not connect to backend.')
  }
}

async function passProfile(profile) {
  const targetId = getTargetId(profile)

  if (!targetId) {
    alert('Could not find user ID for this profile.')
    return
  }

  try {
    const response = await fetch(`/api/pass/${targetId}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      alert(data.error || data.message || 'Could not pass profile')
      return
    }

    profiles.value = profiles.value.filter((p) => getTargetId(p) !== targetId)
  } catch (err) {
    alert('Could not connect to backend.')
  }
}

onMounted(() => {
  loadProfiles()
})
</script>

<template>
  <h2 class="page-title">Dashboard</h2>

  <p class="text-muted">
    Suggested profiles based on your preferences.
  </p>

  <p v-if="loading" class="alert alert-info">
    Loading profiles...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <p v-if="!loading && !error && profiles.length === 0" class="alert alert-warning">
    No suggested profiles available right now.
  </p>

  <div class="row">
    <div
      v-for="profile in profiles"
      :key="profile.user_id || profile.member_id || profile.id"
      class="col-md-4 mb-4"
    >
      <div class="card h-100 match-card">
        <img
          :src="profile.profile_photo || profile.photo || profile.avatar || 'https://placehold.co/600x400?text=Profile'"
          class="card-img-top profile-img"
          alt="Profile photo"
        />

        <div class="card-body">
          <h4>
            {{ profile.name || profile.full_name || profile.username || profile.handle || 'Profile' }}
            <span v-if="profile.age">, {{ profile.age }}</span>
          </h4>

          <p class="text-muted" v-if="profile.location || profile.city_area">
            <i class="bi bi-geo-alt"></i>
            {{ profile.location || profile.city_area }}
          </p>

          <p>
            {{ profile.bio || profile.about_me || profile.description || 'No bio added yet.' }}
          </p>

          <p v-if="profile.match_score">
            <strong>Match Score:</strong> {{ profile.match_score }}%
          </p>

          <div class="mb-3" v-if="profile.interests">
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

          <button class="btn btn-outline-primary mt-2 w-100" @click="saveProfile(profile)">
            <i class="bi bi-bookmark-heart"></i>
            Save Profile
          </button>
        </div>
      </div>
    </div>
  </div>
</template>