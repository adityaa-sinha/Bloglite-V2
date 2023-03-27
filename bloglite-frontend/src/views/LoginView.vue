<template>
  <app-nav full="false"></app-nav>
  <login-form></login-form>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'
import AppNav from '../components/AppNav.vue'
export default {
  name: 'LoginView',
  components: {
    LoginForm,
    AppNav
  },
  // Check if auth token is already present, if yes, redirecting to feed
  beforeCreate() {
    if (localStorage.getItem('auth')) {
      this.$router.push('/feed')
    }
  }
}
</script>

<style scoped></style>
