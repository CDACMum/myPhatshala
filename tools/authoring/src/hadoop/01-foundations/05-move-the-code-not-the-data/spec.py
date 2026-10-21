import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{RECAP}}', recap('Its lesson <a href="../../../big-data-fundamentals/01-introduction/03-distributed-computing-basics/">Distributed computing basics</a> introduced “move the program, not the data” as a general idea. Here you will see exactly how Hadoop does it: block locations, node-local and rack-local tasks, and the counters that prove it.')).replace('{{PLAYGROUND}}', playground(dict(
    title='Locality on, locality off',
    intro='<p>A 2 GB file (16 blocks) is stored on 6 nodes. Green task bars are <b>node-local</b>, amber are <b>rack-local</b>, red are <b>off-rack</b>. Red packets are input blocks being pulled over the network.</p>',
    racks=2, nodes=3, features=['job', 'locality'], speed=2,
    preload=[dict(name='tiffingo_logs_week42.log', sizeMB=2048)],
    **{'try': [
        dict(text='Keep <b>Move code to data</b> ticked and run the job. Almost every bar is green.', on='job-done'),
        dict(text='Untick it and run again. Tasks land anywhere and pull their blocks over the network.', on='job-done-nolocal'),
        dict(text='Open <b>Job runs</b> and compare the network used and the time. Which resource did locality save?'),
    ]},
)))

META = dict(
    module='01-foundations', lesson='05-move-the-code-not-the-data', n='1.5',
    module_label='Module 1 · Foundations: before Hadoop',
    title='Move the code, not the data',
    desc='Data locality in Hadoop: why sending a small program to the data beats moving terabytes over the network, node-local, rack-local and off-rack tasks, delay scheduling, short-circuit reads, locality counters, and when locality is given up in the cloud. With animations, a locality on/off playground, Python you can run, quiz and interview scenarios.',
    og_desc='Programs are kilobytes, data is terabytes. See how Hadoop ships the small thing, and prove it with job counters.',
    minutes=24, level='Beginner → Advanced',
    lead='The single most important idea behind Hadoop fits in five words: move the code, not the data. This lesson shows why with real numbers (a day of copying versus minutes of processing), how Hadoop uses block locations to send each task to a node that already holds its data, what node-local, rack-local and off-rack mean, and how to check locality in a real job. Then switch locality off in the playground and watch the network fill up.',
    chips=['Cluster Playground', 'Runs in your browser (Python)', 'Locality counters'],
)

RUN = dict(
    heading='Move the data or move the code? Do the maths',
    intro='<p>Compare the time to bring all the data to one machine with the time to send a small program to every node and let each read its own share in parallel. Then try the challenges, including a tiny locality-aware scheduler.</p>',
    code='''data_tb = 10
nodes = 40
network_gbps = 10          # link into the single reporting server
local_read_gb_s = 1.0      # each node, many disks in parallel
jar_kb = 50

move_data_h = data_tb * 1024 * 8 / network_gbps / 3600
move_code_s = jar_kb * 8 / 1024 / 1024 / network_gbps
local_min = data_tb * 1024 / nodes / local_read_gb_s / 60

print(f"Move the data : {move_data_h:.1f} hours of transfer")
print(f"Move the code : {move_code_s:.5f} s to send the jar")
print(f"Then each node reads its share in {local_min:.1f} minutes")
''',
    anno=[
        ('move_data_h = data_tb * 1024 * 8 / network_gbps / 3600', 'TB → GB (× 1024), bytes → bits (× 8), ÷ link speed in Gbit/s = seconds, ÷ 3600 = hours.'),
        ('move_code_s = jar_kb * 8 / 1024 / 1024 / network_gbps', 'The same formula for a 50 KB jar: KB → Gbit is ÷ 1024 ÷ 1024 after × 8.'),
        ('local_min = data_tb * 1024 / nodes / local_read_gb_s / 60', 'Each node reads only its own 1/40th of the data, and all nodes read at the same time.'),
    ],
    tasks=[
        dict(label='1 · Data vs code', hint='Press <b>Run</b>. Then make the network 100 Gbps. Moving data is still far slower than reading locally in parallel. Try 400 nodes.', code=None),
        dict(label='2 · Pick a local node', hint='<b>Predict first:</b> which node does each task get? A task goes to the first free node holding its block, otherwise to any free node.',
             code='''blocks = {"T1": ["dn1", "dn4"], "T2": ["dn1", "dn2"], "T3": ["dn1", "dn5"]}
free = ["dn1", "dn2", "dn3"]

for task, holders in blocks.items():
    local = [n for n in holders if n in free]
    node = local[0] if local else free[0]
    free.remove(node)
    print(task, "->", node, "(local)" if local else "(remote)")
'''),
        dict(label='3 · Network distance', hint='Hadoop measures distance as 0 (same node), 2 (same rack), 4 (other rack). Find the closest replica for a task on dn3.',
             code='''rack = {"dn1": "r1", "dn2": "r1", "dn3": "r1", "dn4": "r2", "dn5": "r2"}

def distance(a, b):
    if a == b:
        return 0
    return 2 if rack[a] == rack[b] else 4

replicas = ["dn5", "dn2", "dn4"]
best = min(replicas, key=lambda r: distance("dn3", r))
print({r: distance("dn3", r) for r in replicas}, "-> read from", best)
'''),
        dict(label='4 · Locality report', hint='Turn a list of task placements into the counters Hadoop prints. What percentage were data-local?',
             code='''placements = ["node", "node", "rack", "node", "off", "node", "node", "rack"]
counters = {}
for p in placements:
    counters[p] = counters.get(p, 0) + 1
print(counters)
print(f"Data-local: {counters['node'] / len(placements):.0%}")
'''),
        dict(label='5 · How much is shuffled?', hint='Map tasks turn 128 MB of logs into a small count per city. Compare input size with what crosses the network in the shuffle.',
             code='''splits = 80000
input_mb = splits * 128
cities = 500
bytes_per_count = 20
shuffle_mb = splits * cities * bytes_per_count / 1024 / 1024

print(f"Input read locally : {input_mb / 1024 / 1024:.1f} TB")
print(f"Shuffled over net  : {shuffle_mb / 1024:.2f} GB")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='A locality-aware scheduler, one line at a time',
    intro='<p>Watch the scheduler give each task to a free node that holds its block, and fall back to any free node when none does. The <code>free</code> list shrinks as slots are used.</p>',
    code='''def schedule(tasks, free):
    plan = {}
    for task, holders in tasks.items():
        local = [n for n in holders if n in free]
        node = local[0] if local else free[0]
        free.remove(node)
        plan[task] = node
    return plan

tasks = {"M1": ["dn2", "dn5"], "M2": ["dn2", "dn3"], "M3": ["dn2"]}
print(schedule(tasks, ["dn2", "dn3", "dn4"]))
''',
    notes={10: 'Input :: Each map task with the nodes that hold its block.', (5, 3): 'M3 :: Its only holder, dn2, is already busy, so it gets a remote node.'},
)

WORKED_INTRO = 'Three locality problems from real cluster work: a transfer estimate, a scheduling decision, and a job report built from task placements. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Analytics · estimate', title='Copying 2 TB to a laptop for analysis',
         problem='<p>An analyst wants to copy <b>2 TB</b> of HDFS data to her laptop over the office Wi-Fi (about <b>200 Mbps</b> in practice) to analyse it in Python. How many hours will the copy take? Compare with a 1 Gbps wired link.</p>',
         inp='2 TB · 200 Mbps vs 1000 Mbps',
         approach=['Convert TB to megabits: × 1024 × 1024 × 8.',
                   'Divide by the link speed in Mbps to get seconds.',
                   'Print hours for both links.'],
         code='''data_mbit = 2 * 1024 * 1024 * 8
for name, mbps in [("Wi-Fi", 200), ("Wired 1 Gbps", 1000)]:
    hours = data_mbit / mbps / 3600
    print(f"{name:13}: {hours:.1f} hours")
''', notes={1: 'Units :: 2 TB = 1,67,77,216 megabits.'},
         tryit='The analysis itself is a group-by on one column. What should she do instead of copying? (Run a Hive or Spark query on the cluster and copy only the result.)'),
    dict(level='i', tag='YARN · scheduling', title='Place map tasks with locality first',
         problem='<p>Four map tasks are waiting. Each node has a number of free container slots. Give each task a slot on a node that holds its block if possible, otherwise any node with a free slot, and label each placement.</p>',
         inp='M1 [dn1, dn3] · M2 [dn1, dn2] · M3 [dn1] · M4 [dn4] · free slots dn1 2, dn2 1, dn3 1',
         approach=['For each task, list holders that still have a free slot.',
                   'Use the first one (node-local), or any node with slots (remote).',
                   'Reduce that node\'s free slots by one.'],
         code='''tasks = {"M1": ["dn1", "dn3"], "M2": ["dn1", "dn2"], "M3": ["dn1"], "M4": ["dn4"]}
slots = {"dn1": 2, "dn2": 1, "dn3": 1}

for task, holders in tasks.items():
    local = [n for n in holders if slots.get(n, 0) > 0]
    if local:
        node, kind = local[0], "node-local"
    else:
        node, kind = max(slots, key=slots.get), "remote"
    slots[node] -= 1
    print(task, "->", node, kind)
''', notes={2: 'Slots :: dn4 holds M4\'s block but has no free slot (not in the dictionary).'},
         tryit='Swap the order of M2 and M3. Does a different order give more local tasks? Real schedulers handle this with delay scheduling.'),
    dict(level='a', tag='Performance · job report', title='Turn task placements into locality counters and network cost',
         problem='<p>After a job, each map task\'s placement is known (node, rack or off) and every input block is 128 MB. Produce the job counters, the share of data-local tasks, and how many GB of input crossed the network (rack-local and off-rack only).</p>',
         inp='[node, node, rack, node, off, node, rack, node, node, off] · 128 MB per block',
         approach=['Count each kind with a dictionary.',
                   'Data-local share = node ÷ total.',
                   'Network GB = (rack + off) × 128 ÷ 1024.'],
         code='''placements = ["node", "node", "rack", "node", "off",
              "node", "rack", "node", "node", "off"]
count = {"node": 0, "rack": 0, "off": 0}
for p in placements:
    count[p] += 1
local_share = count["node"] / len(placements)
net_gb = (count["rack"] + count["off"]) * 128 / 1024
print("Data-local map tasks =", count["node"])
print("Rack-local map tasks =", count["rack"])
print("Off-rack map tasks   =", count["off"])
print(f"Data-local share: {local_share:.0%}, input over network: {net_gb} GB")
''', notes={3: 'Counters :: Start every counter at zero.'},
         tryit='A healthy cluster shows well over 90% data-local. What could cause 60%? (Cluster full, too few replicas, wrong rack script.)'),
]

QUIZ = mix([
    dict(q='What is data locality in Hadoop?', options=['Storing all data on the master', 'Running tasks on (or near) the nodes that hold their input data', 'Keeping data in one city', 'Compressing data before storage'], answer=1,
         why='Hadoop sends the computation to the data so that input is read from local disks instead of the network.'),
    dict(q='Why is moving the code cheaper than moving the data?', options=['Code runs faster than data', 'A job jar is KB–MB while input data is GB–TB, and the network is the scarcest resource', 'Data cannot be moved', 'Code is encrypted'], answer=1,
         why='Shipping kilobytes to many nodes is almost free; shipping terabytes to one place takes hours and jams the network.'),
    dict(q='A map task runs on a different node in the same rack as its block. This is:', options=['Node-local', 'Rack-local', 'Off-rack', 'Not allowed'], answer=1,
         why='<b>Rack-local</b>: the data crosses only the rack\'s ToR switch, not the core network.'),
    dict(q='Hadoop\'s network distance between two different nodes in the same rack is:', options=['0', '1', '2', '4'], answer=2,
         why='0 = same node, <b>2 = same rack</b>, 4 = another rack in the same data centre.'),
    dict(q='Which job counters show how well locality worked?', options=['Map input records and Map output records', 'Data-local map tasks and Rack-local map tasks', 'GC time elapsed', 'Bytes written'], answer=1,
         why='The Job Counters section lists <code>Data-local map tasks</code> and <code>Rack-local map tasks</code>.'),
    dict(q='How does replication factor 3 help data locality?', options=['It doesn\'t', 'Each block can be processed locally on any of 3 nodes, so a free local slot is more likely', 'It makes the jar smaller', 'It disables the shuffle'], answer=1,
         why='Three replicas mean three candidate nodes for a node-local task.'),
    dict(q='Which part of a MapReduce job cannot be made data-local?', options=['Reading input splits', 'The shuffle, where map outputs travel to reducers', 'Starting the task JVM', 'Writing map output to local disk'], answer=1,
         why='Reducers need outputs from many mappers, so the <b>shuffle</b> always uses the network. Combiners make it smaller.'),
    dict(q='Why do many cloud setups accept losing data locality?', options=['Cloud disks are faster than RAM', 'Data in object storage plus very fast networks allows elastic compute clusters that can be deleted after the job', 'Locality is illegal in the cloud', 'Cloud jobs have no input'], answer=1,
         why='Separating storage and compute trades some locality for elasticity and cost savings, made practical by fast cloud networks.'),
])

REVISION = [
    '<b>Move the code, not the data</b>: jars are KB, data is TB, the network is the bottleneck.',
    '<b>Data locality</b>: run each task on a node that holds a replica of its input block.',
    'Levels: <b>node-local</b> (distance 0) → <b>rack-local</b> (2) → <b>off-rack</b> (4).',
    'The job gets block locations from the NameNode; YARN tries to place containers on those hosts.',
    '<b>Delay scheduling</b>: wait briefly for a local slot before going remote.',
    '<b>Short-circuit reads</b>: a local task reads the block file straight from disk.',
    'Check counters: <code>Data-local map tasks</code>, <code>Rack-local map tasks</code>.',
    'The <b>shuffle</b> can\'t be local; combiners shrink it.',
    'Cloud object storage gives up locality for elasticity, relying on fast networks.',
]
FAQ = [
    ('What is data locality and why is it important in Hadoop?', 'Data locality means running computation on the node where the data is stored. In Hadoop, map tasks are scheduled on DataNodes that hold a replica of their input split. It matters because network bandwidth, especially between racks, is much more limited than the combined disk bandwidth of the cluster. Moving a small program to many nodes avoids moving terabytes of data.'),
    ('What are the levels of data locality?', 'Node-local (data-local): the task runs on a node with a replica. Rack-local: the task runs on another node in the same rack, reading over the rack switch. Off-rack: the task runs in a different rack, reading through the core network. The scheduler prefers them in that order.'),
    ('How does the scheduler know where the data is?', 'When a job is submitted, the input format computes splits and asks the NameNode for the block locations of each split. The ApplicationMaster includes these hosts and racks in its container requests to the ResourceManager, which tries to allocate containers on those nodes.'),
    ('What can cause poor data locality?', 'A busy or full cluster (no free slots on the right nodes), very small files or uneven block placement, replication factor 1, a wrong or missing rack topology script, newly added empty nodes before running the balancer, or reading data that is not in HDFS at all (for example cloud object storage).'),
    ('Does Spark use data locality?', 'Yes. Spark records preferred locations for each partition (for HDFS input, the block locations) and its scheduler waits a short time (spark.locality.wait) for a slot at the best locality level: process-local, node-local, rack-local, then any.'),
]

PRACTICE_INTRO = 'Transfer estimates and small scheduling programs. The business problems are the kind of questions asked when a team argues “just copy the data”.'
PROBLEMS = [
    dict(level='easy', title='Gigabits to hours', stmt='How many hours does it take to move 5 TB over a 10 Gbps link?', inp='5 TB · 10 Gbps',
         code='print(round(5 * 1024 * 8 / 10 / 3600, 2), "hours")\n', explain='5 TB = 40,960 Gbit; ÷ 10 Gbit/s = 4,096 s ≈ 1.14 hours, and that is with the link to yourself.'),
    dict(level='easy', title='Jar vs data', stmt='A job jar is 200 KB and the input is 4 TB. How many times bigger is the data?', inp='200 KB · 4 TB',
         code='''data_kb = 4 * 1024 * 1024 * 1024
print(f"{data_kb / 200:,.0f} times bigger")
''', explain='About 2 crore times. Sending the program to every node, even 1,000 nodes, is still tiny.'),
    dict(level='easy', title='Classify placements', stmt='A task\'s block is on dn2 (rack r1). Classify running the task on dn2, dn3 (r1) and dn7 (r2).', inp='block on dn2 · rack {dn2: r1, dn3: r1, dn7: r2}',
         code='''rack = {"dn2": "r1", "dn3": "r1", "dn7": "r2"}
for n in ["dn2", "dn3", "dn7"]:
    kind = "node-local" if n == "dn2" else "rack-local" if rack[n] == rack["dn2"] else "off-rack"
    print(n, kind)
''', explain='Same node, same rack, other rack: the three levels of locality.'),
    dict(level='medium', title='Closest replica to read', stmt='A client on dn6 must read a block whose replicas are on dn1, dn5 and dn9. Using Hadoop\'s distance (0, 2, 4), print the replica it should read.', inp='client dn6 · replicas dn1, dn5, dn9 · racks r1: dn1-dn4, r2: dn5-dn8, r3: dn9',
         code='''rack = {"dn1": "r1", "dn5": "r2", "dn6": "r2", "dn9": "r3"}
def dist(a, b):
    return 0 if a == b else 2 if rack[a] == rack[b] else 4
reps = ["dn1", "dn5", "dn9"]
print(min(reps, key=lambda r: dist("dn6", r)))
''', explain='HDFS clients sort replicas by network distance and read the closest: dn5, in the same rack.'),
    dict(level='medium', title='Data-local percentage', stmt='A job ran 1,250 map tasks: 1,180 data-local and 70 rack-local. Print the data-local percentage and whether it meets a 90% target.', inp='1250 tasks · 1180 data-local',
         code='''total, local = 1250, 1180
pct = local / total * 100
print(f"{pct:.1f}% data-local; target met: {pct >= 90}")
''', explain='94.4%: healthy. Track this per job over time; a sudden drop is an early warning.'),
    dict(level='medium', title='Network saved by locality', stmt='A job reads 2,000 blocks of 128 MB. With locality, 3% of tasks are remote; without it, 85% are. How many GB of input cross the network in each case?', inp='2000 × 128 MB · 3% vs 85% remote',
         code='''blocks, mb = 2000, 128
for label, remote in [("with locality", 0.03), ("without", 0.85)]:
    print(f"{label:14}: {blocks * remote * mb / 1024:.1f} GB over the network")
''', explain='7.5 GB vs 212.5 GB. Locality keeps the shared uplinks free for the shuffle and for other jobs.'),
    dict(level='business', title='Copy to a warehouse or query in place?', stmt='A team wants to copy 30 TB from the Hadoop cluster to a separate analytics server every night over a 10 Gbps link, for a report that needs only 2 GB of aggregated results. Estimate both transfers and print a recommendation.', inp='30 TB vs 2 GB · 10 Gbps',
         code='''link = 10            # Gbps
full = 30 * 1024 * 8 / link / 3600
agg = 2 * 8 / link
print(f"Copy all data   : {full:.1f} hours every night")
print(f"Copy the result : {agg:.1f} seconds")
print("Recommendation  : aggregate on the cluster, move only the result")
''', explain='Nearly 7 hours of saturated network every night versus 2 seconds. Push the computation to where the data lives.'),
    dict(level='business', title='Should the hot file get more replicas?', stmt='A small lookup file (one block) is read by every one of 600 map tasks. With 3 replicas, each holder serves 200 tasks. How many replicas are needed so no node serves more than 20 tasks?', inp='600 readers · at most 20 per replica',
         code='''import math
readers, limit = 600, 20
print("Replicas needed:", math.ceil(readers / limit))
''', explain='30 replicas. Hadoop does this for job files: <code>mapreduce.client.submit.file.replication</code> defaults to 10, and the distributed cache spreads small side files to the nodes that need them.'),
]

SCN_INTRO = 'Locality questions that interviewers use to separate people who have memorised definitions from people who understand clusters.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Analytics team · architecture</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Let's copy the data to the BI server every night”</h4>
      <p class="scn__situation">The BI team asks for the full 15 TB clickstream table to be copied from Hadoop to their reporting database every night, so their dashboards can query it. The dashboards show daily totals per city and product.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you apply “move the code, not the data” to a real request?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>15 TB a night over a 10 Gbps link is over 3 hours of a saturated network, and the BI database must store it all.</li>
          <li>The dashboards need aggregates. Compute them on the cluster (Hive/Spark job) and export only the summary tables, probably a few GB.</li>
          <li>If analysts need ad-hoc detail, let them query the cluster directly with Hive, Impala or Spark SQL, or a query engine like Trino that reads the data in place.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> agreeing to copy everything “because the BI tool needs it”.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · performance</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Data-local tasks dropped from 95% to 55%</h4>
      <p class="scn__situation">Last month, jobs on the cluster were 95% data-local. This week they are 55% and the core switch uplinks are saturated. Nothing in the job code changed.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you list concrete causes of poor locality and how to verify each?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li><b>New nodes added without balancing:</b> data sits on old nodes, but free slots are on new ones. Run the balancer.</li>
          <li><b>Rack script changed or broken:</b> check <code>hdfs dfsadmin -printTopology</code>.</li>
          <li><b>Cluster busier:</b> more concurrent jobs mean fewer free slots on the right nodes; review queue capacities and delay-scheduling settings.</li>
          <li><b>Data written with replication 1</b> (to save space) leaves only one local candidate per block. Check with <code>hdfs fsck</code>.</li>
          <li><b>Input moved to object storage</b> or another cluster, where node-local reads are impossible.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “Buy a faster core switch” before finding the cause.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Cloud migration · design</span><span class="scn__tag scn__tag--level">3+ years</span></div>
      <h4>“If locality is so important, why does everyone use S3?”</h4>
      <p class="scn__situation">During a migration discussion, a senior engineer argues against moving from on-prem HDFS to cloud object storage: “We'll lose data locality and everything will be slow.”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand that locality is a trade-off, not a law?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>True: reads become network reads. But cloud data-centre networks are very fast and object stores serve many parallel reads well.</li>
          <li>In return: compute and storage scale separately, clusters can be created per job and deleted, and storage is cheap and highly durable.</li>
          <li>Mitigations: columnar formats (read less), partitioning and predicate pushdown, caching layers, and right-sized instances with high network bandwidth.</li>
          <li>Benchmark the key jobs on both before deciding.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> treating either side as always right. Measure the workload.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Explain data locality to a non-technical manager</h4>
      <p class="scn__situation">Your manager, who is not technical, asks why the Hadoop cluster can process 10 TB in under an hour when copying 10 TB to one server takes a whole day.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you explain a core idea simply and correctly?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>“Imagine a census. Bringing every family to one office would take forever. Instead, we send counters to every area, they count locally at the same time, and only the totals travel back. Our cluster does the same: the data already lives on 40 machines, so we send the small counting program to each machine, all 40 work in parallel on their own part, and only small results come back.”</p>
        <p class="scn__avoid"><b>Avoid:</b> jargon such as “node-local container allocation” with a non-technical audience.</p>
      </div></details>
    </article>'''
