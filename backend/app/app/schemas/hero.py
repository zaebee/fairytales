from typing import Optional

from pydantic import BaseModel
from app.schemas import image


class Hero(BaseModel):
    """Shared hero properties."""
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    portrait: Optional[image.Image] = None


class HeroSet(BaseModel):
    """Shared heroes properties."""
    heroes: Optional[list[Hero]] = None
