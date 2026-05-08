<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

const form = ref({
  name: '',
  age: '',
  bio: '',
  location: '',
  parish: '',
  gender: '',
  looking_for: '',
  occupation: '',
  relationship_type: '',
  interests: ''
})

const profilePhoto = ref(null)

const loading = ref(false)
const error = ref('')
const success = ref('')

function handleFile(event) {
  profilePhoto.value = event.target.files[0]
}

async function createProfile() {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const formData = new FormData()

    Object.keys(form.value).forEach((key) => {
      formData.append(key, form.value[key])
    })

    if (profilePhoto.value) {
      formData.append('profile_photo', profilePhoto.value)
    }

    const response = await fetch('/api/profiles', {
      method: 'POST',
      credentials: 'include',
      body: formData
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not create profile'
      return
    }

    success.value = 'Profile created successfully!'

    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)

  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="card p-4">
        <h2 class="page-title text-center">
          Complete Your Profile
        </h2>

        <form @submit.prevent="createProfile">

          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="form.name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Age</label>
            <input v-model="form.age" type="number" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Bio</label>
            <textarea v-model="form.bio" class="form-control"></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Location</label>
            <input v-model="form.location" type="text" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Parish</label>
            <input v-model="form.parish" type="text" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Gender</label>
            <select v-model="form.gender" class="form-select">
              <option value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Looking For</label>
            <select v-model="form.looking_for" class="form-select">
              <option value="">Select Preference</option>
              <option>Male</option>
              <option>Female</option>
              <option>Any</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Occupation</label>
            <input v-model="form.occupation" type="text" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Relationship Type</label>

            <select v-model="form.relationship_type" class="form-select">
              <option value="">Select Relationship Type</option>

              <option>Friendship</option>
              <option>Casual Dating</option>
              <option>Serious Relationship</option>
              <option>Long-Term Relationship</option>
              <option>Marriage</option>
              <option>Networking</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Interests</label>
            <input
              v-model="form.interests"
              type="text"
              class="form-control"
              placeholder="Music, Sports, Gaming"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Profile Photo</label>
            <input
              type="file"
              class="form-control"
              @change="handleFile"
            />
          </div>

          <div class="text-end mb-3">
            <RouterLink to="/profile/edit" class="btn btn-outline-primary rounded-pill">
               Edit Existing Profile
            </RouterLink>
          </div>

          <p v-if="error" class="alert alert-danger">
            {{ error }}
          </p>

          <p v-if="success" class="alert alert-success">
            {{ success }}
          </p>

          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Saving Profile...' : 'Save Profile' }}
          </button>

        </form>
      </div>
    </div>
  </div>
</template>