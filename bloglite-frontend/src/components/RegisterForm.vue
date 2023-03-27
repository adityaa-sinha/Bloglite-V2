<template>
  <section>
    <div class="container mt-5 pt-5">
      <div class="row">
        <div class="col-12 col col-sm-8 col-md-6 m-auto mt-5 pt-5">
          <div class="card border-0">
            <div class="card-body">
              <div class="card-title"><h2>Register</h2></div>
              <h6 class="card-subtitle mb-2 text-muted">To read and write amazing blogs</h6>
              <!-- Custom submit -->
              <form @submit.prevent="this.userregister">
                <input
                  type="email"
                  class="form-control my-4 py-2"
                  id="Email"
                  placeholder="Email"
                  v-model="email"
                  required
                />
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
                  <!-- after fetch request -->
                  <button v-if="!loading" class="btn btn-success" type="submit">Register</button>
                  <!-- during fetch request -->
                  <div v-else class="spinner-grow text-success" role="status"></div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-3 pt-3 text-center">
      Already a user? <RouterLink to="/login" style="text-decoration: none">Login</RouterLink>
    </div>
  </section>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async userregister() {
      this.loading = true
      const path = ' http://127.0.0.1:5000/register'
      const body = {
        email: this.email,
        username: this.username,
        password: this.password
      }
      let response = await fetch(path, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json' // required to get JSON response
        },
        body: JSON.stringify(body)
      })
      if (!response.ok) {
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
        const parentNode = document.getElementsByClassName('card')[0]
        const node = document.createElement('div')
        const textnode = document.createTextNode(
          'Registration successful! Please login through the log in page.'
        )
        node.appendChild(textnode)
        node.classList.add('alert')
        node.classList.add('alert-success')
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
        this.password = ''
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.btn {
  font-size: large;
}
</style>
