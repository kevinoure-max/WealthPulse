import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()


def get_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is not set")
    conn = psycopg2.connect(url, connect_timeout=10)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS financial_data (
            id          SERIAL PRIMARY KEY,
            date        DATE NOT NULL,
            metric      TEXT NOT NULL,
            value       REAL NOT NULL,
            source      TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def save_data(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()
    records = [
        (row["date"], row["metric"], row["value"], row["source"])
        for _, row in df.iterrows()
    ]
    execute_values(
        cursor,
        """
        INSERT INTO financial_data (date, metric, value, source)
        VALUES %s
        """,
        records,
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_data(metric, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
            SELECT *
            FROM financial_data
            WHERE metric = %s
            """
    params = [metric]

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"
        params.append(end_date)

    cursor.execute(query, params)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    columns = ["id", "date", "metric", "value", "source", "created_at"]
    return pd.DataFrame(rows, columns=columns)
