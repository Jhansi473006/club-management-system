from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE announcements ADD COLUMN poster_url VARCHAR"))
            print("Successfully added column poster_url to announcements")
        except Exception as e:
            print(f"Column poster_url skipped or already exists: {e}")
        
        conn.commit()

if __name__ == "__main__":
    run_migration()
