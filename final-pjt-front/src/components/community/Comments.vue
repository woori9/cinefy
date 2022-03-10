<template>
  <div class="scroll">
    <p>{{ commentCnt }}개의 댓글이 있습니다.</p>
    <form @submit="addComment" >
      <div class="create-form">
        <b-form-input
          id="textarea"
          v-model="content"
          placeholder="Enter something..."
          rows="3"
          max-rows="6"
        >
        </b-form-input>
        <div class="comment-button">
          <b-button type="submit" variant="warning">
            등록
          </b-button>

        </div>
      </div>
    </form>
    <div class="padding-bottom">
      <div v-for="comment in comments" :key="comment.id">
        <p class="comment-border-top">
          <span v-if="updateTargetComment === comment">
            <form @submit="updateComment" class="create-form">
              <b-form-input type="text" v-model="targetContent"></b-form-input>
              <div class="comment-button">
                <b-button type="submit">수정</b-button>
              </div>
            </form>
          </span>
          <span v-else>
            <span class="comment-info">
              <span>
                <span class="font-bold margin-right">{{ comment.username }}</span>
                <span class="text-gray">{{ comment.created_at }}</span> 
              </span>
              <span v-if="comment.username === $store.state.username">
                <b-button variant="link" @click="showUpdateForm(comment)">수정</b-button>
                <b-button class="button-padding" variant="link" @click="deleteComment(comment)">삭제</b-button>
              </span>
            </span>
            <p class="comment-content">{{ comment.content }}</p>
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import fromNow from '../../utils/dayjs'

export default {
  name: 'Comments',
  data() {
    return {
      content: null,
      updateTargetComment: null,
      targetContent: null,
    }
  },
  props: {
    review: {
      type: Object,
    }
  },
  computed: {
    comments() {
      return this.$store.state.comments.map(comment => {
        return {
          ...comment,
          created_at: fromNow(comment.created_at),
          updated_at: fromNow(comment.updated_at)
        }
      })
    },
    commentCnt() {
      return this.$store.state.commentCnt
    },
  },
  methods: {
    addComment: function (event) {
      event.preventDefault()

      if (!this.content) {
        return;
      }
      this.$store.dispatch('addComment', { reviewId: this.review.id, content: this.content })
      this.content = ''
    },
    updateComment: function (event) {
      event.preventDefault()

      if (!this.targetContent) {
        return;
      }
      const targetComment = {
        ...this.updateTargetComment,
        content: this.targetContent
      }
      this.$store.dispatch('updateComment', { reviewId: this.review.id, targetComment })
      this.updateTargetComment = null
      this.targetContent = null
    },
    deleteComment: function (targetComment) {
      this.$store.dispatch('deleteComment', { reviewId: this.review.id, targetComment })
    },
    showUpdateForm: function (comment) {
      this.updateTargetComment = comment
      this.targetContent = this.updateTargetComment.content
    },
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100&display=swap');

.create-form {
  /* display: flex; */
  align-items: center;
  margin-bottom: 1.5rem;
}
.comment-button {
  margin: 0.8rem 0;
  text-align: right;
}
.comment-info {
  display: flex;
  justify-content: space-between;
}
.button-padding {
  padding-right: 0;
}
.font-bold {
  font-weight: bold;
}
.comment-content {
  font-weight: 200;
  white-space: pre-line;
}
.comment-border-top {
  border-bottom: 1px solid rgb(230, 230, 230);
}
.padding-bottom {
  padding-bottom: 15rem;
}
.margin-right {
  margin-right: 1rem;
}
.text-gray {
  color: gray;
}
.scroll {
  height: 30vmax;
}
</style>