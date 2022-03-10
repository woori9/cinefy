<template>
  <b-container>
    <b-row class="justify-content-md-center my-4">
      <b-form-input
        class="search-input"
        v-model="keyword"
        placeholder="검색어를 입력해주세요"
        @input="debounceSearch(keyword)"
        autocomplete="off"
      >
      </b-form-input>
      <b-button variant="warning" @click="debounceSearch(keyword)">
        <font-awesome-icon :icon="['fas', 'search']" />
      </b-button>
    </b-row>

    <div v-if="from === 'reviewEdit'">
      <movie-cards :movies="movieWithPoster"></movie-cards>
    </div>
    <div v-if="from === 'sidebar'">
      <movie-ost :movies="searchedMovies"></movie-ost>
    </div>

  </b-container>
</template>

<script>
import axios from '../../api/movie';
import _ from 'lodash';
import MovieCards from '@/components/movie/MovieCards';
import MovieOst from '@/components/movie/MovieOst';


export default {
  name: 'SearchForm',
  components: {
    MovieCards,
    MovieOst
  },
  props: {
    from: {
      type: String
    }
  },
  data: function () {
    return {
      keyword: '',
      searchedMovies: [],
      selectedMovie: ''
    };
  },
  methods: {
    debounceSearch: _.debounce(async function(keyword) {
      if (keyword.trim()) {
        const encodedKeyword = encodeURI(keyword);
        const response = await axios({
          method: 'get',
          url: '/search/movie?',
          params: {
            query: encodedKeyword,
            language: 'ko-KR'
          }
        });
        const { results } = response.data;
        this.searchedMovies = results;
      } else {
        this.searchedMovies = []
      }
    }, 500),
  },
  computed: {
    movieWithPoster() {
      return this.searchedMovies.filter(movie => movie.poster_path);
    }
  }
}
</script>

<style scoped>
.search-input {
  padding: 10px;
  width: 81%;
  height: 50px;
}
</style>