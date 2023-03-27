<template>
  <div class="col-lg-4 col-md-6 col-sm-12">
    <div class="card rounded-0 mb-5 shadow-sm">
      <img :src="image_url" alt="Blog Image" class="img-fluid blog-img" />
      <div class="card-body">
        <div class="card-title">
          <h2>
            {{ title }}
            <!-- If blog owner, show edit/delete dropdown -->
            <button
              v-if="this.owner"
              type="button"
              class="btn btn-sm btn-light dropdown-toggle float-end"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            ></button>
            <ul class="dropdown-menu">
              <li><router-link :to="'/posts/edit/'+this.post_id" class="dropdown-item">Edit</router-link></li>
              <li>
                <button class="dropdown-item" @click="this.deleteblog"
                  >Delete</button
                >
              </li>
            </ul>
          </h2>
        </div>
        <div class="card-text" v-if="caption_preview != null">
          <p>{{ caption_preview.substring(0, 150) + '...' }}</p>
          <router-link :to="'/posts/' + post_id" class="read-more float-end">
            Read More <i class="bi bi-caret-right-fill"></i
          ></router-link>
        </div>

        <div class="card-text" v-else>
          <p>{{ caption_preview }}</p>
        </div>
      </div>
      <footer class="blockquote-footer m-2 text-end">
        by
        <router-link :to="'/profile/' + this.posted_by" style="text-decoration: none">{{
          posted_by
        }}</router-link>
        on {{ timestamp.substring(0, timestamp.length - 9) }}
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BlogTile',
  props: ['timestamp', 'posted_by', 'title', 'image_url', 'caption_preview', 'post_id', 'owner'],
  methods: {
    async deleteblog() {
      const path = 'http://127.0.0.1:5000/api/blog/' + this.post_id
      let response = await fetch(path, {
        method: 'delete',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (response.ok) {
        this.$router.go()
      }
    }
  }
}
</script>

<style scoped>
.blog-img {
  height: 280px;
  object-fit: cover;
}
.card-text {
  height: 78px;
}
.read-more {
  text-decoration: none;
}
</style>
