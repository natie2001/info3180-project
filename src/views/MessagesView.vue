<script setup>
import { RouterLink } from 'vue-router'

const conversations = [
  {
    id: 1,
    name: 'Ashley Brown',
    lastMessage: 'Hey, nice to meet you!'
  },
  {
    id: 2,
    name: 'Terrica Smith',
    lastMessage: 'What kind of movies do you like?'
  }
]
</script>

<template>
  <h2 class="page-title">Messages</h2>

  <div
    v-for="conversation in conversations"
    :key="conversation.id"
    class="card p-3 mb-3"
  >
    <h4>{{ conversation.name }}</h4>
    <p class="text-muted">{{ conversation.lastMessage }}</p>

    <RouterLink :to="`/chat/${conversation.id}`" class="btn btn-primary">
      Open Conversation
    </RouterLink>
  </div>
</template>