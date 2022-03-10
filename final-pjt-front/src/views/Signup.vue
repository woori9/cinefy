<template>
  <div class="margin-top">
    <h1 class="my-3">Sign into your account</h1>
    <b-form class="signup-form my-2" @submit="signup">

      <div class="form-item">
        <b-form-input
          autocomplete="off"
          class="input-box"
          placeholder="아이디를 입력하세요."
          v-model="auth.username"
          :state="checkUsername"
          id="feedback-user">
        </b-form-input>
        <b-form-invalid-feedback
          v-if="auth.username"
          :state="checkUsername"
          class="feedback">
          {{ message.username }}
        </b-form-invalid-feedback>
        <b-form-valid-feedback
          v-if="auth.username"
          :state="checkUsername"
          class="feedback">
          {{ message.okay }}
        </b-form-valid-feedback>
      </div>

      <div class="form-item">
        <b-form-input
          class="input-box"
          type="password"
          id="text-password"
          aria-describedby="password-help-block"
          placeholder="비밀번호를 입력해주세요."
          v-model="auth.password"
          :state="checkPassword">
        </b-form-input>
        <b-form-invalid-feedback
          :state="checkPassword"
          class="feedback"
          id="password-help-block">
          {{ message.password }}
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="checkPassword" class="feedback" id="password-help-block">
          {{ message.okay }}
        </b-form-valid-feedback>
      </div>

      <div class="form-item">
        <b-form-input
          class="input-box"
          type="password"
          id="confirm-password"
          aria-describedby="password-confirm-help-block"
          placeholder="비밀번호 확인"
          v-model="auth.confirmation"
          :state="checkConfirmation">
        </b-form-input>
        <b-form-invalid-feedback
          :state="checkConfirmation"
          class="feedback"
          id="password-confirm-help-block">
          {{ message.confirmation }}
        </b-form-invalid-feedback>
        <b-form-valid-feedback
          :state="checkConfirmation"
          class="feedback"
          id="password-confirm-help-block">
          {{ message.okay }}
        </b-form-valid-feedback>
      </div>

      <b-button
        class="mt-4 signup-btn"
        type="submit"
        variant="warning"
        @click="signup">
        회원가입
      </b-button>
    </b-form>
  </div>
</template>

<script>
import axios from '../api/server';
import { isValidUsername, isValidPassword, isValidConfirmation } from '../utils/validation';
import {
  NOT_VALID_ID_MESSAGE,
  NOT_VALID_PASSWORD_MESSAGE,
  NOT_SAME_PASSWORD_MESSAGE,
  OKAY_MESSAGE,
  ID_ALREADY_EXIST,
} from '../constant';

export default {
  name: 'Signup',
  data: function () {
    return {
      auth: {
        username: '',
        password: '',
        confirmation: '',
      },
      message: {
        okay: OKAY_MESSAGE,
        username: NOT_VALID_ID_MESSAGE,
        password: NOT_VALID_PASSWORD_MESSAGE,
        confirmation: NOT_SAME_PASSWORD_MESSAGE,
      }
    };
  },
  methods: {
    signup: async function (event) {
      event.preventDefault();

      if (!this.checkUsername) {
        alert(NOT_VALID_ID_MESSAGE)
        return
      }

      if (!this.checkPassword) {
        alert(NOT_VALID_PASSWORD_MESSAGE)
        return
      }

      if(!this.checkConfirmation) {
        alert(NOT_SAME_PASSWORD_MESSAGE)
        return
      }

      try {
        const response = await axios({
          method: 'post',
          url: '/accounts/signup/',
          data: this.auth
        })

        const { status } = response
        if (status === 201) {
          return this.$router.push({ name: 'Login' })
        }
      } catch(err) {
        const { status } = err.response
          if (status === 400) {
            alert(ID_ALREADY_EXIST)
            this.auth.username = '';
            return
          }
      }
    }
  },
  computed: {
    checkUsername() {
      if (!this.auth.username) return null;
      return isValidUsername(this.auth.username);
    },
    checkPassword() {
      if (!this.auth.password) return null;
      return isValidPassword(this.auth.password);
    },
    checkConfirmation() {
      if (!this.auth.confirmation) return null;
      return isValidConfirmation(this.auth.password, this.auth.confirmation);
    },
  }
}
</script>

<style scoped>
.signup-form {
  width: 28%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  margin: auto;
}
.margin-top {
  margin-top: 10rem;
}
.margin-y {
  margin: 1rem 0;
}
.input-box {
  height: 4rem;
}
.form-item {
  position: relative;
  margin-top: 0.5rem;
  padding-bottom: 1.5rem;
}
.feedback {
  text-align: left;
  position: absolute;
  bottom: 0;
  left: 0;
  font-size: 15px;
}
.signup-btn {
  height: 4rem;
  font-size: 1.5rem;
}

</style>
