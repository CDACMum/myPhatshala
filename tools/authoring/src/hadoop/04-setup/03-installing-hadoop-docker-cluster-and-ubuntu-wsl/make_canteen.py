# make_canteen.py: create the practice file canteen_orders.csv (3 lakh orders)
import os
import random

random.seed(7)                       # same file on every computer
prices = {"chai": 15, "vada pav": 20, "samosa": 18, "poha": 25, "idli": 30, "dosa": 45}
items = list(prices)

with open("canteen_orders.csv", "w") as f:
    f.write("order_id,item,amount\n")
    for order_id in range(1001, 1001 + 300_000):
        item = random.choice(items)
        f.write(f"{order_id},{item},{prices[item]}\n")

print(f"Wrote canteen_orders.csv: 300,000 orders, {os.path.getsize('canteen_orders.csv'):,} bytes")

# Check Hadoop's answer with plain Python
counts = {}
with open("canteen_orders.csv") as f:
    next(f)                          # skip the header
    for line in f:
        item = line.split(",")[1]
        counts[item] = counts.get(item, 0) + 1
for item in ["samosa", "vada pav", "dosa"]:
    print(f"{counts[item]:>6}  {item}")
