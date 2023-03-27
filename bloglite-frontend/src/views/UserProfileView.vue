<template>
  <div v-if="!this.loading">
    <!-- When an unauthenticated user visits the page -->
    <div v-if="this.unauth">
      <un-auth></un-auth>
    </div>

    <div v-else>
      <app-nav full="true"></app-nav>
      <!-- Handling errors like user does not exist  -->
      <div v-if="this.error_text">
        <error :msg="this.error_text" style="margin-top: 8rem"></error>
      </div>
      <div v-else>
        <user-stats
          v-if="this.user_stats.user_dp"
          :username="$route.params.username"
          :dp_url="'http://127.0.0.1:5000' + this.user_stats.user_dp"
          :ownprofile="this.user_stats.is_current_user"
          :following="this.user_stats.is_current_user_following"
          :posts_count="this.user_stats.posts"
          :followers_count="this.user_stats.followers"
          :following_count="this.user_stats.following"
        ></user-stats>
        <user-stats
          v-else
          :username="$route.params.username"
          :dp_url="null"
          :ownprofile="this.user_stats.is_current_user"
          :following="this.user_stats.is_current_user_following"
          :posts_count="this.user_stats.posts"
          :followers_count="this.user_stats.followers"
          :following_count="this.user_stats.following"
        ></user-stats>
        <div class="container mt-5">
          <div class="row">
            <div class="col-sm-6">
              <h3>Posts</h3>
            </div>
            <!-- Create new blog and Export blogs option to current user -->
            <div v-if="this.user_stats.is_current_user" class="col-sm-6 d-flex justify-content-end">
              <router-link to="/create-blog" style="text-decoration: none"
                ><i class="bi bi-plus-circle-fill me-3" style="font-style: normal">
                  Create</i
                ></router-link
              ><router-link to="#" style="text-decoration: none" @click="this.export"
                ><i class="bi bi-filetype-csv" style="font-style: normal">
                  Export as CSV</i
                ></router-link
              >
            </div>
            <hr />
          </div>
        </div>
        <!-- User Posts -->
        <div class="container">
          <div class="row">
            <blog-tile
              v-for="blog in this.user_posts"
              :owner="this.user_stats.is_current_user"
              :timestamp="blog.timestamp"
              :posted_by="blog.posted_by"
              :title="blog.title"
              :image_url="'http://127.0.0.1:5000' + blog.image_url"
              :caption_preview="blog.caption"
              :post_id="blog.id"
            ></blog-tile>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- During loading of page -->
  <div v-else>
    <icon-loading></icon-loading>
  </div>
</template>
<style></style>
<script>
import UserStats from '../components/UserStats.vue'
import BlogTile from '../components/BlogTile.vue'
import AppNav from '../components/AppNav.vue'
import UnAuth from '../components/UnAuth.vue'
import IconLoading from '../components/icons/IconLoading.vue'
import error from '../components/error.vue'
export default {
  name: 'UserProfileView',
  components: {
    UserStats,
    BlogTile,
    AppNav,
    UnAuth,
    IconLoading,
    error
  },
  data() {
    return {
      unauth: true,
      loading: true,
      user_stats: '',
      error_text: null,
      user_posts: ''
    }
  },
  methods: {
    async getUserStats() {
      const path = 'http://127.0.0.1:5000/api/stats/' + this.$route.params.username
      const response = await fetch(path, {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
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
        this.user_stats = await response.json()
        this.error_text = ''
      }
    },
    async getUserPosts() {
      const path = 'http://127.0.0.1:5000/api/posts/' + this.$route.params.username
      const response = await fetch(path, {
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
        const error = await response.json()
        this.error_text = error.error_message
      } else {
        this.loading = false
        this.unauth = false
        this.user_posts = await response.json()
        this.error_text = ''
      }
    },
    async export() {
      const path = 'http://127.0.0.1:5000/export'
      let response = await fetch(path, {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (response.ok) {
        let res = await response.json()
        const a = document.createElement('a')
        a.href = 'http://127.0.0.1:5000' + res.download_link
        a.click()
        a.remove()
      }
    }
  },
  created() {
    this.getUserStats()
    this.getUserPosts()
  },
  watch: {
    $route() {
      this.getUserStats()
      this.getUserPosts()
    }
  }
}
</script>
