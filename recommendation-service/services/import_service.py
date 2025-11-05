import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Movie


"""
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
"""

async def import_movies_from_csv(session: AsyncSession, csv_path: str):
  movie_df = pd.read_csv(csv_path)
  
  for _, row in movie_df.iterrows():
    movie = Movie(
      id= int(row["id"]),
      imdb_id=row.get("imdb_id"),
      title=row.get("title", "Unknown"),
      poster_path=row.get("poster_path", "Unknown"),
      home_page=row.get("home_page"),
      vote_average=row.get("vote_average"),
      vote_count=row.get("vote_count", None),
      homepage=row.get("homepage", "Unknown"),
      budget=row.get("budget"),
      adult=row.get("adult"),
      original_language=row.get("original_language"),
      original_title=row.get("original_title"),
      release_date=row.get("release_date"),
      overview=row.get("overview", "Unknonw")
    )
    session.add(movie)
    
  await session.commit()