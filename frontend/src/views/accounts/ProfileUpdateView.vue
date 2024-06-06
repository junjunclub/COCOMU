<template>
  <div class="vh-100 bg-profileupdate">
    <div class="h-100 d-flex justify-content-center align-items-center">
      <section class="card p-5 bg-dark bg-opacity-75 text-white w-50">
        <h1 class="mb-4">회원 정보 수정</h1>
        <form
          class="text-start align-self-center w-100"
          @submit.prevent="updateProfile"
        >
          <label class="form-label mb-1" for="name">이름</label>
          <input
            class="form-control bg-dark text-white mb-3"
            type="text"
            id="name"
            v-model="name"
          />
          <label class="form-label mb-1" for="nickname">닉네임</label>
          <input
            class="form-control bg-dark text-white mb-3"
            type="text"
            id="nickname"
            v-model="nickname"
          />
          <button class="btn btn-outline-secondary w-100" type="submit">
            수정 완료
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAccountStore } from "@/stores/counter"

const accountStore = useAccountStore()

const email = ref(null)
const name = ref(null)
const nickname = ref(null)
const birth = ref(null)
const userInfoPromise = accountStore.getUserInfo()
userInfoPromise.then((data) => {
  email.value = data.email
  name.value = data.name
  nickname.value = data.nickname
  birth.value = data.birth
})

const updateProfile = function () {
  accountStore.updateUserInfo({
    email: email.value,
    name: name.value,
    nickname: nickname.value,
    birth: birth.value,
  })
}
</script>

<style scoped>
.bg-profileupdate {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("@/assets/martian.jpg");
  background-size: cover;
}
</style>
