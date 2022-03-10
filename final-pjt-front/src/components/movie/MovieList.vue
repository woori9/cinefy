<template>
  <div class="swiper-div">
    <h2 class="category">{{ category }}</h2>
    <swiper class="swiper" :options="swiperOption">
      <swiper-slide class="slide-margin" v-for="movie in filteredMovies" :key="movie.id">
        <div class="slide" @click="openModal(movie)">
          <div class="image-box">
            <img :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="poster img" style="width: 200px; height: 300px;">
          </div>
          <p class="margin-y">{{ movie.title }}</p>
        </div>
      </swiper-slide>
      <div class="swiper-button-prev swiper-button" slot="button-prev"></div>
      <div class="swiper-button-next swiper-button" slot="button-next"></div>
    </swiper>
  </div>
</template>

<script>
  import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
  import 'swiper/css/swiper.css'

  export default {
    name: 'MovieList',
    components: {
      Swiper,
      SwiperSlide
    },
    data() {
      return {
        selectedMovie: null,
        swiperOption: {
          slidesPerGroup: 1,
          breakpoints: {
            620: {
              slidesPerView: 2
            },
            910: {
              slidesPerView: 3
            },
            1210: {
              slidesPerView: 4
            },
            1515: {
              slidesPerView: 5
            }
          },
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
          }
        }
      }
    },
    props: {
      movies: {
        type: Array
      },
      category: {
        type: String
      }
    },
    computed: {
      filteredMovies() {
        return this.movies.filter(movie => {
          return movie.poster_path
        })
      }
    },
    methods: {
      openModal(movie) {
        this.$store.dispatch('fetchBeforeOpenModal', movie)
      },
    }
  }
</script>

<style scoped>
.swiper-div {
  margin-bottom: 3rem;
}
.category {
  margin: 3rem 0 1.5rem 0;
  /* margin-left: 17%; */
  /* text-align: left; */
}
.swiper {
  width: 70%;
  justify-content: center;
}
.slide {
  cursor: pointer;
}
.margin-y {
  margin: 0.5rem 0;
}
img {
  border-radius: 5px;
}
.swiper-button {
  color: yellow;
}
.slide-margin {
  margin-top: 1rem;
}
.image-box {
  position: relative;
  top: 0;
  transition: top ease 0.3s;
}
.image-box:hover {
  top: -10px;
}
</style>