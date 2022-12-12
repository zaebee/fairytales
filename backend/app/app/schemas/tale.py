from typing import Optional

from pydantic import BaseModel

from app.schemas import hero


class Structure(BaseModel):
    parts: Optional[str] = None


class Story(BaseModel):
    text: Optional[str] = None


class TaleBase(BaseModel):
    """Shared properties."""
    title: Optional[str] = None
    log_line: Optional[str] = None
    structure: Optional[Structure] = None
    heroes: Optional[hero.HeroBase] = None
    stories: Optional[list[Story]] = None
    max_tokens: int = 250
    temperature: float = 0.5
    tale_style: Optional[str] = None


class TaleCreate(TaleBase):
    """Properties to receive on tale creation."""
    log_line: str


class TaleUpdate(TaleBase):
    """Properties to receive on item update."""
    pass


class TaleInDBBase(TaleBase):
    """Properties shared by models stored in DB."""
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Tale(TaleInDBBase):
    """Properties to return to client."""
    pass


class TaleInDB(TaleInDBBase):
    """Properties properties stored in DB."""
    pass
