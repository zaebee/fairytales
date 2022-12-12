import { mutations } from "./mutations";
import { getters } from "./getters";
import { actions } from "./actions";
import { TalesState } from "./state";

const defaultState: TalesState = {
  step: 0,
  loadingStatus: {
    heroes: false,
    structures: false,
    tale: false,
  },
  notifications: [],
  heroes: [],
  structures: [],
  tale: null,
};

export const talesModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
