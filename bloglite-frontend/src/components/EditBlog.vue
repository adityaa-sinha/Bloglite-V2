<template>
  <div v-if="!error_text">
    <div class="container" style="margin-top: 8rem">
      <h2 class="text-center" style="margin-bottom: 4rem">
        Edit Blog
        <hr />
      </h2>
      <form @submit.prevent="this.editBlog">
        <div class="row mb-4">
          <div class="col-sm-6">
            <label for="title" class="col-form-label">Title:</label>
          </div>
          <div class="col-sm-6">
            <input type="text" v-model="title" id="title" class="form-control" required />
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-sm-6">
            <label for="caption" class="col-form-label">Caption/Description:</label>
          </div>
          <div class="col-sm-6">
            <textarea
              type="text"
              v-model="caption"
              id="caption"
              class="form-control"
              rows="3"
              required
            />
          </div>
        </div>

        <div class="row text-center" style="margin-top: 6rem">
          <div class="col">
            <button type="submit" class="btn btn-success">Submit</button>
            <div v-if="this.error_edit">
              <span class="text-danger">{{ error_edit.error_message }}</span>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
  <div v-else>
    <error :msg="this.error_text.error_message" style="margin-top: 6rem"></error>
  </div>
</template>
<script>
import error from './error.vue'
export default {
  name: 'EditBlog',
  props: ['username', 'post_id'],
  components: {
    error
  },
  data() {
    return {
      title: null,
      caption: null,
      error_text: null,
      error_edit: null
    }
  },
  methods: {
    async editBlog() {
      const body = {
        title: this.title,
        caption: this.caption
      }
      const path = 'http://127.0.0.1:5000/api/blog/' + this.post_id
      //   console.log(path)
      let response = await fetch(path, {
        method: 'put',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        },
        body: JSON.stringify(body)
      })
      if (response.ok) {
        this.$router.push('/profile/' + this.username)
      } else {
        this.error_edit = await response.json()
      }
    },
    async getBlogDetails() {
      const path = 'http://127.0.0.1:5000/api/blog/' + this.post_id
      let response = await fetch(path, {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (response.ok) {
        const blogdetails = await response.json()
        this.title = blogdetails.title
        this.caption = blogdetails.caption
      } else {
        this.error_text = await response.json()
      }
    }
  },
  created() {
    this.getBlogDetails()
  }
}
</script>
