import { api } from "@/api";
import axios from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import { commitAddNotification, commitRemoveNotification } from "../main/mutations";
import {
  commitSetHeroes,
  commitSetStructures,
  commitSetTale,
  commitStepper,
  commitLoadingStatus,
  commitSetHeroPortrait,
  commitSetStructImage,
  commitSelectHeroSet,
  commitSelectStructure,
} from "./mutations";
import { TalesState } from "./state";

type MainContext = ActionContext<TalesState, State>;

export const actions = {
  actionStep(context: MainContext, payload) {
    commitStepper(context, payload);
  },
  actionSelectHeroSet(context: MainContext, payload) {
    commitSelectHeroSet(context, payload);
  },
  actionSelectStructure(context: MainContext, payload) {
    commitSelectStructure(context, payload);
  },
  async actionCheckApiError(context: MainContext, payload: unknown) {
    if (axios.isAxiosError(payload)) {
      const data = payload.response?.data;
      const message = data ? data["detail"] : "";
      commitLoadingStatus(context, {
        heroes: false,
        structures: false,
        portrait: false,
        image: false,
        tale: false,
      });
      commitAddNotification(context, {
        content: `${payload.message}: ${message}`,
        color: "error",
      });
    }
  },
  async actionCreateHeroes(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating heroes" };
      commitLoadingStatus(context, { heroes: true });
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createHeroes(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 300)),
        ])
      )[0];
      commitStepper(context, 1);
      commitSetHeroes(context, response.data);
      commitLoadingStatus(context, { heroes: false });
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Heroes successfully generated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateHeroPortrait(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating hero portrait" };
      commitLoadingStatus(context, { portrait: true });
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createPortrait(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 300)),
        ])
      )[0];
      commitSetHeroPortrait(context, response.data);
      commitLoadingStatus(context, { portrait: false });
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Portrait successfully generated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateStructures(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating structures" };
      commitLoadingStatus(context, { structures: true });
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createStructures(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 300)),
        ])
      )[0];
      commitStepper(context, 2);
      commitSetStructures(context, response.data);
      commitLoadingStatus(context, { structures: false });
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Tale structures successfully generated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateStructImage(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating plot illustration" };
      commitLoadingStatus(context, { image: true });
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createImage(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 300)),
        ])
      )[0];
      commitSetStructImage(context, response.data);
      commitLoadingStatus(context, { image: false });
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Illustration successfully generated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateTale(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating fairy tale" };
      commitLoadingStatus(context, { tale: true });
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createTale(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 300)),
        ])
      )[0];
      commitStepper(context, 3);
      commitSetTale(context, response.data);
      commitLoadingStatus(context, { tale: false });
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Tale successfully generated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { dispatch } = getStoreAccessors<TalesState | any, State>("");

export const dispatchStep = dispatch(actions.actionStep);
export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);

export const dispatchCreateHeroes = dispatch(actions.actionCreateHeroes);
export const dispatchCreateHeroPortrait = dispatch(actions.actionCreateHeroPortrait);
export const dispatchCreateStructures = dispatch(actions.actionCreateStructures);
export const dispatchCreateStructImage = dispatch(actions.actionCreateStructImage);

export const dispatchCreateTale = dispatch(actions.actionCreateTale);

export const dispatchSelectHeroSet = dispatch(actions.actionSelectHeroSet);
export const dispatchSelectStructure = dispatch(actions.actionSelectStructure);
