<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const conversations = ref([])
const loading = ref(true)
const error = ref('')

async function loadConversations() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/conversations', {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not load conversations'
      return
    }

    conversations.value = data.conversations || data.matches || data
  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadConversations()
})
</script>

<template>
  <h2 class="page-title">Messages</h2>

  <p v-if="loading" class="alert alert-info">
    Loading conversations...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <p v-if="!loading && !error && conversations.length === 0" class="alert alert-warning">
    No conversations yet. You need a mutual match before messaging.
  </p>

  <div
    v-for="conversation in conversations"
    :key="conversation.user_id || conversation.id"
    class="card p-3 mb-3"
  >
    <h4>
      {{ conversation.name || conversation.full_name || conversation.username || conversation.handle || 'Conversation' }}
    </h4>

    <p class="text-muted">
      {{ conversation.last_message || conversation.lastMessage || 'Start a conversation.' }}
    </p>

    <RouterLink
      :to="`/chat/${conversation.user_id}`"
      class="btn btn-primary"
    >
      Open Conversation
    </RouterLink>
  </div>
</template>