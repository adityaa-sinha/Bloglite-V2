<template>
  <div v-if="this.loading">
    <icon-loading></icon-loading>
  </div>
  <div v-else>
    <div v-if="this.unauth">
      <un-auth></un-auth>
    </div>
    <div v-else>
      <app-nav full="true"></app-nav>
      <edit-blog :username="this.currentuser" :post_id="this.$route.params.id"></edit-blog>
    </div>
  </div>
</template>
<script>
import AppNav from '../components/AppNav.vue'
import EditBlog from '../components/EditBlog.vue'
import IconLoading from '../components/icons/IconLoading.vue'
import UnAuth from '../components/UnAuth.vue'
export default {
  name: 'EditBlogView',
  components: {
    AppNav,
    EditBlog,
    IconLoading,
    UnAuth
  },
  data() {
    return {
      unauth: true,
      loading: true,
      currentuser: null
    }
  },
  methods: {
    async getCurrentUser() {
      const path = 'http://127.0.0.1:5000/api/currentuser'
      let response = await fetch(path, {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (!response.ok && response.status == 401) {
        this.loading = false
        this.unauth = true
      } else {
        this.loading = false
        this.unauth = false
        const res = await response.json()
        this.currentuser = res.username
      }
    }
  },
  created() {
    this.getCurrentUser()
  }
}
</script>
