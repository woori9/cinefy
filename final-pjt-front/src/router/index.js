import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Community from '@/views/Community.vue'
import ReviewDetail from '@/views/ReviewDetail.vue'
import ReviewEdit from '@/views/ReviewEdit.vue'
import Signup from '@/views/Signup.vue'
import Login from '@/views/Login.vue'
import MyPage from '@/views/MyPage.vue'
import store from '@/store'
import NotFound from '@/components/utils/404.vue'


Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/community',
    name: 'Community',
    component: Community,
  },
  {
    path: '/community/editor',
    name: 'ReviewEdit',
    component: ReviewEdit,
    props: true,
  },
  {
    path: '/community/:reviewId',
    name: 'ReviewDetail',
    component: ReviewDetail,
    props: true,
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/mypage',
    name: 'MyPage',
    component: MyPage,
  },
  {
    path: '/*',
    component: NotFound
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.name === 'Login' || to.name === 'Signup') {
    if (token) {
      next({ name: 'Home' });
    }
  }

  if (!(to.name === 'Community' || to.name === 'ReviewDetail' || to.name === 'ReviewEdit')) {
    store.commit('HIDE_MINI_MODAL')
    next()
  }

  next();
});

export default router;
