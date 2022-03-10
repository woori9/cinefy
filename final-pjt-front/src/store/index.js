import Vue from 'vue'
import Vuex from 'vuex'
import axios from '../api/movie';
import axiosServer from '../api/server';
import axiosYoutube from '../api/youtube'
import days from '../utils/days';
import fromNow from '../utils/dayjs'
import router from '../router'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    username: null,
    userId: null,
    moviesByDate: [],
    thisMonth: null,
    reviews: [],
    isModalVisible: false,
    selectedMovie: null, // MovieDetail
    comments: [],
    commentCnt: 0,
    modalMode: '',
    selectedMovieTitle: '', // SearchForm에서 검색한 영화
    isMiniModalVisible: false,
    movieOST: null
  },
  mutations: {
    HIDE_MINI_MODAL(state) {
      state.isMiniModalVisible = false
    },
    SELECT_MOVIE_TITLE(state, movieTitle) { // 영화 제목 선택 + 모달 닫기
      state.selectedMovieTitle = movieTitle
      state.isModalVisible = false;
    },
    LOGIN(state, { username, user_id }) {
      state.username = username;
      state.userId = user_id
      state.isLoggedIn = true;
      state.userId = user_id;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
    },
    GET_MOVIES_BY_DATE(state, { month, results }) {
      state.thisMonth = month + 1
      state.moviesByDate = results;
    },
    GET_REVIEWS(state, reviews) {
      state.reviews = reviews
    },
    SHOW_MODAL(state, info) {
      if (info === 'search') {
        state.modalMode = info // 'search
      } else {
        state.selectedMovie = info  // {'title':, 'overview': ....}
      }
      state.isModalVisible = true;
    },
    HIDE_MODAL(state) {
      // 아래 두개의 순서가 바뀔 경우
      // 모달 창 -> 로그인 페이지로 강제로 이동했을 때,
      // selectedMovie가 null 이 되어 iframe source 관련 에러가 뜬다.
      state.isModalVisible = false;
      state.selectedMovie = null;
      state.modalMode = ''
    },
    ADD_REVIEW(state, newReview) {
      state.reviews.push(newReview)
      state.selectedMovieTitle = '' // 리뷰 작성하고 searchForm의 selectedMovieTitle=''
    },
    UPDATE_REVIEW(state, targetReview) {
      state.reviews = state.reviews.map(review => {
        if (review.id === targetReview.id) {
          return targetReview
        } else {
          return review
        }
      })
      state.selectedMovieTitle = ''
    },
    DELETE_REVIEW(state, targetReview) {
      state.reviews.splice(state.reviews.indexOf(targetReview), 1)
    },
    GET_COMMENTS(state, targetReview) {
      state.comments = targetReview.comment_set
      state.commentCnt = targetReview.comment_count
    },
    ADD_COMMENT(state, newComment) {
      state.comments.push(newComment)
      state.commentCnt = state.comments.length
    },
    UPDATE_COMMENT(state, targetComment) {
      state.comments = state.comments.map(comment => {
        if (comment.id === targetComment.id) {
          return targetComment
        } else {
          return comment
        }
      })
    },
    DELETE_COMMENT(state, targetComment) {
      state.comments.splice(state.comments.indexOf(targetComment), 1)
      state.commentCnt -= 1
    },
    SET_OST(state, movieOST) {
      state.movieOST = movieOST
      state.isMiniModalVisible = true
    },
  },
  actions: {
    async getOST({ commit }, originalTitle) {
      const response = await axiosYoutube({
        method: 'get',
        params: {
          q: `${originalTitle} ost`
        }
      })
      const { items } = response.data
      const movieOST = items.slice(0, 3).map(item => item.id.videoId)
      // const movieOST = ['c2rgrqEFVKc', '6K-4T1BDwUo']
      commit('SET_OST', movieOST);
    },
    async getMoviesByDate({ commit }) {
      const today = new Date();
      const year = today.getFullYear();
      const month = today.getMonth();
      const last_day = days[month];
      const dateString = `${year-1}-${month + 1}`;
      const { data } = await axios.get('/discover/movie?', {
        params: {
          'primary_release_date.gte': `${dateString}-01`,
          'primary_release_date.lte': `${dateString}-${last_day}`,
          'sort_by': 'popularity.desc',
          'language': 'ko-kr',
          'region': 'KR'
        }
      });
      const { results } = data;
      commit('GET_MOVIES_BY_DATE', { month, results });
    },
    async getReviews({ commit }) {
      const { data } = await axiosServer.get('community/')
      const reviews = data.map((review) => {
        return {
          'NO': review.id,
          '영화 제목': review.movie_title,
          '제목': review.title,
          '작성자': review.username,
          '작성일': fromNow(review.created_at),
          '좋아요': review.like_count
        }
      })
      commit('GET_REVIEWS', reviews);
    },
    async fetchBeforeOpenModal({ commit }, movie) {
      if (!movie.movie_code) {
        movie.movie_code = movie.id
        movie.category = 'with_date'
      }
      const { id, movie_code, title, overview, vote_average, category } = movie
      const response = await axios({
        method: 'get',
        url: `/movie/${movie_code}/credits?`,
        params: {
          language: 'ko-KR'
        }
      })
      const { data } = response
      const actors = data.cast.slice(0, 4).map(actor => actor.name)
      const director = data.crew.find(person => person.job === 'Director').name
      const trailers = await axiosYoutube({
        method: 'get',
        params: {
          q: `${title} trailer`
        }
      })
      const { items } = trailers.data
      const trailer = items[0]

      commit('SHOW_MODAL', { id, title, overview, category, vote_average, actors, director, trailer })
    },
    async addReview({ commit }, newReview) {
      const { data } = await axiosServer({
        method: 'post',
        url: 'community/create/',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        data: {
          ...newReview
        }
      })
      // localStorage.setItem('reviews', JSON.stringify([
      //   ...state.reviews,
      //   data
      // ]))
      commit('ADD_REVIEW', data)
      router.push({ name: 'Community' })
    },
    async updateReview({ commit }, targetReview) {
      const { data } = await axiosServer({
        method: 'put',
        url: `community/${targetReview.id}/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        data: {
          ...targetReview
        }
      })
      // const newReviews = state.reviews.map(review => {
      //   if (review.id === targetReview.id) {
      //     return targetReview
      //   } else {
      //     return review
      //   }
      // })
      // localStorage.setItem('reviews', JSON.stringify(newReviews))
      commit('UPDATE_REVIEW', data)
      router.push({ name: 'ReviewDetail', params: { reviewId: targetReview.id }})
    },
    async deleteReview({ commit }, targetReview) {
      await axiosServer({
        method: 'delete',
        url: `community/${targetReview.id}/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
      })
      // const newReviews = state.reviews.splice(state.reviews.indexOf(targetReview), 1)
      // localStorage.setItem('reviews', JSON.stringify(newReviews))
      commit('DELETE_REVIEW', targetReview)
      router.push({ name: 'Community' })
    },
    async addComment({ commit }, { reviewId, content }) {
      const { data } = await axiosServer({
        method: 'post',
        url: `community/${reviewId}/comments/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        data: {
          content
        }
      })
      commit('ADD_COMMENT', data)
    },
    async updateComment({ commit }, { reviewId, targetComment }) {
      const { data } = await axiosServer({
        method: 'put',
        url: `community/${reviewId}/comments/${targetComment.id}/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        data: {
          ...targetComment
        }
      })
      commit('UPDATE_COMMENT', data)
    },
    async deleteComment({ commit }, { reviewId, targetComment }) {
      await axiosServer({
        method: 'delete',
        url: `community/${reviewId}/comments/${targetComment.id}/`,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      commit('DELETE_COMMENT', targetComment)
    }
  },
})
