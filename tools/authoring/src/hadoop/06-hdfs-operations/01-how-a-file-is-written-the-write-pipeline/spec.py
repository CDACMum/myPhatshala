import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-hdfs-operations', lesson='01-how-a-file-is-written-the-write-pipeline', n='6.1',
    module_label='Module 6 · HDFS operations',
    title='How a file is written: the write pipeline',
    desc='The anatomy of an HDFS write, from real Hadoop 3.5.0 logs: create, addBlock, the DataNode pipeline, 64 KB packets of 512-byte checksummed chunks, the ack queue, completeFile and the _COPYING_ rename. Two real failures: a DataNode killed mid-block (generation stamp bump, pipeline continues on two nodes, later re-replication) and a pipeline setup failure (firstBadLink, excluded node, abandoned block). Python pipeline simulator, quiz and interview scenarios.',
    og_desc='Three copies, but the client sends each byte once. Read a real HDFS write pipeline in the logs, including a DataNode killed mid-write.',
    minutes=28, level='Intermediate',
    lead='When you write a file to HDFS with replication 3, your client uploads the data only once: the DataNodes copy it along a pipeline. This lesson follows a real 134 MB upload through the client, NameNode and DataNode logs, packet by packet, and then breaks it on purpose by killing DataNodes during a write to show how HDFS recovers without failing the upload.',
    chips=['Real client + DataNode logs', 'Failure during write', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Simulate a pipeline with acknowledgements',
    intro='<p>This program sends packets down a three-DataNode pipeline. Each packet stays in the ack queue until every DataNode has stored it. Watch which packets are still unacknowledged at each step.</p>',
    code='''from collections import deque

pipeline = ["dn-1", "dn-3", "dn-4"]
stored = {dn: [] for dn in pipeline}
data_queue = deque(range(5))          # packet numbers 0..4
ack_queue = deque()

while data_queue or ack_queue:
    if data_queue:
        p = data_queue.popleft()
        for dn in pipeline:            # dn-1 stores and forwards, and so on
            stored[dn].append(p)
        ack_queue.append(p)
        print(f"sent packet {p}  waiting for acks: {list(ack_queue)}")
    if len(ack_queue) > 1 or not data_queue:
        done = ack_queue.popleft()     # acks come back in order
        print(f"  ack for packet {done} from {len(pipeline)} DataNodes")

for dn, packets in stored.items():
    print(dn, "has", packets)
''',
    anno=[
        ('for dn in pipeline:            # dn-1 stores and forwards, and so on', 'In real HDFS each DataNode writes the packet to disk and forwards it at the same time; the client only sends to dn-1.'),
        ('ack_queue.append(p)', 'The client keeps the packet in memory until it is acknowledged, so it can resend it if a DataNode fails.'),
        ('done = ack_queue.popleft()     # acks come back in order', 'Acks return in packet order, from the last DataNode back to the client.'),
    ],
    tasks=[
        dict(label='1 · Send five packets', hint='Press <b>Run</b>. Then change the number of packets to 8.', code=None),
        dict(label='2 · How many packets?', hint='<b>Predict first:</b> how many data packets does a full 128 MB block need, and the real 140,760,270-byte file? Each full packet carries 64,512 data bytes.',
             code='''import math
data_per_packet = 64_512
block = 134_217_728
size = 140_760_270
b1 = math.ceil(block / data_per_packet)
b2 = math.ceil((size - block) / data_per_packet)
print("block 1:", b1, "data packets; block 2:", b2, "; total", b1 + b2)
print("the real log numbered 2,186 packets: data packets plus a few control packets")
'''),
        dict(label='3 · Bytes on the wire', hint='Compare network traffic leaving the client when it sends 3 copies itself versus using a pipeline, for 1 GB with replication 3.',
             code='''gb = 1
print("client sends every copy:", gb * 3, "GB from the client")
print("pipeline:", gb, "GB from the client,", gb * 2, "GB forwarded between DataNodes")
'''),
        dict(label='4 · Failure mid-block', hint='dn-3 dies after packet 2. Remove it from the pipeline, put unacknowledged packets back, and continue. Which DataNodes end up with every packet?',
             code='''pipeline = ["dn-1", "dn-3", "dn-4"]
stored = {dn: [] for dn in pipeline}
for p in range(6):
    if p == 3 and "dn-3" in pipeline:
        pipeline.remove("dn-3")        # recovery: continue with the survivors
        print("dn-3 failed; new pipeline", pipeline, "- generation stamp bumped")
    for dn in pipeline:
        stored[dn].append(p)
print({dn: len(ps) for dn, ps in stored.items()})
'''),
        dict(label='5 · Spot the error', hint='This client removes packets from the ack queue as soon as they are sent. Why is that dangerous if a DataNode fails? Make it wait for the ack.',
             code='''ack_queue = []
for p in range(3):
    print("sent", p)
    # bug: forgetting the packet immediately
print("unacknowledged packets kept for resending:", ack_queue)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: trace your own write pipeline',
    intro='<p>This script uploads a 134 MB file from datanode-1 with client debug logging, then summarises the pipelines, packets and acknowledgements from the log. Save it as <code>write_trace.py</code> in the <code>hdfs-lab</code> folder (it needs <code>canteen_orders.csv</code> copied to <code>/tmp</code> inside datanode-1, as in Lesson 5.1).</p>',
    items=[
        dict(title='Pipelines and packets of one upload', file='write_trace.py',
             cmd=open(os.path.join(HERE, 'write_trace.py')).read() + '\n# In the hdfs-lab folder:\n#   docker cp canteen_orders.csv lab5-datanode-1:/tmp/\n#   python3 write_trace.py',
             output='''blk_1073741860 pipeline: datanode-1 -> datanode-3 -> datanode-4
blk_1073741861 pipeline: datanode-1 -> datanode-2 -> datanode-5
packets sent: 2186, acknowledged by all 3 DataNodes: 2186
data bytes per full packet: 64512
first log line 09:43:26,161, last 09:43:28,775''',
             note='Real output, with 5 DataNodes. The first replica is always on datanode-1 (the writer). The pipeline order follows network distance from the writer, so block 2 visits datanode-2 (same rack) before datanode-5 (other rack); the replicas still cover both racks.'),
    ],
)

TRACE = dict(
    heading='Pipeline recovery, one line at a time',
    intro='<p>Follow the client when the middle DataNode fails: unacknowledged packets go back to the front of the data queue and the generation stamp changes.</p>',
    code='''pipeline = ["dn-1", "dn-3", "dn-4"]
gen_stamp = 1023
acked, unacked = [0, 1, 2], [3, 4]
failed = "dn-3"
pipeline.remove(failed)
gen_stamp += 1
resend = unacked
print(pipeline, "blk_1073741847_%d" % gen_stamp, "resend", resend)
''',
    notes={5: 'Exclude :: The failed DataNode leaves the pipeline.',
           6: 'New version :: 1023 → 1024, as in the real log. Old partial replicas with 1023 become stale.',
           7: 'Resend :: Packets that never got all their acks are sent again.'},
)

WORKED_INTRO = 'Three write-path calculations engineers make: upload time, network load on racks, and how much data is at risk while a pipeline runs short. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Planning · ingestion', title='How long will this upload take?',
         problem='<p>An edge node with a 10 Gbit/s link (about 1,100 MB/s usable) uploads 2 TB of logs with replication 3. DataNode disks are not the bottleneck. Estimate the time, and compare with a client that had to send all 3 copies itself.</p>',
         inp='2 TB · 1,100 MB/s · replication 3',
         approach=['Pipeline: the client sends the data once.',
                   'Time = size / link speed.',
                   'Without a pipeline it would send 3×.'],
         code='''tb_mb = 2 * 1024 * 1024
rate = 1100
once = tb_mb / rate / 3600
print(f"pipeline: {once:.1f} h   sending 3 copies itself: {once * 3:.1f} h")
''', notes={3: 'Once :: Replication traffic is between DataNodes, not on the client link.'},
         tryit='Run 4 upload clients on different edge nodes in parallel: the cluster, not one link, becomes the limit.'),
    dict(level='i', tag='Network · racks', title='Cross-rack traffic for a day of writes',
         problem='<p>Jobs write 30 TB per day with replication 3 from tasks running on DataNodes. With the default placement, each block crosses racks once. How much traffic crosses the core switch per day, and the average rate in Gbit/s?</p>',
         inp='30 TB/day · 1 cross-rack copy per block',
         approach=['Cross-rack bytes = data written × 1.',
                   'Average rate = bytes / 86,400 s.',
                   'Convert to Gbit/s.'],
         code='''tb = 30
bytes_cross = tb * 2**40
gbit_s = bytes_cross * 8 / 86_400 / 1e9
print(f"{tb} TB/day across racks = {gbit_s:.1f} Gbit/s on average")
''', notes={3: 'Rate :: Peaks are much higher than the daily average.'},
         tryit='If all three replicas went to different racks, it would double. That is why the default policy keeps two replicas in one rack.'),
    dict(level='a', tag='Risk · recovery', title='Data with fewer than 3 replicas during failures',
         problem='<p>During a busy hour, 200 pipelines are writing at once, each with on average 60 MB of its current block written. A DataNode that is part of 40 of these pipelines dies. Those pipelines continue with 2 replicas. How much just-written data briefly has only 2 replicas, and how long until re-replication at 500 MB/s cluster-wide?</p>',
         inp='40 affected pipelines · 64 MB average per block when complete · 500 MB/s',
         approach=['Affected blocks finish with 2 replicas: about 40 blocks of up to 128 MB.',
                   'Data at reduced redundancy ≈ 40 × 128 MB.',
                   'Time to fix = data / repair rate.'],
         code='''blocks, block_mb, rate = 40, 128, 500
data = blocks * block_mb
print(f"~{data:,} MB with 2 replicas, fixed in ~{data / rate:.0f} s")
''', notes={3: 'Upper bound :: Assumes each affected block grows to a full 128 MB.'},
         tryit='The real lab block was re-replicated 19 s after the write. Small risk windows like this are why replication 3 (not 2) is the default.'),
]

QUIZ = mix([
    dict(q='With replication 3, how many times does the client send each byte over the network?', options=['Once', 'Twice', 'Three times', 'It depends on the block size'], answer=0,
         why='The client sends to the first DataNode only; DataNodes forward along the pipeline.'),
    dict(q='Who chooses the DataNodes for a new block?', options=['The client', 'The NameNode, with the block placement policy', 'The first DataNode', 'YARN'], answer=1,
         why='The addBlock reply lists the DataNodes, e.g. replicas=.4, .6, .7.'),
    dict(q='What is a packet in the write pipeline?', options=['A whole block', 'A unit of about 64 KB of data with checksums', 'One line of the file', 'A DataNode heartbeat'], answer=1,
         why='The real log: 64,512 data bytes per packet, 126 chunks of 512 + 4 bytes.'),
    dict(q='When does the client remove a packet from its ack queue?', options=['As soon as it is sent', 'When all DataNodes in the pipeline have acknowledged it', 'When the block is full', 'When the NameNode says so'], answer=1,
         why='That way it can resend packets if a DataNode fails.'),
    dict(q='Which direction do acknowledgements travel?', options=['From the client to the DataNodes', 'From the last DataNode back through the others to the client', 'From the NameNode to the client', 'They are not used'], answer=1,
         why='DN3 → DN2 → DN1 → client.'),
    dict(q='A DataNode dies in the middle of writing a block. What happens by default?', options=['The upload fails', 'The client removes it, the generation stamp is bumped, and writing continues on the remaining DataNodes', 'All data is rewritten from the start', 'The NameNode stops'], answer=1,
         why='Real log: updatePipeline … newGS=1024 … newNodes=[.4, .7], then the upload finished.'),
    dict(q='Why does hdfs dfs -put write to a file ending in ._COPYING_?', options=['To compress it', 'So readers never see a half-written file under the final name; it is renamed at the end', 'Because HDFS needs it for replication', 'For encryption'], answer=1,
         why='We saw cmd=create …._COPYING_ and later cmd=rename.'),
    dict(q='Which replica does the NameNode usually hear about first when a block completes?', options=['The first in the pipeline', 'The last in the pipeline', 'Always the local one', 'None until the file closes'], answer=1,
         why='addStoredBlock .7, then .6, then .4: the last DataNode finishes first.'),
])

REVISION = [
    'Write = <b>create</b> (NameNode) → <b>addBlock</b> (DataNode list) → <b>pipeline</b> DN1 → DN2 → DN3 → <b>complete</b>.',
    'Client sends each byte <b>once</b>; DataNodes forward. Replicas are written in parallel.',
    'Packets: ~64 KB (64,512 data bytes = 126 × 512-byte chunks, each + 4-byte checksum).',
    'Acks flow back; packets stay in the <b>ack queue</b> until all DataNodes confirm.',
    'Block full → close pipeline → addBlock again. File visible under <code>._COPYING_</code> until renamed (put).',
    'DataNode fails mid-block → exclude it, <b>bump generation stamp</b>, continue on survivors; re-replicate later.',
    'Setup failure → “firstBadLink” → abandon block, exclude node, new block.',
    'Pipeline order = network distance from the writer; replicas still span racks.',
]
FAQ = [
    ('How does a client write a file to HDFS?', 'It asks the NameNode to create the file, then for each block asks for a list of DataNodes. It streams the block as packets to the first DataNode, which stores and forwards them to the second, which forwards to the third. Acknowledgements come back along the pipeline. When all data is written, the client tells the NameNode the file is complete.'),
    ('Does the data pass through the NameNode during a write?', 'No. The NameNode only handles metadata: creating the file, allocating blocks and recording finished replicas. Data flows from the client to DataNodes and between DataNodes.'),
    ('What happens if a DataNode fails during a write?', 'The client detects the error, removes that DataNode from the pipeline, moves unacknowledged packets back to the data queue, gets a new generation stamp for the block from the NameNode, and continues with the remaining DataNodes (possibly adding a replacement). The NameNode re-replicates the block later.'),
    ('What is the generation stamp?', 'A version number attached to each block (the part after the last underscore in blk_1073741847_1024). It is increased during pipeline recovery or append so that replicas left behind on failed DataNodes are recognised as stale and deleted.'),
    ('When can other clients read a file that is being written?', 'They can always see the file, and data in completed blocks. Data in the block being written becomes visible after hflush() (or when the block or file is closed). Only one client can write to a file at a time.'),
    ('Why is data sent in packets instead of whole blocks?', 'So that DataNodes can start forwarding while still receiving, keeping all three copies moving at once, and so that a failure only requires resending a few small packets, not a whole 128 MB block.'),
]

PRACTICE_INTRO = 'Pipeline exercises built on the numbers from the real logs.'
PROBLEMS = [
    dict(level='easy', title='Chunk arithmetic', stmt='A packet has 126 chunks of 512 data bytes, each with a 4-byte checksum. How many data bytes and total bytes per packet?', inp='126 chunks · 512 + 4 bytes',
         code='print(126 * 512, "data bytes,", 126 * 516, "bytes with checksums")\n', explain='64,512 data bytes and 65,016 bytes in total, exactly the packetSize in the client log.'),
    dict(level='easy', title='Packets per block', stmt='How many full 64,512-byte packets fill a 134,217,728-byte block?', inp='134,217,728 / 64,512',
         code='import math\nprint(math.ceil(134217728 / 64512))\n', explain='2,081 data packets (the last one partly full). The log\'s sequence numbers for block 1 run 0 to 2082 because it also counts small control packets, such as the empty last packet that closes the block.'),
    dict(level='easy', title='Second block size', stmt='The file is 140,760,270 bytes with 128 MB blocks. How big is the second block?', inp='140,760,270 − 134,217,728',
         code='print(140760270 - 134217728)\n', explain='6,542,542 bytes, matching addStoredBlock … (size=6542542).'),
    dict(level='medium', title='Order of the chain', stmt='From the DataNode “Receiving … src: … dest: …” lines, reconstruct the pipeline order.', inp='src/dest pairs from the real logs',
         code='''pairs = [("172.19.0.6", "172.19.0.7"), ("172.19.0.4", "172.19.0.4"), ("172.19.0.4", "172.19.0.6")]
nxt = {s: d for s, d in pairs if s != d}
node, chain = "172.19.0.4", ["172.19.0.4"]
while node in nxt:
    node = nxt[node]; chain.append(node)
print(" -> ".join(chain))
''', explain='172.19.0.4 → 172.19.0.6 → 172.19.0.7: datanode-1 → datanode-3 → datanode-4.'),
    dict(level='medium', title='Where did recovery happen?', stmt='updatePipeline reported newLength=40061952. How many packets had been fully acknowledged, and what fraction of the block was written?', inp='40,061,952 bytes · 64,512 per packet · 128 MB block',
         code='''print(40061952 // 64512, "packets;", f"{40061952 / 134217728:.0%} of the block")
''', explain='621 full packets, about 30% of the block, before datanode-3 died. The rest was written to two DataNodes.'),
    dict(level='medium', title='Abandoned block IDs', stmt='The final file has blocks …842, …844, …845, …846. Which block ID was abandoned?', inp='842 · 844 · 845 · 846',
         code='''ids = [842, 844, 845, 846]
print([i for i in range(ids[0], ids[-1] + 1) if i not in ids])
''', explain='…843, the block whose pipeline setup failed with firstBadLink 172.19.0.7.'),
    dict(level='business', title='Network cost of naive copying', stmt='A company ingests 5 TB a day from a branch office over a 1 Gbit/s link (about 110 MB/s). With a pipeline the link carries the data once. How many hours a day would the link be busy if it had to carry 3 copies?', inp='5 TB/day · 110 MB/s',
         code='''hours = 5 * 1024 * 1024 / 110 / 3600
print(f"once: {hours:.1f} h/day, three copies: {hours * 3:.1f} h/day")
''', explain='About 13 hours a day once, 40 hours for three copies: impossible. The pipeline makes remote ingestion feasible.'),
    dict(level='advanced', title='Simulate recovery with resend', stmt='Simulate 6 packets where dn-3 fails after acknowledging packet 2. Count packets each surviving DataNode stores, including resent ones (stored once each).', inp='6 packets · dn-3 fails after packet 2',
         code='''pipeline = ["dn-1", "dn-3", "dn-4"]
stored = {d: set() for d in pipeline}
for p in range(6):
    if p == 3:
        pipeline.remove("dn-3")
    for d in pipeline:
        stored[d].add(p)
print({d: sorted(s) for d, s in stored.items()})
''', explain='dn-1 and dn-4 hold all 6 packets; dn-3 only 0–2, a stale partial replica that the generation stamp lets HDFS discard.'),
]

SCN_INTRO = 'The write path is a favourite deep-dive question. Real log lines make your answer stand out.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · internals</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Walk me through what happens when I run hdfs dfs -put”</h4>
      <p class="scn__situation">The classic anatomy-of-a-write question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the order of steps and who talks to whom.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Client asks the NameNode to create <code>file._COPYING_</code>; NameNode checks permissions and existence and grants a lease.</li>
          <li>For each block the NameNode returns a block ID and three DataNodes (local, other rack, same rack as the second).</li>
          <li>Client streams ~64 KB packets to DN1, which stores and forwards to DN2, then DN3; acks return; packets wait in the ack queue until all confirm.</li>
          <li>After the last block the client calls complete; the NameNode closes the file; put renames it to the final name.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · failure</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A DataNode crashes during a large write. Does the job fail?</h4>
      <p class="scn__situation">A Spark job is writing 2 TB when a worker node reboots.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> pipeline recovery details.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Each affected writer detects the failure (bad ack or timeout), removes the DataNode, puts unacknowledged packets back in its data queue and asks the NameNode to update the pipeline.</li>
          <li>The NameNode bumps the block's generation stamp so the dead node's partial replica is stale; writing continues on the survivors (a replacement may be added depending on the policy).</li>
          <li>The NameNode re-replicates the block afterwards. The job continues; only tasks running on the rebooted node itself are retried by YARN/Spark.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Performance · writes</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Writes became slow cluster-wide after one disk started failing</h4>
      <p class="scn__situation">Job write stages are 3× slower than last week. No DataNode is dead.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you know a pipeline runs at the speed of its slowest member.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Every write that includes the slow DataNode waits for its acks, so one bad disk slows many pipelines.</li>
          <li>Look at DataNode metrics/logs for slow writes (e.g. “Slow BlockReceiver write data to disk” warnings) and the NameNode's slow-node reports.</li>
          <li>Fix: mark the failing volume bad or decommission the node, replace the disk; consider enabling slow-node detection and exclusion.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · consistency</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Can two programs write to the same HDFS file at once?”</h4>
      <p class="scn__situation">A student wants two scripts to append to one log file in HDFS.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> single-writer semantics and leases.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No. HDFS gives one writer a lease on a file; a second writer gets an exception until the lease is released or expires.</li>
          <li>Design instead: each writer writes its own file (e.g. one per task or per hour) in the same directory, and readers process the directory.</li>
          <li>This is exactly how MapReduce and Spark output works: part-00000, part-00001, …</li>
        </ul>
      </div></details>
    </article>
'''
