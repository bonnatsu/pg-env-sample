import csv
import uuid
import random
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

output_file = BASE_DIR / "users_sample.csv"
row_count = 10000

with open(output_file,"w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name","email"])

    for i in range(1,row_count + 1):
        name = f"user{i:05d}"
        email = f"user_{uuid.uuid4()}@test.com"
        writer.writerow([name,email])

output_file = BASE_DIR / "stocks.csv"
row_count = 5000
with open(output_file,"w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([product_id,quantity])

    for i in range(1,row_count + 1):
        product_id = i
        quantity = random.randint(0,10000)
        writer.writerow([product_id,quantity])


print(f"CSV GENERATED: CREATE OK!")