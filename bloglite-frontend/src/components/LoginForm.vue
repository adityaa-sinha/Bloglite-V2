<template>
  <section>
    <div class="container mt-5 pt-5">
      <div class="row">
        <div class="col-12 col col-sm-8 col-md-6 m-auto mt-5 pt-5">
          <div class="card border-0">
            <div class="card-body">
              <div class="card-title"><h2>Log in</h2></div>
              <h6 class="card-subtitle mb-2 text-muted">Continue reading and writing amazing blogs</h6>
              <!-- Custom submit -->
              <form @submit.prevent="this.userlogin">
                <input
                  type="email"
                  class="form-control my-4 py-2"
                  id="Email"
                  placeholder="Email"
                  v-model="email"
                  required
                />
                <p style="text-align: center">OR</p>
                <input
                  type="text"
                  class="form-control my-4 py-2"
                  id="Username"
                  placeholder="Username"
                  v-model="username"
                  required
                />
                <input
                  type="password"
                  class="form-control my-4 py-2"
                  id="Password"
                  placeholder="Password"
                  v-model="password"
                  required
                />
                <div class="text-center mt-3">
                  <!-- after fetch request  -->
                  <button v-if="!loading" class="btn btn-primary" type="submit">Login</button>
                  <!-- during fetch request  -->
                  <div v-else class="spinner-grow text-primary" role="status"></div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-3 pt-3 text-center">
      New to bloglite?
      <RouterLink to="/register" style="text-decoration: none">Register</RouterLink>
    </div>
  </section>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async userlogin() {
      this.loading = true
      const path = ' http://127.0.0.1:5000/login?include_auth_token'
      const body = {
        email: this.email,
        username: this.username,
        password: this.password
      }
      let response = await fetch(path, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json' // required to receive json response
        },
        body: JSON.stringify(body)
      })
      if (!response.ok) {
        // Using vanillaJS because vue was causing a few issues
        const error_data = await response.json()
        const error_list = error_data.response.errors
        const parentNode = document.getElementsByClassName('card')[0]
        for (let i = 0; i < error_list.length; i++) {
          const node = document.createElement('div')
          const textnode = document.createTextNode(error_list[i])
          node.appendChild(textnode)
          node.classList.add('alert')
          node.classList.add('alert-danger')
          node.classList.add('alert-dismissible')
          node.classList.add('fade')
          node.classList.add('show')
          node.setAttribute('role', 'alert')
          const button = document.createElement('button')
          button.setAttribute('type', 'button')
          button.setAttribute('data-bs-dismiss', 'alert')
          button.setAttribute('aria-label', 'Close')
          button.classList.add('btn-close')
          node.appendChild(button)
          parentNode.appendChild(node)
        }
        this.password = ''
        this.loading = false
      } else {
        const res = await response.json()
        const token = res.response.user.authentication_token
        localStorage.setItem('auth', token)
        this.loading = false
        this.$router.push('/')
      }
    }
  },
  // Either email or username is required for authentication
  watch: {
    email() {
      document.getElementById('Username').required = false
    },
    username() {
      document.getElementById('Email').required = false
    }
  }
}
</script>

<style scoped>
.btn {
  font-size: large;
}
</style>
