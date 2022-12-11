import { IHero, ITale, IStructure } from "@/interfaces";

export interface AppNotification {
  content: string;
  color?: string;
  showProgress?: boolean;
}

export interface TalesState {
  notifications: AppNotification[];
  heroes: IHero[];
  structures: IStructure[];
  tale: ITale | null;
}
