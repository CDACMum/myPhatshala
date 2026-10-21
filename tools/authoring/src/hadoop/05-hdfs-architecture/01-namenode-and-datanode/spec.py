import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Metadata here, data there',
    intro='<p>The dark <b>NameNode</b> box holds only metadata. Each DataNode box shows the block replicas stored on it. Use the tabs below the cluster to see the NameNode\'s map.</p>',
    racks=2, nodes=2, features=['upload', 'fail', 'fsck'],
    preload=[dict(name='canteen_orders.csv', sizeMB=500)],
    **{'try': [
        dict(text='Upload a 1 GB file. Watch the NameNode choose DataNodes for each block in the Event log.', on='upload-done'),
        dict(text='Click a DataNode to stop it. The data is still listed in the NameNode metadata: the map survives, one location is gone.', on='node-stop'),
        dict(text='Run <b>hdfs fsck /</b> and read which blocks are under-replicated.', on='fsck'),
    ]},
)))

META = dict(
    module='05-hdfs-architecture', lesson='01-namenode-and-datanode', n='5.1',
    module_label='Module 5 · HDFS architecture',
    title='NameNode and DataNode',
    desc='The master–worker design of HDFS: what the NameNode keeps (namespace, fsimage, edit log, in-memory block map) and what DataNodes keep (block files with .meta checksums), shown on a real Hadoop 3.5.0 cluster with 4 DataNodes in 2 racks: dfsadmin -report, fsck block locations, the NameNode and DataNode folders, reading a block file directly. NameNode memory sizing, playground, Python, quiz and interview scenarios.',
    og_desc='The NameNode keeps the map, DataNodes keep the bytes. Open both on a real cluster and find your file\'s blocks on disk.',
    minutes=28, level='Beginner → Intermediate',
    lead='HDFS splits work between one master and many workers. The NameNode knows every file, folder and block and where each block lives; DataNodes store the blocks as ordinary files and serve them. In this lesson you open both on a real four-DataNode cluster, follow one file from its path to the actual block files on disk, and learn what each daemon must have to stay healthy.',
    chips=['Real 4-DataNode cluster', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='A tiny NameNode in Python',
    intro='<p>This program keeps the two NameNode structures from Part 2: the <b>namespace</b> (path → blocks) and the <b>block map</b> (block → DataNodes). Then it answers the question <code>fsck</code> answers: where are this file\'s blocks?</p>',
    code='''namespace = {
    "/user/hadoop/data/canteen_orders.csv": {"owner": "hadoop", "repl": 3,
                                             "blocks": ["blk_1073741825"]},
    "/user/hadoop/data/canteen_1mb.csv": {"owner": "hadoop", "repl": 3,
                                          "blocks": ["blk_1073741826", "blk_1073741827"]},
}
block_map = {
    "blk_1073741825": ["datanode-1", "datanode-2", "datanode-4"],
    "blk_1073741826": ["datanode-1", "datanode-3", "datanode-4"],
    "blk_1073741827": ["datanode-1", "datanode-2", "datanode-4"],
}

def locate(path):
    meta = namespace[path]
    print(path, "owner", meta["owner"], "replication", meta["repl"])
    for blk in meta["blocks"]:
        print("  ", blk, "->", ", ".join(block_map.get(blk, [])) or "MISSING")

locate("/user/hadoop/data/canteen_1mb.csv")
''',
    anno=[
        ('namespace = {', 'Saved in the fsimage and edit log: survives a restart.'),
        ('block_map = {', 'Kept only in memory and rebuilt from DataNode block reports after a restart.'),
        ('print("  ", blk, "->", ", ".join(block_map.get(blk, [])) or "MISSING")', 'If no DataNode has reported a block, its location list is empty: a missing block.'),
    ],
    tasks=[
        dict(label='1 · Locate a file', hint='Press <b>Run</b>. Then call <code>locate</code> for <code>canteen_orders.csv</code>.', code=None),
        dict(label='2 · A DataNode dies', hint='<b>Predict first:</b> remove <code>datanode-1</code> from every list. Which blocks still have 2 copies, and would any be missing?',
             code='''block_map = {"blk_1": ["datanode-1", "datanode-2", "datanode-4"],
             "blk_2": ["datanode-1", "datanode-3", "datanode-4"],
             "blk_3": ["datanode-1"]}
dead = "datanode-1"
for blk, nodes in block_map.items():
    left = [n for n in nodes if n != dead]
    print(blk, "->", left, "MISSING" if not left else f"{len(left)} copies left")
'''),
        dict(label='3 · NameNode memory', hint='Rule of thumb: about 150 bytes of heap per file, directory and block. Estimate the heap for 1 crore files of 1 block each in 1 lakh directories.',
             code='''files, dirs, blocks_per_file = 1_00_00_000, 1_00_000, 1
objects = files + dirs + files * blocks_per_file
print(f"{objects:,} objects -> about {objects * 150 / 2**30:.1f} GB of heap")
'''),
        dict(label='4 · Blocks per DataNode', hint='The real <code>dfsadmin -report</code> showed 3, 6, 5 and 4 blocks on the four DataNodes. Check that the total matches 6 blocks × 3 replicas.',
             code='''per_node = {"datanode-2": 3, "datanode-1": 6, "datanode-3": 5, "datanode-4": 4}
print("replicas on disks:", sum(per_node.values()))
print("expected:", 6 * 3)
'''),
        dict(label='5 · Spot the error', hint='This lookup crashes for a block that no DataNode has reported yet. Make it print “MISSING” instead.',
             code='''block_map = {"blk_1": ["datanode-1"]}
for blk in ["blk_1", "blk_2"]:
    print(blk, "->", block_map[blk])
''', expect='error'),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: find the real block files of an HDFS file',
    intro='<p>This script asks the NameNode (via <code>fsck</code>) where each block of a file is, finds the matching Docker container for each DataNode IP, and checks the block file on that container\'s disk. Save it as <code>where_is_my_file.sh</code> in the <code>hdfs-lab</code> folder.</p>',
    items=[
        dict(title='From an HDFS path to block files on DataNode disks', file='where_is_my_file.sh',
             cmd=open(os.path.join(HERE, 'where_is_my_file.sh')).read() + '\n# In the hdfs-lab folder:\n#   bash where_is_my_file.sh /user/hadoop/data/canteen_orders.csv',
             output='''blk_1073741825_1001 len=4692009
   on lab5-datanode-1  (172.19.0.4)  file size 4692009 bytes
   on lab5-datanode-2  (172.19.0.5)  file size 4692009 bytes
   on lab5-datanode-4  (172.19.0.7)  file size 4692009 bytes''',
             note='Real output from the lab cluster. Three DataNodes, three identical 4,692,009-byte files: the replicas. The IPs on your machine will differ. On a real cluster you would use <code>ssh</code> to each host instead of <code>docker exec</code>.'),
    ],
)

TRACE = dict(
    heading='A read request, as the NameNode sees it',
    intro='<p>Follow a client asking for one file. Watch how the NameNode combines the namespace and the block map, and notice it never touches the data.</p>',
    code='''namespace = {"/data/orders.csv": ["blk_1", "blk_2"]}
block_map = {"blk_1": ["dn1", "dn3"], "blk_2": ["dn2", "dn4"]}
path = "/data/orders.csv"
blocks = namespace[path]
answer = []
for b in blocks:
    answer.append((b, block_map[b][0]))
print(answer)
''',
    notes={4: 'Namespace :: Path → ordered list of blocks.',
           7: 'Block map :: For each block, pick a DataNode (real HDFS sorts them by distance to the client).',
           8: 'Reply :: Only locations go back; the client then reads from the DataNodes itself.'},
)

WORKED_INTRO = 'Three calculations platform teams really make for HDFS masters and workers: NameNode heap, how many DataNodes a data set needs, and how evenly blocks are spread. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Capacity · NameNode', title='How much heap for the NameNode?',
         problem='<p>An insurance company stores 40 lakh files averaging 300 MB each (128 MB blocks) in 50,000 directories. Using the rule of thumb of 150 bytes per object, estimate NameNode heap. Then double it for safety and growth.</p>',
         inp='40,00,000 files · 300 MB each · 128 MB blocks · 50,000 dirs · 150 B per object',
         approach=['Blocks per file = ceil(300 / 128) = 3.',
                   'Objects = files + directories + blocks.',
                   'Heap = objects × 150 bytes, then × 2 for headroom.'],
         code='''import math
files, dirs = 40_00_000, 50_000
blocks = files * math.ceil(300 / 128)
objects = files + dirs + blocks
heap_gb = objects * 150 / 2**30
print(f"objects {objects:,}  heap ~{heap_gb:.1f} GB  with headroom ~{heap_gb * 2:.1f} GB")
''', notes={4: 'Objects :: Files, folders and blocks each cost NameNode memory.'},
         tryit='Store the same 1.2 PB as 10 KB files instead. How many objects now? This is why small files are a NameNode problem, not a disk problem.'),
    dict(level='i', tag='Capacity · DataNodes', title='How many DataNodes for 500 TB?',
         problem='<p>A team expects 500 TB of data with replication 3. Each worker has 12 disks of 16 TB. Keep 25% free for growth and temporary data. How many DataNodes are needed?</p>',
         inp='500 TB · replication 3 · 12 × 16 TB per node · 25% free',
         approach=['Raw space = data × replication.',
                   'Usable per node = disks × size × 0.75.',
                   'Nodes = ceil(raw / usable per node).'],
         code='''import math
raw_tb = 500 * 3
per_node_tb = 12 * 16 * 0.75
nodes = math.ceil(raw_tb / per_node_tb)
print(f"raw {raw_tb} TB, {per_node_tb:.0f} TB usable per node -> {nodes} DataNodes")
''', notes={4: 'Round up :: You can\'t buy 10.4 servers.'},
         tryit='Add one more node for failure headroom (losing a node must not fill the others). Real plans also add compute needs, not just storage.'),
    dict(level='a', tag='Operations · balance', title='Is data spread evenly over DataNodes?',
         problem='<p>From <code>dfsadmin -report</code> you have DFS Used per DataNode. Flag any node more than 10 percentage points above or below the cluster average utilisation (the same idea the HDFS balancer uses).</p>',
         inp='capacity 100 TB each · used: dn1 62, dn2 58, dn3 81, dn4 35, dn5 60 TB',
         approach=['Utilisation = used / capacity per node.',
                   'Average = total used / total capacity.',
                   'Flag nodes outside average ± 10 points.'],
         code='''used = {"dn1": 62, "dn2": 58, "dn3": 81, "dn4": 35, "dn5": 60}
cap = 100
avg = sum(used.values()) / (cap * len(used)) * 100
print(f"cluster average {avg:.1f}%")
for n, u in used.items():
    pct = u / cap * 100
    flag = "OVER" if pct > avg + 10 else "UNDER" if pct < avg - 10 else "ok"
    print(f"{n}: {pct:.0f}% {flag}")
''', notes={3: 'Average :: Weighted by capacity, as the balancer computes it.'},
         tryit='dn4 is probably a newly added node. Running <code>hdfs balancer -threshold 10</code> moves blocks until every node is within 10 points (Lesson 6.4).'),
]

QUIZ = mix([
    dict(q='What does the NameNode store?', options=['The contents of every file', 'The namespace and metadata: files, directories, permissions, blocks and their locations', 'Only log files', 'Only the list of users'], answer=1,
         why='The NameNode holds metadata only. File bytes live on DataNodes.'),
    dict(q='How is a block replica stored on a DataNode?', options=['In a database table', 'As an ordinary local file (blk_N) plus a .meta checksum file', 'Inside the NameNode\'s fsimage', 'Compressed in a ZIP archive'], answer=1,
         why='We saw blk_1073741825 and blk_1073741825_1001.meta on the DataNode\'s disk.'),
    dict(q='Which piece of NameNode information is NOT saved in the fsimage?', options=['The directory tree', 'File permissions', 'Which DataNodes hold each block', 'Each file\'s list of blocks'], answer=2,
         why='Block locations are rebuilt from DataNode block reports after every restart.'),
    dict(q='When a client reads a file, the data flows:', options=['Through the NameNode', 'Directly from DataNodes to the client', 'Through the SecondaryNameNode', 'Through the ResourceManager'], answer=1,
         why='The NameNode gives locations; bytes come straight from DataNodes.'),
    dict(q='Which command lists every DataNode with its rack, capacity and last contact?', options=['hdfs dfs -ls', 'hdfs dfsadmin -report', 'yarn node -list', 'jps'], answer=1,
         why='dfsadmin -report is the NameNode\'s view of all DataNodes.'),
    dict(q='NameNode memory mainly grows with:', options=['Total bytes stored', 'Number of files, directories and blocks', 'Number of users', 'Network speed'], answer=1,
         why='Each object costs roughly 150 bytes of heap, whatever its size.'),
    dict(q='What happens to HDFS if a single DataNode fails?', options=['All data is lost', 'Reads continue from other replicas and the NameNode re-replicates', 'The NameNode shuts down', 'The cluster must be formatted'], answer=1,
         why='With replication 3, losing one worker is routine.'),
    dict(q='The 36,667-byte .meta file next to a 4,692,009-byte block holds:', options=['A copy of the block', 'Checksums, 4 bytes per 512 bytes of data', 'The file name', 'Encryption keys'], answer=1,
         why='4,692,009 / 512 rounds up to 9,165 checksums × 4 bytes = 36,660, plus a 7-byte header.'),
])

REVISION = [
    'HDFS = <b>one NameNode</b> (master, metadata) + <b>many DataNodes</b> (workers, data).',
    'NameNode: namespace (tree, owners, permissions, replication, file → blocks) + <b>block map</b> (block → DataNodes).',
    'Saved on disk: <b>fsimage + edit log</b>. Not saved: block map (rebuilt from block reports).',
    'DataNode: each replica = <code>blk_N</code> + <code>blk_N_genstamp.meta</code> (checksums, 4 B per 512 B).',
    'Data flows client ↔ DataNode, <b>never through the NameNode</b>.',
    'NameNode heap ≈ 150 B per file/dir/block (rule of thumb): object count matters, not bytes.',
    'Commands: <code>hdfs dfsadmin -report</code>, <code>hdfs fsck PATH -files -blocks -locations</code>.',
    'Ports: NN 8020 / 9870 · DN 9866 / 9867 / 9864.',
]
FAQ = [
    ('What is the difference between NameNode and DataNode?', 'The NameNode is the master that stores metadata: the directory tree, permissions, which blocks make up each file and where they are. DataNodes are workers that store the actual blocks on local disks, serve reads and writes, and report to the NameNode with heartbeats and block reports.'),
    ('Does the NameNode store data?', 'No. It stores only metadata. File contents are stored as blocks on DataNodes, and clients read and write those blocks directly from and to DataNodes.'),
    ('Where does a DataNode store blocks?', 'In the folders listed in dfs.datanode.data.dir, under current/&lt;block pool ID&gt;/current/finalized/, as files named blk_&lt;id&gt; with a matching blk_&lt;id&gt;_&lt;generation stamp&gt;.meta checksum file.'),
    ('What happens if the NameNode fails?', 'Without high availability, the whole file system becomes unavailable until the NameNode is restarted (the data stays on DataNodes but cannot be located). With HA, a standby NameNode takes over automatically.'),
    ('How does the NameNode know where blocks are?', 'From block reports: each DataNode reports all its blocks when it starts and periodically afterwards (every 6 hours by default), plus incremental reports when blocks are added or removed.'),
    ('How much memory does a NameNode need?', 'It depends on the number of files, directories and blocks. A common rule of thumb is about 150 bytes per object, so 10 crore objects need roughly 14 GB of heap, plus headroom.'),
    ('Can there be more than one NameNode?', 'Yes: in HA there is one active and one or more standby NameNodes for the same namespace, and with federation several independent NameNodes each manage part of the namespace on the same DataNodes.'),
]

PRACTICE_INTRO = 'Exercises on metadata, block files and DataNode reports, using numbers from the real cluster.'
PROBLEMS = [
    dict(level='easy', title='Checksum file size', stmt='A block has 1,048,576 bytes. With 4 bytes of checksum per 512 bytes and a 7-byte header, how big is its .meta file?', inp='1,048,576 bytes · 512 B per checksum · 4 B · 7 B header',
         code='''import math
print(math.ceil(1048576 / 512) * 4 + 7, "bytes")
''', explain='8,199 bytes, exactly the size of blk_1073741826_1002.meta on the DataNode.'),
    dict(level='easy', title='Replicas on disk', stmt='6 blocks with replication 3 are spread over 4 DataNodes. How many block files exist in total, and how many on average per node?', inp='6 blocks · replication 3 · 4 DataNodes',
         code='''total = 6 * 3
print(total, "replicas,", total / 4, "per node on average")
''', explain='18 replicas, 4.5 per node on average (the real report showed 3, 6, 5 and 4).'),
    dict(level='easy', title='Parse a report line', stmt='From "Num of Blocks: 6" and "DFS Used: 9481956 (9.04 MB)", print the number of blocks and MB used.', inp='Num of Blocks: 6 · DFS Used: 9481956 (9.04 MB)',
         code='''a = "Num of Blocks: 6"
b = "DFS Used: 9481956 (9.04 MB)"
blocks = int(a.split(":")[1])
used = int(b.split(":")[1].split()[0])
print(blocks, "blocks,", round(used / 2**20, 2), "MB")
''', explain='6 blocks and 9.04 MB, as in the report for datanode-1.'),
    dict(level='medium', title='Heap for small files', stmt='The same 10 TB is stored as 1 GB files or as 100 KB files (one block per file). Estimate NameNode heap for each at 150 bytes per object (file + block).', inp='10 TB · 1 GB vs 100 KB files',
         code='''tb = 10 * 2**40
for size, label in [(2**30, "1 GB"), (100 * 2**10, "100 KB")]:
    files = tb // size
    print(f"{label:>6} files: {files:,} files -> {files * 2 * 150 / 2**20:,.1f} MB heap")
''', explain='About 3 MB of heap for 1 GB files versus about 31 GB for 100 KB files: same data, ten thousand times more metadata.'),
    dict(level='medium', title='Missing blocks after failures', stmt='Given each block\'s DataNodes and a set of dead nodes, list blocks with no live replica.', inp='dead: dn2, dn5',
         code='''blocks = {"b1": ["dn1", "dn2", "dn3"], "b2": ["dn2", "dn5"], "b3": ["dn4", "dn5", "dn6"]}
dead = {"dn2", "dn5"}
print([b for b, nodes in blocks.items() if not set(nodes) - dead])
''', explain='Only b2 is missing: both of its replicas were on dead nodes (it had replication 2).'),
    dict(level='medium', title='Which nodes hold a file?', stmt='Using the real fsck output of canteen_1mb.csv, count how many replicas each DataNode IP holds.', inp='5 blocks × 3 locations (from Part 4)',
         code='''from collections import Counter
locs = [["5", "6", "7"], ["5", "4", "7"], ["6", "7", "5"], ["6", "7", "5"], ["5", "4", "6"]]
print(Counter("172.19.0." + ip for block in locs for ip in block))
''', explain='172.19.0.5 holds all 5 blocks, .7 and .6 hold 4 each, .4 holds 2: 15 replicas in total.'),
    dict(level='business', title='NameNode server budget', stmt='Heap needed is 96 GB. Servers come with 128, 256 or 512 GB RAM; keep at least 32 GB for the OS and other processes. Which is the smallest that fits?', inp='96 GB heap · 32 GB other · 128/256/512',
         code='''need = 96 + 32
print(next(r for r in [128, 256, 512] if r >= need), "GB server")
''', explain='128 GB is exactly enough today, but with no room to grow. Most teams would choose 256 GB for a NameNode.'),
    dict(level='advanced', title='Rebuild the block map', stmt='After a restart the NameNode only has the namespace. Build the block map from three block reports and print each block\'s replica count.', inp='dn1: b1,b2 · dn2: b1,b3 · dn3: b2,b3,b1',
         code='''reports = {"dn1": ["b1", "b2"], "dn2": ["b1", "b3"], "dn3": ["b2", "b3", "b1"]}
block_map = {}
for dn, blocks in reports.items():
    for b in blocks:
        block_map.setdefault(b, []).append(dn)
for b in sorted(block_map):
    print(b, block_map[b], len(block_map[b]), "replicas")
''', explain='b1 has 3 replicas, b2 and b3 have 2 each. This is exactly how the block map is rebuilt at start-up (Lessons 5.5 and 5.6).'),
]

SCN_INTRO = 'Interviewers use NameNode and DataNode questions to see whether you understand where metadata ends and data begins.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Does a 1 TB file pass through the NameNode when I upload it?”</h4>
      <p class="scn__situation">A classic first-round question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the split between the metadata path and the data path.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No. The client asks the NameNode to create the file and allocate blocks; the NameNode returns DataNode addresses.</li>
          <li>The client streams bytes to the first DataNode, which forwards them along a pipeline to the others.</li>
          <li>The NameNode only records metadata (and later learns of finished replicas). That is why one NameNode can serve thousands of DataNodes.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · memory</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>NameNode heap keeps climbing, but the cluster is only 30% full</h4>
      <p class="scn__situation">Disk usage is low, yet the NameNode needs more and more heap and garbage collection pauses are getting longer.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know heap depends on object count?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Check files and blocks (NameNode UI, <code>FilesTotal</code>/<code>BlocksTotal</code> in <code>/jmx</code>) and find directories with millions of small files (<code>hdfs dfs -count</code>).</li>
          <li>Compact small files (merge into larger Parquet/ORC files, use HAR or larger batches in ingestion).</li>
          <li>Short term: increase heap and tune GC; long term: fix the sources of small files, add quotas, or federate the namespace.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Troubleshooting · disk</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>“Someone deleted blk_ files on a DataNode to free space”</h4>
      <p class="scn__situation">A junior admin removed some old-looking <code>blk_</code> files from a full DataNode disk.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> what HDFS does when replicas vanish behind its back.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Those were live replicas. The DataNode will report them missing (block scanner or next block report), and the NameNode will re-replicate from other copies if any exist.</li>
          <li>Run <code>hdfs fsck / -list-corruptfileblocks</code> and check for missing blocks; files whose every replica was deleted are lost.</li>
          <li>Prevent it: free space with HDFS commands (delete data, lower replication of cold data, add disks, run the balancer), never inside the DataNode folders.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · hardware</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Choose hardware for master and worker nodes</h4>
      <p class="scn__situation">You have budget for 1 master and 10 workers. What do you prioritise for each?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you match hardware to each role.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>NameNode: plenty of RAM for the heap, reliable disks (RAID) for metadata, redundant power and network; disk capacity is not important.</li>
          <li>DataNodes: many large disks (JBOD, no RAID), enough RAM and cores for YARN tasks, good network.</li>
          <li>Plan for a standby NameNode (HA) as soon as the cluster matters.</li>
        </ul>
      </div></details>
    </article>
'''
