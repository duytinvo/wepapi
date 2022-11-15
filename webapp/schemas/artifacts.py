from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# from datetime import date


class ShowArtifact(BaseModel):
    timestamp: Optional[datetime] = None
    filename: Optional[str] = None
    dtype: Optional[str] = None
    is_upload: Optional[str] = None

    class Config:  # to convert non dict obj to json
        orm_mode = True
