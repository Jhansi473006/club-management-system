from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN profile_photo_url VARCHAR"))
            print("Added profile_photo_url to users")
        except Exception as e:
            print(f"profile_photo_url skipped or already exists: {e}")
            
        conn.commit()

if __name__ == "__main__":
    run_migration()
