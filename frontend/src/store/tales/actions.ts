import { api } from "@/api";
import axios from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import { commitAddNotification, commitRemoveNotification } from "../main/mutations";
import {
  commitSetHeroes,
  commitResetHeroes,
  commitSetStructures,
  commitResetStructures,
  commitSetTale,
  commitResetTale,
  commitLoadingStatus,
} from "./mutations";
import { TalesState } from "./state";

type MainContext = ActionContext<TalesState, State>;

export const actions = {
  async actionCheckApiError(context: MainContext, payload: unknown) {
    if (axios.isAxiosError(payload)) {
      const data = payload.response?.data;
      const message = data ? data["detail"] : "";
      commitLoadingStatus(context, {
        heroes: false,
        structures: false,
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
      commitResetHeroes(context);
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createHeroes(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 700)),
        ])
      )[0];
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
  async actionCreateStructures(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating structures" };
      commitLoadingStatus(context, { structures: true });
      commitResetStructures(context);
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createStructures(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 700)),
        ])
      )[0];
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
  async actionCreateTale(context: MainContext, payload) {
    try {
      const loadingNotification = { content: "Generating fairy tale" };
      commitLoadingStatus(context, { tale: true });
      commitResetTale(context);
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createTale(payload),
          await new Promise<void>((resolve, _) => setTimeout(() => resolve(), 700)),
        ])
      )[0];
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

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCreateHeroes = dispatch(actions.actionCreateHeroes);
export const dispatchCreateStructures = dispatch(actions.actionCreateStructures);
export const dispatchCreateTale = dispatch(actions.actionCreateTale);
