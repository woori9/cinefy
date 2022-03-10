<template>
  <div>
    <player :video-id="getVideoID" :modaltype="'default'"></player>
    <div v-if="selectedMovie">
      <div class="movie-info">
        <div class="margin-y">
          <h3 class="left-0">{{ selectedMovie.title }}</h3>
          <p class="left-0">출연: <span v-for="actor in actors" :key="actor.id">{{ actor }}</span></p>
          <p class="left-0">감독: {{ selectedMovie.director }}</p>
          <div class="star">
            <star :score="selectedMovie.vote_average"></star>
            <span>{{ selectedMovie.vote_average }}</span>
          </div>
        </div>
      </div>
      <p class="margin-y left-0">{{ selectedMovie.overview }}</p>
    </div>
    <br>
    <div v-if="isRatingVisible">
      <rating :movieId="selectedMovie.id"></rating>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Rating from '@/components/movie/Rating'
import Star from '@/components/utils/Star'
import Player from '@/components/utils/Player'

export default {
  name: 'MovieDetail',
  components: {
    Rating,
    Star,
    Player
  },
  computed: {
    ...mapState([
      'selectedMovie'
    ]),
    actors() {
      return this.selectedMovie.actors.map((actor, index) => {
        if (index !== this.selectedMovie.actors.length - 1) {
          return actor + ', '
        } else {
          return actor
        }
      })
    },
    getVideoID() {
      const { videoId } = this.selectedMovie.trailer.id //'c2rgrqEFVKc' 임시 아이디
      return videoId
    },
    isRatingVisible() {
      if (this.selectedMovie.category.includes('with')) {
        return false
      }
      return true
    }
  }
}
</script>

<style scoped>
.movie-info {
  display: flex;
}
.star {
  display: flex;
  align-items: center;
  /* margin: 0 4rem; */
}
.margin-y {
  margin: 1rem 1rem;
}
.left-0 {
  text-align: left;
  margin-bottom: 0.5rem;
}
</style>