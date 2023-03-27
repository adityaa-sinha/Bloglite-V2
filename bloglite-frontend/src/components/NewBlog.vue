<template>
  <div class="container" style="margin-top: 8rem">
    <h2 class="text-center" style="margin-bottom: 4rem">
      New Blog Details
      <hr />
    </h2>
    <form @submit.prevent="this.postBlog">
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
      <div class="row mb-4">
        <div class="col-sm-6">
          <label for="image" class="col-form-label">Upload image:</label>
        </div>
        <div class="col-sm-6">
          <input
            type="file"
            @change="this.selectFile"
            id="image"
            class="form-control"
            accept="image/png, image/jpeg, image/jpg"
            required
          />
          <span v-if="this.uploading" class="spinner-grow text-light" role="status"> </span>
          <span v-else @click="this.uploadimage" class="btn btn-light mt-2">Upload</span>
          <p class="text-success" v-if="this.uploadsuccess">Upload successful!</p>
        </div>
      </div>
      <div class="row text-center" style="margin-top: 6rem">
        <div class="col">
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  name: 'NewBlog',
  props: ['username'],
  data() {
    return {
      title: null,
      caption: null,
      file: null,
      image_url: null,
      uploading: false,
      uploadsuccess: false
    }
  },
  methods: {
    selectFile(event) {
      this.file = event.target.files[0]
      this.uploadsuccess = false
      this.uploading = false
      if (this.file.size > 4 * 1000 * 1000) {
        alert('Please select a file with size less than 4MB')
      }
      // console.log(this.file)
    },
    async uploadimage() {
      this.uploading = true
      const fd = new FormData()
      fd.append('file', this.file, this.file.name)
      const path = 'http://127.0.0.1:5000/upload-blog-image'
      let response = await fetch(path, {
        method: 'post',
        headers: {
          'Authentication-Token': localStorage.getItem('auth')
        },
        body: fd
      })
      if (response.ok) {
        this.uploading = false
        this.uploadsuccess = true
        const res = await response.json()
        this.image_url = res.link
      }
    },
    async postBlog() {
      if (!this.image_url) {
        alert('Please click the upload button first.')
      } else {
        const body = {
          title: this.title,
          caption: this.caption,
          image_url: this.image_url
        }
        const path = 'http://127.0.0.1:5000/api/blog'
        let response = await fetch(path, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth')
          },
          body: JSON.stringify(body)
        })
        if (response.ok) {
          this.$router.push('/profile/' + this.username)
        }
      }
    }
  }
}
</script>
