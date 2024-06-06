<template>
  <div class="bg-signout row">
    <div class="h-100 d-flex justify-content-center align-items-center">
      <section class="card p-5 bg-dark text-white">
        <p>정말 회원 탈퇴 하시겠습니까?</p>
        <div>
          <button @click="goBack" class="btn btn-secondary me-3">
            아니오, 돌아갑니다.
          </button>
          <button @click="signOutRequest" class="btn btn-outline-danger">
            네, 탈퇴합니다.
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useAccountStore } from "@/stores/counter"

const router = useRouter()
const accountStore = useAccountStore()

const goBack = function () {
  router.go(-1)
}
const signOutRequest = function () {
  accountStore.signOut()
}
</script>

<style scoped>
.bg-signout {
  height: 100vh;
  background-image: url("@/assets/mainpage_cinema.jpg");
}

.bg-signout::before {
  content: "";
  position: absolute;
  top: 56px;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
