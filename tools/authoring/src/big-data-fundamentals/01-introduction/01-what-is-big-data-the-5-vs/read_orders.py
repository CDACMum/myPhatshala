import csv, time
from collections import Counter

start = time.time()
sales = Counter()
with open("orders.csv") as f:
    for row in csv.DictReader(f):
        sales[row["item"]] += int(row["amount"])
print("Read 15 lakh rows in", round(time.time() - start, 1), "seconds")
for item, rs in sales.most_common():
    print(f"{item:10} Rs {rs:,}")
