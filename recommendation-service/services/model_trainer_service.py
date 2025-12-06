import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from surprise import dump, Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sqlalchemy.future import select
from models.database import Rating
import logging

from datetime import datetime
from pathlib import Path
from core.config import settings


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

    async def train_and_save_model(self, session: AsyncSession):
        LATEST_REF_FILE: Path = settings.ml_models_dir / "LATEST_MODEL_PATH.txt"

        try:
            model_dir: Path = settings.ml_models_dir
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            model_filename = f"svd_model_{timestamp}.surprise"
            final_path = (
                model_dir / model_filename
            )  # artifacts/svd_model_20251206_230000.surprise

            # Klasör yoksa oluştur
            final_path.parent.mkdir(parents=True, exist_ok=True)

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
                dump.dump(str(final_path), algo=algo)
                logging.info(f"Model başarıyla {final_path} konumuna kaydedildi.")

                try:
                    with open(LATEST_REF_FILE, "w") as f:
                        f.write(model_filename)

                    logging.info(f"'{model_filename}' en son model olarak işaretlendi.")

                except Exception as e:
                    logging.error(f"LATEST_MODEL_PATH.txt güncellenemedi: {e}")

            except IOError as e:
                logging.error(f"Model dosyaya kaydedilemedi (IO Hatası): {e}")

        except Exception as e:
            logging.error(f"train_and_save_model metodunda bir hata oldu: {e}")
            raise
