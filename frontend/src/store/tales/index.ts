import { mutations } from "./mutations";
import { getters } from "./getters";
import { actions } from "./actions";
import { TalesState } from "./state";

const defaultState: TalesState = {
  step: 0,
  selectedHeroSet: 0,
  selectedStructure: 0,
  loadingStatus: {
    heroes: false,
    structures: false,
    tale: false,
    portrait: false,
    image: false,
  },
  notifications: [],
  heroSets: [],
  heroes: [],
  structure: null,
  structures: [],
  tale: null,
};

export const talesModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
