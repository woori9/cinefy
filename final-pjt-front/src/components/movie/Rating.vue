<template>
  <div class="rating">
    <!-- 작성폼 -->
    <form class="rating-form mb-5" @submit="createRating">
      <star-form
        class="star-form mr-5"
        @rating-input="ratingChanged"
        :initialRank="'0'">
      </star-form>
      <div class="input-width input-box">
        <b-form-input
          class="input-height"
          type="text"
          v-model="content"
          placeholder="평점과 코멘트를 남겨주세요(50자 이내)"
          autocomplete="off">
        </b-form-input>
        <div class="overlay">
          <b-button
            @click="createRating"
            class="submit-btn no-border"
            type="submit"
            variant="warning">
            작성
          </b-button>
        </div>
      </div>
    </form>

    <!-- Rating 리스트 -->
    <div v-for="rating in ratingList" class="rating-list" :key="rating.id">

      <div class="star-update mb-3" v-if="targetRating && (targetRating.id === rating.id)">
        <star-form
          @target-rating-input="targetRatingChanged"
          :initialRank="`${targetRating.rank}`">
        </star-form>
        <div class="ml-5 update-input" >
          <b-form-input
            @keyup.enter="updateRating()"
            v-model="targetRating.content">
          </b-form-input>
        </div>
        <div>
          <b-button class="text-decoration-none" variant="link" @click="deSelectRating()">취소</b-button>
          <b-button class="text-decoration-none" variant="link" @click="updateRating()">제출</b-button>
        </div>
      </div>


    <div v-else class="rating-item mb-4">
      <div class="d-flex mt-1">
        <star :score="rating.rank"></star>
        <div>{{ rating.rank }}</div>
      </div>
      <div class="ml-5 mt-1 rating-username">{{ rating.username }}</div>
      <div class="rating-content mt-1">{{ rating.content }}</div>
        <div v-if="rating.user === userId">
          <b-button class="ml-1 text-decoration-none" @click="selectRating(rating)" variant="link">수정</b-button>
          <b-button class="text-decoration-none" @click="deleteRating(rating.id)" variant="link">삭제</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../api/server'
import { mapState } from 'vuex'
import Star from '@/components/utils/Star'
import StarForm from '@/components/utils/StarForm'


export default {
  name: 'Rating',
  components: {
    Star,
    StarForm
  },
  data() {
    return {
      ratingList: [],
      ratings: 0,
      content: '',
      targetRating: null,
    }
  },
  props: {
    movieId: {
      type: Number
    },
  },
  methods: {
    targetRatingChanged(value) { // event.target.value를 타고 옴으로 String
      this.targetRating.rank = value
    },
    ratingChanged(value) { // event.target.value를 타고 옴으로 String
      this.ratings = value
    },
    async createRating(event) {
      event.preventDefault()
      console.log('crate')
      if(!this.ratings || !this.content.trim()) {
        alert('평점을 기입해 주세요')
        return;
      }

      if (this.submittedRating) {
        alert('평점은 한 번만 등록 가능합니다.')
        this.content = ''
        return;
      }

      if (this.content.trim() && this.ratings) {
        try {
          const token = localStorage.getItem('token')
          const response = await axios({
            method: 'post',
            url: `/movies/${this.movieId}/rating/`,
            headers: { 'Authorization' : `Bearer ${token}` },
            data: {
              rank: this.ratings,
              content: this.content,
              userId: this.userId,
            }
          });
          const { data } = response
          this.ratingList = [ ...this.ratingList, data]
        } catch(err) {
          const { status } = err.response
          if (status === 401) {
            alert('로그인하고 이용해주세요.')
            this.$store.commit('HIDE_MODAL');
            this.$router.push({ name: 'Login' }).catch(()=>{})
          }
        }
        this.content = ''
      }
    },
    selectRating(rating) {
      this.targetRating = { ...rating }
    },
    deSelectRating() {
      this.targetRating = null
    },
    async updateRating() {
      const { rank, content } = this.targetRating
      if (content.trim()) {
        const token = localStorage.getItem('token')
        const response = await axios({
          method: 'put',
          url: `/movies/${this.movieId}/rating/${this.targetRating.id}/`,
          headers: { 'Authorization' : `Bearer ${token}` },
          data: {
            content,
            rank: Number(rank)
          }
        })
        const { data } = response
        this.ratingList = this.ratingList.map(rating => {
          if(rating.id === this.targetRating.id) {
            return {
              ...rating,
              content: data.content,
              rank: data.rank
            }
          }
          return rating
        })

        this.targetRating = null
      }
    },
    async deleteRating(ratingId) {
      const token = localStorage.getItem('token')
      const response = await axios({
        method: 'delete',
        url: `/movies/${this.movieId}/rating/${ratingId}/`,
        headers: { 'Authorization' : `Bearer ${token}` },
      })

      if (response.status === 204) {
        this.ratingList = this.ratingList.filter(rating => rating.id !== ratingId)
      }
    }
  },
  computed: {
    ...mapState(['userId']),
    submittedRating() {
      return this.ratingList.find(rating => rating.user === this.userId)
    },
  },
  mounted() {
    const getRatings = async() => {
      const response = await axios({
        method: 'get',
        url: `/movies/${this.movieId}/rating/`
      })

      const { data } = response
      this.ratingList = data
    }
    getRatings()
  }
}
</script>

<style scoped>
p {
  font-size: 14px;
  margin: 0.5rem 0;
}
.update-input {
  width: 65%;
}
.no_border {
  border-radius: 0px;
}
.up_border {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
.bottom_border {
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
.input-box {
  background-color: white;
  border-radius: 4px;
}
.overlay {
  background-color: #ffffffbc;
  position: relative;
  text-align: right;
}
.rating {
  margin: 0 1rem;
}
.rating-form {
  display: flex;
  align-items: center;
  margin: 1rem 0;
}
.submit-btn {
  width: 5rem;
}
.input-width {
  width: 84%;
}
.input-height {
  height: 4rem;
}
.star-update {
  display: flex;
}
.rating-list {
  /* display: flex; */
  /* justify-content: flex-start; */
  /* margin-left: 12rem; */
  color: rgb(230, 230, 230);
}
.rating-item {
  display: flex;
}
.rating-content {
  text-align: left;
  word-wrap: anywhere;
  max-width: 26rem;
}
.content-form > input {
  width: 300px;
  height: 30px;
  font-size: 20px;
}
.parent {
  position: relative;
}
.rating-username {
  padding-right: 0.9rem;
}
.update-delete {
  position: absolute;
  left: 4rem;
  /* bottom: 0.6rem; */
  /* margin: 0.5rem */
}
</style>
