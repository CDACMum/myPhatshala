"""Three NoSQL ideas using only Python's standard library:
1. a real key-value store on disk (dbm) used as a shopping-cart store
2. JSON documents queried with SQLite's JSON functions (a document-store style)
3. a small graph searched for a fraud ring"""
import dbm, json, sqlite3
from collections import deque

# ---- 1. Key-value: carts stored by key, with an expiry time
with dbm.open("carts_db", "c") as kv:
    now = 1_000_000                       # fixed clock so the output is repeatable
    kv["cart:U9"] = json.dumps({"items": {"thali": 1, "lassi": 2}, "expires": now + 1800})
    kv["cart:U12"] = json.dumps({"items": {"dosa": 1}, "expires": now - 5})   # already expired
    for key in [b"cart:U9", b"cart:U12", b"cart:U99"]:
        raw = kv.get(key)
        if raw is None:
            print(key.decode(), "-> not found")
            continue
        cart = json.loads(raw)
        state = "expired" if cart["expires"] < now else "live"
        print(key.decode(), "->", cart["items"], f"({state})")

# ---- 2. Documents: each kitchen is one JSON document with a nested menu
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE kitchens (doc TEXT)")
docs = [
    {"_id": "K11", "name": "Annapurna", "city": "Pune", "veg": True,
     "menu": [{"dish": "thali", "price": 220}, {"dish": "lassi", "price": 100}]},
    {"_id": "K12", "name": "Spice Box", "city": "Pune", "veg": False,
     "menu": [{"dish": "biryani", "price": 280}], "delivery_partner": "own riders"},
    {"_id": "K13", "name": "Udupi Corner", "city": "Mumbai", "veg": True,
     "menu": [{"dish": "dosa", "price": 150}, {"dish": "filter coffee", "price": 60}]},
]
db.executemany("INSERT INTO kitchens VALUES (?)", [(json.dumps(d),) for d in docs])
rows = db.execute("""
    SELECT json_extract(doc, '$.name'), json_array_length(doc, '$.menu')
    FROM kitchens
    WHERE json_extract(doc, '$.city') = 'Pune' AND json_extract(doc, '$.veg') = 1
""").fetchall()
print("\nVeg kitchens in Pune (name, dishes on menu):", rows)
extra = db.execute("SELECT json_extract(doc, '$.name') FROM kitchens WHERE json_extract(doc, '$.delivery_partner') IS NOT NULL").fetchall()
print("Documents with an extra field nobody planned for:", extra)

# ---- 3. Graph: accounts linked by shared phones and UPI handles
edges = [("A1", "phone:98xx01"), ("A2", "phone:98xx01"), ("A2", "upi:x@ok"), ("A3", "upi:x@ok"),
         ("A3", "device:D7"), ("A4", "device:D7"), ("A5", "phone:77xx22")]
graph = {}
for a, b in edges:
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)
start, seen, queue = "A1", {"A1"}, deque(["A1"])
while queue:
    node = queue.popleft()
    for nxt in graph[node]:
        if nxt not in seen:
            seen.add(nxt)
            queue.append(nxt)
ring = sorted(n for n in seen if n.startswith("A"))
print("\nAccounts connected to A1 through shared phones, UPI ids or devices:", ring)
