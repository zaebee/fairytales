from typing import Optional

from pydantic import BaseModel

from app.schemas import hero
from app.schemas import image as img


class Part(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    text: Optional[str] = None
    image: Optional[img.SceneCreate] = None


class Structure(BaseModel):
    parts: Optional[list[Part]] = None


class Story(BaseModel):
    text: Optional[str] = None


class TaleBase(BaseModel):
    """Shared properties."""
    title: Optional[str] = None
    log_line: Optional[str] = None
    structure: Optional[Structure] = None
    heroes: Optional[list[hero.Hero]] = None
    stories: Optional[list[Story]] = None
    max_tokens: int = 250
    temperature: float = 0.5
    tale_style: Optional[str] = None


class TaleCreate(TaleBase):
    """Properties to receive on tale creation."""
    log_line: str
