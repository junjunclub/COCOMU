<template>
  <div class="full-height bg-dark text-white">
    <section class="h-100 y-padding d-flex justify-content-center flex-column">
      <h1>회원가입</h1>
      <p>
        이미 회원이신가요?
        <RouterLink
          class="fw-bold text-white-50 no-underline"
          to="/accounts/login"
          >로그인</RouterLink
        >
      </p>
      <form
        class="text-start align-self-center w-50"
        @submit.prevent="signUpRequest"
      >
        <label class="form-label" for="username">아이디</label>
        <input
          class="form-control bg-dark text-white"
          type="text"
          name="username"
          id="username"
          v-model="username"
          placeholder="아이디를 입력해주세요"
        /><br />

        <label class="form-label" for="password1">비밀번호</label>
        <input
          class="form-control bg-dark text-white"
          type="password"
          name="password1"
          id="password1"
          v-model="password1"
          placeholder="비밀번호를 입력해주세요"
        /><br />

        <label class="form-label" for="password2">비밀번호 확인</label>
        <input
          class="form-control bg-dark text-white"
          type="password"
          name="password2"
          id="password2"
          v-model="password2"
          placeholder="비밀번호를 다시 한 번 입력해주세요"
        /><br />

        <label class="form-label" for="name">이름</label>
        <input
          class="form-control bg-dark text-white"
          type="text"
          name="name"
          id="name"
          v-model="name"
          placeholder="자신의 실명을 입력해주세요"
        /><br />

        <label class="form-label" for="nickname">닉네임</label>
        <input
          class="form-control bg-dark text-white"
          type="text"
          name="nickname"
          id="nickname"
          v-model="nickname"
          placeholder="사용할 별명을 입력해주세요"
        /><br />

        <label class="form-label" for="email">이메일</label>
        <input
          class="form-control bg-dark text-white"
          type="email"
          name="email"
          id="email"
          v-model="email"
          placeholder="유효한 이메일 주소를 입력해주세요"
        /><br />

        <label class="form-label" for="birth">생년월일</label>
        <input
          class="form-control bg-dark text-white"
          type="date"
          name="birth"
          id="birth"
          v-model="birth"
          placeholder="본인의 생년월일을 입력해주세요"
        /><br />

        <button class="btn btn-outline-light w-100" type="submit">
          회원가입
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { RouterLink } from "vue-router"
import { useAccountStore } from "@/stores/counter"

const accountStore = useAccountStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const name = ref(null)
const email = ref(null)
const nickname = ref(null)
const birth = ref(null)

const signUpRequest = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    name: name.value,
    email: email.value,
    nickname: nickname.value,
    birth: birth.value,
  }

  accountStore.signUp(payload)
}
</script>

<style scoped>
.full-height {
  min-height: 100vh;
}

.y-padding {
  padding: 80px 0px;
}

.no-underline {
  text-decoration: none;
}

::placeholder {
  color: grey;
}
</style>
