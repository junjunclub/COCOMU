<template>
  <div class="min-vw-100 bg-dark text-white">
    <div class="container">
      <!-- search engine -->
      <div class="search-form-container">
        <form @submit.prevent="searchExecute" class="d-flex">
          <input
            type="text"
            v-model="searchKeyword"
            placeholder="영화 검색"
            class="form-control me-2 bg-dark text-white"
          />
          <button type="submit" class="btn btn-outline-light">Search</button>
        </form>
      </div>

      <div
        v-if="
          userData.genre1 != null ||
          userData.genre2 != null ||
          userData.genre3 != null
        "
      >
        <h2 class="my-5">꼬꼬무의 추천영화</h2>
        <div class="row relative-parent recommend-movie-container mb-4">
          <div
            class="bg-recommend-movie"
            :style="{
              backgroundImage: `url(https://image.tmdb.org/t/p/w600_and_h900_bestv2${recommendMovie.backdrop_path})`,
              backgroundSize: 'cover',
              filter: 'blur(5px)',
            }"
          ></div>
          <div class="shadow-lg col-md-4 p-0">
            <img
              :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${recommendMovie.backdrop_path}`"
              class="img-fluid recommend-movie-img"
              alt="Movie poster"
              ref="movieImage"
              @load="setGradientBackground"
            />
          </div>
          <div
            class="col-md-8 movie-details mt-md-4 ps-md-5"
          >
            <div class="title-genres d-flex align-items-center border-bottom">
              <h3
                class="me-3 mix-blend-difference fs-lg-5 recommend-title fs-1"
              >
                {{ recommendMovie.title }}
              </h3>

              <div class="genres">
                <span
                  v-for="(genre, index) in recommendMovie.genres"
                  :key="index"
                  class="badge bg-dark me-1"
                  >{{ genre.name }}</span
                >
              </div>
            </div>
            <div
              class="d-flex align-items-center justify-content-center mt-3"
              style="
                position: absolute;
                top: 50%;
                left: 66%;
                transform: translate(-50%, -50%);
              "
            >
              <RouterLink
                class="btn btn-dark me-2"
                :to="{
                  name: 'MovieDetailView',
                  params: { movieId: recommendMovie.movie_id },
                }"
              >
                상세 정보 보기
              </RouterLink>
              <button
                class="btn btn-dark"
                @click="likeMovie(recommendMovie.movie_id)"
              >
                {{ isLiked ? "찜 목록에서 제거" : "찜 목록에 추가" }}
              </button>
            </div>
          </div>
        </div>

        <h2 class="my-5">좋아하는 장르 기반의 추천 영화</h2>

        <div v-if="genreNames[0]">
          <h3 class="text-start my-4">{{ genreNames[0] }} 장르 추천 목록</h3>
          <div class="row d-flex justify-content-between">
            <div
              v-for="movie in displayedMovies1"
              :key="movie.movie_id"
              class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
              style="width: 18rem; padding: 0"
            >
              <MovieCard :movie="movie" />
            </div>
          </div>
          <button
            v-if="displayedMovies1.length < suggestedMovies1.length"
            @click="loadMoreMovies1"
            class="btn btn-secondary"
          >
            더보기
          </button>
        </div>

        <div v-if="genreNames[1]">
          <h3 class="text-start my-4">{{ genreNames[1] }} 장르 추천 목록</h3>
          <div class="row d-flex justify-content-between">
            <div
              v-for="movie in displayedMovies2"
              :key="movie.movie_id"
              class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
              style="width: 18rem; padding: 0"
            >
              <MovieCard :movie="movie" />
            </div>
          </div>
          <button
            v-if="displayedMovies2.length < suggestedMovies2.length"
            @click="loadMoreMovies2"
            class="btn btn-secondary"
          >
            더보기
          </button>
        </div>
        <div v-if="genreNames[2]">
          <h3 class="text-start my-4">{{ genreNames[2] }} 장르 추천 목록</h3>
          <div class="row d-flex justify-content-between">
            <div
              v-for="movie in displayedMovies3"
              :key="movie.movie_id"
              class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
              style="width: 18rem; padding: 0"
            >
              <MovieCard :movie="movie" />
            </div>
          </div>
          <button
            v-if="displayedMovies3.length < suggestedMovies3.length"
            @click="loadMoreMovies3"
            class="btn btn-secondary"
          >
            더보기
          </button>
        </div>

        <h3 class="text-start my-4">{{ randomGenre }} 장르 추천 목록</h3>
        <div class="row d-flex justify-content-between">
          <div
            v-for="movie in displayedMovies4"
            :key="movie.movie_id"
            class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
            style="width: 18rem; padding: 0"
          >
            <MovieCard :movie="movie" />
          </div>
        </div>
        <button
          v-if="displayedMovies4.length < randomMovies.length"
          @click="loadMoreMovies4"
          class="btn btn-secondary"
        >
          더보기
        </button>
      </div>
      <div v-else>
        <p>선호하는 장르가 없어요. 설정해주세요.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRouter, useRoute, RouterLink } from "vue-router"
import { useMovieStore, useAccountStore } from "@/stores/counter"
import axios from "axios"
import MovieCard from "@/components/MovieCard.vue"
import { shuffle } from "lodash"

const router = useRouter()
const route = useRoute()
const movieStore = useMovieStore()
const accountStore = useAccountStore()

const isLiked = ref(false)

const movies = ref(null)
const suggestedMovies1 = ref([])
const suggestedMovies2 = ref([])
const suggestedMovies3 = ref([])
const randomMovies = ref([])

const displayedMovies1 = ref([])
const displayedCount1 = ref(5)

const displayedMovies2 = ref([])
const displayedCount2 = ref(5)

const displayedMovies3 = ref([])
const displayedCount3 = ref(5)

const displayedMovies4 = ref([])
const displayedCount4 = ref(5)

const genreNames = ref(["", "", ""])
const randomGenre = ref("")
const recommendMovie = ref(null)

const userData = ref(null)
const userDataPromise = accountStore.getUserInfo()
userDataPromise.then((data) => {
  userData.value = data

  axios({
    method: "GET",
    url: `${movieStore.API_URL}/movies/`,
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      movies.value = response.data
      console.log(movies)
      const shuffleMovie = shuffle(movies.value)
      recommendMovie.value = shuffleMovie[77]
      const genresMap = response.data.reduce((map, movie) => {
        movie.genres.forEach((genre) => {
          map[genre.id] = genre.name
        })
        return map
      }, {})

      accountStore.getUserInfo().then((data) => {
        isLiked.value = recommendMovie.value.like_user.includes(data.id)
      })

      const userGenre = [
        userData.value.genre1,
        userData.value.genre2,
        userData.value.genre3,
      ]

      const userGenreFiltered = userGenre.filter((genre) => genre !== null)

      if (userGenreFiltered[0] !== undefined) {
        genreNames.value[0] = genresMap[userGenreFiltered[0]]
        suggestedMovies1.value = movies.value.filter((movie) => {
          return movie.genres.some((genre) => genre.id === userGenreFiltered[0])
        })
        displayedMovies1.value = suggestedMovies1.value.slice(
          0,
          displayedCount1.value
        )
      }

      if (userGenreFiltered[1] !== undefined) {
        genreNames.value[1] = genresMap[userGenreFiltered[1]]
        suggestedMovies2.value = movies.value.filter((movie) => {
          return movie.genres.some((genre) => genre.id === userGenreFiltered[1])
        })
        displayedMovies2.value = suggestedMovies2.value.slice(
          0,
          displayedCount2.value
        )
      }

      if (userGenreFiltered[2] !== undefined) {
        genreNames.value[2] = genresMap[userGenreFiltered[2]]
        suggestedMovies3.value = movies.value.filter((movie) => {
          return movie.genres.some((genre) => genre.id === userGenreFiltered[2])
        })
        displayedMovies3.value = suggestedMovies3.value.slice(
          0,
          displayedCount3.value
        )
      }

      const randomGenres = function () {
        const filteredGenre = movieStore.genres.filter((elem) => {
          return !genreNames.value.includes(elem.name)
        })
        const shuffledGenre = shuffle(filteredGenre)

        return shuffledGenre
      }

      randomGenre.value = randomGenres()[0].name

      if (randomGenre.value !== undefined) {
        randomMovies.value = movies.value.filter((movie) => {
          return movie.genres.some((genre) => genre.name === randomGenre.value)
        })
        displayedMovies4.value = randomMovies.value.slice(
          0,
          displayedCount4.value
        )
      }

      displayedMovies1.value = shuffle(displayedMovies1.value)
      displayedMovies2.value = shuffle(displayedMovies2.value)
      displayedMovies3.value = shuffle(displayedMovies3.value)
      displayedMovies4.value = shuffle(displayedMovies4.value)
    })
    .catch((error) => console.log(error))
})

const loadMoreMovies1 = () => {
  displayedCount1.value += 5
  displayedMovies1.value = suggestedMovies1.value.slice(
    0,
    displayedCount1.value
  )
}

const loadMoreMovies2 = () => {
  displayedCount2.value += 5
  displayedMovies2.value = suggestedMovies2.value.slice(
    0,
    displayedCount2.value
  )
}

const loadMoreMovies3 = () => {
  displayedCount3.value += 5
  displayedMovies3.value = suggestedMovies3.value.slice(
    0,
    displayedCount3.value
  )
}

const loadMoreMovies4 = () => {
  displayedCount4.value += 5
  displayedMovies4.value = randomMovies.value.slice(0, displayedCount4.value)
}

const searchKeyword = ref(null)
const searchExecute = function () {
  router.push({
    name: "MovieSearchView",
    query: { keyword: searchKeyword.value },
  })
}

watch(
  () => route.query.keyword,
  (newKeyword) => {
    if (newKeyword) {
      searchKeyword.value = newKeyword
      fetchSearchResults(newKeyword)
    }
  }
)

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

const likeMovie = function (movieId) {
  movieStore.likeMovie(movieId)
  isLiked.value = !isLiked.value
}
</script>

<style scoped>
.container {
  overflow: auto;
  max-width: 90%;
  margin: 0 auto;
}

.relative-parent {
  position: relative;
  z-index: 3;
}

.mix-blend-difference {
  color: white;
  mix-blend-mode: difference;
}

.bg-recommend-movie {
  width: 100%;
  height: 100%;
  position: absolute;
  background-position: center;
  z-index: -1;
}

.search-form-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.form-control {
  margin-right: 0.5rem;
}

.recommend-movie-container {
  display: flex;
  align-items: flex-start;
}

.recommend-movie-img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}

.movie-details {
  display: flex;
  flex-direction: column;
}

.title-genres {
  display: flex;
  align-items: center;
}

.title-genres h3 {
  margin: 0;
}

.genres .badge {
  margin-right: 5px;
}

.button-container {
  margin-top: auto;
}

.button-container .btn {
  margin-bottom: 0.5rem;
}

.recommend-title {
  text-shadow: 0px 0px 20px rgb(211, 211, 211);
}

::placeholder {
  color: #cdcdcd;
}
</style>
