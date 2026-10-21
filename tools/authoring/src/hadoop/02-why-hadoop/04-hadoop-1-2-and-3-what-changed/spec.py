import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='The failures Hadoop 1 could not survive',
    intro='<p>This cluster has two NameNodes (Hadoop 2 HA) and runs jobs through the ResourceManager. In Hadoop 1, losing the only NameNode stopped the whole file system.</p>',
    racks=2, nodes=3, features=['job', 'ha', 'fail', 'fsck'],
    preload=[dict(name='sales_2026_q1.csv', sizeMB=1024)],
    **{'try': [
        dict(text='Run the job. The ResourceManager hands out containers for the 8 map tasks.', on='job-done'),
        dict(text='Press <b>Stop active NameNode</b>. ZooKeeper notices and the standby becomes active.', on='nn-failover'),
        dict(text='Run <b>hdfs fsck /</b> and the job again: the file system is still there.', on='fsck'),
        dict(text='Now stop the new active NameNode too. With no standby left, HDFS is unavailable: why Hadoop 3 allows more than one standby.', on='nn-stop'),
    ]},
)))

META = dict(
    module='02-why-hadoop', lesson='04-hadoop-1-2-and-3-what-changed', n='2.4',
    module_label='Module 2 · Why Hadoop was born',
    title='Hadoop 1, 2 and 3: what changed',
    desc='Hadoop 1 vs 2 vs 3: JobTracker and TaskTracker slots vs YARN ResourceManager, NodeManagers, ApplicationMasters and containers; NameNode HA and federation in Hadoop 2; erasure coding, multiple standby NameNodes, new ports (9870), Java 8+ and GPUs in Hadoop 3; releases up to 3.5.0. With animations, a playground, Python calculators, quiz and interview scenarios.',
    og_desc='JobTracker to YARN, one NameNode to many, 3× replication to erasure coding: what each Hadoop generation fixed.',
    minutes=25, level='Beginner → Advanced',
    lead='Hadoop kept its core ideas but changed its architecture twice. Hadoop 1 had one JobTracker doing everything and fixed slots that wasted resources. Hadoop 2 introduced YARN and a standby NameNode, so many engines could share a bigger, safer cluster. Hadoop 3 added erasure coding, extra standbys, GPU scheduling and newer Java. This lesson explains each change, why it was needed, and the details (like ports) that trip people up in real work.',
    chips=['1 vs 2 vs 3 table', 'Cluster Playground (HA)', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Slots vs containers: measure the waste',
    intro='<p>In Hadoop 1, each node has fixed map slots and reduce slots. This program fills them with a map-heavy workload and measures how much of the cluster is idle, then does the same with YARN-style containers that can run either kind of task.</p>',
    code='''nodes = 10
map_slots, reduce_slots = 8, 4          # Hadoop 1: fixed per node
containers = map_slots + reduce_slots    # Hadoop 2: same capacity, any task type

maps_waiting, reduces_waiting = 200, 10

h1_used = min(maps_waiting, nodes * map_slots) + min(reduces_waiting, nodes * reduce_slots)
h2_used = min(maps_waiting + reduces_waiting, nodes * containers)

total = nodes * containers
print(f"Hadoop 1: {h1_used} of {total} busy ({h1_used / total:.0%})")
print(f"Hadoop 2: {h2_used} of {total} busy ({h2_used / total:.0%})")
''',
    anno=[
        ('map_slots, reduce_slots = 8, 4', 'In Hadoop 1, an admin fixed these numbers per node. A reduce slot could never run a map task.'),
        ('h1_used = min(...) + min(...)', 'Map tasks can only use map slots and reduce tasks only reduce slots, so each is capped separately.'),
        ('h2_used = min(maps_waiting + reduces_waiting, nodes * containers)', 'With containers, any waiting task can use any free capacity.'),
    ],
    tasks=[
        dict(label='1 · Slot waste', hint='Press <b>Run</b>. Then try a reduce-heavy moment: <code>maps_waiting, reduces_waiting = 5, 120</code>.', code=None),
        dict(label='2 · JobTracker load', hint='<b>Predict first:</b> how many heartbeats per second does one JobTracker handle at 4,000 nodes? Then imagine 10,000 nodes.',
             code='''hb_interval_s = 3
for nodes in [500, 4000, 10000]:
    print(f"{nodes:>6} nodes -> {nodes / hb_interval_s:,.0f} heartbeats/s to ONE JobTracker")
'''),
        dict(label='3 · Replication vs erasure coding', hint='Compare raw storage and how many lost pieces each scheme survives for 600 TB of data.',
             code='''data_tb = 600
schemes = {"replication x3": (3.0, 2), "EC RS-6-3": (9 / 6, 3), "EC RS-10-4": (14 / 10, 4)}
for name, (overhead, survives) in schemes.items():
    print(f"{name:15}: {data_tb * overhead:6.0f} TB raw, survives {survives} lost pieces")
'''),
        dict(label='4 · Old port, new port', hint='A Hadoop 2 guide says to open these ports. Translate them for Hadoop 3. Add 50475 → 9865 (DataNode HTTPS).',
             code='''h2_to_h3 = {50070: 9870, 50470: 9871, 50090: 9868, 50010: 9866, 50020: 9867, 50075: 9864}
old_guide = [50070, 50075, 8088]
for p in old_guide:
    print(p, "->", h2_to_h3.get(p, p), "" if p in h2_to_h3 else "(unchanged)")
'''),
        dict(label='5 · Which version?', hint='Classify features by the Hadoop generation that introduced them. Then add "Docker containers on YARN": 3.',
             code='''introduced = {"JobTracker": 1, "YARN": 2, "NameNode HA": 2, "Federation": 2,
              "Erasure coding": 3, "Multiple standby NameNodes": 3, "GPU scheduling": 3}
by_version = {}
for feature, v in introduced.items():
    by_version.setdefault(v, []).append(feature)
for v in sorted(by_version):
    print(f"Hadoop {v}:", ", ".join(by_version[v]))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Placing tasks in slots vs containers, one line at a time',
    intro='<p>Watch the same five tasks being placed on one node, first with Hadoop 1 slots (2 map + 2 reduce) and then with 4 YARN containers. Notice which tasks are left waiting.</p>',
    code='''tasks = ["map", "map", "map", "map", "reduce"]

slots = {"map": 2, "reduce": 2}
waiting_h1 = []
for t in tasks:
    if slots[t] > 0:
        slots[t] -= 1
    else:
        waiting_h1.append(t)

free_containers = 4
waiting_h2 = tasks[free_containers:]
print("Hadoop 1 waiting:", waiting_h1, "| Hadoop 2 waiting:", waiting_h2)
''',
    notes={3: 'Hadoop 1 :: Fixed slots per task type.', 11: 'Hadoop 2 :: Any task can use any container.'},
)

WORKED_INTRO = 'Three problems from real version decisions: an upgrade checklist, the storage savings of Hadoop 3, and how many NameNodes a cluster needs. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Upgrade · planning', title='What must change when moving a cluster from Hadoop 2 to 3?',
         problem='<p>A team lists its current setup. Print an upgrade checklist: flag Java older than 8, any monitoring that uses old Hadoop 2 ports, and any job still using the Hadoop 1 JobTracker API.</p>',
         inp='java 7 · monitored ports [50070, 8088, 50075] · jobs [("daily_sales", "mapred"), ("fraud", "mapreduce")]',
         approach=['Check the Java version number.',
                   'Look up each monitored port in the old → new port map.',
                   'Old-API jobs (package <code>org.apache.hadoop.mapred</code>) still run, but should be reviewed.'],
         code='''java = 7
ports = [50070, 8088, 50075]
jobs = [("daily_sales", "mapred"), ("fraud", "mapreduce")]
new_port = {50070: 9870, 50075: 9864, 50010: 9866, 50090: 9868}

if java < 8:
    print("Upgrade Java: Hadoop 3 needs Java 8 or later")
for p in ports:
    if p in new_port:
        print(f"Monitoring: change port {p} to {new_port[p]}")
for name, api in jobs:
    if api == "mapred":
        print(f"Review job '{name}': uses the old mapred API")
''', notes={5: 'Map :: The Hadoop 2 → 3 port changes from Part 3.'},
         tryit='Add port 50010 to the monitored list and Java 11. Which lines disappear?'),
    dict(level='i', tag='Storage · Hadoop 3', title='How much disk does erasure coding free up?',
         problem='<p>A cluster stores <b>1.2 PB</b> of business data, all with 3× replication. The team moves the <b>70%</b> that is older than a year to the RS-6-3 erasure-coding policy. How much raw storage is freed, and how many 144 TB nodes is that?</p>',
         inp='1.2 PB · 70% cold · 3× → 1.5× · 144 TB per node',
         approach=['Before: 1,200 TB × 3.',
                   'After: hot 30% × 3 + cold 70% × 1.5.',
                   'Freed raw TB ÷ 144 = nodes no longer needed.'],
         code='''import math
data_tb = 1200
cold = 0.70
before = data_tb * 3
after = data_tb * (1 - cold) * 3 + data_tb * cold * 1.5
freed = before - after
print(f"Before: {before:.0f} TB raw, after: {after:.0f} TB raw")
print(f"Freed: {freed:.0f} TB = about {math.floor(freed / 144)} nodes")
''', notes={5: 'Mix :: Hot data stays replicated; cold data uses 6 data + 3 parity cells.'},
         tryit='Erasure-coded files are slower to read when a node is down (data must be rebuilt). What share would you keep replicated for a reporting cluster?'),
    dict(level='a', tag='High availability · design', title='How many NameNodes and JournalNodes for a given safety level?',
         problem='<p>JournalNodes work by majority: with <i>J</i> JournalNodes the cluster tolerates <i>(J − 1) ÷ 2</i> JournalNode failures. With <i>N</i> NameNodes (one active), it tolerates <i>N − 1</i> NameNode failures. For each target, print the smallest setup that survives that many failures of each kind.</p>',
         inp='targets: survive 1 failure (Hadoop 2 style) and 2 failures (Hadoop 3 style)',
         approach=['NameNodes needed = failures + 1.',
                   'JournalNodes needed = 2 × failures + 1 (an odd number, for a majority).',
                   'Hadoop 2 allowed at most 2 NameNodes; Hadoop 3 allows more.'],
         code='''def ha_setup(failures):
    namenodes = failures + 1
    journalnodes = 2 * failures + 1
    return namenodes, journalnodes

for f in [1, 2]:
    nn, jn = ha_setup(f)
    ok = "Hadoop 2 or 3" if nn <= 2 else "Hadoop 3 only"
    print(f"Survive {f}: {nn} NameNodes + {jn} JournalNodes ({ok})")
''', notes={1: 'Rule :: A majority of JournalNodes must be alive to accept edits.'},
         tryit='Why must the number of JournalNodes be odd? Try 4: how many failures can it survive? (Still 1, so the fourth adds cost but no safety.)'),
]

QUIZ = mix([
    dict(q='In Hadoop 1, which daemon handled both resource management and job scheduling?', options=['ResourceManager', 'JobTracker', 'ApplicationMaster', 'NodeManager'], answer=1,
         why='The <b>JobTracker</b> did both, which made it a bottleneck and a single point of failure.'),
    dict(q='What replaced fixed map and reduce slots in Hadoop 2?', options=['Threads', 'YARN containers that any task type can use', 'Bigger blocks', 'More JobTrackers'], answer=1,
         why='Containers are flexible amounts of memory and CPU, so no capacity is reserved for a task type that isn\'t running.'),
    dict(q='In YARN, which component manages the tasks of one particular job?', options=['ResourceManager', 'NodeManager', 'ApplicationMaster', 'NameNode'], answer=2,
         why='Each application has its own <b>ApplicationMaster</b>; the ResourceManager only allocates resources.'),
    dict(q='Which Hadoop 2 feature removed the NameNode as a single point of failure?', options=['Federation', 'High Availability with an active and a standby NameNode', 'Erasure coding', 'Secondary NameNode'], answer=1,
         why='<b>HDFS HA</b> keeps a standby NameNode in sync via JournalNodes and fails over automatically. The Secondary NameNode only checkpoints.'),
    dict(q='Which feature is new in Hadoop 3?', options=['YARN', 'HDFS erasure coding', 'MapReduce', 'HDFS replication'], answer=1,
         why='Erasure coding arrived in Hadoop 3.0, cutting storage overhead to about 1.5× for suitable data.'),
    dict(q='On Hadoop 3, the NameNode web UI is by default on port:', options=['50070', '8088', '9870', '8020'], answer=2,
         why='Hadoop 3 moved it from 50070 to <b>9870</b>. 8088 is the ResourceManager UI; 8020 is the NameNode RPC port.'),
    dict(q='What is the minimum Java version for Hadoop 3?', options=['Java 6', 'Java 7', 'Java 8', 'Java 17'], answer=2,
         why='Hadoop 3.0 raised the minimum from Java 7 to <b>Java 8</b>. Later 3.x lines also support newer runtimes; check each release\'s notes.'),
    dict(q='What does HDFS Federation do?', options=['Copies data to another country', 'Lets several independent NameNodes each manage part of the namespace, sharing the DataNodes', 'Encrypts all blocks', 'Merges YARN and HDFS'], answer=1,
         why='Federation scales the namespace beyond one NameNode\'s memory, for example one NameNode for <code>/user</code> and another for <code>/data</code>.'),
])

REVISION = [
    '<b>Hadoop 1</b> (2011): JobTracker + TaskTrackers, fixed map/reduce <b>slots</b>, MapReduce only, single NameNode, ~4,000 nodes.',
    '<b>Hadoop 2</b> (GA Oct 2013): <b>YARN</b> = ResourceManager + NodeManagers + one ApplicationMaster per job; <b>containers</b>.',
    'Hadoop 2 also: <b>NameNode HA</b> (active + standby, JournalNodes, ZooKeeper failover), <b>Federation</b>, 128 MB blocks.',
    'Many engines on one cluster: MapReduce, Spark, Tez, Flink.',
    '<b>Hadoop 3</b> (GA Dec 2017): <b>erasure coding</b> (RS-6-3 ≈ 1.5×), <b>2+ standby NameNodes</b>, Java 8+, new ports.',
    'Hadoop 3 YARN: Timeline v2, opportunistic containers, GPUs/FPGAs (3.1), Docker; Router-based Federation.',
    'Ports: NameNode UI 50070 → <b>9870</b>; DataNode 50010 → 9866, 50075 → 9864; Secondary 50090 → 9868; RM UI 8088 unchanged.',
    'Recent: 3.3 (2020, Java 11 runtime, ARM), 3.4.0 (2024), <b>3.5.0 (Apr 2026, servers need JDK 17)</b>.',
]
FAQ = [
    ('What are the differences between Hadoop 1 and Hadoop 2?', 'Hadoop 1 used a single JobTracker for both resource management and job scheduling, with TaskTrackers offering fixed map and reduce slots, ran only MapReduce, had a single NameNode (a SPOF) and scaled to about 4,000 nodes. Hadoop 2 introduced YARN: a ResourceManager for cluster resources, NodeManagers on each node, and an ApplicationMaster per job, using flexible containers. It supports engines beyond MapReduce, adds NameNode High Availability and HDFS Federation, scales further and uses a 128 MB default block size.'),
    ('What new features came in Hadoop 3?', 'HDFS erasure coding (about 1.5× storage overhead instead of 3× for suitable data), support for more than two NameNodes, a minimum of Java 8, default ports moved out of the ephemeral range (NameNode UI on 9870), a rewritten shell, YARN Timeline Service v2, opportunistic containers, resource types such as GPUs and FPGAs (3.1), Docker container support, Router-based Federation, an intra-DataNode disk balancer and much improved cloud storage connectors.'),
    ('Why was the JobTracker a bottleneck?', 'It received heartbeats from every TaskTracker, scheduled every task of every job, tracked their progress and counters, and kept job history in memory. As clusters and job counts grew, one process could not keep up, and if it failed all running jobs were lost.'),
    ('Is the Secondary NameNode a backup NameNode?', 'No. It periodically merges the NameNode\'s edit log into the fsimage (checkpointing) so the edit log does not grow forever and restarts are faster. It cannot take over if the NameNode fails. Automatic failover requires HA with a standby NameNode.'),
    ('What is the difference between replication and erasure coding?', 'Replication stores full copies of each block (3× storage) and reads are simple and fast. Erasure coding splits data into data cells and computes parity cells (for example 6 + 3); any 6 of the 9 cells can rebuild the data. It needs about 1.5× storage but costs CPU and network to encode and rebuild, so it is best for cold, large files.'),
]

PRACTICE_INTRO = 'Questions that test version knowledge with small programs: slots, ports, storage schemes and HA sizing.'
PROBLEMS = [
    dict(level='easy', title='Total slots in Hadoop 1', stmt='A Hadoop 1 cluster has 50 nodes with 6 map and 3 reduce slots each. How many map and reduce slots in total?', inp='50 nodes · 6 map + 3 reduce',
         code='print("map:", 50 * 6, "| reduce:", 50 * 3)\n', explain='300 map and 150 reduce slots. If no reduce tasks are running, those 150 slots do nothing.'),
    dict(level='easy', title='Erasure coding overhead', stmt='Print the storage overhead of RS-6-3 and RS-3-2 erasure coding.', inp='RS-6-3 · RS-3-2',
         code='''for d, p in [(6, 3), (3, 2)]:
    print(f"RS-{d}-{p}: {(d + p) / d:.2f}x")
''', explain='1.50× and 1.67×. Both are well below the 3× of replication; RS-6-3 is the default policy.'),
    dict(level='easy', title='Port lookup', stmt='Write code that prints the Hadoop 3 port for the NameNode web UI, given a dictionary of services.', inp='{"namenode-ui": 9870, "rm-ui": 8088, "datanode-ui": 9864}',
         code='''ports = {"namenode-ui": 9870, "rm-ui": 8088, "datanode-ui": 9864}
print("Open http://localhost:" + str(ports["namenode-ui"]))
''', explain='On a fresh Hadoop 3 install, the NameNode UI is at http://localhost:9870 and YARN at http://localhost:8088.'),
    dict(level='medium', title='Idle slots during a map phase', stmt='A Hadoop 1 cluster has 400 map slots and 200 reduce slots. 1,000 maps are waiting and no reduces. What percentage of all slots is idle? What would it be with 600 general containers?', inp='400 map + 200 reduce slots · 1000 maps waiting',
         code='''total = 400 + 200
used_h1 = min(1000, 400)
used_h2 = min(1000, total)
print(f"Hadoop 1 idle: {(total - used_h1) / total:.0%}")
print(f"Hadoop 2 idle: {(total - used_h2) / total:.0%}")
''', explain='A third of the cluster idles in Hadoop 1 while maps queue up; YARN uses it all.'),
    dict(level='medium', title='Survivable JournalNode failures', stmt='For 3, 4, 5 and 7 JournalNodes, print how many failures a majority-based system survives.', inp='[3, 4, 5, 7]',
         code='''for j in [3, 4, 5, 7]:
    print(j, "JournalNodes survive", (j - 1) // 2, "failure(s)")
''', explain='3 → 1, 4 → 1, 5 → 2, 7 → 3. Even numbers add cost but no extra safety, which is why JournalNodes come in odd numbers.'),
    dict(level='medium', title='Map features to versions', stmt='Given a list of features, print the ones that would NOT exist on a Hadoop 2 cluster.', inp='["YARN", "erasure coding", "NameNode HA", "GPU scheduling", "Federation"]',
         code='''hadoop3_only = {"erasure coding", "GPU scheduling", "multiple standby NameNodes"}
features = ["YARN", "erasure coding", "NameNode HA", "GPU scheduling", "Federation"]
print([f for f in features if f in hadoop3_only])
''', explain='Erasure coding and GPU scheduling need Hadoop 3. YARN, HA and Federation arrived in Hadoop 2.'),
    dict(level='business', title='Should we upgrade to Hadoop 3 for storage savings?', stmt='A 2 PB cluster (raw) is full. 60% of the stored data is cold. Switching cold data from 3× replication to 1.5× erasure coding frees raw disk. The alternative is buying new nodes of 144 TB at Rs 18 lakh each. How much hardware spending does the upgrade avoid?', inp='2,048 TB raw · 60% cold · node 144 TB = Rs 18 lakh',
         code='''import math
raw = 2048
data = raw / 3
cold = data * 0.60
freed = cold * 3 - cold * 1.5
nodes = math.floor(freed / 144)
print(f"Freed {freed:.0f} TB raw = {nodes} nodes = Rs {nodes * 18} lakh avoided")
''', explain='About 614 TB freed, 4 nodes (Rs 72 lakh) not bought, using illustrative prices. Weigh it against upgrade effort and the CPU cost of erasure coding.'),
    dict(level='business', title='Consolidate separate MapReduce and Spark clusters', stmt='A company runs a 40-node Hadoop 1 cluster for MapReduce and a separate 30-node cluster for Spark. Peak usage is 30 nodes and 20 nodes, at different times of day. With one YARN cluster, the worst-case need is the larger peak plus a quiet share of 6 nodes from the other, plus 20% spare. How many nodes are needed?', inp='peaks 30 and 20 at different times · quiet share 6 · +20%',
         code='''import math
need = max(30, 20) + 6
print("Nodes needed:", math.ceil(need * 1.2), "instead of", 40 + 30)
''', explain='44 instead of 70 nodes. Sharing one cluster across engines was a major business reason for YARN.'),
]

SCN_INTRO = 'Version questions show up in almost every Hadoop interview. These scenarios turn the comparison table into practical answers.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Explain the difference between Hadoop 1 and 2 in two minutes.”</h4>
      <p class="scn__situation">The classic question. The interviewer wants the main differences and the reason behind them.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know <i>why</i> YARN exists, not just its name?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Problem:</b> in Hadoop 1, one JobTracker did resource management <i>and</i> scheduled every task of every job. It limited clusters to about 4,000 nodes, was a single point of failure, used fixed map/reduce slots (wasting capacity) and could only run MapReduce.</li>
          <li><b>Fix (Hadoop 2):</b> YARN split it: the ResourceManager manages resources; each job has its own ApplicationMaster; NodeManagers run flexible containers. Result: bigger clusters, better utilisation, and Spark, Tez and others on the same cluster.</li>
          <li><b>Also in Hadoop 2:</b> NameNode HA (active + standby) and Federation.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> saying “Hadoop 2 removed MapReduce”. MapReduce still exists; it runs as a YARN application.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“The NameNode web page won't open”</h4>
      <p class="scn__situation">A colleague installed Hadoop 3.4 from a tutorial and says HDFS is running, but <code>http://localhost:50070</code> shows “connection refused”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know the practical version differences?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Hadoop 3 moved the NameNode UI to <b>9870</b>. Try <code>http://localhost:9870</code>.</li>
          <li>Confirm with <code>jps</code> that the NameNode process is running, and check <code>dfs.namenode.http-address</code> in <code>hdfs-site.xml</code>.</li>
          <li>The tutorial was probably written for Hadoop 2: double-check its other settings too (Java version, script names, ports for DataNodes).</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> reinstalling Hadoop before checking the port.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · upgrade</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Plan an upgrade from Hadoop 2.10 to 3.x</h4>
      <p class="scn__situation">Your company runs a 60-node Hadoop 2.10 cluster with Hive and Spark jobs. Management wants it on a current 3.x release with minimal downtime.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you think through compatibility and risk, not just “install the new version”?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li><b>Inventory:</b> Java version, every job and its libraries (Hive, Spark, custom jars), scripts using old shell behaviour, monitoring and firewalls using old ports.</li>
          <li><b>Compatibility:</b> pick a 3.x release supported by your Hive and Spark versions; upgrade Java first.</li>
          <li><b>Staging:</b> build a staging cluster on the target version and run real jobs on copies of data.</li>
          <li><b>Upgrade:</b> back up NameNode metadata, use an HA rolling upgrade for HDFS where supported, then YARN, keeping a rollback path until finalised.</li>
          <li><b>After:</b> update ports in monitoring, then consider Hadoop 3 features like erasure coding for cold data.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> upgrading production directly, or enabling erasure coding everywhere on day one.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Banking · availability</span><span class="scn__tag scn__tag--level">3+ years</span></div>
      <h4>Two NameNodes or three?</h4>
      <p class="scn__situation">A bank's HDFS cluster uses HA with two NameNodes. Last month, while the standby was down for patching, the active NameNode's server failed, and HDFS was unavailable for an hour.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know what Hadoop 3 added for availability and how quorums work?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>With two NameNodes, maintenance on one leaves no protection. Hadoop 3 supports <b>more than two NameNodes</b>: with one active and two standbys, one can be patched while another still protects the cluster.</li>
          <li>Pair it with <b>five JournalNodes</b> (a majority of 3 must be alive) to tolerate two JournalNode failures as well.</li>
          <li>Run the NameNodes on different racks and power feeds, and schedule maintenance one node at a time.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “Use the Secondary NameNode as a third backup.” It cannot take over.</p>
      </div></details>
    </article>'''
