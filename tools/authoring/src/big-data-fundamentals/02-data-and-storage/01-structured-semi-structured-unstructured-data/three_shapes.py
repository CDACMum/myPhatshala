"""Create one sample file of each shape in a folder, then read each one the right way."""
import csv, json, os, re

os.makedirs("sample_data", exist_ok=True)

# 1. Structured: a CSV with a fixed header
with open("sample_data/orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "city", "amount"])
    w.writerows([["O1", "Pune", 420], ["O2", "Mumbai", 250], ["O3", "Pune", 180]])

# 2. Semi-structured: JSON lines with nesting and a missing key
events = [
    {"order_id": "O1", "items": [{"dish": "thali", "qty": 1}, {"dish": "lassi", "qty": 2}]},
    {"order_id": "O2", "items": [{"dish": "dosa", "qty": 1}], "coupon": "LUNCH20"},
]
with open("sample_data/events.jsonl", "w") as f:
    for e in events:
        f.write(json.dumps(e) + "\n")

# 3. Semi-structured: log lines with a pattern
with open("sample_data/app.log", "w") as f:
    f.write("2026-10-19 13:02:11 INFO  order=O1 status=PLACED ms=120\n")
    f.write("2026-10-19 13:02:15 ERROR order=O2 status=PAY_FAILED ms=3020\n")
    f.write("2026-10-19 13:02:19 INFO  order=O3 status=PLACED ms=95\n")

# 4. Unstructured: free-text reviews
with open("sample_data/reviews.txt", "w") as f:
    f.write("Loved the thali, will order again!\n")
    f.write("Food was cold and delivery very late.\n")

print("Files created:", sorted(os.listdir("sample_data")))

# ---- read each one the right way
with open("sample_data/orders.csv") as f:
    rows = list(csv.DictReader(f))
total = sum(int(r["amount"]) for r in rows)
print(f"\n[structured] {len(rows)} rows, columns {list(rows[0])}, total Rs {total}")

flat = []
with open("sample_data/events.jsonl") as f:
    for line in f:
        e = json.loads(line)
        for item in e["items"]:
            flat.append((e["order_id"], item["dish"], item["qty"], e.get("coupon")))
print(f"[semi-structured JSON] flattened into {len(flat)} item rows:")
for r in flat:
    print("   ", r)

pattern = re.compile(r"(\S+ \S+) (\w+)\s+order=(\w+) status=(\w+) ms=(\d+)")
with open("sample_data/app.log") as f:
    parsed = [pattern.match(line).groups() for line in f]
errors = [p for p in parsed if p[1] == "ERROR"]
print(f"[semi-structured log] {len(parsed)} lines parsed, {len(errors)} error: {errors[0][2]} {errors[0][3]}")

negative = {"cold", "late", "spilled", "wrong"}
with open("sample_data/reviews.txt") as f:
    for line in f:
        words = set(re.findall(r"[a-z]+", line.lower()))
        label = "complaint" if words & negative else "praise"
        print(f"[unstructured] {label:9} <- {line.strip()}")
