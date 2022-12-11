from typing import Optional

from pydantic import BaseModel


class HeroBase(BaseModel):
    """Shared hero properties."""
    names: Optional[list[str]] = None
    descriptions: Optional[list[str]] = None
