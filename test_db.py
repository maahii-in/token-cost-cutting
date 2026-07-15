import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(".env"), override=True)

print("Connecting to PostgreSQL...")

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT")),
    dbname=os.getenv("POSTGRES_DB"),   # use dbname
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

print("✅ Connected successfully!")

cur = conn.cursor()
cur.execute("SELECT version();")

print(cur.fetchone()[0])

cur.close()
conn.close()