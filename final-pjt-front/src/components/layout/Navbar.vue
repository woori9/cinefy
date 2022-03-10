<template>
  <div>
    <b-navbar toggleable="lg" type="dark" class="fixed-top navbar-style">
      <b-navbar variant="faded" type="light">
        <b-navbar-brand href="/">
          <img src="@/assets/logo.png" alt="logo" width="160px;">
        </b-navbar-brand>
      </b-navbar>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item href="/community">Community</b-nav-item>
          <b-nav-item  v-if="isLoggedIn" @click="logout" href="#">Logout</b-nav-item>
          <b-nav-item v-if="isLoggedIn" href="/accounts/mypage">MyPage</b-nav-item>
          <b-nav-item v-if="!isLoggedIn" href="/accounts/login">Login</b-nav-item>
          <b-nav-item v-if="!isLoggedIn" href="/accounts/signup">Signup</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Header',
  methods: {
    logout: function () {
      localStorage.removeItem('token');
      this.$store.commit('LOGOUT');
      this.$router.push({ name: 'Login' });
    }
  },
  computed: {
    ...mapState([
      'isLoggedIn',
      'isModalVisible',
    ])
  }
}
</script>

<style scoped>
.navbar-style {
  background-color: rgba(15, 12, 29, 0.85);
  /* border-bottom: 0.1rem solid rgb(230, 230, 230); */
  -webkit-transition: all 0.6s ease-out;
  -moz-transition: all 0.6s ease-out;
  -o-transition: all 0.6s ease-out;
  -ms-transition: all 0.6s ease-out;
  transition: all 0.6s ease-out;
}
</style>