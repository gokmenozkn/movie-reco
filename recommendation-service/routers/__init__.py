from fastapi import APIRouter
from .movies import router as movies_router
from .ratings import router as ratings_router

router = APIRouter()

router.include_router(movies_router)
router.include_router(ratings_router)