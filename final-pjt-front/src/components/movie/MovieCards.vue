<template>
  <div>
    <div class="searched-movies" v-if="hasResult">
      <div v-for="movie in movies" :key="movie.id">
        <div class="movie-item" @click="selectMovie(movie.title)">
          <img class="movie-img" :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`" alt="poster img" style="width: 190px;">
          <p>{{ movie.title }}</p>
        </div>
        <!-- <b-card
          :title ="movie.title"
          :img-src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :img-alt="movie.title"
          @click="selectMovie(movie.title)"
          img-top
          tag="article"
          style="max-width: 18rem;"
          class="mx-3 my-3"
        >
        </b-card> -->
      </div>
    </div>
    <div v-else>
      <p>검색 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieCards',
  props: {
    movies: {
      type: Array
    }
  },
  methods: {
    selectMovie(movieTitle) {
      this.$store.commit('SELECT_MOVIE_TITLE', movieTitle);
    }
  },
  computed: {
    hasResult() {
      return this.movies.length
    }
  }
}
</script>

<style scoped>
* {
  color: rgb(230, 230, 230);
}
.movie-item {
  display: flex;
  flex-direction: column;
  margin: 1rem;
  cursor: pointer;
}
.movie-img {
  border-radius: 10px;
}
.searched-movies {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  color: rgb(61, 55, 55);
}
</style>
