import { mutations } from "./mutations";
import { getters } from "./getters";
import { actions } from "./actions";
import { TalesState } from "./state";

const defaultState: TalesState = {
  step: 1,
  selectedHeroSet: -1,
  selectedStructure: -1,
  loadingStatus: {
    heroes: false,
    structures: false,
    tale: false,
    portrait: false,
    image: false,
  },
  notifications: [],
  heroSets: [
    {
      heroes: [
        {
          id: 1,
          name: "Zae",
          portrait: {
            uid: "sa2Kh8Kc3qZl94NOE53quzbHacRQ0q4G",
            prompt: "zae is magic prince with blue eyes and green hair",
            style:
              "{}, beautifully lit, steampunk, by rebecca guay, by francois schuiten ",
            path: "https://tales.zae.life/storage/0c/d3/0cd3e3acbb6628284dccdc9194d4a71b30b53f02665bfb874bfc732c2469f828",
          },
          description: "Zae is magic prince with blue eyes and green hair",
        },
        {
          id: 2,
          name: "Moo",
          portrait: null,
          description: "Bee is black-yellow fairy bee with the huge facets eyes",
        },
      ],
    },
  ],
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
