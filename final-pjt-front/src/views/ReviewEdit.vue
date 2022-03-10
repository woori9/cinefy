<template>
  <div class="container">
    <h2 class="margin-top">리뷰 작성</h2>
    <form @submit="editReview" class="input-margin">
      <b-row class="justify-content-center">
        <b-input
          class="input-width"
          v-model.trim="title"
          id="title"
          placeholder="제목을 입력해주세요"
          autocomplete="off"
        >
        </b-input>
      </b-row>

      <b-row class="justify-content-center">
        <b-input
          class="input-width"
          v-model.trim="movieTitle"
          id="movie_title"
          placeholder="영화 제목을 입력해주세요"
          @click="showSearchModal"
          autocomplete="off"
          readonly
        >
        </b-input>
      </b-row>

      <b-row class="justify-content-center">
        <b-form-textarea
          class="input-width text-area"
          v-model.trim="content"
          id="content"
          placeholder="내용을 입력해주세요"
          autocomplete="off"
        >
        </b-form-textarea>
      </b-row>
      <b-button class="my-2" type="submit" variant="warning">작성</b-button>
    </form>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ReviewEdit',
  data() {
    return {
      title: null,
      // movieTitle: null,
      content: null,
    }
  },
  props: {
    review: {
      type: Object,
    }
  },
  computed: {
    ...mapState(['isLoggedIn']),
    movieTitle: {
      get() {
        console.log('movie-title', this.$store.state.selectedMovieTitle)
        return this.$store.state.selectedMovieTitle;
      },
      set(newValue) {
        console.log('####', newValue)
        return newValue
      }
    },
  },
  methods: {
    showSearchModal() {
      this.$store.commit('SHOW_MODAL', 'search')
    },
    editReview: function (event) {
      if (!this.isLoggedIn) {
        alert('로그인 해주세요')
        this.$router.push({ name: 'Login' }).catch(()=>{})
        return;
      }

      event.preventDefault()
      if (!this.title || !this.movieTitle || !this.content) {
        alert('빈칸을 전부 채워주세요')
        return;
      }

      if (this.review) {
        const reviewItem = {
          ...this.review,
          title: this.title,
          movie_title: this.movieTitle,
          content: this.content
        }
        this.$store.dispatch('updateReview', reviewItem)
        
      } else {
        const reviewItem = {
          title: this.title,
          movie_title: this.movieTitle,
          content: this.content
        }
        this.$store.dispatch('addReview', reviewItem)
      }
      
    },
  },
  mounted() {
    if (this.review) {
      this.title = this.review.title
      this.content = this.review.content
    }
  }
}
</script>

<style scoped>
.margin-top {
  margin-top: 2rem;
}
.input-width {
  width: 800px;
  margin: 1.5rem 0;
}
.text-area {
  height: 200px;
}
::-webkit-input-placeholder {
  font-size: 20px;
}
</style>