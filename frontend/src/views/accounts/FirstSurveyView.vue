<template>
  <main>
    <div class="d-flex justify-content-center align-items-center">
      <section class="w-75 my-5 card bg-dark bg-opacity-75 text-white">
        <div>
          <div class="my-5">
            <h1>설문조사</h1>
            <p>원활한 서비스 제공을 위하여 다음 설문에 응답해주세요.</p>
          </div>

          <article class="d-flex justify-content-center">
            <div class="w-75">
              <!-- question 1 -->
              <div class="my-5">
                <h5 class="mb-4">영화를 어떤 경로로 자주 보나요?</h5>
                <div class="row">
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question1"
                      value="영화관"
                      id="answer1-1"
                    />
                    <label class="form-check-label" for="answer1-1"
                      >영화관</label
                    >
                  </div>
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question1"
                      id="answer1-2"
                      value="모바일, 웹"
                    />
                    <label class="form-check-label" for="answer1-2"
                      >모바일, 웹</label
                    >
                  </div>
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question1"
                      id="answer1-3"
                      value="DVD / Blue-ray 구매"
                    />
                    <label class="form-check-label" for="answer1-3"
                      >DVD / Blue-ray 구매</label
                    >
                  </div>
                </div>
              </div>

              <!-- question 2 -->
              <div class="my-5" v-if="isCompleted[1]">
                <h5 class="mb-4">누구와 함께 영화를 보나요?</h5>
                <div class="row">
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question2"
                      value="혼자"
                      id="answer2-1"
                    />
                    <label class="form-check-label" for="answer2-1">혼자</label>
                  </div>
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question2"
                      id="answer2-2"
                      value="가족"
                    />
                    <label class="form-check-label" for="answer2-2"
                      >가족과 함께</label
                    >
                  </div>
                  <div class="form-check col">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question2"
                      id="answer2-3"
                      value="친구"
                    />
                    <label class="form-check-label" for="answer2-3"
                      >친구와 함께</label
                    >
                  </div>
                </div>
              </div>

              <!-- question 3 -->
              <div class="my-5" v-if="isCompleted[2]">
                <h5 class="mb-4">
                  현재 사용 중인 영화 관련 서비스가 있다면 알려주세요.
                </h5>
                <div class="row">
                  <div
                    class="form-check col-4"
                    v-for="(provider, index) in ottList"
                    :key="index"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      name="question3"
                      :value="provider.provider_id"
                      :id="`answer3-${index + 1}`"
                      v-model="selectedOtts"
                    />
                    <label
                      class="form-check-label"
                      :for="`answer3-${index + 1}`"
                      >{{ provider.provider_name }}</label
                    >
                  </div>
                </div>
              </div>

              <!-- question 4 -->
              <div class="my-5" v-if="isCompleted[3]">
                <h5 class="mb-4">선호하는 영화 장르를 골라주세요 (최대 3개)</h5>
                <div class="row">
                  <div
                    class="form-check col-4"
                    v-for="(genre, index) in genreList"
                    :key="index"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      name="question4"
                      :value="genre.id"
                      :id="`answer4-${index + 1}`"
                      v-model="selectedGenres"
                    />
                    <label
                      class="form-check-label"
                      :for="`answer4-${index + 1}`"
                      >{{ genre.name }}</label
                    >
                  </div>
                </div>
              </div>

              <!-- question 5 -->
              <div class="my-5" v-if="isCompleted[4]">
                <h5 class="mb-4">
                  마지막으로, 다음 중 제일 좋아하는 영화를 하나 골라주세요
                </h5>
                <div class="row">
                  <div
                    class="col-4 form-check"
                    v-for="(movie, index) in surveyList"
                    :key="index"
                  >
                    <input
                      class="form-check-input"
                      type="radio"
                      name="question5"
                      :value="movie.id"
                      :id="`answer5-${index + 1}`"
                      v-model="selectedMovie"
                    />
                    <label
                      class="form-check-label"
                      :for="`answer5-${index + 1}`"
                      >{{ movie.title }}</label
                    >
                  </div>
                </div>
                <button class="mt-4 btn btn-secondary" @click="getList">
                  더 보기
                </button>
              </div>

              <!-- complete -->
              <button @click="submitSurvey" class="mb-5 btn btn-outline-light">
                완료
              </button>
            </div>
          </article>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue"
import { RouterLink, useRouter } from "vue-router"
import { useAccountStore, useMovieStore } from "@/stores/counter"
import axios from "axios"

const accountStore = useAccountStore()
const movieStore = useMovieStore()
const router = useRouter()
const apiKey = import.meta.env.VITE_TMDB_API_KEY
const isCompleted = ref({
  1: true,
  2: true,
  3: true,
  4: true,
  5: true,
})

// ottList and selectedOtts
const ottList = []
const selectedOtts = ref([])

for (const ott in movieStore.ottList) {
  ottList.push({ provider_id: ott, provider_name: movieStore.ottList[ott] })
}

// genreList and selectedGenres
const genreList = []
const selectedGenres = ref([])
for (const genre of movieStore.genres) {
  genreList.push({ id: genre.genre_ids, name: genre.name })
}

const selectedMovie = ref(null)
const surveyList = ref([])

let page = 0
const getList = function () {
  axios({
    method: "GET",
    url: "https://api.themoviedb.org/3/movie/top_rated",
    params: {
      api_key: apiKey,
      language: "ko-KR",
      page: ++page,
    },
  })
    .then((response) => {
      surveyList.value.push(...response.data.results)
    })
    .catch((error) => {
      alert("영화 목록을 가져오는 중 오류가 발생했습니다. [List1]")
      console.error(error)
    })
}

getList()

const submitSurvey = function () {
  if (selectedGenres.value.length === 0) {
    alert("장르를 선택해주세요.")
    return
  }

  if (selectedGenres.value.length > 3) {
    alert("선호 장르는 최대 3개까지 선택 가능합니다.")
    return
  }

  if (selectedMovie.value === null) {
    alert("영화를 선택해주세요.")
    return
  }

  const payload = {
    ott: { ott: selectedOtts.value },
    genre1: selectedGenres.value[0],
    genre2: selectedGenres.value[1],
    genre3: selectedGenres.value[2],
  }

  axios({
    method: "PUT",
    url: `${accountStore.API_URL}/accounts/survey/`,
    data: payload,
    headers: { Authorization: `Token ${accountStore.loginToken}` },
  })
    .then((response) => {
      alert("회원가입이 완료되었습니다.")
      router.push({ name: "MovieListView" })
    })
    .catch((error) => {
      alert("오류가 발생했습니다.")
      console.error(error)
    })
}
</script>

<style scoped>
main {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("@/assets/spiderman_nowayhome.jpg");
  background-size: cover;
}
</style>
