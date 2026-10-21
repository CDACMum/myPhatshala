import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)
rd = lambda f: open(os.path.join(HERE, f)).read()

META = dict(
    module='06-hdfs-operations', lesson='04-admin-commands-dfsadmin-fsck-and-balancer', n='6.4',
    module_label='Module 6 · HDFS operations',
    title='Admin commands: dfsadmin, fsck and balancer',
    desc='Run an HDFS cluster like an admin, with real Hadoop 3.5.0 outputs: dfsadmin -report, fsck with blocks and racks, decommissioning a DataNode with dfs.hosts.exclude and refreshNodes (Decommissioned in 52 s), recommissioning, adding a new DataNode and watching the balancer move 914.72 MB in 8 blocks, and why it gave up after 5 idle iterations. Python balancer simulator, quiz and interview scenarios.',
    og_desc='Retire a server without losing a block, and fill a new one: decommission and balancer on a real cluster.',
    minutes=28, level='Intermediate',
    lead='Servers come and go: disks fail, new machines arrive. This lesson shows the tools that keep HDFS healthy through all of it, on a real 5-node cluster: dfsadmin to see and control the cluster, fsck to prove every block is safe, decommissioning to retire a DataNode without risk, and the balancer to spread data onto a new node.',
    chips=['Real decommission and balancer runs', 'Balancer simulator', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='A balancer in 30 lines',
    intro='<p>This program does what <code>hdfs balancer</code> does, simplified: compute each node\'s utilisation (used ÷ capacity) and the cluster average, then move 128 MB blocks from the fullest node to the emptiest until every node is within the threshold of the average.</p>',
    code='''cap = {"dn-1": 4000, "dn-2": 4000, "dn-3": 4000, "dn-6": 4000}    # MB
used = {"dn-1": 3200, "dn-2": 3072, "dn-3": 2944, "dn-6": 0}
threshold = 10          # percent
block = 128             # MB

def util(n):
    return 100 * used[n] / cap[n]

def average():
    return 100 * sum(used.values()) / sum(cap.values())

moves = 0
while True:
    avg = average()
    src = max(used, key=util)
    dst = min(used, key=util)
    if util(src) - avg <= threshold and avg - util(dst) <= threshold:
        break
    used[src] -= block
    used[dst] += block
    moves += 1

print(f"average {average():.1f}%  moves {moves}  ({moves * block} MB)")
for n in cap:
    print(f"  {n}: {util(n):5.1f}%")
''',
    anno=[
        ('    return 100 * used[n] / cap[n]', 'Utilisation is a percentage of capacity, not a block count. That is why a big new disk with 0 blocks is “underutilised”.'),
        ('    if util(src) - avg <= threshold and avg - util(dst) <= threshold:', 'Balanced = every node within ±threshold of the average. Here 10%, the default; the real tool accepts 1 to 100.'),
        ('    used[src] -= block', 'A real move copies the block to the target and then deletes the source replica, so replication never drops.'),
    ],
    tasks=[
        dict(label='1 · Balance a new node', hint='Press <b>Run</b>. How many blocks move before dn-6 is within 10% of the average?', code=None),
        dict(label='2 · Lower the threshold', hint='<b>Predict first:</b> with threshold 5 instead of 10, will more or fewer blocks move?',
             code='''cap, used = {"a": 4000, "b": 4000, "c": 4000, "new": 4000}, {"a": 3200, "b": 3072, "c": 2944, "new": 0}
for threshold in [10, 5, 1]:
    u = dict(used); moves = 0
    while True:
        util = {n: 100 * u[n] / cap[n] for n in u}
        avg = 100 * sum(u.values()) / sum(cap.values())
        s, d = max(util, key=util.get), min(util, key=util.get)
        if util[s] - avg <= threshold and avg - util[d] <= threshold:
            break
        u[s] -= 128; u[d] += 128; moves += 1
    print(f"threshold {threshold:2}%: {moves} moves, {moves * 128} MB")
'''),
        dict(label='3 · Why our lab said “balanced”', hint='Five nodes with 252 GB each; three hold 0.97 GB, two hold nothing. Is anyone more than 5% away from the average?',
             code='''cap = 252
used = [0.97, 0.97, 0.97, 0, 0]
util = [100 * u / cap for u in used]
avg = sum(util) / len(util)
print("utilisations:", [round(x, 2) for x in util], " average", round(avg, 2))
print("balanced at 5%:", all(abs(x - avg) <= 5 for x in util))
'''),
        dict(label='4 · How long will decommissioning take?', hint='A node holds 6 TB. The other nodes can receive re-replication at 400 MB/s in total. Estimate the hours.',
             code='''tb, mb_per_s = 6, 400
seconds = tb * 1024 * 1024 / mb_per_s
print(f"about {seconds / 3600:.1f} hours")
'''),
        dict(label='5 · Spot the error', hint='This check calls the cluster balanced too early: it compares only the fullest node. Fix it to check the emptiest node too.',
             code='''util = {"dn-1": 81.0, "dn-2": 77.0, "dn-3": 74.0, "dn-6": 2.0}
avg = sum(util.values()) / len(util)
balanced = max(util.values()) - avg <= 10
print("average", avg, "balanced:", balanced)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: retire a node, fill a new one',
    intro='<p>Two scripts for the <code>hdfs-lab</code> folder. The first decommissions a DataNode and prints its status every few seconds until it is <i>Decommissioned</i>, checks fsck and recommissions it. The second starts a sixth DataNode with its own small disk and runs the balancer. First add <code>HDFS-SITE.XML_dfs.hosts.exclude=/opt/hadoop/etc/hadoop/dfs.exclude</code> to the <code>config</code> file and recreate the namenode (<code>docker compose up -d</code>).</p>',
    items=[
        dict(title='Decommission and recommission one DataNode', file='decommission_watch.sh',
             cmd=rd('decommission_watch.sh') + '\n# In the hdfs-lab folder (find the IP with: hdfs dfsadmin -printTopology):\n#   bash decommission_watch.sh 172.19.0.7',
             output=rd('decommission_output.txt').strip(),
             note='Real output. Only 2 blocks, yet 60 s: the NameNode checks decommission progress every 30 s. After recommissioning, its replicas were extra copies and were removed: 0 blocks.'),
        dict(title='Add a node, run the balancer', file='add_node_and_balance.sh',
             cmd=rd('add_node_and_balance.sh') + '\n# In the hdfs-lab folder:\n#   bash add_node_and_balance.sh\n# Remove the extra node afterwards:  docker rm -f lab5-datanode-6',
             output=rd('balance_output.txt').strip(),
             note='Real output, with iterations 2 to 4 trimmed. 8 blocks moved in 16 s, then the 1.5 GB RAM disk refused more blocks (“Out of space”) and the balancer stopped after 5 idle iterations. No data was at risk: a failed move leaves the block where it was.'),
    ],
)

TRACE = dict(
    heading='Deciding what a decommission must copy',
    intro='<p>For each block on the retiring node, count the replicas on other live nodes and decide whether a new copy is needed.</p>',
    code='''blocks = {"A": ["dn-2", "dn-4", "dn-5"], "B": ["dn-4", "dn-1", "dn-3"], "C": ["dn-1", "dn-2", "dn-3"]}
retiring = "dn-4"
to_copy = []
for blk, nodes in blocks.items():
    if retiring in nodes:
        others = [n for n in nodes if n != retiring]
        if len(others) < 3:
            to_copy.append((blk, others[0]))
print("copy:", to_copy)
''',
    notes={5: 'Only its blocks :: Blocks that never lived on dn-4 are untouched.',
           6: 'Count others :: Replicas on a decommissioning node no longer count towards the 3.',
           8: 'Source :: Copy from any live replica; the NameNode picks one and a target that keeps rack placement.'},
)

WORKED_INTRO = 'Three admin calculations: how long a decommission takes, how much data a balancer must move, and how much faster it runs with more bandwidth. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Decommission · time', title='How long to retire a 12 TB node?',
         problem='<p>A DataNode holds 12 TB. Re-replication across the cluster reaches about 1 GB/s in total. Roughly how long does decommissioning take, and why does it hardly matter how many blocks there are?</p>',
         inp='12 TB · 1 GB/s',
         approach=['Time = data ÷ total copy speed.',
                   'Convert TB to GB (×1024).',
                   'Convert seconds to hours.'],
         code='''tb, gb_per_s = 12, 1
seconds = tb * 1024 / gb_per_s
print(f"about {seconds / 3600:.1f} hours")
''', notes={2: 'Bytes :: Copy time depends on bytes; block count matters only for tiny amounts, where the 30 s checks dominate (our 2-block run took 60 s).'},
         tryit='About 3.4 hours. Many nodes copy in parallel, which is why decommissioning a node is far faster than restoring 12 TB from a backup.'),
    dict(level='i', tag='Balancer · planning', title='How much must the balancer move?',
         problem='<p>Ten DataNodes of 40 TB each are 75% full. We add five empty 40 TB nodes. With threshold 10%, how much data must move at least, so that each new node is within 10% of the new average?</p>',
         inp='10 × 40 TB at 75% · 5 new × 40 TB · threshold 10%',
         approach=['New average = total used ÷ total capacity.',
                   'Each new node needs at least (average − 10%) × 40 TB.',
                   'Multiply by 5.'],
         code='''used = 10 * 40 * 0.75
cap = 15 * 40
avg = 100 * used / cap
need_each = (avg - 10) / 100 * 40
print(f"average {avg:.1f}%, each new node needs {need_each:.1f} TB, total {5 * need_each:.0f} TB")
''', notes={4: 'Average :: Adding empty capacity lowers the average utilisation.'},
         tryit='The average drops to 50%; each new node must reach 40%: 16 TB each, 80 TB in total.'),
    dict(level='a', tag='Balancer · bandwidth', title='How long will that take at 100 MB/s per node?',
         problem='<p>Moving those 80 TB: each of the 5 new nodes receives at most at the balancer bandwidth (default 100 MB/s per DataNode). How long does it take at 100 MB/s, and at 300 MB/s set with <code>-setBalancerBandwidth</code> at night?</p>',
         inp='80 TB · 5 receivers · 100 or 300 MB/s',
         approach=['Each new node receives 16 TB.',
                   'Time = 16 TB ÷ per-node bandwidth.',
                   'Compare the two settings.'],
         code='''per_node_tb = 16
for mb_s in [100, 300]:
    hours = per_node_tb * 1024 * 1024 / mb_s / 3600
    print(f"{mb_s} MB/s: {hours:.0f} hours ({hours / 24:.1f} days)")
''', notes={3: 'Limit :: The bandwidth limit protects running jobs; raising it trades job speed for faster balancing.'},
         tryit='About 47 hours vs 16 hours. In practice teams balance over several nights, or add new nodes before the old ones are full.'),
]

QUIZ = mix([
    dict(q='How do you start decommissioning a DataNode?', options=['Stop the DataNode process', 'Add it to the dfs.hosts.exclude file and run hdfs dfsadmin -refreshNodes', 'Run hdfs fsck -delete', 'Run the balancer'], answer=1,
         why='Real: echo 172.19.0.7 &gt; dfs.exclude; refreshNodes → Decommission in progress.'),
    dict(q='Can a decommissioning node still serve reads?', options=['No, it is shut down immediately', 'Yes, until it is Decommissioned and stopped', 'Only for small files', 'Only for the NameNode'], answer=1,
         why='Its replicas are used as sources for copying and can serve reads.'),
    dict(q='Why not simply switch a DataNode off to retire it?', options=['It is not allowed', 'HDFS waits until it is declared dead (about 10.5 minutes) before re-replicating; meanwhile blocks have fewer replicas', 'It deletes all files', 'The balancer stops working'], answer=1,
         why='Decommissioning copies first; a sudden stop is treated as a failure.'),
    dict(q='What does the balancer threshold mean?', options=['Maximum number of blocks to move', 'Allowed difference, in % of capacity, between each node and the cluster average', 'Network speed', 'Minimum replication'], answer=1,
         why='The tool\'s own help: “Percentage of disk capacity”; range 1.0 to 100.0.'),
    dict(q='The balancer moved a block from dn-4 to dn-6. What happens to the replication factor?', options=['It increases to 4', 'It stays the same: copy to the target, then delete the source replica', 'It drops to 2', 'It becomes 1'], answer=1,
         why='Balancing never changes how many replicas a block has.'),
    dict(q='What does hdfs fsck do by default?', options=['Repairs corrupt blocks', 'Reports file and block health from NameNode metadata, without changing anything', 'Formats DataNodes', 'Restarts the NameNode'], answer=1,
         why='Only -move and -delete change files.'),
    dict(q='The lab balancer printed “No block has been moved for 5 iterations. Exiting...”. Why?', options=['The cluster was balanced', 'Moves kept failing (target out of space), so it gave up after 5 idle iterations', 'The NameNode crashed', 'The threshold was too high'], answer=1,
         why='“Out of space” on the 1.5 GB disk; max idle iteration = 5.'),
    dict(q='Which command changes the balancer speed on all DataNodes without a restart?', options=['hdfs dfsadmin -setBalancerBandwidth', 'hdfs balancer -speed', 'hdfs dfs -setrep', 'hdfs dfsadmin -refreshNodes'], answer=0,
         why='Real: “Balancer bandwidth is set to 52428800” (50 MB/s).'),
])

REVISION = [
    '<code>hdfs dfsadmin -report</code>: capacity, dead nodes, missing / under-replicated blocks, per-node status.',
    '<code>hdfs fsck path -files -blocks -locations -racks</code>: health from metadata; read-only by default.',
    'Decommission: host in <code>dfs.hosts.exclude</code> → <code>-refreshNodes</code> → <i>Decommission in progress</i> → <i>Decommissioned</i> → stop. Lab: 52 s and 60 s.',
    'Recommission: remove from the exclude file + refresh; excess replicas are deleted, so the node may come back empty.',
    'New nodes are not filled automatically: run <code>hdfs balancer [-threshold 10]</code>.',
    'Balanced = every node within threshold % (of capacity) of the average; range 1 to 100.',
    'Lab balancer: 8 blocks, 914.72 MB in 16 s; then “Out of space” and exit after 5 idle iterations.',
    'Bandwidth: 100 MB/s per node by default; change live with <code>-setBalancerBandwidth</code>.',
]
FAQ = [
    ('What is DataNode decommissioning in HDFS?', 'The safe way to remove a DataNode. You list it in the exclude file (dfs.hosts.exclude) and run hdfs dfsadmin -refreshNodes. The NameNode copies all its block replicas to other nodes while it keeps serving reads. When every block has enough replicas elsewhere, its status becomes Decommissioned and it can be shut down.'),
    ('How do you add a new DataNode to a running cluster?', 'Install Hadoop with the cluster\'s configuration on the new machine and start the DataNode; it registers with the NameNode on its own. If an include file (dfs.hosts) is used, add it there and run -refreshNodes. Then run the balancer so existing data spreads onto it.'),
    ('What does the HDFS balancer do?', 'It moves block replicas from DataNodes whose utilisation is above the cluster average to those below it, until every node is within the threshold (default 10%) of the average. Each move copies the block to the target and then removes one source replica, respecting rack placement, so replication is unchanged.'),
    ('Is it safe to stop the balancer in the middle?', 'Yes. Each block move is complete or not done at all; stopping the balancer leaves the cluster partly balanced but fully consistent. You can rerun it later.'),
    ('What is the difference between fsck in Linux and hdfs fsck?', 'Linux fsck checks and repairs a local file system\'s structures. hdfs fsck reports HDFS health from the NameNode: missing, corrupt and under-replicated blocks per file. It does not repair; HDFS repairs replicas itself, and -move or -delete only deal with files that have lost all good replicas.'),
    ('Why is a decommission stuck in progress?', 'Usually some blocks cannot get new replicas: not enough nodes or racks for the placement policy, full disks, a failing target node, or files still open for writing. The NameNode log shows lines like “still has 1 blocks to replicate”, and hdfs fsck or -report -decommissioning help find them.'),
]

PRACTICE_INTRO = 'Admin exercises using real reports, logs and timings from the lab.'
PROBLEMS = [
    dict(level='easy', title='Read the report', stmt='From the real report lines, how much of the configured capacity is used by HDFS, in %?', inp='Configured Capacity 1352765870080 · DFS Used 3037733930',
         code='''print(f"{100 * 3037733930 / 1352765870080:.2f}%")
''', explain='0.22% of configured capacity. The report printed 3.28% because DFS Used% is relative to Present Capacity (86.37 GB), not the 1.23 TB configured.'),
    dict(level='easy', title='Decommission duration', stmt='The real watcher printed status at t = 2, 8, 14, 20, 28, 34, 40, 46 s (in progress) and 52 s (Decommissioned). How many checks were in progress, and what was the average gap between checks?', inp='2 8 14 20 28 34 40 46 52',
         code='''t = [2, 8, 14, 20, 28, 34, 40, 46, 52]
gaps = [b - a for a, b in zip(t, t[1:])]
print("in progress:", len(t) - 1, " average gap:", sum(gaps) / len(gaps), "s")
''', explain='8 checks in progress, one every 6.25 s on average (sleep plus the time each -report takes), then Decommissioned at 52 s.'),
    dict(level='easy', title='Bandwidth in MB/s', stmt='Convert the real <code>-setBalancerBandwidth 52428800</code> and the default 104857600 to MB/s.', inp='52428800 · 104857600 bytes/s',
         code='''for b in [52428800, 104857600]:
    print(b, "=", b / 1024 / 1024, "MB/s")
''', explain='50 MB/s and 100 MB/s per DataNode.'),
    dict(level='medium', title='Parse balancer moves', stmt='From real “Successfully moved” lines, total the bytes moved and count moves per source.', inp='three log lines',
         code='''from collections import Counter
lines = ["Successfully moved blk_1073741846_1022 with size=19627626 from 172.19.0.4 to 172.19.0.9",
         "Successfully moved blk_1073741860_1038 with size=134217728 from 172.19.0.7 to 172.19.0.9",
         "Successfully moved blk_1073741844_1020 with size=134217728 from 172.19.0.4 to 172.19.0.9"]
total, src = 0, Counter()
for l in lines:
    w = l.split()
    total += int(w[4].split("=")[1]); src[w[6]] += 1
print(total / 1024 / 1024, "MB", dict(src))
''', explain='About 274.7 MB from 3 moves; 172.19.0.4 was the source twice. On all 8 lines this gives the 914.72 MB the balancer printed.'),
    dict(level='medium', title='Over or under?', stmt='Classify nodes like the balancer: over-utilised (&gt; avg + t), above average, below average, under-utilised (&lt; avg − t), with t = 10.', inp='utilisations 92, 81, 70, 64, 12 %',
         code='''util = {"dn-1": 92, "dn-2": 81, "dn-3": 70, "dn-4": 64, "dn-6": 12}
avg, t = sum(util.values()) / len(util), 10
for n, u in util.items():
    kind = "over" if u > avg + t else "above" if u > avg else "under" if u < avg - t else "below"
    print(n, u, kind)
print("average", avg)
''', explain='Average 63.8%: dn-1 and dn-2 over-utilised, dn-3 and dn-4 above average, dn-6 under-utilised. The balancer pairs over with under first, as the real log shows (“overUtilized =&gt; underUtilized”).'),
    dict(level='medium', title='Safe to stop two nodes?', stmt='Given replica locations, can dn-2 and dn-5 be stopped at the same time without making any block unavailable?', inp='block → nodes',
         code='''blocks = {"A": {"dn-2", "dn-4", "dn-5"}, "B": {"dn-2", "dn-5", "dn-3"}, "C": {"dn-1", "dn-2", "dn-3"}}
stop = {"dn-2", "dn-5"}
for b, nodes in blocks.items():
    left = nodes - stop
    print(b, "live replicas left:", len(left), "" if left else "<- UNAVAILABLE")
''', explain='All keep at least 1 replica, but A and B drop to 1: one more failure loses them. Decommission instead, or stop one at a time.'),
    dict(level='business', title='Cost of an empty new rack', stmt='A new rack of 20 nodes (Rs 4.5 lakh each) is added but the balancer is never run; for 6 months it holds only 5% of data while old nodes run near full and jobs slow down. What is the investment sitting mostly idle?', inp='20 × Rs 4.5 lakh · 5% used',
         code='''cost = 20 * 4.5
print(f"Rs {cost:.0f} lakh of hardware, about Rs {cost * 0.95:.1f} lakh of it unused")
''', explain='Rs 90 lakh of servers, about Rs 85.5 lakh worth idle (illustrative). A balancer run on day one puts it to work.'),
    dict(level='advanced', title='Decommission planner', stmt='Simulate decommissioning dn-4: for each of its blocks choose a target node that does not already hold the block, prefers keeping replicas on 2 racks, and has the most free space. Print the plan.', inp='4 blocks · 2 racks · free space per node',
         code='''rack = {"dn-1": 1, "dn-2": 1, "dn-3": 2, "dn-4": 2, "dn-5": 2}
free = {"dn-1": 50, "dn-2": 80, "dn-3": 30, "dn-5": 60}
blocks = {"A": ["dn-2", "dn-4", "dn-5"], "B": ["dn-4", "dn-1", "dn-3"], "D": ["dn-4", "dn-3", "dn-5"]}
for b, nodes in blocks.items():
    if "dn-4" not in nodes:
        continue
    keep = [n for n in nodes if n != "dn-4"]
    racks = {rack[n] for n in keep}
    cands = [n for n in free if n not in keep]
    if len(racks) == 1:                       # all others on one rack: need the other rack
        cands = [n for n in cands if rack[n] not in racks]
    target = max(cands, key=free.get)
    free[target] -= 1
    print(b, "copy to", target, "racks", sorted(racks | {rack[target]}))
''', explain='A goes to dn-1 (dn-2 and dn-5 already span both racks, so the most free space wins after dn-2 is excluded). B goes to dn-2. D (left only on rack 2) must go to rack 1: dn-2. Real NameNodes apply the same ideas with more rules.'),
]

SCN_INTRO = 'Admin questions separate people who have run a cluster from people who have only read about one.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · operations</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“How do you remove a DataNode from a cluster?”</h4>
      <p class="scn__situation">The classic commissioning and decommissioning question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> exclude file, refreshNodes, waiting for completion.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Add the host to the file named by <code>dfs.hosts.exclude</code>, run <code>hdfs dfsadmin -refreshNodes</code>.</li>
          <li>Watch <code>-report</code> until the status is <i>Decommissioned</i>; the NameNode copies all its blocks meanwhile. Then stop the DataNode and remove it.</li>
          <li>Confirm with <code>hdfs fsck /</code>: HEALTHY, 0 under-replicated. Never just switch it off.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · capacity</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>New nodes added last month are almost empty</h4>
      <p class="scn__situation">Old DataNodes are at 92% and jobs fail with disk-full errors, while 10 new nodes are at 8%.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that HDFS never rebalances existing data on its own.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Only new writes land on new nodes; existing blocks stay put. Run <code>hdfs balancer -threshold 10</code> (or lower).</li>
          <li>Run it off-peak, raise <code>-setBalancerBandwidth</code> at night, and repeat until balanced.</li>
          <li>Short term, free space on the full nodes (old temp data, trash) so jobs stop failing.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Troubleshooting</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Decommission has been “in progress” for a day</h4>
      <p class="scn__situation">The NameNode log repeats “still has 1 blocks to replicate”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> placement constraints and stuck blocks.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Find the block in the log (BlockStateChange lines show its replicas) and its file with <code>hdfs fsck</code>.</li>
          <li>Typical causes: no node/rack where a replica may go (small cluster, whole rack being retired), full or failing target disks, a file still open for writing, or replication higher than the node count.</li>
          <li>Fix the cause: add capacity, close or recover the file, lower its replication; in our lab a broken target node kept failing until its pending copy timed out (5 minutes) and another node was chosen.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · health</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“What does hdfs fsck tell you?”</h4>
      <p class="scn__situation">A quick check of whether you know what fsck reads and changes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> read-only report vs repair.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>For a path: files, blocks, replicas (with <code>-files -blocks -locations -racks</code>), and totals of missing, corrupt, under- and over-replicated blocks; status HEALTHY or CORRUPT.</li>
          <li>It reads NameNode metadata only and changes nothing unless you pass <code>-move</code> or <code>-delete</code>.</li>
          <li>HDFS repairs under-replicated blocks itself; fsck tells you whether anything is beyond repair.</li>
        </ul>
      </div></details>
    </article>
'''
