<template>
  <div class="min-vh-100 bg-profile">
    <div class="min-vh-100" v-if="article">
      <div class="min-vh-100 d-flex justify-content-center align-items-center">
        <section class="card w-75 h-75 p-5 bg-dark bg-opacity-75 text-white">
          <div class="d-flex justify-content-between align-items-center">
            <h1 class="text-start mb-3">{{ article.title }}</h1>
            <!-- {{ article }} -->
          </div>
          <div class="text-start fs-5" v-if="article.movie">
            <RouterLink
              class="text-white-50 no-underline fw-blod"
              :to="{
                name: 'MovieDetailView',
                params: { movieId: reviewMovie.movie_id },
              }"
            >
              {{ reviewMovie.title }} </RouterLink
            >에 대한 리뷰에요
          </div>

          <article class="mt-2">
            <div class="text-start">
              <span class="text-start me-3">작성자</span>
              <span class="text-white-50 mb-3">{{
                article.user.nickname
              }}</span>
            </div>

            <div class="text-start">
              <span class="me-3">작성 시간</span>
              <span class="text-white-50 mb-3">{{
                formatDate(article.created_at)
              }}</span>
            </div>
            <div class="text-start">
              <span class="me-3">최종 수정</span>
              <span class="text-white-50 mb-3">{{
                formatDate(article.updated_at)
              }}</span>
            </div>
            <div class="row my-3">
              <div class="text-start fs-3">{{ article.content }}</div>
            </div>
            <div class="text-end">
              <RouterLink
                :to="{ name: 'ArticleListView' }"
                class="btn btn-outline-secondary d-inline-block"
                >목록</RouterLink
              >
              <div
                v-if="accountStore.loginUser === article.user.username"
                class="d-inline"
              >
                <RouterLink
                  :to="{
                    name: 'ArticleUpdateView',
                    query: { articleId: article.pk },
                  }"
                  class="btn btn-outline-secondary ms-3"
                >
                  수정
                </RouterLink>
                <button
                  @click="deleteArticle"
                  class="btn btn-outline-danger ms-3"
                >
                  삭제
                </button>
              </div>
            </div>
            <div class="row mb-3">
              <span class="col text-start mb-3">댓글</span>
              <!-- comment creation -->
              <div>
                <form @submit.prevent="createComment" class="mb-3">
                  <textarea
                    v-model="commentContent"
                    class="form-control mb-3 bg-transparent text-white"
                    rows="3"
                    placeholder="댓글을 입력해주세요"
                  ></textarea>
                  <div class="text-end">
                    <button type="submit" class="btn btn-outline-light">
                      덧글 작성
                    </button>
                  </div>
                </form>
              </div>
              <div class="text-start">
                <!-- comment area -->
                <div v-if="article.comments.length > 0">
                  <div
                    v-for="(comment, index) in article.comments"
                    :key="index"
                  >
                    <div
                      class="d-flex justify-content-between align-items-center"
                    >
                      <span
                        >{{ comment["user"]["nickname"] }} :
                        {{ comment.content }}</span
                      >
                      <div
                        class="text-end"
                        v-if="accountStore.loginUser === comment.user.username"
                      >
                        <button
                          @click="updateComment(comment.pk, comment.content)"
                          class="btn btn-outline-secondary mx-3"
                          style="
                            --bs-btn-padding-y: 0.25rem;
                            --bs-btn-padding-x: 0.5rem;
                          "
                        >
                          수정
                        </button>
                        <button
                          @click="deleteComment(comment.pk)"
                          class="btn btn-outline-danger"
                          style="
                            --bs-btn-padding-y: 0.25rem;
                            --bs-btn-padding-x: 0.5rem;
                          "
                        >
                          삭제
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </section>
        <hr />
      </div>
    </div>
    <div v-else>댓글이 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRoute, useRouter, RouterLink } from "vue-router"
import { useCommunityStore, useAccountStore } from "@/stores/counter"
import axios from "axios"

const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()
const articleId = ref(route.params.articleId)

const currentUser = computed(() => accountStore.currentUser)
console.log(accountStore.loginUser)
console.log(currentUser)

// load article
const article = ref(null)
const reviewMovie = ref(null)
const articlePromise = ref(communityStore.getArticleDetail(articleId.value))
articlePromise.value.then((response) => {
  console.log(response)
  article.value = response

  if (response.movie) {
    axios({
      method: "get",
      url: `${communityStore.API_URL}/movies/searchpk/${response.movie}/`,
      headers: {
        Authorization: `Token ${accountStore.loginToken}`,
      },
    })
      .then((response) => {
        reviewMovie.value = response.data
      })
      .catch((error) => console.error(error))
  }
})

// deleteArticle
const deleteArticle = function () {
  const deleteConfirm = confirm("정말 삭제하시겠습니까?")

  if (deleteConfirm) {
    communityStore.deleteArticle(articleId.value)
  }
}

// createComment
const commentContent = ref(null)
const createComment = function () {
  axios({
    method: "POST",
    url: `${communityStore.API_URL}/community/${articleId.value}/comment_create/`,
    headers: {
      Authorization: `Token ${accountStore.loginToken}`,
    },
    data: {
      content: commentContent.value,
    },
  })
    .then((response) => {
      console.log(response.data)
      article.value.comments.push(response.data)
      commentContent.value = null
    })
    .catch((error) => console.error(error))
}

// deleteComment
const deleteComment = function (commentId) {
  const confirmDelete = confirm("정말 삭제하시겠습니까?")
  if (confirmDelete) {
    axios({
      method: "delete",
      url: `${communityStore.API_URL}/community/${articleId.value}/${commentId}/comment_delete/`,
      headers: {
        Authorization: `Token ${accountStore.loginToken}`,
      },
    })
      .then((response) => {
        article.value.comments = article.value.comments.filter(
          (comment) => comment.pk !== commentId
        )
      })
      .catch((error) => console.error(error))
  }
}

// updateComment
const updateComment = function (commentId, originalContent) {
  const updateContent = prompt("수정할 내용을 입력해주세요.", originalContent)

  // 공백만 있는 것들을 전부 뭉뚱그려서 처리할 수 있으면 그렇게 하기
  if (
    updateContent != null &&
    updateContent != "" &&
    updateContent != originalContent
  ) {
    axios({
      method: "put",
      url: `${communityStore.API_URL}/community/${articleId.value}/${commentId}/comment_update/`,
      headers: {
        Authorization: `Token ${accountStore.loginToken}`,
      },
      data: {
        content: updateContent,
      },
    })
      .then((response) => {
        article.value.comments = article.value.comments.map((comment) => {
          if (comment.pk === commentId) {
            comment.content = updateContent
          }
          return comment
        })
      })
      .catch((error) => console.error(error))
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}
</script>

<style scoped>
.bg-profile {
  background-image: url("@/assets/mainpageticketimage.jpg");
}

.signout-link {
  text-decoration: none;
}

.no-underline {
  text-decoration: none;
}

::placeholder {
  color: grey;
}
</style>
