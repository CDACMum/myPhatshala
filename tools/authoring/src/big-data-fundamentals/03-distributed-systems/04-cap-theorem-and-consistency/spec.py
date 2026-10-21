import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='03-distributed-systems', lesson='04-cap-theorem-and-consistency', n='3.4',
    module_label='Module 3 · Distributed Systems Concepts',
    title='The CAP theorem and consistency models',
    desc='The CAP theorem explained correctly: consistency, availability and partition tolerance, CP vs AP systems, why “pick two” is a myth, PACELC, the consistency ladder (linearizable, sequential, causal, read-your-writes, eventual), tunable quorums, last-write-wins, version vectors and CRDTs. UPI vs Instagram-likes examples, animations and a partition simulator for your PC.',
    og_desc='Why can like counts disagree but your bank balance can\'t? Learn the CAP theorem, PACELC and consistency models with real-time scenarios.',
    minutes=30, level='Beginner → Advanced',
    lead='Your reel shows 1,024 likes while your cousin sees 1,021, yet your bank makes you wait rather than risk a wrong balance. Both are distributed systems facing the same choice. In this lesson you learn what the <b>CAP theorem</b> really says (and the popular myth it isn\'t), compare CP and AP behaviour during a network split, merge a shopping cart correctly, and see why consistency costs latency even on good days (<b>PACELC</b>).',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Partition simulator on your PC'],
)

RUN = dict(
    heading='A network partition, handled CP and AP',
    intro='<p>Three replicas are split into {A} and {B, C}. In CP mode only the majority side accepts writes; in AP mode both sides accept and the values diverge. Run it, then try the challenges: quorum checks, read-your-writes, last-write-wins vs a CRDT counter, a cart merge and a PACELC latency estimate.</p>',
    code='''replicas = ["A", "B", "C"]
sides = [{"A"}, {"B", "C"}]
majority = len(replicas) // 2 + 1

def side_of(node):
    return next(s for s in sides if node in s)

def write(mode, node, value, store):
    side = side_of(node)
    if mode == "CP" and len(side) < majority:
        return "refused (minority side)"
    for n in side:
        store[n] = value
    return "accepted"

for mode in ["CP", "AP"]:
    store = {n: 100 for n in replicas}
    r1 = write(mode, "A", 40, store)
    r2 = write(mode, "B", 70, store)
    print(f"{mode}: via A {r1:24} via B {r2:9} -> {store}")
''',
    anno=[
        ('majority = len(replicas) // 2 + 1', 'With 3 replicas a majority is 2. Only a side with at least 2 nodes may make decisions in CP mode.'),
        ('if mode == "CP" and len(side) < majority:', 'CP gives up availability on the minority side: it refuses rather than risk a conflicting value.'),
        ('for n in side:', 'In AP mode each side updates its own copies, so after both writes the copies disagree.'),
    ],
    tasks=[
        dict(label='1 · CP vs AP', hint='Press <b>Run</b>. Then change the partition to <code>[{"A", "B"}, {"C"}]</code> and repeat. Which writes are refused now?', code=None),
        dict(label='2 · Quorum overlap', hint='A read is guaranteed to see the latest write when R + W > N. Print a table for N = 5 and mark the settings that survive 2 failed nodes for both reads and writes.',
             code='''N = 5
for W in range(1, N + 1):
    for R in range(1, N + 1):
        consistent = R + W > N
        tolerant = (N - W >= 2) and (N - R >= 2)
        if consistent and tolerant:
            print(f"W={W} R={R}: consistent and survives 2 failures")
'''),
        dict(label='3 · Read-your-writes', hint='Each user remembers the version of their last write; a replica can serve their read only if it has reached that version. Change replica versions and see which can serve Riya.',
             code='''replica_version = {"r1": 41, "r2": 44, "r3": 39}
user_last_write = {"riya": 43, "kabir": 30}
for user, needed in user_last_write.items():
    ok = [r for r, v in replica_version.items() if v >= needed]
    print(f"{user} needs version {needed}: can read from {ok or ['leader only']}")
'''),
        dict(label='4 · LWW vs CRDT', hint='Two sides counted likes during a split. Last-write-wins keeps one side; a G-counter adds both sides\' increments. Add a third side with 4 likes.',
             code='''base = 1000
side_increments = {"A": 3, "B": 5}
lww = base + side_increments["B"]                  # keep the "latest" side only
crdt = base + sum(side_increments.values())        # add every side's increments
print("last-write-wins:", lww, "| CRDT counter:", crdt, "| likes lost by LWW:", crdt - lww)
'''),
        dict(label='5 · Cart merge (advanced)', hint='An OR-Set records adds and removes with unique tags; an item is present if it has an add tag not cancelled by a remove. Remove “lassi” on side 2 and merge.',
             code='''side1 = {"adds": {("thali", 1), ("lassi", 2)}, "removes": set()}
side2 = {"adds": {("thali", 1), ("lassi", 2), ("jamun", 3)}, "removes": {("lassi", 2)}}
adds = side1["adds"] | side2["adds"]
removes = side1["removes"] | side2["removes"]
cart = sorted({item for item, tag in adds if (item, tag) not in removes})
print("merged cart:", cart)
'''),
        dict(label='6 · PACELC latency (advanced)', hint='A strongly consistent write waits for the fastest majority of replicas. Compute write latency for majority and for all replicas. Move the third replica from Frankfurt to Chennai (15 ms).',
             code='''rtt_ms = {"Mumbai": 1, "Singapore": 60, "Frankfurt": 120}   # round trip from Mumbai
times = sorted(rtt_ms.values())
majority = len(times) // 2 + 1
print("async write    :", times[0], "ms")
print("majority write :", times[majority - 1], "ms")
print("all replicas   :", times[-1], "ms")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: CP, AP and merging after a split',
    intro='<p>This program splits three replicas into {A} and {B, C}. In CP mode it refuses writes on the minority side; in AP mode it lets both sides count likes, then merges them two ways: last-write-wins, which loses likes, and a CRDT counter, which keeps them all. Save it as <code>cap_sim.py</code> and run it.</p>',
    items=[
        dict(title='CAP choices and conflict resolution', file='cap_sim.py',
             cmd=open(os.path.join(HERE, 'cap_sim.py')).read() + '\n# In a terminal:  python cap_sim.py',
             output=open(os.path.join(HERE, 'cap_sim.out')).read(),
             note='Recorded from a real run with Python 3.13; the simulation is deterministic. These are the numbers used in scenario 1. Try moving node C to A\'s side of the partition: which side can accept writes in CP mode now?'),
    ],
)

TRACE = dict(
    heading='Merging a G-counter, one line at a time',
    intro='<p>A G-counter (a CRDT) keeps one count per replica. Two replicas counted likes independently; merging takes the maximum for each replica\'s slot, then the total is the sum. Watch nothing get lost.</p>',
    code='''a = {"A": 3, "B": 0}
b = {"A": 0, "B": 5}
merged = {}
for node in a:
    merged[node] = max(a[node], b[node])
total = 1000 + sum(merged.values())
print(merged, total)
''',
    notes={1: 'Replica A :: Its own slot counts the 3 likes it received; it hasn\'t heard about B\'s likes yet.',
           5: 'Merge :: Taking the maximum per slot is safe to repeat and order doesn\'t matter.',
           6: 'Total :: The counter\'s value is the sum of all slots: no like is lost.'},
)

WORKED_INTRO = 'Four consistency problems, from classifying data to merging concurrent updates. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='System design · classification', title='CP or AP for each kind of data?',
         problem='<p>Decide CP or AP for each piece of data using one question: during a network fault, is a wrong answer worse than an error?</p>',
         inp='wallet balance, like count, seat booking, product reviews, leader election',
         approach=['For each item, record whether a wrong answer is worse than an error.',
                   'Wrong answer worse → CP. Error worse → AP.',
                   'Print the decisions.'],
         code='''data = [("wallet balance", True), ("like count", False), ("seat booking", True),
        ("product reviews", False), ("leader election", True)]
for name, wrong_is_worse in data:
    choice = "CP (refuse when unsure)" if wrong_is_worse else "AP (answer, reconcile later)"
    print(f"{name:16} -> {choice}")
''', notes={3: 'Decide :: The business impact decides, not the technology.'},
         tryit='Add “OTP verification”, “shopping cart” and “stock of a limited-edition phone”. Defend each choice in one sentence.'),
    dict(level='i', tag='Distributed DB · quorums', title='Check consistency levels for a Cassandra cluster',
         problem='<p>A table has replication factor 3. For each (write level, read level) pair, decide whether reads always see the latest write and how many replica failures each operation tolerates.</p>',
         inp='levels ONE = 1, QUORUM = 2, ALL = 3',
         approach=['Map level names to numbers of replicas.',
                   'Consistent if R + W > N.',
                   'An operation tolerates N − level failed replicas.'],
         code='''N = 3
level = {"ONE": 1, "QUORUM": 2, "ALL": 3}
for w, r in [("ONE", "ONE"), ("QUORUM", "QUORUM"), ("ALL", "ONE"), ("ONE", "QUORUM")]:
    W, R = level[w], level[r]
    print(f"write {w:6} read {r:6}: consistent={R + W > N}, write tolerates {N - W}, read tolerates {N - R}")
''', notes={5: 'Check :: Overlap between the write set and the read set guarantees the read sees the write.'},
         tryit='Which pair would you choose for a user profile that must show users their own updates, but must stay writable when one node is down?'),
    dict(level='i', tag='Conflicts · last-write-wins', title='How last-write-wins loses updates',
         problem='<p>Two replicas accept updates to the same field during a partition, each with a timestamp. Merge with last-write-wins and list the updates that were silently discarded.</p>',
         inp='A: address=Baner at 10:05 · B: address=Wakad at 10:03, phone=98xx at 10:04',
         approach=['Collect every update with its key and timestamp.',
                   'For each key keep only the update with the latest timestamp.',
                   'Updates not kept were lost.'],
         code='''updates = [("A", "address", "Baner", "10:05"), ("B", "address", "Wakad", "10:03"), ("B", "phone", "98xx", "10:04")]
winner = {}
for node, key, value, ts in updates:
    if key not in winner or ts > winner[key][2]:
        winner[key] = (node, value, ts)
lost = [u for u in updates if winner[u[1]][:2] != (u[0], u[2])]
print("merged:", {k: v[1] for k, v in winner.items()})
print("lost  :", lost)
''', notes={4: 'LWW :: The later timestamp wins, regardless of which change the user meant.'},
         tryit='Replica B\'s clock is 3 minutes fast. Add 3 minutes to its timestamps. Which address wins now? This is why LWW depends on clock accuracy.'),
    dict(level='a', tag='CRDTs · counters', title='A PN-counter: likes and unlikes that merge correctly',
         problem='<p>Users can like and unlike. Each replica keeps separate increment (P) and decrement (N) counts per replica. Merge two diverged replicas and compute the true like count.</p>',
         inp='replica A: +4 −1 · replica B: +6 −2 · both start from the same state',
         approach=['Keep P and N dictionaries with one slot per replica.',
                   'Merge by taking the maximum of each slot from both copies.',
                   'Value = sum(P) − sum(N).'],
         code='''copy_a = {"P": {"A": 4, "B": 0}, "N": {"A": 1, "B": 0}}
copy_b = {"P": {"A": 0, "B": 6}, "N": {"A": 0, "B": 2}}
merged = {}
for part in ["P", "N"]:
    merged[part] = {r: max(copy_a[part][r], copy_b[part][r]) for r in ["A", "B"]}
value = sum(merged["P"].values()) - sum(merged["N"].values())
print("merged:", merged)
print("likes:", value)
''', notes={5: 'Merge :: Per-slot maximum works in any order and can be repeated safely.', 6: 'Value :: Total likes minus total unlikes.'},
         tryit='Merge <code>copy_b</code> with the already-merged result again. Does the value change? (It shouldn\'t: CRDT merges are idempotent.)'),
]

QUIZ = [
    dict(q='The CAP theorem says that during a network partition, a distributed system must choose between:', options=['Speed and cost', 'Consistency and availability', 'Replication and partitioning', 'SQL and NoSQL'], answer=1,
         why='Partitions can\'t be avoided, so the real choice when one happens is between <b>consistency</b> and <b>availability</b>.'),
    dict(q='What does “C” mean in CAP?', options=['Compression', 'Every read sees the most recent write (linearizability)', 'Cluster size', 'Cost'], answer=1,
         why='CAP consistency is strong consistency: the system behaves as if there were one up-to-date copy.'),
    dict(q='Why is “CA” not a real option for a distributed system?', options=['It is too expensive', 'Network partitions can always happen, so partition tolerance can\'t be given up', 'CA systems are illegal', 'CA requires Kafka'], answer=1,
         why='Any system spread over a network will sometimes lose messages; “CA” really means “not distributed”.'),
    dict(q='A social app shows slightly different like counts to different users for a few seconds. This is:', options=['Strong consistency', 'Eventual consistency', 'A security bug', 'Linearizability'], answer=1,
         why='Copies converge after updates settle: <b>eventual consistency</b>, an AP choice that is fine for likes.'),
    dict(q='Which system is typically CP?', options=['A CDN cache', 'DNS', 'etcd / ZooKeeper', 'A like counter'], answer=2,
         why='Coordination stores like etcd and ZooKeeper use consensus and refuse service on the minority side to stay correct.'),
    dict(q='PACELC adds which trade-off to CAP?', options=['Security vs speed', 'When there is no partition, latency vs consistency', 'Price vs performance', 'Partitioning vs replication'], answer=1,
         why='Else (no partition): choosing strong consistency still costs latency, because writes must coordinate.'),
    dict(q='With replication factor 3, which Cassandra setting gives strongly consistent reads?', options=['Write ONE, read ONE', 'Write QUORUM, read QUORUM', 'Write ONE, read ONE twice', 'Write ANY, read ONE'], answer=1,
         why='QUORUM is 2 of 3: R + W = 4 &gt; 3, so every read overlaps the latest write.'),
    dict(q='Why can last-write-wins be dangerous?', options=['It is too slow', 'It silently discards concurrent updates and depends on clock accuracy', 'It needs a leader', 'It encrypts data'], answer=1,
         why='When two updates are concurrent, LWW keeps one and drops the other; skewed clocks can even make the older one win. CRDTs or version vectors avoid this.'),
]

REVISION = [
    '<b>CAP</b>: with a network <b>partition</b>, choose <b>consistency</b> (refuse some requests) or <b>availability</b> (answer, maybe stale). P is unavoidable.',
    'CP examples: ZooKeeper, etcd, HBase, Spanner, majority-configured MongoDB. AP examples: Cassandra/Dynamo at low levels, DNS, caches.',
    '“Pick any two” is a myth; many databases are <b>tunable</b> per query (R + W &gt; N for strong reads).',
    '<b>PACELC</b>: else (no partition) choose latency or consistency.',
    'Ladder: <b>linearizable</b> → sequential → causal → read-your-writes/monotonic → <b>eventual</b>.',
    'AP conflicts: last-write-wins (loses data), version vectors, <b>CRDTs</b> (counters, OR-Sets merge safely).',
    'Choose per data: balances, seats and stock strong; likes, views and carts eventual.',
]
FAQ = [
    ('State and explain the CAP theorem.', 'The CAP theorem states that a distributed data store cannot simultaneously provide consistency (every read sees the most recent write), availability (every request to a non-failing node gets a response) and partition tolerance (the system keeps working when network messages between nodes are lost). Because partitions cannot be prevented in a distributed system, the practical meaning is that during a partition the system must sacrifice either consistency (CP: refuse some requests) or availability (AP: answer but possibly return stale or conflicting data).'),
    ('Give examples of CP and AP systems.', 'CP: ZooKeeper, etcd and Consul (consensus-based coordination), HBase, Google Spanner, MongoDB with majority read and write concerns, relational databases with synchronous replication. AP: Cassandra and ScyllaDB at low consistency levels, Dynamo-style key-value stores, Riak, CouchDB, DNS and CDN caches. Many systems are tunable, so the classification depends on configuration.'),
    ('What is eventual consistency?', 'A consistency model in which, if no new updates are made, all replicas eventually converge to the same value. Reads may temporarily return stale data. It allows high availability and low latency and suits data like likes, views and recommendations, but needs rules for resolving concurrent updates.'),
    ('What is PACELC?', 'An extension of CAP by Daniel Abadi: if there is a Partition (P), a system trades Availability (A) against Consistency (C); Else (E), when the network is healthy, it trades Latency (L) against Consistency (C). It highlights that strong consistency has a latency cost even without failures, especially with replicas far apart.'),
    ('What are CRDTs?', 'Conflict-free replicated data types are data structures (such as grow-only counters, PN-counters, grow-only sets and observed-remove sets) designed so that replicas can be updated independently and merged in any order, any number of times, always converging to the same correct result without coordination. They make AP designs safe for counters, sets and collaborative editing.'),
]

PRACTICE_INTRO = 'Consistency and quorum exercises. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Majority side', stmt='Three replicas split into sides of size 1 and 2. Print which side may accept writes in a CP system.', inp='sides [1, 2]',
         code='''sides = {"left": 1, "right": 2}
majority = 3 // 2 + 1
print([s for s, n in sides.items() if n >= majority])
''', explain='Only a side with a majority of all replicas may decide.'),
    dict(level='easy', title='Consistent read?', stmt='N = 3, W = 1, R = 2. Print whether reads always see the latest write.', inp='3, 1, 2',
         code='''N, W, R = 3, 1, 2
print(R + W > N)
''', explain='1 + 2 = 3 is not greater than 3, so a read could miss the write.'),
    dict(level='easy', title='Classify data', stmt='Print “strong” for money and seats, “eventual” for everything else.', inp='balance, likes, seat, views',
         code='''for item in ["balance", "likes", "seat", "views"]:
    print(item, "->", "strong" if item in ("balance", "seat") else "eventual")
''', explain='Consistency is chosen per kind of data.'),
    dict(level='medium', title='Converged?', stmt='Given replica values after updates stop, print whether the system has converged.', inp='{A: 1008, B: 1008, C: 1005}',
         code='''values = {"A": 1008, "B": 1008, "C": 1005}
print("converged" if len(set(values.values())) == 1 else "not yet")
''', explain='Eventual consistency promises convergence only after updates stop and replication catches up.'),
    dict(level='medium', title='G-counter merge', stmt='Merge two G-counters by taking the maximum per slot and print the total.', inp='a {A:5, B:2}, b {A:3, B:7}',
         code='''a, b = {"A": 5, "B": 2}, {"A": 3, "B": 7}
merged = {k: max(a[k], b[k]) for k in a}
print(merged, sum(merged.values()))
''', explain='Each slot only grows, so the maximum is always the most recent count for that replica.'),
    dict(level='advanced', title='Monotonic reads', stmt='A user\'s successive reads return these versions. Print whether any read went backwards.', inp='[12, 14, 13, 15]',
         code='''versions = [12, 14, 13, 15]
backwards = [(a, b) for a, b in zip(versions, versions[1:]) if b < a]
print("went backwards at:", backwards if backwards else "never")
''', explain='Monotonic-read consistency forbids this; pinning a user to one replica (or tracking versions) prevents it.'),
    dict(level='advanced', title='Latency of a quorum write', stmt='Replica round-trip times from the coordinator are given. Print the latency of writes with W = 1, 2 and 3 (the time until W replicas have confirmed).', inp='[2, 45, 110] ms',
         code='''rtts = sorted([2, 45, 110])
for W in [1, 2, 3]:
    print(f"W={W}: {rtts[W - 1]} ms")
''', explain='The write waits for the W-th fastest replica: stronger guarantees cost latency (PACELC).'),
    dict(level='business', title='Cost of eventual vs strong', stmt='A strongly consistent write takes 60 ms, an eventual one 3 ms. A feature makes 2 lakh writes per minute and each request holds a thread for the write time. Print the average busy threads for each (Little\'s law).', inp='2 lakh/min, 60 ms vs 3 ms',
         code='''rate_per_s = 2_00_000 / 60
for name, ms in [("strong", 60), ("eventual", 3)]:
    print(f"{name:8}: about {rate_per_s * ms / 1000:.0f} busy threads")
''', explain='Consistency choices change capacity needs too: 20 times more concurrency for the strong version here.'),
    dict(level='business', title='Oversell risk', stmt='A flash sale of 500 phones uses an eventually consistent stock counter with 2 seconds of lag at 300 orders per second. Roughly how many phones could be oversold?', inp='500 stock, 2 s lag, 300/s',
         code='''lag, rate = 2, 300
print("orders that could see stale stock near the end:", lag * rate)
print("so up to ~", lag * rate, "phones could be oversold -> use strong consistency at checkout")
''', explain='For limited stock, a stale view is fine for browsing, but the final reservation must be strongly consistent.'),
]

SCN_INTRO = 'Consistency questions from interviews and real designs. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
