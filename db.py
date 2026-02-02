import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE")
    )

def init_schema(conn):
    with conn.cursor() as cur:
        with open("schema.sql","r") as f:
            cur.execute(f.read())
    conn.commit()

if __name__ == "__main__":
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("DB_OK:",cur.fetchone())
    conn = get_conn()
    init_schema(conn)
    print("schema_OK")
    cur.close()
    conn.close()