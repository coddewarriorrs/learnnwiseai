import os
import time
import uvicorn
from sqlalchemy import text
from app.database import engine, Base

def init_db_and_seed():
    print("Checking database connection...")
    for i in range(15):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established successfully!")
            break
        except Exception as e:
            print(f"Waiting for database (attempt {i+1}/15): {e}")
            time.sleep(2)
    
    print("Ensuring database tables are created...")
    Base.metadata.create_all(bind=engine)

    # Ensure any new columns exist in existing PostgreSQL tables
    try:
        with engine.connect() as conn:
            cols = [
                ("answer_records", "mistake_type", "VARCHAR(100)"),
                ("answer_records", "explanation_brief", "TEXT"),
                ("answer_records", "explanation_full", "TEXT"),
                ("answer_records", "concept_involved", "VARCHAR(255)"),
                ("answer_records", "how_to_avoid", "TEXT"),
                ("ai_messages", "image_url", "TEXT"),
                ("ai_messages", "audio_url", "TEXT"),
                ("ai_messages", "image_analysis", "JSON"),
            ]
            for table, col, col_type in cols:
                try:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type};"))
                    conn.commit()
                except Exception:
                    pass
    except Exception as e:
        print(f"Schema update note: {e}")
    
    if os.getenv("AUTO_SEED", "true").lower() in ("true", "1", "yes"):
        try:
            print("Verifying database seed data...")
            from seed import run_seed
            run_seed()
            print("Database seed verification complete.")
        except Exception as e:
            print(f"Seed note: {e}")

if __name__ == "__main__":
    init_db_and_seed()
    print("Starting LearnWise AI Backend on http://0.0.0.0:8000 ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

