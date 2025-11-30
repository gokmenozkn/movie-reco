from surprise import dump
from fastapi import FastAPI, HTTPException
from routers import router as api_router
from core.logger import configure_logging

configure_logging()

print("Uygulama başarıyla başlatıldı ve hazır.")

app = FastAPI(
  title="Movie Reco"
)

app.include_router(api_router)

# --- 5. API ENDPOINTS (DIŞARIYA AÇILAN FONKSİYONLAR) ---

@app.get("/", tags=["Status"])
def read_root():
  """API'nin çalışıp çalışmadığını kontrol etmek için basit bir endpoint."""
  return {"status": "OK", "message": "Film Öneri API'sine hoş geldiniz!"}
