import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { defineStore } from "pinia"
import axios from "axios"
import { forIn } from "lodash"

export const useCounterStore = defineStore("counter", () => {
    const count = ref(0)
    const doubleCount = computed(() => count.value * 2)
    function increment() {
        count.value++
    }

    return { count, doubleCount, increment }
})

export const useAccountStore = defineStore(
    "account",
    () => {
        const router = useRouter()

        const API_URL = "http://127.0.0.1:8000"
        const loginToken = ref(null)
        const loginUser = ref(null)

        // 회원가입
        const signUp = function (payload) {
            const username = payload.username
            const password1 = payload.password1
            const password2 = payload.password2
            const name = payload.name
            const email = payload.email
            const nickname = payload.nickname
            const birth = payload.birth

            if (password1 !== password2) {
                alert("비밀번호 확인이 일치하지 않습니다.")
                return
            }

            axios({
                method: "POST",
                url: `${API_URL}/accounts/signup/`,
                data: {
                    username,
                    password1,
                    password2,
                    name,
                    email,
                    nickname,
                    birth,
                },
            })
                .then((response) => {
                    // 회원가입 성공시 설문조사 페이지로 이행
                    const password = password1
                    signUpLogin({ username, password })
                    router.push({ name: "FirstSurveyView" })
                })
                .catch((error) => {
                    const errorMessages = new Set()
                    const alertMessage = error.response.data
                    console.log(alertMessage)
                    for (const messages in alertMessage) {
                        for (const message of alertMessage[messages]) {
                            if (message === "This field may not be null.") {
                                errorMessages.add("모든 항목을 입력해주세요.")
                            } else if (
                                message === "Enter a valid email address."
                            ) {
                                errorMessages.add("이메일 형식을 확인해주세요.")
                            } else if (
                                message ===
                                "A user with that username already exists."
                            ) {
                                errorMessages.add("이미 존재하는 아이디입니다.")
                            } else {
                                errorMessages.add(message)
                            }
                        }
                    }
                    for (const message of errorMessages) {
                        alert(message)
                    }
                })
        }

        // 설문조사
        // 변수명 BE에 들어가는 이름으로 수정해야할듯
        const survey = function (payload) {
            const selectedOTT = payload.question3
            const selectedGenres = payload.question4
            const selectedMovie = payload.question5

            axios({
                method: "PUT",
                url: `${API_URL}/accounts/survey/`,
                data: {
                    selectedOTT,
                    selectedGenres,
                    selectedMovie,
                },
            })
                .then((response) => {
                    console.log(response.data)
                    // 설문조사 완료시 메인 페이지로 이행
                    router.push({ name: "MovieListView" })
                })
                .catch((error) => {
                    alert("오류가 발생했습니다.")
                    console.log(error)
                })
        }

        // 로그인
        const login = function (payload) {
            const username = payload.username
            const password = payload.password

            axios({
                method: "POST",
                url: `${API_URL}/accounts/login/`,
                data: {
                    username,
                    password,
                },
            })
                .then((response) => {
                    // 로그인 성공시 토큰 저장
                    loginToken.value = response.data.key
                    loginUser.value = username
                    console.log(response.data)
                    alert("로그인 되었습니다.")
                    router.push({ name: "HomeView" })
                })
                .catch((error) => {
                    console.log(error)
                    // 로그인 실패시 경고창
                    alert("아이디 또는 비밀번호가 틀렸습니다.")
                })
        }

        const signUpLogin = function (payload) {
            const username = payload.username
            const password = payload.password

            axios({
                method: "POST",
                url: `${API_URL}/accounts/login/`,
                data: {
                    username,
                    password,
                },
            })
                .then((response) => {
                    // 로그인 성공시 토큰 저장
                    loginToken.value = response.data.key
                    loginUser.value = username
                    console.log(response.data)
                })
                .catch((error) => {
                    console.log(error)
                    // 로그인 실패시 경고창
                    alert("아이디 또는 비밀번호가 틀렸습니다.")
                })
        }

        // 회원탈퇴
        const signOut = function () {
            axios({
                method: "DELETE",
                url: `${API_URL}/accounts/profile/delete/`,
                headers: {
                    Authorization: `Token ${loginToken.value}`,
                },
            })
                .then((response) => {
                    // 회원탈퇴 성공시 메인 페이지로 이행
                    loginToken.value = null
                    loginUser.value = null
                    router.push({ name: "HomeView" })
                })
                .catch((error) => console.log(error))
        }

        // 로그아웃
        const logout = function () {
            loginToken.value = null
            loginUser.value = null
            axios({
                method: "POST",
                url: `${API_URL}/accounts/logout/`,
            })
                .then((response) => {
                    router.push({ name: "HomeView" })
                })
                .catch((error) => console.log(error))
        }

        // 로그인 유저 정보
        const getUserInfo = function () {
            return axios({
                method: "GET",
                url: `${API_URL}/accounts/profile/`,
                headers: {
                    Authorization: `Token ${loginToken.value}`,
                },
            })
                .then((response) => {
                    return response.data
                })
                .catch((error) => console.log(error))
        }

        const updateUserInfo = function (payload) {
            const name = payload.name
            const email = payload.email
            const nickname = payload.nickname
            const birth = payload.birth

            axios({
                method: "PUT",
                url: `${API_URL}/accounts/profile/update/`,
                headers: {
                    Authorization: `Token ${loginToken.value}`,
                },
                data: {
                    name,
                    email,
                    nickname,
                    birth,
                },
            })
                .then((response) => {
                    router.push({ name: "ProfileView" })
                })
                .catch((error) =>
                    alert(
                        "오류가 발생했습니다. 입력 내용이 없거나 부적절한 문자를 사용했거나 너무 길지 않은지 확인해주세요."
                    )
                )
        }

        return {
            API_URL,
            loginToken,
            loginUser,
            signUp,
            survey,
            login,
            logout,
            signOut,
            getUserInfo,
            updateUserInfo,
        }
    },
    { persist: true }
)

export const useCommunityStore = defineStore("community", () => {
    const router = useRouter()
    const accountStore = useAccountStore()

    const API_URL = "http://127.0.0.1:8000"

    const getArticleDetail = function (articleId) {
        return axios({
            method: "GET",
            url: `${API_URL}/community/${articleId}`,
            headers: {
                Authorization: `Token ${accountStore.loginToken}`,
            },
        })
            .then((response) => {
                return response.data
            })
            .catch((error) => console.log(error))
    }

    const deleteArticle = function (articleId) {
        axios({
            method: "DELETE",
            url: `${API_URL}/community/${articleId}/delete/`,
            headers: {
                Authorization: `Token ${accountStore.loginToken}`,
            },
        })
            .then((response) => {
                router.push({ name: "ArticleListView" })
            })
            .catch((error) => console.log(error))
    }

    return { API_URL, getArticleDetail, deleteArticle }
})

export const useMovieStore = defineStore("movie", () => {
    const API_URL = "http://127.0.0.1:8000"
    const accountStore = useAccountStore()
    const genres = [
        {
            genre_ids: 28,
            name: "액션",
        },
        {
            genre_ids: 12,
            name: "모험",
        },
        {
            genre_ids: 16,
            name: "애니메이션",
        },
        {
            genre_ids: 35,
            name: "코미디",
        },
        {
            genre_ids: 80,
            name: "범죄",
        },
        {
            genre_ids: 99,
            name: "다큐멘터리",
        },
        {
            genre_ids: 18,
            name: "드라마",
        },
        {
            genre_ids: 10751,
            name: "가족",
        },
        {
            genre_ids: 14,
            name: "판타지",
        },
        {
            genre_ids: 36,
            name: "역사",
        },
        {
            genre_ids: 27,
            name: "공포",
        },
        {
            genre_ids: 10402,
            name: "음악",
        },
        {
            genre_ids: 9648,
            name: "미스터리",
        },
        {
            genre_ids: 10749,
            name: "로맨스",
        },
        {
            genre_ids: 878,
            name: "SF",
        },
        {
            genre_ids: 10770,
            name: "TV 영화",
        },
        {
            genre_ids: 53,
            name: "스릴러",
        },
        {
            genre_ids: 10752,
            name: "전쟁",
        },
        {
            genre_ids: 37,
            name: "서부",
        },
    ]
    const getMovieDetail = function (movieId) {
        axios({
            method: "GET",
            url: `${API_URL}/movies/${movieId}`,
            headers: {
                Authorization: `Token ${accountStore.loginToken}`,
            },
        })
            .then((response) => {
                console.log(response.data)
                return response.data
            })
            .catch((error) => console.log(error))
    }

    const likeMovie = function (movieId) {
        axios({
            method: "POST",
            url: `${API_URL}/movies/${movieId}/likes/`,
            headers: {
                Authorization: `Token ${accountStore.loginToken}`,
            },
        })
            .then((response) => {
                console.log(response.data)
            })
            .catch((error) => console.log(error))
    }

    // 하드코딩 만세!
    const ottList = {
        8: "넷플릭스",
        119: "아마존 프라임 비디오",
        337: "디즈니+",
        356: "웨이브",
        97: "왓챠",
        350: "애플 TV+",
        96: "네이버 스토어",
        3: "Google 플레이 무비",
        11: "MUBI",
        100: "GuideDoc",
        190: "Curiosity Stream",
        521: "Spamflix",
        475: "DOCSVILLE",
        538: "Plex",
        546: "WOW Presents Plus",
        551: "Megellan TV",
        554: "BroadwayHD",
        559: "Filmzie",
        444: "Dekkoo",
        567: "True Story",
        569: "DocAlliance Films",
        315: "Hoichoi",
        677: "Eventive",
        692: "Cultpix",
        701: "FilmBox+",
        1771: "Takflix",
        309: "Sun Nxt",
        445: "Classix",
        1796: "넷플릭스 Basic with Ads",
        283: "Crunchyroll",
    }

    return { API_URL, getMovieDetail, likeMovie, ottList, genres }
})
