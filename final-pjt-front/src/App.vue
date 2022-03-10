<template>
  <div id="app">
    <navbar></navbar>
    <router-view class="padding-top"/>
    <modal v-if="isModalVisible"></modal>
    <mini-modal v-if="isMiniModalVisible"></mini-modal>
    <sidebar></sidebar>
    <cinefy-footer></cinefy-footer>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Modal from '@/components/layout/Modal'
import Navbar from '@/components/layout/Navbar'
import MiniModal from '@/components/layout/MiniModal'
import Sidebar from '@/components/layout/Sidebar'
import CinefyFooter from '@/components/layout/Footer'


export default {
  name: 'App',
  components: {
    Modal,
    Navbar,
    MiniModal,
    Sidebar,
    CinefyFooter,
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const { username, user_id } = JSON.parse(atob(token.split('.')[1]));
      this.$store.commit('LOGIN', { username, user_id });
    }
    this.$store.dispatch('getMoviesByDate');
  },
  computed: {
    ...mapState([
      'isModalVisible',
      'isMiniModalVisible'
    ])
  }
}
</script>

<style >
.padding-top {
  padding-top: 103px;
}
#app {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 17px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(230, 230, 230);
}
</style>
