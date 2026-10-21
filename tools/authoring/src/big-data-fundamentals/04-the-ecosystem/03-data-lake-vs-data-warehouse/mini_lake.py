import csv, json, os, sqlite3

# ---------- BRONZE: the data lake keeps raw data exactly as it arrived ----------
raw_dir = os.path.join("lake", "bronze", "orders", "date=2026-10-19")
os.makedirs(raw_dir, exist_ok=True)
raw_events = [
    {"order_id": 1, "kitchen": "K11", "item": "thali", "amount": 120},
    {"order_id": 2, "kitchen": "K12", "item": "biryani", "amount": "250"},   # amount as text
    {"order_id": 2, "kitchen": "K12", "item": "biryani", "amount": "250"},   # duplicate (retry)
    {"order_id": 3, "kitchen": "K13", "item": "dosa", "amount": -90},        # impossible amount
    {"order_id": 4, "kitchen": "K11", "item": "thali", "amount": 120, "coupon": "LUNCH20"},  # new field!
]
with open(os.path.join(raw_dir, "part-0001.json"), "w") as f:
    for e in raw_events:
        f.write(json.dumps(e) + "\n")
with open(os.path.join("lake", "bronze", "review_0001.txt"), "w") as f:
    f.write("Thali was hot and tasty, delivery 5 min late.")
print("BRONZE :", len(raw_events), "raw order events + 1 review file saved, nothing rejected")

# ---------- SILVER: schema-on-READ - impose structure when we read ----------
clean, seen = [], set()
with open(os.path.join(raw_dir, "part-0001.json")) as f:
    for line in f:
        r = json.loads(line)
        if r["order_id"] in seen:
            continue
        seen.add(r["order_id"])
        clean.append({"order_id": r["order_id"], "kitchen": r["kitchen"], "amount": int(r["amount"])})
os.makedirs(os.path.join("lake", "silver"), exist_ok=True)
with open(os.path.join("lake", "silver", "orders.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["order_id", "kitchen", "amount"])
    w.writeheader(); w.writerows(clean)
print("SILVER :", len(clean), "rows after de-duplication and type fixes")

# ---------- GOLD: a warehouse with schema-on-WRITE (rules checked on insert) ----------
if os.path.exists("warehouse.db"):
    os.remove("warehouse.db")
db = sqlite3.connect("warehouse.db")
db.execute("CREATE TABLE dim_kitchen (kitchen TEXT PRIMARY KEY, city TEXT NOT NULL)")
db.execute("""CREATE TABLE fact_orders (order_id INTEGER PRIMARY KEY,
              kitchen TEXT REFERENCES dim_kitchen(kitchen),
              amount INTEGER NOT NULL CHECK (amount > 0))""")
db.executemany("INSERT INTO dim_kitchen VALUES (?, ?)", [("K11", "Pune"), ("K12", "Pune"), ("K13", "Mumbai")])
for r in clean:
    try:
        db.execute("INSERT INTO fact_orders VALUES (?, ?, ?)", (r["order_id"], r["kitchen"], r["amount"]))
    except sqlite3.IntegrityError as err:
        print("GOLD   : rejected order", r["order_id"], "->", err)
db.commit()

query = """SELECT k.city, COUNT(*) AS orders, SUM(f.amount) AS revenue
           FROM fact_orders f JOIN dim_kitchen k ON f.kitchen = k.kitchen
           GROUP BY k.city ORDER BY revenue DESC"""
for city, orders, revenue in db.execute(query):
    print(f"QUERY  : {city:7} {orders} orders  Rs {revenue}")
db.close()
