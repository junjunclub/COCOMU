<template>
  <div class="vh-100 bg-theater bg-black">
    <div class="h-100 d-flex justify-content-center align-items-center">
      <section class="card p-5 bg-dark bg-opacity-75 text-white">
        <h1>로그인</h1>
        <p>꼬꼬무에 오신 것을 환영합니다</p>
        <form @submit.prevent="loginRequest" class="my-5">
          <input
            class="form-control mb-3 bg-dark text-white"
            type="text"
            name="username"
            id="username"
            v-model="username"
            placeholder="아이디를 입력해주세요"
          />

          <input
            class="form-control mb-3 bg-dark text-white"
            type="password"
            name="password"
            id="password"
            v-model="password"
            placeholder="비밀번호를 입력해주세요"
          />

          <button class="btn btn-outline-light w-100" type="submit">
            로그인
          </button>
        </form>
        <p>
          아직 회원이 아니신가요?
          <RouterLink
            class="no-underline text-white-50 fw-bold"
            to="/accounts/signup"
            >회원가입</RouterLink
          >
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { RouterLink } from "vue-router"
import { useAccountStore } from "@/stores/counter"
import { useRouter } from "vue-router"

const username = ref(null)
const password = ref(null)

const router = useRouter()
const accountStore = useAccountStore()

const loginRequest = function () {
  const payload = {
    username: username.value,
    password: password.value,
  }
  accountStore.login(payload)
}
</script>

<style scoped>
.no-underline {
  text-decoration: none;
}

.bg-theater {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("@/assets/mainpage_theater.jpg");
}

::placeholder {
  color: grey;
}
</style>
