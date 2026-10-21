import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='02-data-and-storage', lesson='03-storage-for-big-data', n='2.3',
    module_label='Module 2 · Data and Storage',
    title='Storage for big data: block, file and object storage (and HDFS)',
    desc='Block vs file vs object storage explained for big data: buckets, keys and prefixes, HDFS blocks and replication, NameNode and DataNodes, durability, erasure coding, storage tiers and lifecycle rules, the small-files problem and why renames are unsafe on S3. Real-time animations, Python you can run, and a mini object store on your PC.',
    og_desc='Where do 2 petabytes live? Learn block, file and object storage and HDFS, watch a file heal itself after a node failure, and build a mini object store.',
    minutes=28, level='Beginner → Advanced',
    lead='Big data lakes don\'t live on a hard disk with folders. In this lesson you compare <b>block</b>, <b>file</b> and <b>object</b> storage and Hadoop\'s <b>HDFS</b>, follow a photo into S3 and watch it age into the archive, write a file into HDFS and see it survive a dead node, meet the small-files problem, and learn why “renaming a folder” can corrupt results in the cloud.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Mini object store on your PC'],
)

RUN = dict(
    heading='A tiny object store in a dictionary',
    intro='<p>Object storage is a giant key → bytes map with metadata. This program builds one with a Python dictionary: <code>put</code>, <code>get</code> and <code>list</code> by prefix. Then try the challenges: split a file into HDFS blocks, survive a node failure, compare replication with erasure coding, cost the small-files problem and plan storage tiers.</p>',
    code='''bucket = {}

def put(key, data, **meta):
    bucket[key] = {"data": data, "size": len(data), **meta}

def get(key):
    return bucket[key]["data"]

def list_prefix(prefix):
    return sorted(k for k in bucket if k.startswith(prefix))

put("orders/date=2026-10-19/part-0.csv", b"O1,Pune,420\\nO2,Thane,250\\n", type="csv")
put("orders/date=2026-10-20/part-0.csv", b"O3,Pune,180\\n", type="csv")
put("reviews/2026/10/19/O1.jpg", b"...jpeg bytes...", type="image", order="O1")

print("All orders keys:", list_prefix("orders/"))
print("One day only   :", list_prefix("orders/date=2026-10-19/"))
print("Read back      :", get("orders/date=2026-10-20/part-0.csv"))
print("Metadata       :", {k: v for k, v in bucket["reviews/2026/10/19/O1.jpg"].items() if k != "data"})
''',
    anno=[
        ('def put(key, data, **meta):', 'Storing is just “this key → these bytes, plus some metadata”. There is no folder to create first.'),
        ('return sorted(k for k in bucket if k.startswith(prefix))', 'A “folder listing” is really a filter on key prefixes. This is why key naming matters so much.'),
        ('put("reviews/2026/10/19/O1.jpg", b"...jpeg bytes...", type="image", order="O1")', 'Metadata travels with the object: type, order id, size.'),
    ],
    tasks=[
        dict(label='1 · Keys and prefixes', hint='Press <b>Run</b>. Add an order for 2026-10-21 and list the whole month with the prefix <code>orders/date=2026-10-</code>.', code=None),
        dict(label='2 · HDFS blocks', hint='Split files into 128 MB blocks and count the raw space with 3 replicas. Try a 1 MB file: does it waste a whole block of disk? (No: HDFS stores only the bytes used.)',
             code='''import math
BLOCK, REPLICAS = 128, 3
for name, size_mb in [("orders.csv", 300), ("big.log", 1000), ("tiny.json", 1)]:
    blocks = math.ceil(size_mb / BLOCK)
    print(f"{name:10} {size_mb:5} MB -> {blocks} blocks, {size_mb * REPLICAS} MB raw on disk")
'''),
        dict(label='3 · Node failure', hint='Each block lives on 3 nodes. When a node dies, find blocks with fewer than 3 copies and copy them to a node that doesn\'t have them yet. Kill <code>"DN3"</code> instead.',
             code='''placement = {"B1": ["DN1", "DN2", "DN4"], "B2": ["DN1", "DN3", "DN4"], "B3": ["DN2", "DN3", "DN4"]}
nodes = ["DN1", "DN2", "DN3", "DN4", "DN5"]
dead = "DN2"
for block, where in placement.items():
    if dead in where:
        where.remove(dead)
        target = next(n for n in nodes if n != dead and n not in where)
        where.append(target)
        print(f"{block}: re-replicated to {target}")
print(placement)
'''),
        dict(label='4 · Copies vs erasure coding', hint='Compare raw space and how many lost pieces each scheme survives. Try erasure coding 10 + 4.',
             code='''data_tb = 500
schemes = {"3 replicas": (1, 2), "erasure 6+3": (6, 3), "erasure 10+4": (10, 4)}
for name, (d, p) in schemes.items():
    raw = data_tb * (d + p) / d
    print(f"{name:13} raw {raw:6.0f} TB  overhead {(raw / data_tb - 1) * 100:4.0f}%  survives {p} lost pieces")
'''),
        dict(label='5 · Small files (advanced)', hint='Same data as many small files or a few big ones. Estimate request cost and open time. Change the file size to 128 MB.',
             code='''total_gb = 500
cost_per_1000_requests = 0.4      # rupees, illustrative
open_ms = 15
for file_mb in [0.05, 1, 128]:
    files = total_gb * 1024 / file_mb
    cost = files / 1000 * cost_per_1000_requests
    hours = files * open_ms / 1000 / 3600
    print(f"{file_mb:7} MB files: {files:12,.0f} files, Rs {cost:9,.0f} per full read, {hours:6.1f} h of opening")
'''),
        dict(label='6 · Lifecycle tiers (advanced)', hint='Move data down tiers by age and compute the monthly bill. Prices are illustrative per GB per month. Change the rules to archive after 180 days.',
             code='''price = {"hot": 1.8, "cool": 1.0, "archive": 0.1}       # Rs per GB-month (illustrative)
daily_gb, days_kept = 200, 3 * 365
def tier(age):
    if age < 90:
        return "hot"
    elif age < 365:
        return "cool"
    return "archive"
bill, gb = {}, {}
for age in range(days_kept):
    t = tier(age)
    gb[t] = gb.get(t, 0) + daily_gb
for t in gb:
    bill[t] = gb[t] * price[t]
print({t: f"{g / 1024:.0f} TB" for t, g in gb.items()})
print("Monthly bill with tiers : Rs", round(sum(bill.values())))
print("If everything stayed hot: Rs", round(daily_gb * days_kept * price["hot"]))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a mini object store and the small-files test',
    intro='<p>This program builds a tiny object store in a folder: objects are saved under hashed names with a metadata file, and “folders” exist only as key prefixes. Then it writes the same data as 5,000 small files and as one big file and times reading both. Only the standard library is used. Save it as <code>storage_lab.py</code> in an empty folder and run it.</p>',
    items=[
        dict(title='Object store + small-files test', file='storage_lab.py',
             cmd=open(os.path.join(HERE, 'storage_lab.py')).read() + '\n# In a terminal:  python storage_lab.py',
             output=open(os.path.join(HERE, 'storage_lab.out')).read(),
             note='Recorded from a real run with Python 3.13 on an SSD. Your times will differ (Windows antivirus scanning can make small files even slower), but the big file always wins. Open the <code>my_bucket/objects</code> folder: there are no <code>reviews</code> or <code>orders</code> folders, only hashed object files and their metadata. Real object stores add HTTP requests on top, so the small-files penalty is larger still.'),
    ],
)

TRACE = dict(
    heading='Re-replicating blocks after a failure, one line at a time',
    intro='<p>Two blocks have three copies each. Node DN2 dies. Watch the program find each block that lost a copy and pick a new node for it.</p>',
    code='''copies = {"B1": ["DN1", "DN2", "DN3"], "B2": ["DN2", "DN3", "DN4"]}
alive = ["DN1", "DN3", "DN4", "DN5"]
for block in copies:
    copies[block] = [n for n in copies[block] if n in alive]
    for n in alive:
        if len(copies[block]) == 3:
            break
        if n not in copies[block]:
            copies[block].append(n)
print(copies)
''',
    notes={1: 'Start :: Each block is stored on three DataNodes. DN2 holds a copy of both.',
           4: 'Remove dead :: Keep only copies on nodes that are still alive.',
           9: 'Re-replicate :: Add a copy on a live node that doesn\'t have one yet.'},
)

WORKED_INTRO = 'Four storage calculations a data engineer actually makes, from HDFS blocks to a tiered storage bill. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Platform design · choosing', title='Block, file or object?',
         problem='<p>Choose a storage type for each workload using simple rules: databases → block; files people share and edit → file; large analytics data, media and backups → object.</p>',
         inp='orders database, finance team reports, data lake, CCTV footage, VM boot disk',
         approach=['Describe each workload with a kind.',
                   'Map each kind to a storage type with a dictionary.',
                   'Print the choice.'],
         code='''workloads = [("orders database", "database"), ("finance team reports", "shared docs"),
             ("data lake", "analytics"), ("CCTV footage", "media"), ("VM boot disk", "database")]
choice = {"database": "block", "shared docs": "file", "analytics": "object", "media": "object"}
for name, kind in workloads:
    print(f"{name:22} -> {choice[kind]} storage")
''', notes={3: 'Rules :: Each kind of workload maps to one storage type.'},
         tryit='Add “ML training images” and “a team wiki”. Then add a kind <code>"backup"</code> and decide where it goes.'),
    dict(level='i', tag='Hadoop · capacity', title='How much raw HDFS space does a table need?',
         problem='<p>A table grows by 400 GB a day and is kept for 180 days. HDFS uses 3 replicas, and admins keep 25% of disk free. How much raw disk is needed, and how many 48 TB nodes?</p>',
         inp='400 GB/day × 180 days, 3 replicas, 25% free, 48 TB per node',
         approach=['Data kept = daily size × days.',
                   'Raw = data × replicas; then divide by 0.75 to keep 25% free.',
                   'Nodes = raw ÷ capacity per node, rounded up.'],
         code='''import math
data_tb = 400 * 180 / 1024
raw_tb = data_tb * 3
needed_tb = raw_tb / 0.75
nodes = math.ceil(needed_tb / 48)
print(f"Data kept : {data_tb:.0f} TB")
print(f"With 3 copies: {raw_tb:.0f} TB")
print(f"With 25% free: {needed_tb:.0f} TB -> {nodes} nodes of 48 TB")
''', notes={3: 'Replicas :: Three full copies triple the space.', 4: 'Headroom :: Clusters need free space for new data and re-replication.'},
         tryit='Switch to erasure coding 6+3 (raw = data × 1.5). How many nodes now?'),
    dict(level='i', tag='Data lake · layout', title='Design object keys for a lake',
         problem='<p>Build keys for daily order files in the format <code>zone/table/date=YYYY-MM-DD/part-NNNNN.parquet</code>, and then list all keys for one week using a prefix filter.</p>',
         inp='5 days of files, 2 parts per day',
         approach=['Generate dates with <code>datetime.timedelta</code>.',
                   'Format each key with zero-padded part numbers.',
                   'Select a week by comparing the date part of the key.'],
         code='''import datetime
start = datetime.date(2026, 10, 17)
keys = []
for d in range(5):
    day = start + datetime.timedelta(days=d)
    for part in range(2):
        keys.append(f"silver/orders/date={day}/part-{part:05d}.parquet")
week = [k for k in keys if "date=2026-10-19" <= k.split("/")[2] <= "date=2026-10-25"]
print("Total keys:", len(keys))
print("Week keys :", len(week))
print(week[0])
''', notes={7: 'Key :: Hive-style <code>date=</code> prefixes let engines skip whole days.', 8: 'Filter :: Comparing the date folder text works because dates are zero-padded.'},
         tryit='Add a second partition level, <code>city=Pune</code>, before the part file. How would you list one city for one week?'),
    dict(level='a', tag='FinOps · lifecycle', title='Monthly bill with and without storage tiers',
         problem='<p>A lake adds 1 TB a day and keeps data for 2 years. Hot storage costs Rs 1,800, cool Rs 1,000 and archive Rs 100 per TB per month (illustrative). Data is hot for 30 days, cool until 1 year, then archive. Compare the steady-state monthly bill with keeping everything hot.</p>',
         inp='1 TB/day, 730 days, tiers 30 d / 365 d',
         approach=['Count how many days of data sit in each tier once the lake is full.',
                   'Multiply TB in each tier by its price.',
                   'Compare with all 730 TB in hot storage.'],
         code='''price = {"hot": 1800, "cool": 1000, "archive": 100}
tb = {"hot": 30, "cool": 365 - 30, "archive": 730 - 365}
tiered = sum(tb[t] * price[t] for t in tb)
all_hot = 730 * price["hot"]
print("TB per tier :", tb)
print("Tiered bill : Rs", tiered)
print("All hot     : Rs", all_hot)
print(f"Saving      : {(1 - tiered / all_hot) * 100:.0f}%")
''', notes={2: 'Ages :: With 1 TB a day, the number of days in a tier equals its TB.', 3: 'Bill :: Sum of TB × price per tier.'},
         tryit='Archive storage often charges to read data back. Add a cost for restoring 20 TB of archive once a month at Rs 2,000 per TB. Is tiering still worth it?'),
]

QUIZ = [
    dict(q='Which storage type is best suited to a busy relational database?', options=['Object storage', 'Block storage', 'Archive tier', 'Tape'], answer=1,
         why='Databases need low-latency, in-place updates of small blocks: <b>block storage</b>.'),
    dict(q='In object storage, what is a “folder” such as orders/date=2026-10-19/?', options=['A real directory on disk', 'Just a common prefix of object keys', 'A separate bucket', 'A database table'], answer=1,
         why='Object storage has a flat namespace; folders are shown by grouping keys with the same <b>prefix</b>.'),
    dict(q='What is the default HDFS block size in Hadoop 2 and later?', options=['4 KB', '64 KB', '128 MB', '1 GB'], answer=2,
         why='HDFS uses large blocks, <b>128 MB</b> by default, to reduce metadata and favour large sequential reads.'),
    dict(q='Which HDFS component stores the mapping of files to blocks and block locations?', options=['DataNode', 'NameNode', 'ResourceManager', 'Secondary DataNode'], answer=1,
         why='The <b>NameNode</b> holds the namespace and block map in memory; DataNodes store the actual blocks.'),
    dict(q='Why are millions of tiny files a problem in a data lake?', options=['Small files cannot be compressed', 'Each file adds fixed overhead: metadata, listing, opening and per-request costs', 'Object stores reject small files', 'Small files are always corrupted'], answer=1,
         why='The overhead per file dominates when files are tiny. Compact them into files of roughly 128 MB to 1 GB.'),
    dict(q='Compared with 3 full replicas, erasure coding (6 data + 3 parity) mainly:', options=['Uses less raw storage for similar fault tolerance', 'Makes data readable without a network', 'Removes the need for metadata', 'Doubles write speed always'], answer=0,
         why='6+3 needs 1.5× raw space (50% overhead) versus 3× for replication, while still surviving 3 lost pieces.'),
    dict(q='Why is renaming a directory on S3 slower and riskier than on HDFS?', options=['S3 encrypts every rename', 'There are no real directories, so every object must be copied and deleted, which is not atomic', 'S3 limits renames to once a day', 'HDFS renames require copying data'], answer=1,
         why='On HDFS a rename is one metadata operation; on object storage it is copy + delete per object and can leave partial results.'),
    dict(q='A rule that moves objects to a cheaper tier after 90 days and deletes them after 5 years is called a:', options=['Replication factor', 'Lifecycle policy', 'Schema registry', 'Partition key'], answer=1,
         why='Lifecycle policies automate tiering and deletion as data ages.'),
]

REVISION = [
    '<b>Block</b>: raw volumes, fastest, in-place updates, one server → databases.',
    '<b>File</b>: folders and paths, shared (NAS, NFS, SMB) → team documents.',
    '<b>Object</b>: bucket + key + metadata over HTTP, flat namespace, cheapest, nearly unlimited → lakes, backups, media.',
    '<b>HDFS</b>: 128 MB blocks × 3 replicas on DataNodes; NameNode keeps the namespace and block map.',
    'Durability ≠ availability. S3 is designed for eleven nines of durability and is strongly consistent since 2020.',
    'Replication (3× space) vs <b>erasure coding</b> (e.g. 6+3 = 1.5× space).',
    'Avoid <b>small files</b> (compact to 128 MB–1 GB); avoid <b>renames</b> on object stores (use table formats); use <b>lifecycle</b> tiers.',
]
FAQ = [
    ('Differentiate block, file and object storage.', 'Block storage presents raw fixed-size blocks to a single server, which builds a file system or database on top; it offers the lowest latency and in-place updates. File storage organises data as files in a directory hierarchy accessed by path, usually shared over a network with NFS or SMB. Object storage keeps data as immutable objects with unique keys and metadata in a flat namespace of buckets, accessed over HTTP; it is the cheapest and most scalable, and is the usual foundation for data lakes, backups and media.'),
    ('Explain HDFS architecture.', 'HDFS splits files into large blocks (128 MB by default) and stores each block on several DataNodes (replication factor 3 by default, spread across racks). The NameNode maintains the file system namespace and the mapping of blocks to DataNodes in memory; DataNodes store blocks and send heartbeats and block reports. When a DataNode fails, the NameNode re-replicates its blocks from surviving copies. Clients ask the NameNode for block locations and then read or write data directly with DataNodes. A standby NameNode provides high availability.'),
    ('Why has object storage replaced HDFS in many companies?', 'Object storage is fully managed, nearly unlimited, very durable and cheap per GB, and it separates storage from compute, so clusters can be resized or shut down without losing data and many engines can share the same data. HDFS ties storage to the compute cluster and requires running and scaling the hardware yourself. HDFS remains common on-premises, especially where data must stay in a company\'s own data centre.'),
    ('What is the small-files problem and how do you fix it?', 'When data is stored as a huge number of tiny files, the fixed per-file costs (NameNode memory in HDFS, listing and request costs in object storage, task overhead in Spark) dominate, making jobs slow and expensive. Fix it by writing larger files (micro-batches, fewer output partitions), compacting existing files into 128 MB to 1 GB files, and using table formats with automatic compaction.'),
    ('What are storage tiers?', 'Classes of storage with different prices and access speeds, for example hot (frequent access, highest cost per GB), cool or infrequent access, cold, and archive (cheapest, with retrieval taking minutes to hours and extra retrieval charges). Lifecycle policies move data between tiers as it ages and delete it when retention ends.'),
]

PRACTICE_INTRO = 'Storage calculations from HDFS blocks to cloud bills. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Blocks in a file', stmt='How many 128 MB HDFS blocks does a 1,000 MB file need?', inp='1000 MB',
         code='''import math
print(math.ceil(1000 / 128))
''', explain='Round up: 7 full blocks plus one partial block.'),
    dict(level='easy', title='Raw space with replicas', stmt='Print the raw disk space for 20 TB of data with 3 replicas.', inp='20 TB, 3 replicas',
         code='''print(20 * 3, "TB")
''', explain='Every block is stored three times.'),
    dict(level='easy', title='Keys under a prefix', stmt='Print the keys that start with <code>orders/</code>.', inp='4 keys',
         code='''keys = ["orders/a.csv", "reviews/x.jpg", "orders/b.csv", "logs/app.log"]
print([k for k in keys if k.startswith("orders/")])
''', explain='This is what a “folder listing” does in object storage.'),
    dict(level='medium', title='Average file size', stmt='Given file sizes in KB, print the average size in MB and say “compact” if it is below 64 MB.', inp='[40, 52, 38, 61, 45]',
         code='''sizes_kb = [40, 52, 38, 61, 45]
avg_mb = sum(sizes_kb) / len(sizes_kb) / 1024
print(round(avg_mb, 3), "MB ->", "compact" if avg_mb < 64 else "ok")
''', explain='A tiny average file size is the classic sign of the small-files problem.'),
    dict(level='medium', title='Under-replicated blocks', stmt='Print the blocks that have fewer than 3 copies.', inp='B1: 3, B2: 2, B3: 3, B4: 1',
         code='''copies = {"B1": 3, "B2": 2, "B3": 3, "B4": 1}
print([b for b, c in copies.items() if c < 3])
''', explain='HDFS tracks exactly this and re-replicates such blocks automatically.'),
    dict(level='advanced', title='Erasure coding overhead', stmt='Print the raw space and overhead percentage for 100 TB with schemes 3 replicas, 6+3 and 10+4.', inp='100 TB',
         code='''for name, d, p in [("3 replicas", 1, 2), ("6+3", 6, 3), ("10+4", 10, 4)]:
    raw = 100 * (d + p) / d
    print(f"{name:10} {raw:.0f} TB  (+{raw - 100:.0f}%)")
''', explain='Erasure coding gives similar fault tolerance with far less extra space.'),
    dict(level='advanced', title='NameNode memory', stmt='Each file and each block takes about 150 bytes of NameNode RAM. Compare 10 lakh files of 1 MB with the same data in 128 MB files.', inp='10 lakh × 1 MB',
         code='''import math
total_mb = 10_00_000
for size in [1, 128]:
    files = total_mb // size
    blocks = files * math.ceil(size / 128)
    ram_mb = (files + blocks) * 150 / 1024 / 1024
    print(f"{size:4} MB files: {files:8} files, NameNode RAM ≈ {ram_mb:.1f} MB")
''', explain='The same data in large files needs about 128 times less NameNode memory.'),
    dict(level='business', title='Tiered storage saving', stmt='600 TB of data: 50 TB hot (Rs 1,800/TB-month), 250 TB cool (Rs 1,000), 300 TB archive (Rs 100). Print the monthly bill and the saving compared with all hot.', inp='600 TB',
         code='''tiered = 50 * 1800 + 250 * 1000 + 300 * 100
all_hot = 600 * 1800
print("Tiered: Rs", tiered)
print("All hot: Rs", all_hot)
print("Saving: Rs", all_hot - tiered)
''', explain='Moving rarely used data down the tiers cuts the bill sharply. (Prices are illustrative.)'),
    dict(level='business', title='Nodes for a Hadoop cluster', stmt='A company must keep 900 TB of data on HDFS with 3 replicas and 30% free space. Each node has 60 TB. How many nodes?', inp='900 TB, 3×, 30% free, 60 TB/node',
         code='''import math
raw = 900 * 3 / 0.7
print("Raw needed:", round(raw), "TB")
print("Nodes:", math.ceil(raw / 60))
''', explain='Replication and free-space headroom multiply the hardware needed.'),
]

SCN_INTRO = 'Storage decisions and problems from real data teams. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
