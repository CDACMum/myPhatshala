import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Follow a file, then a job',
    intro='<p>Keep the <b>Event log</b> tab open. Every line is one step from this lesson: <code>create</code>, <code>addBlock</code> with its pipeline, completion, job submission and tasks.</p>',
    racks=2, nodes=3, features=['upload', 'job', 'fail'],
    **{'try': [
        dict(text='Choose <b>300 MB</b> and upload. How many blocks? Note the 3 DataNodes in each block\'s pipeline in the Event log.', on='upload-done'),
        dict(text='Open <b>NameNode metadata</b>: the last block is smaller. Which racks hold each block?'),
        dict(text='Run the job. One map task per block (M1, M2, M3), then the shuffle (violet) and 2 reducers.', on='job-done'),
        dict(text='Upload again and stop a node while a block is being written. The pipeline carries on with the remaining nodes.', on='node-stop'),
    ]},
)))

META = dict(
    module='03-how-a-cluster-works', lesson='02-the-life-of-a-file-and-a-job-end-to-end', n='3.2',
    module_label='Module 3 · How one Hadoop cluster works',
    title='The life of a file and a job, end to end',
    desc='The HDFS write path (create, addBlock, pipeline, packets, acks, complete), the read path (block locations, nearest replica, checksums) and the life of a MapReduce job on YARN (staging, ApplicationMaster, containers, map, spill, shuffle, reduce, commit, _SUCCESS), with failure recovery at each step. Animations, a playground, Python you can run, quiz and interview scenarios.',
    og_desc='Two commands, hundreds of messages: follow a file into HDFS and a job through YARN, step by step.',
    minutes=28, level='Beginner → Advanced',
    lead='Riya types two commands: put a file into HDFS, then run a job on it. Behind them, a dozen machines exchange hundreds of messages. This lesson follows every one: how a file is created, split into blocks and pushed through a pipeline of DataNodes; how it is read back from the nearest replica; and how a job travels from the client to the ResourceManager, its ApplicationMaster, map and reduce tasks, and finally a new file in HDFS. It is the map you will use for every later module.',
    chips=['Write + read anatomy', 'Job lifecycle animation', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Simulate the write path in Python',
    intro='<p>This program does what the HDFS client does when you upload a file: cut it into blocks, ask a (pretend) NameNode for three DataNodes per block following the rack rule, and count the 64 KB packets that will travel through each pipeline.</p>',
    code='''import math

racks = {"r1": ["dn1", "dn2"], "r2": ["dn3", "dn4"]}

def add_block(n):
    """Pretend NameNode: replica 1 on any node, 2 on the other rack, 3 next to 2."""
    first_rack = "r1" if n % 2 == 0 else "r2"
    other = "r2" if first_rack == "r1" else "r1"
    return [racks[first_rack][n % 2], racks[other][0], racks[other][1]]

size_mb, block_mb, packet_kb = 300, 128, 64
blocks = math.ceil(size_mb / block_mb)
for n in range(blocks):
    mb = min(block_mb, size_mb - n * block_mb)
    pipeline = add_block(n)
    packets = math.ceil(mb * 1024 / packet_kb)
    print(f"block {n + 1}: {mb:>3} MB -> {' -> '.join(pipeline)} ({packets} packets)")
''',
    anno=[
        ('def add_block(n):', 'Plays the NameNode\'s <code>addBlock</code> call: returns the pipeline of DataNodes for the next block.'),
        ('return [racks[first_rack][n % 2], racks[other][0], racks[other][1]]', 'Default placement: one replica on one rack, the next two together on another rack.'),
        ('packets = math.ceil(mb * 1024 / packet_kb)', 'A 128 MB block travels as 2,048 packets of 64 KB, each acknowledged by every DataNode in the pipeline.'),
    ],
    tasks=[
        dict(label='1 · Write a file', hint='Press <b>Run</b>. Then upload 1,000 MB instead. How many blocks and pipelines?', code=None),
        dict(label='2 · Read from the nearest', hint='<b>Predict first:</b> the client runs on dn3. Which replica of each block does it read? Hadoop sorts replicas by network distance (0 same node, 2 same rack, 4 other rack).',
             code='''rack = {"dn1": "r1", "dn2": "r1", "dn3": "r2", "dn4": "r2"}
blocks = {"B1": ["dn1", "dn3", "dn4"], "B2": ["dn2", "dn1", "dn4"], "B3": ["dn4", "dn1", "dn2"]}
client = "dn3"

def dist(a, b):
    return 0 if a == b else 2 if rack[a] == rack[b] else 4

for b, reps in blocks.items():
    best = sorted(reps, key=lambda r: dist(client, r))[0]
    print(b, "read from", best, "distance", dist(client, best))
'''),
        dict(label='3 · Pipeline recovery', hint='DN3 dies while block 1 is being written. The client drops it and continues with the others. What replication does the block have until the NameNode fixes it?',
             code='''pipeline = ["dn1", "dn3", "dn4"]
dead = "dn3"
pipeline = [d for d in pipeline if d != dead]
print("Continue writing to:", pipeline)
print("Block has", len(pipeline), "of 3 replicas; NameNode will add one later")
'''),
        dict(label='4 · Job stages', hint='Print the stages of a job and the application state during each. Add a stage for the output committer.',
             code='''stages = [("submit to RM", "SUBMITTED"), ("waiting for AM container", "ACCEPTED"),
          ("AM running maps", "RUNNING"), ("shuffle + reduce", "RUNNING"),
          ("AM unregisters", "FINISHED")]
for i, (stage, state) in enumerate(stages, 1):
    print(f"{i}. {stage:26} state = {state}")
'''),
        dict(label='5 · Spot the error', hint='This job submission check should refuse to run when the output folder exists, but it never does. Find the bug.',
             code='''existing = {"/data/canteen_orders.csv", "/out/item_totals"}
output = "/out/item_totals"
if output in existing == True:
    print("FileAlreadyExistsException: output directory exists")
else:
    print("Job submitted")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Splitting a file into blocks, one line at a time',
    intro='<p>Watch the client cut a 300 MB file into blocks, asking for a new pipeline each time. Notice how the last block is smaller.</p>',
    code='''size_mb, block_mb = 300, 128
offset = 0
blocks = []
while offset < size_mb:
    length = min(block_mb, size_mb - offset)
    blocks.append((offset, length))
    offset = offset + length
print(blocks)
''',
    notes={5: 'Block :: The last block only holds what is left.', 7: 'Next :: Move the offset to the start of the next block.'},
)

WORKED_INTRO = 'Three calculations that come straight from the write path and the job lifecycle: how much traffic a write creates, how long a write takes, and a full job timeline. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='HDFS · write traffic', title='How much data crosses the network when you upload 1 GB?',
         problem='<p>A client outside the cluster uploads a <b>1 GB</b> file with replication 3. Every replica is sent once over the network (client → DN1, DN1 → DN2, DN2 → DN3). The second and third replicas are on another rack from the first. How many GB travel in total, and how many cross between racks?</p>',
         inp='1 GB · replication 3 · replica 1 on rack A, replicas 2–3 on rack B',
         approach=['Total sent = size × replication (each replica crosses one link).',
                   'Cross-rack: client → DN1 (the client is outside), DN1 → DN2 (rack A to B).',
                   'DN2 → DN3 stays inside rack B.'],
         code='''size_gb, replication = 1, 3
hops = [("client -> DN1", "into rack A"), ("DN1 -> DN2", "rack A -> rack B"), ("DN2 -> DN3", "inside rack B")]
total = size_gb * replication
cross = sum(size_gb for hop, where in hops if "->" in where)
print("Total sent:", total, "GB")
print("Crossing racks or entering the cluster:", cross + size_gb, "GB")
for hop, where in hops:
    print(f"  {hop:12} {where}")
''', notes={4: 'Cross :: Only the DN1 → DN2 hop goes between racks inside the cluster.'},
         tryit='If the client runs on a DataNode, replica 1 is written locally: no network for the first copy. That is why bulk loads often run on cluster nodes.'),
    dict(level='i', tag='HDFS · write time', title='How long does a pipeline write take?',
         problem='<p>A pipeline streams packets: DN1 forwards each packet to DN2 while receiving the next one, so the three copies are written <b>at the same time</b>, limited by the slowest link. Estimate the time to upload <b>10 GB</b> when the slowest link is <b>200 MB/s</b>, versus writing the three copies one after another.</p>',
         inp='10 GB · slowest link 200 MB/s · 3 replicas',
         approach=['Pipelined: time ≈ size ÷ slowest link speed.',
                   'Sequential (one copy after another): 3 × that.',
                   'Print both.'],
         code='''size_mb = 10 * 1024
slowest = 200
pipelined = size_mb / slowest
sequential = 3 * pipelined
print(f"Pipelined : {pipelined:.0f} s")
print(f"Sequential: {sequential:.0f} s")
''', notes={3: 'Pipeline :: All three copies are written as the packets flow.'},
         tryit='Make one DataNode\'s disk slow (80 MB/s). The whole pipeline slows to that speed, which is why one bad disk can hurt many writes.'),
    dict(level='a', tag='MapReduce · job timeline', title='Estimate a whole job, stage by stage',
         problem='<p>A job reads <b>40 GB</b> (128 MB splits). The cluster can run <b>60</b> map tasks at once. Each map takes <b>40 s</b>. Starting the ApplicationMaster takes <b>15 s</b>; after the maps, the shuffle and reduce take <b>90 s</b>; committing takes <b>5 s</b>. Estimate the total time.</p>',
         inp='40 GB · 128 MB splits · 60 slots · 40 s/map · AM 15 s · shuffle+reduce 90 s · commit 5 s',
         approach=['Splits = 40 GB ÷ 128 MB.',
                   'Map waves = splits ÷ 60, rounded up; map time = waves × 40 s.',
                   'Total = AM + map time + shuffle/reduce + commit.'],
         code='''import math
splits = math.ceil(40 * 1024 / 128)
waves = math.ceil(splits / 60)
stages = {"start AM": 15, "maps": waves * 40, "shuffle + reduce": 90, "commit": 5}
for s, secs in stages.items():
    print(f"{s:17}: {secs:>4} s")
print(f"Total: {sum(stages.values())} s for {splits} maps in {waves} waves")
''', notes={2: 'Splits :: One map task per 128 MB split.'},
         tryit='The reducers really start fetching after 5% of maps finish, overlapping with the map phase. How would that change the estimate?'),
]

QUIZ = mix([
    dict(q='During an HDFS write, how does data reach the second and third DataNodes?', options=['The client sends it to each DataNode separately', 'Through a pipeline: DN1 forwards to DN2, which forwards to DN3', 'Via the NameNode', 'The ResourceManager copies it later'], answer=1,
         why='Data flows in a <b>pipeline</b>, and acknowledgements flow back along the same chain.'),
    dict(q='Which NameNode call gives the client the DataNodes for the next block?', options=['complete()', 'addBlock()', 'getBlockLocations()', 'renewLease()'], answer=1,
         why='<code>addBlock</code> allocates a new block ID and returns the pipeline of target DataNodes.'),
    dict(q='When reading a file, which replica does the client use first?', options=['A random one', 'The closest one by network distance', 'Always the first replica written', 'The one on the NameNode'], answer=1,
         why='The NameNode returns locations sorted by distance from the client; it reads the nearest and falls back to others if needed.'),
    dict(q='What does the client do if a checksum does not match while reading?', options=['Returns the corrupt bytes', 'Reads another replica and reports the corrupt one to the NameNode', 'Deletes the file', 'Restarts the cluster'], answer=1,
         why='Checksums catch corruption; the client switches replica and the bad one is replaced.'),
    dict(q='Who launches the MapReduce ApplicationMaster?', options=['The client, on the edge node', 'The ResourceManager, in a container on a NodeManager', 'The NameNode', 'The JobHistory Server'], answer=1,
         why='The RM allocates a container and asks a NodeManager to start the AM there. The application state goes from ACCEPTED to RUNNING.'),
    dict(q='Where do map tasks write their intermediate output?', options=['To HDFS with 3 replicas', 'To the local disk of the node they run on', 'To the NameNode', 'To the client'], answer=1,
         why='Map outputs are temporary, so they go to local disk (no replication). That is why a lost node forces finished maps to be re-run.'),
    dict(q='A job fails immediately with FileAlreadyExistsException. Why?', options=['The input file is missing', 'The output directory already exists; MapReduce refuses to overwrite it', 'HDFS is full', 'The jar is corrupt'], answer=1,
         why='The output check happens at submission to protect previous results. Delete or rename the old output, or choose a new path.'),
    dict(q='What does the _SUCCESS file in an output directory mean?', options=['The input was valid', 'The job completed and its output was committed', 'The NameNode is healthy', 'The file is compressed'], answer=1,
         why='The output committer writes <code>_SUCCESS</code> after all tasks succeed; workflows wait for it before reading the output.'),
])

REVISION = [
    '<b>Write:</b> <code>create</code> (lease) → per block <code>addBlock</code> → 64 KB packets through DN1 → DN2 → DN3, acks back → <code>complete</code>.',
    'New pipeline for each block; last block only as big as needed.',
    '<b>Read:</b> <code>getBlockLocations</code> (sorted by distance) → read nearest DataNode directly → verify CRC → next block.',
    'Masters never carry data. Pipeline failure → continue with remaining DataNodes; NameNode re-replicates later.',
    '<b>Job:</b> client checks output dir, computes splits, uploads jar/conf/splits to staging, submits to RM.',
    'RM starts <b>MRAppMaster</b> (ACCEPTED → RUNNING); AM requests containers near each split.',
    'Map → sort buffer (100 MB) → spill to <b>local disk</b> → partitions. Reducers fetch (shuffle) after 5% of maps.',
    'Reduce → write to HDFS → output committer → <code>part-r-*</code> + <code>_SUCCESS</code>; AM unregisters; history to JobHistory.',
]
FAQ = [
    ('Explain the anatomy of a file write in HDFS.', 'The client calls create() on the DistributedFileSystem, which makes an RPC to the NameNode; the NameNode checks permissions and that the file does not exist, records it and grants a lease. The client\'s output stream splits data into packets in a data queue. A DataStreamer asks the NameNode for a new block (addBlock), which returns a block ID and a pipeline of DataNodes chosen by the placement policy. Packets are sent to the first DataNode, which stores and forwards them to the second, and so on; acknowledgements return along the pipeline and packets are removed from the ack queue. This repeats for each block. On close(), remaining packets are flushed and acknowledged, and the client calls complete() on the NameNode.'),
    ('Explain the anatomy of a file read in HDFS.', 'The client calls open(); the DistributedFileSystem asks the NameNode for the locations of the first blocks, sorted by network distance from the client. The input stream connects to the closest DataNode for the first block and streams the data, verifying checksums. At the end of the block it connects to the best DataNode for the next block, fetching more locations from the NameNode as needed. If a DataNode fails or a checksum does not match, it tries the next replica and reports the problem.'),
    ('What happens if a DataNode fails during a write?', 'The pipeline is closed, packets in the ack queue are put back at the front of the data queue, the failed DataNode is removed, the current block on the good DataNodes gets a new generation stamp (so the partial replica on the failed node will be discarded later), and writing continues with the remaining DataNodes. The NameNode notices the block is under-replicated and creates another replica afterwards.'),
    ('Describe the steps in running a MapReduce job on YARN.', 'The client checks the output path, computes input splits, copies the job jar, configuration and split information to a staging directory in HDFS, and submits the application to the ResourceManager. The RM allocates a container and a NodeManager launches the MRAppMaster. The AM requests containers for map tasks (with locality preferences) and later reduce tasks; NodeManagers launch them. Maps write partitioned, sorted output to local disk; reducers shuffle and merge it, run the reduce function and write output to HDFS through the output committer. The AM then cleans up, writes _SUCCESS, unregisters from the RM, and job history is available from the JobHistory Server.'),
    ('Why are map outputs written to local disk and not to HDFS?', 'They are intermediate and short-lived; replicating them to HDFS would triple the write cost and network traffic for data that is deleted once the job finishes. The trade-off is that if a node is lost before reducers have fetched its map outputs, those map tasks must be re-run.'),
]

PRACTICE_INTRO = 'Practise the two journeys with numbers and small simulations, from counting blocks to building a job timeline.'
PROBLEMS = [
    dict(level='easy', title='Blocks and last block', stmt='A 1,000 MB file is written with 128 MB blocks. How many blocks, and how big is the last one?', inp='1000 MB · 128 MB',
         code='''import math
n = math.ceil(1000 / 128)
print(n, "blocks; last block", 1000 - (n - 1) * 128, "MB")
''', explain='8 blocks; the last holds 104 MB. HDFS does not pad it to 128 MB on disk.'),
    dict(level='easy', title='Packets per block', stmt='How many 64 KB packets make up one full 128 MB block?', inp='128 MB · 64 KB',
         code='print(128 * 1024 // 64, "packets")\n', explain='2,048 packets, each acknowledged by every DataNode in the pipeline.'),
    dict(level='easy', title='Replicas written', stmt='A 2 GB file with replication 3: how many block replicas are written in total (128 MB blocks)?', inp='2 GB · 128 MB · ×3',
         code='print(2 * 1024 // 128 * 3, "block replicas")\n', explain='16 blocks × 3 = 48 replicas, each one a file (plus a checksum file) on some DataNode\'s disk.'),
    dict(level='medium', title='Nearest replica for every block', stmt='For a client on dn2, print the best replica of each block using distance 0/2/4.', inp='racks r1: dn1, dn2 · r2: dn3, dn4 · B1 [dn3, dn4, dn1] · B2 [dn4, dn3, dn2]',
         code='''rack = {"dn1": "r1", "dn2": "r1", "dn3": "r2", "dn4": "r2"}
d = lambda a, b: 0 if a == b else 2 if rack[a] == rack[b] else 4
for b, reps in {"B1": ["dn3", "dn4", "dn1"], "B2": ["dn4", "dn3", "dn2"]}.items():
    print(b, "->", min(reps, key=lambda r: d("dn2", r)))
''', explain='B1 is read from dn1 (same rack), B2 from dn2 itself (same node, distance 0).'),
    dict(level='medium', title='Map waves for a job', stmt='A job reads 25 GB in 128 MB splits on a cluster with 50 map slots. How many map tasks and waves?', inp='25 GB · 128 MB · 50 slots',
         code='''import math
maps = math.ceil(25 * 1024 / 128)
print(maps, "maps in", math.ceil(maps / 50), "waves")
''', explain='200 maps in 4 waves. Doubling the slots would halve the map phase, but not the AM start-up or the reduce phase.'),
    dict(level='medium', title='Output files of a job', stmt='Print the names of the output files of a job with 4 reducers (Hadoop naming), plus the success marker.', inp='4 reducers',
         code='''files = [f"part-r-{i:05d}" for i in range(4)] + ["_SUCCESS"]
print(files)
''', explain='One file per reducer: <code>part-r-00000</code>… Map-only jobs produce <code>part-m-*</code> files instead.'),
    dict(level='business', title='Bulk load: client outside vs on the cluster', stmt='A team uploads 5 TB per night. From an edge node outside the racks, every replica crosses the network. From a DataNode, replica 1 is written locally. How many TB of network traffic does each approach create?', inp='5 TB · replication 3',
         code='''tb = 5
outside = tb * 3
on_node = tb * 2
print("From an edge node :", outside, "TB over the network")
print("From a DataNode   :", on_node, "TB over the network")
''', explain='15 TB vs 10 TB a night. Loading from cluster nodes (or with distributed loaders) saves a third of the network traffic, at the cost of the first node filling faster unless writes are spread out.'),
    dict(level='business', title='SLA check for a nightly job', stmt='The nightly job must finish within 30 minutes. Using the stage times below, does it meet the SLA, and how much slack is left?', inp='queue wait 4 min · AM start 0.5 min · maps 14 min · shuffle+reduce 8 min · commit 0.5 min',
         code='''stages = {"queue wait": 4, "AM start": 0.5, "maps": 14, "shuffle + reduce": 8, "commit": 0.5}
total = sum(stages.values())
print(f"Total {total} min; SLA met: {total <= 30}; slack {30 - total} min")
''', explain='27 minutes, 3 minutes of slack. The queue wait (time in ACCEPTED) is often forgotten in SLA estimates.'),
]

SCN_INTRO = 'Interviewers love asking you to narrate a write, a read or a job, and then break one step. Practise the narration and the failure cases.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“A DataNode dies while I'm writing a file. What happens?”</h4>
      <p class="scn__situation">You have just explained the write pipeline. The interviewer asks what happens if DN2 crashes halfway through block 3.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know pipeline recovery, not just the happy path?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>The client notices missing acknowledgements and closes the pipeline.</li>
          <li>Unacknowledged packets are put back in the queue so nothing is lost.</li>
          <li>DN2 is removed; the block on DN1 and DN3 gets a new generation stamp so DN2's partial copy will later be recognised as stale and deleted.</li>
          <li>Writing continues to DN1 and DN3. The write succeeds as long as at least the minimum replication (1 by default) is met.</li>
          <li>The NameNode later sees block 3 has 2 replicas and schedules a third.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “The write fails and the user must retry.”</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“could only be written to 0 of the 1 minReplication nodes”</h4>
      <p class="scn__situation">A student's freshly installed cluster accepts <code>hdfs dfs -mkdir</code> but every <code>-put</code> fails with this message.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you map an error to the write step where it happens?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><code>mkdir</code> only talks to the NameNode, so metadata works. The error comes at <code>addBlock</code>: the NameNode found <b>no DataNode</b> it could place a block on.</li>
          <li>Check <code>jps</code>: is a DataNode running? Check <code>hdfs dfsadmin -report</code>: live DataNodes and free space.</li>
          <li>Common causes: the DataNode failed to start (often a cluster-ID mismatch after re-formatting the NameNode), the disk is full, or the DataNode can't reach the NameNode (hostname/firewall).</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> reformatting the NameNode again; that wipes metadata and often causes the ID mismatch in the first place.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Data platform · operations</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Jobs stay in ACCEPTED for an hour</h4>
      <p class="scn__situation">Every morning, newly submitted jobs sit in ACCEPTED state for a long time before running, although the cluster “isn't that busy”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know what ACCEPTED means in the job lifecycle?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>ACCEPTED means the RM has the application but has not yet started its <b>ApplicationMaster</b> container.</li>
          <li>Check the queue: it may be at its capacity or at its limit for AMs (<code>maximum-am-resource-percent</code>), so new AMs wait even if some memory is free.</li>
          <li>Check whether the AM container size fits on any node, and whether many small jobs are each holding an AM.</li>
          <li>Fixes: adjust queue capacities or AM limits, schedule big jobs at different times, combine many tiny jobs.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> killing and resubmitting jobs; they go back to the end of the queue.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Data engineering · pipelines</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The downstream job read half-written output</h4>
      <p class="scn__situation">A reporting job starts every day at 6 am and reads <code>/out/daily_sales</code>. Some days its numbers are too low. The upstream MapReduce job sometimes finishes after 6 am.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand output commit and how pipelines should wait for it?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Successful task output is only moved into the final folder at commit, but a downstream job can still start before or during it, or read an old partial folder.</li>
          <li>Make the reporting job depend on the upstream job's completion: in Airflow or Oozie, wait for the <code>_SUCCESS</code> file (or the job status) before starting.</li>
          <li>Write each day to its own dated folder, so readers never see a folder that is being rewritten.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “Just start the report later.” Time-based guesses break on slow days.</p>
      </div></details>
    </article>'''
