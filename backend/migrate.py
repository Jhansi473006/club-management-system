from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE coordinators ADD COLUMN photo_url VARCHAR"))
            print("Added photo_url to coordinators")
        except Exception as e:
            print(f"photo_url skipped or already exists: {e}")
            
        conn.commit()

if __name__ == "__main__":
    run_migration()
