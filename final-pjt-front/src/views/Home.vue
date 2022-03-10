<template>
  <div class="home">
    <main-movies :mains="mains"></main-movies>
    <div v-if="data">
      <movie-list :movies="data.popular" :category="'요즘 핫한 영화'"></movie-list>
      <movie-list :movies="data.now_playing" :category="'현재 상영 중인 영화'"></movie-list>
      <movie-list :movies="data.top_rated" :category="'평점 높은 순'"></movie-list>
      <movie-list :movies="data.upcoming" :category="'Coming Soon'"></movie-list>
      <movie-list :movies="moviesByDate" :category="`${thisMonth}월에 개봉한 영화`"></movie-list>
      <movie-list :movies="data.with_cast.movies" :category="`${forYou} ${data.with_cast.name} 배우 모음전`"></movie-list>
      <movie-list :movies="data.with_crew.movies" :category="`${forYou} ${data.with_crew.name} 감독 모음전`"></movie-list>
      <movie-list :movies="data.with_genres.movies" :category="`이 장르는 어때요? ${data.with_genres.name}`"></movie-list>
    </div>
    <div v-else>
       <b-spinner variant="warning" label="Spinning"></b-spinner>
    </div>
    <button class="fixed-button btn btn-secondary" @click="topLink">TOP</button>
  </div>
</template>

<script>
import MovieList from '@/components/movie/MovieList';
import MainMovies from '@/components/movie/MainMovies';
import axios from '../api/server';

export default {
  name: 'Home',
  data() {
    return {
      data: null,
      mains: null,
      forYou: null,
    }
  },
  components: {
    MovieList,
    MainMovies,
  },
  computed: {
    moviesByDate() {
      return this.$store.state.moviesByDate
    },
    thisMonth() {
      return this.$store.state.thisMonth
    },
    username() {
      return this.$store.state.username
    }
  },
  methods: {
    topLink: function () {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      })
    },
  },
  async mounted() {
    if (this.username) {
      const { data } = await axios({
        method: 'get',
        url: '/movies/recommended/',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
      })
      this.data = data
      this.forYou = this.username + '님을 위한 '
    } else {
      const { data } = await axios({
        method: 'get',
        url: '/movies/recommended/',
      });
      this.data = data
      this.forYou = ''
    }
    this.mains = this.data.popular.slice(0, 10).filter(movie => {
      return movie.poster_path
    }).slice(0, 5)
  }
}
</script>

<style scoped>
.fixed-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
}
</style>
