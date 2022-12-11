export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface ILoader {
  heroes?: boolean;
  structures?: boolean;
  tale?: boolean;
}

export interface IHero {
  names: string[];
  descriptions: string[];
}

export interface IStructure {
  parts: string;
}

export interface IStory {
  text: string;
}

export interface ITale {
  title: string;
  log_line: string;
  structure: IStructure;
  heroes: IHero;
  stories: IStory[];
  temperature: number;
  tale_style: string;
}

export interface ITaleCreate {
  title?: string;
  log_line?: string;
  structure?: IStructure;
  heroes?: IHero;
  stories?: string[];
  temperature?: number;
  tale_style?: string;
}
