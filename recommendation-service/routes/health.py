from fastapi import APIRouter

router = APIRouter()

@router.get('/ready')
async def readiness_check():
  """K8s readiness probe"""
  return {"status": "ready"}

@router.get("/live")
async def liveness_check():
    """K8s liveness probe"""
    return {"status": "live"}