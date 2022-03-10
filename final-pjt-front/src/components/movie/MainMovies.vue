<template>
  <div>
    <swiper class="swiper" :options="swiperOption">
      <swiper-slide v-for="main_movie in mains" :key="main_movie.id">
        <div
          class="image-overlay"
          :style="{ backgroundImage: 'url(' + `https://image.tmdb.org/t/p/original/${main_movie.backdrop_path}` + ')' }"
        >
        </div>
        <img :src="`https://image.tmdb.org/t/p/original/${main_movie.backdrop_path}`" alt="backdrop img" width="60%">
        <div :class="{ displayNone: removeText }">
          <h1 class="title">{{ main_movie.title }}</h1>
          <p class="truncate-overflow">{{ main_movie.overview }}</p>
        </div>
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
      <!-- <div class="image-overlay-gradient"></div> -->
    </swiper>
  </div>
</template>

<script>
  import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
  import 'swiper/css/swiper.css'

  export default {
    name: 'MainMovies',
    components: {
      Swiper,
      SwiperSlide
    },
    props: {
      mains: {
        type: Array
      }
    },
    data() {
      return {
        removeText: false,
        swiperOption: {
          slidesPerView: 1,
          spaceBetween: 30,
          loop: true,
          autoplay: {
            delay: 5000
          },
          pagination: {
            el: '.swiper-pagination',
            clickable: true
          },
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
          }
        }
      }
    },
    methods: {
      onResize: function () {
        if (window.innerWidth < 1220) {
          this.removeText = true
        } else {
          this.removeText = false
        }
      }
    },
    created() {
      window.addEventListener("resize", this.onResize)
    },
    destroyed() {
      window.removeEventListener("resize", this.onResize)
    }
  }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gothic+A1&display=swap');
*{
  font-family: 'Gothic A1', sans-serif;
}
.image-overlay {
  width: 100%;
  height: 100%;
  position: absolute;
  /* background-color: #f85752; */
  opacity: 0.5;
  z-index: -1;
  background-repeat: no-repeat;
  background-size: cover;
  filter: blur(8px);
  -webkit-filter: blur(8px);
}
/* .image-overlay-gradient {
  position: absolute;
  background-color: #f85752;
  width: 100%;
  height: 50px;
} */
.displayNone {
  display: none;
}
.title {
  position: absolute;
  bottom: 10rem;
  left: 28rem;
  color: white;
  font-weight: bold;
  background: rgba(56, 56, 56, 0.3)
}
.truncate-overflow {
  position: absolute;
  bottom: 3em;
  left: 28rem;
  color: white;
  background: rgba(56, 56, 56, 0.3);
  text-align: left;
  max-width: 30em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
.swiper-button {
  color: yellow;
}
</style>