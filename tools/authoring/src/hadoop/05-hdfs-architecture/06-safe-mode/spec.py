import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='05-hdfs-architecture', lesson='06-safe-mode', n='5.6',
    module_label='Module 5 · HDFS architecture',
    title='Safe mode',
    desc='HDFS safe mode: the NameNode\'s read-only start-up state while it waits for block reports, the 0.999 threshold and 30-second extension, manual safe mode, and what a stuck safe mode means. Real Hadoop 3.5.0 runs: restarts with all, none and some DataNodes, SafeModeException on write, “Zero blocklocations” on read, and a missing block that slipped past the whole-number threshold. Python threshold calculator, quiz and interview scenarios.',
    og_desc='Why HDFS says “Name node is in safe mode”, when it ends by itself, and when it never will. Real restarts on a lab cluster.',
    minutes=22, level='Beginner → Intermediate',
    lead='Every time a NameNode starts, it spends a little while in safe mode: it can list files but won\'t change anything until DataNodes have reported where the blocks are. This lesson shows real restarts with all, none and some DataNodes running, explains the threshold and extension behind the countdown, and teaches you to read a stuck safe mode as a symptom rather than an obstacle to force away.',
    chips=['Real restart timelines', 'Threshold calculator', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Will the NameNode leave safe mode?',
    intro='<p>This function applies the safe mode rules: the needed count is the whole-number part of total blocks × threshold, plus the minimum number of live DataNodes. Run it on the real cases from Part 4.</p>',
    code='''def safe_mode(total_blocks, reported, live_dns, threshold=0.999, min_dns=0):
    needed = int(total_blocks * threshold)
    blocks_ok = reported >= needed
    dns_ok = live_dns >= min_dns
    if blocks_ok and dns_ok:
        return f"reported {reported}/{total_blocks} (needed {needed}): leaves after 30 s extension"
    return f"reported {reported}/{total_blocks} (needed {needed}): STAYS in safe mode"

print(safe_mode(8, 8, 4))       # restart, all DataNodes up
print(safe_mode(8, 0, 0))       # restart, no DataNodes
print(safe_mode(9, 8, 3))       # replication-1 file on a stopped DataNode
print(safe_mode(10_00_000, 998_000, 400))
''',
    anno=[
        ('needed = int(total_blocks * threshold)', 'int() keeps only the whole-number part: int(9 × 0.999) = int(8.991) = 8. That is why 8 of 9 was enough in our lab.'),
        ('dns_ok = live_dns >= min_dns', 'dfs.namenode.safemode.min.datanodes is 0 by default, so this never blocks unless an admin sets it.'),
    ],
    tasks=[
        dict(label='1 · The real cases', hint='Press <b>Run</b>. Then try <code>safe_mode(1000, 999, 10)</code> and <code>safe_mode(1000, 998, 10)</code>.', code=None),
        dict(label='2 · How many may be missing?', hint='<b>Predict first:</b> how many blocks can be missing and still let the NameNode leave safe mode, for 9, 1,000 and 1 crore blocks?',
             code='''for total in [9, 1_000, 1_00_00_000]:
    print(f"{total:>11,} blocks: up to {total - int(total * 0.999):,} missing")
'''),
        dict(label='3 · Extension countdown', hint='The real log said “turned off automatically in 28 seconds” at t=10 s. When was the threshold reached, and when will safe mode end?',
             code='''t_now, left, extension = 10, 28, 30
reached = t_now - (extension - left)
print("threshold reached at t =", reached, "s; safe mode ends at t =", t_now + left, "s")
'''),
        dict(label='4 · Allowed or refused?', hint='Classify commands as allowed or refused in safe mode.',
             code='''allowed = {"ls", "stat", "cat", "get", "fsck", "getconf", "saveNamespace"}
for cmd in ["ls", "put", "mkdir", "cat", "rm", "fsck", "setrep", "saveNamespace"]:
    print(f"{cmd:14}", "allowed" if cmd in allowed else "REFUSED")
'''),
        dict(label='5 · Spot the error', hint='This calculator rounds the needed count up, which disagrees with the real NameNode for 9 blocks. Fix it.',
             code='''import math
needed = math.ceil(9 * 0.999)
print("needed:", needed, "-> 8 reported is", "enough" if 8 >= needed else "NOT enough")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: follow a NameNode restart',
    intro='<p>This script restarts the lab NameNode, then every few seconds asks for the safe mode state and reads the NameNode\'s own explanation from <code>/jmx</code>. Save it as <code>safemode_watch.py</code> in the <code>hdfs-lab</code> folder and run it while the DataNodes are up.</p>',
    items=[
        dict(title='Safe mode from restart to OFF', file='safemode_watch.py',
             cmd=open(os.path.join(HERE, 'safemode_watch.py')).read() + '\n# In the hdfs-lab folder:\n#   python3 safemode_watch.py',
             output='''t=  4s  (no answer)              (NameNode not answering yet)
t= 11s  Safe mode is ON          reported 8/8 blocks, off in 25 s
t= 18s  Safe mode is ON          reported 8/8 blocks, off in 18 s
t= 25s  Safe mode is ON          reported 8/8 blocks, off in 11 s
t= 32s  Safe mode is ON          reported 8/8 blocks, off in 4 s
t= 39s  Safe mode is OFF         (off)''',
             note='Real output. Stop one or all DataNodes before running it to see the other cases from Part 4; with none running, the loop ends after 2 minutes with safe mode still ON.'),
    ],
)

TRACE = dict(
    heading='The NameNode counting block reports',
    intro='<p>Follow the safe-block count as three DataNodes report, and see the moment the threshold is reached.</p>',
    code='''total = 9
needed = int(total * 0.999)
safe = set()
reports = {"dn2": ["b1", "b2", "b3", "b4"], "dn3": ["b3", "b5", "b6"], "dn4": ["b7", "b8", "b1"]}
for dn, blocks in reports.items():
    safe.update(blocks)
    print(dn, "reported ->", len(safe), "safe blocks", "(threshold reached)" if len(safe) >= needed else "")
''',
    notes={2: 'Needed :: int(8.991) = 8.',
           6: 'Safe :: A block counts once it has one reported replica, however many DataNodes report it.'},
)

WORKED_INTRO = 'Three safe mode questions that come up in operations: how long a restart will keep the cluster read-only, how much missing data the threshold tolerates, and when forcing safe mode off is reasonable. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Operations · timing', title='How long will the cluster be read-only?',
         problem='<p>A NameNode takes 6 minutes to load its fsimage and edits. DataNodes then report over 4 minutes, with the threshold reached at 3 min 50 s. The extension is 30 s. How long after the restart can jobs write again?</p>',
         inp='load 6 min · threshold at 3 min 50 s after reports start · extension 30 s',
         approach=['Start of safe mode = after loading.',
                   'Threshold time = load + 230 s.',
                   'Add the extension.'],
         code='''load_s, to_threshold_s, extension_s = 6 * 60, 3 * 60 + 50, 30
total = load_s + to_threshold_s + extension_s
print(f"writes allowed after {total // 60} min {total % 60} s")
''', notes={2: 'Sum :: Loading, reporting and extension happen one after another.'},
         tryit='Regular checkpoints shrink the load time (Lesson 5.4); spreading block reports avoids a slow reporting phase.'),
    dict(level='i', tag='Risk · threshold', title='How much data could be missing when it leaves?',
         problem='<p>A cluster has 2 crore blocks averaging 100 MB. With the default threshold, how many blocks (and roughly how much data) may still have no reported replica when the NameNode leaves safe mode?</p>',
         inp='2,00,00,000 blocks · 100 MB each · 0.999',
         approach=['Missing allowed = total − int(total × 0.999).',
                   'Data = missing × 100 MB.',
                   'Convert to TB.'],
         code='''total, mb = 2_00_00_000, 100
missing = total - int(total * 0.999)
print(f"up to {missing:,} blocks, about {missing * mb / 2**20:.1f} TB")
''', notes={3: 'Tolerance :: 0.1% of blocks may still be unreported.'},
         tryit='Those blocks may just be on late DataNodes, but always run fsck after a big restart to see if any are really missing.'),
    dict(level='a', tag='Decision · force leave', title='Should we force safe mode off?',
         problem='<p>Write a small decision helper: given total and reported blocks, the number of DataNodes expected and registered, and whether those missing DataNodes are known to be permanently lost, recommend “wait”, “investigate”, or “leave and accept loss”.</p>',
         inp='case A: 1,000,000 / 990,000, 400 expected / 380 up, not lost · case B: same, nodes lost',
         approach=['If DataNodes are still missing and might return → wait/investigate.',
                   'If they are permanently lost and data is accepted as lost (or other replicas exist elsewhere) → leave, then fsck.',
                   'Print the reasoning.'],
         code='''def advise(total, reported, expected_dns, up_dns, lost_for_good):
    needed = int(total * 0.999)
    if reported >= needed:
        return "wait: it will leave by itself after the extension"
    if up_dns < expected_dns and not lost_for_good:
        return f"investigate: {expected_dns - up_dns} DataNodes not registered yet"
    return "leave safe mode, then run fsck and restore/regenerate missing data"

print("A:", advise(1_000_000, 990_000, 400, 380, False))
print("B:", advise(1_000_000, 990_000, 400, 380, True))
''', notes={4: 'First :: If the threshold is reached, there is nothing to do.'},
         tryit='Case A is the common one: a rack powering up late. Forcing safe mode off there would mark lakhs of healthy blocks as missing.'),
]

QUIZ = mix([
    dict(q='What is HDFS safe mode?', options=['A backup copy of HDFS', 'A read-only NameNode state, mainly at start-up while block reports arrive', 'Encryption of all files', 'A mode where DataNodes stop'], answer=1,
         why='Reads of metadata are allowed; changes and replication are not.'),
    dict(q='When does the NameNode leave start-up safe mode automatically?', options=['After exactly 1 minute', 'When 99.9% of blocks have at least one reported replica, plus a 30 s extension', 'When all DataNodes have restarted twice', 'Never; an admin must leave it'], answer=1,
         why='threshold-pct 0.999, extension 30,000 ms.'),
    dict(q='During safe mode, hdfs dfs -put fails with:', options=['FileNotFoundException', 'Name node is in safe mode (SafeModeException)', 'Permission denied', 'Disk full'], answer=1,
         why='We saw: “put: Cannot create file … Name node is in safe mode.”'),
    dict(q='With all DataNodes stopped, why does hdfs dfs -ls work but -cat fail?', options=['ls is cached on the client', 'The namespace is loaded from the fsimage, but block locations come only from DataNode reports', 'cat needs YARN', 'ls bypasses the NameNode'], answer=1,
         why='“Zero blocklocations … Name node is in safe mode.”'),
    dict(q='Which command should a start-up script run before writing data?', options=['hdfs dfsadmin -safemode leave', 'hdfs dfsadmin -safemode wait', 'hdfs namenode -format', 'hdfs dfs -rm -r /'], answer=1,
         why='wait blocks until safe mode is off, without forcing anything.'),
    dict(q='A NameNode entered safe mode with -safemode enter. When does it leave?', options=['After 30 s', 'When block reports arrive', 'Only when an admin runs -safemode leave', 'At the next checkpoint'], answer=2,
         why='Manual safe mode is never left automatically.'),
    dict(q='With 9 blocks and threshold 0.999, how many must be reported?', options=['9', '8', '7', '1'], answer=1,
         why='int(9 × 0.999) = int(8.991) = 8. Our lab left safe mode with 1 block missing.'),
    dict(q='The NameNode is stuck in safe mode after a restart. The best first step is:', options=['Run -safemode leave immediately', 'Check reported vs total blocks and which DataNodes haven\'t registered', 'Format the NameNode', 'Delete the edit log'], answer=1,
         why='Stuck safe mode is a symptom: usually DataNodes or disks are missing.'),
])

REVISION = [
    'Safe mode = NameNode <b>read-only</b>: metadata reads OK; no create/delete/rename; no replication.',
    'Entered automatically at <b>start-up</b> (after loading fsimage + edits) until block reports arrive.',
    'Leaves when reported safe blocks ≥ <b>int(total × 0.999)</b> and live DNs ≥ min (0), then after a <b>30 s</b> extension.',
    'Real lab: ~40 s in safe mode per restart; with no DataNodes it waits for ever.',
    'Commands: <code>hdfs dfsadmin -safemode get | wait | enter | leave</code>.',
    'Manual (<code>enter</code>) safe mode only ends with <code>leave</code>. Also entered when metadata disk is low.',
    'Errors: put → “Name node is in safe mode”; cat → “Zero blocklocations”.',
    'Stuck = missing DataNodes/blocks. Investigate before forcing; check fsck after leaving.',
]
FAQ = [
    ('What is safe mode in HDFS?', 'A read-only state of the NameNode. At start-up it loads the namespace and then waits for DataNodes to report their blocks. Until enough blocks are reported, it allows reading metadata but no modifications and no replication, so it doesn\'t act on incomplete information.'),
    ('How do I leave safe mode?', 'Normally you just wait: it ends automatically when 99.9% of blocks are reported plus 30 seconds. Use hdfs dfsadmin -safemode wait in scripts. hdfs dfsadmin -safemode leave forces it off, which is appropriate only after you know why it is stuck (or after a manual enter).'),
    ('Why is my NameNode stuck in safe mode?', 'Usually because DataNodes holding a significant share of blocks have not registered: they are down, their disks are not mounted, or dfs.datanode.data.dir points to the wrong folder. It can also be caused by low disk space on the NameNode\'s metadata directories.'),
    ('Can I read files in safe mode?', 'You can read metadata (ls, stat). File data can be read for blocks whose replicas have already been reported; blocks with no reported replica cannot be read yet.'),
    ('What do threshold-pct and extension mean?', 'dfs.namenode.safemode.threshold-pct (0.999) is the fraction of blocks that must have at least dfs.namenode.replication.min reported replicas. dfs.namenode.safemode.extension (30,000 ms) is how long the NameNode stays in safe mode after reaching that threshold, to let late reports arrive.'),
    ('Does leaving safe mode guarantee no data is missing?', 'No. The threshold allows a small fraction of blocks (0.1%, rounded) to be unreported. Run hdfs fsck / after restarts to find missing or corrupt blocks.'),
]

PRACTICE_INTRO = 'Safe mode exercises built on the real restarts from the lab.'
PROBLEMS = [
    dict(level='easy', title='Needed blocks', stmt='Compute the number of blocks that must be reported for totals 8, 9 and 1,000.', inp='8 · 9 · 1000',
         code='''for t in [8, 9, 1000]:
    print(t, "->", int(t * 0.999))
''', explain='7, 8 and 999. For tiny clusters one block may be missing; at 1,000 blocks exactly one may be.'),
    dict(level='easy', title='Extension end', stmt='A NameNode log line at 07:27:01 says “Safe mode will be turned off automatically in 9 seconds.” When should it turn off?', inp='07:27:01 + 9 s',
         code='''from datetime import datetime, timedelta
print((datetime(2026, 10, 21, 7, 27, 1) + timedelta(seconds=9)).time())
''', explain='07:27:10. The real log shows “STATE* Safe mode is OFF” at 07:27:11, one second later because the check runs periodically.'),
    dict(level='easy', title='Time in safe mode', stmt='A log says “Leaving safe mode after 70 secs”. The NameNode spent 25 s waiting for DataNodes to start and 30 s in the extension. How long was it waiting for block reports after the DataNodes started?', inp='70 · 25 · 30',
         code='print(70 - 25 - 30, "s")\n', explain='About 15 s for registration and block reports.'),
    dict(level='medium', title='Parse the NameNode message', stmt='Extract reported, total and seconds left from the real message.', inp='The reported blocks 8 has reached the threshold 0.9990 of total blocks 8. … in 24 seconds.',
         code='''import re
msg = ("The reported blocks 8 has reached the threshold 0.9990 of total blocks 8. "
       "The minimum number of live datanodes is not required. In safe mode extension. "
       "Safe mode will be turned off automatically in 24 seconds.")
r, t = re.search(r"reported blocks (\\d+).*total blocks (\\d+)", msg).groups()
left = re.search(r"in (\\d+) seconds", msg).group(1)
print(f"{r}/{t} reported, {left} s left")
''', explain='8/8 reported, 24 s left: the same parsing safemode_watch.py does.'),
    dict(level='medium', title='Blocks per DataNode needed', stmt='600,000 blocks with replication 3 are spread evenly over 300 DataNodes. Roughly how many DataNodes must report before every block has at least one reported replica, if reports arrive from random nodes? Simulate it.', inp='600,000 blocks · 3 replicas · 300 nodes',
         code='''import random
random.seed(1)
nodes = 300
blocks = [random.sample(range(nodes), 3) for _ in range(60_000)]   # 1/10 sample
order = random.sample(range(nodes), nodes)
reported = set()
for i, n in enumerate(order, 1):
    reported.add(n)
    safe = sum(1 for b in blocks if reported.intersection(b))
    if safe >= int(len(blocks) * 0.999):
        print("threshold reached after", i, "of", nodes, "DataNodes")
        break
''', explain='The threshold was reached after 270 of 300 DataNodes: about 30 nodes (10%) could still be missing, because each block needs only one of its three replicas reported. Replication also shortens safe mode.'),
    dict(level='medium', title='Manual or automatic?', stmt='For each situation, say whether safe mode will end by itself.', inp='restart · enter · disk low',
         code='''cases = {"after restart": True, "after -safemode enter": False, "metadata disk low": False}
for c, auto in cases.items():
    print(f"{c:22} -> {'ends by itself' if auto else 'needs -safemode leave'}")
''', explain='Only start-up safe mode ends automatically; manual and resource-low safe mode need an admin.'),
    dict(level='business', title='Cost of read-only minutes', stmt='Nightly pipelines restart the NameNode for patching. Safe mode lasts 12 minutes, blocking 40 ingestion jobs that each queue Rs 300 of SLA penalty per minute late after a 5-minute grace. What is the penalty, and what if checkpoints cut it to 4 minutes?', inp='12 vs 4 min · 40 jobs · Rs 300/min after 5 min',
         code='''for minutes in [12, 4]:
    late = max(0, minutes - 5)
    print(f"{minutes:>2} min safe mode -> Rs {late * 300 * 40:,}")
''', explain='Rs 84,000 for 12 minutes, nothing for 4. Fast restarts (checkpoints, quick block reports) have real money value.'),
    dict(level='advanced', title='Find missing blocks after leaving', stmt='Given the block → reported DataNodes map after leaving safe mode, list files with missing blocks.', inp='file → blocks · reported replicas',
         code='''files = {"orders.csv": ["b1", "b2"], "scratch_r1.csv": ["b9"], "users.csv": ["b5"]}
reported = {"b1": ["dn2"], "b2": ["dn3", "dn4"], "b5": ["dn2", "dn4"], "b9": []}
for f, blocks in files.items():
    missing = [b for b in blocks if not reported.get(b)]
    print(f, "MISSING " + ", ".join(missing) if missing else "ok")
''', explain='Only scratch_r1.csv (its one replica was on the stopped DataNode), exactly as the real fsck reported.'),
]

SCN_INTRO = 'Safe mode questions check both knowledge and judgement: do you force it, or do you find out why?'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · basics</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“My job fails with ‘Name node is in safe mode’ right after starting HDFS”</h4>
      <p class="scn__situation">A student's script runs start-dfs.sh and immediately hdfs dfs -put.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> what safe mode is and the right fix.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>At start-up the NameNode stays read-only until DataNodes report 99.9% of blocks, plus 30 s.</li>
          <li>Add <code>hdfs dfsadmin -safemode wait</code> after starting HDFS, before any write.</li>
          <li>Don't add <code>-safemode leave</code> to the script: it would hide real problems.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · incident</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Production NameNode stuck in safe mode at 96%</h4>
      <p class="scn__situation">After a data-centre power cut, the NameNode reports 96% of blocks after 30 minutes. Users want you to force it out.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> calm, systematic recovery.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>4% unreported blocks means many DataNodes or disks are missing. Compare expected vs registered DataNodes (<code>dfsadmin -report</code>, UI).</li>
          <li>Check those hosts: powered on? DataNode running? Disks mounted? Logs for clusterID or volume errors.</li>
          <li>As nodes return, the count rises and safe mode ends by itself. Force it off only if the missing nodes are confirmed lost, then run fsck and restore data from backups/DR.</li>
          <li>Communicate: the cluster is readable for reported data meanwhile.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · internals</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Why doesn't the NameNode just start re-replicating straight away?</h4>
      <p class="scn__situation">A design question about the purpose of safe mode.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> understanding of the block map.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Right after start-up the block map is empty: every block looks like it has 0 replicas.</li>
          <li>Acting on that would trigger copies of the whole cluster, followed by mass deletion when reports arrive.</li>
          <li>Safe mode waits until the map is nearly complete, so replication decisions are based on real data.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · maintenance</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>When would you put HDFS into safe mode on purpose?</h4>
      <p class="scn__situation">An interviewer asks for real uses of <code>-safemode enter</code>.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> practical admin experience.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Before <code>hdfs dfsadmin -saveNamespace</code> (required), e.g. to create a clean checkpoint before maintenance.</li>
          <li>To freeze the namespace while taking a metadata backup or before an upgrade.</li>
          <li>Remember to run <code>-safemode leave</code> afterwards: manual safe mode never ends by itself.</li>
        </ul>
      </div></details>
    </article>
'''
