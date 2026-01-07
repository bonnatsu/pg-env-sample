import csv
import psycopg2
from db  import get_conn
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "users_sample.csv"
batch_size = 500

SQL = """
INSERT INTO users (
    user_name,
    email
)
VALUES (%s,%s)
"""

def import_users():
    with get_conn() as conn:
        with conn.cursor() as cur:
            batch = []

            with open(CSV_PATH,newline="",encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    batch.append((
                        row["name"],
                        row["email"],
                    ))

                    if len(batch) >= batch_size:
                        cur.executemany(SQL,batch)
                        batch.clear()

                if batch:
                    cur.executemany(SQL,batch)
    print("bulk insert OK")

if __name__ == "__main__":
    import_users()