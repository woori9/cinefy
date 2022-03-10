<template>
  <div class="container">
    <div class="profile margin-bottom">
      <img src="@/assets/blank-profile-picture.png" class="profile-img" alt="profile img" style="width: 120px; height: 120px;">
      <h3 class="my-username">{{ username }}님 안녕하세요.</h3>
    </div>
    <div class="margin-bottom">
      <h3>내가 쓴 글</h3>
      <div>
        <b-table :items="myReviews" class="table-text" @row-clicked="reviewLink"></b-table>
      </div>
    </div>
    <div class="margin-bottom">
      <h3>내가 본 영화</h3>
      <div class="movies-div">
        <div class="my-movies">
          <div v-for="rating in myRatings" class="my-movie" :key="rating.id">
            <div @click="openModal(rating.movie)">
              <img :src="`https://image.tmdb.org/t/p/original/${rating.movie.poster_path}`" alt="poster img" style="width: 180px; height: 270px;">
              <p class="margin-y">{{ rating.movie.title }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../api/server'

export default {
  name: 'MyPage',
  data() {
    return {
      myRatings: null,
    }
  },
  computed: {
    username() {
      return this.$store.state.username
    },
    myReviews() {
      return this.$store.state.reviews.filter(review => {
         return review['작성자'] === this.username
      }).map(review => {
        return {
            'NO': review['NO'],
            '영화 제목': review['영화 제목'],
            '제목': review['제목'],
            '작성일': review['작성일'],
            '좋아요': review['좋아요']
          }
      })
    }
  },
  methods: {
    reviewLink: function (review) {
      this.$router.push({ name: 'ReviewDetail', params: { reviewId: review['NO'] }})
    },
    openModal(movie) {
      this.$store.dispatch('fetchBeforeOpenModal', movie)
    },
  },
  async created() {
    this.$store.dispatch('getReviews')
    const token = localStorage.getItem('token')
    const response = await axios({
      method: 'get',
      url: '/movies/my-rating/',
      headers: { 'Authorization' : `Bearer ${token}` }
    })
    const { data } = response
    this.myRatings = data
  }
}
</script>

<style scoped>
.container {
  margin-top: 20px;
}
.margin-bottom {
  margin-bottom: 8rem;
}
h3 {
  margin: 3rem 0 1rem 0;
}
.profile {
  display: flex;
}
img {
  border-radius: 5px;
}
.my-username {
  margin-top: 10px;
  margin-left: 20px;
}
.table-text {
  color: rgb(230, 230, 230);
  cursor: pointer;
}
.my-movies {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.my-movie {
  margin: 0 1rem 2rem 1rem;
  cursor: pointer;
}
.margin-y {
  margin: 0.5rem 0;
}
</style>