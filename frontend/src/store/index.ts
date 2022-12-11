import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";

import { mainModule } from "./main";
import { State } from "./state";
import { adminModule } from "./admin";
import { talesModule } from "./tales";

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    tales: talesModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
