import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='05-hdfs-architecture', lesson='04-fsimage-edit-log-and-checkpointing', n='5.4',
    module_label='Module 5 · HDFS architecture',
    title='fsimage, edit log and checkpointing',
    desc='How the NameNode makes its in-memory namespace durable: the fsimage snapshot, the edit log of transactions (OP_MKDIR, OP_ADD, OP_CLOSE, OP_RENAME, OP_DELETE), seen_txid, and checkpoints by the SecondaryNameNode, Standby NameNode or saveNamespace. Real Hadoop 3.5.0 output: metadata folder timeline, a SecondaryNameNode checkpoint log, hdfs oev and hdfs oiv dumps, image retention. Python checkpoint simulator, restart-time calculations, quiz and interview scenarios.',
    og_desc='A photo and a diary: fsimage and the edit log. Read real NameNode metadata files and watch a checkpoint happen.',
    minutes=26, level='Intermediate',
    lead='The NameNode answers every request from memory, yet it survives restarts without losing a single file. The trick is an fsimage snapshot plus an edit log of every change since, merged regularly by a checkpoint. In this lesson you read the real metadata files of a running cluster, decode the edit log entries of your own commands, and watch the SecondaryNameNode take a checkpoint, then learn why skipping checkpoints has caused hours-long outages.',
    chips=['Real metadata files', 'oev / oiv dumps', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Rebuild a namespace from a photo and a diary',
    intro='<p>This program does what a NameNode does at start-up: load the fsimage (a dictionary of paths), then replay each edit after it, in transaction order. The edits are the five real operations from Part 4.</p>',
    code='''fsimage_txid = 66
fsimage = {"/user/hadoop/data": "dir",
           "/user/hadoop/data/canteen_orders.csv": "file"}
edits = [
    (68, "OP_MKDIR", "/user/hadoop/data/edits_demo", None),
    (69, "OP_ADD", "/user/hadoop/data/edits_demo/hello.txt", None),
    (70, "OP_CLOSE", "/user/hadoop/data/edits_demo/hello.txt", None),
    (71, "OP_RENAME_OLD", "/user/hadoop/data/edits_demo/hello.txt",
         "/user/hadoop/data/edits_demo/namaste.txt"),
    (72, "OP_DELETE", "/user/hadoop/data/edits_demo", None),
]

ns = dict(fsimage)
for txid, op, path, dst in edits:
    if txid <= fsimage_txid:
        continue
    if op == "OP_MKDIR":
        ns[path] = "dir"
    elif op == "OP_ADD":
        ns[path] = "file (open)"
    elif op == "OP_CLOSE":
        ns[path] = "file"
    elif op == "OP_RENAME_OLD":
        ns[dst] = ns.pop(path)
    elif op == "OP_DELETE":
        ns = {p: k for p, k in ns.items() if p != path and not p.startswith(path + "/")}
    print(f"txid {txid}: {op:14} -> {len(ns)} paths")
print(sorted(ns))
''',
    anno=[
        ('if txid <= fsimage_txid:', 'Edits already contained in the fsimage are skipped. Only transactions after the image\'s txid are replayed.'),
        ('ns[path] = "file (open)"', 'OP_ADD creates the file while it is being written; OP_CLOSE marks it complete.'),
        ('ns = {p: k for p, k in ns.items() if p != path and not p.startswith(path + "/")}', 'Deleting a directory removes everything below it too.'),
    ],
    tasks=[
        dict(label='1 · Replay the edits', hint='Press <b>Run</b>. The final namespace should match the real fsimage_…073 listing: no edits_demo.', code=None),
        dict(label='2 · Restart time', hint='<b>Predict first:</b> loading an fsimage takes 2 minutes, and replay runs at 50,000 edits per second. How long is a restart with 10 lakh, 1 crore and 10 crore edits since the last checkpoint?',
             code='''load_s, rate = 120, 50_000
for edits in [10_00_000, 1_00_00_000, 10_00_00_000]:
    total = load_s + edits / rate
    print(f"{edits:>13,} edits -> {total / 60:5.1f} minutes")
'''),
        dict(label='3 · When is the next checkpoint?', hint='A checkpoint happens after 3600 s or 10 lakh transactions, whichever comes first. With 400 changes per second, which trigger fires first?',
             code='''period_s, txns = 3600, 1_000_000
for per_second in [50, 400]:
    by_count = txns / per_second
    first = min(period_s, by_count)
    print(f"{per_second} tx/s: checkpoint after {first:.0f} s ({'count' if by_count < period_s else 'time'})")
'''),
        dict(label='4 · Read file names', hint='Parse the real names from the metadata folder: which transactions does each edits file cover, and which is the newest fsimage?',
             code='''names = ["edits_0000000000000000001-0000000000000000044", "edits_0000000000000000065-0000000000000000066",
         "edits_inprogress_0000000000000000067", "fsimage_0000000000000000064", "fsimage_0000000000000000066"]
for n in names:
    parts = n.split("_")
    if n.startswith("edits_inprogress"):
        print(n[:16], "from", int(parts[2]), "onwards (being written)")
    elif n.startswith("edits"):
        a, b = parts[1].split("-")
        print("edits", int(a), "to", int(b))
print("newest image txid:", max(int(n.split("_")[1]) for n in names if n.startswith("fsimage")))
'''),
        dict(label='5 · Spot the error', hint='This replay applies the edits in the wrong order, so the rename fails. Fix it so edits are replayed by transaction ID.',
             code='''ns = {}
edits = [(71, "rename", "a", "b"), (69, "add", "a", None)]
for txid, op, path, dst in edits:
    if op == "add":
        ns[path] = "file"
    elif op == "rename":
        ns[dst] = ns.pop(path)
print(ns)
''', expect='error'),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: watch your commands land in the edit log',
    intro='<p>This script makes four changes in HDFS, then decodes the newest edit log segments with <code>hdfs oev</code> and prints only the transactions your commands created. Save it as <code>edit_log_report.py</code> in the <code>hdfs-lab</code> folder and run it while the cluster is up.</p>',
    items=[
        dict(title='Your commands, as NameNode transactions', file='edit_log_report.py',
             cmd=open(os.path.join(HERE, 'edit_log_report.py')).read() + '\n# In the hdfs-lab folder:\n#   python3 edit_log_report.py',
             output='''last transaction before our changes: 109
txid  110  OP_MKDIR        /user/hadoop/data/demo   [edits_inprogress_0000000000000000099]
txid  111  OP_ADD          /user/hadoop/data/demo/order.txt   [edits_inprogress_0000000000000000099]
txid  112  OP_CLOSE        /user/hadoop/data/demo/order.txt   [edits_inprogress_0000000000000000099]
txid  113  OP_RENAME_OLD   /user/hadoop/data/demo/order.txt -> /user/hadoop/data/demo/order_old.txt   [edits_inprogress_0000000000000000099]
txid  114  OP_DELETE       /user/hadoop/data/demo   [edits_inprogress_0000000000000000099]''',
             note='Real output. The script reads the last transaction ID from the NameNode\'s <code>/jmx</code> first, so it shows only new entries. Run it twice: the transaction numbers keep growing, and after a checkpoint the entries move from the in-progress file to a closed segment.'),
    ],
)

TRACE = dict(
    heading='A checkpoint, one line at a time',
    intro='<p>Follow the SecondaryNameNode: it loads the old image, applies only newer edits, and produces an image with a new transaction ID.</p>',
    code='''image_txid, image = 64, {"/data"}
edits = [(65, "start", None), (66, "end", None), (67, "start", None),
         (68, "mkdir", "/data/demo"), (69, "add", "/data/demo/a.txt")]
rolled_at = 69
for txid, op, path in edits:
    if image_txid < txid <= rolled_at and op in ("mkdir", "add"):
        image.add(path)
image_txid = rolled_at
print("new fsimage txid:", image_txid, sorted(image))
''',
    notes={4: 'Roll :: The NameNode closed the edit log at txid 69; later edits wait for the next checkpoint.',
           6: 'Merge :: Apply only edits after the old image and up to the roll point.',
           8: 'Result :: The new image\'s file name will be fsimage_…069.'},
)

WORKED_INTRO = 'Three checkpoint calculations that matter in operations: how fast edits accumulate, how long a restart would take right now, and whether metadata storage is safe. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Operations · rate', title='How many edits per day?',
         problem='<p>A cluster\'s jobs create 30 lakh files a day (each create is OP_ADD + OP_CLOSE plus a few block allocations, about 5 transactions in total) and delete as many. Deleting is one transaction per path. How many transactions per day, and how often is the 10 lakh-transaction checkpoint trigger reached?</p>',
         inp='30,00,000 creates × 5 tx · 30,00,000 deletes × 1 tx · trigger 10,00,000',
         approach=['Transactions = creates × 5 + deletes × 1.',
                   'Checkpoints by count = transactions / 10 lakh.',
                   'Compare with the hourly trigger (24 a day).'],
         code='''creates, deletes = 30_00_000, 30_00_000
tx = creates * 5 + deletes
by_count = tx / 1_000_000
print(f"{tx:,} transactions/day -> count trigger {by_count:.0f} times/day, time trigger 24 times/day")
''', notes={3: 'Rate :: Here the hourly trigger wins: 24 a day against 18 by count.'},
         tryit='Raise creates to 1 crore a day. The count trigger now fires about 53 times a day (roughly every 27 minutes), more often than the hourly one: the SecondaryNameNode must keep up.'),
    dict(level='i', tag='Operations · restart', title='How long would a restart take now?',
         problem='<p>The last successful checkpoint was 9 days ago (it has been failing silently). The cluster logs 2 crore transactions a day. Loading the fsimage takes 4 minutes and replay runs at 60,000 transactions per second. Estimate the restart time, then the time if checkpoints were working (at most 10 lakh edits).</p>',
         inp='9 days × 2 crore tx · load 4 min · 60,000 tx/s',
         approach=['Edits to replay = days × daily transactions.',
                   'Restart = load + edits / rate.',
                   'Compare with the healthy case.'],
         code='''daily, days, rate, load_min = 2_00_00_000, 9, 60_000, 4
for label, edits in [("broken checkpoints", daily * days), ("healthy", 1_000_000)]:
    minutes = load_min + edits / rate / 60
    print(f"{label:20}: {edits:>13,} edits -> {minutes:6.0f} min")
''', notes={3: 'Replay :: Every transaction since the last image must be re-applied.'},
         tryit='The broken case is almost an hour of downtime (about 54 minutes) instead of 4. This is why “time since last checkpoint” is a standard NameNode alert.'),
    dict(level='a', tag='Admin · resilience', title='Check the metadata directories',
         problem='<p>Write a checker for <code>dfs.namenode.name.dir</code>: warn if there is only one directory, if two directories are on the same disk, or if any is under <code>/tmp</code>.</p>',
         inp='"file:///data/1/nn,file:///data/1/nn-copy,file:///tmp/nn" · disks: /data/1, /tmp',
         approach=['Split the comma-separated value.',
                   'Map each path to its disk (mount point).',
                   'Apply the three checks.'],
         code='''value = "file:///data/1/nn,file:///data/1/nn-copy,file:///tmp/nn"
dirs = [d.replace("file://", "") for d in value.split(",")]
disk = lambda p: "/".join(p.split("/")[:3])
problems = []
if len(dirs) < 2:
    problems.append("only one metadata directory")
if len({disk(d) for d in dirs}) < len(dirs):
    problems.append("several directories on the same disk")
problems += [f"{d} is under /tmp" for d in dirs if d.startswith("/tmp")]
print(dirs)
print("\\n".join(problems) or "looks good")
''', notes={4: 'Disk :: Here the first two path parts stand for the mount point.'},
         tryit='Fix it to two directories on different disks (e.g. /data/1/nn and /data/2/nn). In HA clusters the edit log is also on JournalNodes.'),
]

QUIZ = mix([
    dict(q='What is the fsimage?', options=['A log of recent changes', 'A complete snapshot of the namespace as of a transaction ID', 'A copy of all file data', 'A DataNode report'], answer=1,
         why='fsimage_N is the namespace after transaction N.'),
    dict(q='What does the edit log record?', options=['Block contents', 'Every namespace change (mkdir, create, rename, delete…) with a transaction ID', 'DataNode heartbeats', 'User passwords'], answer=1,
         why='We decoded OP_MKDIR, OP_ADD, OP_CLOSE, OP_RENAME_OLD and OP_DELETE.'),
    dict(q='What is the main job of the SecondaryNameNode?', options=['Take over when the NameNode fails', 'Merge the fsimage with the edit log into a new fsimage (checkpoint)', 'Store a second copy of every block', 'Run MapReduce jobs'], answer=1,
         why='It is a checkpoint helper, not a standby.'),
    dict(q='By default, a checkpoint happens:', options=['Every 3 seconds', 'Every hour or after 10 lakh transactions, whichever comes first', 'Once a day', 'Only when an admin runs it'], answer=1,
         why='dfs.namenode.checkpoint.period = 3600 and dfs.namenode.checkpoint.txns = 1,000,000.'),
    dict(q='At start-up, the NameNode:', options=['Reads every DataNode\'s disk', 'Loads the latest fsimage and replays the edits after it', 'Formats itself', 'Copies the SecondaryNameNode\'s memory'], answer=1,
         why='Then it waits for block reports to rebuild the block map (safe mode).'),
    dict(q='Why are long periods without checkpoints dangerous?', options=['DataNodes stop', 'The edit log grows and the next restart must replay all of it, which can take hours', 'Files are deleted', 'Replication stops'], answer=1,
         why='Restart time grows with the number of edits since the last image.'),
    dict(q='In an HA cluster, who performs checkpoints?', options=['The SecondaryNameNode', 'The Standby NameNode', 'The ResourceManager', 'Each DataNode'], answer=1,
         why='HA clusters have no SecondaryNameNode; the Standby does it.'),
    dict(q='What does hdfs dfsadmin -saveNamespace require?', options=['The NameNode in safe mode', 'All DataNodes stopped', 'A formatted cluster', 'YARN to be running'], answer=0,
         why='We entered safe mode, saved the namespace, and left safe mode.'),
])

REVISION = [
    '<b>fsimage_N</b> = full namespace after transaction N. <b>edits</b> = every change after it (write-ahead log).',
    'Files: <code>edits_A-B</code> (closed), <code>edits_inprogress_N</code> (current), <code>seen_txid</code>, <code>VERSION</code>.',
    'Ops: OP_MKDIR, OP_ADD + OP_CLOSE (create), OP_RENAME(_OLD), OP_DELETE, plus segment start/end markers.',
    'Start-up = load latest fsimage + replay newer edits (+ wait for block reports).',
    '<b>Checkpoint</b>: roll edits → download → merge → upload new fsimage. Every <b>1 h or 10 lakh tx</b>.',
    'Done by <b>SecondaryNameNode</b> (non-HA) or <b>Standby NameNode</b> (HA); manually with <code>-saveNamespace</code> (safe mode).',
    'SecondaryNameNode is <b>not</b> a backup NameNode. 2 images retained by default.',
    'Tools: <code>hdfs oiv</code> (fsimage), <code>hdfs oev</code> (edits), <code>dfsadmin -fetchImage</code> (backup).',
]
FAQ = [
    ('What are fsimage and edit log in HDFS?', 'The fsimage is a persistent snapshot of the entire file system namespace at a certain transaction ID. The edit log records every change made after that snapshot. Together they let the NameNode rebuild its in-memory namespace after a restart.'),
    ('What is checkpointing in HDFS?', 'Merging the latest fsimage with the edit log that follows it to produce a new fsimage, so that the edit log stays short and restarts are fast. It is done periodically by the SecondaryNameNode (or Standby NameNode in HA).'),
    ('Is the SecondaryNameNode a backup of the NameNode?', 'No. It only creates checkpoints. If the NameNode fails, the SecondaryNameNode cannot serve clients. Its latest checkpoint can help recover metadata, but it may be missing recent edits. Automatic takeover requires HA with a Standby NameNode.'),
    ('How often does a checkpoint happen?', 'By default every 3600 seconds (dfs.namenode.checkpoint.period) or when 1,000,000 transactions have accumulated (dfs.namenode.checkpoint.txns), whichever comes first. The SecondaryNameNode checks the transaction count every 60 seconds.'),
    ('Does the fsimage contain block locations?', 'No. It contains each file\'s list of blocks but not which DataNodes hold them. Locations come from DataNode block reports after start-up.'),
    ('How can I read an fsimage or edits file?', 'With the offline viewers: hdfs oiv -p XML|Delimited -i fsimage_N -o out for images, and hdfs oev -i edits_file -o out.xml for edit logs. Run them on copies, not on files the NameNode is using.'),
    ('What happens if the edit log is lost?', 'All namespace changes since the last checkpoint are lost: files created or renamed after it disappear from the namespace, even though their blocks may still be on DataNodes. That is why edits are written to several directories or JournalNodes.'),
]

PRACTICE_INTRO = 'Exercises on transactions, checkpoint timing and metadata files, using real file names from the lab.'
PROBLEMS = [
    dict(level='easy', title='Transactions in a segment', stmt='How many transactions does edits_0000000000000000045-0000000000000000062 contain?', inp='45 to 62',
         code='print(62 - 45 + 1)\n', explain='18 transactions (both ends included).'),
    dict(level='easy', title='Newest image', stmt='Given the image files fsimage_…064, fsimage_…066 and fsimage_…073, which one will the NameNode load at restart?', inp='064 · 066 · 073',
         code='print("fsimage_%019d" % max([64, 66, 73]))\n', explain='fsimage_0000000000000000073, the highest transaction ID.'),
    dict(level='easy', title='Operations per create', stmt='Creating one empty file produced OP_ADD and OP_CLOSE. How many transactions for 1,000 empty files?', inp='1,000 files · 2 ops each',
         code='print(1000 * 2)\n', explain='2,000 transactions. Files with data also log block allocations.'),
    dict(level='medium', title='Which edits to replay?', stmt='The newest fsimage is at txid 73 and the edit segments are 1-44, 45-62, 63-64, 65-66, 67-73 and in-progress from 74 (now at 81). Which transactions are replayed at restart?', inp='image 73 · segments … · in-progress 74–81',
         code='''image = 73
segments = [(1, 44), (45, 62), (63, 64), (65, 66), (67, 73), (74, 81)]
replay = [s for s in segments if s[1] > image]
print(replay, "->", sum(b - max(a, image + 1) + 1 for a, b in replay), "transactions")
''', explain='Only segment 74–81: 8 transactions. Everything up to 73 is already in the image.'),
    dict(level='medium', title='Retention', stmt='With num.checkpoints.retained = 2, which fsimage files remain after images at txids 64, 66 and 73 have been written?', inp='64 · 66 · 73 · retain 2',
         code='print(sorted([64, 66, 73])[-2:])\n', explain='[66, 73]: exactly what the folder listing showed after saveNamespace (064 was removed).'),
    dict(level='medium', title='Checkpoint trigger', stmt='The cluster logs 250 transactions per second. Will the time (3600 s) or count (10 lakh) trigger fire first, and after how long?', inp='250 tx/s',
         code='''t = 1_000_000 / 250
print("count" if t < 3600 else "time", "trigger after", min(t, 3600), "s")
''', explain='Time: 10 lakh transactions would take 4,000 s at 250/s, so the hourly time trigger (3,600 s) fires first.'),
    dict(level='business', title='Cost of a slow restart', stmt='A restart with a huge edit log takes 3 hours instead of 10 minutes. 400 analysts each lose Rs 1,200 of work per hour of downtime. What does the extra time cost?', inp='170 extra minutes · 400 people · Rs 1,200/h',
         code='''extra_h = (180 - 10) / 60
print(f"Rs {extra_h * 400 * 1200 / 1e5:.1f} lakh")
''', explain='About Rs 13.6 lakh for one restart, more than the cost of monitoring checkpoints for years.'),
    dict(level='advanced', title='Detect a stuck checkpoint', stmt='Given (time, last checkpoint txid, current txid) samples, alert if the checkpoint txid has not changed for more than 2 hours while transactions keep increasing.', inp='samples every hour',
         code='''samples = [(0, 500, 900), (1, 500, 1_200_000), (2, 500, 2_400_000), (3, 500, 3_500_000)]
first = next(t for t, cp, cur in samples if cp == samples[-1][1])
t_now, cp, cur = samples[-1]
if t_now - first > 2 and cur > cp:
    print(f"ALERT: no checkpoint for {t_now - first} h, {cur - cp:,} edits pending")
''', explain='The checkpoint txid has been stuck at 500 for 3 hours while 35 lakh edits accumulated: the SecondaryNameNode is failing.'),
]

SCN_INTRO = 'Interviewers love the SecondaryNameNode because its name misleads so many candidates.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“The NameNode crashed. Can the SecondaryNameNode take over?”</h4>
      <p class="scn__situation">A very common trick question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you know what the SecondaryNameNode actually does.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No. The SecondaryNameNode only merges the fsimage and edit log into checkpoints; it never serves clients.</li>
          <li>Restart the NameNode (it loads its fsimage + edits). If its metadata disks are lost, the SecondaryNameNode's latest checkpoint can be used to recover, losing edits since that checkpoint.</li>
          <li>Automatic takeover needs HA: an active and a standby NameNode with shared edits on JournalNodes.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · incident</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>The NameNode has been “starting” for two hours</h4>
      <p class="scn__situation">After a planned restart the NameNode UI shows Startup Progress stuck in “Loading edits”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> root cause and prevention.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>It is replaying a very large edit log, which means checkpoints haven't been happening. Check the SecondaryNameNode/Standby logs and the last checkpoint time.</li>
          <li>Let it finish (interrupting makes it start again). Afterwards fix the checkpoint process: memory, connectivity on port 9868/9870, disk space for <code>checkpoint.dir</code>.</li>
          <li>Prevent: alert on time and transactions since the last checkpoint; before planned restarts run <code>saveNamespace</code> in safe mode.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · durability</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Why is every change written to the edit log before it's acknowledged?</h4>
      <p class="scn__situation">An interviewer asks why the NameNode doesn't just update memory and write a snapshot every minute.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> write-ahead logging.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Memory is lost on a crash. If changes were only in memory, a crash would forget every file created since the last snapshot, even though clients were told “success”.</li>
          <li>Appending a small record to a log (and syncing it) is cheap; rewriting a multi-GB image is not. So: log first, then apply, then acknowledge.</li>
          <li>Snapshots (checkpoints) only exist to keep the log short. Databases use the same idea (write-ahead log + checkpoints).</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Analytics · metadata</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Find the folders with the most small files, without slowing the NameNode</h4>
      <p class="scn__situation">A manager wants a report of small files per team across a 40-crore-file namespace.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> that you know the offline fsimage approach.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Running <code>hdfs dfs -ls -R</code> or <code>-count</code> over everything would load the NameNode heavily.</li>
          <li>Instead download the latest image (<code>hdfs dfsadmin -fetchImage</code>), convert it with <code>hdfs oiv -p Delimited</code>, and analyse the table with Hive or Spark: count files under 1 MB per top-level folder or owner.</li>
          <li>Schedule it daily to track progress.</li>
        </ul>
      </div></details>
    </article>
'''
