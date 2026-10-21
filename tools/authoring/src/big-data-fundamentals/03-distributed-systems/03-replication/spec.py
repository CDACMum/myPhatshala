import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='03-distributed-systems', lesson='03-replication', n='3.3',
    module_label='Module 3 · Distributed Systems Concepts',
    title='Replication: leaders, followers and copies',
    desc='Replication explained: single-leader, multi-leader and leaderless replication, synchronous vs asynchronous vs semi-synchronous, replication lag and read-your-writes, failover, RPO and RTO, Kafka acks and in-sync replicas, quorums, split brain, fencing tokens and consensus (Raft). Real-time animations and a replication simulator for your PC.',
    og_desc='A database dies at 2 am and the app is back in 28 seconds. Learn how replication works, when copies lose data, and how split brain is prevented.',
    minutes=30, level='Beginner → Advanced',
    lead='Big data systems keep several copies of everything, so that a dead disk at 2 am means seconds of downtime instead of lost data. In this lesson you learn how <b>leaders</b> and <b>followers</b> stay in sync, why “acknowledged” doesn\'t always mean “safe”, what Kafka\'s <code>acks=all</code> guarantees, and how majorities and fencing tokens stop two leaders from taking over at once.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Replication simulator on your PC'],
)

RUN = dict(
    heading='A leader and two followers',
    intro='<p>Writes go to the leader\'s log. Each follower copies the log after its own delay. The program shows what each copy contains at a moment in time, which reads would be stale, and what a failover would lose. Then try the challenges: synchronous writes, choosing the new leader, quorums, Kafka acks and fencing tokens.</p>',
    code='''writes = [(0, "O1"), (2, "O2"), (4, "O3"), (6, "O4")]   # (time, order)
lag = {"F1": 1, "F2": 4}                                 # seconds behind the leader
now = 7

leader = [o for t, o in writes if t <= now]
followers = {f: [o for t, o in writes if t + d <= now] for f, d in lag.items()}

print("leader:", leader)
for f, data in followers.items():
    stale = len(leader) - len(data)
    print(f"{f}: {data}  ({stale} behind)")

# The leader crashes now: promote the follower with the most data
new_leader = max(followers, key=lambda f: len(followers[f]))
lost = [o for o in leader if o not in followers[new_leader]]
print("promote", new_leader, "| acknowledged but lost:", lost)
''',
    anno=[
        ('lag = {"F1": 1, "F2": 4}                                 # seconds behind the leader', 'Asynchronous followers apply changes a little later. Each has its own lag.'),
        ('followers = {f: [o for t, o in writes if t + d <= now] for f, d in lag.items()}', 'A follower has a write only if the write\'s time plus its lag has passed.'),
        ('new_leader = max(followers, key=lambda f: len(followers[f]))', 'On failover, the most up-to-date follower is promoted, losing as little as possible.'),
    ],
    tasks=[
        dict(label='1 · Lag and failover', hint='Press <b>Run</b>. Change <code>now</code> to 10: does anything get lost? Then make F1\'s lag 3.', code=None),
        dict(label='2 · Synchronous write', hint='With synchronous replication the write finishes only when every follower confirms, so its latency is the slowest one. Compare with waiting for just one follower (semi-sync).',
             code='''follower_ms = {"F1": 3, "F2": 4, "F3": 40}     # time for each follower to confirm
leader_ms = 2
print("async     :", leader_ms, "ms")
print("semi-sync :", leader_ms + min(follower_ms.values()), "ms (wait for the fastest)")
print("sync (all):", leader_ms + max(follower_ms.values()), "ms (wait for the slowest)")
'''),
        dict(label='3 · Read-your-writes', hint='After a user writes, route that user\'s reads to the leader for 5 seconds; others read from a follower. Change the time of Riya\'s read.',
             code='''last_write = {"riya": 100}            # time of each user's last write
def route(user, now):
    if user in last_write and now - last_write[user] < 5:
        return "leader"
    return "follower"
for user, t in [("riya", 101), ("riya", 107), ("kabir", 101)]:
    print(user, "at", t, "->", route(user, t))
'''),
        dict(label='4 · Quorums', hint='With N replicas, a read of R and a write of W always overlap if R + W > N. List all safe (W, R) pairs for N = 5.',
             code='''N = 3
for W in range(1, N + 1):
    for R in range(1, N + 1):
        print(f"W={W} R={R}:", "safe" if R + W > N else "may be stale")
'''),
        dict(label='5 · Kafka acks (advanced)', hint='Simulate a leader crash right after a write. Which acks settings lose an acknowledged message? Change <code>copied_before_crash</code> to 2.',
             code='''replicas = 3
copied_before_crash = 0        # followers that had the message when the leader crashed
for acks in ["0", "1", "all"]:
    acknowledged = acks in ("0", "1") or copied_before_crash >= replicas - 1
    survives = copied_before_crash >= 1
    lost = acknowledged and not survives
    print(f"acks={acks:3}: producer told OK={acknowledged}, message survives={survives}, LOST={lost}")
'''),
        dict(label='6 · Fencing tokens (advanced)', hint='Storage accepts a write only if its epoch is at least the highest epoch seen. The old leader (epoch 1) tries to write after the new leader (epoch 2). Add a write from epoch 3.',
             code='''highest = 0
store = []
for leader, epoch, value in [("A", 1, "x=1"), ("B", 2, "x=2"), ("A", 1, "x=99")]:
    if epoch >= highest:
        highest = epoch
        store.append(value)
        print(f"{leader} (epoch {epoch}) write {value}: accepted")
    else:
        print(f"{leader} (epoch {epoch}) write {value}: REJECTED, stale leader")
print("final:", store)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: async vs semi-sync replication',
    intro='<p>This program simulates a leader and two followers on a clock. A client writes every two ticks; followers copy after a delay. It reads from a lagging follower, crashes the leader, promotes the best follower and lists acknowledged writes that were lost. Then it repeats with semi-synchronous replication and checks quorum settings. Save it as <code>replication_sim.py</code> and run it.</p>',
    items=[
        dict(title='Replication, failover and quorums', file='replication_sim.py',
             cmd=open(os.path.join(HERE, 'replication_sim.py')).read() + '\n# In a terminal:  python replication_sim.py',
             output=open(os.path.join(HERE, 'replication_sim.out')).read(),
             note='Recorded from a real run with Python 3.13; the simulation is deterministic, so you get the same output. Change <code>lag</code> or <code>crash_at</code> and see how many acknowledged writes are lost with async replication, and that semi-sync loses none as long as the follower it waited for survives.'),
    ],
)

TRACE = dict(
    heading='Followers applying the log, one line at a time',
    intro='<p>The leader\'s log has three entries. Follower F2 already has the first one. Watch it apply only the entries it is missing, in order.</p>',
    code='''leader_log = ["O1", "O2", "O3"]
f2 = ["O1"]
position = len(f2)
while position < len(leader_log):
    f2.append(leader_log[position])
    position = position + 1
print(f2 == leader_log, f2)
''',
    notes={3: 'Position :: Where F2 must continue: the length of what it already has.',
           5: 'Apply :: Entries are applied strictly in log order.'},
)

WORKED_INTRO = 'Four replication problems, from counting copies to choosing quorum settings. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Capacity · copies', title='How much disk do copies need?',
         problem='<p>A Kafka cluster stores 20 TB of messages per week with replication factor 3, keeping 1 week. HDFS stores 50 TB with replication 3. How much raw disk does each need?</p>',
         inp='Kafka 20 TB × 3, HDFS 50 TB × 3',
         approach=['Raw disk = data × replication factor.',
                   'Add both systems for the total.'],
         code='''systems = {"Kafka": (20, 3), "HDFS": (50, 3)}
total = 0
for name, (tb, rf) in systems.items():
    raw = tb * rf
    total = total + raw
    print(f"{name}: {tb} TB of data x {rf} copies = {raw} TB of disk")
print("Total raw disk:", total, "TB")
''', notes={4: 'Copies :: Every byte is stored replication-factor times.'},
         tryit='Move the HDFS data to erasure coding 6+3 (1.5×). How much disk is saved?'),
    dict(level='i', tag='Database · lag monitoring', title='Which replicas are safe to read from?',
         problem='<p>Each read replica reports its lag in seconds. Reports can tolerate 30 s of lag; the checkout page tolerates 1 s. Print which replicas each workload may use.</p>',
         inp='r1: 0.4 s, r2: 12 s, r3: 75 s',
         approach=['Store each replica\'s lag.',
                   'For each workload, keep replicas with lag below its limit.',
                   'If none qualifies, fall back to the primary.'],
         code='''lag = {"r1": 0.4, "r2": 12, "r3": 75}
limits = {"checkout": 1, "reports": 30}
for workload, limit in limits.items():
    ok = [r for r, l in lag.items() if l <= limit]
    print(f"{workload:8}: {ok if ok else ['primary']}")
''', notes={4: 'Filter :: Only replicas fresh enough for this workload.'},
         tryit='r1 suddenly lags 5 s during a spike. Which replicas can checkout use now? What should the router do?'),
    dict(level='i', tag='Reliability · RPO', title='How much data can async replication lose?',
         problem='<p>Orders arrive at 3,000 per second. The async replica usually lags 0.5 s, but up to 4 s during peaks. How many orders could be lost if the primary died at a normal moment, and at a peak?</p>',
         inp='3,000 orders/s, lag 0.5 s normal, 4 s peak',
         approach=['Orders at risk = arrival rate × lag.',
                   'Compute for both lags.',
                   'Compare with the business\'s acceptable loss (RPO).'],
         code='''rate = 3000
for label, lag_s in [("normal", 0.5), ("peak", 4)]:
    at_risk = int(rate * lag_s)
    print(f"{label:6}: up to {at_risk} acknowledged orders could be lost")
print("RPO target: 0 orders -> needs synchronous or semi-sync replication")
''', notes={3: 'Risk :: Everything written during the lag window exists only on the primary.'},
         tryit='The business accepts losing at most 500 orders. What is the maximum lag you can allow at 3,000 orders/s?'),
    dict(level='a', tag='Distributed DB · quorums', title='Choose quorum settings for each workload',
         problem='<p>With N = 3 replicas, list all (W, R) combinations, mark which are consistent (R + W > N), and pick the fastest consistent setting for a write-heavy workload (smallest W) and for a read-heavy one (smallest R).</p>',
         inp='N = 3',
         approach=['Enumerate W and R from 1 to N.',
                   'Keep combinations with R + W > N.',
                   'Write-heavy: smallest W, then smallest R. Read-heavy: smallest R, then smallest W.'],
         code='''N = 3
safe = [(w, r) for w in range(1, N + 1) for r in range(1, N + 1) if r + w > N]
print("consistent settings:", safe)
write_heavy = min(safe, key=lambda p: (p[0], p[1]))
read_heavy = min(safe, key=lambda p: (p[1], p[0]))
print("write-heavy pick (W, R):", write_heavy)
print("read-heavy pick  (W, R):", read_heavy)
''', notes={2: 'Safe :: Read and write sets must share at least one replica.', 4: 'Pick :: Fewest write acknowledgements, then fewest reads.'},
         tryit='Try N = 5. Which setting would you choose to survive two replicas being down for both reads and writes?'),
]

QUIZ = [
    dict(q='What is the main purpose of replication?', options=['To split data into smaller parts', 'To keep copies of data on several nodes for availability, durability and read scaling', 'To compress data', 'To encrypt data'], answer=1,
         why='Replication copies data; partitioning splits it. Most systems do both.'),
    dict(q='In single-leader replication, where do writes go?', options=['To any replica', 'Only to the leader', 'Only to followers', 'To a backup tape'], answer=1,
         why='The leader accepts writes and sends changes to followers in order.'),
    dict(q='Which statement about asynchronous replication is true?', options=['Writes wait for every follower', 'The leader acknowledges immediately, so a crash can lose the latest writes', 'It never has replication lag', 'It needs no leader'], answer=1,
         why='Async is fast but followers lag; writes acknowledged just before a crash may never reach a follower.'),
    dict(q='A user updates their address but sees the old one on refresh. Reads go to async replicas. This is a violation of:', options=['Read-your-writes consistency', 'Partition tolerance', 'Durability', 'Normalisation'], answer=0,
         why='Route a user\'s reads to the leader (or an up-to-date replica) for a while after they write.'),
    dict(q='What does Kafka\'s acks=all guarantee?', options=['The message is written to disk on the producer', 'The leader confirms only after all in-sync replicas have the message', 'Consumers have read the message', 'The message is encrypted'], answer=1,
         why='With min.insync.replicas ≥ 2, an acknowledged message exists on at least two brokers.'),
    dict(q='Why do clusters often have an odd number of nodes, such as 3 or 5?', options=['Odd numbers are faster', 'So a majority can always be formed and a network split leaves only one side with a quorum', 'Licences are cheaper', 'Even numbers can\'t replicate'], answer=1,
         why='Majority quorums prevent two leaders; with 3 nodes, only the side with 2 can elect one.'),
    dict(q='Two nodes both believe they are leader after a network partition. This is called:', options=['Data skew', 'Split brain', 'Replication lag', 'Hot partition'], answer=1,
         why='<b>Split brain</b> lets data diverge. Prevent it with majority quorums and fencing tokens.'),
    dict(q='Why is replication not a substitute for backups?', options=['Replicas are always slower', 'Mistakes like accidental deletes are copied to every replica too', 'Replicas can\'t be read', 'Backups are required by Kafka'], answer=1,
         why='Replication protects against hardware failure; backups protect against mistakes, bugs and corruption.'),
]

REVISION = [
    'Replication = copies on several nodes → availability, durability, read scaling, lower latency.',
    'Architectures: <b>single-leader</b> (most common), <b>multi-leader</b> (multi-region), <b>leaderless</b> (quorums, R + W &gt; N).',
    '<b>Sync</b> (safe, slower) vs <b>async</b> (fast, can lose last writes) vs <b>semi-sync</b> (wait for one).',
    '<b>Replication lag</b> → stale reads; fix with read-your-writes routing.',
    '<b>Failover</b>: detect, promote most up-to-date follower, redirect, old leader rejoins as follower. RPO = data loss, RTO = downtime.',
    'Kafka: RF 3, <code>min.insync.replicas=2</code>, <code>acks=all</code>, no unclean leader election.',
    '<b>Split brain</b> prevented by majority quorums, fencing tokens/epochs and consensus (Raft, ZooKeeper). Replication ≠ backup.',
]
FAQ = [
    ('What is replication? Explain its types.', 'Replication keeps copies of the same data on multiple nodes for fault tolerance, availability, durability and read scalability. In single-leader replication one node accepts writes and streams changes to followers (PostgreSQL, MySQL, Kafka partitions). In multi-leader replication several nodes accept writes and exchange changes, useful across regions but requiring conflict resolution. In leaderless replication clients write to and read from several replicas and use quorums (R + W > N) for consistency, as in Cassandra and DynamoDB-style systems.'),
    ('Compare synchronous and asynchronous replication.', 'In synchronous replication the leader acknowledges a write only after replicas confirm it, so no acknowledged data is lost if the leader fails, but write latency is higher and a slow or unavailable replica can block writes. In asynchronous replication the leader acknowledges immediately and replicas apply changes later, giving low latency but replication lag and possible loss of recent writes on failover. Semi-synchronous replication waits for at least one replica, balancing the two.'),
    ('What is replication lag and what problems does it cause?', 'Replication lag is the delay between a write on the leader and its application on a follower. It causes stale reads, users not seeing their own updates (read-your-writes violations), data appearing to go backwards when reads hit different replicas (monotonic-read violations), and data loss on failover with asynchronous replication.'),
    ('What is split brain and how is it prevented?', 'Split brain occurs when a network partition leads two nodes to act as leader simultaneously, both accepting writes so the data diverges. It is prevented by requiring a majority quorum to elect and keep a leader, by fencing tokens or epoch numbers that make storage reject writes from an old leader, and by using consensus algorithms such as Raft or Paxos (as in etcd, ZooKeeper and Kafka KRaft).'),
    ('How does Kafka replication work?', 'Each partition has one leader broker and follower brokers that copy its log; followers that are fully caught up form the in-sync replica set (ISR). Producers choose acks=0 (no confirmation), acks=1 (leader only) or acks=all (all in-sync replicas). With replication factor 3, min.insync.replicas=2 and acks=all, an acknowledged message is stored on at least two brokers, and if the leader fails an in-sync follower takes over without losing it.'),
]

PRACTICE_INTRO = 'Replication exercises, from lag to quorums. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Raw storage', stmt='Print the raw storage for 12 TB of data with replication factor 3.', inp='12 TB, RF 3',
         code='''print(12 * 3, "TB")
''', explain='Each copy needs the full space.'),
    dict(level='easy', title='Replica lag', stmt='The leader is at log position 10,500 and a follower at 10,320. Print the lag in entries.', inp='10500, 10320',
         code='''print(10500 - 10320, "entries behind")
''', explain='Lag can be measured in log positions as well as seconds.'),
    dict(level='easy', title='Majority size', stmt='Print the majority (quorum) size for clusters of 3, 4, 5 and 7 nodes.', inp='3, 4, 5, 7',
         code='''for n in [3, 4, 5, 7]:
    print(n, "nodes -> majority", n // 2 + 1)
''', explain='A 4-node cluster needs 3 for a majority, so it tolerates only 1 failure, like a 3-node cluster.'),
    dict(level='medium', title='Failures tolerated', stmt='Print how many node failures a majority-quorum cluster tolerates for 3, 5 and 7 nodes.', inp='3, 5, 7',
         code='''for n in [3, 5, 7]:
    print(n, "nodes tolerate", (n - 1) // 2, "failures")
''', explain='A cluster keeps working while a majority is alive.'),
    dict(level='medium', title='Promote the best follower', stmt='Given each follower\'s last log position, print the one to promote.', inp='F1: 880, F2: 905, F3: 870',
         code='''pos = {"F1": 880, "F2": 905, "F3": 870}
print(max(pos, key=pos.get))
''', explain='The most up-to-date follower loses the least data.'),
    dict(level='advanced', title='Writes at risk', stmt='Orders arrive at 1,200/s. Async lag samples are given. Print the maximum number of orders at risk.', inp='lags [0.2, 0.4, 1.8, 0.3]',
         code='''lags = [0.2, 0.4, 1.8, 0.3]
print(int(1200 * max(lags)), "orders at risk in the worst case")
''', explain='Plan for the worst lag, not the average.'),
    dict(level='advanced', title='Stale-read probability', stmt='A read goes to one of 3 replicas at random; at that moment 1 replica has the latest write. With R reads combined (taking the newest value), what is the chance of a stale result for R = 1, 2, 3?', inp='3 replicas, 1 up to date',
         code='''from math import comb
N, fresh = 3, 1
for R in [1, 2, 3]:
    stale = comb(N - fresh, R) / comb(N, R)
    print(f"R={R}: chance of stale result {stale:.0%}")
''', explain='Reading more replicas lowers the chance of missing the newest value; with R + W > N it becomes zero.'),
    dict(level='business', title='Cost of a standby', stmt='A database server costs Rs 2.5 lakh a month. A synchronous standby doubles that. One hour of downtime costs the business Rs 40 lakh, and without a standby a failure causes 4 hours of downtime about once a year. Is the standby worth it?', inp='Rs 2.5 lakh/month, Rs 40 lakh/hour, 4 h/year',
         code='''standby_per_year = 2.5 * 12
downtime_cost = 40 * 4
print(f"standby: Rs {standby_per_year} lakh/year vs expected downtime: Rs {downtime_cost} lakh/year")
print("worth it" if downtime_cost > standby_per_year else "not worth it")
''', explain='Availability decisions are business decisions: compare the cost of copies with the cost of being down.'),
    dict(level='business', title='Cross-region RPO', stmt='A bank replicates asynchronously to a DR region with an average lag of 2 s and 800 transactions/s. The regulator expects RPO under 5 minutes. Print the transactions at risk and whether the RPO is met.', inp='2 s lag, 800/s, RPO 300 s',
         code='''lag, rate, rpo = 2, 800, 300
print("transactions at risk:", lag * rate)
print("RPO met" if lag <= rpo else "RPO NOT met")
''', explain='Async cross-region replication usually meets minute-level RPOs, while synchronous replication across distant regions would slow every transaction.'),
]

SCN_INTRO = 'Replication questions from real incidents and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
