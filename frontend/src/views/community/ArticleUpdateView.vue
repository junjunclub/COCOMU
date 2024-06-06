<template>
  <div class="min-vh-100 container py-5" id="page">
    <div class="container card p-5 bg-light bg-opacity-25">
      <h1 class="mb-3 text-start">게시글 수정</h1>
      <form @submit.prevent="updateArticle" class="row g-3">
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
          <p>{{ article }}</p>
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
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
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
const route = useRoute()
console.log(route.params)
const article = ref(null)

console.log(route.query.articleId)

const category = ref(null)
const title = ref(null)
const content = ref(null)
const movie = ref(null)
const articleId = ref(route.query.articleId)

const reviewMovie = ref(null)
const articlePromise = ref(communityStore.getArticleDetail(articleId.value))
articlePromise.value.then((response) => {
  console.log(response)
  article.value = response

  category.value = response.category
  title.value = response.title
  content.value = response.content
  movie.value = response.movie
})

const searchingKeyword = ref(null)
onMounted(() => {
  communityStore.getArticleDetail(articleId.value).then((response) => {
    article.value = response
  })
})

// if (article.value.movie) {
//   axios({
//     method: "get",
//     url: `${movieStore.API_URL}/movies/searchpk/${article.value.movie.id}/`,
//     headers: {
//       Authorization: `Token ${accountStore.loginToken}`,
//     },
//   }).then((response) => {
//     movie.value = response.data
//   })
// }
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
  selectedMovie.title
  console.log(selectedMovie.value)
}

// "Save changes" 버튼 클릭 이벤트 핸들러
const saveSelectedMovie = () => {
  // 선택된 영화가 있을 경우에만 실행
  if (selectedMovie.value) {
    // Django에게 외부 API를 호출하도록 요청
    axios({
      method: "GET",
      url: `${movieStore.API_URL}/movies/${selectedMovie.value.id}`, // Django가 외부 API로 요청하는 URL
      headers: {
        Authorization: `Token ${accountStore.loginToken}`,
      },
    })
      .then((response) => {
        // 영화 정보를 성공적으로 받은 경우에만 게시물을 저장
        if (response.data) {
          // 영화 정보를 저장하고 게시물을 생성
          movie.value = response.data
          createArticle()
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

const updateArticle = function () {
  axios({
    method: "PUT",
    url: `${communityStore.API_URL}/community/${articleId.value}/update/`,
    data: {
      category: category.value,
      title: title.value,
      content: content.value,
      movie: movie.value,
    },
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
  })
    .then((response) => {
      router.push({
        name: "ArticleDetailView",
        params: { articleId: articleId.value },
      })
    })
    .catch((error) => {
      console.log(articleId.value)
      console.error(error)
    })
}
</script>

<style scoped>
#page {
  background-image: url("@/assets/write.jpg");
  background-size: cover;
}
</style>
