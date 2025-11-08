from sqlalchemy import Integer, Column, String, Boolean, Text, DateTime, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db.base import Base

"""
Movie Schema:

budget: 30000000
genres: [{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]
id: 862
imdb_id: tt0114709
title: Toy Story
overview: String
poster_path: /rhIRbceoE9lR4veEXuwCC2wARtG.jpg
release_date: 1995-10-30
vote_average: 7.7
vote_count: 5415

===================================================

Rating Schema:

user_id
movie_id
rating

===================================================

Genre Schema:

id: int
name: str
"""

movie_genre = Table(
  'movie_genres',
  Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
  Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
)

class Movie(Base):
  __tablename__ = "movies"

  id = Column(Integer, primary_key=True, index=True)
  imdb_id = Column(String(255))
  title = Column(String(255))

  overview = Column(Text)
  poster_path = Column(String(500))
  release_date = Column(DateTime)

  vote_average = Column(Float)
  vote_count = Column(Integer)

  # relation
  genres = relationship("Genre", secondary=movie_genre, back_populates="movies")


class Rating(Base):
  __tablename__ = "ratings"

  id = Column(Integer, primary_key=True)

  user_id = Column(Integer, nullable=False, index=True)
  movie_id = Column(Integer, nullable=False, index=True)
  rating = Column(Float, nullable=False)

class Genre(Base):
  __tablename__ = "genres"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), nullable=False)

  #relationship
  movies = relationship("Movie", secondary=movie_genre, back_populates="genres")