<template>
  <app-nav full="false"></app-nav>
  <register-form></register-form>
</template>

<script>
import RegisterForm from '../components/RegisterForm.vue'
import AppNav from '../components/AppNav.vue'
export default {
  name: 'RegisterView',
  components: {
    RegisterForm,
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
