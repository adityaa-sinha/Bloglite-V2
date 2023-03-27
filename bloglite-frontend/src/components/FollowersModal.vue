<template>
  <div
    class="modal fade"
    id="followersModal"
    tabindex="-1"
    aria-labelledby="followersModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="followersModalLabel">{{ username }}'s followers</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body mx-3">
          <div v-if="this.followers_list" v-for="user in this.followers_list">
            <div class="row mb-3">
              <div class="col">
                <router-link :to="'/profile/' + user.username">
                  <img
                    v-if="user.dp_url"
                    class="dp"
                    :src="'http://127.0.0.1:5000' + user.dp_url"
                    alt="dp"
                    data-bs-dismiss="modal"
                  />
                  <icon-dp v-else class="dp" data-bs-dismiss="modal"></icon-dp>
                </router-link>
                <router-link :to="'/profile/' + user.username" class="mx-3 user-link"
                  ><span data-bs-dismiss="modal">{{ user.username }}</span></router-link
                >
              </div>
            </div>
            <hr />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import IconDp from './icons/IconDp.vue'
export default {
  name: 'FollowersModal',
  props: ['username'],
  data() {
    return {
      followers_list: ''
    }
  },
  components: {
    IconDp
  },
  methods: {
    async getFollowers() {
      const path = 'http://127.0.0.1:5000/api/followers/' + this.username
      let response = await fetch(path, {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        }
      })
      if (response.ok) {
        this.followers_list = await response.json()
      }
    }
  },
  created() {
    this.getFollowers()
  },
  watch: {
    username: function () {
      this.getFollowers()
    }
  }
}
</script>
<style scoped>
.dp {
  height: 70px;
  width: 70px;
  border-radius: 50%;
  object-fit: cover;
  object-position: top;
}
.user-link {
  text-decoration: none;
}
</style>
