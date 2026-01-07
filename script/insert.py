import csv
import psycopg2
from db  import get_conn

CSV_PATH = "./users_sample_csv"
batch_size = 500

SQL = """
INSERT INTO users (
    user_id,
    user_name,
    email,
    create_at
)
VALUES (%s,%s,%s,%s)
"""

def import_users():
    with get_conn() as conn:
        with conn.cursor() as cur:
            batch = []

            with open(CSV_PATH,newline="",encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    batch.append((
                        int(row["user_id"]),
                        row["user_name"],
                        row["email"],
                        row["create_at"]
                    ))

                    if len(batch) >= batch_size:
                        cur.executemany(SQL,batch)
                        batch.clear()

                if batch:
                    cur.executemany(SQL,batch)
    print("bulk insert OK")

if __name__ == "__main__":
    import_users()