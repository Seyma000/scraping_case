import httpx
import time
from src.models.campground import Campground
from database import SessionLocal, CampgroundDB
from sqlalchemy.exc import IntegrityError

API_URL = "https://thedyrt.com/api/v6/locations/search-results"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_campgrounds(bbox: tuple[float, float, float, float]):
    params = {
        "filter[search][drive_time]": "any",
        "filter[search][air_quality]": "any",
        "filter[search][electric_amperage]": "any",
        "filter[search][max_vehicle_length]": "any",
        "filter[search][price]": "any",
        "filter[search][rating]": "any",
        "filter[search][bbox]": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "sort": "recommended",
        "page[number]": 1,
        "page[size]": 500
    }
    with httpx.Client(headers=HEADERS) as client:
        response = client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()

def save_campgrounds(data):
    print("🔍 API response:", data)  # Print full API response for debug
    db = SessionLocal()
    for item in data.get("data", []):
        try:
            attributes = item.get("attributes", {})
            attributes["id"] = item["id"]
            attributes["links"] = item.get("links", {})
            print("🔎 Sample campground data:", attributes)
            break  # sadece ilk kampı göster ve çık

            model = Campground.model_validate(attributes)

            db_model = CampgroundDB(
                id=model.id,
                type=model.type,
                url=model.links.self,
                name=model.name,
                latitude=model.latitude,
                longitude=model.longitude,
                region_name=model.region_name,
                administrative_area=model.administrative_area,
                nearest_city_name=model.nearest_city_name,
                accommodation_type_names=model.accommodation_type_names,
                bookable=model.bookable,
                camper_types=model.camper_types,
                operator=model.operator,
                photo_url=str(model.photo_url) if model.photo_url else None,
                photo_urls=[str(url) for url in model.photo_urls],
                photos_count=model.photos_count,
                rating=model.rating,
                reviews_count=model.reviews_count,
                slug=model.slug,
                price_low=model.price_low,
                price_high=model.price_high,
                availability_updated_at=model.availability_updated_at
            )
            db.merge(db_model)
            db.commit()
        except Exception as e:
            print(f"⛔ Skipped invalid record {item.get('id', 'unknown')}: {e}")
            db.rollback()
    db.close()

def run_nationwide_scrape():
    min_lng, max_lng = -125, -66
    min_lat, max_lat = 24, 49
    step = 1.0

    lat = min_lat
    while lat < max_lat:
        lng = min_lng
        while lng < max_lng:
            bbox = (lng, lat, lng + step, lat + step)
            print(f"📦 Fetching bbox: {bbox}")
            try:
                data = fetch_campgrounds(bbox)
                save_campgrounds(data)
                return  # sadece bir bbox işlenip çıkılsın diye eklendi
            except Exception as e:
                print(f"❌ Error in bbox {bbox}: {e}")
            time.sleep(0.5)
            lng += step
        lat += step

if __name__ == "__main__":
    run_nationwide_scrape()