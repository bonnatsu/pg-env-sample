import csv

row_count = 10000
output_file = "users_sample_csv"

with open(output_file,"w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name","email"])

    for i in range(1,row_count + 1):
        name = f"user{i:05d}"
        email = f"user{i:05d}@test.com"
        writer.writerow([name,email])

print(f"CSV GENERATED: {row_count} rows -> {output_file}")