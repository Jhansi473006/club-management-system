from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        cols = [
            "instructions TEXT",
            "helpline VARCHAR",
            "registration_deadline TIMESTAMP WITH TIME ZONE"
        ]
        for col in cols:
            try:
                conn.execute(text(f"ALTER TABLE events ADD COLUMN {col}"))
                print(f"Added column {col} to events")
            except Exception as e:
                print(f"Column {col} skipped or already exists: {e}")
        
        conn.commit()

if __name__ == "__main__":
    run_migration()
