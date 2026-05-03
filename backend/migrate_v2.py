from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        print("Starting migrations...")
        
        # 1. Create event_photos table
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS event_photos (
                    id SERIAL PRIMARY KEY,
                    event_id INTEGER NOT NULL,
                    photo_url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            """))
            print("Created event_photos table")
        except Exception as e:
            print(f"Error creating event_photos: {e}")

        # 2. Add registration_link to events
        try:
            conn.execute(text("ALTER TABLE events ADD COLUMN registration_link TEXT"))
            print("Added registration_link to events")
        except Exception as e:
            print(f"registration_link for events skipped: {e}")

        # 3. Add registration_link and deadline to announcements
        try:
            conn.execute(text("ALTER TABLE announcements ADD COLUMN registration_link TEXT"))
            print("Added registration_link to announcements")
        except Exception as e:
            print(f"registration_link for announcements skipped: {e}")

        try:
            conn.execute(text("ALTER TABLE announcements ADD COLUMN deadline TIMESTAMP"))
            print("Added deadline to announcements")
        except Exception as e:
            print(f"deadline for announcements skipped: {e}")
            
        conn.commit()
        print("Migrations completed.")

if __name__ == "__main__":
    run_migration()
