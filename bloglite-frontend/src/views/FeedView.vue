<template>
  <!-- During loading of page -->
  <div v-if="loading">
    <icon-loading></icon-loading>
  </div>

  <div v-else>
    <!-- When an unauthenticated user visits the page -->
    <div v-if="this.unauth">
      <un-auth></un-auth>
    </div>

    <div v-else>
      <app-nav full="true"></app-nav>
      <div class="container text-center" style="margin-top: 5rem">
        <router-link to="/create-blog" style="text-decoration: none;"><i class="bi bi-pencil"></i><span class="ms-2">Write a blog</span></router-link>
      </div>

      <div class="container" style="margin-top: 3rem">
        <!-- Errors like no posts to show on feed is handled here -->
        <div v-if="error_text">
          <error :msg="error_text"></error>
        </div>
        
        <div v-else>
          <div class="row">
            <blog-tile
              v-for="blog in this.posts_list"
              :timestamp="blog.timestamp"
              :posted_by="blog.posted_by"
              :title="blog.title"
              :image_url="'http://127.0.0.1:5000'+blog.image_url"
              :caption_preview="blog.caption"
              :post_id="blog.id"
            ></blog-tile>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNav from '../components/AppNav.vue'
import BlogTile from '../components/BlogTile.vue'
import error from '../components/error.vue'
import UnAuth from '../components/UnAuth.vue'
import IconLoading from '../components/icons/IconLoading.vue'
export default {
  name: 'FeedView',
  components: {
    AppNav,
    BlogTile,
    error,
    UnAuth,
    IconLoading
  },
  data() {
    return {
      unauth: true,
      error_text: null,
      posts_list: null,
      loading: true
    }
  },
  methods: {
    async getFeed() {
      const response = await fetch('http://127.0.0.1:5000/api/feed', {
        method: 'get',
        headers: {
          'Content-type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })

      if (!response.ok && response.status != 401) {
        this.loading = false
        this.unauth = false
        const error = await response.json()
        this.error_text = error.error_message
      } else if (!response.ok && response.status == 401) {
        this.loading = false
        this.unauth = true
      } else {
        this.loading = false
        this.unauth = false
        const res = await response.json()
        this.posts_list = res
      }
    }
  },
  created() {
    this.getFeed()
  }
}
</script>

<style scoped></style>
