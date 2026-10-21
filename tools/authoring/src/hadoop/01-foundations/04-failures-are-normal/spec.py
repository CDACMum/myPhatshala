import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='How much can you break?',
    intro='<p>A 1 GB file is stored with 3 replicas on 2 racks. Click nodes to stop them, use <b>⏩ Skip to timeout</b> to jump past the 10.5-minute wait, and run <b>hdfs fsck /</b> to check the file system.</p>',
    racks=2, nodes=3, features=['fail', 'chaos', 'fsck', 'job'],
    preload=[dict(name='irctc_bookings.log', sizeMB=1024)],
    **{'try': [
        dict(text='Stop one DataNode, then skip to the timeout. Watch the green “copy” packets re-replicate its blocks.', on='rereplicated'),
        dict(text='Press <b>Reset</b>. Now stop <b>all three nodes of rack 1</b>, skip to the timeout and run <b>hdfs fsck /</b>. Under-replicated, yes, but is any block missing? (Rack awareness at work.)', on='fsck'),
        dict(text='Press <b>Reset</b> again. Quickly stop all of rack 1 <b>and</b> one node of rack 2, then skip to the timeout. Now some blocks are <b>MISSING</b>.', on='block-missing'),
        dict(text='With a block missing, run the job. It fails with <code>BlockMissingException</code>. Start a node again to bring the data back.', on='job-failed'),
    ]},
)))

META = dict(
    module='01-foundations', lesson='04-failures-are-normal', n='1.4',
    module_label='Module 1 · Foundations: before Hadoop',
    title='Failures are normal',
    desc='Why failures are expected in big clusters, the arithmetic of disk and node failure rates, every kind of failure (disk, node, rack, corruption, stragglers, masters, human error) and how Hadoop survives each one: replication, heartbeats, re-replication, checksums, retries and HA. With animations, a break-it-yourself playground, a Monte Carlo simulation, quiz and interview scenarios.',
    og_desc='With 10,000 disks, something breaks every day. See how Hadoop makes failures not matter, then break a cluster yourself.',
    minutes=26, level='Beginner → Advanced',
    lead='On your laptop a dead disk is a disaster. In a cluster of thousands of disks it is a normal Tuesday. This lesson does the arithmetic of how often hardware fails at scale, walks through every kind of failure a Hadoop cluster meets, and shows the mechanisms that make them harmless: three copies on two racks, heartbeats, automatic re-replication, checksums and task retries. Then you get to break the playground cluster on purpose.',
    chips=['Break-it playground', 'Runs in your browser (Python)', 'Data-loss simulation'],
)

RUN = dict(
    heading='The arithmetic of failure',
    intro='<p>How many failures should a cluster expect? Multiply the number of devices by the yearly failure rate. Run it, then try the challenges, including the chance that every copy of a block is lost.</p>',
    code='''afr = {"disk": 0.015, "node": 0.04, "rack switch": 0.02}
count = {"disk": 3000, "node": 250, "rack switch": 10}

for part in afr:
    per_year = count[part] * afr[part]
    print(f"{part:12}: {per_year:5.1f} failures a year "
          f"(one every {365 / per_year:.0f} days)")
''',
    anno=[
        ('afr = {"disk": 0.015, ...}', 'Annualised failure rates (illustrative): 1.5% of disks, 4% of whole nodes, 2% of rack switches fail in a year.'),
        ('per_year = count[part] * afr[part]', 'Expected failures = devices × rate. 3,000 × 0.015 = 45.'),
        ('365 / per_year', 'The average gap between failures in days.'),
    ],
    tasks=[
        dict(label='1 · Failures per year', hint='Press <b>Run</b>. Then make the cluster 10 times bigger. How often does a disk fail now?', code=None),
        dict(label='2 · At least one today', hint='<b>Predict first:</b> with 10,000 disks, is the chance that at least one fails <i>today</i> closer to 4%, 34% or 98%?',
             code='''p_day = 0.015 / 365          # one disk failing on a given day
for n in [100, 1000, 10000]:
    p_any = 1 - (1 - p_day) ** n
    print(f"{n:>6} disks: {p_any:.0%} chance of at least one failure today")
'''),
        dict(label='3 · All copies lost?', hint='Chance that all copies of one block are on nodes that are down at the same moment, if 0.1% of nodes are down at any time. Compare 1, 2 and 3 copies.',
             code='''down = 0.001           # 0.1% of nodes are down at any moment
for copies in [1, 2, 3]:
    p = down ** copies
    print(f"{copies} copies: 1 in {1 / p:,.0f}")
'''),
        dict(label='4 · Retries', hint='A task fails 10% of the time because of a bad node. Hadoop tries up to 4 times. What is the chance the task finally fails? Try a 30% failure rate.',
             code='''p_fail = 0.10
for attempts in [1, 2, 3, 4]:
    print(attempts, "attempt(s): job fails with probability", f"{p_fail ** attempts:.4%}")
'''),
        dict(label='5 · Is any block on one rack only?', hint='This checks a placement for blocks whose copies are all on the same rack. Move one copy of B3 to rack r2 and run again.',
             code='''rack_of = {"dn1": "r1", "dn2": "r1", "dn3": "r1", "dn4": "r2", "dn5": "r2"}
blocks = {"B1": ["dn1", "dn4", "dn5"], "B2": ["dn2", "dn4", "dn1"], "B3": ["dn1", "dn2", "dn3"]}

for b, nodes in blocks.items():
    racks = {rack_of[n] for n in nodes}
    status = "OK" if len(racks) >= 2 else "DANGER: one rack only"
    print(b, sorted(racks), status)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: five years of failures, simulated',
    intro='<p>This Monte Carlo simulation places 20,000 blocks on 200 nodes with 1, 2 or 3 copies, then lets nodes fail at random for five simulated years. A failed node is repaired within a day. Each “block-loss event” is a day on which every copy of some block was on a dead node. Save it as <code>loss_sim.py</code> and run it.</p>',
    items=[
        dict(title='Why HDFS keeps three copies', file='loss_sim.py',
             cmd=open(os.path.join(HERE, 'loss_sim.py')).read() + '\n# In a terminal:  python loss_sim.py',
             output='''1 copy:   4850 block-loss events in 5 years
2 copies:      4 block-loss events in 5 years
3 copies:      0 block-loss events in 5 years''',
             note='Recorded with <code>random.seed(42)</code>, so you will get the same numbers. Change the seed or the failure rate and run again: one copy always loses data, two copies sometimes do, three almost never. This model is simplified (it ignores racks and whole-rack failures), which is exactly why real HDFS also spreads copies over racks.'),
    ],
)

TRACE = dict(
    heading='Re-replication planning, one line at a time',
    intro='<p>A node has died. Watch the NameNode-style loop count the surviving copies of each block and decide how many new copies to make.</p>',
    code='''target = 3
replicas = {"B1": ["dn1", "dn4", "dn5"], "B2": ["dn2", "dn4", "dn6"], "B3": ["dn2", "dn3", "dn5"]}
dead = "dn2"

to_copy = {}
for block, nodes in replicas.items():
    alive = [n for n in nodes if n != dead]
    if len(alive) < target:
        to_copy[block] = target - len(alive)
print("New copies needed:", to_copy)
''',
    notes={3: 'Failure :: dn2 has just been declared dead.', (7, 2): 'B2 :: One of its three replicas was on dn2.'},
)

WORKED_INTRO = 'Three questions a platform team answers about failures: how often, how long to recover, and whether the placement is safe. Each solution runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Operations · planning', title='How many disk swaps per month?',
         problem='<p>A cluster has <b>80 nodes</b> with <b>12 disks</b> each. About <b>1.5%</b> of disks fail per year. How many disk replacements should the ops team plan for each month, and how many spare disks should they keep for a quarter?</p>',
         inp='80 × 12 disks · AFR 1.5%',
         approach=['Total disks = nodes × disks per node.',
                   'Failures per year = disks × 0.015. Divide by 12 for a month.',
                   'Spares for a quarter = 3 months, rounded up, plus one for luck.'],
         code='''import math
disks = 80 * 12
per_year = disks * 0.015
per_month = per_year / 12
spares = math.ceil(per_month * 3) + 1
print("Disks:", disks)
print(f"Failures per month: {per_month:.1f}")
print("Spare disks for a quarter:", spares)
''', notes={3: 'Rate :: 960 × 0.015 = 14.4 disk failures a year.'},
         tryit='The disks are 5 years old and the failure rate has risen to 4%. How many spares now?'),
    dict(level='i', tag='Reliability · recovery time', title='How long is the cluster “at risk” after a node dies?',
         problem='<p>A node with <b>100 TB</b> of replicas dies. Re-replication can use <b>30 nodes</b> copying at <b>60 MB/s</b> each. Until it finishes, some blocks have only 2 copies. How many hours is that window, with and without waiting for the 10.5-minute timeout?</p>',
         inp='100 TB · 30 nodes × 60 MB/s · timeout 630 s',
         approach=['Copy time = data ÷ total copy speed.',
                   'Add the detection timeout before copying starts.',
                   'Print both in hours.'],
         code='''tb, nodes, mb_s = 100, 30, 60
timeout_s = 630

copy_s = tb * 1024 * 1024 / (nodes * mb_s)
print(f"Copying       : {copy_s / 3600:.1f} hours")
print(f"With detection: {(copy_s + timeout_s) / 3600:.1f} hours")
''', notes={4: 'Copy :: 1,04,85,760 MB over 1,800 MB/s in total.'},
         tryit='Double the nodes doing the copying. The window halves. This is one reason bigger clusters recover faster.'),
    dict(level='a', tag='Data safety · audit', title='Which blocks would a rack failure destroy?',
         problem='<p>An auditor wants to know: if any <b>one rack</b> fails, which blocks lose <b>every</b> copy? Check each rack in turn against the block placement and print the blocks at risk.</p>',
         inp='racks r1 = {dn1, dn2, dn3}, r2 = {dn4, dn5} · B1 dn1 dn4 dn5 · B2 dn2 dn3 dn1 · B3 dn4 dn5 dn2',
         approach=['For each rack, take the set of its nodes.',
                   'A block is lost with that rack if <b>all</b> of its nodes are in the rack (set subset).',
                   'Print the blocks at risk for each rack.'],
         code='''racks = {"r1": {"dn1", "dn2", "dn3"}, "r2": {"dn4", "dn5"}}
blocks = {"B1": {"dn1", "dn4", "dn5"}, "B2": {"dn2", "dn3", "dn1"}, "B3": {"dn4", "dn5", "dn2"}}

for rack, nodes in racks.items():
    at_risk = [b for b, where in blocks.items() if where <= nodes]
    print("If", rack, "fails, lost:", at_risk)
''', notes={5: 'Subset :: <code>where &lt;= nodes</code> is True when every copy is inside that rack.'},
         tryit='B2 is in danger. This is exactly what happens without a rack-topology script. Move one copy of B2 to dn4 and check again.'),
]

QUIZ = mix([
    dict(q='A cluster has 2,000 disks with a 1.5% annual failure rate. About how many disk failures per year?', options=['About 3', 'About 15', 'About 30', 'About 300'], answer=2,
         why='2,000 × 0.015 = <b>30</b>, roughly one every 12 days.'),
    dict(q='Why does HDFS place replicas of a block on at least two racks?', options=['Racks are faster', 'A whole rack can fail together (power or switch), so copies must not all be in one rack', 'The NameNode requires it to start', 'To use more network'], answer=1,
         why='A rack is a <b>failure domain</b>. Spreading copies across racks means one rack failure never loses all copies.'),
    dict(q='How does HDFS detect silent data corruption on disk?', options=['It doesn\'t; disks report all errors', 'By storing checksums (CRC32C) for every 512 bytes and checking them on read and in a background scanner', 'By comparing file sizes', 'By asking the user'], answer=1,
         why='Checksums catch bytes that changed without an error. A corrupt replica is replaced from a good one.'),
    dict(q='A map task fails because its node ran out of memory. What does Hadoop do by default?', options=['Fails the whole job immediately', 'Retries the task, up to 4 attempts in total', 'Ignores the task', 'Restarts the cluster'], answer=1,
         why='Each task gets up to <b>4 attempts</b> by default (mapreduce.map.maxattempts / reduce.maxattempts), usually on other nodes.'),
    dict(q='An analyst accidentally deletes a folder. Does replication 3 protect the data?', options=['Yes, two copies remain', 'No: the delete applies to all replicas. Use trash, snapshots or backups.', 'Yes, the NameNode refuses deletes', 'Only on weekends'], answer=1,
         why='<b>Replication is not backup.</b> It protects against hardware failure, not against changes made by users or bugs.'),
    dict(q='What is a “straggler”?', options=['A node that is dead', 'A node or task that is alive but much slower than the others', 'A deleted block', 'A spare disk'], answer=1,
         why='Stragglers hold up jobs. Speculative execution starts a backup copy of the slow task elsewhere.'),
    dict(q='After a dead DataNode returns, some blocks have 4 copies. What happens?', options=['Nothing; more is better', 'The NameNode deletes the surplus replicas to get back to the replication factor', 'The file is corrupted', 'The node is formatted'], answer=1,
         why='Over-replicated blocks waste space, so the NameNode removes extra copies, choosing which ones to keep good rack spread.'),
    dict(q='Why are big clusters built from ordinary (commodity) hardware rather than very reliable servers?', options=['Ordinary servers never fail', 'Software handles failures with copies and retries, which is cheaper than making every machine nearly perfect', 'Reliable servers are illegal', 'Hadoop cannot run on good hardware'], answer=1,
         why='At scale, failures happen anyway. It is cheaper to tolerate them in software than to pay a high premium for every machine.'),
])

REVISION = [
    'At scale, <b>failure is the norm</b>: expected failures = devices × annual failure rate.',
    'Chance of ≥1 failure among n devices: 1 − (1 − p)<sup>n</sup>. Grows fast with n.',
    'HDFS: <b>3 replicas</b>, on at least <b>2 racks</b>. Lose a node → read another copy.',
    'Dead node (≈10.5 min) → <b>re-replication</b> from surviving copies, most endangered blocks first.',
    'Returned node → surplus replicas deleted.',
    '<b>Checksums</b> (CRC32C per 512 bytes) + background <b>block scanner</b> catch corruption.',
    'Tasks retried up to <b>4</b> times; <b>speculative execution</b> for stragglers.',
    '<b>NameNode HA</b> for master failure; a <b>DR cluster</b> for a whole site.',
    '<b>Replication is not backup</b>: use trash, snapshots and copies elsewhere.',
]
FAQ = [
    ('Why is “failure is the norm” in big data systems?', 'Because a cluster has thousands of disks, nodes, cables and switches. Even if each part rarely fails, the chance that some part fails on a given day is high: 3,000 disks at 1.5% a year is about 45 disk failures a year. Systems like HDFS are therefore designed to expect failures and recover automatically.'),
    ('How does HDFS achieve fault tolerance?', 'It splits files into blocks and stores each block on several DataNodes (3 by default) across at least two racks. DataNodes send heartbeats and block reports; when a node or disk is lost, the NameNode re-replicates under-replicated blocks from surviving copies. Checksums detect corrupt replicas. Clients reading data simply switch to another replica if one fails. The NameNode itself is protected by High Availability.'),
    ('What is the difference between replication and backup?', 'Replication keeps live copies of the current data to survive hardware failure. Every change, including a mistaken delete, is applied to all replicas. A backup is a separate, point-in-time copy (or a snapshot) that lets you go back to an earlier state after user errors, bugs or ransomware.'),
    ('How does MapReduce handle a failed task?', 'The ApplicationMaster notices the failure (error, lost container, or no progress within the timeout) and reschedules the task attempt, preferably on another node. By default a task is tried up to 4 times; if all attempts fail the job fails. Completed map outputs on a lost node are re-run because they were stored on that node\'s local disk.'),
    ('What is speculative execution?', 'When a task runs much slower than other tasks of the same job, the framework may launch a duplicate attempt on another node. Whichever attempt finishes first is used and the other is killed. It helps with stragglers caused by slow hardware, not with tasks that are slow because they have more data (skew).'),
]

PRACTICE_INTRO = 'Reliability calculations and checks, from simple counts to the audits real platform teams run.'
PROBLEMS = [
    dict(level='easy', title='Failures per week', stmt='A cluster has 5,000 disks with an annual failure rate of 2%. How many disk failures per week?', inp='5000 disks · 2%',
         code='print(round(5000 * 0.02 / 52, 1), "per week")\n', explain='100 failures a year ÷ 52 weeks ≈ 1.9 a week.'),
    dict(level='easy', title='MTBF across the cluster', stmt='Each node fails on average once every 25 years (MTBF). With 500 nodes, how many days between node failures, on average?', inp='MTBF 25 years · 500 nodes',
         code='print(round(25 * 365 / 500, 1), "days")\n', explain='500 nodes × (1/25) = 20 failures a year, one every 18.25 days.'),
    dict(level='easy', title='Copies left', stmt='A block has replicas on dn1, dn4, dn7. dn4 and dn7 die. How many copies are left, and is the block under-replicated?', inp='[dn1, dn4, dn7] · dead {dn4, dn7}',
         code='''replicas = ["dn1", "dn4", "dn7"]
dead = {"dn4", "dn7"}
left = [n for n in replicas if n not in dead]
print("Left:", left, "| under-replicated:", len(left) < 3)
''', explain='One copy left: the block is very endangered and goes to the front of the re-replication queue.'),
    dict(level='medium', title='Find missing and under-replicated blocks', stmt='Given block placements and the dead nodes, print each block\'s status: OK, UNDER (1–2 live copies) or MISSING (0).', inp='B1 [1,2,3] · B2 [2,4,5] · B3 [4,5,6] · dead {4, 5, 6}',
         code='''blocks = {"B1": [1, 2, 3], "B2": [2, 4, 5], "B3": [4, 5, 6]}
dead = {4, 5, 6}
for b, nodes in blocks.items():
    live = len([n for n in nodes if n not in dead])
    status = "OK" if live == 3 else "MISSING" if live == 0 else "UNDER"
    print(b, live, status)
''', explain='This is what <code>hdfs fsck</code> reports. B3 is missing: all its copies were on the three dead nodes, probably the same rack.'),
    dict(level='medium', title='Retry success rate', stmt='A flaky network makes 20% of task attempts fail. With up to 4 attempts, what share of tasks finally succeed?', inp='20% fail per attempt · 4 attempts',
         code='''p = 0.20
print(f"Succeed: {1 - p ** 4:.2%}")
''', explain='Fails only if all 4 attempts fail: 0.2⁴ = 0.16%. Retries turn an unreliable network into a reliable job.'),
    dict(level='medium', title='Checksum check', stmt='Use Python\'s <code>zlib.crc32</code> to compute a checksum of a data chunk, flip one character, and show that the checksum changes.', inp='b"order,city,amount"',
         code='''import zlib
good = b"order,city,amount"
bad = b"order,citx,amount"
print(zlib.crc32(good), zlib.crc32(bad), zlib.crc32(good) == zlib.crc32(bad))
''', explain='HDFS uses CRC32C (a close relative) for every 512 bytes. One changed byte gives a different checksum, so corruption is caught.'),
    dict(level='business', title='Cost of not having rack awareness', stmt='Without rack awareness, about 2% of blocks end up with all copies in one rack. A rack fails twice a year and holds 1/8 of the cluster. The cluster has 50 lakh blocks. How many blocks are expected to become unavailable each year?', inp='50,00,000 blocks · 2% single-rack · 1/8 per rack · 2 rack failures/year',
         code='''blocks = 50_00_000
single_rack = blocks * 0.02
per_rack = single_rack / 8
print("Blocks unavailable per year:", int(per_rack * 2))
''', explain='About 25,000 blocks a year become unreadable until the rack is fixed, each one possibly breaking a job or a dashboard. A topology script fixes this for free.'),
    dict(level='business', title='How much extra disk does safety cost?', stmt='The business stores 400 TB. Compare the raw disk needed with replication 2 and 3, and the extra cost at Rs 2,000 per TB of raw disk.', inp='400 TB · repl 2 vs 3 · Rs 2,000/TB',
         code='''data, price = 400, 2000
for r in [2, 3]:
    print(f"replication {r}: {data * r} TB raw, Rs {data * r * price / 1e5:.0f} lakh")
print(f"Extra for the 3rd copy: Rs {data * price / 1e5:.0f} lakh")
''', explain='The third copy costs Rs 8 lakh here (illustrative price), but it is what makes data loss practically impossible. Erasure coding (Module 7) cuts this for cold data.'),
]

SCN_INTRO = 'Failure situations interviewers love, because they reveal whether you understand how Hadoop actually behaves.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · incident</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>A DataNode died. Should we restart everything?</h4>
      <p class="scn__situation">At 11 pm the monitoring shows one DataNode down out of 60. A junior admin wants to restart the whole cluster “to be safe”. You are on call. What do you do?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you trust and understand HDFS's self-healing, and avoid making things worse?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li><b>Don't restart the cluster.</b> That would stop all jobs and put the NameNode in safe mode while it waits for block reports.</li>
          <li>Check <code>hdfs dfsadmin -report</code> and <code>hdfs fsck /</code>: expect under-replicated blocks but 0 missing.</li>
          <li>After the timeout, HDFS re-replicates automatically. Watch the under-replicated count fall.</li>
          <li>Find out why the node died (logs, hardware alerts), and fix or replace it during working hours.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> panicking, or manually copying blocks around.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Banking · data safety</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>“We have 3 replicas, so we don't need backups”</h4>
      <p class="scn__situation">In a design review for a bank's reporting cluster, a manager says backups are unnecessary because HDFS already stores everything three times.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know what replication protects against, and what it doesn't?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Replication protects against <b>hardware</b> failures: disks, nodes, a rack.</li>
          <li>It does <b>not</b> protect against a user deleting data, a buggy job overwriting it, ransomware, or losing the whole data centre: every change reaches all replicas.</li>
          <li>Use HDFS <b>trash</b> (deleted files kept for a while), <b>snapshots</b> of important directories, and regular copies to a <b>second cluster</b> or cloud storage (DistCp). Regulated industries usually require a DR site anyway.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> agreeing that replication equals backup.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · incident</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>fsck says “CORRUPT”: 12 missing blocks</h4>
      <p class="scn__situation">After a power problem in one row of racks, <code>hdfs fsck /</code> reports 12 missing blocks in yesterday's sales folder. Five nodes are still down.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you investigate missing blocks calmly, and do you know they may come back?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>Missing usually means “no live replica right now”, not “destroyed”. Bring the five nodes back: when they send block reports, the blocks often reappear.</li>
          <li>Use <code>hdfs fsck / -list-corruptfileblocks</code> and <code>-files -blocks -locations</code> to see which files and nodes are involved.</li>
          <li>If nodes are truly lost, restore the affected files from the source system, a snapshot or the DR copy, then delete the broken files.</li>
          <li>Afterwards, ask why all copies were in the failed racks: is rack awareness configured correctly?</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> running <code>fsck -delete</code> straight away. It removes the files before you know whether the blocks can come back.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Why not just buy servers that never fail?”</h4>
      <p class="scn__situation">The interviewer asks: “Wouldn't it be simpler to buy top-quality servers with RAID and dual everything, so failures don't happen?”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand the economics behind Hadoop's design?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No hardware never fails. With thousands of machines, even very reliable ones fail regularly.</li>
          <li>Highly reliable servers cost much more per TB and per core, and you still need a plan for when they fail.</li>
          <li>Hadoop's idea: use affordable commodity servers and make failures harmless in software (replicas, retries, re-replication). Adding capacity stays cheap.</li>
          <li>Spend extra on the few components that matter most: master nodes, network core, power.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> saying commodity hardware is “bad hardware”. It is ordinary, well-supported hardware without a premium for extra reliability.</p>
      </div></details>
    </article>'''
