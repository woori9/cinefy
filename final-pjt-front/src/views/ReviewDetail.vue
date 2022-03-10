<template>
  <div class="review container" v-if="isLoggedIn">
    <!-- <h1>Review Detail</h1> -->
    <div class="review-header">
      <h2>영화 리뷰</h2>
      <b-button
        class="back-button"
        variant="link"
        @click="communityLink"
      >목록으로
      </b-button>
    </div>
    <div v-if="review" class="review-detail">
      <div class="title-div">
        <h1 class="review-title">{{ review.title }}</h1>
        <span class="update-delete" v-if="review.username === $store.state.username">
          <b-dropdown id="dropdown-right" dropright toggle-class="m-2" no-caret>
            <template slot="button-content">
              <font-awesome-icon :icon="['fas', 'ellipsis-v']" />
            </template>
            <b-dropdown-item @click="editLink(review.movie_title)">
              수정
              <font-awesome-icon :icon="['fas', 'edit']" />
            </b-dropdown-item>
            <b-dropdown-item @click="deleteReview">
              삭제
              <font-awesome-icon :icon="['fas', 'trash-alt']" />
            </b-dropdown-item>
          </b-dropdown>
        </span>
      </div>

      <div class="review-info">
        <p>
          <font-awesome-icon :icon="['fas', 'tag']" />
          {{ review.movie_title }}
        </p>
        <p>
          <span class="margin-right">{{ review.username }}</span>
          <span class="margin-right text-gray">작성 | {{ createdAt }}</span> 
          <span class="margin-right text-gray">수정 | {{ updatedAt }}</span> 
        </p>
      </div>
      
      <div class="review-content">{{ review.content }}</div>
      
      <div class="like">
        <b-button @click="like" pill variant="outline-warning" class="margin-y">
          
          <span v-if="isLiked">
            <span>좋아요 취소</span>
            <font-awesome-icon :icon="['fas', 'heart']"  class="like-cnt-margin" />
            <span>{{ likeCnt }}</span>
          </span>
          <span v-else>
            <span>좋아요</span>
            <font-awesome-icon :icon="['far', 'heart']" class="like-cnt-margin" />
            <span>{{ likeCnt }}</span>
          </span>
        </b-button>
      </div>
    </div>
    <Comments :review="review" class="comments"/>
  </div>
</template>

<script>
import axiosServer from '../api/server';
import Comments from '@/components/community/Comments.vue'
import fromNow from '../utils/dayjs'

export default {
  name: 'ReviewDetail',
  components: {
    Comments
  },
  data() {
    return {
      review: null,
      isLiked: false,
      likeCnt: 0,
    }
  },
  computed: {
    userId() {
      return this.$store.state.userId
    },
    isLoggedIn() {
      return this.$store.state.isLoggedIn
    },
    createdAt() {
      return fromNow(this.review.created_at)
    },
    updatedAt() {
      return fromNow(this.review.updated_at)
    }
  },
  methods: {
    communityLink: function () {
      this.$router.push({ name: 'Community' })
    },
    editLink: function (movieTitle) {
      this.$store.commit('SELECT_MOVIE_TITLE', movieTitle); //추가!!
      this.$router.push({ name: 'ReviewEdit', params: { review: this.review } })
    },
    deleteReview: function () {
      this.$store.dispatch('deleteReview', this.review)
    },
    like: async function () {
      const { data } = await axiosServer({
        method: 'post',
        url: `community/${this.review.id}/like/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      this.isLiked = data.isLiked
      this.likeCnt = data.likeCnt
    }
  },
  created() {
    const reviewId = this.$route.params.reviewId
    const getReview = async(id) => {
      const token = localStorage.getItem('token');
      const { data } = await axiosServer({
        method: 'get',
        url: `/community/${id}`,
        headers: { 'Authorization' : `Bearer ${token}` }
      });
      this.review = data;
      this.likeCnt = data.like_count
      this.isLiked = data.like_users.indexOf(this.userId) > -1 ? true : false
      this.$store.commit('GET_COMMENTS', this.review)
      return;
    }
    getReview(reviewId);
  },
}
</script>

<style scoped>
.review {
  padding: 107px 3rem;
}
.back-button {
  padding: 0;
}
.review-header {
  display: flex;
  justify-content: space-between;
  text-align: left;
  margin-bottom: 2rem;
}
.title-div {
  display: flex;
  justify-content: space-between;
  margin: 1.5rem 0;
}
.review-detail {
  border-top: 1px solid rgb(255, 255, 248);
}
.review-info {
  margin-bottom: 1.5rem;
  text-align: left;
}
.review-content {
  font-size: 20px;
  text-align: left;
  font-weight: 300;
  white-space: pre-line;
}
.like {
  display: flex;
  justify-content: center;
  align-items: center;
}
.margin-y {
  margin: 2rem 0 2rem 1rem;
}
.margin-right {
  margin-right: 1.5rem;
}
.like-cnt-margin {
  margin-left: 0.3rem;
  margin-right: 0.3rem;
}
.text-gray {
  color: gray;
}
.comments {
  /* border: 1px solid rgb(51, 255, 0); */
  text-align: left;
}
</style>