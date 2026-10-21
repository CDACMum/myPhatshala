import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Replicas across racks',
    intro='<p>Two racks of three DataNodes. Check where each block\'s replicas landed, then break things and watch the NameNode repair them.</p>',
    racks=2, nodes=3, features=['upload', 'fail', 'chaos', 'fsck'],
    preload=[dict(name='upi_txns.csv', sizeMB=768)],
    **{'try': [
        dict(text='In the NameNode metadata tab, check one block: are its replicas in both racks?', on='fsck'),
        dict(text='Stop one DataNode and fast-forward: watch it go from “no heartbeat” to DEAD, then re-replication.', on='rereplicated'),
        dict(text='Stop all three nodes of one rack. Run fsck: any missing blocks?', on='fsck'),
    ]},
)))

META = dict(
    module='05-hdfs-architecture', lesson='03-replication-and-rack-awareness', n='5.3',
    module_label='Module 5 · HDFS architecture',
    title='Replication and rack awareness',
    desc='How HDFS keeps three copies of every block and where it puts them: the default placement policy (writer node, another rack, same rack as the second), topology scripts, setrep, under- and over-replicated blocks, and automatic re-replication. Shown on a real Hadoop 3.5.0 cluster with 2 racks: fsck -racks output, a DataNode stopped and declared dead, 4 blocks re-replicated in seconds, extra replicas deleted when it returned. Python placement simulator, quiz and interview scenarios.',
    og_desc='Three copies, two racks, automatic repair. Watch HDFS heal itself after a DataNode dies on a real cluster.',
    minutes=28, level='Beginner → Intermediate',
    lead='Replication is what lets Hadoop run on ordinary servers that fail. This lesson explains the replication factor, the rack-aware placement rule that balances safety against network cost, and what the NameNode does when replicas go missing or reappear, with real timings from a two-rack cluster where we stopped DataNodes on purpose.',
    chips=['Real failure timeline', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Simulate the default placement policy',
    intro='<p>This program places three replicas of each block with HDFS\'s default rule on a cluster of two racks, then checks the result the way <code>fsck</code> would: at least two racks, at most two replicas per rack.</p>',
    code='''import random
random.seed(7)
racks = {"/rack1": ["dn1", "dn2"], "/rack2": ["dn3", "dn4"]}
rack_of = {dn: r for r, nodes in racks.items() for dn in nodes}

def place(writer=None):
    first = writer if writer in rack_of else random.choice(list(rack_of))
    other_racks = [r for r in racks if r != rack_of[first]]
    second = random.choice(racks[random.choice(other_racks)])
    third = random.choice([d for d in racks[rack_of[second]] if d != second])
    return [first, second, third]

for blk in ["blk_A", "blk_B", "blk_C"]:
    replicas = place()
    used = [rack_of[d] for d in replicas]
    ok = len(set(used)) >= 2 and max(used.count(r) for r in used) <= 2
    print(blk, replicas, used, "OK" if ok else "BAD")
''',
    anno=[
        ('first = writer if writer in rack_of else random.choice(list(rack_of))', 'Replica 1: on the writer\'s own node if the writer is a DataNode (fast, local write); otherwise a random node.'),
        ('second = random.choice(racks[random.choice(other_racks)])', 'Replica 2: any node in a <b>different</b> rack, so a rack failure can\'t take everything.'),
        ('third = random.choice([d for d in racks[rack_of[second]] if d != second])', 'Replica 3: a different node in the <b>same rack as replica 2</b>, so the data crosses racks only once.'),
    ],
    tasks=[
        dict(label='1 · Place three blocks', hint='Press <b>Run</b>. Then call <code>place("dn1")</code>: the first replica should always be dn1.', code=None),
        dict(label='2 · Without rack awareness', hint='<b>Predict first:</b> with no topology script, every node is in <code>/default-rack</code>. Can a block survive the loss of “a rack” now?',
             code='''racks = {"/default-rack": ["dn1", "dn2", "dn3", "dn4"]}
replicas = ["dn1", "dn3", "dn4"]
print("racks used:", {r for r, ns in racks.items() for d in replicas if d in ns})
print("one rack lost -> live replicas:", 0)
'''),
        dict(label='3 · Cross-rack traffic', hint='Writing 1 TB with replication 3: how much data crosses between racks with the default policy, and with all three replicas on different racks?',
             code='''tb = 1
default_cross = tb * 1      # replica 1 -> replica 2 only
three_racks = tb * 2        # 1 -> 2 and 2 -> 3 both cross
print("default policy:", default_cross, "TB across racks")
print("three racks:   ", three_racks, "TB across racks")
'''),
        dict(label='4 · Dead-node time', hint='Compute when a silent DataNode is declared dead: 2 × recheck interval + 10 × heartbeat interval, for the defaults and for our lab.',
             code='''for name, recheck_s, hb_s in [("default", 300, 3), ("lab", 15, 3)]:
    t = 2 * recheck_s + 10 * hb_s
    print(f"{name:8} dead after {t} s = {t // 60} min {t % 60} s")
'''),
        dict(label='5 · Spot the error', hint='This placement puts replica 3 in the wrong rack. Compare with the rule and fix it.',
             code='''racks = {"/rack1": ["dn1", "dn2"], "/rack2": ["dn3", "dn4"]}
rack_of = {d: r for r, ns in racks.items() for d in ns}
first, second = "dn1", "dn3"
third = [d for d in racks[rack_of[first]] if d != first][0]
used = [rack_of[d] for d in (first, second, third)]
print([first, second, third], used)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: check every block\'s rack spread',
    intro='<p>This script runs <code>fsck -racks</code> on the lab cluster and checks each block against the placement rules. Save it as <code>rack_check.py</code> in the <code>hdfs-lab</code> folder and run it while the cluster is up.</p>',
    items=[
        dict(title='Rack spread of every block under /user/hadoop/data', file='rack_check.py',
             cmd=open(os.path.join(HERE, 'rack_check.py')).read() + '\n# In the hdfs-lab folder:\n#   python3 rack_check.py',
             output='''blk_1073741826: {'/rack1': 2, '/rack2': 1}  OK
blk_1073741827: {'/rack2': 2, '/rack1': 1}  OK
blk_1073741828: {'/rack2': 2, '/rack1': 1}  OK
blk_1073741829: {'/rack1': 2, '/rack2': 1}  OK
blk_1073741830: {'/rack1': 2, '/rack2': 1}  OK
blk_1073741825: {'/rack1': 2, '/rack2': 1}  OK''',
             note='Real output, taken after the DataNode stop/start experiments in Part 4: re-replication kept the rack rule for every block. Run it after your own experiments; a “CHECK” line means a block is in only one rack (mis-replicated).'),
    ],
)

TRACE = dict(
    heading='How the NameNode reacts to a dead DataNode',
    intro='<p>Follow the block map when dn3 is declared dead: which blocks become under-replicated, and where the new copies go.</p>',
    code='''block_map = {"A": ["dn1", "dn3", "dn4"], "B": ["dn2", "dn3", "dn4"], "C": ["dn1", "dn2", "dn4"]}
dead = "dn3"
for blk in block_map:
    block_map[blk] = [d for d in block_map[blk] if d != dead]
under = [b for b, ds in block_map.items() if len(ds) < 3]
for b in under:
    target = next(d for d in ["dn1", "dn2", "dn4"] if d not in block_map[b])
    block_map[b].append(target)
print(under, block_map)
''',
    notes={4: 'Forget :: Replicas on the dead node are removed from the block map.',
           5: 'Find :: Blocks with fewer than 3 live replicas.',
           7: 'Target :: A live node that doesn\'t already hold the block (real HDFS also checks racks and load).'},
)

WORKED_INTRO = 'Three replication questions engineers answer with numbers: what replication costs in disk, how long re-replication takes after a failure, and whether a planned maintenance window is safe. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Capacity · disk', title='Raw disk for different replication factors',
         problem='<p>A bank keeps 200 TB of transaction history. How much raw disk is needed with replication 1, 2 and 3, keeping 20% of disk free?</p>',
         inp='200 TB · replication 1, 2, 3 · 20% free',
         approach=['Raw = data × replication.',
                   'Disk to buy = raw / 0.8.',
                   'Compare the three.'],
         code='''data_tb = 200
for r in [1, 2, 3]:
    raw = data_tb * r
    print(f"replication {r}: {raw} TB raw, buy {raw / 0.8:.0f} TB")
''', notes={3: 'Raw :: Each replica is a full copy.'},
         tryit='With erasure coding RS-6-3 the factor is 1.5 instead of 3. How much disk does that save on 200 TB?'),
    dict(level='i', tag='Operations · recovery', title='How long does re-replication take?',
         problem='<p>A DataNode with 24 TB of block replicas dies. 40 other DataNodes help, each copying at about 100 MB/s in total for re-replication. Roughly how long until every block has 3 replicas again?</p>',
         inp='24 TB lost · 40 nodes · 100 MB/s each',
         approach=['Total bandwidth = nodes × rate.',
                   'Time = data / bandwidth.',
                   'Convert to minutes.'],
         code='''lost_mb = 24 * 1024 * 1024
bandwidth = 40 * 100
seconds = lost_mb / bandwidth
print(f"about {seconds / 60:.0f} minutes ({seconds / 3600:.1f} hours)")
''', notes={3: 'Parallel :: Every surviving node sends and receives copies at once.'},
         tryit='With only 5 surviving nodes the same repair takes 8 times longer. This is why big clusters heal faster, and why the window of risk matters.'),
    dict(level='a', tag='Maintenance · risk', title='Is it safe to take these nodes down?',
         problem='<p>You want to reboot dn2 and dn5 together. Given each block\'s replica locations, list the blocks that would have no live replica during the reboot, and those left with only one.</p>',
         inp='5 blocks with replica lists · nodes down: dn2, dn5',
         approach=['For each block, remove the nodes going down.',
                   'Zero left → data unavailable; one left → at risk.',
                   'Report both lists before approving the change.'],
         code='''blocks = {"b1": ["dn1", "dn2", "dn3"], "b2": ["dn2", "dn5", "dn6"],
          "b3": ["dn2", "dn5"], "b4": ["dn4", "dn5", "dn6"], "b5": ["dn1", "dn3", "dn4"]}
down = {"dn2", "dn5"}
unavailable = [b for b, ds in blocks.items() if not set(ds) - down]
at_risk = [b for b, ds in blocks.items() if len(set(ds) - down) == 1]
print("unavailable:", unavailable)
print("only one copy left:", at_risk)
''', notes={4: 'Set difference :: Nodes that stay up.'},
         tryit='b3 has replication 2 and both copies are on the nodes going down. Reboot one node at a time, or raise b3\'s replication first.'),
]

QUIZ = mix([
    dict(q='What is the default replication factor in HDFS?', options=['1', '2', '3', '5'], answer=2,
         why='dfs.replication defaults to 3.'),
    dict(q='With the default policy and a writer that is not a DataNode, where do the 3 replicas go?', options=['All on one rack', 'Random node; a node on another rack; another node on that same second rack', 'Three different racks', 'All on the writer'], answer=1,
         why='That is BlockPlacementPolicyDefault. Our fsck showed 2 replicas in one rack and 1 in the other for every block.'),
    dict(q='Why not put all three replicas in three different racks?', options=['HDFS does not support it', 'It would double cross-rack traffic for every write', 'It uses more disk', 'Racks can only hold one replica'], answer=1,
         why='The default rule crosses racks once per write while still surviving a rack failure.'),
    dict(q='How does Hadoop learn which rack a DataNode is in?', options=['From the DataNode\'s host name automatically', 'From a topology script or mapping (net.topology.script.file.name)', 'From YARN', 'It guesses by IP range'], answer=1,
         why='Without a mapping every node is in /default-rack.'),
    dict(q='A DataNode stops sending heartbeats. With default settings, when is it declared dead?', options=['After 3 seconds', 'After 30 seconds', 'After about 10 minutes 30 seconds', 'Never'], answer=2,
         why='2 × 5 min recheck + 10 × 3 s heartbeat = 630 s. Our lab used 15 s rechecks, so about 60 s.'),
    dict(q='What does hdfs dfs -setrep -w 2 file do?', options=['Writes the file twice', 'Changes the file\'s replication factor to 2 and waits until it is reached', 'Moves the file to rack 2', 'Deletes two blocks'], answer=1,
         why='We saw Live_repl change from 3 to 2 and back to 3.'),
    dict(q='A dead DataNode comes back with its old replicas. What happens?', options=['Its data is ignored for ever', 'Blocks become over-replicated and the extra replicas are deleted', 'The NameNode must be formatted', 'All blocks get 4 replicas permanently'], answer=1,
         why='We saw “Pending deletion blocks: 7”, then 0.'),
    dict(q='Which fsck status means a block has enough replicas but all of them are in one rack?', options=['Under-replicated', 'Mis-replicated', 'Corrupt', 'Missing'], answer=1,
         why='Mis-replicated blocks violate the placement policy even though the count is fine.'),
])

REVISION = [
    'Replication factor: <code>dfs.replication</code> = <b>3</b>, per file; change with <code>hdfs dfs -setrep [-w] N</code>.',
    'Default placement: 1st on writer\'s node (or random), 2nd on <b>another rack</b>, 3rd on <b>another node of the 2nd\'s rack</b>.',
    'Benefits: survives a rack failure; only one cross-rack transfer per write; nearby replicas for reads.',
    'Racks come from <code>net.topology.script.file.name</code>; otherwise <code>/default-rack</code>. Check: <code>hdfs dfsadmin -printTopology</code>.',
    'Dead node: 2 × recheck (5 min) + 10 × heartbeat (3 s) = <b>10 min 30 s</b> by default.',
    'Under-replicated → copied; over-replicated → extras deleted; mis-replicated → wrong rack spread.',
    'Real lab: dead at ~56 s (15 s recheck), 4 under-replicated blocks repaired within 7 s.',
    'Replication 3 = 3× raw disk; erasure coding ≈ 1.5× for cold data.',
]
FAQ = [
    ('What is rack awareness in Hadoop?', 'The NameNode knows which rack each DataNode is in (from a topology script or mapping) and uses it to place replicas: by default one replica on one rack and two on another. This protects data against a whole rack failing while limiting cross-rack network traffic, and lets schedulers prefer rack-local data.'),
    ('How does HDFS place the three replicas of a block?', 'The first replica goes on the writer\'s node if the writer is a DataNode, otherwise on a random node; the second on a node in a different rack; the third on a different node in the same rack as the second. More replicas go to random nodes, keeping at most two per rack where possible.'),
    ('What happens when a DataNode fails?', 'The NameNode stops receiving its heartbeats. After the dead-node interval (10 min 30 s by default) it marks the node dead, removes its replicas from the block map, and schedules copies of the now under-replicated blocks from surviving replicas to other DataNodes.'),
    ('How do I change the replication of a file?', 'Use hdfs dfs -setrep N path (add -w to wait until the change is complete; giving a directory applies it to every file below it). New files follow dfs.replication of the writing client.'),
    ('What is the difference between under-replicated and missing blocks?', 'An under-replicated block still has at least one live replica, so it is readable and HDFS will copy it. A missing block has no live replica at all: its data cannot be read until a node holding it returns.'),
    ('Is replication a backup?', 'No. Replication protects against hardware failure, but deletes and bad writes are applied to every replica. Backups, snapshots and DistCp copies to another cluster protect against those.'),
    ('How is the rack of a DataNode configured?', 'Set net.topology.script.file.name in core-site.xml to a script that prints one rack path (e.g. /dc1/rack07) for each IP or host name it is given, or use TableMapping with a host-to-rack file.'),
]

PRACTICE_INTRO = 'Replication and placement exercises, including checks on the real fsck output from the lab.'
PROBLEMS = [
    dict(level='easy', title='Replicas on disk', stmt='A 640 MB file with 128 MB blocks and replication 3: how many block replicas are stored in total?', inp='640 MB · 128 MB · 3',
         code='print(640 // 128 * 3, "replicas")\n', explain='5 blocks × 3 = 15 replicas.'),
    dict(level='easy', title='Dead-node timer', stmt='Compute the dead-node time for recheck-interval 300 s and heartbeat 3 s.', inp='300 s · 3 s',
         code='print(2 * 300 + 10 * 3, "seconds")\n', explain='630 seconds = 10 minutes 30 seconds.'),
    dict(level='easy', title='Racks per block', stmt='Count the racks used by each replica list from the real fsck output.', inp='[rack1, rack2, rack2] · [rack1, rack1, rack2]',
         code='''for reps in [["/rack1", "/rack2", "/rack2"], ["/rack1", "/rack1", "/rack2"]]:
    print(reps, "->", len(set(reps)), "racks")
''', explain='Both use 2 racks with 2 replicas in one of them: exactly the default policy.'),
    dict(level='medium', title='Mis-replicated check', stmt='Flag blocks whose replicas are all in one rack or have more than 2 replicas in one rack.', inp='three replica-rack lists',
         code='''from collections import Counter
blocks = {"b1": ["r1", "r2", "r2"], "b2": ["r1", "r1", "r1"], "b3": ["r2", "r1", "r1"]}
for b, rs in blocks.items():
    c = Counter(rs)
    print(b, "OK" if len(c) >= 2 and max(c.values()) <= 2 else "MIS-REPLICATED")
''', explain='b2 has all three replicas in rack r1: a rack failure would make it unavailable.'),
    dict(level='medium', title='Lost rack', stmt='For each block, how many replicas survive if rack r1 is lost?', inp='b1: r1,r2,r2 · b2: r1,r1,r2 · b3: r1,r1,r1',
         code='''blocks = {"b1": ["r1", "r2", "r2"], "b2": ["r1", "r1", "r2"], "b3": ["r1", "r1", "r1"]}
for b, rs in blocks.items():
    print(b, sum(r != "r1" for r in rs), "left")
''', explain='b1 keeps 2, b2 keeps 1, b3 keeps 0: the mis-replicated block is the only one lost.'),
    dict(level='medium', title='Cross-rack bytes', stmt='A 1 GB file is written with the default policy by a client on a DataNode. How many GB cross racks? How many if replication is 2?', inp='1 GB · replication 3 and 2',
         code='''rack = {"dn1": "r1", "dn3": "r2", "dn4": "r2"}
for pipeline in [["dn1", "dn3", "dn4"], ["dn1", "dn3"]]:
    hops = sum(rack[a] != rack[b] for a, b in zip(pipeline, pipeline[1:]))
    print(f"replication {len(pipeline)}: {pipeline} -> {hops} GB crosses racks")
''', explain='The write pipeline dn1 → dn3 → dn4 has one cross-rack hop (dn1 → dn3), so 1 GB crosses racks with replication 3 or 2; the dn3 → dn4 hop stays inside rack r2.'),
    dict(level='business', title='Cost of replication', stmt='Disk costs Rs 3,000 per TB. 500 TB of data: compare the disk cost of replication 3 with erasure coding at 1.5×.', inp='500 TB · Rs 3,000/TB · 3× vs 1.5×',
         code='''for name, f in [("replication 3", 3), ("erasure coding", 1.5)]:
    print(f"{name:15}: Rs {500 * f * 3000 / 1e5:.1f} lakh")
''', explain='Rs 45 lakh against Rs 22.5 lakh of raw disk: why cold data moves to erasure coding.'),
    dict(level='advanced', title='Placement for a writer on a DataNode', stmt='Write a function placing 3 replicas for a writer on dn4 with racks r1=[dn1,dn2] and r2=[dn3,dn4], and check the rule.', inp='writer dn4',
         code='''racks = {"r1": ["dn1", "dn2"], "r2": ["dn3", "dn4"]}
rack_of = {d: r for r, ds in racks.items() for d in ds}
def place(writer):
    first = writer
    second = racks[[r for r in racks if r != rack_of[first]][0]][0]
    third = [d for d in racks[rack_of[second]] if d != second][0]
    return [first, second, third]
p = place("dn4")
print(p, [rack_of[d] for d in p])
''', explain='[dn4, dn1, dn2] in racks [r2, r1, r1]: local first replica, then two in the other rack.'),
]

SCN_INTRO = 'Replication questions test whether you can reason about failures and their cost.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · placement</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Explain where the three replicas of a block go, and why”</h4>
      <p class="scn__situation">Probably the most common HDFS interview question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the rule and its reasons.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Replica 1 on the writer's node (or a random node if the client is outside the cluster), replica 2 on another rack, replica 3 on a different node in replica 2's rack.</li>
          <li>Reasons: survives a whole rack failure; the write crosses racks only once; reads can find a nearby copy.</li>
          <li>Requires a correct topology script; otherwise everything is in /default-rack.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · failure</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A DataNode died 2 minutes ago. Why is nothing being re-replicated?</h4>
      <p class="scn__situation">A junior engineer sees a DataNode process crash and expects immediate copying.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the dead-node timeout and why it exists.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The NameNode waits 10 min 30 s by default (2 × recheck interval + 10 heartbeats) before declaring a node dead.</li>
          <li>The delay avoids copying terabytes every time a node is briefly slow or restarting.</li>
          <li>Meanwhile the node is marked stale after 30 s, and reads can avoid it if <code>dfs.namenode.avoid.read.stale.datanode</code> is enabled.</li>
          <li>If the node won't return, re-replication starts automatically after the timeout.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · racks</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>After a rack power failure, some files were unreadable</h4>
      <p class="scn__situation">The cluster has replication 3, yet a single rack outage made several files unavailable.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you suspect the rack mapping.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>With correct rack awareness that can't happen, so check <code>hdfs dfsadmin -printTopology</code>: probably no topology script, or nodes mapped to the wrong racks.</li>
          <li>Also check files with replication 1 or 2, and mis-replicated blocks in <code>fsck</code>.</li>
          <li>Fix the mapping; then fsck shows mis-replicated blocks, which the NameNode corrects over time (or run the balancer).</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Cost · storage</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Can we save money with replication 2?”</h4>
      <p class="scn__situation">A manager wants to reduce disk costs by a third.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> balanced judgement about risk.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Replication 2 survives only one failure; a second disk failure during re-replication loses blocks, and rack failure protection becomes weaker.</li>
          <li>Better options: erasure coding for cold data (≈1.5×), deleting or archiving unused data, compressing with efficient formats.</li>
          <li>Replication 2 can be acceptable for data that can be regenerated quickly (intermediate results).</li>
        </ul>
      </div></details>
    </article>
'''
