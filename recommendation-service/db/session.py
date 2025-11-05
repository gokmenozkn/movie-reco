from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.database_url, echo=(settings.app_env == "dev"))

async_session_factory = async_sessionmaker(
  bind=engine,
  expire_on_commit=False,
  autoflush=False,
  autocommit=False,
  class_=AsyncSession
)

async def get_db() -> AsyncSession:
  async with async_session_factory() as session:
    try:
      yield session
    finally:
      await session.close()