import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from surprise import dump, Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sqlalchemy.future import select
from models.database import Rating
import logging


class ModelTrainerService:
    async def _load_ratings_from_db(self, session: AsyncSession) -> pd.DataFrame:
        try:
            logging.info("Model eğitmek için Rating verileri yükleniyor")

            result = await session.execute(
                select(Rating.user_id, Rating.movie_id, Rating.rating)
            )
            ratings_data = result.all()

            logging.info("Veritabanından veriler başarıyla yüklendi.")

            return pd.DataFrame(ratings_data, columns=["userId", "movieId", "rating"])
        except Exception as e:
            logging.error(
                f"Model eğitmek için Rating tablosu yüklenirken bir hata oluştu: {e}"
            )
            raise RuntimeError(
                f"Model eğitmek için Rating tablosu yüklenirken bir hata oluştu: {e}"
            )

    async def train_and_save_model(self, session: AsyncSession, model_path: str):
        try:
            ratings_df = await self._load_ratings_from_db(session)

            if ratings_df.empty:
                logging.warning(
                    "Rating tablosundan hiç veri gelmedi. Model eğitimi atlanıyor."
                )
                return

            ratings_df = ratings_df.astype(
                {"userId": "int32", "movieId": "int32", "rating": "float32"}
            )

            reader = Reader(rating_scale=(0.5, 5.0))
            data = Dataset.load_from_df(
                ratings_df[["userId", "movieId", "rating"]], reader
            )

            # Model eğitimi
            trainset, testset = train_test_split(data, test_size=0.2)

            logging.info(f"Eğitim setinin boyutu: {trainset.n_ratings}")
            logging.info(f"Test setinin boyutu: {len(testset)}")

            algo = SVD()
            logging.info("Model eğitimi başlıyor...")

            try:
                algo.fit(trainset)
                logging.info("Model eğitimi tamamlandı.")
            except Exception as e:
                logging.error(
                    f"SVD model eğitimi sırasında kritik bir hata oluştu: {e}"
                )
                return  # başarısız olursa durdur

            # Modeli dosyaya kaydet
            try:
                dump.dump(model_path, algo=algo)
                logging.info(f"Model başarıyla {model_path} konumuna kaydedildi.")
            except IOError as e:
                logging.error(f"Model dosyaya kaydedilemedi (IO Hatası): {e}")

        except Exception as e:
            logging.error(f"train_and_save_model metodunda bir hata oldu: {e}")
            raise
