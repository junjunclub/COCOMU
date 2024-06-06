<template>
  <div
    class="card movie-card bg-transparent text-white"
    style="width: 18rem; position: relative"
    @mouseover="isHovered = true"
    @mouseleave="isHovered = false"
  >
  <div v-if="movie.poster_path">
    <img
      :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movie.poster_path}`"
      class="card-img-top movie-img"
      alt="Movie poster"
    />
  </div>
  <div v-else>
    <img
      class="img-fluid default-img"
      src="@/assets/poster_default.jpg"
      alt="defaultImg"
    />
  </div>
    <div v-if="isHovered" class="hover-overlay">
      <div class="hover-buttons">
        <!-- <button class="btn btn-primary" @click="goToDetail">자세히 보기</button> -->
        <a
          :href="`http://127.0.0.1:5173/movies/${movie.movie_id}`"
          class="btn btn-primary"
          >자세히 보기</a
        >
        <button class="btn btn-secondary" @click="likeMovie">
          {{ isLiked ? "찜하기 취소" : "찜하기" }}
        </button>
      </div>
    </div>
    <div class="card-body">
      <p class="card-title">{{ movie.title }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useMovieStore, useAccountStore } from "@/stores/counter"
import { useRoute } from "vue-router"
import axios from "axios"

const accountStore = useAccountStore()
const movieStore = useMovieStore()

// Props를 가져오는 방법
const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
})

// 컴포지션 API를 사용하여 상태 정의
const isHovered = ref(false)
const isLiked = ref(false)

// 라우터 사용
const router = useRouter()
const route = useRoute()

axios({
  method: "GET",
  url: `${movieStore.API_URL}/movies/${props.movie.movie_id}`,
  headers: {
    Authorization: `Token ${accountStore.loginToken}`,
  },
})
  .then((response) => {
    accountStore.getUserInfo().then((data) => {
      isLiked.value = response.data.like_user.includes(data.id)
    })
  })
  .catch((error) => {
    console.log(error)
  })

// 메서드 정의
const goToDetail = () => {
  router.push({
    name: "MovieDetailView",
    params: { movieId: props.movie.movie_id },
    force: true,
  })
}

const likeMovie = () => {
  console.log(props.movie)
  movieStore.likeMovie(props.movie.movie_id)
  isLiked.value = !isLiked.value
}
</script>

<style scoped>
.card {
  border: none;
}

.movie-card {
  transition: background-color 0.3s;
  position: relative;
  overflow: hidden;
}
.movie-img {
  transition: filter 0.3s;
}
.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}
.hover-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.hover-buttons button {
  width: 100px;
}
</style>
