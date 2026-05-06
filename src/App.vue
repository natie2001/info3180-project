<script setup>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <AppHeader />

  <main class="container py-4">
    <RouterView />
  </main>

  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
}
</style>