<template>
  <div class="bg-bookmark">
    <div class="h-100 d-flex justify-content-center align-items-center">
      <section
        class="innerscroll card h-75 p-5 bg-dark bg-opacity-75 text-white w-75"
      >
        <h1>{{ userInfo.name }}님의 찜목록</h1>
        <div v-if="bookmarkList">
          <p class="mb-1">
            찜목록에 있는 모든 영화를 시청하는 최적 가격은 약
            {{ cost }}원 이에요
          </p>
          <p class="mb-5" v-if="bestOTT">
            가장 가성비가 좋은 OTT 서비스는
            {{ movieStore.ottList[bestOTT.ottId] }}에요. 영화 한 편당 약
            {{ Math.floor(bestOTT.cost) }}원이에요!
          </p>
          <p>
            아래 목록의 사이트에서 가장 합리적인 조합의 가격으로 구독, 대여,
            구매 할 수 있어요!
          </p>
          <!-- 최적 가격 알고리즘 결과 나열 -->
          <div class="mb-4">
            <div
              class="text-start"
              v-for="(value, key, index) in costOTT"
              :key="index"
            >
              <div class="mb-3" v-if="value.length > 0">
                <div class="mb-3">
                  <img
                    :src="`https://media.themoviedb.org/t/p/original${ottLogo[key]}`"
                    class="rounded ott-logo"
                    alt=""
                  />
                  <span class="fs-4 fw-semibold ms-3">{{
                    movieStore.ottList[key]
                  }}</span>
                </div>
                <div v-for="(movie, index) in value" :key="index">
                  <span class="mb-1">{{ movie.title }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="text-start" v-if="cannotWatch.length > 0">
            <h5>다음 목록의 영화는 아쉽게도, 현재 시청하기가 어려워요 :(</h5>
            <div v-for="(movie, index) in cannotWatch" :key="index">
              <span class="mb-1">{{ movie.title }}</span>
            </div>
          </div>
        </div>
        <div
          class="d-flex flex-wrap justify-content-evenly"
          v-if="bookmarkList"
        >
          <div v-for="movie in bookmarkList" :key="movie.movie_id">
            <RouterLink
              class="no-underline m-3"
              :to="{
                name: 'MovieDetailView',
                params: { movieId: movie.movie_id },
              }"
            >
              <div class="card movie-card bg-transparent">
                <div>
                  <img
                    class="movie-poster"
                    :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movie.poster_path}`"
                    alt="Movie Poster"
                  />
                </div>
                <p class="text-white mt-3">{{ movie.title }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
        <div v-else>
          <p>북마크한 영화가 없습니다.</p>
        </div>
        <div>
          <h3>참고해주세요!</h3>
          <div>
            <p>꼬꼬무의 서비스 추천 알고리즘은 다음과 같이 구현되어 있어요</p>
            <ul class="text-start">
              <li>
                구독형 서비스의 기회비용은 1개월 가격을 기준으로, 찜목록에 담긴
                해당 구독형 서비스로 시청가능한 영화의 수로 나누어 한 편당
                가성비를 계산해요
              </li>
              <li>
                꼬꼬무는 기회비용을 계산하기 때문에, 회원가입 설문조사 당시에
                이미 이용중이라고 답변해준 OTT 서비스의 구독료는 0원으로
                계산해요
              </li>
              <li>
                각 영화의 대여 및 구매 비용이 다르기 때문에 영화당 각각 5,000원,
                15,000원으로 책정하고 계산된 가격을 보여줘요
              </li>
              <li>
                구독형 서비스, 대여, 구매(소장)가 모두 불가능한 영화가 존재할 수
                있어요. 이 경우 따로 명시하고 있어요
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRouter, RouterLink } from "vue-router"
import { useAccountStore, useMovieStore } from "@/stores/counter"
import axios from "axios"

const accountStore = useAccountStore()
const movieStore = useMovieStore()
const router = useRouter()
const tmdbAPIKey = import.meta.env.VITE_TMDB_API_KEY

// get providerInfo from TMDB for get OTT Logo
const ottLogo = {
  8: "/pbpMk2JmcoNnQwx5JGpXngfoWtp.jpg",
  119: "/dQeAar5H991VYporEjUspolDarG.jpg",
  337: "/97yvRBw1GzX7fXprcF80er19ot.jpg",
  356: "/hPcjSaWfMwEqXaCMu7Fkb529Dkc.jpg",
  97: "/5gmEivxOGPdq4Afpq1f8ktLtEW1.jpg",
  350: "/2E03IAZsX4ZaUqM7tXlctEPMGWS.jpg",
  96: "/crFbxg6jkiKc14gpIGMkre9Y3mu.jpg",
  3: "/8z7rC8uIDaTM91X0ZfkRf04ydj2.jpg",
  11: "/fj9Y8iIMFUC6952HwxbGixTQPb7.jpg",
  100: "/eKVmLFHW5PeNhuR7Nedd8OIxW2M.jpg",
  190: "/oR1aNm1Qu9jQBkW4VrGPWhqbC3P.jpg",
  521: "/k2YgZyxij5RcnS1qqUYEUrJB4oQ.jpg",
  475: "/5zqbck5mo8PuVbGu2ngBUdn5Yga.jpg",
  538: "/vLZKlXUNDcZR7ilvfY9Wr9k80FZ.jpg",
  546: "/6dET59jNU0ADysghEjl8Unuc7Ca.jpg",
  551: "/mSH24WQcRDJ2fsL5iucXqqRnSRb.jpg",
  554: "/6IYZ4NjwPikxN7J9cfSmuyeHeMm.jpg",
  559: "/eUBxtrqO26wAJfYOZJOzhQEo3mm.jpg",
  444: "/x6nRFzF32hCzMHaVM4RHRo7lsgS.jpg",
  567: "/aRPDQvVcpeY07sjI6lAALMCL0ti.jpg",
  569: "/vbXJBJVv3u3YWt6ml0l0ldDblXT.jpg",
  315: "/u7dwMceEbjxd1N3TLEUBILSK2x6.jpg",
  677: "/fwx5Ed64TkfWiRH1SOSkc4781Ts.jpg",
  692: "/uauVx3dGWt0GICqdMCBYJObd3Mo.jpg",
  701: "/fbveJTcro9Xw2KuPIIoPPePHiwy.jpg",
  1771: "/ed0vz5bryWIhQB5sHiuGvHKnHHn.jpg",
  309: "/6KEQzITx2RrCAQt5Nw9WrL1OI8z.jpg",
  445: "/uFjAjvrKMII0H766QzyHDNkZdKX.jpg",
  1796: "/kICQccvOh8AIBMHGkBXJ047xeHN.jpg",
  283: "/mXeC4TrcgdU6ltE9bCBCEORwSQR.jpg",
}

// get userInfo
const userInfo = ref(null)
const userInfoPromise = accountStore.getUserInfo()
userInfoPromise.then((data) => {
  userInfo.value = data
})

// get bookmarkList
const bookmarkList = ref(null)
const bestOTT = ref(null)
const cost = ref(0)
const costOTT = ref({
  8: [],
  119: [],
  337: [],
  356: [],
  97: [],
  350: [],
  96: [],
  3: [],
  11: [],
  100: [],
  190: [],
  521: [],
  475: [],
  538: [],
  546: [],
  551: [],
  554: [],
  559: [],
  444: [],
  567: [],
  569: [],
  315: [],
  677: [],
  692: [],
  701: [],
  1771: [],
  309: [],
  445: [],
  1796: [],
  283: [],
})
const cannotWatch = ref([])

axios({
  method: "GET",
  url: `${accountStore.API_URL}/accounts/profile/bookmark/`,
  headers: { Authorization: `Token ${accountStore.loginToken}` },
})
  .then((response) => {
    console.log(response.data)
    bookmarkList.value = response.data

    // calculate best case of sum of the cost
    let countMoviesByOTT = {
      8: 0,
      119: 0,
      337: 0,
      356: 0,
      97: 0,
      350: 0,
      96: 0,
      3: 0,
      11: 0,
      100: 0,
      190: 0,
      521: 0,
      475: 0,
      538: 0,
      546: 0,
      551: 0,
      554: 0,
      559: 0,
      444: 0,
      567: 0,
      569: 0,
      315: 0,
      677: 0,
      692: 0,
      701: 0,
      1771: 0,
      309: 0,
      445: 0,
      1796: 0,
      283: 0,
    }
    let watchOnOTT = {
      8: [],
      119: [],
      337: [],
      356: [],
      97: [],
      350: [],
      96: [],
      3: [],
      11: [],
      100: [],
      190: [],
      521: [],
      475: [],
      538: [],
      546: [],
      551: [],
      554: [],
      559: [],
      444: [],
      567: [],
      569: [],
      315: [],
      677: [],
      692: [],
      701: [],
      1771: [],
      309: [],
      445: [],
      1796: [],
      283: [],
    }
    let totalRentCount = 0
    let countMoviesByRent = {
      8: 0,
      119: 0,
      337: 0,
      356: 0,
      97: 0,
      350: 0,
      96: 0,
      3: 0,
      11: 0,
      100: 0,
      190: 0,
      521: 0,
      475: 0,
      538: 0,
      546: 0,
      551: 0,
      554: 0,
      559: 0,
      444: 0,
      567: 0,
      569: 0,
      315: 0,
      677: 0,
      692: 0,
      701: 0,
      1771: 0,
      309: 0,
      445: 0,
      1796: 0,
      283: 0,
    }
    let watchOnRent = []
    let totalBuyCount = 0
    let countMoviesByBuy = {
      8: 0,
      119: 0,
      337: 0,
      356: 0,
      97: 0,
      350: 0,
      96: 0,
      3: 0,
      11: 0,
      100: 0,
      190: 0,
      521: 0,
      475: 0,
      538: 0,
      546: 0,
      551: 0,
      554: 0,
      559: 0,
      444: 0,
      567: 0,
      569: 0,
      315: 0,
      677: 0,
      692: 0,
      701: 0,
      1771: 0,
      309: 0,
      445: 0,
      1796: 0,
      283: 0,
    }
    let watchOnBuy = []
    // 1USD = 1300KRW 고정 환율 적용함, 월간 요금제 기준
    // 190 Curiosity Stream 까지 가격 지정됨
    let priceOfOTT = {
      8: 13500,
      119: 7787,
      337: 9900,
      356: 7900,
      97: 7900,
      350: 6500,
      96: 4900,
      3: 9900,
      11: 12987,
      100: 10387,
      190: 6487,
      521: 9900,
      475: 9900,
      538: 9900,
      546: 9900,
      551: 9900,
      554: 9900,
      559: 9900,
      444: 9900,
      567: 9900,
      569: 9900,
      315: 9900,
      677: 9900,
      692: 9900,
      701: 9900,
      1771: 9900,
      309: 9900,
      445: 9900,
      1796: 5500,
      283: 9900,
    }
    let resultOTT = []
    let resultRent = []
    let resultBuy = []
    // 이미 사용중인 OTT의 가격은 0으로 설정
    for (const price in priceOfOTT) {
      if (
        price === userInfo.value.genre1 ||
        price === userInfo.value.genre2 ||
        price === userInfo.value.genre3
      ) {
        priceOfOTT[price] = 0
      }
    }

    // 영화별로 OTT 있으면 카운트 올리고 해당 OTT에 추가
    // OTT가 없으면 Rent가 가능한지 찾음
    // Rent가 안되면 Buy 가능한지 찾음
    // Buy도 안되면 못보는 영화에 추가
    for (const movie of response.data) {
      if (movie.provide_info.flatrate.length > 0) {
        for (const ott of movie.provide_info.flatrate) {
          countMoviesByOTT[ott] += 1
        }
      } else if (movie.provide_info.rent.length > 0) {
        for (const rent of movie.provide_info.rent) {
          countMoviesByRent[rent] += 1
        }
        totalRentCount += 1
        watchOnRent.push(movie)
        costOTT.value[movie.provide_info.rent[0]].push(movie)
      } else if (movie.provide_info.buy.length > 0) {
        for (const buy of movie.provide_info.buy) {
          countMoviesByBuy[buy] += 1
        }
        totalBuyCount += 1
        costOTT.value[movie.provide_info.buy[0]].push(movie)
      } else {
        cannotWatch.value.push(movie)
      }
    }

    let bestOTTcost = 99999

    // 가격 합산
    let validOTT = {
      8: false,
      119: false,
      337: false,
      356: false,
      97: false,
      350: false,
      96: false,
      3: false,
      11: false,
      100: false,
      190: false,
      521: false,
      475: false,
      538: false,
      546: false,
      551: false,
      554: false,
      559: false,
      444: false,
      567: false,
      569: false,
      315: false,
      677: false,
      692: false,
      701: false,
      1771: false,
      309: false,
      445: false,
      1796: false,
      283: false,
    }
    for (const movie of response.data) {
      if (movie.provide_info.flatrate.length > 0) {
        let mostCheapOTT = movie.provide_info.flatrate[0]
        for (const ott of movie.provide_info.flatrate) {
          if (
            priceOfOTT[ott] / countMoviesByOTT[ott] <
            priceOfOTT[mostCheapOTT] / countMoviesByOTT[mostCheapOTT]
          ) {
            mostCheapOTT = ott
          }
        }
        if (
          movie.provide_info.rent.length > 0 &&
          priceOfOTT[mostCheapOTT] / countMoviesByOTT[mostCheapOTT] > 5000
        ) {
          cost.value += 5000
          costOTT.value[movie.provide_info.rent[0]].push(movie)
        } else if (
          movie.provide_info.rent.length === 0 &&
          movie.provide_info.buy.length > 0 &&
          priceOfOTT[mostCheapOTT] / countMoviesByOTT[mostCheapOTT] > 15000
        ) {
          cost.value += 15000
          costOTT.value[movie.provide_info.buy[0]].push(movie)
        } else {
          validOTT[mostCheapOTT] = true
          costOTT.value[mostCheapOTT].push(movie)
        }
      }
    }
    for (const ott in validOTT) {
      if (validOTT[ott]) {
        cost.value += priceOfOTT[ott]
      }
    }
    cost.value += totalRentCount * 5000
    cost.value += totalBuyCount * 15000

    if (Object.values(countMoviesByOTT).some((value) => value > 0)) {
      for (const ott in countMoviesByOTT) {
        if (
          countMoviesByOTT[ott] > 0 &&
          priceOfOTT[ott] / countMoviesByOTT[ott] < bestOTTcost
        ) {
          bestOTTcost = priceOfOTT[ott] / countMoviesByOTT[ott]
          bestOTT.value = {
            ottId: ott,
            cost: priceOfOTT[ott] / countMoviesByOTT[ott],
          }
        }
      }
    }
  })
  .catch((error) => console.log(error))
</script>

<style scoped>
.bg-bookmark {
  min-height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("@/assets/interstellar.jpg");
  background-size: cover;
}

.ott-logo {
  width: 50px;
  height: 50px;
}

.innerscroll {
  overflow-y: auto;
}

.movie-card {
  width: 200px;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card {
  border: none;
}

.no-underline {
  text-decoration: none;
}
</style>
