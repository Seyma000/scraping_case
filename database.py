from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/campgrounds"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CampgroundDB(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    url = Column(String)  # From links.self
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    region_name = Column(String)
    administrative_area = Column(String, nullable=True)
    nearest_city_name = Column(String, nullable=True)
    accommodation_type_names = Column(JSON)
    bookable = Column(Boolean)
    camper_types = Column(JSON)
    operator = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    photo_urls = Column(JSON)
    photos_count = Column(Integer)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer)
    slug = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    availability_updated_at = Column(DateTime, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)