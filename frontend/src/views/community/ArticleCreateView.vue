<template>
  <div id="page">
    <div class="container py-5">
      <div class="container card p-5 bg-light bg-opacity-25">
        <h1 class="mb-3 text-start">게시글 작성</h1>
        <form @submit.prevent="createArticle" class="row g-3">
          <div class="col-md-4">
            <p class="text-start">카테고리</p>
            <select
              name="category"
              id="category"
              v-model="category"
              class="form-select bg-light bg-opacity-50"
              required
            >
              <option value="" disabled selected>
                카테고리를 선택해주세요
              </option>
              <option value="잡담">잡담</option>
              <option value="리뷰">리뷰</option>
              <option value="질문">질문</option>
            </select>
            <div class="invalid-feedback">카테고리를 선택해주세요.</div>
          </div>
          <div class="col-md-8">
            <p class="text-start" v-if="category === '리뷰'">영화 제목</p>
            <input
              v-if="category === '리뷰'"
              type="text"
              name="movie"
              id="movie"
              v-model="movie.title"
              class="form-control bg-light bg-opacity-50"
              placeholder="리뷰 대상 영화 ID 작성"
              :required="category === '리뷰' && !movie"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            />
            <div class="invalid-feedback">영화 ID를 입력해주세요.</div>
          </div>
          <div class="col-md-12">
            <p class="text-start">제목</p>
            <input
              type="text"
              name="title"
              id="title"
              v-model="title"
              class="form-control bg-light bg-opacity-50"
              placeholder="제목을 입력해주세요"
              required
            />
            <div class="invalid-feedback">제목을 입력해주세요.</div>
          </div>
          <div class="col-md-12">
            <p class="text-start">내용</p>
            <textarea
              name="content"
              id="content"
              v-model="content"
              class="form-control bg-light bg-opacity-50"
              rows="5"
              placeholder="내용을 입력해주세요"
              required
            ></textarea>
            <div class="invalid-feedback">내용을 입력해주세요.</div>
          </div>
          <div class="col-md-12">
            <button type="submit" class="btn btn-dark">작성</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal -->
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              영화제목을 검색하세요.
            </h1>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="searchExecute" class="d-flex">
              <input
                type="text"
                v-model="searchingKeyword"
                placeholder="영화 검색"
                class="form-control me-2"
              />
              <button type="submit" class="btn btn-primary">Search</button>
            </form>
            <div v-for="movie in searchResults" :key="movie.movie_id">
              <p
                @click="selectMovie(movie)"
                @mouseover="setPointerCursor"
                :style="{ fontWeight: isSelected(movie) ? 'bold' : 'normal' }"
                class="m-1 border-bottom text-start"
              >
                {{ movie.title }}
              </p>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              닫기
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="saveSelectedMovie"
              data-bs-dismiss="modal"
            >
              영화제목 저장
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import {
  useCommunityStore,
  useAccountStore,
  useMovieStore,
} from "@/stores/counter"
import axios from "axios"

const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const movieStore = useMovieStore()
const router = useRouter()

const category = ref("")
const title = ref("")
const content = ref("")
const movie = ref("")

const createArticle = () => {
  console.log(movie.value)
  if (category.value === "리뷰" && !movie.value) {
    // 영화가 선택되지 않은 경우 유효성 검사 실패
    return
  }

  axios({
    method: "POST",
    url: `${communityStore.API_URL}/community/create/`,
    data: {
      category: category.value,
      title: title.value,
      content: content.value,
      movie: movie.value.id,
    },
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      console.log(response)
      router.push({
        name: "ArticleDetailView",
        params: { articleId: response.data.pk },
      })
    })
    .catch((error) => {
      console.error(error)
    })
}

const searchingKeyword = ref(null)

if (searchingKeyword.value) {
  fetchSearchResults(searchingKeyword.value)
}

const searchResults = ref([])

const fetchSearchResults = (keyword) => {
  axios({
    method: "get",
    url: `${accountStore.API_URL}/movies/search/${keyword}`,
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      searchResults.value = response.data
      console.log(searchResults)
    })
    .catch((error) => {
      alert("검색 결과를 가져오는데 실패했습니다.")
    })
}

const searchExecute = function () {
  if (searchingKeyword.value) {
    fetchSearchResults(searchingKeyword.value)
  }
}
// 클릭한 영화 정보를 저장할 변수
const selectedMovie = ref(null)

// 영화 정보 클릭 이벤트 핸들러
const selectMovie = (movie) => {
  selectedMovie.value = movie
  console.log(selectedMovie.value)
}

// "Save changes" 버튼 클릭 이벤트 핸들러
const saveSelectedMovie = () => {
  // 선택된 영화가 있을 경우에만 실행
  if (selectedMovie.value) {
    // Django에게 외부 API를 호출하도록 요청
    axios({
      method: "GET",
      url: `${movieStore.API_URL}/movies/${selectedMovie.value.movie_id}`, // Django가 외부 API로 요청하는 URL
      headers: {
        Authorization: `Token ${accountStore.loginToken}`,
      },
    })
      .then((response) => {
        // 영화 정보를 성공적으로 받은 경우에만 게시물을 저장
        console.log(response.data)
        if (response.data) {
          movie.value = response.data
        } else {
          // 응답이 없거나 유효한 데이터가 없는 경우 알림
          console.error("No valid movie data received from external API.")
        }
      })
      .catch((error) => {
        // API 호출이 실패한 경우 오류 메시지 출력
        console.error("Failed to retrieve movie data from external API:", error)
      })
  } else {
    // 선택된 영화가 없는 경우 알림
    console.error("No movie selected to save.")
  }
}

const setPointerCursor = () => {
  document.body.style.cursor = "pointer"
}

// 선택된 영화인지 확인하는 메소드
const isSelected = (movie) => {
  return selectedMovie.value === movie
}
</script>

<style scoped>
#page {
  min-height: 100vh;
  background-image: url("@/assets/write.jpg");
  background-size: cover;
}

.text-center {
  text-align: start;
}
</style>
