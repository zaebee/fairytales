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
  setStructrues(state: TalesState, payload: IStructure[]) {
    state.structures = payload;
  },
  setTale(state: TalesState, payload: ITale) {
    state.tale = payload;
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
    if (!state.structure) {
      return;
    }
    const image = payload[0];
    const updatedParts = state.structure.parts.filter((part) => {
      if (part.id === image.scene_id) {
        part.image = image;
      }
      return part;
    });
    state.structure.parts = updatedParts;
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

export const commitSelectHeroSet = commit(mutations.selectHeroSet);
export const commitSelectStructure = commit(mutations.selectStructure);
