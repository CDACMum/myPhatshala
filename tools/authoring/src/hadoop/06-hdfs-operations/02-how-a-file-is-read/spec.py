import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-hdfs-operations', lesson='02-how-a-file-is-read', n='6.2',
    module_label='Module 6 · HDFS operations',
    title='How a file is read',
    desc='The anatomy of an HDFS read from real Hadoop 3.5.0 logs: getBlockLocations, replicas sorted by network distance, a client on a DataNode reading every block locally, a client off the DataNodes spreading reads, and per-512-byte checksums. A replica corrupted on purpose: the client reports “Found Checksum error … at 499712”, reads another replica (identical MD5), and the NameNode replaces the bad copy in 6 seconds. Python distance-sorting simulator, quiz and interview scenarios.',
    og_desc='Nearest replica first, and never trust a damaged one. Watch HDFS read around a corrupted block on a real cluster.',
    minutes=24, level='Intermediate',
    lead='Reading a file from HDFS is a conversation with the NameNode followed by direct transfers from DataNodes. This lesson shows both on a real cluster: which DataNode serves each block depending on where the client runs, how every 512 bytes are checked, and what happens when we corrupt a replica on purpose: the reader gets correct data anyway, and HDFS repairs itself within seconds.',
    chips=['Real client logs', 'Corruption repaired live', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Sort replicas by distance, like the NameNode',
    intro='<p>This program computes the network distance from a client to each replica (0 same node, 2 same rack, 4 other rack) and sorts the replica list, shuffling ties as HDFS does. Try it for a client on a DataNode and for one outside the racks.</p>',
    code='''import random
random.seed(3)
rack = {"dn-1": "/rack1", "dn-2": "/rack1", "dn-3": "/rack2", "dn-4": "/rack2"}

def distance(client, dn):
    if client == dn:
        return 0
    if rack.get(client) == rack[dn]:
        return 2
    return 4

def sorted_replicas(client, replicas):
    shuffled = random.sample(replicas, len(replicas))     # ties in random order
    return sorted(shuffled, key=lambda dn: distance(client, dn))

replicas = ["dn-1", "dn-2", "dn-3"]
for client in ["dn-2", "dn-4", "edge-node"]:
    order = sorted_replicas(client, replicas)
    print(f"{client:9} reads from {order[0]}   (order {order})")
''',
    anno=[
        ('if rack.get(client) == rack[dn]:', 'A client that is not in any rack (like an edge node or our namenode container) never matches, so every replica is distance 4.'),
        ('shuffled = random.sample(replicas, len(replicas))     # ties in random order', 'Shuffling before a stable sort keeps the distance order but randomises equal distances, spreading load. That is why the off-cluster read used several DataNodes.'),
    ],
    tasks=[
        dict(label='1 · Who reads from where?', hint='Press <b>Run</b>. Then add a client <code>"dn-3"</code>.', code=None),
        dict(label='2 · Chunk with the error', hint='<b>Predict first:</b> byte 500,000 was changed. Which 512-byte chunk is that, and where does it start?',
             code='''offset = 500_000
chunk = offset // 512
print("chunk", chunk, "starts at", chunk * 512, "(the log said: at 499712)")
'''),
        dict(label='3 · Checksums catch one changed byte', hint='Compute a CRC per 512-byte chunk, change one byte, and find the chunk that no longer matches.',
             code='''import zlib
data = bytearray(b"71484,poha,25\\n" * 200)          # about 2.8 KB
sums = [zlib.crc32(data[i:i + 512]) for i in range(0, len(data), 512)]
data[1500] = ord("X")
for n, i in enumerate(range(0, len(data), 512)):
    if zlib.crc32(data[i:i + 512]) != sums[n]:
        print("checksum error in chunk", n, "at offset", i)
'''),
        dict(label='4 · Fail over to the next replica', hint='The first replica is corrupt and the second DataNode is dead. Which replica does the client finally read?',
             code='''replicas = ["dn-2", "dn-1", "dn-3"]
corrupt, dead = {"dn-2"}, {"dn-1"}
for dn in replicas:
    if dn in dead:
        print(dn, "not responding -> next")
    elif dn in corrupt:
        print(dn, "checksum error -> report bad block, next")
    else:
        print("read from", dn); break
'''),
        dict(label='5 · Spot the error', hint='This sorting puts the farthest replica first. Fix the sort.',
             code='''dist = {"dn-1": 2, "dn-2": 0, "dn-3": 4}
order = sorted(dist, key=lambda d: -dist[d])
print("read from", order[0])
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: who serves your reads?',
    intro='<p>This script prints where each block of <code>canteen_1mb.csv</code> has replicas, then reads the file from two clients (the namenode container and datanode-2) with client debug logging and shows which DataNode served each block. Save it as <code>read_trace.py</code> in the <code>hdfs-lab</code> folder.</p>',
    items=[
        dict(title='Same file, two clients, different DataNodes', file='read_trace.py',
             cmd=open(os.path.join(HERE, 'read_trace.py')).read() + '\n# In the hdfs-lab folder:\n#   python3 read_trace.py',
             output='''block 0 replicas on: datanode-1, datanode-2, datanode-3
block 1 replicas on: datanode-1, datanode-2, datanode-3
block 2 replicas on: datanode-1, datanode-2, datanode-3
block 3 replicas on: datanode-1, datanode-2, datanode-3
block 4 replicas on: datanode-1, datanode-2, datanode-3
client namenode-1  read from: datanode-2, datanode-3, datanode-3, datanode-3, datanode-1
client datanode-2  read from: datanode-2, datanode-2, datanode-2, datanode-2, datanode-2''',
             note='Real output. The off-cluster client\'s choices are random among equally distant replicas, so your order will differ; the client on datanode-2 always reads locally.'),
    ],
)

TRACE = dict(
    heading='Reading a file block by block',
    intro='<p>Follow a client reading a 3-block file from the sorted location lists, skipping a dead DataNode for one block.</p>',
    code='''locations = {0: ["dn-2", "dn-1", "dn-3"], 1: ["dn-2", "dn-3", "dn-1"], 2: ["dn-1", "dn-2", "dn-3"]}
dead = {"dn-1"}
served = []
for block, nodes in locations.items():
    for dn in nodes:
        if dn not in dead:
            served.append((block, dn))
            break
print(served)
''',
    notes={4: 'Per block :: Each block has its own sorted list; the best DataNode can differ per block.',
           6: 'Skip :: A DataNode that failed is put on the stream\'s dead list and skipped.'},
)

WORKED_INTRO = 'Three read-path questions with numbers: how much locality saves on the network, how rare silent corruption really is at scale, and how hedged reads cut tail latency. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Network · locality', title='How much traffic does data locality save?',
         problem='<p>A daily job reads 40 TB. With good scheduling, 85% of reads are node-local, 12% rack-local and 3% off-rack. Without locality, assume 0% local, 20% rack-local and 80% off-rack. How many TB cross the core network in each case?</p>',
         inp='40 TB · 85/12/3% vs 0/20/80%',
         approach=['Only off-rack reads cross the core switch.',
                   'Core traffic = total × off-rack share.',
                   'Compare.'],
         code='''tb = 40
for name, off in [("with locality", 0.03), ("without", 0.80)]:
    print(f"{name:14}: {tb * off:.1f} TB through the core network")
''', notes={3: 'Core :: Node-local reads never leave the machine; rack-local ones stay in the rack.'},
         tryit='32 TB vs 1.2 TB a day: locality is why Hadoop clusters could use cheaper, oversubscribed core networks.'),
    dict(level='i', tag='Integrity · scale', title='How many corrupt chunks per day?',
         problem='<p>Suppose disks return a silently wrong byte once per 10<sup>14</sup> bits read. A cluster reads 2 PB per day. How many checksum errors per day would you expect, and why does HDFS still return correct data?</p>',
         inp='1 error per 1e14 bits · 2 PB/day',
         approach=['Bits read = 2 PB × 8.',
                   'Errors = bits / 1e14.',
                   'Each is caught by the 512-byte checksums and served from another replica.'],
         code='''bits = 2 * 2**50 * 8
print(f"about {bits / 1e14:.0f} silent errors per day, each caught by a checksum")
''', notes={1: 'Scale :: Rare events become daily events on big clusters.'},
         tryit='Without end-to-end checksums, those errors would end up inside reports and models without anyone noticing.'),
    dict(level='a', tag='Latency · hedged reads', title='Do hedged reads help the slowest requests?',
         problem='<p>Each block read normally takes 20 ms, but out of 50 reads, 2 hit a slow disk and take 800 ms. With hedged reads, if a read hasn\'t finished in 50 ms, a second read starts on another replica (which takes the normal 20 ms) and the faster one wins. Compare the slowest read and the average with and without hedging.</p>',
         inp='50 reads · 2 at 800 ms · hedge after 50 ms',
         approach=['Without hedging, slow reads take 800 ms.',
                   'With hedging, a slow read takes 50 ms + 20 ms for the second replica.',
                   'Compare the worst case and the average.'],
         code='''reads = [20] * 48 + [800, 800]
hedge_after, other_replica = 50, 20
hedged = [r if r <= hedge_after else min(r, hedge_after + other_replica) for r in reads]
print("slowest read: without", max(reads), "ms, with hedging", max(hedged), "ms")
print("average: without", sum(reads) / len(reads), "ms, with hedging", sum(hedged) / len(hedged), "ms")
print("extra reads started:", sum(r > hedge_after for r in reads))
''', notes={3: 'Hedge :: Only reads still running after 50 ms get a second attempt.'},
         tryit='Hedged reads cost extra reads (here 2 of 50). HDFS supports them with dfs.client.hedged.read.threadpool.size and dfs.client.hedged.read.threshold.millis.'),
]

QUIZ = mix([
    dict(q='What does the NameNode send to a reading client?', options=['The file data', 'Block IDs and replica locations, sorted by distance', 'Only the file size', 'A list of other clients'], answer=1,
         why='The LocatedBlocks reply: length, blocks, offsets and locations.'),
    dict(q='A client runs on a DataNode that holds a replica. Where does it read from?', options=['A random DataNode', 'Its own DataNode (distance 0)', 'The NameNode', 'The DataNode in another rack'], answer=1,
         why='Real log: all 5 blocks from 172.19.0.3, the client\'s own DataNode.'),
    dict(q='Why did the client in the namenode container read from different DataNodes?', options=['It was misconfigured', 'All replicas were equally far, so the order was shuffled', 'The NameNode was overloaded', 'Blocks were missing'], answer=1,
         why='Equal distances are randomised to spread load.'),
    dict(q='How often are checksums stored for HDFS data?', options=['Once per file', 'Once per block', 'Every 512 bytes', 'Every 64 KB'], answer=2,
         why='dfs.bytes-per-checksum = 512; the error was reported at 499,712 = 976 × 512.'),
    dict(q='What does the client do on a checksum error?', options=['Returns the corrupt data', 'Reads the data from another replica and reports the bad replica to the NameNode', 'Deletes the file', 'Restarts the DataNode'], answer=1,
         why='The output MD5 matched the original, and reportBadBlocks appeared in the NameNode log.'),
    dict(q='After reportBadBlocks, the NameNode:', options=['Ignores it', 'Copies the block from a good replica and deletes the corrupt one', 'Marks the whole file read-only', 'Formats the DataNode'], answer=1,
         why='A new replica appeared on datanode-4 six seconds later; the bad files were removed.'),
    dict(q='Which configuration enables reading local block files directly, bypassing the DataNode?', options=['dfs.replication', 'dfs.client.read.shortcircuit', 'dfs.blocksize', 'fs.defaultFS'], answer=1,
         why='Short-circuit local reads; false by default.'),
    dict(q='All replicas of a block are corrupt. What happens on read?', options=['HDFS repairs it from the NameNode', 'The read fails (BlockMissingException) and fsck reports the file as corrupt', 'The NameNode returns zeros', 'The file is silently skipped'], answer=1,
         why='The NameNode holds no data to repair from.'),
])

REVISION = [
    'Read = <code>open()</code> → <b>getBlockLocations</b> (NameNode) → read each block <b>directly from a DataNode</b> → <code>close()</code>.',
    'Locations sorted by <b>distance</b>: same node (0) &lt; same rack (2) &lt; other rack (4); ties shuffled.',
    'Lab: client on dn-2 read all 5 blocks locally; off-cluster client spread across dn-1/2/3.',
    'Checksums every <b>512 bytes</b>, verified by the reading client (end-to-end).',
    'Checksum error → next replica + <b>reportBadBlocks</b> → NameNode re-replicates and deletes the bad copy.',
    'Dead DataNode → next replica; the stream remembers it as dead.',
    'Extras: short-circuit local reads, hedged reads, block scanner (every 504 h).',
    'NameNode never sends data.',
]
FAQ = [
    ('How does a client read a file from HDFS?', 'It opens the file, which asks the NameNode for the locations of the file\'s blocks. For each block, the NameNode lists the DataNodes holding replicas sorted by distance from the client. The client reads each block directly from the closest DataNode, verifying checksums, then moves to the next block.'),
    ('How does HDFS choose which replica to read?', 'The NameNode sorts replicas by network distance from the client: same node first, then same rack, then other racks, using the rack topology. Replicas at the same distance are shuffled so load is spread. The client tries them in that order.'),
    ('How does HDFS detect corrupted data?', 'Writers compute a CRC checksum for every 512 bytes, stored in the .meta file next to each block replica. Readers recompute and compare. DataNodes also verify blocks in the background with the block scanner.'),
    ('What happens when a client finds a corrupt block?', 'It reads that part from another replica, so the application still gets correct data, and reports the corrupt replica to the NameNode. The NameNode marks it corrupt, creates a new replica from a good copy and deletes the bad one.'),
    ('What are short-circuit local reads?', 'When the client and the replica are on the same machine and dfs.client.read.shortcircuit is enabled (with a domain socket path), the client reads the block file directly from local disk using a file descriptor passed by the DataNode, avoiding the TCP data path.'),
    ('Does reading put load on the NameNode?', 'Only for metadata: open and block location lookups. The data transfer itself is between client and DataNodes, which is why HDFS reads scale with the number of DataNodes.'),
]

PRACTICE_INTRO = 'Read-path exercises using real offsets, IPs and logs from the lab.'
PROBLEMS = [
    dict(level='easy', title='Distance table', stmt='Compute the distance from a client on dn-3 (rack2) to dn-1 (rack1), dn-4 (rack2) and dn-3.', inp='client dn-3',
         code='''rack = {"dn-1": 1, "dn-3": 2, "dn-4": 2}
for dn in ["dn-1", "dn-4", "dn-3"]:
    d = 0 if dn == "dn-3" else 2 if rack[dn] == 2 else 4
    print(dn, d)
''', explain='dn-1: 4 (other rack), dn-4: 2 (same rack), dn-3: 0 (itself).'),
    dict(level='easy', title='Block for an offset', stmt='With 1 MB blocks, which block holds byte 1,500,000 of the file, and at what offset inside it?', inp='1,500,000 · 1,048,576',
         code='print(1500000 // 1048576, 1500000 % 1048576)\n', explain='Block 1 (the second), offset 451,424 inside it: blk_1073741827 in our file.'),
    dict(level='easy', title='Count servers', stmt='Count how many blocks each DataNode served in the real off-cluster read: dn-2, dn-3, dn-3, dn-3, dn-1.', inp='dn-2 · dn-3 · dn-3 · dn-3 · dn-1',
         code='''from collections import Counter
print(Counter(["dn-2", "dn-3", "dn-3", "dn-3", "dn-1"]))
''', explain='dn-3: 3, dn-2: 1, dn-1: 1. Random among equal distances; over many reads it evens out.'),
    dict(level='medium', title='Which replica healed it?', stmt='Before: replicas [.3, .4, .6]. After the bad-block report: [.4, .7, .6]. Which replica was removed and which added?', inp='before / after lists',
         code='''before, after = {"172.19.0.3", "172.19.0.4", "172.19.0.6"}, {"172.19.0.4", "172.19.0.7", "172.19.0.6"}
print("removed:", before - after, " added:", after - before)
''', explain='Removed 172.19.0.3 (datanode-2, the corrupted copy); added 172.19.0.7 (datanode-4).'),
    dict(level='medium', title='Checksum bytes per block', stmt='How many checksum bytes does a 128 MB block need, and what fraction of the data is that?', inp='134,217,728 bytes · 4 B per 512 B',
         code='''b = 134217728
c = b // 512 * 4
print(c, "bytes", f"({c / b:.2%})")
''', explain='1,048,576 bytes (1 MB) of checksums per 128 MB block: 0.78% overhead for end-to-end integrity.'),
    dict(level='medium', title='Parse a LocatedBlock', stmt='From the real LocatedBlock text, extract block ID, size, offset and location IPs.', inp='LocatedBlock{…blk_1073741826_1002; getBlockSize()=1048576; … offset=0; locs=[…]}',
         code='''import re
s = ("LocatedBlock{BP-1507681208-172.19.0.3-1792565333483:blk_1073741826_1002; getBlockSize()=1048576; "
     "corrupt=false; offset=0; locs=[DatanodeInfoWithStorage[172.19.0.3:9866,DS-1,DISK], "
     "DatanodeInfoWithStorage[172.19.0.4:9866,DS-2,DISK], DatanodeInfoWithStorage[172.19.0.6:9866,DS-3,DISK]]")
print(re.search(r"(blk_\\d+)", s).group(1), re.search(r"getBlockSize\\(\\)=(\\d+)", s).group(1),
      re.search(r"offset=(\\d+)", s).group(1), re.findall(r"(\\d+\\.\\d+\\.\\d+\\.\\d+):9866", s))
''', explain='blk_1073741826, 1048576 bytes at offset 0, replicas on .3, .4 and .6.'),
    dict(level='business', title='Saving by locality', stmt='Core network capacity costs Rs 8 lakh per 10 Gbit/s per year. Without locality, a cluster would need 40 Gbit/s of core capacity; with locality, 4 Gbit/s. What is the yearly saving?', inp='Rs 8 lakh per 10 Gbit/s · 40 vs 4 Gbit/s',
         code='''import math
cost = lambda g: math.ceil(g / 10) * 8
print(f"Rs {cost(40) - cost(4)} lakh per year")
''', explain='Rs 32 lakh − Rs 8 lakh = Rs 24 lakh per year (illustrative prices), just from reading where the data is.'),
    dict(level='advanced', title='Read with corruption and failover', stmt='Simulate reading 3 blocks with sorted replicas, where some replicas are corrupt and some DataNodes dead. Return the serving DataNode per block and the list of bad-block reports.', inp='3 blocks · corrupt {(1, dn-2)} · dead {dn-3}',
         code='''locs = {0: ["dn-2", "dn-1", "dn-3"], 1: ["dn-2", "dn-3", "dn-1"], 2: ["dn-3", "dn-2", "dn-1"]}
corrupt, dead = {(1, "dn-2")}, {"dn-3"}
served, reports = {}, []
for b, nodes in locs.items():
    for dn in nodes:
        if dn in dead:
            continue
        if (b, dn) in corrupt:
            reports.append((b, dn)); continue
        served[b] = dn; break
print("served:", served, " reported bad:", reports)
''', explain='Block 0 from dn-2, block 1 from dn-1 (after the corrupt dn-2 copy and dead dn-3), block 2 from dn-2. One bad-block report: block 1 on dn-2.'),
]

SCN_INTRO = 'Read-path questions test whether you understand locality and integrity, two of HDFS\'s core promises.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · internals</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Explain how HDFS reads a file”</h4>
      <p class="scn__situation">The anatomy-of-a-read question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> NameNode vs DataNode roles and replica choice.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Client opens the file; the NameNode returns block locations, each list sorted by distance from the client.</li>
          <li>The client reads each block directly from the nearest DataNode, verifying 512-byte checksums, then moves to the next block.</li>
          <li>On failure or checksum error it uses the next replica and reports bad replicas. The NameNode never transfers data.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · integrity</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Logs show many “Found Checksum error” warnings from one DataNode</h4>
      <p class="scn__situation">Jobs still succeed, but the warnings keep appearing for different blocks on the same host.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you treat it as a hardware signal.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Clients are reading around corrupt replicas and HDFS re-replicates them, so data is safe for now.</li>
          <li>Repeated errors on one host point to a failing disk, controller or memory. Check which volume the blocks are on, SMART data, kernel logs.</li>
          <li>Mark the volume failed or decommission the node, replace the hardware, and run <code>fsck</code> to confirm no file has lost all good replicas.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Performance · locality</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Reads from BI tools on the edge node are slow; jobs are fast</h4>
      <p class="scn__situation">Analysts pull large files to an edge node and complain about speed.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> remote reads vs local reads.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The edge node isn't a DataNode, so every read is remote and limited by its network link; jobs read locally on DataNodes.</li>
          <li>Move the heavy work into the cluster (Hive/Spark queries returning small results) instead of copying raw data out.</li>
          <li>If raw transfers are needed: faster edge-node networking, parallel readers, or columnar formats so less data is read.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · reliability</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“If a disk silently flips a bit, will my report be wrong?”</h4>
      <p class="scn__situation">A manager worries about silent data corruption.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> end-to-end checksums.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No (unless every replica is bad). Each 512 bytes has a checksum created when the data was written; readers verify it.</li>
          <li>A mismatch makes the client read another replica and report the bad one, which HDFS replaces.</li>
          <li>Real demo: one byte changed on disk → “Found Checksum error … at 499712” → output identical to the original.</li>
        </ul>
      </div></details>
    </article>
'''
