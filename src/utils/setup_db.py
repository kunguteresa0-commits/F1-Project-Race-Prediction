from sqlalchemy import text
from src.utils.db import get_engine
from pathlib import Path

def init_db():
    engine = get_engine()
    schema_path = Path("sql/schema.sql")
    
    if not schema_path.exists():
        print(f"❌ Could not find {schema_path}")
        return

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    with engine.begin() as conn:
        print("🛠️ Creating tables in SQL...")
        for statement in schema_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))
    print("✅ Database schema initialized!")

if __name__ == "__main__":
    init_db()