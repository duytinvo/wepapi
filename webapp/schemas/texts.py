from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# from datetime import date


class DocBase(BaseModel):
    text: Optional[str] = None
    caption: Optional[str] = None


class DocCreate(DocBase):
    text: str
    caption: Optional[str]


class ShowDoc(DocBase):
    text: str
    caption: Optional[str]
    # filename: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:  # to convert non dict obj to json
        orm_mode = True
