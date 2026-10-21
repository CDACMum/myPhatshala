import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = label_box(14, 40, 150, 80, ['orders', '40 crore rows', 'one server: full'], 'red', 10)
sc += arrow(170, 80, 206, 80, 'ink3', 2) + t(188, 70, 'split', 8.2, 'ink3')
sc += label_box(212, 30, 120, 100, ['router', 'hash(user_id) % 4', '→ shard'], 'acc', 9.6)
for k in range(4):
    y = 14 + k * 34
    sc += arrow(334, 80, 380, y + 15, 'ink3', 1.3) + label_box(384, y, 240, 30, [f'shard {k}: users with hash % 4 = {k}'], ['blue', 'green', 'violet', 'acc'][k], 8.8)
scene_svg = scene('One full orders table split by a router into four shards based on a hash of the user id.', sc,
                  'One table too big for one machine becomes <tspan font-weight="700" class="s-acc">four smaller tables on four machines</tspan>.')

story = f'''  <div class="story">
    <p class="narration">During his internship Kabir hears the phrase “we’re resharding the orders database next month” in a meeting. Later, Riya asks him what it means. He isn’t sure either, so they both go to Arjun Sir.</p>

{scene_svg}

K> Sir, the orders table has 40 crore rows and the database server is almost full. The team says they’ll “shard” it. Is that like making a backup copy?
A> No, a copy is <b>replication</b>, our next lesson. <b>Sharding</b> means <i>splitting</i> the data: some users' orders on machine 0, others on machine 1, and so on. Each machine holds only a part, so together they hold far more and share the work.
R> Like a library that puts books A to F on one shelf and G to M on another?
A> Exactly, Riya. That’s <b>range partitioning</b>. Another way is to hash each key, like a lucky-number formula, so the data spreads evenly. The big decision is the <b>partition key</b>: the field that decides where each row goes.
K> And if we choose the wrong key?
A> Then one shard gets overloaded while others sit idle, or simple queries suddenly have to ask every machine. Today you’ll see what happens when a shard is added, why one celebrity kitchen can melt a shard, and why partitioning by date makes “today” a hotspot.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Partitioning at three levels
L1> Shelves in a library, coaches in a train
      <ul>
        <li><b>Partitioning</b> means splitting a big collection into smaller parts. A library splits books across shelves; a train splits passengers across coaches.</li>
        <li><b>Range:</b> shelf 1 for A–F, shelf 2 for G–M. Easy to find a range (“all books starting with C”), but some shelves can get crowded.</li>
        <li><b>Hash:</b> a formula turns each name into a number and picks a shelf. Books spread evenly, but “all books starting with C” means checking every shelf.</li>
        <li><b>Directory:</b> a notebook at the entrance lists which shelf each book is on. Flexible, but the notebook must always be available.</li>
      </ul>
      <p><b>The key question:</b> which field decides the shelf? Choose the one most queries use, with many different values.</p>
L2> Strategies, keys and where partitioning shows up
      <ul>
        <li><b>Horizontal vs vertical:</b> horizontal partitioning splits <i>rows</i> (sharding when the parts are on different machines); vertical partitioning splits <i>columns</i> into separate tables or stores.</li>
        <li><b>Good partition key:</b> high cardinality (many distinct values), even distribution, and present in most queries. User id is often good for an app; city is usually poor (few values, very uneven).</li>
        <li><b>Routing:</b> a router or the client library computes the shard from the key. Queries with the key go to one shard; queries without it must ask every shard and merge results (<b>scatter-gather</b>).</li>
        <li><b>Everywhere in big data:</b> HDFS blocks, Spark partitions, Kafka topic partitions (ordering is guaranteed only within one partition), Cassandra and DynamoDB partition keys, and date folders in a lake (<code>date=2026-10-19/</code>) used for pruning.</li>
      </ul>
L3> Rebalancing, consistent hashing and hot keys
      <ul>
        <li><b>The mod-N problem:</b> with <code>hash(key) % N</code>, changing N from 4 to 5 moves about 80% of keys, a huge data migration.</li>
        <li><b>Consistent hashing:</b> place shards and keys on a ring; each key belongs to the next shard clockwise. Adding a shard moves only about 1/N of keys. <b>Virtual nodes</b> (many points per shard) keep the load even. Used in Cassandra, DynamoDB and many caches.</li>
        <li><b>Fixed partitions:</b> another approach (Kafka, Elasticsearch, Couchbase) creates many more partitions than machines up front and moves whole partitions when nodes join.</li>
        <li><b>Hot keys:</b> one huge customer or one viral event overloads one shard. Fixes: split the key with a suffix (key + random 0–9), cache it, or give it a dedicated shard.</li>
        <li><b>Secondary indexes:</b> a <i>local</i> index per shard makes writes cheap but reads scatter-gather; a <i>global</i> index partitioned by the indexed field makes reads cheap but writes touch several shards.</li>
        <li><b>Cross-shard work:</b> joins and transactions across shards are slow and complex, so data that is used together should share a partition key (for example user id on both orders and payments).</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Partitioning</b> divides a large dataset into smaller, independent subsets called partitions, so that storage and processing can be spread across resources. <b>Horizontal partitioning</b> splits rows by the value of a <b>partition key</b>; when the partitions live on different servers it is called <b>sharding</b>. Common strategies are <b>range</b> partitioning (contiguous key ranges), <b>hash</b> partitioning (a hash function of the key) and <b>directory/list</b> partitioning (an explicit mapping). <b>Vertical partitioning</b> splits columns into separate tables.',
    'Partitioning means cutting a huge table into smaller pieces by some rule, for example by user id or by date. Sharding is when those pieces are put on different machines, so each machine stores and handles only part of the data.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Partition / shard', 'One piece of the data. “Shard” is used when the pieces are on different database servers.'),
    ('Partition key', 'The field whose value decides which partition a row goes to.'),
    ('Cardinality', 'The number of distinct values a field has. User id: crores. City: a few dozen.'),
    ('Router', 'The component that maps a key to its shard.'),
    ('Scatter-gather', 'Sending a query to every shard and merging the answers.'),
    ('Rebalancing', 'Moving data between shards when machines are added or removed.'),
    ('Consistent hashing', 'A hashing scheme where adding or removing a shard moves only a small fraction of keys.'),
    ('Hot partition / hot key', 'A partition or key that receives far more traffic than others.'),
]) + '''

  <h3>Partitioning across the big data stack</h3>
''' + facts([
    ('HDFS', 'files split into 128 MB blocks spread over DataNodes'),
    ('Spark', 'DataFrames split into partitions processed in parallel; shuffles repartition by key'),
    ('Kafka', 'topics split into partitions; order is kept only within a partition; partition count limits consumer parallelism'),
    ('Cassandra / DynamoDB', 'partition key hashed onto a ring of nodes'),
    ('Data lake / warehouse', 'tables partitioned by date or region folders; queries skip partitions they don’t need'),
    ('Sharded SQL', 'MySQL/PostgreSQL shards behind a router (for example Vitess or Citus)'),
]) + lv + '''
EXAM> Define partitioning and sharding, then explain <b>range, hash and directory</b> partitioning with one example and one advantage and disadvantage each. Mention how to choose a partition key and the hot-spot problem. A small diagram of keys going to shards earns extra marks.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Range partitioning', 'Contiguous ranges of the key: dates, ids 1–10 lakh, names A–F. Great for range queries; risk of hotspots on the newest range.', 'Ordered ranges'),
    ('Hash partitioning', 'hash(key) decides the partition. Even spread, no hotspots from ordering; range queries must hit every partition.', 'Even spread'),
    ('Directory / list', 'A lookup table maps keys (or groups like regions) to partitions. Very flexible; the directory must be fast and highly available.', 'Lookup table'),
    ('Composite', 'Combine methods: hash on user id to pick a shard, then range on date inside it. Common in Cassandra-style keys.', 'Hash + range'),
]) + '''

  <h3>Side by side</h3>
''' + table(['', 'Range', 'Hash', 'Directory'], [
    ['<b>How a row is placed</b>', 'Which range its key falls in', 'hash(key) % N or on a ring', 'Look up the key in a table'],
    ['<b>Range queries</b>', 'Efficient (few partitions)', 'Must ask all partitions', 'Depends on the mapping'],
    ['<b>Balance</b>', 'Can be uneven; newest range is hot', 'Even for good keys', 'Can be tuned by hand'],
    ['<b>Adding a node</b>', 'Split a range', 'mod-N moves most keys; consistent hashing moves ~1/N', 'Update the directory'],
    ['<b>Example</b>', 'Orders by month', 'Users by hash(user_id)', 'Tenants mapped to shards'],
]) + '''

  <h3>Choosing a partition key</h3>
''' + table(['Candidate key', 'Distinct values', 'Spread', 'Used in most queries?', 'Verdict'], [
    ['city', 'about 50', 'Very uneven (metros dominate)', 'Sometimes', 'Poor'],
    ['order_date', '365 per year', 'All writes hit today', 'For reports, yes', 'Good for analytics, poor for live writes'],
    ['user_id', 'crores', 'Even', 'Yes (my orders, my payments)', 'Good for the app'],
    ['order_id', 'billions', 'Even', 'Only for single-order look-ups', 'Good spread, but user queries scatter'],
], minw=620) + '''
TIP> Partition by what you <b>query</b>, not by what you <b>store</b>. If the app always asks “orders of this user”, partition by user id. If analysts always ask “orders on this date”, partition the lake table by date. The same data can be partitioned differently in different systems.'''

# ---------------------------------------------------------------- steps
c1 = '''import hashlib
def shard_for(user, n=4):
    return int(hashlib.md5(user.encode()).hexdigest(), 16) % n
for u in ["U9", "U42", "U777", "U1001"]:
    print(u, "-> shard", shard_for(u))'''
c2 = '''ranges = [("2026-01", "2026-03", "P0"), ("2026-04", "2026-06", "P1"),
          ("2026-07", "2026-09", "P2"), ("2026-10", "2026-12", "P3")]
def part_for(month):
    return next(p for lo, hi, p in ranges if lo <= month <= hi)
print("2026-10 ->", part_for("2026-10"), "| 2026-02 ->", part_for("2026-02"))'''
c3 = '''import hashlib
h = lambda k: int(hashlib.md5(k.encode()).hexdigest(), 16)
keys = [f"U{i}" for i in range(1000)]
moved = sum(1 for k in keys if h(k) % 4 != h(k) % 5)
print(f"mod-N, 4 -> 5 shards: {moved / len(keys):.0%} of keys move")'''
c4 = '''directory = {"tenant_acme": "shard-A", "tenant_bigbazaar": "shard-B", "tenant_small_1": "shard-C"}
print(directory["tenant_bigbazaar"])
directory["tenant_bigbazaar"] = "shard-D"     # move a big tenant to its own shard
print(directory["tenant_bigbazaar"])'''
steps = stepper([
    ('Pick the partition key',
     '<p>TiffinGo’s app mostly asks “show <i>this user’s</i> orders” and “place an order for <i>this user</i>”. So the orders table is partitioned by <code>user_id</code>.</p>',
     'The key decides everything else: balance, which queries are fast, and which queries must visit every shard.'),
    ('Hash partitioning spreads users evenly',
     code('python', 'hash_route.py', c1, run_code(c1)),
     'A stable hash (here MD5; never Python’s <code>hash()</code>, which changes between runs) turns each user id into a big number; <code>% 4</code> picks one of four shards. Similar ids land on different shards, so load spreads evenly.'),
    ('Range partitioning keeps dates together',
     code('python', 'range_route.py', c2, run_code(c2)),
     'For analytics, ranges of dates are natural: a report on October reads only P3. The catch: every new order goes into the newest range, so one partition takes all the writes.'),
    ('The trouble with % N when you grow',
     code('python', 'mod_n.py', c3, run_code(c3)),
     'Going from 4 to 5 shards changes <code>hash % N</code> for most keys, so most of the data would have to move. Consistent hashing reduces this to roughly one fifth (see scenario 1).'),
    ('Directory partitioning for special cases',
     code('python', 'directory.py', c4, run_code(c4)),
     'A lookup table lets you place big customers deliberately and move them without rehashing anyone else. It is common in multi-tenant SaaS products. The directory itself must be fast and highly available.'),
    ('Queries with and without the key',
     '<p>“Orders of U42” goes to one shard. “All orders from Pune today” has no user id, so the router asks all shards and merges the results.</p>',
     'Scatter-gather works, but it gets slower and costlier as shards grow. Such analytical questions are better answered from a data lake or warehouse copy partitioned by date.'),
])

# ---------------------------------------------------------------- two-view animation
def ph(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
def laptop(title, inner):
    return ('<rect x="40" y="20" width="280" height="168" rx="10" class="s-board"/><rect x="50" y="32" width="260" height="144" rx="4" class="s-card2"/><path d="M24 198h312l-12 14H36z" style="fill:#2B3A34"/>' + t(180, 48, title, 9.4, bold=True) + inner)
see = [
    ph('My orders', t(180, 100, 'Loading…', 9, 'ink2')),
    ph('My orders', ''.join(t(138, 70 + k * 20, f'O10{43 - k}', 8.4, anchor='start', mono=True) + t(222, 70 + k * 20, ['₹420', '₹180', '₹250', '₹90'][k], 8.4, anchor='end', bold=True) for k in range(4))),
    ph('My orders', ''.join(t(138, 70 + k * 20, f'O10{43 - k}', 8.4, anchor='start', mono=True) + t(222, 70 + k * 20, ['₹420', '₹180', '₹250', '₹90'][k], 8.4, anchor='end', bold=True) for k in range(4)) + t(180, 170, 'loaded in 8 ms', 8.6, 'green', bold=True)),
    laptop('Support console', t(60, 76, "Search: all orders from Pune today", 8.8, 'blue', anchor='start') + t(180, 130, 'searching…', 9, 'ink2')),
    laptop('Support console', t(60, 76, "Search: all orders from Pune today", 8.8, 'blue', anchor='start') + t(180, 120, '41,236 orders', 12, bold=True) + t(180, 142, 'took 2.4 s', 9, 'red', bold=True)),
    laptop('Support console', t(60, 76, "Search: all orders from Pune today", 8.8, 'blue', anchor='start') + t(180, 120, '41,236 orders', 12, bold=True) + t(180, 142, 'now 0.3 s (from the analytics copy)', 9, 'green', bold=True)),
]
def shards(hl=None, all_=False, extra=''):
    o = label_box(130, 20, 100, 36, ['router'], 'acc', 9.4)
    for k in range(4):
        x = 12 + k * 86
        on = all_ or hl == k
        o += label_box(x, 110, 78, 50, [f'shard {k}', ['users A', 'users B', 'users C', 'users D'][k]], ('red' if all_ else 'green') if on else 'card', 9)
        o += arrow(180, 58, x + 39, 108, 'red' if all_ else ('green' if on else 'ink3'), 2 if on else 1, dash=not on)
    return o + extra
behind = [
    shards() + t(180, 180, 'request: orders of user U9', 9, 'ink', bold=True) + t(180, 202, 'The router receives the request with user_id = U9.', 9, 'ink2'),
    shards(3) + t(180, 180, 'hash(U9) % 4 = 3', 9, 'green', bold=True, mono=True) + t(180, 202, 'The key tells the router exactly which shard to ask.', 9, 'ink2'),
    shards(3) + t(180, 202, 'One shard answers with 4 rows. Other shards are untouched.', 9, 'ink2'),
    shards() + t(180, 180, 'query: city = Pune (no user_id)', 9, 'red', bold=True) + t(180, 202, 'The query has no shard key.', 9, 'ink2'),
    shards(all_=True) + t(180, 180, 'scatter to all 4, gather, merge', 9, 'red', bold=True) + t(180, 202, 'Every shard scans its data; the router merges the answers.', 9, 'ink2'),
    label_box(20, 30, 140, 60, ['app shards', 'by user_id', '(live orders)'], 'green', 9) + arrow(162, 60, 196, 60) + label_box(200, 30, 140, 60, ['lake table', 'by date, city', '(analytics copy)'], 'blue', 9) + t(180, 130, 'Same data, partitioned twice:', 9.4, bold=True) + t(180, 150, 'by user for the app, by date for analysis.', 9, 'ink2'),
]
see_caps = ['Riya opens “My orders”.', 'Her last four orders appear.', 'The whole list loaded in about 8 milliseconds.',
            'A support agent searches for all of today’s orders from Pune.', 'The search works but takes 2.4 seconds.', 'After the fix, the same search takes 0.3 seconds.']
behind_caps = ['The request reaches the router carrying Riya’s user id, U9.',
               'The router hashes the shard key: hash(U9) % 4 = 3. Only shard 3 holds her orders.',
               'Shard 3 returns four rows. The other three shards don’t do any work at all.',
               'The support search filters by city, which is not the shard key.',
               'So the router must <b>scatter</b> the query to all four shards and <b>gather</b> and merge the results: slower, and it grows with every shard added.',
               'The fix is to answer analytical questions from a copy partitioned for them: a lake or warehouse table partitioned by date and city. (Timings are illustrative.)']
two = anim_two('Queries on a sharded database', 'What users see, and how the router finds the data', 'Riya opening her orders and an agent searching all orders from one city',
               'A router sending one query to one shard and another query to all shards', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: adding a shard (real numbers from shard_lab.out)
def keys_grid(moved_frac, color):
    o = ''
    for i in range(100):
        x = 20 + (i % 20) * 16
        y = 40 + (i // 20) * 16
        mv = (i * 37 % 100) < moved_frac
        o += fill(x, y, 12, 12, color if mv else 'grey', rx=2, opacity=None if mv else .7)
    return o
fr1 = [
    keys_grid(0, 'red') + t(180, 26, '3,000 users on 4 shards', 9.6, bold=True) + cap('Traffic grows. We add a 5th shard.', 'How many users must move to a different shard?', 'card', y=130, h=44),
    keys_grid(80, 'red') + t(180, 26, 'hash % N: 4 → 5', 9.6, 'red', bold=True, mono=True) + cap('80% of users change shard (2,412 of 3,000).', 'Almost the whole database must be copied.', 'red', y=130, h=44),
    '<circle cx="180" cy="94" r="62" style="fill:none;stroke:var(--line);stroke-width:8"/>' + ''.join(f'<circle cx="{180 + 62 * __import__("math").cos(a)}" cy="{94 + 62 * __import__("math").sin(a)}" r="7" style="fill:{c}"/>' for a, c in [(0.3, 'var(--blue)'), (1.9, 'var(--green)'), (3.4, 'var(--violet)'), (4.9, 'var(--track)')]) + t(180, 98, 'hash ring', 9, 'ink3') + cap('Consistent hashing: shards and keys sit on a ring;', 'each key belongs to the next shard clockwise.', 'blue', y=168, h=44),
    '<circle cx="180" cy="94" r="62" style="fill:none;stroke:var(--line);stroke-width:8"/>' + ''.join(f'<circle cx="{180 + 62 * __import__("math").cos(a)}" cy="{94 + 62 * __import__("math").sin(a)}" r="7" style="fill:{c}"/>' for a, c in [(0.3, 'var(--blue)'), (1.9, 'var(--green)'), (3.4, 'var(--violet)'), (4.9, 'var(--track)'), (2.6, '#D64545')])
    + '<path d="M118 94 A62 62 0 0 1 128 61" style="fill:none;stroke:#D64545;stroke-width:8"/>' + t(180, 98, 'new shard S4', 9, 'red', bold=True) + cap('The new shard takes over only one arc of the ring.', 'Keys elsewhere stay where they are.', 'blue', y=168, h=44),
    keys_grid(22, 'green') + t(180, 26, 'consistent hashing: 4 → 5', 9.6, 'green', bold=True) + cap('Only 22% of users move (653 of 3,000).', 'Virtual nodes keep each shard’s share even.', 'green', y=130, h=44),
]
s1 = anim_one('Real-time scenario 1', 'Adding a fifth shard: who has to move?',
              'These numbers come from the program in “Run it on your PC”: 3,000 users on 4 shards, then a 5th shard is added. Compare simple <code>hash % N</code> with consistent hashing.',
              'Rebalancing', 'Keys that must move when adding a shard, with modulo hashing and with consistent hashing', fr1,
              ['3,000 users are spread over 4 shards. Traffic grows, so a fifth shard is added.',
               'With <code>hash(user) % N</code>, changing N from 4 to 5 changes the shard for 80% of users. Almost all data must be copied while the system is live.',
               '<b>Consistent hashing</b> places shards (and many virtual points per shard) on a ring. Each key goes to the next shard point clockwise.',
               'A new shard takes over only the keys on its own arcs of the ring; every other key stays put.',
               'Only 22% of users move, close to the ideal of one in five. Cassandra, DynamoDB and many caches use this idea.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: hot key
def load_bars(vals, hot=None, note=None):
    rows = [(f'shard {k}', v, 'red' if (hot is not None and k == hot) else 'green', f'{v}%') for k, v in enumerate(vals)]
    return t(14, 22, 'CPU per shard', 9, 'ink2', anchor='start') + bars(rows, x=90, y=32, w=210, gap=22)
fr2 = [
    load_bars([40, 42, 38, 41]) + cap('Normal day: orders spread evenly by kitchen_id.', '', 'green', y=130, h=34),
    load_bars([44, 100, 40, 43], hot=1) + cap('A famous biryani kitchen runs a ₹1 offer. Its orders', 'all hash to shard 1, which is overloaded: a hot key.', 'red', y=124, h=44),
    load_bars([44, 100, 40, 43], hot=1) + cap('Adding shards doesn’t help: one key always maps', 'to one shard, however many shards there are.', 'red', y=124, h=44),
    load_bars([62, 64, 61, 63]) + box(14, 122, 332, 30, 'card') + t(180, 141, 'key = kitchen_id + "#" + random(0–9)', 8.8, mono=True) + cap('Fix: split the hot key into 10 sub-keys', 'spread over shards; readers combine the parts.', 'green', y=158, h=44),
    load_bars([45, 47, 44, 46]) + cap('Plus: cache the menu, and queue order writes', 'so short bursts are smoothed out.', 'green', y=130, h=44),
]
s2 = anim_one('Real-time scenario 2', 'One viral offer melts one shard',
              'Orders are sharded by kitchen. Then one famous kitchen announces a ₹1 biryani offer at 8 pm. Watch the CPU of each shard.',
              'Hot key', 'CPU per shard when one key becomes extremely popular, and the fix by splitting the key', fr2,
              ['On a normal day kitchens are spread evenly, so every shard runs at around 40% CPU.',
               'The viral offer sends a flood of orders for one kitchen id. Every one of them hashes to shard 1, which hits 100% while the others stay calm.',
               'Adding more shards changes nothing for this key: one key always maps to exactly one shard.',
               '<b>Split the hot key:</b> append a random suffix 0–9 so the kitchen’s orders spread over ten sub-keys on different shards; reads combine the parts.',
               'Caching the menu and queueing order writes smooth the burst further. (Load figures are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): date range hotspot vs pruning
def months(hl_write=None, hl_read=None, composite=False):
    o = ''
    names = ['Jul', 'Aug', 'Sep', 'Oct']
    for k, n in enumerate(names):
        x = 14 + k * 84
        tone = 'card'
        if hl_write is not None and k == hl_write:
            tone = 'red'
        if hl_read is not None and k in hl_read:
            tone = 'green'
        o += label_box(x, 40, 78, 44, [n, 'partition'], tone, 9.4)
    return o
fr3 = [
    months() + t(180, 26, 'Orders range-partitioned by month', 9.6, 'acc', bold=True) + cap('Reports love this: “October revenue” reads one partition.', '', 'blue', y=110, h=34),
    months(hl_read={3}) + t(180, 26, 'Report for October → 1 of 4 partitions', 9.6, 'green', bold=True) + cap('Partition pruning: the other months are skipped.', '', 'green', y=110, h=34),
    months(hl_write=3) + t(180, 26, 'But all new orders go to October', 9.6, 'red', bold=True) + cap('Writes: 100% on the newest partition (a moving hotspot).', 'Older partitions sit idle for writes.', 'red', y=104, h=44),
    ''.join(label_box(14 + k * 84, 40, 78, 44, [f'bucket {k}', 'Oct, hashed'], 'green', 9) for k in range(4)) + t(180, 26, 'Composite: hash bucket + date', 9.6, 'green', bold=True, mono=True)
    + cap('Key = (hash(order_id) % 4, date). New orders spread', 'over 4 buckets; a date range reads 4 small pieces.', 'green', y=104, h=44),
    box(14, 30, 332, 96, 'card') + t(180, 50, 'Choose per system', 9.8, 'acc', bold=True) + t(28, 72, '• live order database: hash by user_id (even writes)', 8.6, anchor='start') + t(28, 90, '• lake table: partition by date (prune reports)', 8.6, anchor='start') + t(28, 108, '• time series store: bucket + time (both)', 8.6, anchor='start')
    + cap('The same data, partitioned differently for each job.', '', 'blue', y=140, h=34),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Partitioning by date: great for reports, bad for writes',
              'Range partitioning by date makes date-range reports fast, but it creates a moving hotspot: every new row lands in the newest partition. Watch the trade-off and the composite-key fix.',
              'Range hotspots', 'Monthly partitions showing pruning for reads, a write hotspot, and a composite key', fr3,
              ['Orders are range-partitioned by month: July, August, September, October.',
               'A report on October reads only the October partition and skips the rest: <b>partition pruning</b>.',
               'But every new order belongs to the current month, so all writes hit one partition while the others sit idle. The hotspot moves forward every month.',
               'A <b>composite key</b> adds a hash bucket in front of the date: new orders spread over four buckets, and a date-range query reads four small pieces instead of one.',
               'In practice each system is partitioned for its job: the live database by user id, the lake by date, and time-series stores by bucket plus time.'])

realworld = '''  <p>Three live scenarios: adding a shard with and without consistent hashing (real numbers), a viral offer that overloads one shard, and an advanced look at the date-partitioning trade-off.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Partitioning in real systems</h3>
''' + usecase('<rect x="14" y="22" width="22" height="46" rx="3" style="fill:var(--blue)"/><rect x="40" y="22" width="22" height="46" rx="3" style="fill:var(--green)"/><rect x="66" y="22" width="22" height="46" rx="3" style="fill:var(--violet)"/><rect x="92" y="22" width="14" height="46" rx="3" style="fill:var(--track)"/>',
              '1. Payment and order databases sharded by user', 'Large payment apps and marketplaces shard their transactional databases by user or merchant id, so a user’s history and new payments stay on one shard, and add shards as users grow.', ['Request with user_id', '*Router → one shard', 'Fast, isolated']) + usecase(
    '<path d="M16 45h88" style="stroke:var(--violet);stroke-width:3"/><rect x="20" y="34" width="20" height="22" rx="3" style="fill:var(--violet)"/><rect x="50" y="34" width="20" height="22" rx="3" style="fill:var(--violet);opacity:.7"/><rect x="80" y="34" width="20" height="22" rx="3" style="fill:var(--violet);opacity:.5"/>',
    '2. Kafka topics with many partitions', 'An orders topic might have 48 partitions keyed by order id, so 48 consumers can process in parallel while each order’s events stay in order within its partition.', ['Producers', '*48 partitions by key', '48 consumers']) + usecase(
    '<rect x="16" y="20" width="88" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="49" text-anchor="middle" font-size="9" class="s-blue mono">date=2026-10-19</text>',
    '3. Lake tables partitioned by date', 'Almost every analytics table in a lake is partitioned by event date (sometimes also region), so daily jobs and reports scan only the days they need.', ['Daily data', '*date=… folders', 'Pruned queries']) + usecase(
    '<circle cx="60" cy="45" r="28" style="fill:none;stroke:var(--green);stroke-width:5"/><circle cx="88" cy="45" r="6" style="fill:var(--green)"/><circle cx="46" cy="21" r="6" style="fill:var(--green)"/><circle cx="46" cy="69" r="6" style="fill:var(--green)"/>',
    '4. Distributed caches and NoSQL rings', 'Cassandra, DynamoDB and distributed caches place keys on a consistent-hash ring, so nodes can be added or replaced with only a small share of keys moving.', ['Key', '*Position on ring', 'Owner node'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', '“We’re resharding next month”', story)
        + part(2, 'definition', 'Definition', 'What are partitioning and sharding?', definition)
        + part(3, 'types', 'Types and ways to use it', 'Range, hash, directory and composite partitioning', types)
        + part(4, 'steps', 'Step by step', 'Sharding an orders table', steps)
        + part(5, 'animation', 'See it happen', 'Two queries: one shard or all shards', '  <p>Step through the six frames. Left: Riya checking her orders and a support agent searching by city. Right: how the router finds the data.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: partitions under pressure', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('System design · partitioning', 'Fresher', 'Choose a shard key for a chat app',
            'A chat app stores messages. The main screens are “messages in this conversation, newest first” and “my conversations”. Messages reach crores per day. How would you partition the messages table?',
            'can you choose a key from the access pattern and spot hotspots?',
            '<p>Partition by <code>conversation_id</code> (all messages of a chat together, so one query reads one partition), clustered by time descending. Bound partition size for huge group chats by adding a time bucket: <code>(conversation_id, month)</code>. Keep “my conversations” in a separate table partitioned by <code>user_id</code>. Avoid partitioning by date (write hotspot) or by user for messages (a conversation would span many partitions).</p>',
            'picking a key without saying which queries it serves.')
        + scn('Operations · rebalancing', '1–3 years', 'We need to go from 8 to 12 shards',
              'A sharded MySQL setup uses <code>user_id % 8</code>. Growth means you need 12 shards. How do you migrate safely?',
              'do you understand the cost of mod-N resharding and safe migration steps?',
              '<ol><li>Recognise that changing the modulus moves most users. Consider moving to a directory-based or consistent-hash scheme, or to many logical shards (for example 1,024) mapped onto physical servers, so future growth moves whole logical shards.</li><li>Copy data to the new layout in the background, then dual-write new changes to old and new locations.</li><li>Verify counts and checksums per user range.</li><li>Switch reads gradually, then writes; keep a rollback path.</li><li>Finally, clean up the old copies.</li></ol>',
              'changing the modulus in production and copying everything in one big bang.')
        + scn('Streaming · Kafka', '1–3 years', 'Order events are processed out of order',
              'Consumers sometimes process “order delivered” before “order placed” for the same order. The topic has 12 partitions and producers don’t set a message key.',
              'do you know how Kafka partitioning affects ordering?',
              '<p>Without a key, messages are spread across partitions, and Kafka guarantees order only within one partition. Set the message key to <code>order_id</code> so all events for an order go to the same partition and are consumed in order by one consumer. Choose enough partitions for the needed parallelism, and watch for hot keys. Changing partition count later remaps keys, so plan it up front.</p>',
              'adding a sleep in consumers or using a single partition for everything.')
        + scn('Fundamentals · interview', 'Fresher', '“What is the difference between partitioning and replication?”',
              'Interviewers often ask this to check basic distributed-systems vocabulary.',
              'can you separate splitting data from copying data?',
              '<p><b>Partitioning (sharding)</b> splits data into parts so each node stores and processes only a subset; it increases capacity and throughput. <b>Replication</b> stores copies of the same data on several nodes; it increases availability, durability and read capacity. Real systems use both: each partition is replicated (for example HDFS blocks with 3 replicas, Kafka partitions with a replication factor, Cassandra partitions on several nodes).</p>',
              'using the two words as if they mean the same thing.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
