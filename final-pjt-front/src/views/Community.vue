<template>
  <div class="community container">
    <b-button class="toggle-sidebar-btn" variant="warning" v-b-toggle.sidebar-border>
      <font-awesome-icon :icon="['fas', 'chevron-right']" color="#purple" size="2x"/>
    </b-button>
    
    <!-- <img src="../assets/image.jpg" alt="community"> -->
    <div class="community-header">
      <div class="community-header-content"></div>
      <h3 class="community-header-text">c o m m u n i t y</h3>
    </div>
    <div>
      <b-button class="edit-btn" @click="editLink" variant="outline-warning">글쓰기</b-button>
    </div>
    <div class="review-board parent-box">
      <div class="overflow-auto" v-if="reviews.length">
        <b-table
          class="table-color"
          :items="reviews"
          @row-clicked="reviewLink"
          :per-page="perPage"
          :current-page="currentPage"
        >
        </b-table>
        <div class="community-pagination">
          <b-pagination
            class="my-pagination"
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
          >
          </b-pagination>
        </div>
      </div>
      <div v-else>
        <h3>게시물이 존재하지 않습니다.</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Community',
  data() {
    return {
      perPage: 5,
      currentPage: 1,
    }
  },
  computed: {
    reviews() {
      return this.$store.state.reviews
    },
    rows() {
      return this.reviews.length
    }
  },
  methods: {
    reviewLink: function (review) {
      if (this.$store.state.isLoggedIn) {
        const reviewId = review['NO']
        this.$router.push({ name: 'ReviewDetail', params: { reviewId }})
      } else {
        this.$router.push({ name: 'Login' })
      }
    },
    editLink: function () {
      this.$router.push({ name: 'ReviewEdit', params: { review: null } })
    }
  },
  created() {
    this.$store.dispatch('getReviews')
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600&display=swap');

.community {
  margin-top: 50px;
  /* height: 500px; */
  height: 55vmax;
}
.community-header-content {
  background-repeat: no-repeat;
  background-image: url("../assets/community-header.png");
  width: 1110px;
  height: 300px;
  background-position: center center;
}
.community-header-text {
  font-family: 'Outfit', sans-serif;
  color: rgb(255, 255, 255);
  font-size: 50px;
  margin-top: -60px;
}
.review-board {
  margin-top: 60px;
  color: rgb(230, 230, 230);
  cursor: pointer;
}
.edit-btn {
  position: absolute;
  margin-left: 30em;
}
.review-item {
  cursor: pointer;
}
.toggle-sidebar-btn {
  position: absolute;
  left: 0;
  top: 50%;
}
.parent-box {
  position: relative;
}
.community-pagination {
  position: absolute;
  top: 22rem;
  left: 29rem;
}
.table-color{
  background-color: rgb(15, 12, 29) !important;
  color: white !important;
}
.table-color > tbody > tr:hover {
  background-color: white !important;
  color: rgb(15, 12, 29) !important;
}
.page-item.active .page-link {
    background-color: rgb(104, 54, 202) !important;
    border-color: rgb(104, 54, 202)!important;
    color: rgb(255, 223, 80) !important;
}
.page-item .page-link {
    background-color: rgb(246, 245, 241) !important;
    border-color: rgb(246, 245, 241) !important;
    color: rgb(4, 6, 98) !important;
}
.page-item.disabled .page-link {
    background-color: rgb(246, 245, 241) !important;
    border-color: rgb(246, 245, 241) !important;
    color: rgb(4, 6, 98) !important;
}
</style>
