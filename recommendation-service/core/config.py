from pydantic import BaseModel
import os

class Settings(BaseModel):
  database_url: str = os.getenv("DATABASE_URL", "")
  app_env: str = os.getenv("APP_ENV", "dev")

settings = Settings()