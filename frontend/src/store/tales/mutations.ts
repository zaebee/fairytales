import { IHero, IStructure, ITale, ILoader } from "@/interfaces";
import { TalesState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { AppNotification } from "../main/state";

export const mutations = {
  setLoadingStatus(state: TalesState, payload: ILoader) {
    Object.assign(state.loadingStatus, payload);
  },
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
  resetHeroes(state: TalesState) {
    state.heroes = [];
  },
  setStructrues(state: TalesState, payload: IStructure[]) {
    state.structures = payload;
  },
  resetStructrues(state: TalesState) {
    state.structures = [];
  },
  setTale(state: TalesState, payload: ITale) {
    state.tale = payload;
  },
  resetTale(state: TalesState) {
    state.tale = null;
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { commit } = getStoreAccessors<TalesState | any, State>("");

export const commitLoadingStatus = commit(mutations.setLoadingStatus);
export const commitSetHeroes = commit(mutations.setHeroes);
export const commitResetHeroes = commit(mutations.resetHeroes);
export const commitSetStructures = commit(mutations.setStructrues);
export const commitResetStructures = commit(mutations.resetStructrues);
export const commitSetTale = commit(mutations.setTale);
export const commitResetTale = commit(mutations.resetTale);
