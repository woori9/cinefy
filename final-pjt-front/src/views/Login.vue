<template>
  <div class="margin-top">
    <h1 class="my-3">Login</h1>
    <b-form class="login-form my-2" @submit="login">
      <div class="form-item">
        <b-form-input
          class="input-box"
          placeholder="아이디를 입력하세요."
          v-model="auth.username"
          id="username"
          required>
        </b-form-input>
      </div>

      <div class="form-item">
        <b-form-input
          type="password"
          id="password"
          class="input-box"
          placeholder="비밀번호를 입력하세요."
          v-model="auth.password"
          required>
        </b-form-input>
      </div>

      <b-button
        class="mt-4 form-item login-btn"
        type="submit"
        variant="warning"
        @click="login">
        로그인
      </b-button>

      <div class="d-flex justify-content-center">
        <p class="mt-3 font-size">아직 회원이 아니신가요?</p>
        <b-button
          class="text-decoration-none font-size"
          variant="link"
          @click="toSignup">
          회원가입
        </b-button>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from '../api/server';

export default {
  name: 'Login',
  data: function () {
    return {
      auth: {
        username: '',
        password: '',
      }
    }
  },
  methods: {
    login: async function (event) {
      event.preventDefault();

      try {
        const response = await axios({
          method: 'post',
          url: '/api/token/',
          data: this.auth
        });

        const { access } = response.data;
        const { username, user_id } = JSON.parse(atob(access.split('.')[1]));
        localStorage.setItem('token', access);
        this.$store.commit('LOGIN', { username, user_id });
        this.$router.push({ name: 'Home'});
      } catch(err) {
        const { status } = err.response
        if (status === 401) {
          alert('입력한 정보를 다시 한번 확인해 주세요')
          return;
        }
      }
    },
    toSignup() {
      this.$router.push({ name: 'Signup' })
    }
  }
}
</script>

<style scoped>
.test {
  font-size: 15px;
  align-items: center;
}
.login-form {
  width: 28%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  margin: auto;
}
.form-item {
  margin: 2rem;
}
.font-size {
  font-size: 2rem
}
.input-box {
  height: 4rem;
}
.margin-top {
  margin-top: 10rem;
}
.margin-y {
  margin: 1.5rem 0;
}
.login-btn {
  height: 4rem;
  font-size: 1.5rem;
}
</style>
