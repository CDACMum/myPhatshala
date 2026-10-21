import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Silence means dead',
    intro='<p>Each DataNode shows the time since its last heartbeat (♥). Stop one and watch the counter grow until the NameNode gives up on it.</p>',
    racks=2, nodes=3, features=['fail', 'fsck'],
    preload=[dict(name='irctc_bookings.log', sizeMB=640)],
    **{'try': [
        dict(text='Watch the pink heartbeat dots, then click a DataNode to stop it: its “♥ … ago” counter keeps growing.', on='node-stop'),
        dict(text='Press <b>Skip to timeout</b>: the node becomes DEAD at 10 min 30 s.', on='node-dead'),
        dict(text='Wait for re-replication in the Event log: the NameNode sends copy commands in heartbeat replies.', on='rereplicated'),
        dict(text='Start the node again by clicking it: it re-joins.', on='node-start'),
    ]},
)))

META = dict(
    module='05-hdfs-architecture', lesson='05-heartbeats-and-block-reports', n='5.5',
    module_label='Module 5 · HDFS architecture',
    title='Heartbeats and block reports',
    desc='How the NameNode knows which DataNodes are alive and what they store: heartbeats every 3 s with commands in the reply, stale (30 s) and dead (10 min 30 s) nodes, full block reports every 6 hours and incremental reports. Real Hadoop 3.5.0 timeline of a frozen DataNode going live → stale → dead → re-registered, last-contact readings from /jmx, triggerBlockReport, Python state machine, quiz and interview scenarios.',
    og_desc='“Present!” every 3 seconds. Watch a frozen DataNode go stale, then dead, then come back, on a real cluster.',
    minutes=24, level='Intermediate',
    lead='The NameNode never polls its DataNodes. It learns everything from two messages they send: a heartbeat every three seconds and block reports listing what they store. This lesson shows both on a real cluster: a DataNode frozen on purpose, the NameNode\'s view of it changing from live to stale to dead, and the re-registration and block report when it returns.',
    chips=['Real failure timeline', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='The NameNode\'s view of a DataNode',
    intro='<p>This function classifies a DataNode from the seconds since its last heartbeat, using the real default thresholds. Run it for the readings from the lab, then try the challenges.</p>',
    code='''HEARTBEAT = 3            # dfs.heartbeat.interval (s)
STALE = 30               # dfs.namenode.stale.datanode.interval (s)
RECHECK = 300            # dfs.namenode.heartbeat.recheck-interval (s)
DEAD = 2 * RECHECK + 10 * HEARTBEAT

def state(last_contact):
    if last_contact >= DEAD:
        return "DEAD"
    if last_contact >= STALE:
        return "STALE"
    return "LIVE"

print("dead after", DEAD, "seconds")
for seconds in [2, 27, 43, 300, 629, 630, 900]:
    print(f"last contact {seconds:>3}s -> {state(seconds)}")
''',
    anno=[
        ('DEAD = 2 * RECHECK + 10 * HEARTBEAT', 'The famous 10 min 30 s: 2 × 300 s + 10 × 3 s = 630 s.'),
        ('if last_contact >= STALE:', 'Stale nodes are still live; they can be avoided for reads and writes if the avoid-stale options are on.'),
    ],
    tasks=[
        dict(label='1 · Classify readings', hint='Press <b>Run</b>. Then set <code>RECHECK = 15</code> (our lab) and check that 51 s is still live but 60 s is dead.', code=None),
        dict(label='2 · Heartbeats per day', hint='<b>Predict first:</b> how many heartbeats does one DataNode send per day? And a 1,000-node cluster per second?',
             code='''per_day = 24 * 3600 // 3
print("one DataNode:", f"{per_day:,}", "heartbeats/day")
print("1000 nodes:", 1000 // 3, "heartbeats per second at the NameNode")
'''),
        dict(label='3 · Block report schedule', hint='A DataNode registered at 06:49:03. With a 6-hour interval, when are its next three full reports due?',
             code='''from datetime import datetime, timedelta
start = datetime(2026, 10, 21, 6, 49, 3)
for i in range(1, 4):
    print("report", i, (start + timedelta(hours=6 * i)).strftime("%d %b %H:%M:%S"))
'''),
        dict(label='4 · Missed heartbeats', hint='How many heartbeats has a node missed when it is declared dead with the default settings?',
             code='''dead_after = 2 * 300 + 10 * 3
print(dead_after // 3, "missed heartbeats")
'''),
        dict(label='5 · Spot the error', hint='This check marks a node dead as soon as it is stale. Fix the order of the conditions.',
             code='''def state(t, stale=30, dead=630):
    if t >= stale:
        return "STALE"
    if t >= dead:
        return "DEAD"
    return "LIVE"
print(state(700))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: watch a DataNode die and come back',
    intro='<p>This script freezes datanode-4 with <code>docker pause</code> (no heartbeats, but the process stays), asks the NameNode about it every 8 seconds for 80 seconds, then unfreezes it. Save it as <code>heartbeat_watch.py</code> in the <code>hdfs-lab</code> folder and run it while the lab cluster is up.</p>',
    items=[
        dict(title='Live → dead → live, from the NameNode\'s side', file='heartbeat_watch.py',
             cmd=open(os.path.join(HERE, 'heartbeat_watch.py')).read() + '\n# In the hdfs-lab folder:\n#   python3 heartbeat_watch.py',
             output='''t=  8s  NameNode says: live  lastContact=10s
t= 16s  NameNode says: live  lastContact=19s
t= 25s  NameNode says: live  lastContact=27s
t= 33s  NameNode says: live  lastContact=35s
t= 41s  NameNode says: live  lastContact=43s
t= 49s  NameNode says: live  lastContact=51s
t= 57s  NameNode says: dead  lastContact=60s
t= 65s  NameNode says: dead  lastContact=68s
t= 74s  NameNode says: dead  lastContact=76s
t= 82s  NameNode says: dead  lastContact=84s
after unpause: ('live', 0)''',
             note='Real output with the lab\'s 15 s recheck interval. With default settings the same script would need to run for more than 10 minutes to see “dead”. The block re-replication this triggers is covered in Lesson 5.3.'),
    ],
)

TRACE = dict(
    heading='Rebuilding a block map from reports',
    intro='<p>Follow the NameNode as two full block reports and one incremental report arrive. Watch the block map grow and change.</p>',
    code='''block_map = {}
reports = [("full", "dn1", ["b1", "b2"]),
           ("full", "dn2", ["b1", "b3"]),
           ("incremental", "dn2", ["+b2", "-b3"])]
for kind, dn, items in reports:
    for item in items:
        blk = item.lstrip("+-")
        if item.startswith("-"):
            block_map[blk].remove(dn)
        else:
            block_map.setdefault(blk, []).append(dn)
print(block_map)
''',
    notes={5: 'Report :: Full reports list everything; incremental ones only changes.',
           8: 'Deleted :: A replica the DataNode removed is dropped from the map.',
           10: 'Added :: A replica the DataNode now holds is recorded.'},
)

WORKED_INTRO = 'Three calculations about heartbeats and reports that platform teams make: NameNode load, timer trade-offs, and the cost of a false death. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Load · NameNode', title='How many messages does the NameNode handle?',
         problem='<p>A cluster has 600 DataNodes. Each sends a heartbeat every 3 s and a full block report every 6 hours, and on average 2 incremental reports per second while jobs run. How many messages per second reach the NameNode from DataNodes?</p>',
         inp='600 nodes · heartbeat 3 s · full report 6 h · 2 incremental/s per node',
         approach=['Heartbeats/s = nodes / 3.',
                   'Full reports/s = nodes / (6 × 3600).',
                   'Incremental/s = nodes × 2. Add them up.'],
         code='''nodes = 600
hb = nodes / 3
full = nodes / (6 * 3600)
inc = nodes * 2
print(f"heartbeats {hb:.0f}/s, full reports {full:.3f}/s, incremental {inc:.0f}/s")
print(f"total ~{hb + full + inc:.0f} messages per second")
''', notes={4: 'Incremental :: Busy clusters send far more small block updates than heartbeats.'},
         tryit='Full reports are rare but huge (one entry per replica); incremental reports are frequent but tiny. Both matter for NameNode sizing.'),
    dict(level='i', tag='Tuning · trade-off', title='Faster detection vs false alarms',
         problem='<p>A team wants faster dead-node detection. With recheck intervals of 300, 120 and 30 s, compute the dead time. Then, if the cluster sees GC pauses up to 90 s about once a week per node across 500 nodes, which settings would declare healthy nodes dead?</p>',
         inp='recheck 300 / 120 / 30 s · heartbeat 3 s · GC pauses ≤ 90 s',
         approach=['Dead time = 2 × recheck + 10 × 3.',
                   'A pause longer than the dead time causes a false death.',
                   'Count false deaths per week.'],
         code='''pause, nodes = 90, 500
for recheck in [300, 120, 30]:
    dead = 2 * recheck + 30
    false = nodes if pause >= dead else 0
    print(f"recheck {recheck:>3}s: dead after {dead:>3}s, false deaths/week ~{false}")
''', notes={4: 'Compare :: With recheck 30 s the dead time is exactly 90 s, so a 90 s pause is enough to kill the node.'},
         tryit='Each false death triggers re-replication of terabytes. That is why defaults are conservative and stale-node avoidance is used for faster reaction instead.'),
    dict(level='a', tag='Operations · re-registration', title='How long until a returning node\'s data counts again?',
         problem='<p>A DataNode with 12 lakh replicas comes back after a network outage. It re-registers on its next heartbeat, then sends a full block report that the NameNode processes at 4 lakh replicas per second. How long until all its replicas are back in the block map?</p>',
         inp='12,00,000 replicas · heartbeat 3 s · 4,00,000 replicas/s',
         approach=['Worst-case wait for the next heartbeat: 3 s.',
                   'Processing time = replicas / rate.',
                   'Add them.'],
         code='''replicas, rate, hb = 12_00_000, 4_00_000, 3
print(f"about {hb + replicas / rate:.0f} seconds")
''', notes={2: 'Report :: Block reports are processed in batches by the NameNode.'},
         tryit='In our lab the node had 8 blocks, so it was “live, lastContact 0” within 6 seconds of unpausing.'),
]

QUIZ = mix([
    dict(q='How often does a DataNode send a heartbeat by default?', options=['Every 3 seconds', 'Every 30 seconds', 'Every 6 hours', 'Only at start-up'], answer=0,
         why='dfs.heartbeat.interval = 3 s.'),
    dict(q='How does the NameNode send commands (like “copy this block”) to a DataNode?', options=['It opens a connection to the DataNode', 'In the reply to the DataNode\'s heartbeat', 'By email', 'Through YARN'], answer=1,
         why='The NameNode never initiates calls; commands ride on heartbeat replies.'),
    dict(q='With default settings, when is a silent DataNode declared dead?', options=['3 s', '30 s', '10 min 30 s', '6 hours'], answer=2,
         why='2 × 5 min + 10 × 3 s. After 30 s it is only “stale”.'),
    dict(q='What is in a full block report?', options=['File names and owners', 'Every block replica the DataNode stores (ID, length, generation stamp)', 'The DataNode\'s CPU usage', 'Heartbeat timestamps'], answer=1,
         why='File names live in the NameNode namespace; DataNodes only know blocks.'),
    dict(q='How often are full block reports sent by default?', options=['Every 3 s', 'Every hour', 'Every 6 hours (plus at start-up)', 'Once a week'], answer=2,
         why='dfs.blockreport.intervalMsec = 21,600,000 ms; incremental reports fill the gaps.'),
    dict(q='A paused (frozen) DataNode process, from the NameNode\'s point of view, is:', options=['Healthy, because the process exists', 'The same as a stopped one: no heartbeats, so eventually dead', 'Decommissioned', 'In safe mode'], answer=1,
         why='We saw it go dead at about 60 s with lab settings.'),
    dict(q='What does hdfs dfsadmin -triggerBlockReport host:9867 do?', options=['Restarts the DataNode', 'Makes that DataNode send a full block report now', 'Deletes old blocks', 'Formats the DataNode'], answer=1,
         why='The “Last Block Report” time changed from 06:49:03 to 06:59:19.'),
    dict(q='Why not set the dead-node timeout to 10 seconds?', options=['It is not allowed', 'Short pauses (GC, network blips) would cause false deaths and huge re-replication', 'It uses more disk', 'DataNodes would stop'], answer=1,
         why='Conservative timers avoid expensive false alarms.'),
])

REVISION = [
    '<b>Heartbeat</b>: DataNode → NameNode every <b>3 s</b>: alive + capacity/load. Reply carries <b>commands</b>.',
    'The NameNode never calls DataNodes; it only measures silence.',
    '<b>Stale</b> after 30 s; <b>dead</b> after 2 × recheck (5 min) + 10 × 3 s = <b>10 min 30 s</b>.',
    '<b>Full block report</b>: all replicas, at registration and every <b>6 h</b>. <b>Incremental</b>: changes in between.',
    'Block reports build the block map (not saved in the fsimage).',
    'Commands: transfer (replicate), invalidate (delete), recover, re-register.',
    'Check: “Last contact”, “Last Block Report” in <code>dfsadmin -report</code>; <code>/jmx</code> LiveNodes/DeadNodes.',
    '<code>hdfs dfsadmin -triggerBlockReport host:9867</code> forces a report.',
]
FAQ = [
    ('What is a heartbeat in Hadoop?', 'A small periodic message (every 3 seconds by default) from each DataNode to the NameNode saying it is alive, with its storage capacity, usage and load. The NameNode uses the reply to send the DataNode commands.'),
    ('What happens if the NameNode stops receiving heartbeats from a DataNode?', 'After 30 seconds the node is marked stale; after 10 minutes 30 seconds (default) it is marked dead. Its replicas are then removed from the block map and the affected blocks are re-replicated from other copies.'),
    ('What is a block report?', 'A list of all the block replicas stored on a DataNode, sent when it registers and then every 6 hours by default. Incremental block reports announce new and deleted replicas in between. The NameNode uses them to know where each block is.'),
    ('Why does a DataNode need to send block reports if the NameNode chose where blocks go?', 'Because reality can differ: disks fail, files are corrupted or deleted, nodes return with old replicas, and block locations are not stored in the fsimage. Reports are the source of truth for which replicas exist.'),
    ('How is the dead-node timeout calculated?', '2 × dfs.namenode.heartbeat.recheck-interval + 10 × dfs.heartbeat.interval. With defaults: 2 × 300 s + 10 × 3 s = 630 s.'),
    ('Can the NameNode contact a DataNode directly?', 'No. In the DataNode protocol the DataNode always initiates the RPC (heartbeats, reports); the NameNode responds, putting any commands in its replies.'),
]

PRACTICE_INTRO = 'Timer and report exercises using the real readings from the lab cluster.'
PROBLEMS = [
    dict(level='easy', title='Lab dead time', stmt='Compute the dead-node time for the lab (recheck 15 s, heartbeat 3 s).', inp='15 s · 3 s',
         code='print(2 * 15 + 10 * 3, "s")\n', explain='60 s, matching the real timeline (live at 51 s, dead at 57–60 s).'),
    dict(level='easy', title='Milliseconds to hours', stmt='Convert dfs.blockreport.intervalMsec = 21600000 to hours.', inp='21,600,000 ms',
         code='print(21600000 / 1000 / 3600, "hours")\n', explain='6.0 hours.'),
    dict(level='easy', title='Stale or not', stmt='With a 30 s stale interval, classify last-contact readings 27, 35 and 51 s.', inp='27 · 35 · 51',
         code='''for s in [27, 35, 51]:
    print(s, "stale" if s >= 30 else "fresh")
''', explain='27 s fresh; 35 and 51 s stale (but still live until the dead limit).'),
    dict(level='medium', title='Parse the JMX reading', stmt='From the real JMX line "729c51a07ee2:9866 lastContact=51s blocks=8", extract the host and the seconds.', inp='729c51a07ee2:9866 lastContact=51s blocks=8',
         code='''line = "729c51a07ee2:9866 lastContact=51s blocks=8"
host = line.split(":")[0]
seconds = int(line.split("lastContact=")[1].split("s")[0])
print(host, seconds)
''', explain='Host 729c51a07ee2 (datanode-4), 51 seconds since its last heartbeat.'),
    dict(level='medium', title='Apply an incremental report', stmt='Apply the incremental report +b4, -b1 from dn3 to the block map.', inp='b1:[dn1,dn3] · b4:[dn2]',
         code='''bm = {"b1": ["dn1", "dn3"], "b4": ["dn2"]}
for item in ["+b4", "-b1"]:
    blk = item[1:]
    if item[0] == "+":
        bm.setdefault(blk, []).append("dn3")
    else:
        bm[blk].remove("dn3")
print(bm)
''', explain='b1 keeps only dn1, b4 gains dn3. Incremental reports keep the map current between full reports.'),
    dict(level='medium', title='Heartbeat load', stmt='How many heartbeats per second does a NameNode receive from 3,000 DataNodes?', inp='3000 nodes · 3 s',
         code='print(3000 / 3, "per second")\n', explain='1,000 heartbeats per second, each answered, which is why heartbeat handling must be cheap.'),
    dict(level='business', title='False death cost', stmt='A false dead-node event re-replicates 20 TB at 4 GB/s cluster-wide and slows jobs by 20% during copying. How long are jobs slowed?', inp='20 TB · 4 GB/s',
         code='''seconds = 20 * 1024 / 4
print(f"{seconds / 60:.0f} minutes of slower jobs")
''', explain='About 85 minutes of degraded performance for nothing, if the node comes back right after. Hence conservative timeouts.'),
    dict(level='advanced', title='Timeline classifier', stmt='Given (t, lastContact) samples, print the first time the node becomes stale and dead, for stale 30 s and dead 60 s.', inp='real lab samples',
         code='''samples = [(8, 10), (16, 19), (25, 27), (33, 35), (41, 43), (49, 51), (57, 60), (65, 68)]
stale = next(t for t, lc in samples if lc >= 30)
dead = next(t for t, lc in samples if lc >= 60)
print("stale first seen at t =", stale, "s; dead first seen at t =", dead, "s")
''', explain='Stale at t = 33 s (last contact 35 s) and dead at t = 57 s (60 s), consistent with the thresholds and the real readings.'),
]

SCN_INTRO = 'Heartbeat questions check whether you understand how the NameNode can manage thousands of nodes cheaply.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“How does the NameNode know a DataNode has failed?”</h4>
      <p class="scn__situation">Asked in almost every HDFS interview.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> heartbeats, timeouts and consequences.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>DataNodes send heartbeats every 3 s. The NameNode tracks time since the last one.</li>
          <li>After 30 s the node is stale; after 10 min 30 s (2 × recheck + 10 heartbeats) it is declared dead.</li>
          <li>Then its replicas are removed from the block map, and under-replicated blocks are copied from surviving replicas, with commands sent in other DataNodes' heartbeat replies.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · flapping</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A DataNode keeps going dead and coming back</h4>
      <p class="scn__situation">The NameNode UI shows one node dead several times a day, each time followed by re-replication and then excess deletions.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> systematic debugging.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Correlate dead times with the DataNode's GC log (long pauses), kernel/disk logs (hung I/O), and network errors.</li>
          <li>Common fixes: right-size the DataNode heap and GC settings, replace the failing disk, fix the NIC/switch port.</li>
          <li>Meanwhile, consider decommissioning the node so it stops causing re-replication storms.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · protocol</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Why do DataNodes call the NameNode, not the other way round?</h4>
      <p class="scn__situation">A system design follow-up question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> scalability reasoning.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>With thousands of DataNodes, the NameNode would need many outgoing connections and timeouts to poll them; instead each node pushes a tiny message on a schedule.</li>
          <li>Failure detection becomes trivial: silence. No connection management for dead nodes.</li>
          <li>Commands piggyback on replies, so there is no extra round trip.</li>
          <li>The same push model is used by YARN NodeManagers to the ResourceManager.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · repair</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>After replacing a disk, the NameNode still shows old block counts</h4>
      <p class="scn__situation">A disk on a DataNode was replaced and its data restored from another copy, but the NameNode's numbers look out of date.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> block report timing.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The next full block report may be hours away (every 6 h).</li>
          <li>Run <code>hdfs dfsadmin -triggerBlockReport host:9867</code>, then check “Last Block Report” and the block counts in <code>dfsadmin -report</code>.</li>
          <li>Verify with <code>hdfs fsck /</code> that no blocks are missing or corrupt.</li>
        </ul>
      </div></details>
    </article>
'''
