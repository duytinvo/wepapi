from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from webapp.db.base_class import Base


class Doc(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    caption = Column(String)
    # filename = Column(String)
    timestamp = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="docs")
