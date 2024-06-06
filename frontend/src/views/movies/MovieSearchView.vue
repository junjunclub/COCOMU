<template>
  <div class="min-vh-100 container bg-dark text-white">
    <div class="search-form-container">
      <form @submit.prevent="searchExecute" class="d-flex">
        <input
          type="text"
          v-model="searchingKeyword"
          placeholder="영화 검색"
          class="form-control me-2 bg-transparent text-white"
        />
        <button type="submit" class="btn btn-outline-light">Search</button>
      </form>
    </div>
    <div class="mb-5">{{ searchedKeyword }}에 대한 검색결과입니다.</div>
    <!-- let got searchResult Array form -->
    <div class="row d-flex justify-content-evenly">
      <div
        v-for="movie in searchResult"
        :key="movie.movie_id"
        class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
        style="width: 18rem; padding: 0"
      >
        <MovieCard :movie="movie" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAccountStore } from "@/stores/counter"
import MovieCard from "@/components/MovieCard.vue"
import axios from "axios"

const tmdbKey = import.meta.env.VITE_TMDB_API_KEY
const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const searchedKeyword = ref(route.query.keyword)
const searchResult = ref([])

const fetchSearchResults = (keyword) => {
  axios({
    method: "get",
    url: `${accountStore.API_URL}/movies/search/${keyword}`,
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      searchResult.value = response.data
    })
    .catch((error) => {
      alert("검색 결과를 가져오는데 실패했습니다.")
    })
}

if (searchedKeyword.value) {
  fetchSearchResults(searchedKeyword.value)
}

const searchingKeyword = ref(null)
const searchExecute = function () {
  router.push({
    name: "MovieSearchView",
    query: { keyword: searchingKeyword.value },
  })
}

watch(
  () => route.query.keyword,
  (newKeyword) => {
    searchedKeyword.value = newKeyword
    if (newKeyword) {
      fetchSearchResults(newKeyword)
    }
  }
)
</script>

<style scoped>
.search-form-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

::placeholder {
  color: gray;
}
</style>
