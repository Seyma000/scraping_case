
from sqlalchemy import text
from database import engine, init_db, SessionLocal, CampgroundDB

# 1. Drop table if exists
with engine.connect() as conn:
    print("🧹 Dropping existing 'campgrounds' table if it exists...")
    conn.execute(text("DROP TABLE IF EXISTS campgrounds CASCADE;"))
    conn.commit()

# 2. Recreate table
print("🛠 Recreating table with SQLAlchemy models...")
init_db()

# 3. Test connection and count records
db = SessionLocal()
count = db.query(CampgroundDB).count()
print(f"✅ Table created. Current record count: {count}")
db.close()
