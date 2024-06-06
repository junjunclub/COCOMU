<template key>
  <div class="min-vh-100 movie-detail container bg-dark text-white">
    <div v-if="movieDetail" class="row">
      <div class="col-md-4 mb-4">
        <div v-if="movieDetail.poster_path">
          <img
            class="img-fluid poster"
            :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movieDetail.poster_path}`"
            :alt="movieDetail.title"
            @error="setDefaultPoster"
          />
        </div>
        <div v-else>
          <img
            class="img-fluid default-img"
            src="@/assets/poster_default.jpg"
            alt="defaultImg"
          />
        </div>
      </div>
      <div class="col-md-8">
        <div
          class="title d-flex justify-content-between align-items-center mb-3"
        >
          <div class="d-flex align-items-center">
            <h2 class="me-3">{{ movieDetail.title }}</h2>
            <div class="genres">
              <span
                v-for="(genre, index) in movieDetail.genres"
                :key="index"
                class="genre badge bg-dark me-1"
                >{{ genre.name }}</span
              >
            </div>
          </div>
          <div class="btn-group" role="group">
            <button class="btn btn-outline-light" @click="likeMovie">
              {{ isLiked ? "찜 목록에서 제거" : "찜 목록에 추가" }}
            </button>
          </div>
        </div>
        <div class="overview mb-3">
          <h4 class="text-start">줄거리</h4>
          <p class="text-start">{{ movieDetail.overview }}</p>
        </div>
        <div class="actors mb-3">
          <h4 class="text-start">배우 및 감독</h4>
          <div class="row">
            <div
              v-for="(actor, index) in movieDetail.actor"
              :key="index"
              class="col-6 col-md-4 col-lg-2"
            >
              <div class="actor">
                <div v-if="actor.profile_path">
                <img
                  class="img-fluid actor-img"
                  :src="`https://image.tmdb.org/t/p/w300_and_h450_bestv2${actor.profile_path}`"
                  :alt="actor.name"
                  @error="setDefaultPersonImage"
                />
              </div>
                <div v-else>
                  <img
                    class="img-fluid default-img"
                    src="@/assets/profile_defaultimg.jpg"
                    alt="defaultImg"
                  />
                </div>
                <p class="actor-name">{{ actor.name }}</p>
                <p class="actor-original-name">{{ actor.character }}</p>
              </div>
            </div>
            <div class="col-6 col-md-4 col-lg-2">
              <div class="director">
                <div v-if="movieDetail.director.profile_path">
                  <img
                    class="img-fluid director-img"
                    :src="`https://image.tmdb.org/t/p/w300_and_h450_bestv2${movieDetail.director.profile_path}`"
                    :alt="movieDetail.director.name"
                  />
                </div>
                <div v-else>
                  <img
                    class="img-fluid default-img"
                    src="@/assets/profile_defaultimg.jpg"
                    alt="defaultImg"
                  />
                </div>
                <p class="director-name">{{ movieDetail.director.name }}</p>
              </div>
            </div>
          </div>
          <button class="btn btn-primary" @click="getRecommendations">
            AI 추천받기
          </button>

          <div v-if="recommendMovies.length > 0" class="row mt-4">
            <div
              v-for="(movie, index) in recommendMovies"
              :key="movie.movie_id"
              class="col-12 col-sm-6 col-md-4 mb-4"
            >
              <MovieCard :movie="movie" />
            </div>
          </div>
          <div v-else class="mt-4">
            <div v-if="!isLoading">추천버튼을 클릭하세요</div>
            <div v-else>
              <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading text-center">로딩 중...</div>
  </div>
</template>

<script setup>
import axios from "axios"
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useMovieStore, useAccountStore } from "@/stores/counter"
import MovieCard from "@/components/MovieCard.vue"

const defaultPoster = "@/assets/poster_default.jpg"
const defaultPersonPoster = "@/assets/profile_defaultimg.jpg"

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const accountStore = useAccountStore()

const movieId = ref(route.params.movieId)
const movieDetail = ref(null)
const isLiked = ref(false)
const searchResult = ref(null)
const recommendMovies = ref([])

const isLoading = ref(false)

axios({
  method: "GET",
  url: `${movieStore.API_URL}/movies/${movieId.value}`,
  headers: {
    Authorization: `Token ${accountStore.loginToken}`,
  },
})
  .then((response) => {
    movieDetail.value = response.data

    accountStore.getUserInfo().then((data) => {
      isLiked.value = movieDetail.value.like_user.includes(data.id)
    })
  })
  .catch((error) => {
    console.log(error)
    alert("유효하지 않은 영화 ID입니다. 영화 메인 페이지로 이동합니다.")
    router.push({ name: "MovieListView" })
  })

const likeMovie = function () {
  movieStore.likeMovie(movieId.value)
  isLiked.value = !isLiked.value
}

const getRecommendations = function () {
  isLoading.value = true
  axios({
    method: "get",
    url: `${accountStore.API_URL}/movies/${movieId.value}/recommend`,
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      searchResult.value = response.data
      recommendMovies.value = searchResult.value.related_movies
      console.log(recommendMovies.value)
      isLoading.value = false
    })
    .catch((error) => {
      console.log(error)
      alert("OpenAI API 사용량이 초과되었습니다. 잠시 후 다시 시도해주세요.")
      isLoading.value = false
    })
}

const setDefaultPoster = (event) => {
  event.target.src = defaultPoster
}

const setDefaultPersonImage = (event) => {
  event.target.src = defaultPersonPoster
}
</script>

<style scoped>
.movie-detail {
  padding-top: 50px;
}

.poster {
  max-width: 100%;
}

.title {
  border-bottom: 1px solid #ccc;
}

.btn-outline-light {
  padding: 0.5rem 1rem;
}

.genre {
  margin-right: 5px;
}

.overview {
  line-height: 1.6;
}

.actor-img,
.director-img {
  width: 100%;
  border-radius: 5px;
  margin-bottom: 10px;
}

.default-img {
  width: 100%;
}

.actor-name,
.director-name {
  font-weight: bold;
}

.actor-original-name {
  font-style: italic;
}

.loading {
  margin-top: 50px;
  font-size: 18px;
}
</style>
