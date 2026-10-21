import csv, os, random, time

random.seed(7)
items = [("chai", 20), ("coffee", 25), ("vada pav", 25), ("samosa", 15), ("poha", 30)]
start = time.time()
with open("orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["txn_id", "item", "amount", "mode", "day"])
    for i in range(1, 1_500_001):
        item, price = random.choice(items)
        w.writerow([f"T{i}", item, price, random.choice(["UPI", "cash"]), i // 3700 + 1])
secs = time.time() - start
print("Rows written :", 1_500_000)
print("File size    :", round(os.path.getsize("orders.csv") / 1024**2, 1), "MB")
print("Time taken   :", round(secs, 1), "seconds")
print("Excel limit  :", 1_048_576, "rows -> this file is too big for one sheet")
