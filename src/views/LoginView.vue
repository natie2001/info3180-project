<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuthStore()

async function login() {
  error.value = ''
  loading.value = true

  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Login failed'
      return
    }
    await auth.fetchCurrentUser()
    
    if (data.has_profile) {
      router.push('/dashboard')
    } else {
      router.push('/profile')
    }
    
  } catch (err) {
    error.value = 'Could not connect to server.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4">
        <h2 class="page-title text-center">Login</h2>

        <form @submit.prevent="login">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
          </div>

          <p v-if="error" class="alert alert-danger">
            {{ error }}
          </p>

          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <p class="text-center mt-3">
          No account?
          <RouterLink to="/register">Register here</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>