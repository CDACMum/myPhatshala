# formats_bench.py: write the same 10 lakh orders as CSV, JSON, Avro, Parquet and ORC,
# then compare file size and how long it takes to answer "total amount" from each.
# Needs:  pip install pyarrow fastavro
import csv, gzip, json, os, random, time
import fastavro
import pyarrow as pa, pyarrow.csv as pacsv, pyarrow.orc as orc, pyarrow.parquet as pq

random.seed(42)
N = 1_000_000
items = ["chai", "coffee", "vada pav", "samosa", "poha", "idli", "dosa", "maggi"]
rows = [{"order_id": i, "canteen": f"C{random.randint(1, 400):03d}", "item": random.choice(items),
         "amount": random.choice([15, 20, 25, 30, 40, 50]), "mode": random.choice(["UPI", "cash", "card"]),
         "ts": 1_760_000_000 + i * 3} for i in range(N)]
cols = list(rows[0])
os.makedirs("formats", exist_ok=True)
results = []

def timed(fn):
    t = time.perf_counter(); out = fn(); return out, time.perf_counter() - t

# ---- write every format -------------------------------------------------
def w_csv():
    with open("formats/orders.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
def w_csv_gz():
    with gzip.open("formats/orders.csv.gz", "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
def w_json():
    with open("formats/orders.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
schema = {"type": "record", "name": "Order", "fields": [
    {"name": "order_id", "type": "long"}, {"name": "canteen", "type": "string"},
    {"name": "item", "type": "string"}, {"name": "amount", "type": "int"},
    {"name": "mode", "type": "string"}, {"name": "ts", "type": "long"}]}
def w_avro():
    with open("formats/orders.avro", "wb") as f: fastavro.writer(f, schema, rows, codec="deflate")
table = pa.Table.from_pylist(rows)
def w_parquet(): pq.write_table(table, "formats/orders.parquet", compression="snappy")
def w_orc(): orc.write_table(table, "formats/orders.orc", compression="zlib")

# ---- answer SUM(amount) from each ---------------------------------------
def r_csv():
    with open("formats/orders.csv") as f: return sum(int(r["amount"]) for r in csv.DictReader(f))
def r_csv_gz():
    with gzip.open("formats/orders.csv.gz", "rt") as f: return sum(int(r["amount"]) for r in csv.DictReader(f))
def r_json():
    with open("formats/orders.jsonl") as f: return sum(json.loads(l)["amount"] for l in f)
def r_avro():
    with open("formats/orders.avro", "rb") as f: return sum(r["amount"] for r in fastavro.reader(f))
def r_parquet(): return pa.compute.sum(pq.read_table("formats/orders.parquet", columns=["amount"])["amount"]).as_py()
def r_orc(): return pa.compute.sum(orc.read_table("formats/orders.orc", columns=["amount"])["amount"]).as_py()
def r_csv_arrow(): return pa.compute.sum(pacsv.read_csv("formats/orders.csv")["amount"]).as_py()

import pyarrow.compute
for name, path, w, r in [("CSV", "orders.csv", w_csv, r_csv), ("CSV, fast reader", "orders.csv", None, r_csv_arrow),
                         ("CSV + gzip", "orders.csv.gz", w_csv_gz, r_csv_gz),
                         ("JSON Lines", "orders.jsonl", w_json, r_json), ("Avro (deflate)", "orders.avro", w_avro, r_avro),
                         ("Parquet (snappy)", "orders.parquet", w_parquet, r_parquet), ("ORC (zlib)", "orders.orc", w_orc, r_orc)]:
    _, wt = timed(w) if w else (None, 0.0)
    total, rt = timed(r)
    results.append((name, os.path.getsize("formats/" + path), wt, rt, total))

base = results[0][1]
print(f"{N:,} orders, 6 columns\n")
print(f"{'format':17}{'size MB':>9}{'vs CSV':>8}{'write s':>9}{'SUM(amount) s':>15}  total")
for name, size, wt, rt, total in results:
    wcol = f"{wt:9.2f}" if wt else f"{'-':>9}"
    print(f"{name:17}{size / 1e6:9.1f}{size / base:8.0%}{wcol}{rt:15.3f}  {total:,}")

# Parquet keeps statistics per column chunk: the reader can skip data without opening it
meta = pq.ParquetFile("formats/orders.parquet").metadata
rg = meta.row_group(0)
print(f"\nParquet: {meta.num_row_groups} row group(s), {meta.num_columns} columns")
st = rg.column(3).statistics
print(f"column 'amount' in row group 0: min={st.min} max={st.max} nulls={st.null_count}")
print("schema stored in the file:", pq.read_schema("formats/orders.parquet").names)
