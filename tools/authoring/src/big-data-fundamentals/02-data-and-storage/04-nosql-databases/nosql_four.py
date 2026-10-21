# nosql_four.py: the four NoSQL data models, using only Python's standard library.
import dbm, json, os, random, sqlite3, time
from collections import deque

random.seed(3)
os.makedirs("nosql_lab", exist_ok=True)

# ---- 1. KEY-VALUE: get and put by key, nothing else (like Redis, DynamoDB) ----
with dbm.open("nosql_lab/carts", "n") as kv:
    t = time.perf_counter()
    for i in range(20_000):
        kv[f"cart:U{i}"] = json.dumps({"items": ["chai"], "total": 20})
    t_put = time.perf_counter() - t
    t = time.perf_counter()
    for i in random.sample(range(20_000), 5_000):
        json.loads(kv[f"cart:U{i}"])
    t_get = time.perf_counter() - t
    print("1. KEY-VALUE  20,000 puts in", f"{t_put:.2f} s;", "5,000 random gets in", f"{t_get * 1000:.0f} ms")
    print("              kv['cart:U42'] ->", kv["cart:U42"].decode(), "  (engine:", dbm.whichdb("nosql_lab/carts") + ")")

# ---- 2. DOCUMENT: JSON documents, different fields, query inside them (like MongoDB) ----
db = sqlite3.connect("nosql_lab/docs.db")
db.execute("CREATE TABLE IF NOT EXISTS menus (doc TEXT)")
docs = [{"canteen": "C017", "city": "Pune", "items": [{"name": "poha", "price": 30}], "veg_only": True},
        {"canteen": "C233", "city": "Nashik", "items": [{"name": "chai", "price": 20}, {"name": "egg roll", "price": 45}]},
        {"canteen": "C102", "city": "Pune", "items": [{"name": "dosa", "price": 40}], "timings": {"open": "08:00", "close": "20:00"}}]
db.executemany("INSERT INTO menus VALUES (?)", [(json.dumps(d),) for d in docs])
rows = db.execute("""SELECT json_extract(doc, '$.canteen'), json_extract(doc, '$.timings.close')
                     FROM menus WHERE json_extract(doc, '$.city') = 'Pune'""").fetchall()
print("2. DOCUMENT   Pune canteens (canteen, closing time):", rows)

# ---- 3. WIDE-COLUMN: rows grouped by a partition key, sorted by a clustering key (like Cassandra) ----
db.execute("""CREATE TABLE IF NOT EXISTS orders_by_canteen (
                canteen TEXT, ts INTEGER, item TEXT, amount INTEGER,
                PRIMARY KEY (canteen, ts))""")
db.executemany("INSERT INTO orders_by_canteen VALUES (?,?,?,?)",
               [(f"C{random.randint(1, 400):03d}", i, random.choice(["chai", "poha", "dosa"]), 30) for i in range(200_000)])
good = db.execute("EXPLAIN QUERY PLAN SELECT * FROM orders_by_canteen WHERE canteen='C017' AND ts > 150000").fetchall()
bad = db.execute("EXPLAIN QUERY PLAN SELECT * FROM orders_by_canteen WHERE item='dosa'").fetchall()
print("3. WIDE-COL   query by partition key ->", good[0][-1])
print("              query by other column  ->", bad[0][-1])
n = db.execute("SELECT COUNT(*) FROM orders_by_canteen WHERE canteen='C017' AND ts > 150000").fetchone()[0]
print("              last orders of C017:", n)

# ---- 4. GRAPH: nodes and relationships; follow edges (like Neo4j) ----
ordered = {"Riya": {"poha", "chai"}, "Kabir": {"chai", "samosa"}, "Asha": {"samosa", "dosa"}, "Dev": {"dosa"}}
graph = {}
for person, items in ordered.items():
    for item in items:
        graph.setdefault(person, set()).add(item)
        graph.setdefault(item, set()).add(person)
def hops(start, goal):
    seen, q = {start}, deque([(start, [start])])
    while q:
        node, path = q.popleft()
        if node == goal:
            return path
        for nxt in graph[node] - seen:
            seen.add(nxt); q.append((nxt, path + [nxt]))
print("4. GRAPH      how is Riya connected to Dev?", " -> ".join(hops("Riya", "Dev")))
also = {i for p in graph["chai"] for i in graph[p]} - ordered["Riya"]
print("              people who ordered chai also ordered:", sorted(also))
db.close()
