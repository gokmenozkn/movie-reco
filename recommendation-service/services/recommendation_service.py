import pandas as pd
from surprise import dump
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RecommendationService:
  def __init__(self, model_path: str, ratings_path: str):
    self.model_path = model_path
    self.ratings_path = ratings_path
    
    self.model = None
    self.ratings_df: pd.DataFrame = None
    self._popular_movies_cache = None

  def _load_model(self):
    """
    Modeli dosyadan yükler.
    """
    try:
      logging.info(f"Model yükleniyor: {self.model_path}")
      _, self.model = dump.load(self.model_path)
      logging.info("Model başarıyla yüklendi.")
    except FileNotFoundError:
      logging.error(f"Model dosyası bulunamadı: {self.model_path}")
      raise RuntimeError(f"Model dosyası bulunamadı: {self.model_path}")
    except Exception as e:
      logging.error(f"Model yüklenirken beklenmedik bir hata oluştu: {e}")
      raise RuntimeError(f"Model yüklenirken bir hata oluştu: {e}")
  
  def get_model(self):
    """
    Modeli döndürür.
    """
    if self.model is None:
      self._load_model()
    
    return self.model
  
  def _load_data(self):
    """
    CSV dosyalarını yükler.
    """

    try:
      logging.info(f"Derecelendirme verisi yükleniyor: {self.ratings_path}")
      self.ratings_df = pd.read_csv(self.ratings_path)
      logging.info("Ratings CSV başarıyla yüklendi.")
    
    except FileNotFoundError as e:
      logging.error(f"Veri dosyası bulunamadı: {e.filename}")
      raise RuntimeError(f"Veri dosyası bulunamadı: {e.filename}")
    except Exception as e:
      logging.error(f"Veri yüklenirken beklenmedik bir hata oluştu: {e}")
      raise RuntimeError(f"Veri yüklenirken beklenmedik bir hata oluştu: {e}")

  def _get_dataframes(self):
    """
    Veri setlerini döndürür.
    """
    if self.ratings_df is None:
      self._load_data()
    return self.ratings_df

  def predict(self, user_id, item_id):
    model = self.get_model()
    
    if model:
      prediction = model.predict(uid=user_id, iid=item_id)
      return prediction
    else:
      raise RuntimeError("Tahmin için model yüklenemedi")

  def get_popular_movies(self, top_n: int = 10, min_ratings_threshold: int = 100):
    """
    En popüler filmleri listeler.
    Popülerlik belirli bir eşiğin üstünde oy almış filmlerin ortalama
    puanına göre belirlenir

    Args:
      top_n (int): Döndürülecek film sayısı
      min_ratings_threshold (int): Bir filmin listeye girmesi için gereken oy min sayısı

    Returns:
      pandas.Dataframe: Popüler filmleri içeren bir dataframe
                        (rating_count, avg_rating sütunları).
    """
    
    if self._popular_movies_cache is None:
      logging.info("Popüler filmler listesi hesaplanıyor...")
      ratings = self._get_dataframes()

      # movie_ratings_count = ratings.groupby('moveId').size().reset_index(name='rating_count')
      # popular_movie_ids = movie_ratings_count[
      #   movie_ratings_count['rating_count'] >= min_ratings_threshold
      # ]

      movie_stats = ratings.groupby('movieId')['rating'].agg(
        rating_count='count',
        avg_rating='mean'
      ).reset_index()

      popular_movie_stats = movie_stats[movie_stats['rating_count'] >= min_ratings_threshold]
      top_movies = popular_movie_stats.sort_values(
          by=['avg_rating', 'rating_count'], 
          ascending=[False, False]
        ).head(top_n).reset_index(drop=True)
      
      self._popular_movies_cache = top_movies
      logging.info("Popüler filmler hazırlandı")
      
    return self._popular_movies_cache

  def get_personalized_recommendations(self, user_id: int, n=10):
    pass