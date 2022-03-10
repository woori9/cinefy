<template>
  <div class="movie-ost">
    <div v-for="movie in movies" :key="movie.id" @click="pickMovie(movie.original_title)">
      <div class="d-flex m-2 align-items-center">
        <div v-if="movie.poster_path">
          <img class="ost-image" :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`">
        </div>
        <div v-else>
          <img class="ost-image" src="@/assets/album.png"/>
        </div>

        <div class="ml-3">
          <div>{{ movie.title }}</div>
          <div class="text-muted">{{ movie.release_date }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieOst',
  props: {
    movies: {
      type: Array
    }
  },
  methods: {
    pickMovie(originalTitle) {
      this.$store.dispatch('getOST', originalTitle);
    },
  }
}
</script>

<style scoped>

.ost-image {
  height: 70px;
  width: 70px;
}
.text-muted {
  text-align: left;
}
</style>