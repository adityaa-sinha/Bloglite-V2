<template>
  <nav v-if="full == 'true'" class="navbar navbar-expand-lg bg-body-tertiary fixed-top">
    <div class="container">
      <span class="navbar-brand">
        <RouterLink to="/" style="text-decoration: none; color: white"
          ><img
            alt="Bloglite logo"
            class="logo"
            src="@/assets/logo.png"
            width="30"
            height="30"
          /><span class="app-name" style="margin-left: 0.5rem">Bloglite</span></RouterLink
        >
      </span>
      <div style="float: right">
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarTogglerDemo02"
          aria-controls="navbarTogglerDemo02"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <!-- Search button opens SearchModal -->
              <router-link to="#" class="nav-link active" data-bs-toggle="modal" data-bs-target="#search"
                >Search</router-link
              >
            </li>
            <li class="nav-item">
              <router-link :to="'/profile/' + this.current_username" class="nav-link active"
                >My Profile</router-link
              >
            </li>
            <li class="nav-item">
              <button @click="this.logoutuser" class="btn btn-outline-light mx-3">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
  <nav v-else class="navbar fixed-top">
    <div class="container">
      <span class="navbar-brand m-2 h1">
        <RouterLink to="/" style="text-decoration: none; color: white"
          ><img
            alt="Bloglite logo"
            class="logo"
            src="@/assets/logo.png"
            width="30"
            height="30"
          /><span class="app-name" style="margin-left: 0.5rem">Bloglite</span></RouterLink
        >
      </span>
    </div>
  </nav>
  <search-modal></search-modal>
</template>

<script>
import SearchModal from './SearchModal.vue'
export default {
  name: 'AppNav',
  props: ['full'],
  data() {
    return {
      current_username: ''
    }
  },
  methods: {
    logoutuser() {
      localStorage.removeItem('auth')
      this.$router.push('/')
    },
    async get_current_user() {
      const response = await fetch('http://127.0.0.1:5000/api/currentuser', {
        method: 'get',
        headers: {
          'Content-type': 'application/json', // required to get JSON response
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (response.status != 401) {
        const res = await response.json()
        this.current_username = res.username
      }
    }
  },
  components: {
    SearchModal
  },
  created() {
    this.get_current_user()
  }
}
</script>
<style></style>
