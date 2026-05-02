import os
import pandas as pd
from sqlalchemy import create_engine, text

def get_engine():
    db_url = os.getenv("DATABASE_URL", "postgresql://f1user:f1password@db:5432/f1db")
    return create_engine(db_url)

def upsert_df(df, table_name, constraint_cols=None):
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql("temp_table", conn, if_exists="replace", index=False)
        cols = ", ".join(df.columns)
        query = f"""
            INSERT INTO {table_name} ({cols})
            SELECT {cols} FROM temp_table
            ON CONFLICT ({", ".join(constraint_cols) if constraint_cols else ""}) 
            DO NOTHING;
        """
        if constraint_cols:
            conn.execute(text(query))
        else:
            df.to_sql(table_name, conn, if_exists="append", index=False)
    print(f"✅ Data upserted to table: {table_name}")