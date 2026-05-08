import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    profile: null,
    hasProfile: false
  }),

  actions: {
    async fetchCurrentUser() {
      const response = await fetch('/api/auth/me', {
        credentials: 'include'
      })

      if (!response.ok) {
        this.user = null
        this.profile = null
        this.hasProfile = false
        return
      }

      const data = await response.json()

      this.user = data.user
      this.profile = data.profile
      this.hasProfile = data.has_profile
    },

    clearUser() {
      this.user = null
      this.profile = null
      this.hasProfile = false
    }
  }
})