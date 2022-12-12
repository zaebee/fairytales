import { TalesState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";

export const getters = {
  readStepper: (state: TalesState) => {
    return state.step;
  },
  readStatus: (state: TalesState) => (part: string) => {
    return state.loadingStatus[part];
  },
  readHeroes: (state: TalesState) => state.heroes,
  selectedHeroes: (state: TalesState) => (index: number) => {
    if (state.heroes.length > index) {
      return state.heroes[index];
    }
  },
  readStructures: (state: TalesState) => state.structures,
  readStructuresHtml: (state: TalesState) => {
    const structuresHtml = state.structures.map((struct) => {
      return { parts: struct.parts.replace(/\n/g, "<br />") };
    });
    return structuresHtml;
  },
  selectedStructure: (state: TalesState) => (index: number) => {
    if (state.structures.length > index) {
      return state.structures[index];
    }
  },
  readTale: (state: TalesState) => state.tale,
  readStoriesHtml: (state: TalesState) => {
    if (!state.tale) {
      return {};
    }
    const taleHtml = state.tale.stories.map((story) => {
      return { text: story.text.replace(/\n/g, "<br />") };
    });
    return taleHtml;
  },
};

const { read } = getStoreAccessors<TalesState, State>("");

export const readStepper = read(getters.readStepper);
export const readStatus = read(getters.readStatus);
export const readHeroes = read(getters.readHeroes);
export const readStructures = read(getters.readStructures);
export const readStructuresHtml = read(getters.readStructuresHtml);
export const readTale = read(getters.readTale);
export const readStoriesHtml = read(getters.readStoriesHtml);
export const selectedHeroes = read(getters.selectedHeroes);
export const selectedStructure = read(getters.selectedStructure);
