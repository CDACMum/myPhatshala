import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Test every fix',
    intro='<p>Three racks, a standby NameNode, and every feature switched on. Each checklist item tests one line of Riya\'s board.</p>',
    racks=3, nodes=3, features=['upload', 'fail', 'job', 'locality', 'ha', 'fsck'],
    preload=[dict(name='bharatsearch_pages.txt', sizeMB=1024)],
    **{'try': [
        dict(text='<b>Doesn\'t fit →</b> upload a 2 GB file and see its blocks spread across nine nodes.', on='upload-done'),
        dict(text='<b>Too slow + network →</b> run the job: parallel tasks, almost all data-local.', on='job-done'),
        dict(text='<b>Disks die →</b> stop a node and skip to the timeout: re-replication.', on='rereplicated'),
        dict(text='<b>Master is a SPOF →</b> stop the active NameNode: the standby takes over.', on='nn-failover'),
        dict(text='<b>Is it healthy? →</b> run <b>hdfs fsck /</b>.', on='fsck'),
    ]},
)))

META = dict(
    module='02-why-hadoop', lesson='03-how-hadoop-solved-each-problem', n='2.3',
    module_label='Module 2 · Why Hadoop was born',
    title='How Hadoop solved each problem',
    desc='Hadoop\'s architecture as answers to concrete problems: HDFS for storage, replication for failures, MapReduce for parallel processing, data locality for the network, the map/reduce model for simplicity, YARN and HA in Hadoop 2, erasure coding in Hadoop 3, and the problems Hadoop did not solve. With animations, a full-feature playground, a tiny MapReduce in Python, quiz and interview scenarios.',
    og_desc='Every part of Hadoop exists to fix one problem. Map them, test them in a live cluster, and learn what Hadoop does not fix.',
    minutes=25, level='Beginner → Advanced',
    lead='Every component of Hadoop exists because of a specific problem: data that doesn\'t fit, disks that die, jobs that take days, a jammed network, mountains of plumbing code, and a master that must not fail. This lesson maps each problem to its fix, runs a tiny MapReduce in Python so you see exactly which part you write and which part Hadoop does, and ends with the problems Hadoop never solved, which is why Spark and other tools exist.',
    chips=['Full-feature playground', 'Tiny MapReduce in Python', 'Strengths and limits'],
)

RUN = dict(
    heading='A tiny MapReduce, in 20 lines of Python',
    intro='<p>This is the whole MapReduce idea on one machine. <code>map_fn</code> and <code>reduce_fn</code> are the only parts you would write in Hadoop; <code>run_job</code> plays the framework: it splits the input, runs every map, shuffles and sorts by key, and runs every reduce.</p>',
    code='''def map_fn(line):                        # YOU write this
    city, amount = line.split(",")
    return [(city, int(amount))]

def reduce_fn(city, amounts):            # YOU write this
    return city, sum(amounts)

def run_job(lines, splits=2):            # HADOOP does this part
    parts = [lines[i::splits] for i in range(splits)]
    mapped = [kv for part in parts for line in part for kv in map_fn(line)]
    groups = {}
    for k, v in sorted(mapped):          # shuffle and sort by key
        groups.setdefault(k, []).append(v)
    return [reduce_fn(k, vs) for k, vs in groups.items()]

orders = ["Pune,240", "Delhi,120", "Pune,60", "Goa,300", "Delhi,80"]
print(run_job(orders))
''',
    anno=[
        ('def map_fn(line):', 'Map: turn one input record into zero or more (key, value) pairs. Here: (city, amount).'),
        ('parts = [lines[i::splits] for i in range(splits)]', 'Split the input into pieces, like HDFS blocks. <code>lines[i::2]</code> takes every second line starting at <code>i</code>.'),
        ('for k, v in sorted(mapped):', 'Shuffle and sort: all values with the same key end up together, in key order.'),
        ('return [reduce_fn(k, vs) for k, vs in groups.items()]', 'Reduce: called once per key with the list of all its values.'),
    ],
    tasks=[
        dict(label='1 · Sales per city', hint='Press <b>Run</b>. Then add <code>"Goa,50"</code> to the orders. Only the input changed; the framework code didn\'t.', code=None),
        dict(label='2 · Word count', hint='<b>Predict first:</b> what does the output look like? Change only <code>map_fn</code> and <code>reduce_fn</code>; <code>run_job</code> stays the same.',
             code='''def map_fn(line):
    return [(w, 1) for w in line.lower().split()]

def reduce_fn(word, ones):
    return word, sum(ones)

def run_job(lines, splits=2):
    parts = [lines[i::splits] for i in range(splits)]
    mapped = [kv for part in parts for line in part for kv in map_fn(line)]
    groups = {}
    for k, v in sorted(mapped):
        groups.setdefault(k, []).append(v)
    return [reduce_fn(k, vs) for k, vs in groups.items()]

print(run_job(["Hadoop stores data", "Hadoop processes data", "data data data"]))
'''),
        dict(label='3 · Max per key', hint='Find the biggest order per city. Which function do you change? Replace <code>sum</code> with something else.',
             code='''def map_fn(line):
    city, amount = line.split(",")
    return [(city, int(amount))]

def reduce_fn(city, amounts):
    return city, max(amounts)

def run_job(lines):
    groups = {}
    for k, v in sorted(kv for line in lines for kv in map_fn(line)):
        groups.setdefault(k, []).append(v)
    return [reduce_fn(k, vs) for k, vs in groups.items()]

print(run_job(["Pune,240", "Delhi,120", "Pune,60", "Goa,300", "Delhi,80"]))
'''),
        dict(label='4 · A failed split is re-run', hint='The framework retries a split whose map fails the first time. Watch the attempt numbers; make split 0 fail twice.',
             code='''import itertools
failures = {1: 1}                        # split 1 fails once
def run_split(n, attempt):
    if failures.get(n, 0) >= attempt:
        raise RuntimeError(f"split {n} lost its node")
    return f"split {n} ok on attempt {attempt}"

for n in range(3):
    for attempt in itertools.count(1):
        try:
            print(run_split(n, attempt)); break
        except RuntimeError as e:
            print("  retry:", e)
'''),
        dict(label='5 · Spot the error', hint='This map function crashes on one bad record. Real data always has some. Make it skip lines that don\'t have exactly two fields.',
             expect='error',
             code='''def map_fn(line):
    city, amount = line.split(",")
    return [(city, int(amount))]

for line in ["Pune,240", "Delhi", "Goa,300"]:
    print(map_fn(line))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Map, shuffle and reduce, one line at a time',
    intro='<p>Follow three orders through map (records → pairs), shuffle (pairs grouped by key) and reduce (one total per city). Watch the <code>groups</code> dictionary build up.</p>',
    code='''orders = ["Pune,240", "Goa,300", "Pune,60"]

pairs = []
for line in orders:
    city, amt = line.split(",")
    pairs.append((city, int(amt)))

groups = {}
for city, amt in sorted(pairs):
    groups.setdefault(city, []).append(amt)

for city, amts in groups.items():
    print(city, sum(amts))
''',
    notes={3: 'Map :: Each order becomes one (city, amount) pair.', 8: 'Shuffle :: Group the pairs by key, in sorted order.', 11: 'Reduce :: One total per city.'},
)

WORKED_INTRO = 'Three problems that show each layer of Hadoop doing its job: a MapReduce on business data, the storage cost of replication versus erasure coding, and the gain from YARN sharing one cluster. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Retail · MapReduce', title='Total sales per store with map and reduce',
         problem='<p>A chain of chai stalls logs each sale as <code>store,item,amount</code>. Using only a map function and a reduce function, compute the total sales per store.</p>',
         inp='["Kharghar,chai,20", "Vashi,samosa,15", "Kharghar,samosa,15", "Vashi,chai,20", "Kharghar,chai,20"]',
         approach=['Map: from each line, emit (store, amount).',
                   'Shuffle: group amounts by store (sorted).',
                   'Reduce: sum each store\'s list.'],
         code='''def map_fn(line):
    store, item, amount = line.split(",")
    return (store, int(amount))

def reduce_fn(store, amounts):
    return store, sum(amounts)

sales = ["Kharghar,chai,20", "Vashi,samosa,15", "Kharghar,samosa,15",
         "Vashi,chai,20", "Kharghar,chai,20"]
groups = {}
for store, amt in sorted(map_fn(s) for s in sales):
    groups.setdefault(store, []).append(amt)
for store, amts in groups.items():
    print(reduce_fn(store, amts))
''', notes={10: 'Shuffle :: This loop is what Hadoop does for you between map and reduce.'},
         tryit='Change the map function to emit (item, amount) instead. The same framework now gives sales per item.'),
    dict(level='i', tag='Storage · cost', title='Replication or erasure coding for old data?',
         problem='<p>A telecom keeps <b>600 TB</b> of call records. The last 3 months (<b>60 TB</b>) are hot; the rest is cold. Compare raw disk needed if everything uses 3× replication, versus hot data at 3× and cold data with erasure coding (RS-6-3, 1.5×).</p>',
         inp='600 TB total · 60 TB hot · replication 3× · erasure coding 1.5×',
         approach=['All replicated: 600 × 3.',
                   'Mixed: 60 × 3 + 540 × 1.5.',
                   'Print the saving.'],
         code='''total, hot = 600, 60
cold = total - hot
all_rep = total * 3
mixed = hot * 3 + cold * 1.5
print("All 3x replication:", all_rep, "TB raw")
print("Hot 3x + cold EC   :", mixed, "TB raw")
print(f"Saving: {all_rep - mixed:.0f} TB ({1 - mixed / all_rep:.0%})")
''', notes={4: 'RS-6-3 :: 6 data cells + 3 parity cells = 9 for every 6, so 1.5×.'},
         tryit='Erasure coding costs CPU and network to rebuild lost data, and reads of small files get slower. That is why it suits cold data only.'),
    dict(level='a', tag='YARN · utilisation', title='Why sharing one cluster with YARN beats separate clusters',
         problem='<p>Three teams each have their own 20-node cluster. Their busy hours differ: each cluster is 90% busy for 6 hours a day and 10% busy for the rest. Compare average utilisation with separate clusters, and the number of nodes a shared YARN cluster would need to give every team its peak.</p>',
         inp='3 teams × 20 nodes · 90% busy 6 h, 10% busy 18 h · peaks at different times',
         approach=['Average utilisation of one cluster = (0.9 × 6 + 0.1 × 18) ÷ 24.',
                   'Shared cluster: at any hour, at most one team is at peak (18 nodes busy) and two are quiet (2 each).',
                   'Nodes needed = 18 + 2 + 2, plus some spare.'],
         code='''peak, quiet = 0.9, 0.1
avg = (peak * 6 + quiet * 18) / 24
print(f"Separate clusters: {avg:.0%} average utilisation, 60 nodes")

shared_needed = 20 * peak + 2 * 20 * quiet
print(f"Shared YARN cluster: about {shared_needed:.0f} nodes busy at worst")
print(f"With 25% spare: {shared_needed * 1.25:.0f} nodes instead of 60")
''', notes={6: 'Shared :: One team at peak + two quiet teams.'},
         tryit='What if all three teams peak at the same hour? Then sharing saves nothing at peak, which is why YARN queues have guaranteed minimums (Module 11).'),
]

QUIZ = mix([
    dict(q='Which Hadoop module solves “the data doesn\'t fit on one machine”?', options=['YARN', 'HDFS', 'Hadoop Common', 'ZooKeeper'], answer=1,
         why='<b>HDFS</b> splits files into blocks spread over many DataNodes.'),
    dict(q='In MapReduce, which parts does the programmer normally write?', options=['The scheduler and the shuffle', 'The map and reduce functions (plus a small driver)', 'The NameNode', 'The network protocol'], answer=1,
         why='You write the map and reduce logic; splitting, scheduling, shuffling, sorting and retries are done by the framework.'),
    dict(q='What does the shuffle phase do?', options=['Deletes duplicate files', 'Moves map outputs to reducers, grouped and sorted by key', 'Randomly reorders input lines', 'Compresses blocks'], answer=1,
         why='The shuffle sends each key\'s values from all mappers to the reducer responsible for that key, sorted by key.'),
    dict(q='Which problem did YARN (Hadoop 2) solve?', options=['Disks failing', 'Only MapReduce could use the cluster, and one JobTracker limited scale', 'Files were too big', 'Java was too slow'], answer=1,
         why='YARN separated resource management from MapReduce, so many engines (Spark, Tez…) can share one cluster, and scaling improved.'),
    dict(q='What does erasure coding in Hadoop 3 mainly save?', options=['CPU time', 'Storage: about 1.5× overhead instead of 3× for cold data', 'Network ports', 'NameNode RAM'], answer=1,
         why='Erasure coding stores parity instead of full copies, cutting raw storage for rarely read data.'),
    dict(q='Which of these did classic Hadoop MapReduce NOT handle well?', options=['Scanning a whole 100 TB data set', 'Iterative machine-learning algorithms that reread data many times', 'Surviving node failures', 'Storing raw log files'], answer=1,
         why='MapReduce writes intermediate data to disk and restarts tasks each pass, so iterative jobs are slow. Spark addressed this with in-memory processing.'),
    dict(q='What is “schema-on-read”?', options=['Data must match a table schema before it can be stored', 'Raw data is stored as it is, and structure is applied when it is read', 'Schemas are read from ZooKeeper', 'Only CSV files can be read'], answer=1,
         why='Hadoop stores any bytes; tools like Hive or Spark apply a schema when querying.'),
    dict(q='Hadoop\'s four core modules are:', options=['HDFS, Hive, Pig, HBase', 'Common, HDFS, YARN, MapReduce', 'NameNode, DataNode, Spark, Kafka', 'Java, Linux, SSH, XML'], answer=1,
         why='<b>Hadoop Common, HDFS, YARN and MapReduce</b>. Hive, Pig, HBase and Spark are ecosystem projects.'),
])

REVISION = [
    'Four core modules: <b>Common</b> (shared code), <b>HDFS</b> (storage), <b>YARN</b> (resources), <b>MapReduce</b> (processing).',
    'Doesn\'t fit → HDFS blocks. Disks die → 3 replicas, re-replication, checksums.',
    'Too slow → parallel map tasks. Network → data locality.',
    'Plumbing → you write <b>map</b> + <b>reduce</b>; framework does splits, scheduling, <b>shuffle and sort</b>, retries.',
    'Growth → add nodes; NameNode tracks each block; balancer spreads data.',
    'Hadoop 2: <b>YARN</b> (many engines, better scale) + <b>NameNode HA</b>. Hadoop 3: <b>erasure coding</b>, multiple standbys.',
    'Schema-on-read: store raw, structure at query time.',
    'Not solved by MapReduce: low latency, iterative ML, streaming, small files, in-place updates → Spark, Flink, Trino, Iceberg/Delta/Hudi.',
]
FAQ = [
    ('What are the core components of Hadoop?', 'Hadoop Common (shared libraries, configuration and utilities), HDFS (distributed storage with a NameNode for metadata and DataNodes for blocks), YARN (resource management with a ResourceManager, NodeManagers and per-application ApplicationMasters) and MapReduce (the batch processing model and engine that runs on YARN).'),
    ('How does Hadoop achieve scalability?', 'By scaling out: HDFS spreads blocks over any number of DataNodes and the NameNode tracks each block individually, so adding nodes adds capacity without re-sharding. MapReduce creates one task per input split, so more nodes means more tasks run in parallel. YARN schedules resources across all nodes.'),
    ('Which part of a MapReduce job is handled by the framework?', 'Computing input splits, scheduling map tasks near their data, running the map tasks, partitioning, spilling, sorting and shuffling map outputs to reducers, merging them, running reduce tasks, writing output to HDFS, tracking progress and counters, and retrying failed or slow tasks. The developer supplies the map and reduce functions and job configuration.'),
    ('What problems does Hadoop not solve well?', 'Low-latency queries and point lookups, iterative and interactive workloads with MapReduce, real-time streaming, very large numbers of small files, and in-place updates of records. Other tools fill these gaps: HBase for lookups, Spark for iterative and in-memory work, Flink/Kafka for streaming, Trino/Impala for interactive SQL, and table formats such as Iceberg, Delta Lake and Hudi for updates.'),
    ('Why was YARN introduced?', 'In Hadoop 1 the JobTracker handled both resource management and job tracking, which limited cluster size and allowed only MapReduce jobs. YARN separated these: the ResourceManager manages resources for the whole cluster, and each application has its own ApplicationMaster. This improved scalability and let other engines like Spark and Tez share the same cluster.'),
]

PRACTICE_INTRO = 'Practise the MapReduce way of thinking (map → shuffle → reduce) and the arithmetic behind Hadoop\'s storage choices.'
PROBLEMS = [
    dict(level='easy', title='Map one line', stmt='Write a map function that turns "Pune,UPI,450" into ("UPI", 450), and test it.', inp='"Pune,UPI,450"',
         code='''def map_fn(line):
    city, mode, amount = line.split(",")
    return (mode, int(amount))
print(map_fn("Pune,UPI,450"))
''', explain='The key you emit decides how data is grouped. Here the key is the payment mode.'),
    dict(level='easy', title='Group pairs by key', stmt='Group these pairs by key into a dictionary of lists: [("a",1),("b",2),("a",3)].', inp='[("a",1),("b",2),("a",3)]',
         code='''pairs = [("a", 1), ("b", 2), ("a", 3)]
groups = {}
for k, v in pairs:
    groups.setdefault(k, []).append(v)
print(groups)
''', explain='This is the shuffle in one loop. In Hadoop it happens across the network between thousands of tasks.'),
    dict(level='easy', title='Raw disk for replication 3', stmt='How much raw disk does 250 TB of data need with replication 3, and with erasure coding at 1.5×?', inp='250 TB',
         code='print("Replication:", 250 * 3, "TB | EC:", 250 * 1.5, "TB")\n', explain='750 TB vs 375 TB. EC halves raw storage for data that is rarely read.'),
    dict(level='medium', title='Average order per city', stmt='Using map and reduce, compute the average order amount per city.', inp='["Pune,240", "Delhi,120", "Pune,60", "Delhi,80", "Goa,300"]',
         code='''orders = ["Pune,240", "Delhi,120", "Pune,60", "Delhi,80", "Goa,300"]
groups = {}
for city, amt in sorted((o.split(",")[0], int(o.split(",")[1])) for o in orders):
    groups.setdefault(city, []).append(amt)
for city, amts in groups.items():
    print(city, sum(amts) / len(amts))
''', explain='Average must be computed in the reducer from all values. Averaging partial averages from different mappers would give wrong answers.'),
    dict(level='medium', title='Count words longer than 4 letters', stmt='Write map and reduce logic that counts only words longer than 4 letters.', inp='["Hadoop stores data", "Spark caches data in memory"]',
         code='''lines = ["Hadoop stores data", "Spark caches data in memory"]
pairs = [(w.lower(), 1) for l in lines for w in l.split() if len(w) > 4]
counts = {}
for w, one in sorted(pairs):
    counts[w] = counts.get(w, 0) + one
print(counts)
''', explain='Filtering in the map step means fewer pairs are shuffled. Doing work early, before the network, is a key MapReduce habit.'),
    dict(level='medium', title='Which tool for the job?', stmt='For each workload, print whether batch Hadoop fits ("yes") or not ("no").', inp='scan 2 years of logs · show one user profile in 50 ms · nightly sales report · live fraud alert in 1 s',
         code='''workloads = {"scan 2 years of logs": "batch", "show one user profile in 50 ms": "lookup",
             "nightly sales report": "batch", "live fraud alert in 1 s": "stream"}
for w, kind in workloads.items():
    print(f"{w:32}: {'yes' if kind == 'batch' else 'no'}")
''', explain='Batch fits Hadoop. Lookups need a database or HBase; streams need Kafka with Flink or Spark Streaming.'),
    dict(level='business', title='NameNode memory for small files', stmt='A team stores 40 crore small files of 200 KB each (one block per file). Using about 150 bytes per file object and 150 per block object, estimate the NameNode memory. Then estimate it if the same data were packed into 256 MB files.', inp='40 crore files × 200 KB · 150 B per object',
         code='''files = 40_00_00_000
small_gb = files * 2 * 150 / 1024**3
data_mb = files * 200 / 1024
big_files = data_mb / 256
big_gb = big_files * 2 * 150 / 1024**3
print(f"Small files : ~{small_gb:.0f} GB of NameNode heap")
print(f"Packed files: ~{big_gb:.2f} GB")
''', explain='About 112 GB versus well under 1 GB for the same bytes. The small-files problem is one of the main things Hadoop did not solve by itself (Module 7).'),
    dict(level='business', title='Cost of keeping cold data replicated', stmt='Cold data of 900 TB is kept at 3× replication. Switching it to erasure coding (1.5×) frees raw disk. At Rs 2,500 per TB of raw disk, how much hardware does the switch save?', inp='900 TB · 3× → 1.5× · Rs 2,500/TB',
         code='''saved_tb = 900 * (3 - 1.5)
print(f"Saved {saved_tb:.0f} TB raw = Rs {saved_tb * 2500 / 1e5:.1f} lakh")
''', explain='1,350 TB of raw disk, about Rs 33.8 lakh of hardware (illustrative price), plus the power and rack space for it.'),
]

SCN_INTRO = 'Interviewers often test architecture knowledge by giving you a problem and asking which part of Hadoop handles it.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · architecture</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Walk me through what happens when I run a Hadoop job.”</h4>
      <p class="scn__situation">The interviewer wants the end-to-end flow, naming which component does what, for a job that reads a file in HDFS and writes results.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you connect HDFS, YARN and MapReduce into one story?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>The file is already in <b>HDFS</b>: blocks on DataNodes, metadata on the NameNode.</li>
          <li>The client submits the job to the <b>ResourceManager</b>, which starts an <b>ApplicationMaster</b> in a container.</li>
          <li>The AM computes input splits from block locations and asks YARN for containers on (or near) those nodes.</li>
          <li><b>NodeManagers</b> launch map tasks; each reads its block locally and writes partitioned, sorted output to local disk.</li>
          <li>Reducers <b>shuffle</b> (fetch) their partitions from all mappers, merge them and run reduce, writing output to HDFS.</li>
          <li>The AM tracks progress and re-runs failed tasks; when done, it reports success and exits.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> mentioning the JobTracker for a modern cluster (that was Hadoop 1).</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">ML team · architecture</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The ML training job takes 14 hours in MapReduce</h4>
      <p class="scn__situation">A data scientist implemented a training algorithm with 30 iterations as 30 chained MapReduce jobs over the same 2 TB data set. It takes 14 hours.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know which problems MapReduce did not solve, and what replaced it?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Each MapReduce job rereads the 2 TB from HDFS and writes its results back to HDFS, so 30 iterations mean about 60 full passes over disk, plus job start-up each time.</li>
          <li>Move it to <b>Spark</b> on the same YARN cluster: load the data once, <code>cache()</code> it in executor memory, and iterate in memory. Spark MLlib already has many algorithms.</li>
          <li>Keep HDFS as the storage; only the engine changes.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “Add more nodes.” The waste is in the repeated I/O, not the lack of machines.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · capacity</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Each team wants its own cluster</h4>
      <p class="scn__situation">Three departments each ask for a separate 30-node Hadoop cluster so that “others don't slow us down”. Finance asks whether that is necessary.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand what YARN was built for?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Separate clusters sit idle outside each team's busy hours, and data must be copied between them.</li>
          <li>One shared cluster with <b>YARN queues</b> (Capacity or Fair Scheduler) gives each team a guaranteed share, lets them borrow idle capacity, and keeps one copy of shared data.</li>
          <li>Isolation concerns are handled with queue limits, pre-emption, and per-team security (Kerberos, Ranger policies).</li>
          <li>Separate clusters can still make sense for strict regulatory isolation or very different software versions.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> dismissing the teams' concern; explain how queues address it.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Banking · data correction</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>“Just update the wrong rows in HDFS”</h4>
      <p class="scn__situation">A bug wrote wrong interest amounts into 5,000 rows of a 2 TB table stored as files in HDFS. A manager asks you to “run an UPDATE on those rows”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know HDFS is write-once, and how updates are handled in practice?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>HDFS files can't be edited in the middle. Plain Hive tables on files are corrected by <b>rewriting</b> the affected partitions (for example only the dates involved).</li>
          <li>Modern table formats (Apache Iceberg, Delta Lake, Hudi) or Hive ACID tables support <code>UPDATE</code>/<code>MERGE</code> by writing new files and tracking which rows are current.</li>
          <li>Fix the bug first, then reprocess from raw data if possible, keeping the raw layer unchanged.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> suggesting editing HDFS blocks directly.</p>
      </div></details>
    </article>'''
