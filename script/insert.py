import csv
import psycopg2
import uuid
from db  import get_conn
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "users_sample.csv"
CSV_STOCKS_PATH = BASE_DIR / "users_sample.csv"
batch_size = 500

SQL = """
INSERT INTO users (
    name,
    email
)
VALUES (%s,%s)
"""

SQL_STOCKS = """
INSERT INTO STOCKS (
    product_id,
    quantity
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

def import_stocks():
    with get_conn() as conn:
        with conn.cursor as cur:
            batch = []

            with open(CSV_STOCKS_PATH,newline="",encoding="utf-8") as f:
                reader = csv.DictReader((f))

                for row in reader:
                    batch.append((
                        row["product_id"],
                        row["quantity"]
                    ))

                    if len(batch) >= batch_size:
                        cur.executemany(SQL_STOCKS,batch)
                        batch.clear()

                if batch:
                    cur.executemany(SQL_STOCKS,batch)

    print("STOCKS INSERT OK!")


if __name__ == "__main__":
    import_users()
    import_stocks()