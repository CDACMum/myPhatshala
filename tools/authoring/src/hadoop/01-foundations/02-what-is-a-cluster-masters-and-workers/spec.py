import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Masters, workers and a failure',
    intro='<p>The <b>NameNode</b> and <b>ResourceManager</b> at the top are the masters. Each DataNode is a worker. The two bars at the bottom of each node are its <b>containers</b>: places where one task can run. A 1 GB file (8 blocks) is already stored.</p>',
    racks=2, nodes=3, features=['job', 'fail'],
    preload=[dict(name='canteen_orders.csv', sizeMB=1024)],
    **{'try': [
        dict(text='Press <b>Run word count job</b>. The ResourceManager gives one map task (M1…M8) per block to the workers. Let it finish.', on='job-done'),
        dict(text='Run it again, and while the green bars are filling, <b>click a busy node</b> to stop it. Its tasks are re-run elsewhere (marked M′).', on='node-stop'),
        dict(text='Open the <b>Event log</b> and <b>Job runs</b> tabs. Compare the time of the two runs.'),
        dict(text='Press <b>⏩ Skip to timeout</b>: after 10 min 30 s of silence the NameNode declares the node dead.', on='node-dead'),
    ]},
)))

META = dict(
    module='01-foundations', lesson='02-what-is-a-cluster-masters-and-workers', n='1.2',
    module_label='Module 1 · Foundations: before Hadoop',
    title='What is a cluster? Masters and workers',
    desc='What a computer cluster is, the master–worker architecture, heartbeats and timeouts, how a master assigns tasks and recovers from a dead worker, and how Hadoop uses masters and workers in HDFS and YARN. With animations, a cluster playground, Python simulations, quiz and interview scenarios.',
    og_desc='A cluster is a team of computers. Meet the masters that coordinate, the workers that do the work, and the heartbeats between them.',
    minutes=25, level='Beginner → Intermediate',
    lead='A cluster is many computers acting as one. This lesson explains how: one or two masters keep track of everything, many workers store data and run tasks, and heartbeats every few seconds tell the master who is still alive. You will watch a worker die in the middle of a job and see the master quietly give its work to others, then do it yourself in the Cluster Playground.',
    chips=['Cluster Playground', 'Runs in your browser (Python)', 'Master and workers on your PC'],
)

RUN = dict(
    heading='A tiny master and its workers in Python',
    intro='<p>This program plays the master. It has a queue of tasks and three workers, and gives each free worker the next task, round after round, until the queue is empty. Then try the challenges, including a worker that dies.</p>',
    code='''from collections import deque

queue = deque(["T1", "T2", "T3", "T4", "T5", "T6", "T7"])
workers = ["W1", "W2", "W3"]
done = {w: [] for w in workers}

round_no = 0
while queue:
    round_no += 1
    for w in workers:
        if queue:
            done[w].append(queue.popleft())
    print("after round", round_no, "->", done)
''',
    anno=[
        ('queue = deque([...])', 'A <code>deque</code> (double-ended queue) gives the next item quickly with <code>popleft()</code>: first in, first out, like a real job queue.'),
        ('done = {w: [] for w in workers}', 'The master\'s table: for each worker, the list of tasks it has run.'),
        ('while queue:', 'Keep going while tasks are waiting. An empty deque counts as <code>False</code>.'),
    ],
    tasks=[
        dict(label='1 · Hand out tasks', hint='Press <b>Run</b>. Add a fourth worker <code>"W4"</code>. How many rounds now?', code=None),
        dict(label='2 · Who is dead?', hint='<b>Predict first:</b> with a timeout of 30 s, which workers are declared dead at time 100? Then change <code>timeout</code> to 10.',
             code='''last_heartbeat = {"W1": 98, "W2": 61, "W3": 95, "W4": 40}
now, timeout = 100, 30

for w, t in last_heartbeat.items():
    silent = now - t
    status = "DEAD" if silent > timeout else "alive"
    print(f"{w}: silent {silent:>2} s -> {status}")
'''),
        dict(label='3 · Re-run lost tasks', hint='W2 dies with two tasks. The master gives them to the other workers, one each, in turn. Try it with W1 dying instead.',
             code='''running = {"W1": ["T1"], "W2": ["T2", "T5"], "W3": ["T3"]}
dead = "W2"

lost = running.pop(dead)
alive = list(running)
for i, task in enumerate(lost):
    target = alive[i % len(alive)]
    running[target].append(task + "'")      # ' marks a second attempt
print("lost:", lost)
print("now :", running)
'''),
        dict(label='4 · Least-loaded first', hint='Real masters give a task to the worker with the most free room, not just the next one in line. Run it, then make W3 start with 3 tasks.',
             code='''load = {"W1": 2, "W2": 0, "W3": 1}      # tasks already running
for task in ["T7", "T8", "T9", "T10"]:
    w = min(load, key=load.get)         # worker with the fewest tasks
    load[w] += 1
    print(task, "->", w, load)
'''),
        dict(label='5 · Spot the error', hint='This “master” crashes when the queue runs out in the middle of a round. Find the line and protect it with <code>if queue:</code>.',
             expect='error',
             code='''from collections import deque
queue = deque(["T1", "T2", "T3", "T4"])
workers = ["W1", "W2", "W3"]
while queue:
    for w in workers:
        print(w, "gets", queue.popleft())
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a master with real worker processes',
    intro='<p>Your computer can be a tiny cluster too: one <b>master</b> process and one <b>worker</b> process per CPU core. Python\'s <code>ProcessPoolExecutor</code> keeps a task queue and gives tasks to whichever worker is free, exactly like a cluster master. Save this as <code>workers.py</code> and run it.</p>',
    items=[
        dict(title='Watch tasks go to different worker processes', file='workers.py',
             cmd=open(os.path.join(HERE, 'workers.py')).read() + '\n# In a terminal:  python workers.py',
             output='''Master PID 1726 starting 2 workers
  task 0 done by worker PID 1727
  task 1 done by worker PID 1728
  task 2 done by worker PID 1727
  task 3 done by worker PID 1728
  task 4 done by worker PID 1727
  task 5 done by worker PID 1728
  task 6 done by worker PID 1727
  task 7 done by worker PID 1728
Total evens: 8000000
Time: 0.6 s''',
             note='Recorded on a 2-core machine, so there are 2 workers. With 8 cores you\'ll see 8 different worker PIDs, and the order of finished tasks will change from run to run: whichever worker is free takes the next task. The <code>if __name__ == "__main__":</code> line matters on Windows: without it, each worker would start its own master.'),
    ],
)

TRACE = dict(
    heading='The master\'s timeout check, one line at a time',
    intro='<p>The master loops over its table of last heartbeats. Watch <code>silent</code> change for each worker and see which ones end up in the <code>dead</code> list.</p>',
    code='''def find_dead(last_seen, now, timeout):
    dead = []
    for w, t in last_seen.items():
        silent = now - t
        if silent > timeout:
            dead.append(w)
    return dead

table = {"W1": 95, "W2": 40, "W3": 99}
print("Dead:", find_dead(table, 100, 30))
''',
    notes={9: 'Table :: The master keeps only the time of the last heartbeat from each worker.',
           (4, 2): 'W2 :: Silent for 60 seconds, longer than the 30-second timeout.'},
)

WORKED_INTRO = 'Three jobs a cluster master really does: share out work, notice dead workers, and recover their tasks. Each solution runs live, and the trace shows the master\'s table changing in memory.'
EXAMPLES = [
    dict(level='b', tag='Scheduling · fairness', title='Share 7 input files among 3 workers',
         problem='<p>A report job has 7 input files. Give them to 3 workers in turn (file 1 to W1, file 2 to W2, …) and print each worker\'s list.</p>',
         inp='files part-1 … part-7 · workers W1, W2, W3',
         approach=['Create an empty list for each worker.',
                   'For file number <code>i</code>, the worker is <code>i % 3</code>: 0, 1, 2, 0, 1, 2, 0.',
                   'Print the lists.'],
         code='''files = ["part-1", "part-2", "part-3", "part-4", "part-5", "part-6", "part-7"]
workers = ["W1", "W2", "W3"]
plan = {w: [] for w in workers}
for i, f in enumerate(files):
    plan[workers[i % len(workers)]].append(f)
for w in workers:
    print(w, plan[w])
''', notes={3: 'Plan :: One empty list per worker.'},
         tryit='With 7 files and 3 workers, W1 gets one extra. What happens with 100 files and 7 workers? Is the work still nearly equal?'),
    dict(level='i', tag='Cluster health · monitoring', title='Which DataNodes are dead?',
         problem='<p>HDFS declares a DataNode dead after <b>630 seconds</b> (10 min 30 s) without a heartbeat. Given the last heartbeat time of each node and the current time, print the dead nodes and how many are alive.</p>',
         inp='now = 2000 s · dn1 1998, dn2 1200, dn3 1999, dn4 1500, dn5 1360',
         approach=['Silence = now − last heartbeat.',
                   'Dead if silence > 630 seconds.',
                   'Count the rest as alive.'],
         code='''TIMEOUT = 630
now = 2000
last = {"dn1": 1998, "dn2": 1200, "dn3": 1999, "dn4": 1500, "dn5": 1360}

dead = []
for node, t in last.items():
    if now - t > TIMEOUT:
        dead.append(node)
print("Dead :", dead)
print("Alive:", len(last) - len(dead), "of", len(last))
''', notes={1: 'Timeout :: 2 × 5-minute recheck + 10 × 3-second heartbeat = 630 s, the HDFS default.'},
         tryit='dn5 has been silent for 640 s and dn4 for 500 s. Why might an admin <i>not</i> want a much shorter timeout? (Think of a network switch rebooting for 2 minutes.)'),
    dict(level='a', tag='Fault tolerance · recovery', title='Re-run a dead worker\'s tasks on the least-loaded workers',
         problem='<p>Workers report their running tasks. W2 has died. Move each of its tasks, one at a time, to whichever live worker currently has the fewest tasks, marking it as a new attempt.</p>',
         inp='W1 [T1, T4] · W2 [T2, T5, T6] · W3 [T3] · dead W2',
         approach=['Remove the dead worker from the table and keep its task list.',
                   'For each lost task, find the live worker with the fewest tasks using <code>min(…, key=…)</code>.',
                   'Add the task there as attempt 2 (written with ′).'],
         code='''def least_loaded(table):
    return min(table, key=lambda w: len(table[w]))

running = {"W1": ["T1", "T4"], "W2": ["T2", "T5", "T6"], "W3": ["T3"]}
lost = running.pop("W2")
for task in lost:
    w = least_loaded(running)
    running[w].append(task + "'")
print(running)
''', notes={5: 'Dead :: <code>pop</code> removes W2 and returns its tasks in one step.'},
         tryit='Add a fourth worker <code>"W4": []</code> before the loop. Where do the lost tasks go now?'),
]

QUIZ = mix([
    dict(q='In Hadoop HDFS, which node is the master?', options=['DataNode', 'NameNode', 'NodeManager', 'Edge node'], answer=1,
         why='The <b>NameNode</b> is the HDFS master: it holds the file-system metadata. DataNodes are the workers.'),
    dict(q='In YARN, which pair is master and worker?', options=['NameNode and DataNode', 'ResourceManager and NodeManager', 'Driver and executor', 'Client and server'], answer=1,
         why='The <b>ResourceManager</b> allocates resources for the whole cluster; <b>NodeManagers</b> run containers on each worker.'),
    dict(q='What is a heartbeat?', options=['A backup of the master', 'A regular message from a worker to the master saying it is alive, often with status', 'A failed task', 'The cluster\'s clock'], answer=1,
         why='Heartbeats let the master know who is alive. In HDFS they are sent every 3 seconds by default.'),
    dict(q='By default, roughly how long does the NameNode wait before declaring a silent DataNode dead?', options=['3 seconds', '30 seconds', 'About 10 minutes 30 seconds', '24 hours'], answer=2,
         why='About <b>10.5 minutes</b> (2 × 5-minute recheck interval + 10 × 3-second heartbeat interval), so short network hiccups do not cause false alarms.'),
    dict(q='Why is a big job split into many small tasks?', options=['Small tasks use less electricity', 'Tasks run in parallel on many workers, and a failure only redoes one small piece', 'The master cannot read big files', 'Tasks are easier to name'], answer=1,
         why='Parallelism and cheap recovery: only the failed piece is re-run, not the whole job.'),
    dict(q='What does “shared-nothing” mean for a Hadoop cluster?', options=['Nodes share one big disk', 'Each node has its own CPU, memory and disks; nodes share only the network', 'Users cannot share files', 'Only one job can run at a time'], answer=1,
         why='Shared-nothing nodes are independent, so the cluster grows by adding nodes.'),
    dict(q='A master with no backup is an example of a:', options=['Heartbeat', 'Single point of failure', 'Block report', 'Container'], answer=1,
         why='If the only master fails, the whole cluster stops. Hadoop 2 added NameNode High Availability to remove this SPOF.'),
    dict(q='Which system is peer-to-peer (no master), unlike HDFS?', options=['YARN', 'Spark', 'Apache Cassandra', 'MapReduce'], answer=2,
         why='Cassandra nodes are all equal and coordinate among themselves. HDFS, YARN and Spark use masters.'),
])

REVISION = [
    '<b>Cluster</b>: networked nodes that work together as one system.',
    '<b>Master</b> coordinates (metadata, health, assignment). <b>Workers</b> store data and run tasks.',
    'HDFS: <b>NameNode</b> + DataNodes. YARN: <b>ResourceManager</b> + NodeManagers. Per job: ApplicationMaster.',
    '<b>Heartbeat</b>: worker → master every few seconds (HDFS: 3 s). The reply can carry instructions.',
    'Dead after a <b>timeout</b> (HDFS default ≈ 10 min 30 s), not after one missed heartbeat.',
    'Jobs → many small <b>tasks</b>: parallel, and a failure only redoes one piece.',
    'Dead worker → its tasks are <b>re-run</b> elsewhere automatically.',
    'Master can be a bottleneck and a <b>SPOF</b>: Hadoop 2+ uses an active and a standby NameNode.',
    'Hadoop clusters are <b>shared-nothing</b>. Cassandra is a peer-to-peer contrast.',
]
FAQ = [
    ('Explain the master–slave (master–worker) architecture of Hadoop.', 'Hadoop has two master–worker systems. In HDFS, the NameNode stores the namespace and the location of every block, and DataNodes store the blocks and send heartbeats and block reports. In YARN, the ResourceManager allocates cluster resources and NodeManagers launch and monitor containers on each worker; each application also gets an ApplicationMaster that manages its own tasks. A worker node normally runs both a DataNode and a NodeManager.'),
    ('What is a heartbeat and why is it needed?', 'A small periodic message from a worker to the master. It tells the master the worker is alive and carries status such as free space or task progress. Without heartbeats the master could not detect failures and would keep sending work to dead nodes. The master replies with commands, for example to copy or delete blocks.'),
    ('What happens when a DataNode stops sending heartbeats?', 'After the timeout (about 10.5 minutes by default) the NameNode marks it dead, stops sending it requests, and re-replicates every block that now has fewer copies than required, using the surviving replicas. Running tasks on that node fail and are rescheduled by the ApplicationMaster.'),
    ('Why not declare a node dead immediately after one missed heartbeat?', 'Short pauses are common: garbage collection, a busy disk, a switch restarting. Declaring a node dead triggers heavy work (re-copying all its blocks over the network). A timeout avoids false alarms that would waste bandwidth.'),
    ('Is the master a single point of failure in Hadoop?', 'In Hadoop 1, yes: one NameNode. Since Hadoop 2, HDFS High Availability runs an active and a standby NameNode sharing edits through JournalNodes, with ZooKeeper-based automatic failover. The ResourceManager can also run in HA mode.'),
]

PRACTICE_INTRO = 'Small programs that do the master\'s job: count, check health, assign and recover. The business problems are taken from real cluster operations.'
PROBLEMS = [
    dict(level='easy', title='Count workers and masters', stmt='Given a list of (node, role), print how many nodes have each role.', inp='[("nn1","master"),("rm1","master"),("dn1","worker"),("dn2","worker"),("dn3","worker")]',
         code='''nodes = [("nn1", "master"), ("rm1", "master"), ("dn1", "worker"), ("dn2", "worker"), ("dn3", "worker")]
count = {}
for name, role in nodes:
    count[role] = count.get(role, 0) + 1
print(count)
''', explain='<code>count.get(role, 0)</code> returns 0 the first time a role is seen. Real clusters have a handful of masters and many workers.'),
    dict(level='easy', title='Heartbeats per hour', stmt='A DataNode sends a heartbeat every 3 seconds. How many does one node send per hour, and how many does the NameNode receive per hour from 500 nodes?', inp='3 s interval · 500 nodes',
         code='''per_node = 3600 // 3
print("One node:", per_node)
print("500 nodes:", per_node * 500)
''', explain='1,200 per node per hour; 6 lakh per hour for 500 nodes. Heartbeats are tiny, but this is one reason the master must be efficient.'),
    dict(level='easy', title='The HDFS dead-node timeout', stmt='The timeout is 2 × recheck interval + 10 × heartbeat interval. Calculate it in seconds for the defaults: recheck 300 s, heartbeat 3 s. Print it as minutes and seconds.', inp='recheck 300 s · heartbeat 3 s',
         code='''t = 2 * 300 + 10 * 3
print(t, "seconds =", t // 60, "min", t % 60, "s")
''', explain='630 s = 10 min 30 s. Administrators can lower the recheck interval to detect failures faster.'),
    dict(level='medium', title='Rounds needed', stmt='A job has N tasks and the cluster has W workers with S slots each. Each round, every slot runs one task. Print how many rounds (“waves”) are needed for N = 50, W = 6, S = 4.', inp='N = 50, W = 6, S = 4',
         code='''import math
N, W, S = 50, 6, 4
print(math.ceil(N / (W * S)), "waves")
''', explain='24 tasks run at once, so 50 tasks need 3 waves (24 + 24 + 2). Hadoop users call these map “waves”.'),
    dict(level='medium', title='Find the slow worker', stmt='Given each worker\'s finished task times in seconds, print the worker whose average is more than 1.5 times the cluster average.', inp='W1 [30, 32, 31] · W2 [29, 30] · W3 [95, 90] · W4 [33]',
         code='''times = {"W1": [30, 32, 31], "W2": [29, 30], "W3": [95, 90], "W4": [33]}
all_t = [t for ts in times.values() for t in ts]
avg = sum(all_t) / len(all_t)
for w, ts in times.items():
    a = sum(ts) / len(ts)
    if a > 1.5 * avg:
        print(w, "is slow:", round(a), "s vs cluster", round(avg), "s")
''', explain='A worker that is alive but much slower is a <b>straggler</b> (bad disk, overheating). Hadoop can launch a backup copy of its tasks elsewhere: <b>speculative execution</b>.'),
    dict(level='medium', title='Blacklist a flaky node', stmt='Tasks failed on these nodes in the last hour. Print the nodes with 3 or more failures, which the scheduler should stop using.', inp='["dn4","dn2","dn4","dn7","dn4","dn2","dn9","dn2","dn2"]',
         code='''failures = ["dn4", "dn2", "dn4", "dn7", "dn4", "dn2", "dn9", "dn2", "dn2"]
count = {}
for n in failures:
    count[n] = count.get(n, 0) + 1
bad = sorted(n for n, c in count.items() if c >= 3)
print("Stop using:", bad, count)
''', explain='MapReduce does something similar: if many tasks of a job fail on one node, that node is blacklisted for the job.'),
    dict(level='business', title='Will the job finish before 6 am?', stmt='A nightly job has 400 tasks of about 6 minutes each. The cluster has 20 workers with 8 slots each. One worker usually fails during the night, losing 8 running tasks that must be redone. The job starts at 1 am. Print the estimated finish time.', inp='400 tasks × 6 min · 20 workers × 8 slots · 8 tasks redone',
         code='''import math
tasks, minutes = 400 + 8, 6
slots = 19 * 8                     # plan for one worker lost
waves = math.ceil(tasks / slots)
total = waves * minutes
print("Waves:", waves, "| minutes:", total)
print(f"Finish at about {1 + total // 60}:{total % 60:02d} am")
''', explain='Plan with one worker fewer and the redone tasks included. 408 tasks on 152 slots = 3 waves = 18 minutes, well before 6 am.'),
    dict(level='business', title='How much does a dead node cost in re-copying?', stmt='A dead DataNode held 60 TB of block replicas. The cluster can spend 2 GB/s in total on re-replication. How many hours until every block has its full number of copies again?', inp='60 TB lost · 2 GB/s',
         code='''tb = 60
gb_per_s = 2
hours = tb * 1024 / gb_per_s / 3600
print(round(hours, 1), "hours")
''', explain='About 8.5 hours of network and disk work. This is why the NameNode does not declare nodes dead too quickly, and why very large nodes make recovery slow.'),
]

SCN_INTRO = 'Interview situations about masters, workers and heartbeats. Think of your answer, then compare it with the model answer.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Telecom · operations</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“The NameNode server crashed. Is our data gone?”</h4>
      <p class="scn__situation">At 2 am the only NameNode of a 40-node cluster crashes. The DataNodes are all fine. A manager panics: “Have we lost all the data?”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know what the master stores, what the workers store, and why masters need protection?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The <b>file contents</b> are safe: the blocks are on the DataNodes' disks.</li>
          <li>But without the NameNode, nobody knows which blocks form which file, so the file system is <b>unavailable</b> until it comes back.</li>
          <li>The NameNode's metadata is saved on its own disk (the fsimage and edit log). Restart it on the same or a new machine from that saved metadata, and the DataNodes re-register with block reports.</li>
          <li>Long-term fix: <b>NameNode High Availability</b> with a standby that takes over automatically, and backups of the metadata directories.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid saying:</b> “The Secondary NameNode will take over.” It doesn't. It only helps with checkpoints (Module 5).</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · performance</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The job is stuck at 99% for 20 minutes</h4>
      <p class="scn__situation">A sales job always reaches 99% in 10 minutes, then waits 20 more minutes for the last task. The node running that task is alive and sending heartbeats.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you tell a slow worker (straggler) from a dead one, and do you know the remedies?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>Check which task is slow and on which node. If <b>one node</b> is always slow (failing disk, overheating), it is a straggler: fix or remove it. <b>Speculative execution</b> runs a backup copy of the slow task on another node and uses whichever finishes first.</li>
          <li>If it is always the <b>same piece of data</b>, it is <b>data skew</b>: one task gets far more data than others (for example one huge city or one product). Fix the partitioning or split the hot key.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “Add more nodes.” That doesn't help one big task.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · design</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Make the dead-node timeout 10 seconds?</h4>
      <p class="scn__situation">A teammate wants failures detected faster, so he proposes changing HDFS to declare a DataNode dead after 10 seconds of silence instead of about 10 minutes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand the trade-off between fast detection and false alarms?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>A 10-second timeout would mark nodes dead during harmless pauses: a long garbage-collection pause, a switch reboot, a busy disk.</li>
          <li>Each false “death” makes the NameNode re-copy all of that node's blocks (often many TB), flooding the network. When the node returns, the extra copies must be deleted again.</li>
          <li>Reading data is already protected: clients and tasks simply use another replica if one node does not respond. Re-replication can safely wait a few minutes.</li>
          <li>If faster detection is truly needed, lower it moderately and test, and look at stale-node settings that avoid slow nodes without declaring them dead.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> treating faster as always better. Detection speed has a cost.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Why does Hadoop need a master at all?”</h4>
      <p class="scn__situation">The interviewer says: “Cassandra works without a master. Why didn't Hadoop do the same?”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand the trade-offs, not just the definitions?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>HDFS must know exactly which blocks make up each file and where they are. One master gives a single, consistent answer and makes decisions (placement, re-replication) simple.</li>
          <li>The master is also where scheduling decisions are easy: one place sees all free resources.</li>
          <li>The costs: the master can become a bottleneck (memory for metadata) and a single point of failure. Hadoop answers with High Availability and federation.</li>
          <li>Cassandra is built for a different job: always-on reads and writes of small records, where avoiding a master improves availability.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> saying one design is simply “better”. Each fits a different problem.</p>
      </div></details>
    </article>'''
