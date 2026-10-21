# one_machine.py: how much data can ONE ordinary computer aggregate quickly?
import random, time, csv, os, tempfile

random.seed(1)
items = ["chai", "vada pav", "samosa", "poha", "idli", "dosa", "thali", "lassi"]
rows = 2_000_000
path = os.path.join(tempfile.gettempdir(), "orders_2m.csv")

t0 = time.time()
with open(path, "w", newline="") as f:
    w = csv.writer(f)
    for i in range(rows):
        w.writerow([i, random.choice(items), random.randint(10, 300)])
t1 = time.time()

totals = {}
with open(path, newline="") as f:
    for _, item, amount in csv.reader(f):
        totals[item] = totals.get(item, 0) + int(amount)
t2 = time.time()

size_mb = os.path.getsize(path) / 1024 / 1024
print(f"Rows: {rows:,}  File: {size_mb:.0f} MB")
print(f"Write: {t1 - t0:.1f} s   Group-by in plain Python: {t2 - t1:.1f} s")
print("Top item:", max(totals, key=totals.get))
print(f"Rough speed: {rows / (t2 - t1) / 1e6:.1f} million rows per second on one core")
os.remove(path)
