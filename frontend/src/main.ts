// Import Component hooks before component definitions
import "./component-hooks";
import Vue from "vue";
import vuetify from "./plugins/vuetify";
import VueYandexMetrika from "./plugins/metrika";
import App from "./App.vue";
import router from "./router";
import store from "@/store";
import "./registerServiceWorker";

Vue.config.productionTip = false;

Vue.use(VueYandexMetrika, {
  id: 91701398,
  clickmap: true,
  trackLinks: true,
  accurateTrackBounce: true,
  webvisor: true,
  router: router,
  env: process.env.NODE_ENV,
});

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
