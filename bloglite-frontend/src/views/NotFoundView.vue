<template>
  <div class="container text-center">
    <div class="row d-flex align-items-center min-vh-100">
      <div class="col">
        <img alt="Bloglite logo" class="logo" src="@/assets/logo.png" width="50" height="50" />
        <h1 class="text-muted" style="margin-top: 4rem">404</h1>
        <p class="text-muted">Page Not Found</p>
        <router-link to="/" style="text-decoration: none">Go home</router-link>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'NotFoundView'
}
</script>
