from pydantic import BaseModel
import os
from pathlib import Path
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Load env
load_dotenv()


class Settings(BaseModel):
	base_dir: Path = Path(__file__).parent.parent
	data_dir: Path = base_dir / "data"
	ml_models_dir: Path = base_dir / "artifacts"

	ratings_path: Path = data_dir / "ratings_small.csv"
	movies_path: Path = data_dir / "movies_metadata.csv"

	# Varsayılan ML model adı
	DEFAULT_MODEL_FILE = "svd_model.surprise"

	app_env: str = os.getenv("APP_ENV", "dev")
	postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
	postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
	postgres_dbname: str = os.getenv("POSTGRES_DB", "recommendation_db")
	postgres_host: str = "localhost"
	postgres_port: str = "5432"

	@property
	def model_path(self) -> Path:
		return self.ml_models_dir / self.DEFAULT_MODEL_FILE

	# Async engine ile PostgreSQL url
	@property
	def get_database_url(self) -> str:
		print(f"db password: {self.postgres_password}")
		print(f"db user: {self.postgres_user}")

		return URL.create(
			"postgresql+asyncpg",
			self.postgres_user,
			self.postgres_password,
			self.postgres_host,
			self.postgres_port,
			self.postgres_dbname,
		).render_as_string(hide_password=False)

	# Senkron PostgreSQL url
	@property
	def get_sync_db_url(self) -> str:
		return URL.create(
			"postgresql+psycopg2",
			self.postgres_user,
			self.postgres_password,
			self.postgres_host,
			self.postgres_port,
			self.postgres_dbname,
		).render_as_string(hide_password=False)


settings = Settings()
