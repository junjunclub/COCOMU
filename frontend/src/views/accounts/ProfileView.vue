<template>
  <div class="vh-100 bg-profile">
    <div class="vh-100" v-if="userInfo">
      <div class="h-100 d-flex justify-content-center align-items-center">
        <section class="card w-50 p-5 bg-dark bg-opacity-75 text-white">
          <h1 class="text-start mb-3">{{ userInfo.name }}님</h1>
          <div class="text-end">
            <RouterLink
              class="btn btn-outline-light"
              :to="{ name: 'ProfileUpdateView' }"
              >회원정보 수정</RouterLink
            >
          </div>
          <article class="mt-5">
            <h5 class="text-start text-white-50 mb-3">개인 정보</h5>
            <div class="row mb-3">
              <span class="col text-start">아이디</span
              ><span class="col text-end">{{ userInfo.username }}</span>
            </div>
            <div class="row mb-3">
              <span class="col text-start">이메일</span
              ><span class="col text-end">{{ userInfo.email }}</span>
            </div>
            <div class="row mb-3">
              <span class="col text-start">닉네임</span
              ><span class="col text-end">{{ userInfo.nickname }}</span>
            </div>
            <div class="row mb-3">
              <span class="col text-start">생년월일</span
              ><span class="col text-end">{{ userInfo.birth }}</span>
            </div>
            <hr />
            <div class="row">
              <h5 class="col text-start text-white-50">서비스 이용 정보</h5>
              <div class="col text-end mb-3">
                <RouterLink
                  class="btn btn-outline-light"
                  :to="{ name: 'SecondSurveyView' }"
                  >가입 설문 재응답</RouterLink
                >
              </div>
            </div>
            <div class="row">
              <span class="col text-start">내 서비스</span>
              <div class="col text-end mb-3">
                <div
                  v-if="userInfo.ott"
                  v-for="serviceId in userInfo.ott.ott"
                  :key="serviceId"
                >
                  <span>{{ ottName[serviceId] }}</span>
                </div>
              </div>
            </div>
          </article>
          <RouterLink
            class="text-start text-white-50 signout-link"
            :to="{ name: 'SignOutView' }"
            >회원 탈퇴</RouterLink
          >
        </section>
      </div>
    </div>
    <div v-else>오류: 데이터 없음</div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter, RouterLink } from "vue-router"
import { useAccountStore, useMovieStore } from "@/stores/counter"
import axios from "axios"

const router = useRouter()
const accountStore = useAccountStore()
const movieStore = useMovieStore()
const userInfo = ref(null)

// OTT id -> 이름 변환기
const ottName = movieStore.ottList

// 로그인 되어 있지 않으면 로그인 시키게 이동시킴
if (accountStore.loginToken) {
  axios({
    method: "GET",
    url: `${accountStore.API_URL}/accounts/profile/`,
    headers: { Authorization: `Token ${accountStore.loginToken}` },
  })
    .then((response) => {
      userInfo.value = response.data
      console.log(response.data)
    })
    .catch((error) => console.log(error))
} else {
  alert("로그인이 필요합니다.")
  router.push({ name: "LoginView" })
}
</script>

<style scoped>
.bg-profile {
  background-image: url("@/assets/mainpageticketimage.jpg");
}

.signout-link {
  text-decoration: none;
}
</style>
