<script setup>
import { RouterLink } from 'vue-router'

const matches = [
  {
    id: 1,
    name: 'Ashley Brown',
    age: 23,
    location: 'Kingston',
    sharedInterests: ['Music', 'Food']
  },
  {
    id: 2,
    name: 'Jordan Smith',
    age: 25,
    location: 'Montego Bay',
    sharedInterests: ['Movies', 'Fitness']
  }
]
</script>

<template>
  <h2 class="page-title">Your Matches</h2>

  <p class="text-muted">
    These are users who liked you back.
  </p>

  <div class="row">
    <div
      v-for="match in matches"
      :key="match.id"
      class="col-md-6 mb-3"
    >
      <div class="card p-3">
        <h4>{{ match.name }}, {{ match.age }}</h4>

        <p class="text-muted">
          <i class="bi bi-geo-alt"></i>
          {{ match.location }}
        </p>

        <p>
          <strong>Shared interests:</strong>
          {{ match.sharedInterests.join(', ') }}
        </p>

        <RouterLink :to="`/chat/${match.id}`" class="btn btn-primary">
          Message
        </RouterLink>
      </div>
    </div>
  </div>
</template>