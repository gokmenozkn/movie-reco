from sqlalchemy import Integer, Column, String, Boolean, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

class Movie(Base):
  __tablename__ = "movies"

  id = Column(Integer, primary_key=True, index=True)
  imdb_id = Column(String(255))
  title = Column(String(255))
  homepage = Column(String(500))
  budget = Column(Integer)
  adult = Column(Boolean)

  original_language = Column(String(255))
  original_title = Column(String(255))
  overview = Column(Text)
  poster_path = Column(String(500))
  release_date = Column(DateTime)

  vote_average = Column(Float)
  vote_count = Column(Integer)


class Ratings(Base):
  __tablename__ = "ratings"

  id = Column(Integer, primary_key=True)

  user_id = Column(Integer, nullable=False, index=True)
  movie_id = Column(Integer, nullable=False, index=True)
  rating = Column(Float, nullable=False)