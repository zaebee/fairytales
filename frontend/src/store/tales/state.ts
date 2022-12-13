import { IHero, ITale, IStructure, ILoader, IHeroPortrait, IHeroSet } from "@/interfaces";
import { AppNotification } from "../main/state";

export interface TalesState {
  step: number,
  selectedHeroSet: number,
  selectedStructure: number,
  loadingStatus: ILoader,
  notifications: AppNotification[];
  heroes: IHero[];
  heroSets: IHeroSet[];
  structure: IStructure | null;
  structures: IStructure[];
  tale: ITale | null;
}
