import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"
// accounts pages
import SignUpView from "@/views/accounts/SignUpView.vue"
import FirstSurveyView from "@/views/accounts/FirstSurveyView.vue"
import SecondSurveyView from "@/views/accounts/SecondSurveyView.vue"
import LoginView from "@/views/accounts/LoginView.vue"
import ProfileView from "@/views/accounts/ProfileView.vue"
import SignOutView from "@/views/accounts/SignOutView.vue"
import ProfileUpdateView from "@/views/accounts/ProfileUpdateView.vue"
import BookmarkView from "@/views/accounts/BookmarkView.vue"
// movies pages
import MovieListView from "@/views/movies/MovieListView.vue"
import MovieDetailView from "@/views/movies/MovieDetailView.vue"
import MovieSearchView from "@/views/movies/MovieSearchView.vue"
// reviews pages
import ArticleListView from "@/views/community/ArticleListView.vue"
import ArticleDetailView from "@/views/community/ArticleDetailView.vue"
import ArticleCreateView from "@/views/community/ArticleCreateView.vue"
import ArticleUpdateView from "@/views/community/ArticleUpdateView.vue"

// import { getActivePinia } from "pinia"
import { useAccountStore } from "@/stores/counter"

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "HomeView",
            component: HomeView,
        },
        {
            path: "/accounts",
            children: [
                {
                    path: "signup",
                    name: "SignUpView",
                    component: SignUpView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (accountStore.loginToken) {
                            alert("이미 로그인 되어 있습니다.")
                            return "/"
                        }
                    },
                },
                {
                    path: "signup/survey",
                    name: "FirstSurveyView",
                    component: FirstSurveyView,
                    beforeEnter: (to, from) => {
                        console.log(from.path)
                        const accountStore = useAccountStore()
                        if (from.path !== "/accounts/signup") {
                            alert("잘못된 접근입니다.")
                            return "/"
                        }
                    },
                },
                {
                    path: "login",
                    name: "LoginView",
                    component: LoginView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (accountStore.loginToken) {
                            alert("이미 로그인 되어 있습니다.")
                            return "/"
                        }
                    },
                },
                {
                    path: "profile",
                    name: "ProfileView",
                    component: ProfileView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (!accountStore.loginToken) {
                            alert("로그인이 필요한 서비스입니다.")
                            return "/accounts/login"
                        }
                    },
                },
                {
                    path: "survey",
                    name: "SecondSurveyView",
                    component: SecondSurveyView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (!accountStore.loginToken) {
                            alert("로그인이 필요한 서비스입니다.")
                            return "/accounts/login"
                        }
                    },
                },
                {
                    path: "update",
                    name: "ProfileUpdateView",
                    component: ProfileUpdateView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (!accountStore.loginToken) {
                            alert("로그인이 필요한 서비스입니다.")
                            return "/accounts/login"
                        }
                    },
                },
                {
                    path: "signout",
                    name: "SignOutView",
                    component: SignOutView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (!accountStore.loginToken) {
                            alert("로그인이 필요한 서비스입니다.")
                            return "/accounts/login"
                        }
                    },
                },
                {
                    path: "bookmark",
                    name: "BookmarkView",
                    component: BookmarkView,
                    beforeEnter: (to, from) => {
                        const accountStore = useAccountStore()
                        if (!accountStore.loginToken) {
                            alert("로그인이 필요한 서비스입니다.")
                            return "/accounts/login"
                        }
                    },
                },
            ],
        },
        {
            path: "/movies",
            children: [
                {
                    path: "",
                    name: "MovieListView",
                    component: MovieListView,
                },
                {
                    path: ":movieId",
                    name: "MovieDetailView",
                    component: MovieDetailView,
                },
                {
                    path: "search",
                    name: "MovieSearchView",
                    component: MovieSearchView,
                },
            ],
            beforeEnter: (to, from) => {
                const accountStore = useAccountStore()
                if (!accountStore.loginToken) {
                    alert("로그인이 필요한 서비스입니다.")
                    return "/accounts/login"
                }
            },
        },
        {
            path: "/community",
            children: [
                {
                    path: "",
                    name: "ArticleListView",
                    component: ArticleListView,
                },
                {
                    path: ":articleId",
                    name: "ArticleDetailView",
                    component: ArticleDetailView,
                },
                {
                    path: "create",
                    name: "ArticleCreateView",
                    component: ArticleCreateView,
                },
                {
                    path: "update",
                    name: "ArticleUpdateView",
                    component: ArticleUpdateView,
                },
            ],
            beforeEnter: (to, from) => {
                const accountStore = useAccountStore()
                if (!accountStore.loginToken) {
                    alert("로그인이 필요한 서비스입니다.")
                    return "/accounts/login"
                }
            },
        },
    ],
})

export default router
