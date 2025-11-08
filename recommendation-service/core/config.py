from pydantic import BaseModel
import os
from pathlib import Path

class Settings(BaseModel):
  base_dir: Path = Path(__file__).parent
  data_dir: Path = base_dir / "data"

  ratings_path: Path = data_dir / "ratings_small.csv"
  movies_path: Path = data_dir / "movies_metadata.csv"

  database_url: str = os.getenv("DATABASE_URL", "")
  app_env: str = os.getenv("APP_ENV", "dev")
  postgres_user: str = os.getenv("POSTGRES_USER", "")
  postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
  postgres_dbname: str = os.getenv("POSTGRES_DB", "")

settings = Settings()