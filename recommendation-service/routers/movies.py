from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services import import_service

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/popular")
def get_popular():
    return { "message": "Popüler filmler yakında" }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_movies(
    db: AsyncSession = Depends(get_db)
):
    """
    CSV dosyalarından filmleri, türleri ve reytingleri veritabanına aktarır.
    Tüm işlemler 'atomik' bir transaction içinde yürütülür.
    """

    # CSV dosyalarınızın bulunduğu yolları buraya yazın
    MOVIES_METADATA_PATH = "movies_metadata.csv"
    RATINGS_PATH = "ratings_small.csv"

    try:
        print("Veri aktarımı başlıyor...")

        await import_service.import_movies_and_genres_from_csv(session=db, csv_path=MOVIES_METADATA_PATH)

        await import_service.import_ratings_from_csv(session=db, csv_path=RATINGS_PATH)

        await db.commit()

        print("Veri aktarımı başarıyla tamamlandı.")
        return {"message": "Filmler, türler ve reytingler başarıyla veritabanına aktarıldı."}

    except FileNotFoundError as e:
        print(f"HATA: Dosya bulunamadı - {e.filename}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dosya bulunamadı: {e.filename}"
        )
    
    except Exception as e:
        # Eğer import_movies veya import_ratings sırasında herhangi bir hata olursa,
        # 'commit' asla çalışmaz ve 'rollback' ile tüm değişiklikler geri alınır.
        # Veritabanınız güvende kalır.
        print(f"HATA: Veri aktarımı sırasında bir hata oluştu: {str(e)}")
        await db.rollback() # İşlemi geri al
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Veri aktarımı başarısız oldu: {str(e)}"
        )