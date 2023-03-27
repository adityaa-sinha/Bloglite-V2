<template>
  <div class="container" style="margin-top: 6rem">
    <div class="row">
      <div class="col-lg-6">
        <img
          :src="'http://127.0.0.1:5000' + this.image_url"
          class="img-fluid mb-4"
          alt="Blog Image"
        />
      </div>
      <div class="col-lg-6">
        <div class="row">
          <span class="col-sm"
            ><i class="bi bi-pen-fill me-2"></i
            ><router-link class="text-decoration-none" :to="'/profile/' + this.posted_by">{{
              posted_by
            }}</router-link>
          </span>
          <!-- when v-if was not given it was reading .substring property of undefined, which was causing problems -->
          <span v-if="timestamp" class="col-sm" style="text-align: end">{{
            timestamp.substring(0, timestamp.length - 9)
          }}</span>
          <hr />
        </div>
        <div class="row">
          <h2>{{ title }}</h2>
        </div>
        <div class="row">
          <p class="text-justify">
            {{ caption }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Blog',
  props: ['title', 'caption', 'image_url', 'timestamp', 'posted_by']
}
</script>
