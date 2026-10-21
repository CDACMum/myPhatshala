"""Write the same 2 lakh orders as CSV, CSV.gz, JSON lines, Avro, Parquet and ORC,
then compare file sizes and the time to answer one question.
Needs:  pip install pyarrow fastavro"""
import csv, gzip, json, os, random, time
import fastavro
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.orc as orc
import pyarrow.parquet as pq

def inr(n):
    """Indian digit grouping: 18977156 -> 1,89,77,156"""
    s = str(n)
    head, tail = s[:-3], s[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail
        head = head[:-2]
    return (head + "," + tail) if head else tail


random.seed(7)
N = 200_000
cities = ["Pune", "Mumbai", "Nashik", "Nagpur", "Thane"]
dishes = ["thali", "dosa", "biryani", "pav bhaji", "lassi", "chai"]
rows = [{"order_id": i, "city": random.choice(cities), "dish": random.choice(dishes),
         "amount": random.randint(40, 900), "day": f"2026-10-{random.randint(1, 31):02d}"} for i in range(N)]
os.makedirs("formats", exist_ok=True)
cols = list(rows[0])

with open("formats/orders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
with gzip.open("formats/orders.csv.gz", "wt", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
with open("formats/orders.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
schema = {"name": "Order", "type": "record", "fields": [
    {"name": "order_id", "type": "long"}, {"name": "city", "type": "string"},
    {"name": "dish", "type": "string"}, {"name": "amount", "type": "int"}, {"name": "day", "type": "string"}]}
with open("formats/orders.avro", "wb") as f:
    fastavro.writer(f, fastavro.parse_schema(schema), rows, codec="deflate")
table = pa.Table.from_pylist(rows)
pq.write_table(table, "formats/orders.parquet", compression="snappy")
orc.write_table(table, "formats/orders.orc", compression="zstd")

print("File sizes for", inr(N), "orders:")
base = os.path.getsize("formats/orders.csv")
for name in ["orders.csv", "orders.jsonl", "orders.csv.gz", "orders.avro", "orders.parquet", "orders.orc"]:
    size = os.path.getsize("formats/" + name)
    print(f"  {name:15} {size / 1024 / 1024:6.2f} MB   ({size / base * 100:5.1f}% of CSV)")

# Question: total amount for Pune. A row format must read every column of every row.
t = time.perf_counter()
total = 0
with open("formats/orders.csv") as f:
    for r in csv.DictReader(f):
        if r["city"] == "Pune":
            total += int(r["amount"])
csv_s = time.perf_counter() - t

t = time.perf_counter()
part = pq.read_table("formats/orders.parquet", columns=["city", "amount"])
pq_total = pc.sum(pc.filter(part["amount"], pc.equal(part["city"], "Pune"))).as_py()
pq_s = time.perf_counter() - t

print(f"\nTotal for Pune from CSV    : Rs {inr(total)}")
print(f"Total for Pune from Parquet: Rs {inr(pq_total)}  (read only 2 of 5 columns)")
print(f"Parquet was about {csv_s / pq_s:.0f}x faster on this machine")
meta = pq.ParquetFile("formats/orders.parquet").metadata
print(f"Parquet footer: {meta.num_row_groups} row group(s), {meta.num_columns} columns, schema stored inside the file")
