from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON
from database import Base, SessionLocal  # SessionLocal burada önemli!

# SQLAlchemy Model
class CampgroundDB(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type: Optional[str] = None  # Zorunlu olmaktan çıkarıldı
    url = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    region_name = Column(String)
    administrative_area = Column(String, nullable=True)
    nearest_city_name = Column(String, nullable=True)
    accommodation_type_names = Column(JSON, nullable=True)
    bookable = Column(Boolean)
    camper_types = Column(JSON, nullable=True)
    operator = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    photo_urls = Column(JSON, nullable=True)
    photos_count = Column(Integer)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer)
    slug = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    availability_updated_at = Column(DateTime, nullable=True)

# Pydantic Model
class Campground(BaseModel):
    id: str
    type: str
    links: dict
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region_name: Optional[str] = None
    administrative_area: Optional[str] = None
    nearest_city_name: Optional[str] = None
    accommodation_type_names: Optional[List[str]] = []
    bookable: Optional[bool] = None
    camper_types: Optional[List[str]] = []
    operator: Optional[str] = None
    photo_url: Optional[HttpUrl] = None
    photo_urls: Optional[List[HttpUrl]] = []
    photos_count: Optional[int] = 0
    rating: Optional[float] = None
    reviews_count: Optional[int] = 0
    slug: Optional[str] = None
    price_low: Optional[float] = None
    price_high: Optional[float] = None
    availability_updated_at: Optional[datetime] = None

    class Config:
        extra = "ignore"

# Kayıtları veritabanına kaydeden fonksiyon
def save_campgrounds(data):
    db = SessionLocal()
    success_count = 0
    fail_count = 0

    for item in data.get("data", []):
        try:
            attributes = item.get("attributes", {})
            attributes["id"] = item["id"]
            attributes["links"] = item.get("links", {})

            # Doğrulama
            model = Campground.model_validate(attributes)

            # SQLAlchemy modeline çevirme
            db_model = CampgroundDB(
                id=model.id,
                type=model.type,
                url=model.links.get("self"),
                name=model.name,
                latitude=model.latitude,
                longitude=model.longitude,
                region_name=model.region_name,
                administrative_area=model.administrative_area,
                nearest_city_name=model.nearest_city_name,
                accommodation_type_names=model.accommodation_type_names or [],
                bookable=model.bookable,
                camper_types=model.camper_types or [],
                operator=model.operator,
                photo_url=str(model.photo_url) if model.photo_url else None,
                photo_urls=[str(url) for url in model.photo_urls or []],
                photos_count=model.photos_count,
                rating=model.rating,
                reviews_count=model.reviews_count,
                slug=model.slug,
                price_low=model.price_low,
                price_high=model.price_high,
                availability_updated_at=model.availability_updated_at
            )

            db.merge(db_model)  # varsa günceller, yoksa ekler
            db.commit()
            success_count += 1

        except Exception as e:
            print(f"⛔ Skipped invalid record {item.get('id', 'unknown')}: {e}")
            db.rollback()
            fail_count += 1

    db.close()
    print(f"✅ Saved: {success_count} | ❌ Skipped: {fail_count}")
