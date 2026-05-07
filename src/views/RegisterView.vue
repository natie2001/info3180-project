<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const loading = ref(false)

async function register() {
  error.value = ''

  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(form.value)
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.message || 'Registration failed'
      return
    }

    router.push('/login')
  } catch (err) {
    error.value = 'Could not connect to server.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card p-4">
        <h2 class="page-title text-center">Create Account</h2>

        <form @submit.prevent="register">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="form.name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Confirm Password</label>
            <input v-model="form.confirmPassword" type="password" class="form-control" required />
          </div>

          <p v-if="error" class="alert alert-danger">
            {{ error }}
          </p>

          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Creating account...' : 'Register' }}
          </button>
        </form>

        <p class="text-center mt-3">
          Already have an account?
          <RouterLink to="/login">Login here</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>