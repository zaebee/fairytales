import {
  ITale,
  ILoader,
  IHeroSet,
  IHeroPortrait,
  IStructure,
  IStructImage,
} from "@/interfaces";
import { TalesState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { AppNotification } from "../main/state";

export const mutations = {
  setStepper(state: TalesState, payload: number) {
    state.step = payload;
  },
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
  setHeroes(state: TalesState, payload: IHeroSet[]) {
    state.heroSets = payload;
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
  setHeroPortrait(state: TalesState, payload: IHeroPortrait[]) {
    const portrait = payload[0];
    const updatedHeroes = state.heroes.filter((hero) => {
      if (hero.id === portrait.hero_id) {
        hero.portrait = portrait;
      }
      return hero;
    });
    state.heroes = updatedHeroes;
  },
  setStructImage(state: TalesState, payload: IStructImage[]) {
    const image = payload[0];
    const updatedStructures = state.structures.filter((struct) => {
      if (struct.id === image.scene_id) {
        struct.image = image;
      }
      return struct;
    });
    state.structures = updatedStructures;
  },
  selectHeroSet(state: TalesState, payload: number) {
    state.selectedHeroSet = payload;
    const heroSet = state.heroSets[payload];
    state.heroes = heroSet && heroSet.heroes ? heroSet.heroes : [];
  },
  selectStructure(state: TalesState, payload: number) {
    state.selectedStructure = payload;
    const structure = state.structures[payload];
    state.structure = structure ? structure : null;
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { commit } = getStoreAccessors<TalesState | any, State>("");

export const commitStepper = commit(mutations.setStepper);
export const commitLoadingStatus = commit(mutations.setLoadingStatus);

export const commitSetHeroes = commit(mutations.setHeroes);
export const commitSetHeroPortrait = commit(mutations.setHeroPortrait);
export const commitSetStructures = commit(mutations.setStructrues);
export const commitSetStructImage = commit(mutations.setStructImage);
export const commitSetTale = commit(mutations.setTale);

export const commitResetHeroes = commit(mutations.resetHeroes);
export const commitResetTale = commit(mutations.resetTale);
export const commitResetStructures = commit(mutations.resetStructrues);

export const commitSelectHeroSet = commit(mutations.selectHeroSet);
export const commitSelectStructure = commit(mutations.selectStructure);
