# data_types.py: create one day of canteen data in three shapes, then read each one.
import csv, json, os, random, struct, zlib
from collections import Counter

random.seed(11)
os.makedirs("canteen_drop", exist_ok=True)
items = [("chai", 20), ("vada pav", 25), ("samosa", 15), ("poha", 30), ("coffee", 25)]

# 1. STRUCTURED: fixed columns, every row the same shape
with open("canteen_drop/orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "item", "amount", "mode"])
    for i in range(1, 2001):
        item, price = random.choice(items)
        w.writerow([f"O{i}", item, price, random.choice(["UPI", "cash"])])

# 2. SEMI-STRUCTURED: JSON events; fields vary, and a new app version adds nested data
with open("canteen_drop/app_events.jsonl", "w") as f:
    for i in range(1, 1001):
        e = {"event": random.choice(["open_app", "view_menu", "add_to_cart", "pay"]), "user": f"U{random.randint(1, 300)}"}
        if e["event"] == "pay":
            e["amount"] = random.choice([15, 20, 25, 30])
        if i > 600:                                    # app v2.0 released mid-day
            e["device"] = {"os": random.choice(["android", "ios"]), "app_version": "2.0"}
        f.write(json.dumps(e) + "\n")

# 3. UNSTRUCTURED: free text and an image (bytes with no rows or fields)
notes = ["Samosa was cold today", "Chai is the best on campus!", "Long queue at lunch, staff was polite",
         "Poha too salty", "Loved the vada pav", "Payment by UPI failed twice", "Coffee machine broken again"]
with open("canteen_drop/feedback.txt", "w") as f:
    for _ in range(300):
        f.write(random.choice(notes) + "\n")

def tiny_png(path, w, h):                              # a real PNG: header + one colour
    raw = b"".join(b"\x00" + b"\xd9\x77\x06" * w for _ in range(h))
    def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    open(path, "wb").write(png)
tiny_png("canteen_drop/menu_board.png", 640, 480)

print(f"{'file':20} {'bytes':>8}  shape")
for name, shape in [("orders.csv", "structured"), ("app_events.jsonl", "semi-structured"),
                    ("feedback.txt", "unstructured"), ("menu_board.png", "unstructured")]:
    print(f"{name:20} {os.path.getsize('canteen_drop/' + name):>8,}  {shape}")

# Reading each shape needs a different amount of work
with open("canteen_drop/orders.csv") as f:
    sales = Counter()
    for row in csv.DictReader(f):                      # columns known in advance
        sales[row["item"]] += int(row["amount"])
print("\nCSV   -> revenue by item:", dict(sales.most_common(3)))

keys = Counter()
with open("canteen_drop/app_events.jsonl") as f:
    for line in f:
        e = json.loads(line)
        keys.update(e.keys())                          # schema discovered while reading
print("JSON  -> fields seen (and how often):", dict(keys))

words = Counter()
for line in open("canteen_drop/feedback.txt"):
    for w in ["cold", "salty", "failed", "broken", "best", "loved", "polite"]:
        if w in line.lower():
            words[w] += 1
print("TEXT  -> keyword counts:", dict(words))

with open("canteen_drop/menu_board.png", "rb") as f:
    head = f.read(24)
print("IMAGE -> PNG size from header bytes:", struct.unpack(">II", head[16:24]), "(no rows, no columns)")
