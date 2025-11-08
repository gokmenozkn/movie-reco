from surprise import dump
from fastapi import FastAPI, HTTPException
from services.recommendation_service import RecommendationService
import pandas as pd
import os
from typing import List
from schemas.movie import PopularMovieResponse
from routers import router as api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "recommendation_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "ratings_small.csv")

COLD_START_RATING_THRESHOLD = 10

recommender = RecommendationService(MODEL_PATH, DATA_PATH)

print("Uygulama başarıyla başlatıldı ve hazır.")

app = FastAPI(
  title="Movie Reco"
)

app.include_router(api_router)

# --- 5. API ENDPOINTS (DIŞARIYA AÇILAN FONKSİYONLAR) ---

@app.get("/", tags=["Status"])
def read_root():
  """API'nin çalışıp çalışmadığını kontrol etmek için basit bir endpoint."""
  return {"status": "OK", "message": "Film Öneri API'sine hoş geldiniz!"}


@app.get("/recommend/{user_id}", tags=["Recommendations"])
def recommend_for_user(user_id: int):
  """
  Bir kullanıcı ID'si için film önerileri döndürür.
  Eğer kullanıcının yeterli sayıda oyu yoksa (soğuk başlangıç),
  en popüler filmleri önerir. Aksi takdirde, kişiselleştirilmiş öneriler sunar.
  """
  # Veri setinde böyle bir kullanıcı olup olmadığını kontrol et
  
  # if user_rating_count < COLD_START_RATING_THRESHOLD:
  #   # Soğuk Başlangıç: Popüler filmleri öner
  #   recommendation_type = "popular"
  #   # recommendations = get_popular_recommendations()
  #   recommendations = recommender.get_popular_movies()
  # else:
  #   # Kişiselleştirilmiş Öneri: SVD modelini kullan 
  #   recommendation_type = "personalized"
  #   recommendations = get_personalized_recommendations(user_id)
      
  recommendation_type = 'popular'
  return {
    "user_id": user_id,
    "type": recommendation_type
  }

@app.get('/movies/popular', response_model=List[PopularMovieResponse])
def popular_movies_endpoint():
  popular_movies = recommender.get_popular_movies()
  movies_list = popular_movies.to_dict('records')

  return movies_list