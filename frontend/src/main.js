// vue js primary modules
import { createApp } from "vue"
import { createPinia } from "pinia"
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"

// bootstrap
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"

// font
import "pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css"

import App from "./App.vue"
import router from "./router"

// font-awesome
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { fas } from "@fortawesome/free-solid-svg-icons"
import { far } from "@fortawesome/free-regular-svg-icons"
import { library } from "@fortawesome/fontawesome-svg-core"

// dayjs
import dayjs from 'dayjs';

library.add(fas, far)

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(router)
app.use(pinia)
app.component("font-awesome-icon", FontAwesomeIcon)

app.mount("#app")
