<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const messages = ref([])
const newMessage = ref('')
const loading = ref(true)
const error = ref('')
const currentUserId = ref(null)
const peerName = ref('Match')

async function loadCurrentUser() {
  const response = await fetch('/api/auth/me', {
    credentials: 'include'
  })

  const data = await response.json()

  currentUserId.value = data.user.id
}

async function loadPeerProfile() {
  try {
    const response = await fetch(`/api/profiles/${route.params.id}`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      peerName.value =
        data.profile?.name ||
        data.name ||
        'Match'
    }
  } catch (err) {
    console.log(err)
  }
}

async function loadMessages() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`/api/messages/${route.params.id}`, {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not load messages'
      return
    }

    messages.value = data.messages || data.thread || data
  } catch (err) {
    error.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

async function sendMessage() {
  if (!newMessage.value.trim()) return

  try {
    const response = await fetch(`/api/messages/${route.params.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        message: newMessage.value,
        body: newMessage.value,
        content: newMessage.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Could not send message'
      return
    }

    newMessage.value = ''
    await loadMessages()
  } catch (err) {
    error.value = 'Could not connect to backend.'
  }
}

onMounted(async () => {
  await loadCurrentUser()
  await loadPeerProfile()
  await loadMessages()
})
</script>

<template>
  <h2 class="page-title">Chat</h2>

  <p v-if="loading" class="alert alert-info">
    Loading messages...
  </p>

  <p v-if="error" class="alert alert-danger">
    {{ error }}
  </p>

  <div class="card p-3 mb-3">
    <p v-if="!loading && messages.length === 0" class="text-muted">
      No messages yet. Start the conversation.
    </p>

    <div
      v-for="message in messages"
      :key="message.id || message.created_at"
      class="mb-2"
    >
      <strong>
        {{ 
          (message.author_id || message.sender_id) === currentUserId 
            ? 'You'
            : peerName
        }}:
      </strong>

      {{ message.body || message.message || message.content || message.text }}
    </div>
  </div>

  <form @submit.prevent="sendMessage">
    <div class="mb-3">
      <textarea
        v-model="newMessage"
        class="form-control"
        rows="3"
        placeholder="Type your message..."
      ></textarea>
    </div>

    <button class="btn btn-primary">
      Send
    </button>
  </form>
</template>