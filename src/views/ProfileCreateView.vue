<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const profile = ref({
  age: '',
  location: '',
  bio: '',
  interests: '',
  occupation: '',
  education: '',
  visibility: 'public'
})

function saveProfile() {
  alert('Profile saved')
  router.push('/profile')
}
</script>

<template>
  <div class="card p-4">
    <h2 class="page-title">Create Profile</h2>

    <form @submit.prevent="saveProfile">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Age</label>
          <input v-model="profile.age" type="number" class="form-control" required />
        </div>

        <div class="col-md-6 mb-3">
          <label class="form-label">Location</label>
          <input v-model="profile.location" type="text" class="form-control" required />
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Bio</label>
        <textarea v-model="profile.bio" class="form-control" rows="4" required></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Interests</label>
        <input
          v-model="profile.interests"
          type="text"
          class="form-control"
          placeholder="Music, Travel, Cooking"
          required
        />
        <small class="text-muted">Enter at least 3 interests separated by commas.</small>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Occupation</label>
          <input v-model="profile.occupation" type="text" class="form-control" />
        </div>

        <div class="col-md-6 mb-3">
          <label class="form-label">Education</label>
          <input v-model="profile.education" type="text" class="form-control" />
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Profile Picture</label>
        <input type="file" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Visibility</label>
        <select v-model="profile.visibility" class="form-select">
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>

      <button class="btn btn-primary">
        Save Profile
      </button>
    </form>
  </div>
</template>