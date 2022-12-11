import { IHero, IStructure, ITale } from "@/interfaces";
import { TalesState, AppNotification } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";

export const mutations = {
  addNotification(state: TalesState, payload: AppNotification) {
    state.notifications.push(payload);
  },
  removeNotification(state: TalesState, payload: AppNotification) {
    state.notifications = state.notifications.filter(
      (notification) => notification !== payload,
    );
  },
  setHeroes(state: TalesState, payload: IHero[]) {
    state.heroes = payload;
  },
  setStructrues(state: TalesState, payload: IStructure[]) {
    state.structures = payload;
  },
  setTale(state: TalesState, payload: ITale) {
    state.tale = payload;
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { commit } = getStoreAccessors<TalesState | any, State>("");

export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitSetHeroes = commit(mutations.setHeroes);
export const commitSetStructures = commit(mutations.setStructrues);
export const commitSetTale = commit(mutations.setTale);
