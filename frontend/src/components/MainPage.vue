<template>
  <div class="bg-black text-white">
    <article
      class="half-sized d-flex justify-content-center align-items-center"
    >
      <div>
        <h2>똑똑한 영화 추천 서비스</h2>
        <p>
          좋아하는 영화를 추천 받고<br />
          영화를 더 재미있게 즐기세요
        </p>
      </div>
    </article>
    <article
      class="half-sized d-flex justify-content-center align-items-center"
    >
      <div>
        <h2>경제적인 영화 추천 서비스</h2>
        <p>
          좋아하는 영화를 더 가성비 있게<br />
          영화를 보는 가장 싸고 좋은 방법
        </p>
      </div>
    </article>
    <div class="half-sized d-flex justify-content-center align-items-center">
      <div>
        <h2>지금 꼬꼬무에서 시작하세요</h2>
        <RouterLink
          v-if="accountStore.loginToken"
          class="btn btn-outline-light"
          to="/movies"
          >시작하기</RouterLink
        >
        <RouterLink v-else class="btn btn-outline-light" to="/accounts/login"
          >시작하기</RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router"
import { useAccountStore } from "@/stores/counter"

const accountStore = useAccountStore()
</script>

<style scoped>
h2 {
  font-size: 48px;
}

div > p {
  font-size: 24px;
}

.half-sized {
  height: 50vh;
}
</style>
