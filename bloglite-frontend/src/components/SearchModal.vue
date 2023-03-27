<template>
  <div
    class="modal fade"
    id="search"
    tabindex="-1"
    aria-labelledby="searchModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <div class="input-group">
            <div class="input-group-text"><i class="bi bi-search"></i></div>
            <input
              type="text"
              class="form-control modal-title"
              id="searchModalLabel"
              placeholder="Type username to search"
              v-model="query"
              @input="this.search"
            />
          </div>
          <button
            type="button"
            class="btn-close m-1"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body mx-3">
          <div v-if="this.query" v-for="user in this.search_results">
            <div class="row mb-3">
              <div class="col">
                <router-link :to="'/profile/' + user.username">
                  <img v-if="user.dp_url"
                    class="dp"
                    :src="'http://127.0.0.1:5000'+user.dp_url"
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
          <div v-else></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import IconDp from './icons/IconDp.vue'
export default {
  name: 'SearchModal',
  data() {
    return {
      query: '',
      search_results: ''
    }
  },
  components:{
    IconDp
  },
  methods: {
    async search() {
      const body = {
        username: this.query
      }
      const path = 'http://127.0.0.1:5000/api/search'
      const response = await fetch(path, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('auth')
        },
        body: JSON.stringify(body)
      })
      if (response.ok) {
        this.search_results = await response.json()
      }
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
