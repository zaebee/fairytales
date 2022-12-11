import { IHero, ITale, IStructure, ILoader } from "@/interfaces";
import { AppNotification } from "../main/state";

export interface TalesState {
  loadingStatus: ILoader,
  notifications: AppNotification[];
  heroes: IHero[];
  structures: IStructure[];
  tale: ITale | null;
}
