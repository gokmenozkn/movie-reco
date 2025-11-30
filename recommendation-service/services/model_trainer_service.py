import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from surprise import dump, Dataset, Reader, SVD
from surprise.model_selection import train_test_split

class ModelTrainerService:
    
    async def _load_ratings_from_db(self, session: AsyncSession):
        pass

    async def train_and_save_model(self, session: AsyncSession, model_path: str):
        pass