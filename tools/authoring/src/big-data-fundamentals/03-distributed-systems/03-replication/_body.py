import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = t(80, 24, '02:13 am', 12, 'red', bold=True, mono=True)
sc += label_box(14, 40, 130, 70, ['Leader DB', '✗ disk failure'], 'red', 10)
sc += arrow(150, 75, 196, 75, 'ink3', 2) + t(173, 64, 'failover', 8.2, 'ink3')
sc += label_box(204, 40, 130, 70, ['Follower 1', 'promoted to leader'], 'green', 10)
sc += label_box(350, 40, 130, 70, ['Follower 2', 'now follows F1'], 'blue', 10)
sc += box(496, 30, 130, 90, 'card') + t(561, 52, 'Orders app', 9.6, bold=True) + t(561, 72, 'down for 28 s', 9, 'red', bold=True) + t(561, 92, '1 order to re-check', 8.6, 'ink2')
scene_svg = scene('At 2:13 am the leader database fails, a follower is promoted, and the orders app is down for 28 seconds with one order to re-check.', sc,
                  'Because copies existed, a dead disk meant <tspan font-weight="700" class="s-acc">28 seconds of downtime, not a lost business</tspan>.')

story = f'''  <div class="story">
    <p class="narration">On the internship’s on-call channel at 2:13 am an alert fires: <i>“orders-db primary down”</i>. Twenty-eight seconds later: <i>“failover complete, replica-1 promoted”</i>. In the morning Kabir reads the incident note. One line worries him: <i>“1 order acknowledged in the last second before the crash needs manual reconciliation.”</i></p>

{scene_svg}

K> Sir, the database died and the app came back in 28 seconds. How? And how can an order be “acknowledged” and then go missing?
A> Because the data was <b>replicated</b>: the same data was kept on three machines. One, the <b>leader</b>, takes all writes; the two <b>followers</b> copy everything it does. When the leader died, a follower was promoted.
R> So why was one order missing?
A> Because the followers copy <i>slightly later</i>, a fraction of a second behind. The leader had said “OK” to that order before any follower had copied it. That is <b>asynchronous</b> replication: fast, but a crash can lose the last moment of writes.
K> Then why not wait for the followers every time?
A> That’s <b>synchronous</b> replication: safer, but every write waits for the slowest copy. Today you’ll see this trade-off, watch a failover step by step, learn what Kafka’s <code>acks=all</code> really means, and see the scariest failure of all: two leaders at once, called <b>split brain</b>.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Replication at three levels
L1> Photocopies of the class notes
      <ul>
        <li><b>Replication</b> is keeping copies of the same data on several machines, like photocopying the topper’s notes for three friends. If one copy is lost, the others still have it.</li>
        <li><b>Why:</b> survive failures (<b>availability</b>), never lose data (<b>durability</b>), let more people read at once (<b>read scaling</b>), and keep copies close to users (<b>lower latency</b>).</li>
        <li><b>Leader and followers:</b> one person writes the notes (the leader); the others copy from them (followers). Everyone asks the leader to change something.</li>
        <li><b>Not a backup:</b> if you delete a page by mistake, the deletion is copied too. Replication protects against machines failing, backups against mistakes.</li>
      </ul>
L2> Sync vs async, lag and read replicas
      <ul>
        <li><b>Synchronous:</b> the leader confirms a write only after followers have it. No loss on leader failure, but writes are slower and a slow follower slows everyone.</li>
        <li><b>Asynchronous:</b> the leader confirms immediately and followers catch up later. Fast, but the last moments of writes can be lost in a crash, and followers lag behind.</li>
        <li><b>Semi-synchronous:</b> wait for <i>one</i> follower, not all. A common middle ground.</li>
        <li><b>Replication lag:</b> a read from a follower may show old data. Problems this causes: a user doesn’t see their own update (<b>read-your-writes</b>), or sees data jump backwards when reads hit different replicas (<b>monotonic reads</b>).</li>
        <li><b>Replication factor:</b> how many copies. HDFS blocks: 3. Kafka partitions: commonly 3, with <code>min.insync.replicas=2</code> and producers using <code>acks=all</code>.</li>
      </ul>
L3> Failover, split brain and consensus
      <ul>
        <li><b>Failover:</b> detect that the leader is dead (heartbeat timeouts), choose the most up-to-date follower, promote it, and redirect clients. Too short a timeout causes needless failovers; too long means longer outages.</li>
        <li><b>RPO and RTO:</b> Recovery Point Objective = how much recent data you can afford to lose (async replication: seconds); Recovery Time Objective = how long you can be down (automatic failover: tens of seconds).</li>
        <li><b>Split brain:</b> a network partition makes the old leader and a newly elected one both accept writes. Prevent it with <b>majority quorums</b> (only the side with more than half the nodes can elect a leader) and <b>fencing tokens</b> (increasing epoch numbers; storage rejects writes from older epochs).</li>
        <li><b>Consensus:</b> algorithms like Raft and Paxos (used in etcd, ZooKeeper and Kafka’s KRaft) let nodes agree on one leader and one order of writes despite failures.</li>
        <li><b>Multi-leader and leaderless:</b> several nodes accept writes (multi-region apps, Cassandra/Dynamo-style quorums with R + W &gt; N). Concurrent writes conflict and must be resolved: last-write-wins (can silently drop data), version vectors, or CRDTs that merge automatically.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Replication</b> is maintaining copies of the same data on multiple nodes to provide <b>fault tolerance</b>, <b>high availability</b>, <b>durability</b>, <b>read scalability</b> and lower latency. In <b>leader-based</b> (primary–replica) replication one node accepts writes and streams changes to followers; replication can be <b>synchronous</b> (the write is acknowledged after replicas confirm), <b>asynchronous</b> (acknowledged immediately, replicas apply later) or <b>semi-synchronous</b>. <b>Multi-leader</b> and <b>leaderless</b> replication allow writes at several nodes and must resolve conflicts. The number of copies is the <b>replication factor</b>.',
    'Replication means keeping the same data on several machines. Usually one machine (the leader) takes the changes and the others (followers) copy them. If the leader breaks, a follower takes over. Copies can be updated straight away (safe but slower) or a moment later (fast but a crash can lose the last few changes).') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Leader / primary', 'The node that accepts writes and sends changes to the others.'),
    ('Follower / replica', 'A node that keeps a copy by applying the leader’s changes.'),
    ('Replication log', 'The ordered list of changes (for example a write-ahead log) that followers replay.'),
    ('Replication lag', 'How far behind a follower is, in seconds or in log entries.'),
    ('Failover', 'Promoting a follower to leader when the leader fails.'),
    ('Split brain', 'Two nodes both acting as leader at the same time.'),
    ('Quorum', 'The minimum number of nodes that must agree for a read or write to count.'),
    ('RPO / RTO', 'Maximum acceptable data loss / downtime after a failure.'),
]) + '''

  <h3>Replication in tools you will use</h3>
''' + facts([
    ('HDFS', 'every block stored 3 times by default, on different racks where possible'),
    ('Kafka', 'each partition has a leader and followers; in-sync replicas (ISR); producers choose acks=0, 1 or all'),
    ('PostgreSQL / MySQL', 'primary with streaming read replicas; sync or async; managed services automate failover'),
    ('Cassandra', 'leaderless; replication factor per keyspace; consistency level chosen per query'),
    ('Cloud object storage', 'copies or erasure-coded pieces across availability zones, handled for you'),
]) + lv + '''
EXAM> Define replication, list its <b>benefits</b> (availability, durability, read scaling, latency), and compare <b>synchronous vs asynchronous</b> in a table (latency, data-loss risk, availability). Name the three architectures (single-leader, multi-leader, leaderless) with one example each, and mention replication lag and failover.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Single-leader', 'One leader takes all writes; followers copy and can serve reads. Simple and consistent ordering. PostgreSQL, MySQL, Kafka partitions, HDFS NameNode HA.', 'Most common'),
    ('Multi-leader', 'Several leaders (often one per region) accept writes and sync with each other. Good for multi-region apps; conflicts must be resolved.', 'Multi-region'),
    ('Leaderless', 'Clients write to several replicas and read from several; quorums (R + W > N) give consistency. Cassandra, DynamoDB-style stores.', 'Quorums'),
]) + '''

  <h3>Synchronous vs asynchronous</h3>
''' + table(['', 'Synchronous', 'Asynchronous', 'Semi-synchronous'], [
    ['<b>Write acknowledged</b>', 'After all chosen replicas confirm', 'Immediately by the leader', 'After at least one replica confirms'],
    ['<b>Write latency</b>', 'Highest (waits for slowest)', 'Lowest', 'Medium'],
    ['<b>Data loss if leader dies</b>', 'None', 'Last moments of writes', 'None if that replica survives'],
    ['<b>Effect of a slow replica</b>', 'Slows every write', 'Only increases lag', 'Tolerates slow extra replicas'],
    ['<b>Typical use</b>', 'Payments within one region', 'Read replicas, cross-region copies', 'Default for many critical databases'],
], minw=620) + '''
TIP> Replication is not a backup. A bad <code>DELETE</code> or a bug that corrupts rows is replicated to every copy within seconds. Keep point-in-time backups or snapshots too, and test restoring them.'''

# ---------------------------------------------------------------- steps
c1 = '''leader, followers = [], {"F1": [], "F2": []}
def write(entry):
    leader.append(entry)            # 1. leader appends to its log
    return "OK"                     # 2. async: acknowledge immediately
print(write("order O1"), write("order O2"))
print("leader:", leader, "| F1:", followers["F1"])'''
c2 = '''leader = ["order O1", "order O2"]
followers = {"F1": [], "F2": []}
for f in followers:                 # 3. followers copy the log in order
    followers[f].extend(leader)
print(followers)'''
c3 = '''leader = ["O1", "O2", "O3", "O4"]
f2 = ["O1", "O2"]                   # F2 is two entries behind
print("read from leader:", len(leader), "orders | read from F2:", len(f2), "orders")
print("lag:", len(leader) - len(f2), "entries")'''
c4 = '''logs = {"F1": ["O1", "O2", "O3"], "F2": ["O1", "O2"]}
acked = ["O1", "O2", "O3", "O4"]    # the leader had said OK to O4
new_leader = max(logs, key=lambda f: len(logs[f]))
print("promote:", new_leader, "| lost:", [o for o in acked if o not in logs[new_leader]])'''
steps = stepper([
    ('The leader writes and acknowledges',
     code('python', 'leader.py', c1, run_code(c1)),
     'Every write goes to the leader, which appends it to its replication log. With asynchronous replication it says “OK” right away, before any follower has the change.'),
    ('Followers replay the log',
     code('python', 'followers.py', c2, run_code(c2)),
     'Followers receive the log entries <b>in the same order</b> and apply them, so they end up with identical data. Order matters: “add ₹100” then “set to ₹0” gives a different result in the other order.'),
    ('Reads from a follower can be stale',
     code('python', 'lag.py', c3, run_code(c3)),
     'Followers are good for spreading read load, but they can be behind. A user who just changed their address might read the old one from a lagging follower.'),
    ('The leader fails: promote the best follower',
     code('python', 'failover.py', c4, run_code(c4)),
     'The most up-to-date follower becomes leader. O4 had been acknowledged by the old leader but never reached a follower, so it is lost: the cost of asynchronous replication.'),
    ('Redirect clients and rejoin',
     '<p>Clients learn the new leader’s address (through a DNS change, a proxy or a coordination service). When the old leader comes back, it must rejoin as a <b>follower</b> and discard writes the new leader never had.</p>',
     'If the old leader came back still believing it was the leader, there would be two leaders: split brain (scenario 3).'),
    ('Choose the safety level per data',
     '<p>Payments: synchronous or semi-synchronous replication within a region. Analytics replicas and cross-region copies: asynchronous. Kafka: <code>acks=all</code> with <code>min.insync.replicas=2</code> for important topics.</p>',
     'Replication is a dial between speed and safety. Choose it per dataset, based on how much loss (RPO) and downtime (RTO) the business can accept.'),
])

# ---------------------------------------------------------------- two-view animation: read-your-writes
def ph(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
addr_old, addr_new = 'Flat 4, Kothrud', 'Flat 12, Baner'
see = [
    ph('Delivery address', box(136, 64, 88, 28, 'card', rx=4) + t(180, 82, addr_new, 7.8) + fill(144, 112, 72, 20, 'acc', rx=10) + t(180, 126, 'SAVE', 8.4, extra=' style="fill:#fff"', bold=True)),
    ph('Delivery address', '<circle cx="180" cy="90" r="16" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M173 90l5 5 9-9" style="stroke:var(--green);stroke-width:2.5;fill:none"/>' + t(180, 128, 'Address saved', 9, 'green', bold=True)),
    ph('Profile', t(180, 80, 'Refreshing…', 9, 'ink2')),
    ph('Profile', t(180, 74, 'Address:', 8.6, 'ink2') + t(180, 92, addr_old, 8.6, 'red', bold=True) + t(180, 124, '“But I just changed it!”', 8, 'ink2')),
    ph('Profile', t(180, 80, 'Refreshing…', 9, 'ink2')),
    ph('Profile', t(180, 74, 'Address:', 8.6, 'ink2') + t(180, 92, addr_new, 8.6, 'green', bold=True) + t(180, 124, 'correct every time', 8, 'green')),
]
def nodes(leader_v, f1_v, f2_v, read=None, write=False, note=''):
    o = label_box(130, 26, 100, 50, ['Leader', leader_v], 'green' if write else 'card', 9)
    o += label_box(20, 120, 120, 50, ['Follower 1', f1_v], 'card', 9) + label_box(220, 120, 120, 50, ['Follower 2', f2_v], 'red' if read == 'F2' else 'card', 9)
    o += arrow(150, 78, 90, 118, 'ink3', 1.4, dash=True) + arrow(210, 78, 270, 118, 'ink3', 1.4, dash=True)
    if read == 'L':
        o += '<rect x="126" y="22" width="108" height="58" rx="8" style="fill:none;stroke:var(--green);stroke-width:2.5"/>'
    return o + t(180, 200, note, 9, 'ink2')
behind = [
    nodes('old', 'old', 'old', write=True, note='The write goes to the leader.'),
    nodes('NEW', 'old', 'old', write=True, note='Leader saves it and says OK (async).'),
    nodes('NEW', 'NEW', 'old', note='Follower 1 has copied it; Follower 2 lags.'),
    nodes('NEW', 'NEW', 'old', read='F2', note='Her read lands on lagging Follower 2: old data.'),
    nodes('NEW', 'NEW', 'old', read='L', note='Fix: her reads go to the leader for a minute.'),
    nodes('NEW', 'NEW', 'NEW', read='L', note='Read-your-writes: she always sees her change.'),
]
see_caps = ['Riya changes her delivery address to Baner and taps Save.',
            'The app confirms: address saved.',
            'She refreshes her profile to double-check.',
            'It shows the old Kothrud address. She panics: did the change fail?',
            'After the fix, she refreshes again.',
            'The new address appears, every time.']
behind_caps = ['The update is sent to the leader database.',
               'The leader stores it and acknowledges immediately. Replication to followers is asynchronous.',
               'Follower 1 has applied the change; Follower 2 is still a second behind.',
               'Her profile read is load-balanced to Follower 2, which hasn’t applied the change yet. She sees stale data.',
               'Fix for <b>read-your-writes</b>: for a short time after a user writes, send that user’s reads to the leader (or to a replica known to be up to date).',
               'Now she always sees her own changes, while other users\' reads still spread across followers.']
two = anim_two('Read-your-writes', 'What Riya sees, and which copy answers', 'Riya changing her address and checking her profile',
               'A leader and two followers with replication lag, and the read-your-writes fix', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: failover
def cl(lead='L', dead=None, lab=None, hl=None, extra=''):
    names = ['Node A', 'Node B', 'Node C']
    o = ''
    for k, n in enumerate(names):
        x = 20 + k * 115
        role = (lab or {}).get(n, 'leader' if n == lead else 'follower')
        tone = 'red' if n == dead else ('green' if role == 'leader' else 'card')
        o += label_box(x, 50, 100, 52, [n, role], tone, 9.4)
    return o + extra
fr1 = [
    cl('Node A') + t(180, 30, 'Normal: A leads, B and C follow', 9.6, bold=True) + cap('Heartbeats every second. Writes go to A.', '', 'card', y=130, h=34),
    cl('Node A', dead='Node A', lab={'Node A': '✗ down'}) + t(180, 30, '02:13:00 · A’s disk fails', 9.6, 'red', bold=True) + cap('Heartbeats from A stop. Writes start failing.', '', 'red', y=130, h=34),
    cl('Node A', dead='Node A', lab={'Node A': '✗ down', 'Node B': 'log: 1,204', 'Node C': 'log: 1,199'}) + t(180, 30, '02:13:10 · timeout reached', 9.6, 'acc', bold=True) + cap('B and C compare logs: B is more up to date.', 'B and C are a majority (2 of 3), so they may elect.', 'amber', y=124, h=44),
    cl('Node B', dead='Node A', lab={'Node A': '✗ down', 'Node B': 'NEW leader', 'Node C': 'follows B'}) + t(180, 30, '02:13:20 · B promoted', 9.6, 'green', bold=True) + cap('Clients are redirected to B. Writes resume.', 'Any writes A had not sent to B are lost (async).', 'green', y=124, h=44),
    cl('Node B', lab={'Node A': 'follower', 'Node B': 'leader', 'Node C': 'follower'}) + t(180, 30, 'Morning · A repaired', 9.6, 'blue', bold=True) + cap('A rejoins as a follower and copies from B.', 'It must never come back as a second leader.', 'blue', y=124, h=44),
]
s1 = anim_one('Real-time scenario 1', '2:13 am: the leader dies',
              'Three database nodes: A leads, B and C follow. At 2:13 am A\'s disk fails. Watch an automatic failover step by step, and where data can be lost.',
              'Automatic failover', 'Three database nodes, the leader failing and a follower being promoted', fr1,
              ['Normally Node A is the leader. B and C copy its log and everyone exchanges heartbeats every second.',
               'A\'s disk fails. Its heartbeats stop and client writes start failing.',
               'After a timeout (here 10 seconds) B and C compare how far their logs go. B is the most up to date. Together they form a majority of the three nodes, so they are allowed to elect a new leader.',
               'B is promoted and clients are redirected to it; writes resume after about 20–30 seconds in total. With asynchronous replication, the last writes A had acknowledged but not yet sent are lost.',
               'When A is repaired, it rejoins as a <b>follower</b>, discards anything B never had, and copies from B.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: Kafka acks
def kafka(acks, leader_has, followers_have, dead=False, note1='', note2='', tone='blue'):
    o = label_box(10, 36, 90, 46, ['Producer', f'acks={acks}'], 'acc', 9.2) + arrow(102, 59, 128, 59)
    o += label_box(130, 30, 100, 58, ['Leader', 'msg ✓' if leader_has else '—'], 'red' if dead else 'green', 9.2)
    o += label_box(250, 20, 100, 36, ['Follower 1: ' + ('✓' if followers_have else '—')], 'card', 8.6) + label_box(250, 64, 100, 36, ['Follower 2: ' + ('✓' if followers_have else '—')], 'card', 8.6)
    o += arrow(232, 50, 248, 38, 'ink3', 1.2, dash=True) + arrow(232, 68, 248, 82, 'ink3', 1.2, dash=True)
    return o + cap(note1, note2, tone, y=120, h=44)
fr2 = [
    kafka(0, True, False, note1='acks=0: fire and forget. The producer doesn’t wait.', note2='Fastest; messages can vanish without anyone knowing.', tone='amber'),
    kafka(1, True, False, note1='acks=1: OK once the leader has written it.', note2='Followers haven’t copied it yet.', tone='blue'),
    kafka(1, True, False, dead=True, note1='The leader crashes now. A follower becomes leader', note2='without the message: acknowledged, then lost.', tone='red'),
    kafka('all', True, True, note1='acks=all: OK only when all in-sync replicas have it.', note2='Set min.insync.replicas=2 so at least 2 copies exist.', tone='green'),
    kafka('all', True, True, dead=True, note1='Leader crashes: a follower already has the message.', note2='Nothing acknowledged is lost. Slightly slower writes.', tone='green'),
]
s2 = anim_one('Real-time scenario 2', 'Kafka acks: when is a message really safe?',
              'A payments service writes events to a Kafka topic with replication factor 3. The producer setting <code>acks</code> decides when the producer is told “done”. Watch what each setting means when a broker crashes.',
              'acks = 0, 1, all', 'A Kafka producer, a leader and two followers under different acks settings', fr2,
              ['<b>acks=0:</b> the producer sends and moves on without any confirmation. Fastest, but messages can be lost silently.',
               '<b>acks=1:</b> the producer gets “OK” once the partition leader has written the message, before followers have copied it.',
               'If the leader crashes at that moment, a follower becomes leader without the message. The producer was told it succeeded, but the message is gone.',
               '<b>acks=all:</b> the producer gets “OK” only when all in-sync replicas have the message. With <code>min.insync.replicas=2</code>, at least two copies must exist or the write is refused.',
               'Now a leader crash loses nothing that was acknowledged. The cost is a few milliseconds more per write. For payments, orders and anything you can’t recreate, use acks=all.'])

# ---------------------------------------------------------------- scenario 3 (advanced): split brain + fencing
def sb(stage):
    o = '<path d="M180 30V170" style="stroke:#D64545;stroke-width:3;stroke-dasharray:6 4"/>' if stage >= 1 else ''
    left = [('Node A', {0: 'leader (epoch 1)', 1: 'leader (epoch 1)', 2: 'still thinks: leader', 3: 'steps down', 4: 'epoch 1 writes rejected'}[stage], 'green' if stage < 2 else ('red' if stage == 2 else 'card'))]
    right = [('Node B', 'leader (epoch 2)' if stage >= 2 else 'follower', 'green' if stage >= 2 else 'card'), ('Node C', 'follower', 'card')]
    o += label_box(30, 60, 120, 50, [left[0][0], left[0][1]], left[0][2], 9)
    o += label_box(220, 40, 120, 46, [right[0][0], right[0][1]], right[0][2], 9) + label_box(220, 100, 120, 46, [right[1][0], right[1][1]], right[1][2], 9)
    return o
fr3 = [
    sb(0) + t(180, 22, 'A leads; B and C follow', 9.6, bold=True) + cap('Three nodes, one leader with epoch number 1.', '', 'card', y=176, h=34),
    sb(1) + t(180, 22, 'Network partition', 9.6, 'red', bold=True) + cap('A is cut off from B and C, but A is still running', 'and some clients can still reach it.', 'red', y=170, h=44),
    sb(2) + t(180, 22, 'B and C (a majority) elect B, epoch 2', 9.6, 'acc', bold=True) + cap('Danger: A doesn’t know and still accepts writes.', 'Two leaders = split brain. Data diverges.', 'red', y=170, h=44),
    sb(3) + t(180, 22, 'Defence 1: majority quorum', 9.6, 'green', bold=True) + cap('A alone is 1 of 3, not a majority: it must stop', 'accepting writes once it can’t reach a quorum.', 'green', y=170, h=44),
    sb(4) + t(180, 22, 'Defence 2: fencing token', 9.6, 'green', bold=True) + cap('Storage remembers epoch 2 and rejects any write', 'carrying the older epoch 1. Only one leader wins.', 'green', y=170, h=44),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Split brain: two leaders at once',
              'The worst replication failure is not a crash but a network split, where the old leader keeps running and a new one is elected. Watch how majorities and fencing tokens keep only one leader in charge.',
              'Split brain and fencing', 'A network partition creating two leaders, prevented by majority quorums and fencing tokens', fr3,
              ['Node A is the leader in “epoch 1”; B and C follow.',
               'A network fault separates A from B and C. A is alive, and some clients on its side can still send it writes.',
               'B and C stop hearing from A and, being two of three nodes, elect B as leader in epoch 2. If A keeps accepting writes, there are two leaders and two diverging versions of the data: <b>split brain</b>.',
               '<b>Majority quorum:</b> a leader must be able to reach a majority. A can reach only itself (1 of 3), so it steps down and refuses writes. This is why clusters use odd numbers of nodes: 3 or 5.',
               '<b>Fencing tokens:</b> every new leader gets a higher epoch number, and storage rejects writes carrying an older one. Consensus systems such as Raft (etcd, Kafka KRaft) and ZooKeeper provide exactly these guarantees.'])

realworld = '''  <p>Three live scenarios: an automatic failover at 2 am, what Kafka’s acks setting really guarantees, and an advanced look at split brain and how fencing prevents it.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Replication at work</h3>
''' + usecase('<rect x="14" y="20" width="40" height="50" rx="6" class="s-soft-green" style="stroke:var(--green)"/><rect x="66" y="20" width="40" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><path d="M54 45h12" style="stroke:var(--ink);stroke-width:2"/>',
              '1. Managed databases with standby replicas', 'Cloud databases (such as Amazon RDS Multi-AZ or Azure SQL) keep a synchronous standby in another zone and fail over automatically, typically within a minute or two.', ['Primary (zone A)', '*Sync standby (zone B)', 'Auto failover']) + usecase(
    '<rect x="20" y="20" width="22" height="50" rx="3" style="fill:var(--blue)"/><rect x="50" y="20" width="22" height="50" rx="3" style="fill:var(--blue);opacity:.6"/><rect x="80" y="20" width="22" height="50" rx="3" style="fill:var(--blue);opacity:.6"/>',
    '2. Read replicas for reports and dashboards', 'Reporting and analytics queries are sent to read replicas so they don’t slow down the primary that serves the app. Reports may lag by a few seconds, which is fine for them.', ['Primary: app writes', '*Async read replicas', 'Dashboards']) + usecase(
    '<path d="M16 45h88" style="stroke:var(--violet);stroke-width:3"/><circle cx="30" cy="45" r="8" style="fill:var(--violet)"/><circle cx="60" cy="45" r="8" style="fill:var(--violet)"/><circle cx="90" cy="45" r="8" style="fill:var(--violet)"/>',
    '3. Kafka for payments and orders', 'Fintech and e-commerce teams run critical topics with replication factor 3, <code>min.insync.replicas=2</code> and <code>acks=all</code>, so a broker failure loses no acknowledged events.', ['Producer acks=all', '*3 replicas, ISR ≥ 2', 'No acknowledged loss']) + usecase(
    '<circle cx="35" cy="45" r="18" class="s-soft-acc" style="stroke:var(--track)"/><circle cx="85" cy="45" r="18" class="s-soft-acc" style="stroke:var(--track)"/><path d="M53 45h14" style="stroke:var(--track);stroke-width:2;stroke-dasharray:3 3"/>',
    '4. Disaster recovery across regions', 'Banks and large platforms keep an asynchronous copy in another region (for example Mumbai and Hyderabad) and rehearse switching over, accepting a few seconds of possible data loss in a regional disaster.', ['Region 1', '*Async cross-region copy', 'DR region'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', '2:13 am: “orders-db primary down”', story)
        + part(2, 'definition', 'Definition', 'What is replication?', definition)
        + part(3, 'types', 'Types and ways to use it', 'Leaders, followers and how they sync', types)
        + part(4, 'steps', 'Step by step', 'One write, three copies, one failure', steps)
        + part(5, 'animation', 'See it happen', 'Riya changes her address: which copy answers?', '  <p>Step through the six frames. Left: Riya updating and re-checking her address. Right: the leader and followers, and which copy serves each request.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: copies under failure', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Database design · availability', 'Fresher', 'Make the orders database survive a server failure',
            'The orders database runs on one server. Management wants it to survive a hardware failure with at most a minute of downtime and no lost orders.',
            'can you design basic replication with clear RPO/RTO?',
            '<ul><li>Add a <b>synchronous (or semi-synchronous) standby</b> in another availability zone: RPO ≈ 0 for committed orders.</li><li>Automate failover with health checks and a managed service or a tool like Patroni, aiming for an RTO under a minute.</li><li>Connect apps through a stable endpoint (DNS or proxy) that moves to the new primary.</li><li>Add async read replicas for reports.</li><li>Keep point-in-time backups for mistakes and test restores regularly.</li></ul>',
            'saying “take nightly backups” as the answer to availability.')
        + scn('Consistency · user experience', '1–3 years', '“I paid but the app says unpaid”',
              'After adding read replicas, some customers see “payment pending” for a few seconds right after paying, and pay again.',
              'do you recognise replication lag and read-your-writes?',
              '<p>Reads go to asynchronous replicas that haven’t applied the payment yet. Fix: route a user’s reads to the primary for a short window after they write (or for critical screens like payment status), or read from a replica only if it has caught up to the user’s last write position. Make the payment API idempotent so a second tap doesn’t charge twice, and show “processing” instead of “unpaid” while confirming.</p>',
              'removing replicas entirely, or adding a fixed sleep before reading.')
        + scn('Streaming · durability', '1–3 years', 'Messages lost during a broker restart',
              'During a rolling restart of Kafka brokers, a few order events disappeared, although producers logged success.',
              'do you know how acks, ISR and unclean leader election interact?',
              '<p>Producers were probably using <code>acks=1</code> (or the topic allowed unclean leader election), so a leader acknowledged messages and then lost leadership before followers copied them. Fix: replication factor 3, <code>min.insync.replicas=2</code>, producers with <code>acks=all</code> and idempotence enabled, and <code>unclean.leader.election.enable=false</code>. Restart brokers one at a time, waiting for under-replicated partitions to return to zero.</p>',
              'adding retries in consumers, which can’t bring back a message that was never stored.')
        + scn('Fundamentals · interview', 'Fresher', '“Is replication the same as backup?”',
              'Interviewers like this question because many candidates say yes.',
              'do you understand what each protects against?',
              '<p>No. Replication keeps live copies so the system survives machine, disk or zone failures with little downtime; every change, including mistakes and corruption, is copied within seconds. Backups are point-in-time copies kept separately so you can restore data after accidental deletes, bugs, ransomware or logical corruption. Production systems need both, and backups must be tested by actually restoring them.</p>',
              'saying “we have three replicas, so we don’t need backups”.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
