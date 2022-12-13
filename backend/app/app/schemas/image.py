from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    uid: Optional[str] = None
    prompt: Optional[str] = None
    style: Optional[str] = None
    path: Optional[str] = None


class Portrait(Image):
    hero_id: int
    prompt: str


class PortraitCreate(Image):
    hero_id: int
    prompt: str


class Scene(Image):
    scene_id: int
    prompt: str


class SceneCreate(Image):
    scene_id: int
    prompt: str
