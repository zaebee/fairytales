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
  portrait?: boolean;
  image?: boolean;
}

export interface IHeroPortrait {
  uid?: string;
  path?: string;
  style?: string;
  prompt?: string;
  hero_id?: number;
}

export interface IHeroPortraitCreate {
  uid?: string;
  path?: string;
  style?: string;
  prompt: string;
  hero_id: string;
}

export interface IHero {
  id: number;
  name: string;
  description: string;
  portrait?: IHeroPortrait | null;
}

export interface IHeroSet {
  heroes: IHero[];
}

export interface IStructImage {
  uid?: string;
  path?: string;
  style?: string;
  prompt?: string;
  scene_id?: number;
}

export interface IStructImageCreate {
  uid?: string;
  path?: string;
  style?: string;
  prompt: string;
  scene_id: string;
}

export interface IPart {
  id: number;
  text: string;
  name: string;
  image?: IStructImage | null;
}

export interface IStructure {
  id: number;
  parts: IPart[];
}

export interface IStory {
  text: string;
}

export interface ITale {
  title: string;
  log_line: string;
  structure: IStructure;
  heroes: IHero[];
  stories: IStory[];
  temperature: number;
  max_tokens: number;
  tale_style: string;
}

export interface ITaleCreate {
  title?: string;
  log_line?: string;
  structure?: IStructure;
  heroes?: IHero[];
  stories?: IStory[];
  temperature?: number;
  max_tokens?: number;
  tale_style?: string;
}
