<template>
  <div class="container-fluid text-center">
    <div class="row d-flex align-items-center min-vh-100">
      <div class="col"></div>
      <div class="col">
        <img
          alt="Bloglite logo"
          class="logo animate__animated animate__slideInUp"
          src="@/assets/logo.png"
          width="50"
          height="50"
        />
        <h1 class="welcome-message">Welcome to <span class="app-name">Bloglite</span></h1>
        <p>Please login to continue using bloglite</p>
        <router-link to="/login" type="button" class="btn btn-primary m-2">Login</router-link>
        <router-link to="/register" type="button" class="btn btn-success">Register</router-link>
      </div>
      <div class="col"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingHeader'
}
</script>

<style scoped>
.welcome-message {
  padding-top: 2rem;
}
</style>
