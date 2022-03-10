<template>
  <div class="modal-box">
    <div class="content">
      <div class="modal-body">
        <div v-if="modalMode === 'search'">
          <search-form :from="'reviewEdit'"></search-form>
        </div>
        <div v-else>
          <movie-detail></movie-detail>
        </div>
      </div>
      <div class="modal-footer">
        <b-button @click="closeModal" type="button" class="fixed-button" variant="secondary">Close</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import MovieDetail from '@/components/movie/MovieDetail';
import SearchForm from '@/components/utils/SearchForm';

export default {
  name: 'Modal',
  components: {
    MovieDetail,
    SearchForm,
  },
  methods: {
    closeModal() {
      this.$store.commit('HIDE_MODAL');
    },
  },
  computed: {
    ...mapState(['modalMode']),
  }
}
</script>

<style scoped>
.modal-box {
  display: flex;
  position: fixed;
  justify-content: center;
  align-items: flex-start;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  overflow: auto;
  z-index: 1; /* Sit on top */
  background-color: rgba(9, 13, 29,0.6); /* Black w/ opacity */
}

.content {
  background-color: rgb(9, 13, 29);
  border-radius: 15px;
  padding: 20px;
  border: 1px solid #888;
  width: 60%; /* Could be more or less, depending on screen size */
  margin-top: 8rem;
  margin-bottom: 0.5rem;
}
</style>