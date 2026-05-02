from src.utils.db import get_engine
from sqlalchemy import text

engine = get_engine()
with engine.connect() as conn:
    # 1. Add constructor_id to results (if it's missing)
    conn.execute(text("ALTER TABLE results ADD COLUMN IF NOT EXISTS constructor_id TEXT"))
    
    # 2. Add team_form to features (so training doesn't fail)
    conn.execute(text("ALTER TABLE features ADD COLUMN IF NOT EXISTS team_form FLOAT"))
    
    conn.commit()
    print("✅ Database columns added!")