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
      <div v-if="this.error_text">
        <error :msg="this.error_text.error_message" style="margin-top: 6rem"></error>
      </div>
      <div v-else>
        <Blog
          :title="this.blogdetails.title"
          :caption="this.blogdetails.caption"
          :image_url="this.blogdetails.image_url"
          :timestamp="this.blogdetails.timestamp"
          :posted_by="this.blogdetails.posted_by"
        ></Blog>
      </div>
    </div>
  </div>
</template>
<script>
import Blog from '../components/Blog.vue'
import AppNav from '../components/AppNav.vue'
import IconLoading from '../components/icons/IconLoading.vue'
import UnAuth from '../components/UnAuth.vue'
import error from '../components/error.vue'

export default {
  name: 'PostView',
  data() {
    return {
      blogdetails: '',
      loading: true,
      unauth: true,
      error_text: ''
    }
  },
  components: {
    Blog,
    AppNav,
    IconLoading,
    UnAuth,
    error
  },
  methods: {
    async getBlogDetails() {
      const path = 'http://127.0.0.1:5000/api/blog/' + this.$route.params.id
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
      } else if (!response.ok && response.status != 401) {
        this.loading = false
        this.unauth = false
        this.error_text = await response.json()
      } else {
        this.loading = false
        this.unauth = false
        this.blogdetails = await response.json()
      }
    }
  },
  created() {
    this.getBlogDetails()
  }
}
</script>
