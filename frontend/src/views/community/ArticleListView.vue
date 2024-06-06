<template>
  <header class="bg-dark bg-opacity-50 text-white">
    <div class="container my-5" id="bgimg">
      <h1 class="text-start mb-4 text-white">Community</h1>
      <div v-if="paginatedArticles.length > 0">
        <table class="table table-dark table-hover rounded-3 overflow-hidden">
          <thead>
            <tr>
              <th scope="col">카테고리</th>
              <th scope="col">제목</th>
              <th scope="col">작성자</th>
              <th scope="col">작성일자</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(article, index) in paginatedArticles" :key="index">
              <td>{{ article.category }}</td>
              <td>
                <RouterLink
                  :to="{
                    name: 'ArticleDetailView',
                    params: { articleId: article.pk },
                  }"
                  class="text-white"
                >
                  {{ article.title }}
                </RouterLink>
              </td>
              <td>{{ article.user["nickname"] }}</td>
              <td>{{ formatDate(article.created_at) }}</td>
            </tr>
          </tbody>
        </table>

        <nav aria-label="Page navigation" class="pag">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a
                class="page-link"
                href="#"
                @click.prevent="changePage(currentPage - 1)"
                >Previous</a
              >
            </li>
            <li
              v-for="page in totalPages"
              :key="page"
              class="page-item"
              :class="{ active: currentPage === page }"
            >
              <a class="page-link" href="#" @click.prevent="changePage(page)">{{
                page
              }}</a>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentPage === totalPages }"
            >
              <a
                class="page-link"
                href="#"
                @click.prevent="changePage(currentPage + 1)"
                >Next</a
              >
            </li>
          </ul>
        </nav>
      </div>
      <div v-else class="alert alert-warning">
        첫번째 게시글을 작성해주세요!
      </div>
      <div v-if="accountStore.loginToken" class="text-end mt-4">
        <RouterLink
          class="btn btn-outline-light write"
          :to="{ name: 'ArticleCreateView' }"
        >
          글쓰기
        </RouterLink>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from "vue"
import { RouterLink } from "vue-router"
import { useCommunityStore, useAccountStore } from "@/stores/counter"
import axios from "axios"
import dayjs from 'dayjs'

const now = dayjs()


const communityStore = useCommunityStore()
const accountStore = useAccountStore()

const articles = ref([])
const currentPage = ref(1)
const itemsPerPage = 10

axios({
  method: "GET",
  url: `${communityStore.API_URL}/community/`,
  headers: {
    Authorization: `Token ${accountStore.loginToken}`,
  },
})
  .then((response) => {
    articles.value = response.data
    console.log(now)
  })
  .catch((error) => {
    console.error(error)
  })

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const totalPages = computed(() =>
  Math.ceil(articles.value.length / itemsPerPage)
)

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return articles.value.slice(start, end)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>

<style scoped>
header {
  position: relative;
  background-image: url("@/assets/sen.jpg");
  background-size: cover;
  min-height: 100vh;
  z-index: 1;
}
header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8); /* 어두운 오버레이 추가 */
  z-index: 2;
}
.container {
  position: relative;
  z-index: 3; /* 컨테이너의 z-index를 오버레이보다 높게 설정 */
  max-width: 1000px;
  margin: 0 auto;
  min-height: 750px;
  opacity: 1;
}
.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
  border-collapse: collapse;
}
/* .table tr {
  border: 1px solid #dee2e6;
} */
/* .table th,
.table td {
  padding: 0.75rem;
  vertical-align: top;
  color: white;
} */
/* .table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #dee2e6;
} */
/* .table tbody {
  border-top: 2px solid #dee2e6;
} */

/* .table td {
  padding: 0.5rem;
  border: none;
  border-bottom: 1px solid #dee2e6;
} */
.pagination {
  margin: 0;
}
.pagination .page-item.disabled .page-link {
  pointer-events: none;
  color: #6c757d;
  background-color: #5c5c5c33;
  border: none;
}
.pagination .page-item.active .page-link {
  z-index: 1;
  color: #fff;
  background-color: #929292a8; /* Active page color to black */
  border: none;
}
.pagination .page-link {
  color: #000; /* Page link color to black */
  text-decoration: none;
  background-color: #fff;
  border: 1px solid #dee2e6;
}
.write {
  margin-left: 20px;
  padding: 10px 20px;
  /* color: white; */
  cursor: pointer;
}

table tr td,
table tr th {
  background-color: rgba(0, 0, 0, 0.3) !important;
}
</style>
