import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Movie, Rating, Genre
from sqlalchemy.future import select
import math, ast, datetime

"""
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
"""

async def import_movies_from_csv(session: AsyncSession, csv_path: str):
  movie_df = pd.read_csv(csv_path)
  
  for _, row in movie_df.iterrows():
    movie = Movie(
      id= int(row["id"]),
      imdb_id=row.get("imdb_id"),
      title=row.get("title", "Unknown"),

      poster_path=row.get("poster_path", "Unknown"),
      vote_average=row.get("vote_average"),
      vote_count=row.get("vote_count", None),
      
      release_date=row.get("release_date"),
      overview=row.get("overview", "Unknonw")
    )
    session.add(movie)
    
  await session.commit()

"""
  Bu servis, veritabanı oturumunu (session) bir parametre olarak alır
  ancak 'commit' işlemini ÇAĞIRMAZ. 
  İşlemin ne zaman commit edileceğine veya hata anında 'rollback' yapılacağına 
  API endpoint'i karar verecektir.
"""
async def import_movies_and_genres_from_csv(session: AsyncSession, csv_path: str):
  df = pd.read_csv(csv_path)

  # Veritabanında zaten var olan türleri hızlıca aramak için
  existing_genres_result = await session.execute(select(Genre))
  genres_in_db = { genre.id: genre for genre in existing_genres_result.scalars() }

  movies_to_add = []

  for _, row in df.iterrows():
    try:
      movie_id = int(row["id"]),
    except (ValueError, TypeError):
      continue

    vote_avg = row.get("vote_average")
    vote_cnt = row.get("vote_count")

    vote_average = float(vote_avg) if pd.notna(vote_avg) and not math.isnan(float(vote_avg)) else 0.0
    vote_count = int(vote_cnt) if pd.notna(vote_cnt) and not math.isnan(float(vote_cnt)) else 0

    release_date_obj = None
    if pd.notna(row.get("release_date")):
      try:
        release_date_obj = datetime.strptime(str(row["release_date"]), '%Y-%m-%d').date()
      except ValueError:
        release_date_obj = None # Hatalı formatı atla
    
    # --- 2. Movie Nesnesini Oluşturma ---
    movie = Movie(
      id=movie_id,
      imdb_id=str(row.get("imdb_id", "")),
      title=str(row.get("title", "Unknown")),
      poster_path=str(row.get("poster_path", "")),
      vote_average=vote_average,
      vote_count=vote_count,
      release_date=release_date_obj,
      overview=str(row.get("overview", ""))
    )

    # --- 3. Genre (İlişkisel) Verisini İşleme ---
    genre_str = row.get("genres")

    if pd.notna(genre_str) and genre_str:
      try:
        # ast.literal_eval, "[{'id': 16, 'name': 'Animation'}, ...]" 
        # gibi bir string'i güvenle Python listesine çevirir.
        genres_list = ast.literal_eval(genre_str)

        for genre_data in genres_list:
          genre_id = int(genre_data['id'])
          genre_name = genre_data['name']

          # "Get-or-Create" mantığı:
          # Tür, önbelleğimizde (yani DB'de) var mı?
          if genre_id in genres_in_db:
            genre_obj = genres_in_db[genre_id]
          else:
            # Yoksa, yeni bir tane oluştur, session'a ve önbelleğe ekle
            genre_obj = Genre(id=genre_id, name=genre_name)
            session.add(genre_obj) # Yeni türü session'a ekle
            genres_in_db[genre_id] = genre_obj
          
          # SQLAlchemy'nin sihri burada:
          # Sadece nesneyi listeye eklemeniz yeterli.
          # SQLAlchemy, 'movie_genre' ara tablosunu doldurmayı bilir.
          movie.genres.append(genre_obj)

      except (ValueError, SyntaxError):
        # Hatalı 'genres' string'lerini atla
        pass

    movies_to_add.append(movie)

  # Tüm filmleri toplu olarak session'a ekle (daha verimli)
  session.add_all(movies_to_add)
  print(f"{len(movies_to_add)} adet film ve ilişkili türleri oturuma eklendi.")


async def import_ratings_from_csv(session: AsyncSession, csv_path: str):
  df = pd.read_csv(csv_path)
  
  ratings_to_add = []
  for _, row in df.iterrows():
    try:
      rating = Rating(
        user_id = int(row["userId"]),
        movie_id = int(row["movieId"]),
        rating = float(row["rating"]),
      )
      ratings_to_add.append(rating)
      # session.add(rating)
    except (ValueError, TypeError):
      # hatalı satırları geç
      continue

  session.add_all(ratings_to_add)
  print(f"{len(ratings_to_add)} adet reyting oturuma eklendi.")