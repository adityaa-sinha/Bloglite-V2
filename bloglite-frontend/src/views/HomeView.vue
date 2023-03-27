<template>
  <landing-header></landing-header>
</template>

<style scoped></style>
<script>
import LandingHeader from '../components/LandingHeader.vue'
export default {
  name: 'HomeView',
  components: {
    LandingHeader
  },
  // Check if auth token is already present, if yes, redirecting to feed
  beforeCreate() {
    if (localStorage.getItem('auth')) {
      this.$router.push('/feed')
    }
  }
}
</script>
