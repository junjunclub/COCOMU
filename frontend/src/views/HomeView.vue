<template>
  <header class="text-white d-flex justify-content-center align-items-center">
    <div>
      <h1 class="title">COCOMU</h1>
      <h2>꼬리에 꼬리를 무는 무비 이야기</h2>
    </div>
  </header>
  <MainPage />
</template>

<script setup>
import MainPage from "@/components/MainPage.vue"
</script>

<style scoped>
header {
  height: 100vh;
  background-image: url("@/assets/mainbackground.jpg");
  background-size: cover;
}

header::before {
  content: "";
  position: absolute;
  top: 56px;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(2, 2, 2, 0.4);
  z-index: 1;
}

header > div {
  z-index: 2;
}

.title {
  font-size: 65px;
}
</style>
