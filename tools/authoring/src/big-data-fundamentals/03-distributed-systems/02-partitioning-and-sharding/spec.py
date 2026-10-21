import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='03-distributed-systems', lesson='02-partitioning-and-sharding', n='3.2',
    module_label='Module 3 · Distributed Systems Concepts',
    title='Partitioning and sharding: splitting data across machines',
    desc='Partitioning and sharding explained: range, hash, directory and composite partitioning, choosing a partition key, routing and scatter-gather queries, rebalancing, consistent hashing with virtual nodes, hot keys and date hotspots, local vs global indexes, and partitions in HDFS, Spark, Kafka, Cassandra and data lakes. Real SQLite shards on your PC.',
    og_desc='How do 40 crore orders fit on many machines? Learn range and hash partitioning, consistent hashing and hot keys, and build four real shards on your PC.',
    minutes=30, level='Beginner → Advanced',
    lead='When one table is too big for one machine, you split it: that is <b>partitioning</b>, and when the parts live on different servers, <b>sharding</b>. In this lesson you choose a partition key, route queries to one shard or all of them, see why adding a shard can move 80% of your data (and how consistent hashing cuts that to about 20%), and watch a viral offer overload a single shard.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Four real shards on your PC'],
)

RUN = dict(
    heading='Route orders to shards',
    intro='<p>Orders are routed to 4 shards by a stable hash of the user id. The program prints how many orders land on each shard, then answers one query that has the shard key and one that doesn\'t. Then try the challenges: range partitioning, choosing a key, mod-N rebalancing, consistent hashing and hot keys.</p>',
    code='''import hashlib

def shard_for(key, n=4):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % n

orders = [("O1", "U9", "Pune"), ("O2", "U42", "Thane"), ("O3", "U9", "Pune"),
          ("O4", "U7", "Mumbai"), ("O5", "U42", "Pune"), ("O6", "U13", "Nashik")]
shards = {0: [], 1: [], 2: [], 3: []}
for oid, user, city in orders:
    shards[shard_for(user)].append((oid, user, city))

for s, rows in shards.items():
    print(f"shard {s}: {rows}")

# With the shard key: ask one shard
target = shard_for("U9")
print("orders of U9 -> shard", target, ":", [r[0] for r in shards[target] if r[1] == "U9"])

# Without the shard key: ask every shard (scatter-gather)
pune = [r[0] for rows in shards.values() for r in rows if r[2] == "Pune"]
print("orders from Pune -> all shards:", pune)
''',
    anno=[
        ('return int(hashlib.md5(key.encode()).hexdigest(), 16) % n', 'A stable hash turns the key into a big number; <code>% n</code> picks a shard. (Python\'s built-in <code>hash()</code> changes between runs, so it can\'t be used for routing.)'),
        ('shards[shard_for(user)].append((oid, user, city))', 'All orders of one user land on the same shard, because the user id is the partition key.'),
        ('pune = [r[0] for rows in shards.values() for r in rows if r[2] == "Pune"]', 'City is not the shard key, so every shard must be searched: scatter-gather.'),
    ],
    tasks=[
        dict(label='1 · Hash routing', hint='Press <b>Run</b>. Add 10 more orders for different users and check whether the shards stay balanced.', code=None),
        dict(label='2 · Range partitions', hint='Partition orders by month into quarterly partitions and count how many partitions a report on Oct–Nov must read. Try a report on Mar–Aug.',
             code='''bounds = [("Q1", 1, 3), ("Q2", 4, 6), ("Q3", 7, 9), ("Q4", 10, 12)]
def parts_for(m1, m2):
    return [name for name, lo, hi in bounds if lo <= m2 and hi >= m1]
print("Oct-Nov report reads:", parts_for(10, 11))
print("Mar-Aug report reads:", parts_for(3, 8))
'''),
        dict(label='3 · Compare keys', hint='Measure balance for two candidate keys: city and user id. Largest ÷ average shows the skew (1.0 is perfect).',
             code='''import hashlib, random
random.seed(5)
orders = [(f"U{random.randint(1, 500)}", random.choice(["Mumbai"] * 6 + ["Pune"] * 3 + ["Nashik"])) for _ in range(2000)]
h = lambda k: int(hashlib.md5(k.encode()).hexdigest(), 16) % 4
for name, key in [("city", lambda o: o[1]), ("user_id", lambda o: o[0])]:
    counts = [0, 0, 0, 0]
    for o in orders:
        counts[h(key(o))] += 1
    print(f"{name:8}: {counts} skew {max(counts) / (len(orders) / 4):.2f}")
'''),
        dict(label='4 · Mod-N resharding', hint='How many keys change shard when going from N to N+1 shards with <code>% N</code>? Try 10 → 11.',
             code='''import hashlib
h = lambda k: int(hashlib.md5(k.encode()).hexdigest(), 16)
keys = [f"user{i}" for i in range(2000)]
for n in [2, 4, 8]:
    moved = sum(1 for k in keys if h(k) % n != h(k) % (n + 1))
    print(f"{n} -> {n + 1} shards: {moved / len(keys):.0%} of keys move")
'''),
        dict(label='5 · Consistent hashing (advanced)', hint='Shards are placed on a ring with 50 virtual points each. Adding a 5th shard moves only about 1/5 of keys. Change the virtual points to 1 and see the balance get worse.',
             code='''import bisect, hashlib
h = lambda s: int(hashlib.md5(s.encode()).hexdigest(), 16)
def ring(nodes, v=50):
    pts = sorted((h(f"{n}-{i}"), n) for n in nodes for i in range(v))
    return [p for p, _ in pts], [n for _, n in pts]
def owner(key, r):
    i = bisect.bisect(r[0], h(key)) % len(r[0])
    return r[1][i]
keys = [f"user{i}" for i in range(2000)]
r4, r5 = ring(["A", "B", "C", "D"]), ring(["A", "B", "C", "D", "E"])
moved = sum(1 for k in keys if owner(k, r4) != owner(k, r5))
load = {n: sum(1 for k in keys if owner(k, r5) == n) for n in "ABCDE"}
print(f"moved: {moved / len(keys):.0%}")
print("keys per shard after adding E:", load)
'''),
        dict(label='6 · Split a hot key (advanced)', hint='One kitchen gets 70% of orders. Appending a suffix 0–9 to its key spreads it across shards. Compare shard loads before and after.',
             code='''import hashlib, random
random.seed(2)
h = lambda k: int(hashlib.md5(k.encode()).hexdigest(), 16) % 4
orders = ["K_famous" if random.random() < 0.7 else f"K{random.randint(1, 300)}" for _ in range(4000)]
before, after = [0] * 4, [0] * 4
for k in orders:
    before[h(k)] += 1
    key = f"{k}#{random.randint(0, 9)}" if k == "K_famous" else k
    after[h(key)] += 1
print("before:", before)
print("after :", after)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: four real shards with SQLite',
    intro='<p>This program creates four SQLite database files, routes 20,000 orders to them by a hash of the user id, then compares a query with the shard key (one database) and one without it (all four). Finally it measures how many users would move when a fifth shard is added, with <code>% N</code> and with consistent hashing. Only the standard library is used. Save it as <code>shard_lab.py</code> and run it.</p>',
    items=[
        dict(title='Shards, routing and rebalancing', file='shard_lab.py',
             cmd=open(os.path.join(HERE, 'shard_lab.py')).read() + '\n# In a terminal:  python shard_lab.py',
             output=open(os.path.join(HERE, 'shard_lab.out')).read(),
             note='Recorded from a real run with Python 3.13; with the same seed you get the same numbers. Open the <code>shards</code> folder: there are four separate databases, and each user\'s orders are entirely in one of them. The rebalancing numbers (80% vs 22%) are the ones used in scenario 1 above.'),
    ],
)

TRACE = dict(
    heading='Routing by range, one line at a time',
    intro='<p>Three orders are placed into quarterly partitions by month. Watch the loop find the first partition whose range contains each month.</p>',
    code='''parts = {"Q3": (7, 9), "Q4": (10, 12)}
placed = {}
for oid, month in [("O1", 8), ("O2", 10), ("O3", 11)]:
    for name, (lo, hi) in parts.items():
        if lo <= month <= hi:
            placed[oid] = name
            break
print(placed)
''',
    notes={1: 'Ranges :: Each partition owns a range of months.',
           5: 'Match :: The month falls inside this range.',
           7: 'Stop :: The first matching partition wins; stop searching.'},
)

WORKED_INTRO = 'Four partitioning problems, from routing by hash to finding hot keys. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Database · routing', title='Which shard holds this user?',
         problem='<p>Users are sharded across 3 database servers by <code>md5(user_id) % 3</code>. Print the server for each user and how many users each server holds.</p>',
         inp='U1 … U9, 3 servers',
         approach=['Compute a stable hash of each user id.',
                   'Take the remainder when dividing by 3.',
                   'Count users per server.'],
         code='''import hashlib
servers = {0: 0, 1: 0, 2: 0}
for i in range(1, 10):
    user = f"U{i}"
    s = int(hashlib.md5(user.encode()).hexdigest(), 16) % 3
    servers[s] += 1
    print(user, "-> server", s)
print("users per server:", servers)
''', notes={5: 'Route :: Same user, same server, every time.'},
         tryit='Try 100 users. Are the servers roughly balanced? Hashing gives a good spread only when there are many keys.'),
    dict(level='i', tag='Data lake · pruning', title='How many date partitions does a query scan?',
         problem='<p>A lake table has one partition per day for 2026. A query asks for 15–21 October. Count partitions scanned with date partitioning and without (one big folder treated as 1 partition containing everything).</p>',
         inp='365 daily partitions, 7-day query',
         approach=['Turn each date into its day number in the year.',
                   'Partitions scanned = days in the query range.',
                   'Compare the fraction of data scanned.'],
         code='''import datetime
total_partitions = 365                          # one folder per day of 2026
lo = datetime.date(2026, 10, 15).timetuple().tm_yday
hi = datetime.date(2026, 10, 21).timetuple().tm_yday
scanned = hi - lo + 1
print("partitions scanned:", scanned, "of", total_partitions, f"(days {lo}-{hi} of the year)")
print(f"data read: {scanned / total_partitions:.1%} of the table")
''', notes={5: 'Prune :: Only the partitions for days 288–294 are opened; the other 358 are skipped.'},
         tryit='Change to monthly partitions (12 of them). How much of the table does the same query read now?'),
    dict(level='i', tag='Design · key choice', title='Score candidate partition keys',
         problem='<p>For each candidate key, count distinct values and the share of rows in the biggest value. A good key has many values and a small biggest share.</p>',
         inp='8 sample orders, keys: city, user_id, order_id',
         approach=['For each key, count rows per value.',
                   'Distinct values = number of keys in the count.',
                   'Biggest share = largest count ÷ total rows.'],
         code='''orders = [("O1", "U1", "Mumbai"), ("O2", "U2", "Mumbai"), ("O3", "U1", "Pune"), ("O4", "U3", "Mumbai"),
          ("O5", "U4", "Mumbai"), ("O6", "U2", "Thane"), ("O7", "U5", "Mumbai"), ("O8", "U6", "Pune")]
for name, idx in [("order_id", 0), ("user_id", 1), ("city", 2)]:
    counts = {}
    for o in orders:
        counts[o[idx]] = counts.get(o[idx], 0) + 1
    print(f"{name:8}: {len(counts)} distinct, biggest share {max(counts.values()) / len(orders):.0%}")
''', notes={5: 'Count :: How many rows each value of this key has.'},
         tryit='Order id has the best spread, but the app queries orders by user. Which key would you pick, and why?'),
    dict(level='a', tag='Operations · hot keys', title='Detect hot keys from a traffic sample',
         problem='<p>From a sample of requests, find keys whose traffic is more than 5 times the average key, and suggest how many sub-keys to split each into so that each part is at most 2× average.</p>',
         inp='sample of 40 requests over 9 keys',
         approach=['Count requests per key with <code>Counter</code>, and the average per key.',
                   'A key is hot if its count is more than 5 × average.',
                   'Sub-keys needed = ceil(count ÷ (2 × average)).'],
         code='''import math
from collections import Counter
sample = ["K7"] * 24 + ["K1", "K2", "K3", "K4"] * 3 + ["K5", "K6", "K8", "K9"]
counts = Counter(sample)
avg = len(sample) / len(counts)
for k, c in counts.items():
    if c > 5 * avg:
        print(f"{k} is hot: {c} requests vs average {avg:.1f} -> split into {math.ceil(c / (2 * avg))} sub-keys")
''', notes={5: 'Average :: Requests per distinct key.', 7: 'Hot :: Far above the average share.'},
         tryit='Lower the threshold to 2 × average. Which other keys appear? Is splitting them worth the extra complexity for readers?'),
]

QUIZ = [
    dict(q='Splitting a table\'s rows across several database servers by a key is called:', options=['Replication', 'Sharding (horizontal partitioning)', 'Normalisation', 'Indexing'], answer=1,
         why='<b>Sharding</b> is horizontal partitioning across servers. Replication copies data; it doesn\'t split it.'),
    dict(q='Which partitioning method makes a query for a range of dates fastest?', options=['Hash partitioning', 'Range partitioning by date', 'Random placement', 'Round robin'], answer=1,
         why='Range partitions keep consecutive dates together, so a date range touches only a few partitions.'),
    dict(q='Which is usually the best partition key for an app\'s orders table, where screens show “my orders”?', options=['city', 'order_status', 'user_id', 'payment_method'], answer=2,
         why='<b>user_id</b> has many values, spreads evenly and matches the main query, so “my orders” hits one shard.'),
    dict(q='A query filters by a column that is not the shard key. What must the system do?', options=['Reject the query', 'Ask every shard and merge the results (scatter-gather)', 'Read only shard 0', 'Rebuild the index'], answer=1,
         why='Without the key the router can\'t know which shard holds the rows, so it fans out to all of them.'),
    dict(q='With hash(key) % N, roughly what share of keys move when going from 4 to 5 shards?', options=['About 20%', 'About 50%', 'About 80%', '0%'], answer=2,
         why='Most remainders change when N changes; in our test, 80% of keys moved.'),
    dict(q='What is the main benefit of consistent hashing?', options=['It encrypts keys', 'Adding or removing a node moves only a small share (about 1/N) of keys', 'It removes the need for replicas', 'It sorts keys by date'], answer=1,
         why='Only keys on the new node\'s arcs of the ring move; virtual nodes keep the load balanced.'),
    dict(q='All orders for one viral kitchen overload one shard. This is called:', options=['A hot key / hot partition', 'A cache miss', 'Schema drift', 'A network partition'], answer=0,
         why='One key with extreme traffic always maps to one shard. Fix it by splitting the key, caching or a dedicated shard.'),
    dict(q='In Kafka, why should all events of one order use the same message key?', options=['To compress them', 'So they go to the same partition and are read in order', 'To delete them faster', 'Keys are required for security'], answer=1,
         why='Kafka guarantees ordering only within a partition; the key decides the partition.'),
]

REVISION = [
    '<b>Partitioning</b> splits data; <b>sharding</b> = horizontal partitions on different servers. Vertical partitioning splits columns.',
    '<b>Range</b> (ranges of key; fast range queries; newest range is hot) · <b>Hash</b> (even spread; range queries scatter) · <b>Directory</b> (lookup table) · <b>Composite</b>.',
    'Good partition key: high cardinality, even spread, used by most queries.',
    'With the key → one shard. Without it → <b>scatter-gather</b> to all shards.',
    'mod-N resharding moves most keys; <b>consistent hashing</b> + virtual nodes moves ≈ 1/N.',
    '<b>Hot keys</b>: split with suffixes, cache, or isolate. Date ranges create a moving write hotspot.',
    'Partitions everywhere: HDFS blocks, Spark partitions, Kafka partitions (order per partition), Cassandra rings, lake date folders.',
]
FAQ = [
    ('What is sharding and why is it used?', 'Sharding is horizontal partitioning of a database across multiple servers: each shard stores a subset of rows chosen by a partition (shard) key. It is used when data size or write throughput exceeds what one server can handle, because each shard stores and serves only part of the data, and shards can be added as the system grows.'),
    ('Compare range and hash partitioning.', 'Range partitioning assigns contiguous key ranges to partitions, which makes range queries efficient and data easy to reason about, but can create hotspots (for example all new dates in one partition) and uneven sizes. Hash partitioning assigns rows by a hash of the key, giving an even distribution and avoiding ordering hotspots, but range queries must visit every partition and plain mod-N hashing makes adding partitions expensive.'),
    ('How do you choose a good partition key?', 'Choose a key with high cardinality and an even distribution of data and traffic, that appears in most queries so they can be routed to a single partition, and that keeps data used together (such as a user\'s orders and payments) on the same partition. Avoid low-cardinality keys like city or status and monotonically increasing keys like timestamps for write-heavy tables.'),
    ('What is consistent hashing?', 'A technique where both nodes and keys are hashed onto a circular space (a ring); each key belongs to the first node clockwise from its position. When a node is added or removed, only the keys in the affected arc move, about 1/N of all keys, instead of most keys as with hash mod N. Virtual nodes (many ring positions per physical node) even out the load. It is used in Cassandra, DynamoDB and distributed caches.'),
    ('What problems does sharding introduce?', 'Queries without the shard key become scatter-gather, joins and transactions across shards are complex and slow, hot keys can overload a shard, rebalancing data when adding shards is operationally hard, and secondary indexes must be designed as local (cheap writes, scattered reads) or global (cheap reads, more expensive writes).'),
]

PRACTICE_INTRO = 'Partitioning exercises, from routing a key to sizing Kafka partitions. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Shard for an id', stmt='Numeric customer ids are sharded with id % 6. Print the shard of each id.', inp='101, 256, 999, 1200',
         code='''for cid in [101, 256, 999, 1200]:
    print(cid, "-> shard", cid % 6)
''', explain='The remainder of division picks the shard.'),
    dict(level='easy', title='Range lookup', stmt='Partitions: P0 for ids 1–1000, P1 for 1001–2000, P2 for 2001–3000. Print the partition of id 1500.', inp='1500',
         code='''ranges = [("P0", 1, 1000), ("P1", 1001, 2000), ("P2", 2001, 3000)]
print(next(p for p, lo, hi in ranges if lo <= 1500 <= hi))
''', explain='Find the range that contains the id.'),
    dict(level='easy', title='Rows per partition', stmt='Count orders per city partition.', inp='6 orders',
         code='''cities = ["Pune", "Mumbai", "Pune", "Thane", "Mumbai", "Mumbai"]
counts = {}
for c in cities:
    counts[c] = counts.get(c, 0) + 1
print(counts)
''', explain='Uneven counts reveal a poor partition key.'),
    dict(level='medium', title='Skew ratio', stmt='Given rows per shard, print the skew (largest ÷ average) and whether it is above 1.5.', inp='[120, 95, 300, 110]',
         code='''rows = [120, 95, 300, 110]
skew = max(rows) / (sum(rows) / len(rows))
print(round(skew, 2), "unbalanced" if skew > 1.5 else "ok")
''', explain='A skew of 1.0 is perfect; large values mean one shard does most of the work.'),
    dict(level='medium', title='Scatter-gather merge', stmt='Each shard returns its top-2 orders by amount. Merge them into the global top-3.', inp='3 shards',
         code='''shard_results = [[("O1", 900), ("O7", 650)], [("O3", 880), ("O9", 300)], [("O5", 990), ("O2", 410)]]
merged = sorted([r for res in shard_results for r in res], key=lambda r: -r[1])
print(merged[:3])
''', explain='The router combines partial answers; each shard only needs to send its own top results.'),
    dict(level='advanced', title='Keys moved with mod-N', stmt='For numeric ids 1–1000, print how many change shard when going from 5 to 6 shards with id % N.', inp='ids 1–1000',
         code='''moved = sum(1 for i in range(1, 1001) if i % 5 != i % 6)
print(moved, "of 1000 move")
''', explain='Most keys move, which is why systems prefer consistent hashing or fixed logical partitions.'),
    dict(level='advanced', title='Logical to physical shards', stmt='1,024 logical shards are spread over 4 servers; one server is added. Move whole logical shards so all 5 servers have nearly equal counts, and print how many logical shards moved.', inp='1024 logical, 4 → 5 servers',
         code='''logical = 1024
before = [logical // 4] * 4
target = [logical // 5 + (1 if i < logical % 5 else 0) for i in range(5)]
moved = sum(max(0, b - t) for b, t in zip(before, target[:4]))
print("target per server:", target)
print("logical shards moved:", moved, f"({moved / logical:.0%})")
''', explain='With many small logical shards, growth moves only the minimum amount of data: about one fifth here.'),
    dict(level='business', title='Kafka partitions for throughput', stmt='A topic must handle 60 MB/s at peak. One consumer processes 4 MB/s. Plan 50% headroom. How many partitions (and consumers) are needed?', inp='60 MB/s, 4 MB/s per consumer, +50%',
         code='''import math
print(math.ceil(60 * 1.5 / 4), "partitions")
''', explain='Each partition is read by at most one consumer in a group, so partitions set the maximum parallelism.'),
    dict(level='business', title='Shards for a growing table', stmt='The orders table is 6 TB and grows 250 GB a month. Each shard server should hold at most 2 TB. How many shards are needed now and in 2 years?', inp='6 TB, +250 GB/month, 2 TB per shard',
         code='''import math
now = 6
later = now + 0.25 * 24
print("now:", math.ceil(now / 2), "shards | in 2 years:", math.ceil(later / 2), "shards")
''', explain='Plan the shard count (and the rebalancing method) for growth, not just for today.'),
]

SCN_INTRO = 'Partitioning decisions from real systems and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
