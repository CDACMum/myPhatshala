import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{RECAP}}', recap('Its lesson <a href="../../../big-data-fundamentals/01-introduction/02-why-one-computer-is-not-enough/">Why one computer is not enough</a> explained <i>why</i> scaling out beats scaling up (cost curve, ceiling, failures). This lesson is the practical next step: <i>how many</i> nodes a Hadoop cluster needs.')).replace('{{PLAYGROUND}}', playground(dict(
    title='Same job, three cluster sizes',
    intro='<p>Pick a cluster size, run the job, then pick another size and run it again. The <b>Job runs</b> tab keeps every result so you can compare.</p>',
    racks=3, nodes=1, features=['job', 'scale'], sizes=[3, 6, 9], speed=4,
    preload=[dict(name='tiffingo_clicks.json', sizeMB=4096)],
    **{'try': [
        dict(text='With <b>3 nodes</b> (6 task slots), run the job. 32 map tasks need about 6 waves.', on='job-done'),
        dict(text='Switch to <b>9 nodes</b> and run it again.', on='resize'),
        dict(text='Open <b>Job runs</b>. Did 3× the nodes give 3× the speed? Why not exactly? (The reduce part and start-up time do not shrink.)'),
    ]},
)))

META = dict(
    module='01-foundations', lesson='03-scale-out-in-practice', n='1.3',
    module_label='Module 1 · Foundations: before Hadoop',
    title='Scale out in practice: how big should a cluster be?',
    desc='How data engineers size a Hadoop cluster: replication, temp space, headroom, growth, compression and compute windows, step by step with real formulas. Adding nodes, the HDFS balancer, few big vs many small nodes, with animations, a cluster playground, Python calculators, quiz and interview scenarios.',
    og_desc='Turn “200 TB growing 40% a year” into a number of nodes and racks, the way platform teams really do it.',
    minutes=26, level='Beginner → Advanced',
    lead='“Add more machines” is the easy part. The real question every data team faces is: how many? This lesson turns business requirements (data size, growth, copies, deadlines) into a number of nodes, with formulas you can reuse in interviews and at work. Then you will add nodes to a full cluster, watch the balancer spread the data, and test in the playground whether three times the nodes really means three times the speed.',
    chips=['Cluster Playground', 'Runs in your browser (Python)', 'Sizing calculator'],
)

RUN = dict(
    heading='A cluster sizing calculator',
    intro='<p>This function turns business requirements into a number of storage nodes, using the formulas from Part 2. Change the inputs and run it again, then try the challenges.</p>',
    code='''import math

def storage_nodes(data_tb, replication=3, temp=0.25, headroom=0.25, node_tb=144):
    raw_tb = data_tb * replication / (1 - temp - headroom)
    return raw_tb, math.ceil(raw_tb / node_tb)

for data in [50, 200, 500]:
    raw, nodes = storage_nodes(data)
    print(f"{data:>4} TB data -> {raw:>6.0f} TB raw -> {nodes:>3} nodes")
''',
    anno=[
        ('def storage_nodes(data_tb, replication=3, temp=0.25, headroom=0.25, node_tb=144):', 'Default values hold the usual assumptions, so a caller only passes what is different, for example <code>storage_nodes(200, node_tb=240)</code>.'),
        ('raw_tb = data_tb * replication / (1 - temp - headroom)', 'With the defaults, this is data × 3 ÷ 0.5 = data × 6.'),
        ('return raw_tb, math.ceil(raw_tb / node_tb)', 'Return two values at once (a tuple). <code>math.ceil</code> rounds up: you cannot buy half a node.'),
    ],
    tasks=[
        dict(label='1 · Storage nodes', hint='Press <b>Run</b>. Then call <code>storage_nodes(200, node_tb=240)</code>: bigger nodes, fewer of them.', code=None),
        dict(label='2 · Growth', hint='<b>Predict first:</b> after 3 years at 40% growth, is 200 TB closer to 400 or 550? Then try 60% growth.',
             code='''data = 200
for year in range(1, 4):
    data = data * 1.40
    print("Year", year, ":", round(data), "TB")
'''),
        dict(label='3 · Compute nodes', hint='A job of 9,000 task-minutes must finish in 120 minutes. Each node runs 16 tasks at once. How many nodes for compute? Halve the window to 60 minutes.',
             code='''import math
task_minutes = 9000
window = 120
slots_per_node = 16

nodes = math.ceil(task_minutes / (window * slots_per_node))
print("Compute needs", nodes, "nodes")
'''),
        dict(label='4 · The bigger number wins', hint='Final size = max(storage, compute) + spares. Make the job 40,000 task-minutes: does compute now decide?',
             code='''import math
storage = math.ceil(200 * 3 / 0.5 / 144)
compute = math.ceil(9000 / (120 * 16))
spares = 2
print("Storage:", storage, "| Compute:", compute)
print("Buy:", max(storage, compute) + spares, "nodes")
'''),
        dict(label='5 · Spot the error', hint='This sizing says 1 node. Something important is missing. Fix the formula (hint: copies and free space).',
             code='''import math
data_tb = 120
node_tb = 144
print("Nodes needed:", math.ceil(data_tb / node_tb))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Growing data year by year, one line at a time',
    intro='<p>Watch <code>data</code> grow 40% each time round the loop, and see the function called once per year to turn it into nodes. Each call gets its own frame.</p>',
    code='''import math

def nodes_for(data_tb):
    raw = data_tb * 6
    return math.ceil(raw / 144)

data = 100
for year in [1, 2, 3]:
    data = data * 1.4
    print("Year", year, round(data), "TB ->", nodes_for(data), "nodes")
''',
    notes={4: 'Formula :: × 3 copies ÷ 0.5 (temp + headroom) = × 6.', 7: 'Today :: 100 TB of business data.'},
)

WORKED_INTRO = 'Three sizing problems from real platform planning: storage only, a deadline, and a three-year plan that adds nodes each year. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Platform planning · storage', title='How many nodes for 80 TB of data?',
         problem='<p>A college research group wants to store <b>80 TB</b> of sensor data in HDFS with replication 3, 25% temp space and 25% headroom. Each node has <b>96 TB</b> raw. How many nodes, and how many racks of 10?</p>',
         inp='80 TB · ×3 · ÷0.5 · 96 TB/node · 10 nodes/rack',
         approach=['Raw = data × 3 ÷ 0.5.',
                   'Nodes = raw ÷ 96, rounded up.',
                   'Racks = nodes ÷ 10, rounded up. Use at least 2 racks so copies can span racks.'],
         code='''import math
raw = 80 * 3 / 0.5
nodes = math.ceil(raw / 96)
racks = max(2, math.ceil(nodes / 10))
print("Raw disk:", raw, "TB")
print("Nodes:", nodes)
print("Racks:", racks)
''', notes={4: 'Racks :: <code>max(2, …)</code>: one rack would be a single failure domain.'},
         tryit='Use replication 2 instead of 3. How many nodes are saved, and what risk do you take?'),
    dict(level='i', tag='Banking · batch window', title='Will the nightly job fit in the window?',
         problem='<p>A bank\'s risk job has <b>6,000 map tasks</b> of about <b>5 minutes</b> each. The cluster has <b>30 nodes</b> with <b>12 slots</b> each. Reduces take a fixed 20 minutes after the maps. The job must finish within <b>90 minutes</b>. Does it fit, and if not, how many nodes are needed?</p>',
         inp='6,000 tasks × 5 min · 30 nodes × 12 slots · +20 min · 90 min window',
         approach=['Waves = tasks ÷ (nodes × slots), rounded up.',
                   'Job time = waves × 5 + 20.',
                   'If too slow, add nodes one at a time until it fits.'],
         code='''import math

def job_minutes(nodes, tasks=6000, minutes=5, slots=12, reduce_min=20):
    waves = math.ceil(tasks / (nodes * slots))
    return waves * minutes + reduce_min

nodes = 30
print(nodes, "nodes:", job_minutes(nodes), "min")
while job_minutes(nodes) > 90:
    nodes += 1
print("Need", nodes, "nodes:", job_minutes(nodes), "min")
''', notes={8: 'Search :: Add one node at a time until the job fits the 90-minute window.'},
         tryit='The reduce part is fixed at 20 minutes. If the window were 25 minutes, could any number of nodes meet it? This is Amdahl\'s law in action.'),
    dict(level='a', tag='Data platform · 3-year plan', title='How many nodes to add each year?',
         problem='<p>TiffinGo has <b>200 TB</b> today, growing <b>40%</b> a year. Storage uses the ×6 rule (3 copies ÷ 0.5), nodes have <b>144 TB</b>, and they keep <b>2 spare</b> nodes. For each of the next 3 years, print the nodes needed and how many to buy that year.</p>',
         inp='200 TB · +40%/year · ×6 · 144 TB/node · +2 spares · 3 years',
         approach=['Start with the nodes needed for today\'s data.',
                   'Each year: grow the data, compute the nodes needed, and buy the difference from last year.',
                   'Never buy a negative number (you don\'t sell nodes when data shrinks).'],
         code='''import math

def needed(data_tb):
    return math.ceil(data_tb * 6 / 144) + 2

data = 200
have = needed(data)
print("Today:", have, "nodes")
for year in [1, 2, 3]:
    data = data * 1.4
    need = needed(data)
    buy = max(0, need - have)
    have = have + buy
    print(f"Year {year}: {data:.0f} TB, need {need}, buy {buy}")
''', notes={7: 'Start :: Nodes for today\'s 200 TB, including spares.'},
         tryit='Finance asks to buy everything on day one instead. How many nodes is that, and how many sit idle in year 1?'),
]

QUIZ = mix([
    dict(q='You must store 100 TB in HDFS with replication 3. Ignoring temp space and headroom, how much raw disk is needed?', options=['100 TB', '133 TB', '300 TB', '600 TB'], answer=2,
         why='Every block is stored 3 times: 100 × 3 = <b>300 TB</b>.'),
    dict(q='With replication 3, 25% temp space and 25% headroom, raw disk needed is about:', options=['data × 3', 'data × 4', 'data × 6', 'data × 9'], answer=2,
         why='data × 3 ÷ (1 − 0.25 − 0.25) = data × 3 ÷ 0.5 = <b>data × 6</b>.'),
    dict(q='Storage sizing says 13 nodes; compute sizing says 5 nodes. How many do you plan for (before spares)?', options=['5', '9', '13', '18'], answer=2,
         why='The cluster must meet both requirements, so you take the <b>larger</b>: 13.'),
    dict(q='Data of 100 TB grows 50% every year. After 2 years it is:', options=['150 TB', '200 TB', '225 TB', '250 TB'], answer=2,
         why='Growth compounds: 100 × 1.5 × 1.5 = <b>225 TB</b>.'),
    dict(q='After adding 4 empty DataNodes, why might old jobs not get faster immediately?', options=['New nodes need a week to warm up', 'Existing blocks stay on the old nodes until the balancer moves some to the new ones', 'HDFS ignores new nodes for 24 hours', 'Jobs only run on master nodes'], answer=1,
         why='Old data is still only on the old nodes. Run the <b>HDFS balancer</b> to spread blocks to the new nodes.'),
    dict(q='Why can many smaller nodes be better than a few very large nodes of the same total size?', options=['They use less power', 'A failure loses a smaller share, re-replication is faster, and work spreads over more disks and NICs', 'They need no network', 'HDFS supports only small nodes'], answer=1,
         why='Smaller failure “blast radius”, faster recovery and more parallelism. The cost is more machines to manage and more rack space.'),
    dict(q='Doubling the nodes of a cluster usually makes a job:', options=['Exactly twice as fast', 'Faster, but often less than twice as fast', 'Slower', 'No different'], answer=1,
         why='Parts of a job do not split: start-up, coordination, the reduce phase, the slowest task. Speed-up is real but not perfect (Amdahl\'s law).'),
    dict(q='In the cloud, with data kept in object storage (like S3), a Hadoop/Spark cluster is mostly sized for:', options=['Storage only', 'Compute for the jobs, often created and deleted per job', 'Nothing: the cloud sizes itself', 'Exactly the same as on-premises'], answer=1,
         why='Separating storage from compute means clusters are sized for the work, and can be scaled or shut down without moving data.'),
])

REVISION = [
    '<b>Scale out</b> = add nodes. <b>Sizing</b> = decide how many, before buying.',
    'Storage: raw = data × replication ÷ (1 − temp − headroom). Defaults (3, 25%, 25%) give <b>× 6</b>.',
    'Compute: nodes = task-minutes ÷ (window × slots per node).',
    'Final size = <b>max</b>(storage, compute) + spares. Round <b>up</b>.',
    'Growth compounds: data × (1 + rate)<sup>years</sup>. Measure compression on real samples.',
    'Use at least 2 racks so replicas span failure domains.',
    'New nodes start empty: run <code>hdfs balancer -threshold 10</code>.',
    'Many small nodes: smaller blast radius, faster re-replication. Few big nodes: less space and power.',
    'More nodes ≠ proportionally faster: fixed parts of a job remain (Amdahl).',
    'Cloud: storage in object stores, clusters sized for compute and often temporary.',
]
FAQ = [
    ('How do you size a Hadoop cluster?', 'Start from requirements: current data, growth rate, retention period and compression. Multiply by the replication factor, add temporary space for intermediate data (about 25% of raw is a common rule of thumb) and headroom (20–30%). Divide by usable disk per node to get storage nodes. Separately estimate compute nodes from the workload and time windows. Take the larger number, add spares for failures, and spread nodes over at least two racks. State your assumptions.'),
    ('Why do we keep free headroom in HDFS?', 'A nearly full HDFS causes failed writes, uneven nodes and slow jobs. Free space absorbs growth spikes, job temp files and re-replication after a node dies (the surviving nodes must hold the lost replicas).'),
    ('What does the HDFS balancer do?', 'It moves blocks from over-utilised DataNodes to under-utilised ones until every node\'s usage is within a threshold (for example 10%) of the cluster average. It runs in the background with limited bandwidth so normal work continues. It is typically used after adding nodes.'),
    ('Is it better to have more small nodes or fewer large nodes?', 'It depends. More small nodes give more parallel disks and network ports, a smaller share lost per failure and faster re-replication. Fewer large nodes save rack space, power and management effort, and suit cold archive data. Very dense nodes make failures expensive to recover from.'),
    ('Why doesn\'t doubling the nodes always halve the job time?', 'Some parts of a job are serial or fixed: start-up, planning, the reduce or final step, waiting for the slowest task, and coordination overhead. Amdahl\'s law says the serial part limits the maximum speed-up. Moving more data over the network can also add cost.'),
]

PRACTICE_INTRO = 'Sizing questions of the kind asked in data engineering interviews and in real capacity reviews. Work them out on paper first, then run the code.'
PROBLEMS = [
    dict(level='easy', title='Raw disk for 50 TB', stmt='How much raw disk is needed for 50 TB of data with replication 3, 25% temp and 25% headroom?', inp='50 TB · 3 · 0.25 · 0.25',
         code='print(50 * 3 / (1 - 0.25 - 0.25), "TB")\n', explain='50 × 3 ÷ 0.5 = 300 TB: six times the data.'),
    dict(level='easy', title='Nodes from raw disk', stmt='The cluster needs 1,000 TB raw. Each node has 12 disks of 16 TB. How many nodes?', inp='1000 TB raw · 12 × 16 TB',
         code='import math\nprint(math.ceil(1000 / (12 * 16)), "nodes")\n', explain='Each node has 192 TB, so 1000 ÷ 192 = 5.2 → 6 nodes.'),
    dict(level='easy', title='Waves of tasks', stmt='A job has 500 tasks. The cluster has 25 nodes with 8 slots each. How many waves?', inp='500 tasks · 25 × 8 slots',
         code='import math\nprint(math.ceil(500 / (25 * 8)), "waves")\n', explain='200 tasks run at once, so 500 tasks need 3 waves.'),
    dict(level='medium', title='Compression saves nodes', stmt='300 TB of logs compress 4× as Parquet. Using the ×6 rule and 144 TB nodes, how many nodes without and with compression?', inp='300 TB · 4× · ×6 · 144 TB',
         code='''import math
for label, tb in [("raw logs", 300), ("Parquet", 300 / 4)]:
    print(label, "->", math.ceil(tb * 6 / 144), "nodes")
''', explain='13 vs 4 nodes. Good file formats are one of the biggest cost levers in big data (Module 10).'),
    dict(level='medium', title='When does the cluster get full?', stmt='A cluster can hold 400 TB of business data. Data is 150 TB and grows 35% a year. In which year does it pass 400 TB?', inp='capacity 400 · 150 TB · +35%/year',
         code='''data, year = 150, 0
while data <= 400:
    data *= 1.35
    year += 1
print("Year", year, "->", round(data), "TB")
''', explain='150 → 203 → 273 → 369 → 498. It passes in year 4, so new nodes must be ordered in year 3, allowing for delivery time.'),
    dict(level='medium', title='Re-replication time after a failure', stmt='A node with 200 TB of replicas dies. The other 39 nodes each copy at 100 MB/s for re-replication, in parallel. Roughly how many hours until all copies are restored?', inp='200 TB · 39 nodes × 100 MB/s',
         code='''mb = 200 * 1024 * 1024
rate = 39 * 100            # MB per second, all nodes together
print(round(mb / rate / 3600, 1), "hours")
''', explain='About 15 hours with these numbers. Denser nodes take longer, which raises the risk that a second failure hits a block before it is fully copied again.'),
    dict(level='business', title='Cloud cluster per night vs always on', stmt='A nightly job needs 40 nodes for 2 hours. A cloud node costs Rs 35 per hour. Compare a cluster kept on all day (24 h) with one created only for the job, for 30 days.', inp='40 nodes · Rs 35/h · 2 h vs 24 h · 30 days',
         code='''rate, nodes, days = 35, 40, 30
always = nodes * 24 * rate * days
per_job = nodes * 2 * rate * days
print(f"Always on : Rs {always / 1e5:.2f} lakh")
print(f"Per job   : Rs {per_job / 1e5:.2f} lakh")
print(f"Saved     : Rs {(always - per_job) / 1e5:.2f} lakh")
''', explain='Rs 10.08 lakh vs Rs 0.84 lakh a month (illustrative prices). With data in object storage, creating clusters per job saves most of the compute bill.'),
    dict(level='business', title='Full sizing note for a manager', stmt='Write a small program that prints a sizing note: data 120 TB, growth 30% for 2 years, replication 3, 25% temp, 25% headroom, 144 TB nodes, 2 spares, 12 nodes per rack.', inp='120 TB · 30% × 2 years · 3 · 0.25 · 0.25 · 144 TB · +2 · 12/rack',
         code='''import math
data = 120 * 1.3 ** 2
raw = data * 3 / (1 - 0.25 - 0.25)
nodes = math.ceil(raw / 144) + 2
racks = max(2, math.ceil(nodes / 12))
print(f"Data in 2 years : {data:.0f} TB")
print(f"Raw disk needed : {raw:.0f} TB")
print(f"Nodes (+2 spare): {nodes}")
print(f"Racks           : {racks}")
''', explain='Always present the result with its assumptions. If the manager changes growth or replication, the note can be re-run in seconds.'),
]

SCN_INTRO = 'Sizing and scaling situations that come up in data engineering interviews. Decide your answer first, then compare.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Data platform · capacity</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“We have 100 TB. How many 100 TB nodes do we need?”</h4>
      <p class="scn__situation">The interviewer gives you exactly this question and waits. There is no more information.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know that HDFS needs far more raw disk than the data size, and do you ask about assumptions?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>Not one. First, questions: replication factor? growth rate and retention? compression? workload? Then a default calculation:</p>
        <ul>
          <li>100 TB × 3 copies = 300 TB, ÷ 0.5 for temp space and headroom = <b>600 TB raw</b>, so <b>6 nodes</b>, plus 1–2 spares.</li>
          <li>With 40% growth for 2 years: 196 TB of data, about 12 nodes, plus spares.</li>
          <li>Check compute too, and spread over at least two racks.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid saying:</b> “One node, because 100 TB fits.”</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Retail · operations</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>We added 10 nodes and nothing got faster</h4>
      <p class="scn__situation">A 30-node cluster was 85% full and jobs were slow. The team added 10 new nodes yesterday. Today jobs are just as slow, and the new nodes show almost no disk usage.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know how HDFS treats new nodes and how to fix the imbalance safely?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>New DataNodes start empty. Existing blocks stay on the old nodes, so tasks reading old data still run (data-local) mostly on the old 30 nodes.</li>
          <li>Run the <b>balancer</b>: <code>hdfs balancer -threshold 10</code>, with a bandwidth limit so production jobs are not hurt, preferably at night.</li>
          <li>Check that the new nodes are in the topology script (correct racks) and that their NodeManagers are registered, so YARN can use their CPU.</li>
          <li>Also check that the slowness was really storage-related; if jobs were CPU- or network-bound, more disks alone wouldn't help.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “Wait a few days, it will balance itself.” Only new writes go to new nodes.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Infrastructure · hardware choice</span><span class="scn__tag scn__tag--level">3+ years</span></div>
      <h4>24 × 22 TB disks per node: good idea?</h4>
      <p class="scn__situation">To save rack space, a vendor proposes very dense nodes: 24 disks of 22 TB each (528 TB per node). The cluster would have only 8 nodes instead of 30 smaller ones.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you reason about failure blast radius, recovery time and parallelism?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Failure impact:</b> one node is 12.5% of the cluster. Its loss forces re-copying up to ~528 TB, which can take a day or more and loads the network.</li>
          <li><b>Rack awareness:</b> with 8 nodes, spreading replicas over racks evenly is harder.</li>
          <li><b>Compute:</b> fewer nodes means fewer cores and NICs for parallel tasks, unless the CPU is scaled up too.</li>
          <li><b>When it's fine:</b> mostly cold, archival data with light processing, possibly with erasure coding.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> judging only by cost per TB.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Startup · cloud cost</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The cloud bill doubled, but data only grew 10%</h4>
      <p class="scn__situation">A startup runs a 50-node cloud Hadoop cluster 24 hours a day. Jobs run only from midnight to 4 am. The bill has doubled since last year.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know how cloud clusters are sized differently from on-premises ones?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Keep data in object storage (S3, GCS, ADLS) instead of HDFS on the cluster's disks, so the cluster holds no data of its own.</li>
          <li>Create the cluster for the nightly jobs and delete it after, or autoscale it down to a few nodes during the day: about 4 hours a day instead of 24 can cut the compute bill roughly in proportion.</li>
          <li>Use cheaper spot/preemptible nodes for task-only nodes that can be lost safely.</li>
          <li>Check which jobs grew; maybe one job is rescanning all history every night.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> treating a cloud cluster like on-prem hardware that must run all the time.</p>
      </div></details>
    </article>'''
