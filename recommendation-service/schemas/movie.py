from pydantic import BaseModel

class PopularMovieResponse(BaseModel):
  movieId: int
  rating_count: int
  avg_rating: float

  class Config:
    from_attributes = True