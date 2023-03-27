<template>
  <div class="container" style="margin-top: 10rem">
    <div class="row justify-content-center">
      <div class="col-lg-4 col-md-6 col-sm-12">
        <!-- If dp available -->
        <img v-if="dp_url" class="dp" :src="dp_url" alt="Profile Picture" />
        <!-- Else dp icon -->
        <icon-dp v-else></icon-dp>
        <!-- DP Upload, if current user -->
        <label v-if="ownprofile" class="dp_upload_label btn btn-light" for="dp_upload"
          ><icon-camera></icon-camera
        ></label>
        <input
          v-if="ownprofile"
          type="file"
          style="display: none"
          name="file"
          id="dp_upload"
          @change="this.upload_dp"
          accept="image/png, image/jpeg, image/jpg"
        />
        <!-- Handling errors like wrong file type -->
        <p class="text-warning" v-if="ownprofile && error_msg">{{ error_msg.message }}</p>
      </div>
      <div class="col-lg-4 col-md-6 col-sm-12">
        <div class="row">
          <h2 class="mt-5">{{ username }}</h2>
          <div v-if="!ownprofile">
            <div v-if="following">
              <button v-if="!progress" class="btn btn-outline-light" @click="this.unfollowuser">
                Unfollow
              </button>
              <div v-else class="spinner-grow text-light" role="status"></div>
            </div>
            <div v-else>
              <button v-if="!progress" class="btn btn-light" @click="this.followuser">
                Follow
              </button>
              <div v-else class="spinner-grow text-light" role="status"></div>
            </div>
          </div>
        </div>
        <div class="row mt-4">
          <button class="btn btn-outline-light modals">
            {{ posts_count }} <br />
            Posts
          </button>
          <button
            class="btn btn-outline-light modals"
            data-bs-toggle="modal"
            data-bs-target="#followersModal"
          >
            {{ followers_count }} <br />
            Followers
          </button>
          <button
            class="btn btn-outline-light modals"
            data-bs-toggle="modal"
            data-bs-target="#followingModal"
          >
            {{ following_count }} <br />
            Following
          </button>
        </div>
      </div>
    </div>
  </div>
  <following-modal :username="this.username"></following-modal>
  <followers-modal :username="this.username"></followers-modal>
</template>
<style scoped>
.dp {
  border-radius: 50%;
  object-fit: cover;
  object-position: top;
  height: 200px;
  width: 200px;
}

.modals {
  width: 33%;
  border: none;
  text-align: start;
}
.dp_upload_label {
  position: absolute;
  margin-top: 150px;
}
</style>
<script>
import IconDp from './icons/IconDp.vue'
import IconCamera from './icons/IconCamera.vue'
import FollowingModal from './FollowingModal.vue'
import FollowersModal from './FollowersModal.vue'
export default {
  name: 'UserStats',
  data() {
    return {
      error_msg: '',
      progress: false
    }
  },
  props: [
    'username',
    'dp_url',
    'ownprofile',
    'following',
    'posts_count',
    'followers_count',
    'following_count'
  ],
  components: {
    IconDp,
    IconCamera,
    FollowingModal,
    FollowersModal
  },
  methods: {
    async upload_dp(event) {
      if (event.target.files[0].size > 4 * 1000 * 1000) {
        alert('File size should be less than 4MB')
      } else {
        const fd = new FormData()
        fd.append('file', event.target.files[0], event.target.files[0].name)
        const path = 'http://127.0.0.1:5000/upload-dp'
        let response = await fetch(path, {
          method: 'post',
          headers: {
            'Authentication-Token': localStorage.getItem('auth')
          },
          body: fd
        })
        if (response.ok) {
          this.$router.go()
        } else {
          this.error_msg = await response.json()
        }
      }
    },
    async followuser() {
      this.progress = true
      const path = 'http://127.0.0.1:5000/api/follow'
      const body = {
        target_username: this.$route.params.username
      }
      let response = await fetch(path, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        },
        body: JSON.stringify(body)
      })
      if (response.ok) {
        this.progress = false
        this.$router.go()
      }
    },
    async unfollowuser() {
      this.progress = true
      const path = 'http://127.0.0.1:5000/api/unfollow'
      const body = {
        target_username: this.$route.params.username
      }
      let response = await fetch(path, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        },
        body: JSON.stringify(body)
      })
      if (response.ok) {
        this.progress = false
        this.$router.go()
      }
    }
  }
}
</script>
