# 🏕️ The Dyrt Campground Scraper

Bu proje, [The Dyrt](https://thedyrt.com/) platformundaki kamp alanı verilerini otomatik olarak toplayan, doğrulayan ve PostgreSQL veritabanına kaydeden bir scraping sistemidir.

## 🚀 Özellikler

- 📦 Kamp alanı verilerini API üzerinden çeker
- ✅ Pydantic ile veri doğrulama ve modelleme
- 🗺️ Belirli coğrafi koordinatlara göre veri filtreleme
- 🧠 Hatalı kayıtları atlayarak sağlam kayıtları kaydetme
- 🐘 PostgreSQL veritabanına kayıt
- 🐳 Docker ile kolay kurulum ve çalıştırma

## 🛠️ Teknolojiler

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker

## ⚙️ Kullanım

1. PostgreSQL veritabanını kur ve yapılandır.
2. `.env` dosyasını oluştur ve veritabanı bağlantı bilgilerini gir.
3. Docker ile projeyi başlat:

```bash
docker-compose up --build
