from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# DATABASE_URL = "postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>"
db_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@localhost:5432/{settings.postgres_dbname}"

engine = create_async_engine(settings.get_database_url, echo=(settings.app_env == "dev"))

async_session_factory = async_sessionmaker(
  bind=engine,
  expire_on_commit=False,
  autoflush=False,
  autocommit=False,
  class_=AsyncSession
)

async def get_db():
  async with async_session_factory() as session:
    try:
      yield session
    finally:
      await session.close()