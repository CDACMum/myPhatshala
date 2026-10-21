import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='02-data-and-storage', lesson='04-nosql-databases', n='2.4',
    module_label='Module 2 · Data and Storage',
    title='NoSQL databases: key-value, document, wide-column and graph',
    desc='NoSQL databases explained: key-value (Redis, DynamoDB), document (MongoDB), wide-column (Cassandra, HBase) and graph (Neo4j), SQL vs NoSQL, query-first data modelling, partition keys, denormalisation, TTL, ACID vs BASE, tunable consistency and polyglot persistence. Real-time animations, Python simulations and a NoSQL lab on your PC.',
    og_desc='Why does one food-delivery app use five databases? Learn the four NoSQL families, design a Cassandra table and catch a fraud ring with a graph.',
    minutes=30, level='Beginner → Advanced',
    lead='One food-delivery app can use five databases: PostgreSQL for money, Redis for carts, MongoDB for menus, Cassandra for rider GPS and Neo4j for referrals. In this lesson you meet the four <b>NoSQL</b> families, compare them with SQL, watch a cache save a flash sale, design a Cassandra table around its query, and catch a cashback fraud ring with a graph.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'NoSQL lab on your PC'],
)

RUN = dict(
    heading='Four NoSQL models in plain Python',
    intro='<p>Each NoSQL family is simulated with ordinary Python data structures: a dictionary for key-value, nested dictionaries for documents, partitions of sorted rows for wide-column, and an adjacency list for a graph. Run it, then try the challenges: cache-aside, denormalisation, choosing a partition key, quorum consistency and graph hops.</p>',
    code='''# 1. Key-value: get/set by key only
kv = {"session:7f3a": "U9", "cart:U9": {"thali": 1, "lassi": 2}}
print("KV       :", kv["cart:U9"])

# 2. Document: nested, flexible records, queried by fields
kitchens = [{"_id": "K11", "city": "Pune", "veg": True, "menu": ["thali", "lassi"]},
            {"_id": "K12", "city": "Pune", "veg": False, "menu": ["biryani"], "halal": True}]
print("Document :", [k["_id"] for k in kitchens if k["city"] == "Pune" and k["veg"]])

# 3. Wide-column: partition by key, rows sorted inside the partition
pings = {"R77": [(1, "18.50,73.85"), (2, "18.51,73.86"), (3, "18.52,73.86")],
         "R12": [(1, "19.07,72.87")]}
print("Wide-col :", "latest R77 ->", pings["R77"][-1])

# 4. Graph: nodes and relationships
friends = {"Riya": ["Kabir", "Meera"], "Kabir": ["Arjun"], "Meera": ["Zoya"]}
two_hops = [ff for f in friends["Riya"] for ff in friends.get(f, [])]
print("Graph    :", "friends of Riya's friends ->", two_hops)
''',
    anno=[
        ('print("KV       :", kv["cart:U9"])', 'Key-value stores answer one question very fast: “what is stored under this key?”'),
        ('{"_id": "K12", "city": "Pune", "veg": False, "menu": ["biryani"], "halal": True}]', 'Documents can have different fields. K12 has <code>halal</code>; K11 doesn\'t, and nothing breaks.'),
        ('print("Wide-col :", "latest R77 ->", pings["R77"][-1])', 'All of R77\'s rows sit in one partition, already sorted, so “latest” is the last row.'),
        ('two_hops = [ff for f in friends["Riya"] for ff in friends.get(f, [])]', 'Following relationships hop by hop is what graph databases are built for.'),
    ],
    tasks=[
        dict(label='1 · Four models', hint='Press <b>Run</b>. Add a third kitchen document with a field nobody else has, and a new rider partition with three pings.', code=None),
        dict(label='2 · Cache-aside', hint='Count how many reads reach the slow database when a cache sits in front. Change the request list to have more repeats.',
             code='''database = {"K11": "Annapurna menu", "K12": "Spice Box menu", "K13": "Udupi menu"}
cache, db_reads = {}, 0
requests = ["K11", "K11", "K12", "K11", "K13", "K12", "K11", "K11"]
for k in requests:
    if k in cache:
        value = cache[k]                 # hit: fast
    else:
        db_reads += 1                    # miss: go to the database
        value = database[k]
        cache[k] = value
print("requests:", len(requests), "| database reads:", db_reads)
print(f"hit ratio: {(1 - db_reads / len(requests)) * 100:.0f}%")
'''),
        dict(label='3 · Denormalise', hint='The order document stores a copy of the kitchen name, so showing an order needs no join. What happens if the kitchen is renamed? Update both places.',
             code='''kitchens = {"K11": {"name": "Annapurna"}}
orders = [{"_id": "O1", "kitchen_id": "K11", "kitchen_name": "Annapurna", "total": 420},
          {"_id": "O2", "kitchen_id": "K11", "kitchen_name": "Annapurna", "total": 180}]
for o in orders:
    print(o["_id"], o["kitchen_name"], o["total"])     # no join needed

kitchens["K11"]["name"] = "Annapurna Bhojnalay"     # rename
stale = [o["_id"] for o in orders if o["kitchen_name"] != kitchens[o["kitchen_id"]]["name"]]
print("orders with a stale copy:", stale)
'''),
        dict(label='4 · Pick a partition key', hint='Compare partition sizes for two keys. A good key gives many partitions of similar size. Try <code>key = lambda p: p["rider"]</code>.',
             code='''pings = [{"city": c, "rider": f"R{r}"} for c, n in [("Mumbai", 60), ("Pune", 15), ("Thane", 5)] for r in range(n)]
for name, key in [("city", lambda p: p["city"]), ("rider", lambda p: p["rider"])]:
    sizes = {}
    for p in pings:
        sizes[key(p)] = sizes.get(key(p), 0) + 1
    print(f"key={name:5} partitions={len(sizes):3} largest={max(sizes.values()):3} smallest={min(sizes.values())}")
'''),
        dict(label='5 · Quorum reads (advanced)', hint='With N replicas, a read that asks R replicas and a write that waits for W replicas always overlap when R + W > N. Try N=3, W=1, R=1.',
             code='''N = 3
for W, R in [(1, 1), (2, 2), (3, 1), (1, 3)]:
    overlap = R + W > N
    print(f"N={N} W={W} R={R}: R+W={R + W} ->", "always sees latest write" if overlap else "may read stale data")
'''),
        dict(label='6 · Graph hops (advanced)', hint='Breadth-first search finds everyone within 3 hops of an account through shared devices. Change <code>MAX_HOPS</code> to 1 and 2.',
             code='''links = {"A1": ["phone1"], "phone1": ["A1", "A2"], "A2": ["phone1", "upi7"],
         "upi7": ["A2", "A3"], "A3": ["upi7", "dev9"], "dev9": ["A3", "A4"], "A4": ["dev9"]}
MAX_HOPS = 6
frontier, seen = ["A1"], {"A1": 0}
while frontier:
    node = frontier.pop(0)
    if seen[node] == MAX_HOPS:
        continue
    for nxt in links[node]:
        if nxt not in seen:
            seen[nxt] = seen[node] + 1
            frontier.append(nxt)
print({n: hops for n, hops in seen.items() if n.startswith("A")})
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: key-value, documents and a graph',
    intro='<p>Python\'s standard library includes a real on-disk key-value store (<code>dbm</code>) and SQLite with JSON functions. This program uses them to store carts by key with an expiry, query JSON kitchen documents by their fields, and find a fraud ring in a small graph. Save it as <code>nosql_lab.py</code> in an empty folder and run it.</p>',
    items=[
        dict(title='NoSQL ideas with the standard library', file='nosql_lab.py',
             cmd=open(os.path.join(HERE, 'nosql_lab.py')).read() + '\n# In a terminal:  python nosql_lab.py',
             output=open(os.path.join(HERE, 'nosql_lab.out')).read(),
             note='Recorded from a real run with Python 3.13; any Python 3.9+ gives the same output. The program creates <code>carts_db</code> files (their exact names depend on your operating system). To try the real products, install Redis or MongoDB Community, or use their free cloud tiers, and repeat the same three ideas.'),
    ],
)

TRACE = dict(
    heading='Cache-aside, one line at a time',
    intro='<p>Three requests arrive for kitchen pages. Watch the first request for each kitchen miss the cache and read the database, and the repeat request hit the cache.</p>',
    code='''db = {"K11": "Annapurna", "K12": "Spice Box"}
cache = {}
db_reads = 0
for key in ["K11", "K12", "K11"]:
    if key not in cache:
        db_reads = db_reads + 1
        cache[key] = db[key]
    page = cache[key]
print(db_reads, cache)
''',
    notes={2: 'Cache :: Starts empty, like Redis after a restart.',
           6: 'Miss :: Not in cache yet, so the slow database is read.',
           7: 'Fill :: Save the value so the next request is fast.'},
)

WORKED_INTRO = 'Four NoSQL design tasks, from choosing a family to finding a ring in a graph. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='System design · choosing', title='Which database family for each feature?',
         problem='<p>Pick a database family for each feature using its main access pattern.</p>',
         inp='payments, user sessions, product catalogue, chat history, friend suggestions',
         approach=['Write each feature\'s access pattern.',
                   'Map patterns to families with a dictionary.',
                   'Print the choice.'],
         code='''features = [("payments", "transactions"), ("user sessions", "get by key"),
            ("product catalogue", "flexible records"), ("chat history", "huge writes by key+time"),
            ("friend suggestions", "relationships")]
family = {"transactions": "relational (SQL)", "get by key": "key-value",
          "flexible records": "document", "huge writes by key+time": "wide-column",
          "relationships": "graph"}
for f, pattern in features:
    print(f"{f:19} -> {family[pattern]}")
''', notes={4: 'Rules :: Each access pattern points to the family built for it.'},
         tryit='Add “OTP with 5-minute expiry” and “IoT temperature readings”. Which families fit?'),
    dict(level='i', tag='Document store · embedding', title='Embed or reference?',
         problem='<p>For each child collection, decide whether to embed it inside the parent document or keep it separate: embed if it is always read with the parent and stays small (under 100 items); otherwise reference it.</p>',
         inp='menu (40 items, read together), reviews (grows forever), addresses (3, read together), orders (grows forever)',
         approach=['Describe each child with its expected size and whether it is read with the parent.',
                   'Apply the rule.',
                   'Print the decision and why.'],
         code='''children = [("menu", 40, True), ("reviews", 100000, False),
            ("addresses", 3, True), ("orders", 500000, False)]
for name, size, read_together in children:
    if read_together and size < 100:
        print(f"{name:9}: embed (small, read with parent)")
    else:
        print(f"{name:9}: reference (large or read separately)")
''', notes={4: 'Rule :: Bounded and read together → embed. Unbounded → reference.'},
         tryit='MongoDB limits a document to 16 MB. If a review averages 1 KB, how many reviews would fill one document?'),
    dict(level='i', tag='Wide-column · key design', title='Measure partition balance for two key designs',
         problem='<p>Messages are partitioned either by <code>group_id</code> or by <code>(group_id, month)</code>. Compute the number of partitions and the largest partition for each design.</p>',
         inp='3 groups with 1,200, 90 and 30 messages over 6 months',
         approach=['Start from the number of messages per group (spread evenly over 6 months).',
                   'Compute partition sizes for each candidate key.',
                   'Compare the largest partition: smaller is safer.'],
         code='''counts = {"G1": 1200, "G2": 90, "G3": 30}      # messages per group over 6 months
months = 6
by_group = dict(counts)
by_group_month = {(g, m): c // months for g, c in counts.items() for m in range(1, months + 1)}
for name, sizes in [("group", by_group), ("group+month", by_group_month)]:
    print(f"{name:12}: {len(sizes):2} partitions, largest {max(sizes.values())} messages")
''', notes={4: 'Split :: Adding the month to the key divides each group into 6 smaller partitions.'},
         tryit='Add a <code>"G4"</code> with 6,000 messages. Is <code>group+month</code> still enough, or does G4 need an extra bucket number?'),
    dict(level='a', tag='Fraud analytics · graph', title='Find connected groups of accounts',
         problem='<p>Accounts are linked when they share an identifier. Find every connected group (ring) with more than one account.</p>',
         inp='5 accounts; pairs that share a phone or device',
         approach=['Build an undirected adjacency list from the pairs of accounts that share an identifier.',
                   'For each unvisited account, walk the graph to collect its whole group.',
                   'Every group found this way has at least two accounts: a possible ring.'],
         code='''shared = [("A1", "A2"), ("A3", "A4"), ("A4", "A5")]  # pairs of accounts sharing a phone or device
adj = {}
for a, b in shared:
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)
seen, rings = set(), []
for acct in sorted(adj):
    if acct in seen: continue
    stack, group = [acct], []
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            group.append(n)
            stack.extend(adj[n])
    rings.append(sorted(group))
print("Rings:", rings)
''', notes={4: 'Graph :: Each pair becomes two directed edges, so we can walk either way.', 11: 'Walk :: Depth-first search collects everything connected to this account.'},
         tryit='Add the pair <code>("A2", "A3")</code>. Which rings merge?'),
]

QUIZ = [
    dict(q='Which NoSQL family is best for storing user sessions and carts that are read and written by a single key?', options=['Graph', 'Key-value', 'Wide-column', 'Relational'], answer=1,
         why='<b>Key-value</b> stores like Redis give millisecond get/set by key, often with automatic expiry.'),
    dict(q='MongoDB is an example of which type of database?', options=['Key-value', 'Document', 'Wide-column', 'Graph'], answer=1,
         why='MongoDB stores JSON-like (BSON) <b>documents</b> with nested fields and flexible schemas.'),
    dict(q='Cassandra and HBase belong to which family?', options=['Wide-column', 'Graph', 'Document', 'Relational'], answer=0,
         why='They are <b>wide-column</b> stores, built for huge write volumes partitioned by key and sorted inside each partition.'),
    dict(q='Which question is a graph database best at?', options=['Total revenue per month', 'Is this account connected to a known fraudster within 3 hops?', 'Store a 2 GB video', 'Look up one value by its key'], answer=1,
         why='Multi-hop relationship questions are natural and fast in a <b>graph</b> database.'),
    dict(q='In NoSQL data modelling, what usually comes first?', options=['Normalising the data to third normal form', 'Listing the queries (access patterns) the application will run', 'Choosing the server hardware', 'Writing stored procedures'], answer=1,
         why='NoSQL tables and documents are shaped to answer known queries with as few look-ups as possible.'),
    dict(q='What does BASE stand for?', options=['Basic, Atomic, Secure, Exact', 'Basically Available, Soft state, Eventually consistent', 'Batch, Async, Stream, Event', 'Big, Available, Scalable, Elastic'], answer=1,
         why='BASE describes systems that prefer availability and accept eventual consistency, in contrast with ACID.'),
    dict(q='With 3 replicas, which setting guarantees a read sees the latest successful write?', options=['W=1, R=1', 'W=2, R=2', 'W=1, R=2', 'W=0, R=3'], answer=1,
         why='Reads and writes overlap when <b>R + W &gt; N</b>: 2 + 2 = 4 &gt; 3.'),
    dict(q='Partitioning rider GPS data by city made Mumbai\'s partition huge. This problem is called:', options=['A hot partition', 'Schema drift', 'A cache miss', 'Denormalisation'], answer=0,
         why='One partition gets far more data and traffic than the rest: a <b>hot partition</b>. Choose a key that spreads load evenly.'),
]

REVISION = [
    'NoSQL = <b>not only SQL</b>: non-relational models, flexible schemas, horizontal scaling.',
    '<b>Key-value</b> (Redis, DynamoDB) · <b>Document</b> (MongoDB) · <b>Wide-column</b> (Cassandra, HBase) · <b>Graph</b> (Neo4j).',
    'SQL: fixed schema, joins, ACID, vertical scaling. NoSQL: flexible, denormalised, horizontal, often BASE/tunable.',
    'Model from <b>queries</b>: denormalise; embed small, bounded children; reference unbounded ones.',
    '<b>Partition key</b> spreads data and load; avoid hot partitions; clustering key sorts rows inside.',
    'Cache-aside: check cache → on miss read DB and store with TTL → invalidate on change.',
    'Quorum: R + W &gt; N for read-your-latest-write. LSM trees for heavy writes. Polyglot persistence = right store per job.',
]
FAQ = [
    ('What are the types of NoSQL databases? Give examples.', 'Key-value stores (Redis, Amazon DynamoDB, Memcached) map unique keys to values for very fast look-ups, used for caches, sessions and carts. Document stores (MongoDB, Couchbase, Firestore) hold JSON-like documents with nested, flexible fields, used for catalogues and profiles. Wide-column stores (Cassandra, HBase, Bigtable) organise rows into partitions sorted by clustering keys across many nodes, used for time series, logs and messaging. Graph databases (Neo4j, Amazon Neptune) store nodes and relationships, used for fraud detection, recommendations and social networks.'),
    ('Differentiate SQL and NoSQL databases.', 'SQL databases use tables with predefined schemas, support joins and ACID transactions, and typically scale vertically with read replicas. NoSQL databases use key-value, document, wide-column or graph models, allow flexible schemas, scale horizontally, denormalise data around access patterns and often offer eventual or tunable consistency. SQL suits transactional systems and ad-hoc analysis; NoSQL suits very high scale, flexible data and specific access patterns.'),
    ('What is the CAP-related trade-off in NoSQL databases?', 'In a distributed database, when the network partitions, a system must choose between consistency (every read sees the latest write) and availability (every request gets a response). Many NoSQL systems, such as Cassandra, favour availability with tunable consistency, while others, such as HBase, favour consistency. Lesson 3.4 explains the CAP theorem in detail.'),
    ('When should you not use NoSQL?', 'When you need complex multi-table transactions (payments, accounting), rich ad-hoc queries and joins across many entities, or strong consistency everywhere without careful design, and when the data comfortably fits a single well-indexed relational database. Adding a NoSQL store also adds operational complexity.'),
    ('What is polyglot persistence?', 'Using several kinds of data stores in one system, each chosen for a specific workload: for example a relational database for orders and payments, Redis for caching and sessions, a document store for catalogues, a wide-column store for event history, and a search engine for text search.'),
]

PRACTICE_INTRO = 'NoSQL modelling and access-pattern exercises. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Get with a default', stmt='Read a key from a key-value dictionary; print “not found” if it is missing.', inp='keys cart:U9, cart:U99',
         code='''kv = {"cart:U9": {"thali": 1}}
for k in ["cart:U9", "cart:U99"]:
    print(k, "->", kv.get(k, "not found"))
''', explain='<code>get</code> with a default avoids an error for missing keys.'),
    dict(level='easy', title='Query documents by a field', stmt='Print the names of kitchens in Pune.', inp='3 documents',
         code='''docs = [{"name": "Annapurna", "city": "Pune"}, {"name": "Udupi", "city": "Mumbai"}, {"name": "Spice Box", "city": "Pune"}]
print([d["name"] for d in docs if d["city"] == "Pune"])
''', explain='Document stores filter and index by fields inside the documents.'),
    dict(level='easy', title='Expired keys', stmt='Each key has an expiry time. At time 100, print the keys still alive.', inp='otp1 exp 90, otp2 exp 120, cart exp 300',
         code='''expiry = {"otp1": 90, "otp2": 120, "cart": 300}
now = 100
print([k for k, exp in expiry.items() if exp > now])
''', explain='This is what a TTL does automatically in Redis or Cassandra.'),
    dict(level='medium', title='Latest rows from a partition', stmt='Pings are stored per rider. Print the 2 most recent pings of R7.', inp='R7: t=1,2,3,4',
         code='''pings = {"R7": [(1, "A"), (2, "B"), (3, "C"), (4, "D")], "R9": [(1, "X")]}
print(sorted(pings["R7"], reverse=True)[:2])
''', explain='In Cassandra, clustering by time descending makes this a cheap read of the first rows.'),
    dict(level='medium', title='Friends of friends', stmt='Print people two hops from Riya who are not already her friends.', inp='small friend graph',
         code='''g = {"Riya": ["Kabir", "Meera"], "Kabir": ["Arjun", "Meera"], "Meera": ["Zoya"]}
direct = set(g["Riya"])
two = {ff for f in direct for ff in g.get(f, [])} - direct - {"Riya"}
print(sorted(two))
''', explain='Set operations remove existing friends and Riya herself.'),
    dict(level='advanced', title='Hit ratio needed', stmt='The database handles at most 3,000 reads per second. Traffic is 2,00,000 reads per second. What minimum cache hit ratio is needed?', inp='3,000 vs 2,00,000',
         code='''db_max, traffic = 3000, 200000
needed = 1 - db_max / traffic
print(f"Minimum hit ratio: {needed * 100:.1f}%")
''', explain='Only misses reach the database, so misses must stay at or below 3,000 per second.'),
    dict(level='advanced', title='Quorum settings', stmt='For N = 5 replicas, print every (W, R) pair with R + W > N where both are between 1 and 5, and the smallest such R for W = 3.', inp='N = 5',
         code='''N = 5
pairs = [(w, r) for w in range(1, 6) for r in range(1, 6) if r + w > N]
print(len(pairs), "valid pairs")
print("smallest R for W=3:", min(r for w, r in pairs if w == 3))
''', explain='Stronger writes (bigger W) allow lighter reads (smaller R), and the other way round.'),
    dict(level='business', title='Redis memory for sessions', stmt='5 crore daily users, 30% active at peak, each session is 2 KB. How many GB of cache memory are needed (add 30% overhead)?', inp='5 crore, 30%, 2 KB, +30%',
         code='''users = 5_00_00_000
active = users * 0.30
gb = active * 2 / 1024 / 1024 * 1.3
print(f"Memory needed: {gb:.0f} GB")
''', explain='Capacity planning for an in-memory store: active keys × size × overhead.'),
    dict(level='business', title='Cache saving', stmt='Each database read costs Rs 0.002 in compute; a cache read costs Rs 0.0001. With 1 crore reads a day and a 95% hit ratio, print the daily cost with and without the cache.', inp='1 crore reads, 95% hits',
         code='''reads = 1_00_00_000
no_cache = reads * 0.002
with_cache = reads * 0.95 * 0.0001 + reads * 0.05 * 0.002
print("Without cache: Rs", round(no_cache))
print("With cache   : Rs", round(with_cache))
''', explain='A cache cuts both latency and cost, as long as the data can tolerate a short staleness. (Costs are illustrative.)'),
]

SCN_INTRO = 'NoSQL design questions from real interviews and projects. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
