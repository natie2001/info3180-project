<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const newMessage = ref('')

const messages = ref([
  {
    sender: 'Ashley',
    text: 'Hey, nice to meet you!'
  },
  {
    sender: 'You',
    text: 'Nice to meet you too!'
  }
])

function sendMessage() {
  if (!newMessage.value.trim()) return

  messages.value.push({
    sender: 'You',
    text: newMessage.value
  })

  newMessage.value = ''
}
</script>

<template>
  <h2 class="page-title">Chat #{{ route.params.id }}</h2>

  <div class="card p-3 mb-3">
    <div
      v-for="(message, index) in messages"
      :key="index"
      class="mb-2"
    >
      <strong>{{ message.sender }}:</strong>
      {{ message.text }}
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