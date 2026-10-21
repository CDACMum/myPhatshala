import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Which role matters how much?',
    intro='<p><b>Client</b> = edge node, dark boxes = masters (two NameNodes for HA), DataNode boxes = workers. Break each kind and compare what happens.</p>',
    racks=3, nodes=3, features=['job', 'fail', 'ha', 'fsck'],
    preload=[dict(name='orders.parquet', sizeMB=1024)],
    **{'try': [
        dict(text='Run the job from the edge node (the Client box). Watch which boxes do the work.', on='job-done'),
        dict(text='Stop a <b>worker</b> during a job: routine. Tasks re-run, data stays available.', on='node-stop'),
        dict(text='Stop the active <b>master</b> (NameNode): only HA saves you.', on='nn-failover'),
        dict(text='Run <b>hdfs fsck /</b>: losing one worker never loses data.', on='fsck'),
    ]},
)))

META = dict(
    module='03-how-a-cluster-works', lesson='03-node-roles-master-worker-edge-and-gateway', n='3.3',
    module_label='Module 3 · How one Hadoop cluster works',
    title='Node roles: master, worker, edge and gateway',
    desc='The roles of nodes in a Hadoop cluster: master nodes (NameNode, ResourceManager, JournalNodes, ZooKeeper), worker nodes (DataNode + NodeManager), edge/gateway nodes for users and clients, and utility nodes (Hive Metastore, HiveServer2, managers). Hardware per role, example layouts from 1 to 200+ nodes, cloud equivalents, with animations, a playground, Python, quiz and interview scenarios.',
    og_desc='Masters coordinate, workers work, edge nodes are the front door. Learn every role and how real clusters are laid out.',
    minutes=24, level='Beginner → Intermediate',
    lead='Every machine in a Hadoop cluster has a role, and respecting the roles is what keeps a cluster healthy. This lesson explains master nodes (protected coordinators), worker nodes (storage and compute managed by YARN), edge or gateway nodes (where users and tools connect) and utility nodes (supporting services), what runs on each, what hardware they need, and how companies lay them out for clusters of 5, 50 and 500 machines.',
    chips=['Role layouts by size', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Plan the roles for a cluster',
    intro='<p>This program assigns roles to the machines of a cluster: three masters for HA, one utility node, two edge nodes, and workers for the rest. Then it prints the plan. Try the challenges to check a layout for mistakes.</p>',
    code='''def plan(total, ha=True):
    masters = 3 if ha else 1
    utility, edge = 1, 2 if total >= 20 else 1
    workers = total - masters - utility - edge
    roles = {}
    for i in range(1, masters + 1):
        roles[f"master{i}"] = "master"
    roles["util1"] = "utility"
    for i in range(1, edge + 1):
        roles[f"edge{i}"] = "edge"
    for i in range(1, workers + 1):
        roles[f"worker{i}"] = "worker"
    return roles

roles = plan(30)
summary = {}
for host, role in roles.items():
    summary[role] = summary.get(role, 0) + 1
print(summary)
''',
    anno=[
        ('masters = 3 if ha else 1', 'High availability needs three machines for the JournalNode and ZooKeeper majorities; without HA, one master.'),
        ('utility, edge = 1, 2 if total >= 20 else 1', 'Tuple assignment: <code>utility = 1</code>, and <code>edge</code> is 2 for bigger clusters, 1 for small ones.'),
        ('workers = total - masters - utility - edge', 'Every remaining machine is a worker: storage and compute.'),
    ],
    tasks=[
        dict(label='1 · Plan 30 nodes', hint='Press <b>Run</b>. Then try <code>plan(8, ha=False)</code> for a small cluster.', code=None),
        dict(label='2 · Daemons per role', hint='<b>Predict first:</b> how many DataNode processes run in a 30-node cluster with 3 masters, 1 utility and 2 edge nodes?',
             code='''daemons = {"master": ["NameNode", "ResourceManager", "JournalNode", "ZooKeeper"],
           "utility": ["HiveMetastore", "HiveServer2"], "edge": [],
           "worker": ["DataNode", "NodeManager"]}
counts = {"master": 3, "utility": 1, "edge": 2, "worker": 24}
total = {}
for role, n in counts.items():
    for d in daemons[role]:
        total[d] = total.get(d, 0) + n
print(total)
'''),
        dict(label='3 · Check quorum placement', hint='ZooKeeper must run on an odd number of <i>different</i> hosts. Is this layout safe? Move one ZooKeeper to m3.',
             code='''zookeeper_hosts = ["m1", "m2", "m2"]
distinct = set(zookeeper_hosts)
print("Servers:", len(zookeeper_hosts), "| distinct hosts:", len(distinct))
print("Safe" if len(distinct) == len(zookeeper_hosts) and len(distinct) % 2 == 1 else "Not safe")
'''),
        dict(label='4 · Who may log in?', hint='Filter the hosts where ordinary users may log in. Only edge nodes should appear.',
             code='''roles = {"m1": "master", "m2": "master", "util1": "utility",
         "edge1": "edge", "edge2": "edge", "w1": "worker", "w2": "worker"}
login_ok = [h for h, r in roles.items() if r == "edge"]
print("Users may log in to:", login_ok)
'''),
        dict(label='5 · Spot the error', hint='This layout check should flag worker daemons on a master, but it crashes. Read the error and fix the dictionary key.',
             expect='error',
             code='''hosts = {"m1": {"role": "master", "daemons": ["NameNode", "DataNode"]}}
for name, h in hosts.items():
    if h["role"] == "master" and "DataNode" in h["deamons"]:
        print(name, ": worker daemon on a master!")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Counting roles, one line at a time',
    intro='<p>Watch the loop turn a host-to-role map into a summary: a dictionary that counts how many hosts have each role.</p>',
    code='''roles = {"m1": "master", "m2": "master", "e1": "edge", "w1": "worker", "w2": "worker"}
summary = {}
for host, role in roles.items():
    summary[role] = summary.get(role, 0) + 1
print(summary)
''',
    notes={4: 'Count :: <code>get(role, 0)</code> starts each new role at zero.'},
)

WORKED_INTRO = 'Three tasks from real cluster design reviews: lay out a cluster, find rule violations in someone else\'s layout, and cost the hardware by role. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Design · layout', title='Lay out a 12-node cluster without HA',
         problem='<p>A college lab gets 12 servers for a Hadoop cluster. No HA is needed. Assign 1 master, 1 edge node and the rest as workers, and print the daemons each host will run.</p>',
         inp='12 hosts · no HA',
         approach=['Host 1 is the master: NameNode, SecondaryNameNode, ResourceManager, JobHistoryServer.',
                   'Host 2 is the edge node: no daemons, only clients.',
                   'Hosts 3–12 are workers: DataNode and NodeManager.'],
         code='''hosts = [f"lab{i:02d}" for i in range(1, 13)]
layout = {hosts[0]: ["NameNode", "SecondaryNameNode", "ResourceManager", "JobHistoryServer"],
          hosts[1]: ["(clients only)"]}
for h in hosts[2:]:
    layout[h] = ["DataNode", "NodeManager"]
for h in hosts[:3] + hosts[-1:]:
    print(h, layout[h])
print("Workers:", len(hosts) - 2)
''', notes={2: 'Masters :: In a non-HA cluster, the Secondary NameNode does checkpoints.'},
         tryit='Now add HA: which three hosts become masters, and how many workers are left?'),
    dict(level='i', tag='Design review · rules', title='Find the mistakes in a proposed layout',
         problem='<p>A teammate proposes this layout. Check three rules: (1) no DataNode or NodeManager on a master; (2) ZooKeeper on an odd number of distinct hosts; (3) the two NameNodes on different racks. Print every violation.</p>',
         inp='m1 (rack1): NameNode, ZooKeeper, DataNode · m2 (rack1): NameNode, ZooKeeper · m3 (rack2): ZooKeeper, ZooKeeper',
         approach=['Loop over hosts; flag worker daemons on a master.',
                   'Collect hosts running ZooKeeper; compare distinct count with total and check it is odd.',
                   'Compare the racks of the two NameNode hosts.'],
         code='''layout = {"m1": ("rack1", ["NameNode", "ZooKeeper", "DataNode"]),
          "m2": ("rack1", ["NameNode", "ZooKeeper"]),
          "m3": ("rack2", ["ZooKeeper", "ZooKeeper"])}
for h, (rack, ds) in layout.items():
    if {"DataNode", "NodeManager"} & set(ds):
        print("Rule 1:", h, "runs worker daemons")
zk = [h for h, (r, ds) in layout.items() for d in ds if d == "ZooKeeper"]
if len(set(zk)) != len(zk) or len(set(zk)) % 2 == 0:
    print("Rule 2: ZooKeeper on", len(zk), "servers but", len(set(zk)), "hosts")
nn_racks = {r for h, (r, ds) in layout.items() if "NameNode" in ds}
if len(nn_racks) < 2:
    print("Rule 3: both NameNodes on", nn_racks)
''', notes={4: 'Rule 1 :: Set intersection finds any worker daemon.'},
         tryit='Fix all three problems in the dictionary until the program prints nothing.'),
    dict(level='a', tag='Budget · hardware', title='What does each role cost?',
         problem='<p>For a 40-node cluster with 3 masters, 1 utility, 2 edge and 34 workers, compute the hardware cost per role and the share spent on workers. Prices (illustrative): master Rs 9 lakh, utility Rs 5 lakh, edge Rs 4 lakh, worker Rs 12 lakh.</p>',
         inp='3 × 9 L · 1 × 5 L · 2 × 4 L · 34 × 12 L',
         approach=['Multiply count × price for each role.',
                   'Sum for the total.',
                   'Worker share = worker cost ÷ total.'],
         code='''roles = {"master": (3, 9), "utility": (1, 5), "edge": (2, 4), "worker": (34, 12)}
total = 0
for role, (n, lakh) in roles.items():
    cost = n * lakh
    total += cost
    print(f"{role:8}: {n:>2} x Rs {lakh} lakh = Rs {cost} lakh")
worker_cost = roles["worker"][0] * roles["worker"][1]
print(f"Total Rs {total} lakh; workers are {worker_cost / total:.0%}")
''', notes={6: 'Cost :: Count times price per role.'},
         tryit='Workers are dense with disks, so they dominate. Masters are only a few per cent, which is why skimping on master reliability is a false saving.'),
]

QUIZ = mix([
    dict(q='Where should ordinary users log in to run commands and submit jobs?', options=['The NameNode', 'An edge (gateway) node', 'Any worker node', 'The ZooKeeper server'], answer=1,
         why='Edge nodes have the client tools and configuration and run no core daemons, so user activity can\'t disturb the cluster.'),
    dict(q='Which daemons run on a typical worker node?', options=['NameNode and ResourceManager', 'DataNode and NodeManager', 'HiveServer2 and Metastore', 'JournalNode and ZKFC'], answer=1,
         why='Workers provide storage (<b>DataNode</b>) and compute (<b>NodeManager</b>).'),
    dict(q='Why is running a heavy script on the NameNode host dangerous?', options=['It deletes HDFS data', 'It competes for the NameNode\'s memory and CPU, causing pauses that slow every HDFS operation', 'It changes the replication factor', 'It is not dangerous'], answer=1,
         why='The NameNode keeps all metadata in its JVM heap; starving it causes long pauses for the whole cluster.'),
    dict(q='Why do ZooKeeper and JournalNodes run on 3 or 5 different machines?', options=['To use spare disk space', 'They work by majority (quorum), so an odd number on separate hosts survives failures', 'Because Hadoop requires exactly 3 masters', 'To store more blocks'], answer=1,
         why='With 3 hosts, a majority of 2 survives one failure; with 5, a majority of 3 survives two.'),
    dict(q='Which service usually runs on a utility node?', options=['DataNode', 'Hive Metastore and its database', 'NodeManager', 'Map tasks'], answer=1,
         why='Utility nodes host supporting services such as the Hive Metastore, HiveServer2, Oozie, Ranger and the cluster manager.'),
    dict(q='In Amazon EMR, which node type runs YARN only, without HDFS?', options=['Primary node', 'Core node', 'Task node', 'Edge node'], answer=2,
         why='<b>Task nodes</b> add compute only, so they can be added or removed (or use spot instances) without risking HDFS data. Core nodes run both.'),
    dict(q='Why should users not run processes by hand on worker nodes?', options=['Workers have no Python', 'Work outside YARN uses memory YARN thinks is free, so containers can fail and nothing is accounted', 'It is faster on masters', 'Workers are read-only'], answer=1,
         why='All work on workers should go through YARN so it is scheduled, limited and fair.'),
    dict(q='A small 8-node test cluster without HA typically has:', options=['3 masters, 5 workers', '1 master, 1 edge, 6 workers', '8 masters', '4 edge, 4 workers'], answer=1,
         why='One master (NameNode, RM, history), one edge node for users, and the rest as workers.'),
])

REVISION = [
    '<b>Master</b>: NameNode(s), ResourceManager(s), JobHistory, JournalNodes, ZKFC. Few, reliable, protected.',
    '<b>Worker</b>: DataNode + NodeManager. Many, identical, replaceable. All work goes through YARN.',
    '<b>Edge / gateway</b>: client tools + configs, user logins, notebooks, schedulers. No core daemons.',
    '<b>Utility</b>: ZooKeeper, Hive Metastore + DB, HiveServer2, Oozie, Ranger, cluster manager.',
    'Quorum services (ZooKeeper, JournalNodes) on 3 or 5 <b>different</b> hosts; NameNodes on different racks.',
    'Layouts: 1 node (learning) · small: 1 master + edge + workers · medium: 3 masters, utility, 2 edges · large: dedicated masters, federation.',
    'Cloud: EMR primary / core / task; Dataproc master / primary workers / secondary workers.',
    'Rule of thumb: users only on edge nodes.',
]
FAQ = [
    ('What is an edge node in Hadoop?', 'A machine that has the Hadoop client libraries, configuration files and tools (hdfs, yarn, hive/beeline, spark-submit, notebooks) but runs no core cluster daemons. It is the controlled entry point for users and applications: they log in there, interact with HDFS and submit jobs, while the work runs on the workers. It is often the only cluster host reachable from the corporate network.'),
    ('What runs on master nodes?', 'The coordinating services: the active and standby NameNodes (with ZKFCs), JournalNodes for the shared edit log, the ResourceManager(s), the JobHistory Server, and often ZooKeeper. In non-HA clusters, the Secondary NameNode. Masters are sized for memory and reliability and protected from user workloads.'),
    ('Why not run DataNodes on master nodes?', 'Storage and compute work on a master competes with the master daemons for memory, CPU and disk I/O, risking pauses or crashes that affect the whole cluster. It also makes masters harder to maintain, because taking one down would also remove data and compute capacity.'),
    ('How many ZooKeeper servers should a cluster have?', 'An odd number, usually 3 for most clusters and 5 for large or critical ones, each on a different host and ideally on different racks. ZooKeeper needs a majority to operate, so 3 servers tolerate one failure and 5 tolerate two; 4 servers still tolerate only one.'),
    ('How do node roles map to cloud services like EMR?', 'EMR\'s primary node runs the master services; core nodes run HDFS DataNodes and YARN NodeManagers; task nodes run only NodeManagers, so they can be scaled in and out freely. Dataproc similarly has master nodes, primary workers (HDFS + YARN) and optional secondary workers (compute only, often preemptible).'),
]

PRACTICE_INTRO = 'Small programs and calculations for planning and checking node roles.'
PROBLEMS = [
    dict(level='easy', title='How many workers?', stmt='A 50-node cluster has 3 masters, 2 utility nodes and 3 edge nodes. How many workers?', inp='50 − 3 − 2 − 3',
         code='print(50 - 3 - 2 - 3, "workers")\n', explain='42 workers. Capacity planning uses this number, not 50.'),
    dict(level='easy', title='Quorum survivors', stmt='For 3 and 5 ZooKeeper servers, print the majority size and how many failures each survives.', inp='[3, 5]',
         code='''for n in [3, 5]:
    majority = n // 2 + 1
    print(n, "servers: majority", majority, "| survives", n - majority, "failure(s)")
''', explain='3 → majority 2, survives 1. 5 → majority 3, survives 2.'),
    dict(level='easy', title='Role of a host', stmt='Given a dictionary of host roles, print the role of edge2 and of worker7.', inp='{"edge2": "edge", "worker7": "worker", "m1": "master"}',
         code='''roles = {"edge2": "edge", "worker7": "worker", "m1": "master"}
print("edge2:", roles["edge2"], "| worker7:", roles["worker7"])
''', explain='A host-to-role inventory is the first thing to keep in any cluster runbook.'),
    dict(level='medium', title='Group hosts by role', stmt='Turn a host → role map into role → sorted list of hosts.', inp='{"w2": "worker", "m1": "master", "e1": "edge", "w1": "worker", "m2": "master"}',
         code='''roles = {"w2": "worker", "m1": "master", "e1": "edge", "w1": "worker", "m2": "master"}
by_role = {}
for h, r in roles.items():
    by_role.setdefault(r, []).append(h)
for r in sorted(by_role):
    print(r, sorted(by_role[r]))
''', explain='The same reverse mapping cluster managers show as “hosts by role”.'),
    dict(level='medium', title='Racks of the masters', stmt='Check that the three masters are on three different racks; print the racks used and whether the rule holds.', inp='{"m1": "r1", "m2": "r2", "m3": "r2"}',
         code='''rack = {"m1": "r1", "m2": "r2", "m3": "r2"}
used = set(rack.values())
print("Racks used:", sorted(used), "| all different:", len(used) == len(rack))
''', explain='m2 and m3 share r2: losing that rack would take two of three JournalNodes and ZooKeepers, breaking the majority.'),
    dict(level='medium', title='Edge nodes for the users', stmt='Each edge node comfortably serves about 25 active users. With 140 users and one spare for maintenance, how many edge nodes are needed?', inp='140 users · 25 per node · +1 spare',
         code='''import math
print(math.ceil(140 / 25) + 1, "edge nodes")
''', explain='6 for the load plus 1 spare: 7. Big companies put edge nodes behind a load balancer.'),
    dict(level='business', title='Task nodes for a sale weekend', stmt='An EMR cluster has 20 core nodes. For a sale weekend, analytics needs 3× the usual compute for 60 hours. Task nodes cost Rs 30 per hour (spot). How many task nodes and what extra cost?', inp='20 core · 3× compute · 60 h · Rs 30/h',
         code='''core = 20
extra_nodes = core * 3 - core
cost = extra_nodes * 60 * 30
print("Add", extra_nodes, "task nodes; extra cost Rs", cost)
''', explain='40 task nodes for Rs 72,000 (illustrative price). Task nodes add compute without HDFS, so removing them after the weekend is safe.'),
    dict(level='business', title='Cost of the outage from a user on a master', stmt='A user\'s script on the NameNode host caused a 40-minute HDFS slowdown. 120 analysts were blocked, each costing Rs 900 per hour, and 3 nightly SLAs were missed at Rs 50,000 each. Estimate the cost.', inp='40 min · 120 analysts · Rs 900/h · 3 × Rs 50,000',
         code='''people = 120 * 900 * 40 / 60
sla = 3 * 50_000
print(f"Lost time: Rs {people:,.0f} | SLA penalties: Rs {sla:,} | Total: Rs {people + sla:,.0f}")
''', explain='About Rs 2.2 lakh for one mistake (illustrative). A second edge node and restricted logins cost far less.'),
]

SCN_INTRO = 'Role questions are about judgement: where things should run, and what to do when someone breaks the rules.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · design</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Lay out roles for a 20-node cluster</h4>
      <p class="scn__situation">You have 20 identical servers and the business wants HDFS to keep running even if one master fails. How do you assign roles?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know which services need HA and how to place quorums?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>3 masters</b> on different racks: active NameNode + ZKFC on m1, standby NameNode + ZKFC on m2, and JournalNode + ZooKeeper on all three; ResourceManager (and a standby) on m2/m3; JobHistory on m3.</li>
          <li><b>1 utility</b> node for Hive Metastore + database and HiveServer2 (or on m3 if budget is tight).</li>
          <li><b>1–2 edge</b> nodes for users and tools.</li>
          <li><b>14–15 workers</b> with DataNode + NodeManager.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> putting DataNodes on the masters “to use the disks”.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · incident</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Containers keep getting killed on one worker</h4>
      <p class="scn__situation">Tasks on worker <code>w12</code> are often killed with “running beyond physical memory limits” or the node runs out of memory. Other workers are fine.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you consider work happening outside YARN?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>Log in (as an admin) and check what else is running: <code>top</code> often shows a user's script, a stray Python process or a forgotten service on that worker.</li>
          <li>YARN offers memory based on configuration; anything running outside YARN takes memory YARN believes is free, so the OS or YARN kills containers.</li>
          <li>Stop the stray process, move the user to the edge node, and restrict logins on workers.</li>
          <li>If nothing extra is running, check the node's memory settings against its real RAM.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> simply raising container memory for all jobs.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Security · access</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Analysts want SSH access to every node</h4>
      <p class="scn__situation">The analytics team asks for SSH to all cluster machines “to debug jobs faster”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you meet the real need while protecting the cluster?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Give access to <b>edge nodes</b> only. Masters and workers stay on the private cluster network, reachable by admins.</li>
          <li>Provide what they actually need for debugging: the ResourceManager and JobHistory UIs, <code>yarn logs -applicationId</code> for container logs (with log aggregation on), and the Spark History Server.</li>
          <li>Use Kerberos and Ranger so their permissions are the same whatever tool they use.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> a flat “no” without offering the tools that solve their problem.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Cloud · cost</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Scale down an EMR cluster safely</h4>
      <p class="scn__situation">An EMR cluster has 10 core nodes and 30 task nodes. Overnight, the load drops. Your manager asks you to remove 25 nodes to save money.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know which cloud roles hold data?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Remove <b>task nodes</b> first: they run only YARN, so removing them loses no HDFS data (running tasks are retried elsewhere).</li>
          <li>Removing <b>core nodes</b> means decommissioning their DataNodes so HDFS can copy their blocks away first, which is slow and risky if done in bulk.</li>
          <li>Better still, keep data in S3 and size HDFS (core nodes) small, so the cluster can shrink freely, or use managed autoscaling.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> terminating core nodes directly; with replication 3 on a small cluster you can lose blocks.</p>
      </div></details>
    </article>'''
