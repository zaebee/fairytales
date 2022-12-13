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
  readHeroSets: (state: TalesState) => state.heroSets,
  readHeroPortrait: (state: TalesState) => (index: number) => {
    if (state.heroes.length && state.heroes[index].portrait) {
      return state.heroes[index].portrait;
    }
  },
  readHeroesPortraitsComplete: (state: TalesState) => {
    return (
      state.heroes.length &&
      state.heroes.every((hero) => {
        return hero.portrait && hero.portrait.path;
      })
    );
  },
  readStructures: (state: TalesState) => state.structures,
  readStructuresHtml: (state: TalesState) => {
    return state.structures;
  },
  selectedStructure: (state: TalesState) => {
    if (state.structure) {
      return state.structure;
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
export const readHeroSets = read(getters.readHeroSets);
export const readStructures = read(getters.readStructures);
export const readStructuresHtml = read(getters.readStructuresHtml);
export const readTale = read(getters.readTale);
export const readStoriesHtml = read(getters.readStoriesHtml);

export const selectedStructure = read(getters.selectedStructure);

export const readHeroPortrait = read(getters.readHeroPortrait);
export const readHeroesPortraitsComplete = read(getters.readHeroesPortraitsComplete);
