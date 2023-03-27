<template>
  <div class="container text-center">
    <div class="row d-flex align-items-center min-vh-100">
      <div class="col"></div>
      <div class="col">
        <img alt="Bloglite logo" class="logo" src="@/assets/logo.png" width="50" height="50" />
        <h1 class="text-muted" style="margin-top: 4rem">401</h1>
        <p class="text-muted">You are not authenticated. Please supply the correct credentials.</p>
        <router-link to="/" @click="this.goHome" style="text-decoration: none">Go home</router-link>
      </div>
      <div class="col"></div>
    </div>
  </div>
</template>
<style></style>
<script>
export default {
  name: 'UnAuth',
  methods: {
    goHome() {
      localStorage.removeItem('auth')
    }
  }
}
</script>
