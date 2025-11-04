from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

class Movie(Base):
  __tablename__ = "movies"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(255))
