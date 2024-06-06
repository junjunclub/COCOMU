<script setup>
import { RouterLink, RouterView } from "vue-router"
import { useAccountStore } from "./stores/counter"

const accountStore = useAccountStore()

const logoutRequest = function () {
  accountStore.logout()
  alert("로그아웃 되었습니다.")
}
</script>

<template>
  <div>
    <nav class="row py-3 navbar bg-dark text-white">
      <div class="text-start col-4 px-5">
        <RouterLink class="nav-link" to="/">
          <img src="@/assets/white_logo.png" style="height: 25px" />
        </RouterLink>
      </div>
      <div class="text-center col-4">
        <RouterLink class="nav-link d-inline" to="/movies">영화</RouterLink> |
        <RouterLink class="nav-link d-inline" to="/community"
          >커뮤니티</RouterLink
        >
      </div>
      <div class="text-end col-4 px-5">
        <div v-if="accountStore.loginToken">
          <RouterLink class="nav-link d-inline" to="/accounts/profile"
            >프로필</RouterLink
          >
          |
          <RouterLink class="nav-link d-inline" to="/accounts/bookmark">
            찜 목록
          </RouterLink>
          |
          <p
            class="nav-link d-inline"
            @click="logoutRequest"
            style="cursor: pointer"
          >
            로그아웃
          </p>
        </div>
        <div v-else>
          <RouterLink class="nav-link d-inline" to="/accounts/login"
            >로그인</RouterLink
          >
          |
          <RouterLink class="nav-link d-inline" to="/accounts/signup"
            >회원가입</RouterLink
          >
        </div>
      </div>
    </nav>
    <div class="text-center">
      <div class="row">
        <RouterView class="col-12" />
      </div>
    </div>
    <footer
      class="py-3 bg-dark d-flex justify-content-center align-items-center text-white"
    >
      <p class="my-0">Copyright 2024. COCOMU All Rights Reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
div {
  font-family: "Pretendard Variable";
}

nav {
  z-index: 3;
}
</style>
