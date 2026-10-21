import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = label_box(250, 14, 140, 40, ['TiffinGo app'], 'acc', 11)
dbs = [('PostgreSQL', 'orders, payments', 'blue', 10), ('Redis', 'carts, sessions', 'red', 136), ('MongoDB', 'kitchen menus', 'green', 262), ('Cassandra', 'rider GPS history', 'violet', 388), ('Neo4j', 'referral graph', 'acc', 514)]
for name, use, tone, x in dbs:
    sc += label_box(x, 92, 116, 46, [name, use], tone, 9.6) + arrow(320, 56, x + 58, 90, 'ink3', 1.3)
scene_svg = scene('The TiffinGo app connected to five databases: PostgreSQL for orders, Redis for carts, MongoDB for menus, Cassandra for rider GPS history and Neo4j for referrals.', sc,
                  'One app, five databases, <tspan font-weight="700" class="s-acc">each chosen for one job</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Kabir draws TiffinGo’s architecture from their tech blog for his notes. He expects one database. He finds five: PostgreSQL, Redis, MongoDB, Cassandra and Neo4j. In college they learned only MySQL and normalisation.</p>

{scene_svg}

K> Sir, why five databases? Couldn’t they keep everything in one MySQL database with good indexes?
A> For a small app, yes. But imagine two lakh carts updating every second during a sale, menus whose fields differ for every kitchen, and every rider sending a location every five seconds. A single relational database would struggle with some of these jobs, or cost a fortune.
R> So the others are “NoSQL” databases? Does that mean they don’t use SQL at all?
A> “NoSQL” today means <b>not only SQL</b>. They drop some relational features, like fixed schemas or joins, to gain others: massive scale, flexible documents, millisecond look-ups, or easy relationship queries. There are four big families: <b>key-value</b>, <b>document</b>, <b>wide-column</b> and <b>graph</b>.
K> And the orders stay in PostgreSQL?
A> Exactly. Money needs strict transactions, which relational databases do best. Choosing the right store for each job is called <b>polyglot persistence</b>. Today you’ll see a cache save a flash sale, design a Cassandra table around its queries, and catch a fraud ring with a graph.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> NoSQL at three levels
L1> Four kinds of storage cupboards
      <ul>
        <li><b>Key-value</b> is a cloakroom: give a token (key), get your item (value) instantly. Example: Redis storing <code>cart:U9 → {thali: 1}</code>.</li>
        <li><b>Document</b> is a file folder per customer: each folder holds a whole form with nested sections, and two folders can have different fields. Example: MongoDB storing a kitchen with its whole menu inside.</li>
        <li><b>Wide-column</b> is a giant register split into many books by a key: each rider’s book holds his location pages in time order. Example: Cassandra storing GPS pings per rider.</li>
        <li><b>Graph</b> is a friendship map: dots (people, phones, accounts) connected by lines (shares, refers, pays). Example: Neo4j finding who is connected to whom.</li>
      </ul>
      <p><b>Simple rule:</b> money and strict rules → relational (SQL). Speed by key → key-value. Flexible records → document. Huge write streams → wide-column. Relationships → graph.</p>
L2> Model data around your queries
      <ul>
        <li><b>Access patterns first:</b> in NoSQL you list the questions the app will ask (“get a rider’s last 50 positions”) and shape the data to answer each one with a single look-up. Relational design normalises first and joins later.</li>
        <li><b>Denormalisation:</b> data is copied where it is read (a kitchen’s name stored inside each order document) to avoid joins, accepting extra storage and harder updates.</li>
        <li><b>Embed or reference (documents):</b> embed things read together and bounded in size (a menu inside a kitchen); reference things that grow without limit (all orders of a kitchen).</li>
        <li><b>Partition key (wide-column, key-value at scale):</b> decides which machine holds the data. A good key spreads load evenly and keeps one query on one partition.</li>
        <li><b>TTL:</b> many NoSQL stores can expire data automatically (carts after 30 minutes, OTPs after 5 minutes).</li>
      </ul>
L3> ACID vs BASE, tunable consistency and storage engines
      <ul>
        <li><b>ACID vs BASE:</b> relational databases promise Atomicity, Consistency, Isolation, Durability. Many NoSQL systems chose <b>BASE</b> (Basically Available, Soft state, Eventually consistent) to stay available and fast across many machines. Modern MongoDB and DynamoDB do support multi-document transactions, at a cost.</li>
        <li><b>Tunable consistency:</b> Cassandra lets each query choose how many replicas must answer. With N replicas, if read replicas R plus write replicas W is greater than N, every read sees the latest write (more in Lesson 3.4).</li>
        <li><b>Storage engines:</b> B-trees (most relational databases) are good at reads and updates in place; <b>LSM trees</b> (Cassandra, HBase, RocksDB) turn writes into fast sequential appends and merge files in the background, which suits huge write volumes.</li>
        <li><b>Hot partitions:</b> one celebrity account or one city can overload a single partition. Fix with better keys or by splitting (bucketing) hot keys.</li>
        <li><b>NewSQL:</b> distributed SQL databases (Google Spanner, CockroachDB, YugabyteDB, TiDB) scale out like NoSQL while keeping SQL and ACID transactions.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>NoSQL</b> (“not only SQL”) database is a non-relational database that stores data in models other than fixed relational tables, typically to achieve <b>horizontal scalability</b>, <b>flexible schemas</b> and high performance for specific access patterns. The four main families are <b>key-value stores</b>, <b>document stores</b>, <b>wide-column stores</b> and <b>graph databases</b>. Many NoSQL systems relax strict ACID guarantees in favour of availability and partition tolerance (BASE), often offering tunable or eventual consistency.',
    'NoSQL databases are databases that don’t force every record into the same table shape. Some store simple key → value pairs, some store whole JSON documents, some store huge numbers of rows spread across many machines, and some store connections between things. Each one is very good at one kind of job.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Key-value pair', 'A unique key and its value: <code>otp:9876 → 482913</code>.'),
    ('Document', 'A self-contained JSON-like record that can have nested fields and lists.'),
    ('Partition key', 'The part of a key that decides which machine stores the row.'),
    ('Clustering key', 'In wide-column stores, the order of rows inside a partition (for example by time).'),
    ('Node / edge', 'In a graph: a thing (account, phone) and a relationship between two things (USES, REFERS).'),
    ('Denormalisation', 'Copying data into several places so each read needs no joins.'),
    ('TTL (time to live)', 'An automatic expiry time on a key or row.'),
    ('Polyglot persistence', 'Using several kinds of databases in one system, each for what it does best.'),
]) + '''

  <h3>The four families and well-known examples</h3>
''' + facts([
    ('Key-value', 'Redis, Amazon DynamoDB, Memcached, etcd · caches, sessions, carts, rate limits, OTPs'),
    ('Document', 'MongoDB, Couchbase, Google Firestore, Azure Cosmos DB · catalogues, user profiles, content, app data'),
    ('Wide-column', 'Apache Cassandra, Apache HBase, ScyllaDB, Google Bigtable · time series, IoT, event logs, messaging'),
    ('Graph', 'Neo4j, Amazon Neptune, TigerGraph · fraud rings, recommendations, social networks, knowledge graphs'),
]) + lv + '''
EXAM> Answer “types of NoSQL databases” with all four families: <b>data model, example product, typical use</b>, plus one line each on <b>schema flexibility, horizontal scaling and BASE vs ACID</b>. Add a short SQL vs NoSQL comparison table for full marks.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Key-value', 'A giant dictionary. Get or set by key in about a millisecond. Values are opaque blobs; no queries on their contents.', 'Fastest look-ups'),
    ('Document', 'JSON-like documents with nesting and flexible fields. Query and index by fields inside the document.', 'Flexible records'),
    ('Wide-column', 'Rows grouped into partitions by key and sorted inside each partition. Built for huge write volumes across many nodes.', 'Massive writes'),
    ('Graph', 'Nodes and relationships stored directly. Multi-hop questions (“friends of friends”) are fast and natural.', 'Relationships'),
]) + '''

  <h3>SQL vs NoSQL</h3>
''' + table(['', 'Relational (SQL)', 'NoSQL'], [
    ['<b>Data model</b>', 'Tables with rows and columns', 'Key-value, document, wide-column or graph'],
    ['<b>Schema</b>', 'Fixed, defined in advance', 'Flexible; can differ per record'],
    ['<b>Scaling</b>', 'Mostly vertical (bigger server); read replicas', 'Horizontal (add nodes) by design'],
    ['<b>Joins</b>', 'Powerful, central to design', 'Limited or none; data denormalised'],
    ['<b>Transactions</b>', 'Strong ACID', 'Often BASE / tunable; some support ACID'],
    ['<b>Design approach</b>', 'Normalise, then query anything', 'Start from the queries, shape data for them'],
    ['<b>Best for</b>', 'Payments, orders, accounting, reports', 'Caches, catalogues, events, time series, graphs'],
], minw=600) + '''

  <h3>Same order, four models</h3>
''' + table(['Family', 'How order O1043 might be stored'], [
    ['Key-value', '<code>order:O1043 → {"user": "U9", "total": 420, "status": "DELIVERED"}</code>'],
    ['Document', '<code>{"_id": "O1043", "user": {"id": "U9", "name": "Riya"}, "items": [{"dish": "thali", "qty": 1}], "total": 420}</code>'],
    ['Wide-column', 'partition <code>user_id = U9</code>, rows sorted by <code>order_time DESC</code>: O1043, O1012, O0987…'],
    ['Graph', '<code>(Riya)-[:PLACED]->(O1043)-[:FROM]->(Annapurna Kitchen)</code>'],
], minw=560) + '''
TIP> NoSQL is not “better” than SQL. Most companies keep money in a relational database and add NoSQL stores around it. In interviews, always justify a NoSQL choice by the <b>access pattern</b> and <b>scale</b>, not by fashion.'''

# ---------------------------------------------------------------- steps
c1 = '''import time
cache = {}
def set_key(k, v, ttl):
    cache[k] = (v, time.time() + ttl)
def get_key(k):
    v, exp = cache.get(k, (None, 0))
    return v if time.time() < exp else None
set_key("cart:U9", {"thali": 1, "lassi": 2}, ttl=1800)
set_key("otp:9876", "482913", ttl=-1)          # already expired
print(get_key("cart:U9"), get_key("otp:9876"))'''
c2 = '''kitchens = [
    {"_id": "K11", "name": "Annapurna", "veg": True, "menu": [{"dish": "thali", "price": 220}]},
    {"_id": "K12", "name": "Spice Box", "veg": False, "menu": [{"dish": "biryani", "price": 280}], "halal": True},
]
veg = [k["name"] for k in kitchens if k["veg"]]
print("veg kitchens:", veg, "| K12 extra field halal:", kitchens[1].get("halal"))'''
c3 = '''pings = {}   # partition key = rider, rows kept sorted by time
for rider, t, lat in [("R7", 3, 18.52), ("R9", 1, 19.07), ("R7", 1, 18.50), ("R7", 2, 18.51)]:
    pings.setdefault(rider, []).append((t, lat))
    pings[rider].sort()
print("R7 partition:", pings["R7"])
print("latest for R7:", pings["R7"][-1])'''
c4 = '''refers = {"Riya": ["Kabir", "Meera"], "Kabir": ["Arjun"], "Meera": [], "Arjun": ["Zoya"]}
level1 = refers["Riya"]
level2 = [p for f in level1 for p in refers[f]]
print("referred by Riya:", level1, "| their referrals:", level2)'''
steps = stepper([
    ('Key-value: Riya’s cart in Redis',
     code('python', 'cart_kv.py', c1, run_code(c1)),
     'A cart is read and written by one key, many times a minute, and is useless after half an hour. A key-value store with a TTL does exactly this in about a millisecond, and the expired OTP disappears by itself.'),
    ('Document: each kitchen is one document',
     code('python', 'menus_doc.py', c2, run_code(c2)),
     'The menu lives inside the kitchen document, so one read fetches the whole page. Kitchens can have extra fields (like <code>halal</code>) without changing a schema for everyone.'),
    ('Wide-column: rider pings partitioned by rider',
     code('python', 'pings_wide.py', c3, run_code(c3)),
     'Each rider’s pings live together in one partition, kept sorted by time. “Latest position of R7” reads one partition, even when there are billions of pings in total spread over many nodes.'),
    ('Graph: who referred whom',
     code('python', 'referrals_graph.py', c4, run_code(c4)),
     'Relationships are stored directly, so “referrals of my referrals” is a short walk. In SQL each extra hop is another self-join on a large table.'),
    ('Relational: the payment itself',
     '<p>When Riya pays ₹420, the order row, the payment row and the wallet balance change together inside one PostgreSQL transaction: all or nothing.</p>',
     'This is where <b>ACID</b> matters most. If the payment fails half-way, nothing is saved. That is why money stays in a relational database.'),
    ('Polyglot persistence',
     '<p>One order touched five databases, each doing what it does best. Events from all of them also flow into the data lake for analytics.</p>',
     'The cost: more systems to run, monitor and keep in sync. Teams add a new database only when an access pattern truly needs it.'),
])

# ---------------------------------------------------------------- two-view animation
def ph(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
see = [
    ph('Welcome back, Riya', t(180, 90, 'Hi Riya!', 12, bold=True) + t(180, 110, 'Pune · Kharadi', 8.4, 'ink2')),
    ph('Annapurna Kitchen', ''.join(t(138, 70 + k * 18, d, 8.2, anchor='start') + t(222, 70 + k * 18, p, 8.2, anchor='end', bold=True) for k, (d, p) in enumerate([('Thali', '₹220'), ('Lassi', '₹100'), ('Gulab jamun', '₹60')])) + t(180, 140, 'Pure veg · 4.2 ★', 8.2, 'green')),
    ph('Cart', t(180, 74, 'Thali × 1', 9) + t(180, 92, 'Lassi × 2', 9) + t(180, 120, '₹420', 12, bold=True) + fill(144, 140, 72, 20, 'acc', rx=10) + t(180, 154, 'PAY', 8.4, extra=' style="fill:#fff"', bold=True)),
    ph('Paid', '<circle cx="180" cy="94" r="20" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M171 94l6 6 12-12" style="stroke:var(--green);stroke-width:3;fill:none"/>' + t(180, 140, '₹420 · UPI', 9, bold=True)),
    ph('Tracking', '<path d="M140 160 Q170 90 218 76" style="fill:none;stroke:var(--blue);stroke-width:2;stroke-dasharray:4 3"/><circle cx="218" cy="76" r="6" style="fill:var(--green)"/><circle cx="168" cy="112" r="7" style="fill:var(--track)"/>' + t(180, 190, 'rider 1.2 km away', 8.4, 'blue', bold=True)),
    ph('For you', t(180, 70, 'Your friends ordered:', 8.4, 'ink2') + label_box(136, 82, 88, 30, ['Kabir · Biryani'], 'card', 8) + label_box(136, 118, 88, 30, ['Meera · Dosa'], 'card', 8) + t(180, 172, 'Refer & earn ₹50', 8.4, 'acc', bold=True)),
]
def db(name, tone, line1, line2, ms):
    return (label_box(40, 30, 280, 46, [name], tone, 12) + box(20, 90, 320, 62, 'card') + t(180, 114, line1, 8.6, mono=True) + t(180, 134, line2, 8.4, 'ink2')
            + t(180, 184, ms, 10, 'green', bold=True))
behind = [
    db('Redis (key-value)', 'red', 'GET session:7f3a… → {user: U9, city: Pune}', 'session token from the phone is the key', '≈ 1 ms'),
    db('MongoDB (document)', 'green', 'find({_id: "K11"}) → name, rating, menu[…]', 'whole kitchen page in one document read', '≈ 5 ms'),
    db('Redis (key-value)', 'red', 'HSET cart:U9 thali 1 lassi 2 · EXPIRE 1800', 'every tap updates the cart key; expires in 30 min', '≈ 1 ms per update'),
    db('PostgreSQL (relational)', 'blue', 'BEGIN; INSERT order; INSERT payment; COMMIT;', 'all-or-nothing ACID transaction for money', 'safe, consistent'),
    db('Cassandra (wide-column)', 'violet', 'INSERT INTO pings (rider, ts, lat, lon) …', 'partition = rider R77, rows sorted by time', '1 write per rider every 5 s'),
    db('Neo4j (graph)', 'acc', '(Riya)-[:FRIEND]->(f)-[:ORDERED]->(dish)', 'two hops through the relationship graph', '≈ 20 ms'),
]
see_caps = ['Riya opens the app and is greeted by name; it already knows her area.',
            'She opens Annapurna Kitchen and sees its full menu and rating.',
            'She adds a thali and two lassis; the cart updates instantly with every tap.',
            'She pays ₹420 by UPI and gets a confirmation.',
            'She watches the rider move towards her on the map.',
            'The app shows what her friends ordered and invites her to refer someone.']
behind_caps = ['The app looks up her <b>session</b> in Redis by its token: a key-value read in about a millisecond.',
               'The kitchen page is one <b>MongoDB document</b> containing name, rating and the nested menu.',
               'The cart is a Redis key updated on every tap, with a 30-minute expiry (TTL).',
               'The payment and order are written in one PostgreSQL <b>ACID transaction</b>: either both are saved or neither is.',
               'The rider’s phone writes a location every five seconds into <b>Cassandra</b>, partitioned by rider and sorted by time.',
               'A two-hop <b>graph</b> query finds dishes her friends ordered. (Timings are typical, not exact.)']
two = anim_two('One app session, five databases', 'What Riya sees, and which database answers', 'Riya using the food-delivery app',
               'Which database serves each step and how it is queried', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: cache-aside
def flow(app_db=False, hit=None, note=''):
    o = label_box(10, 40, 90, 46, ['App', 'server'], 'acc', 9.4) + label_box(135, 40, 90, 46, ['Redis', 'cache'], 'red', 9.4) + label_box(260, 40, 90, 46, ['Database', 'PostgreSQL'], 'blue', 9.4)
    o += arrow(102, 56, 133, 56)
    if hit is True:
        o += arrow(133, 72, 102, 72, 'green') + t(118, 100, 'hit', 8.4, 'green', bold=True)
    if hit is False:
        o += t(118, 100, 'miss', 8.4, 'red', bold=True)
    if app_db:
        o += '<path d="M55 88 V112 H305 V88" style="fill:none;stroke:#8A94A0;stroke-width:1.6;stroke-dasharray:4 3"/>' + t(180, 108, 'read from database (≈ 80 ms under load)', 8.2, 'ink2')
    return o
fr = [
    flow() + t(180, 22, '00:00 · flash sale: 2 lakh menu reads per second', 9.6, 'red', bold=True) + cap('Every page asks the database for the same hot menus.', 'The database CPU hits 100%; pages take 3 seconds.', 'red', y=130, h=44),
    flow(hit=False, app_db=True) + t(180, 22, 'Cache-aside: check the cache first', 9.6, 'acc', bold=True) + cap('First request: not in cache (miss), so read the database', 'and store the result in Redis with a 60 s TTL.', 'blue', y=130, h=44),
    flow(hit=True) + t(180, 22, 'Next requests: cache hit', 9.6, 'green', bold=True) + cap('The next 59 seconds of requests are served from memory', 'in about 1 ms. The database barely notices.', 'green', y=130, h=44),
    flow(hit=True) + t(180, 22, 'Hit ratio 99%', 9.6, 'green', bold=True) + bars([('DB reads / s', 1, 'green', '2,000'), ('cache reads / s', 99, 'red', '1,98,000')], x=120, y=118, w=170, gap=22) + cap('Only 1% of reads reach the database.', '', 'green', y=172, h=34),
    flow(hit=True) + t(180, 22, 'Price change? Invalidate the key', 9.6, 'acc', bold=True) + cap('When a kitchen edits its menu, the app deletes that key,', 'so the next read fetches fresh data. Short TTLs limit staleness.', 'blue', y=130, h=44),
]
s1 = anim_one('Real-time scenario 1', 'Flash sale: a key-value cache saves the database',
              'At midnight a sale starts and everyone opens the same few kitchen pages. Watch the <b>cache-aside</b> pattern take the load off the database.',
              'Cache-aside with Redis', 'App, Redis cache and database during a flash sale using the cache-aside pattern', fr,
              ['Two lakh page views a second all ask the database for the same popular menus. Its CPU saturates and pages slow to three seconds.',
               '<b>Cache-aside:</b> the app first asks Redis. On a miss it reads the database and saves the result in Redis with a short expiry (TTL).',
               'For the next minute, every request for that menu is a <b>hit</b>, served from memory in about a millisecond.',
               'With a 99% hit ratio, only 2,000 of the 2 lakh reads per second reach the database.',
               'When data changes, the app deletes (invalidates) the cached key; the short TTL also limits how stale data can get. (Numbers are illustrative.)'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: cassandra partition key design
def parts(sizes, labels, hot=None):
    o = ''
    mx = 100   # same scale in both designs
    for k, (sz, lb) in enumerate(zip(sizes, labels)):
        x = 16 + k * 58
        h = round(sz / mx * 100)
        o += fill(x, 140 - h, 46, h, 'red' if k == hot else 'violet', rx=3) + t(x + 23, 154, lb, 7.6, 'ink3')
    return o
fr2 = [
    t(180, 22, 'Query: last 50 positions of rider R77', 9.6, 'blue', bold=True, mono=True) + box(14, 40, 332, 60, 'card') + t(180, 62, 'Wrong design: PRIMARY KEY (city, ts)', 9.2, 'red', bold=True, mono=True) + t(180, 82, 'one partition per city, every rider mixed in', 8.6, 'ink2')
    + cap('Partitioning by city looked natural.', 'Let’s see what happens.', 'card', y=120, h=34),
    t(180, 22, 'Partition sizes by city', 9.6, 'red', bold=True) + parts([100, 18, 12, 9, 7, 6], ['Mumbai', 'Pune', 'Thane', 'Nashik', 'Nagpur', 'Surat'], hot=0) + cap('Mumbai’s partition is huge and growing forever:', 'one node does most of the work (a hot partition).', 'red', y=164, h=44),
    t(180, 22, 'And the query is slow', 9.6, 'red', bold=True) + box(14, 40, 332, 60, 'red') + t(180, 62, 'scan Mumbai partition → filter rider = R77', 9, mono=True) + t(180, 82, 'reads millions of rows to return 50', 8.6, 'ink2')
    + cap('The table was not designed for the question asked.', '', 'red', y=120, h=34),
    t(180, 22, 'Better: PRIMARY KEY ((rider_id, day), ts)', 9.6, 'green', bold=True, mono=True) + parts([12, 11, 12, 10, 11, 12], ['R77·19', 'R12·19', 'R77·20', 'R40·19', 'R12·20', 'R9·19']) + cap('Many small partitions of similar size (same scale as', 'before), spread evenly. Rows sorted by ts DESC inside.', 'green', y=164, h=44),
    t(180, 22, 'The query is now one partition read', 9.6, 'green', bold=True) + box(14, 40, 332, 60, 'green') + t(180, 62, "SELECT … WHERE rider_id='R77' AND day='2026-10-19'", 8.2, mono=True) + t(180, 82, 'LIMIT 50 → first 50 rows of one partition', 8.6, 'ink2')
    + cap('Milliseconds, whatever the total data size.', 'Design the key from the query: that is NoSQL modelling.', 'green', y=120, h=44),
]
s2 = anim_one('Real-time scenario 2', 'Designing a Cassandra table around its query',
              'TiffinGo stores every rider’s GPS ping, crores per day. Support agents need “the last 50 positions of rider R77”. Watch a natural-looking table fail, and a query-first design succeed.',
              'Partition key design', 'Cassandra partitions for rider GPS data, designed badly by city and well by rider and day', fr2,
              ['The first design partitions rider pings by <code>city</code>, with time as the clustering key.',
               'Partitions are badly unbalanced: Mumbai’s is several times bigger than the others and grows without limit, so one node is overloaded. This is a <b>hot partition</b>.',
               'Worse, the support query must scan the whole Mumbai partition and filter for one rider, reading millions of rows to return fifty.',
               'The better key is <code>(rider_id, day)</code>: many small, similar-sized partitions spread evenly, each with rows sorted newest first.',
               'The query becomes a single-partition read of the first 50 rows: milliseconds at any scale. In NoSQL you design the table for the query, not the other way round. (Sizes are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): graph fraud ring
P = {'A1': (40, 60), 'A2': (130, 40), 'A3': (220, 60), 'A4': (310, 40), 'A5': (28, 126), 'ph': (85, 110), 'upi': (175, 110), 'dev': (265, 110)}
E = [('A1', 'ph'), ('A2', 'ph'), ('A2', 'upi'), ('A3', 'upi'), ('A3', 'dev'), ('A4', 'dev')]
names = {'ph': 'phone 98xx01', 'upi': 'UPI x@ok', 'dev': 'device D7'}
def g(hl_nodes=(), hl_edges=(), red=False):
    o = ''
    for a, b in E:
        on = (a, b) in hl_edges
        o += f'<path d="M{P[a][0]} {P[a][1]}L{P[b][0]} {P[b][1]}" style="stroke:{"#D64545" if on else "var(--line)"};stroke-width:{2.5 if on else 1.5}"/>'
    for n, (x, y) in P.items():
        acct = n.startswith('A')
        on = n in hl_nodes
        col = '#D64545' if on and red else ('var(--track)' if on else ('var(--blue)' if acct else 'var(--violet)'))
        if acct:
            o += f'<circle cx="{x}" cy="{y}" r="14" style="fill:{col}"/>' + t(x, y + 4, n, 8.4, extra=' style="fill:#fff"', bold=True)
        else:
            o += f'<rect x="{x - 30}" y="{y - 10}" width="60" height="20" rx="10" style="fill:{col}"/>' + t(x, y + 4, names[n], 7, extra=' style="fill:#fff"', bold=True)
    return o
fr3 = [
    g() + cap('Accounts (blue) and the phones, UPI ids and devices', 'they use (violet). A5 shares nothing.', 'blue', y=150, h=44),
    g({'A1'}) + cap('A1 claims a ₹500 new-user cashback.', 'Is A1 really a new user?', 'amber', y=150, h=44),
    g({'A1', 'ph', 'A2'}, {('A1', 'ph'), ('A2', 'ph')}) + cap('Hop 1–2: A1 shares a phone number with A2.', '', 'amber', y=150, h=34),
    g({'A1', 'ph', 'A2', 'upi', 'A3', 'dev', 'A4'}, set(E), True) + cap('Hops 3–6: A2 shares a UPI id with A3, who shares', 'a device with A4. Four “new users”, one person: a ring.', 'red', y=150, h=44),
    g({'A1', 'ph', 'A2', 'upi', 'A3', 'dev', 'A4'}, set(E), True) + cap('Graph query: one traversal, milliseconds.', 'In SQL: a chain of self-joins on huge tables, often minutes.', 'green', y=150, h=44),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Catching a cashback fraud ring with a graph',
              'A promotion gives ₹500 to every new user. Fraudsters create many accounts. Each account looks innocent alone; the fraud only shows up in the connections between them.',
              'Graph traversal', 'A graph of accounts linked by shared phones, UPI ids and devices, revealing a fraud ring', fr3,
              ['Accounts are nodes, and so are the phones, UPI ids and devices they use. An edge means “this account used this phone”.',
               'Account A1 claims the new-user cashback. Alone, it looks normal.',
               'Following edges: A1 shares a phone number with A2.',
               'Continuing: A2 shares a UPI id with A3, and A3 shares a device with A4. Four “new” accounts belong to one ring, so all four claims are held. A5 is untouched.',
               'A graph database answers this with one traversal in milliseconds. In SQL each hop is another self-join on very large tables, which gets slow quickly as hops increase.'])

realworld = '''  <p>Three live scenarios: a key-value cache that saves a flash sale, a Cassandra table designed around its query, and an advanced graph search that exposes a fraud ring.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>NoSQL in Indian products you use</h3>
''' + usecase('<rect x="20" y="22" width="80" height="46" rx="6" class="s-soft-acc" style="stroke:#D64545"/><text x="60" y="50" text-anchor="middle" font-size="11" font-weight="700" class="s-red">cache</text>',
              '1. Caches, OTPs and rate limits: key-value', 'Payment, food and shopping apps use Redis or similar stores for sessions, carts, OTPs with expiry and “max 5 attempts per minute” rate limits.', ['Request', '*Redis by key (~1 ms)', 'Answer']) + usecase(
    '<text x="60" y="52" text-anchor="middle" font-size="18" font-weight="700" class="s-green mono">{ }</text>',
    '2. Product catalogues: document stores', 'Phones, sarees and groceries have completely different attributes. Shopping platforms store each product as a document with its own fields and nested variants.', ['Seller upload', '*Document per product', 'Search + product page']) + usecase(
    '<path d="M16 60 Q40 20 60 46 T104 30" style="fill:none;stroke:var(--violet);stroke-width:3"/>',
    '3. Messages and IoT: wide-column', 'Chat histories, smart-meter readings and vehicle telemetry are huge append-only streams read by key and time. Wide-column stores such as Cassandra and HBase are built for this.', ['Devices', '*Partition by device + day', 'Recent history']) + usecase(
    '<circle cx="30" cy="30" r="9" style="fill:var(--track)"/><circle cx="90" cy="30" r="9" style="fill:var(--track)"/><circle cx="60" cy="66" r="9" style="fill:var(--track)"/><path d="M30 30L90 30L60 66Z" style="fill:none;stroke:var(--track);stroke-width:2"/>',
    '4. Fraud and recommendations: graphs', 'Banks and fintechs look for rings of accounts sharing devices and identifiers; e-commerce and social apps recommend “people also bought” from relationship graphs.', ['Events', '*Graph of entities', 'Ring alerts, suggestions'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Five databases for one app?', story)
        + part(2, 'definition', 'Definition', 'What is a NoSQL database?', definition)
        + part(3, 'types', 'Types and ways to use it', 'Key-value, document, wide-column and graph', types)
        + part(4, 'steps', 'Step by step', 'One order across five databases', steps)
        + part(5, 'animation', 'See it happen', 'One app session: what Riya sees, and which database answers', '  <p>Step through the six frames. Left: Riya using the app. Right: the database that serves each step, and the query it runs.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: NoSQL under pressure', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('System design · storage choice', 'Fresher', 'SQL or NoSQL for a new feature?',
            'A ride-hailing app wants to store (a) payments, (b) the live location of every driver, updated every 4 seconds, (c) driver profiles with optional documents, and (d) “riders who travel similar routes”. Which store for each?',
            'can you justify a database choice from access patterns?',
            '<ul><li><b>Payments:</b> relational (PostgreSQL/MySQL): ACID transactions.</li><li><b>Live locations:</b> key-value (Redis) keyed by driver for the current position, plus a wide-column store (Cassandra) partitioned by driver and day for history.</li><li><b>Driver profiles:</b> document store (MongoDB): flexible optional fields.</li><li><b>Similar routes:</b> a graph or batch analytics in the lake, depending on how real-time it must be.</li></ul><p>Then mention the cost of running several systems and keeping them consistent.</p>',
            'choosing NoSQL because it is “faster” or “modern”, or MongoDB for money transfers without discussing transactions.')
        + scn('Data modelling · Cassandra', '1–3 years', 'A Cassandra table keeps timing out',
              'A messages table uses <code>PRIMARY KEY (group_id, sent_at)</code>. A few huge groups now time out on reads, and their nodes run hot.',
              'do you understand partition sizing and hot partitions?',
              '<p>Huge groups create unbounded partitions that live on one set of replicas. Re-key to bound partition size, for example <code>PRIMARY KEY ((group_id, month), sent_at)</code> or add a bucket number for very active groups. Read the latest bucket first and page backwards. Monitor partition sizes and set alerts on large partitions. Migrate by dual-writing to the new table and backfilling.</p>',
              'adding more nodes, which doesn’t split a single hot partition.')
        + scn('Reliability · caching', '1–3 years', 'Customers see old prices',
              'After adding a Redis cache in front of the product database, some customers see yesterday’s prices for hours.',
              'do you know cache invalidation and TTL trade-offs?',
              '<ol><li>Set a sensible TTL so stale entries expire (minutes, not days).</li><li>On every price update, delete or update the cache key in the same code path (cache-aside invalidation), or publish a change event that cache updaters consume.</li><li>For the final checkout price, always read from the source database.</li><li>Monitor hit ratio and staleness.</li></ol>',
              'disabling the cache entirely, or caching prices with no expiry.')
        + scn('Fundamentals · interview', 'Fresher', '“What is the difference between SQL and NoSQL?”',
              'A standard opening question in data engineering interviews.',
              'can you compare them fairly, with examples and trade-offs?',
              '<p>SQL databases store data in tables with fixed schemas, support joins and strong ACID transactions, and usually scale vertically (plus read replicas). NoSQL databases use other models (key-value, document, wide-column, graph), allow flexible schemas, scale horizontally across many nodes, and are designed around specific access patterns, often with relaxed or tunable consistency. Use SQL for transactional systems and complex ad-hoc queries; use NoSQL for very high scale, flexible records, low-latency key look-ups, time series or relationship-heavy queries. Many systems use both.</p>',
              'saying NoSQL has no schema at all, or that SQL can’t scale.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
