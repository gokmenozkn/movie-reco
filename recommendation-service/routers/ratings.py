from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/")
async def rate_movie():
    return { "message": "Ratings sekmesine hoşgeldiniz..." }