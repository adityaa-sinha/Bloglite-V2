import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import FeedView from '../views/FeedView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import CreateBlogView from '../views/CreateBlogView.vue'
import PostView from '../views/PostView.vue'
import EditBlogView from '../views/EditBlogView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/profile/:username',
      name: 'profile',
      component: UserProfileView
    },
    {
      path: '/create-blog',
      name: 'createblog',
      component: CreateBlogView
    },
    {
      path: '/posts/:id(\\d+)',
      name: 'post',
      component: PostView
    },
    {
      path: '/posts/edit/:id(\\d+)',
      name: 'editblog',
      component: EditBlogView
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notfound',
      component: NotFoundView
    }
  ]
})

export default router
