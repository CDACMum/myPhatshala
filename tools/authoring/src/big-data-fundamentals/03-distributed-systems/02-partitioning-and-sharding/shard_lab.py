"""Four real SQLite database files used as shards.
Orders are routed by a hash of the user id. Then we compare a query that uses the
shard key with one that doesn't, and measure how many keys move when a shard is added."""
import bisect, hashlib, os, random, sqlite3

SHARDS = 4
os.makedirs("shards", exist_ok=True)


def h(text):
    """A stable hash (Python's built-in hash() changes between runs)."""
    return int(hashlib.md5(text.encode()).hexdigest(), 16)


conns = []
for i in range(SHARDS):
    path = f"shards/orders_{i}.db"
    if os.path.exists(path):
        os.remove(path)
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE orders (order_id TEXT, user_id TEXT, city TEXT, amount INT)")
    conns.append(c)

random.seed(11)
cities = ["Pune", "Mumbai", "Thane", "Nashik"]
for n in range(20_000):
    user = f"U{random.randint(1, 3000)}"
    shard = h(user) % SHARDS
    conns[shard].execute("INSERT INTO orders VALUES (?, ?, ?, ?)",
                         (f"O{n}", user, random.choice(cities), random.randint(50, 900)))
for c in conns:
    c.commit()

print("Rows per shard:", [c.execute("SELECT COUNT(*) FROM orders").fetchone()[0] for c in conns])

# Query 1: by the shard key -> exactly one shard
user = "U42"
shard = h(user) % SHARDS
rows = conns[shard].execute("SELECT COUNT(*), SUM(amount) FROM orders WHERE user_id = ?", (user,)).fetchone()
print(f"\nOrders of {user}: ask shard {shard} only -> {rows[0]} orders, Rs {rows[1]}")

# Query 2: not by the shard key -> ask every shard and merge (scatter-gather)
parts = [c.execute("SELECT COUNT(*) FROM orders WHERE city = 'Pune'").fetchone()[0] for c in conns]
print(f"Orders from Pune: ask all {SHARDS} shards {parts} -> total {sum(parts)}")

# Adding a fifth shard: how many users would have to move?
users = [f"U{i}" for i in range(1, 3001)]
moved_mod = sum(1 for u in users if h(u) % 4 != h(u) % 5)

def ring(nodes, vnodes=100):
    points = sorted((h(f"{n}#{v}"), n) for n in nodes for v in range(vnodes))
    return [p for p, _ in points], [n for _, n in points]

def owner(key, r):
    keys, names = r
    i = bisect.bisect(keys, h(key)) % len(keys)
    return names[i]

r4, r5 = ring(["S0", "S1", "S2", "S3"]), ring(["S0", "S1", "S2", "S3", "S4"])
moved_ring = sum(1 for u in users if owner(u, r4) != owner(u, r5))
print(f"\nAdding a 5th shard, users that must move:")
print(f"  hash % N          : {moved_mod} of {len(users)} ({moved_mod / len(users):.0%})")
print(f"  consistent hashing: {moved_ring} of {len(users)} ({moved_ring / len(users):.0%})")
