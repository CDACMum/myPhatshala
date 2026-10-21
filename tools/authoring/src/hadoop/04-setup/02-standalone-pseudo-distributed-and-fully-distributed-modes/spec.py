import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='One node, then many',
    intro='<p>This cluster starts with <b>one DataNode and replication 1</b>, like pseudo-distributed mode. Work through the list: first see why one node is not enough, then grow the cluster.</p>',
    racks=1, nodes=1, replication=1, features=['upload', 'job', 'fail', 'scale', 'fsck'],
    sizes=[1, 3, 6],
    preload=[dict(name='canteen_orders.csv', sizeMB=300)],
    **{'try': [
        dict(text='Run the job on the one-node cluster. It works: every task runs on the same node.', on='job-done'),
        dict(text='Click the only DataNode to stop it. No other copy exists anywhere.', on='node-stop'),
        dict(text='Run <b>hdfs fsck /</b> to see the damage.', on='fsck'),
        dict(text='Grow the cluster to <b>3 nodes</b> (this restarts it with the same data).', on='resize'),
        dict(text='Upload a file with <b>Replication 3</b>, then stop any node: the data survives.', on='upload-done'),
    ]},
)))

META = dict(
    module='04-setup', lesson='02-standalone-pseudo-distributed-and-fully-distributed-modes', n='4.2',
    module_label='Module 4 · Setup',
    title='Standalone, pseudo-distributed and fully distributed modes',
    desc='The three ways to run Hadoop: standalone (local) mode with one JVM and local files, pseudo-distributed mode with every daemon on one machine, and fully distributed mode across many machines. The settings that decide the mode (fs.defaultFS, mapreduce.framework.name, dfs.replication, workers), the same job run in all three with real Hadoop 3.5.0 output, a mode-detection script, playground, quiz and interview scenarios.',
    og_desc='Same Hadoop download, three modes. See exactly what changes, with real outputs from all three.',
    minutes=24, level='Beginner',
    lead='The Hadoop you download can run as a simple local program, as a one-machine cluster, or as a real multi-machine cluster. Which one you get depends on a handful of settings. This lesson runs the same job in all three modes on a real Hadoop 3.5.0 install, shows what jps and the configuration report in each, and explains when each mode is used at work.',
    chips=['Real Hadoop 3.5.0 output', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Work out the mode from the settings',
    intro='<p>The mode is decided by a few configuration values. This function reads them (here typed in as dictionaries, exactly as <code>hdfs getconf</code> printed them on our three test machines) and names the mode.</p>',
    code='''def mode(conf):
    fs = conf.get("fs.defaultFS", "file:///")
    if fs.startswith("file:"):
        return "standalone"
    host = fs.split("//")[1].split(":")[0]
    if host in ("localhost", "127.0.0.1"):
        return "pseudo-distributed"
    return "fully distributed (NameNode on " + host + ")"

machines = {
    "fresh unpack": {},
    "Riya's WSL": {"fs.defaultFS": "hdfs://localhost:9000", "dfs.replication": "1"},
    "Docker cluster": {"fs.defaultFS": "hdfs://namenode", "dfs.replication": "3"},
}
for name, conf in machines.items():
    print(f"{name:15} -> {mode(conf)}")
''',
    anno=[
        ('fs = conf.get("fs.defaultFS", "file:///")', 'If the setting is missing, Hadoop uses its default: <code>file:///</code>, the local disk. That is why a fresh unpack is standalone.'),
        ('host = fs.split("//")[1].split(":")[0]', '<code>hdfs://localhost:9000</code> → after <code>//</code> is <code>localhost:9000</code> → before <code>:</code> is <code>localhost</code>.'),
        ('"Docker cluster": {"fs.defaultFS": "hdfs://namenode", "dfs.replication": "3"},', 'No port means the default NameNode RPC port, 8020.'),
    ],
    tasks=[
        dict(label='1 · Three machines', hint='Press <b>Run</b>. Then add a machine with <code>{"fs.defaultFS": "hdfs://nn1.corp.in:8020"}</code>.', code=None),
        dict(label='2 · Count the JVMs', hint='<b>Predict first:</b> how many Java processes (excluding Jps) does each mode run when idle? A worker runs a DataNode and a NodeManager.',
             code='''masters = ["NameNode", "SecondaryNameNode", "ResourceManager"]
worker = ["DataNode", "NodeManager"]
print("standalone, idle  :", 0)
print("pseudo            :", len(masters) + len(worker))
for workers in [3, 10]:
    print(f"fully, {workers:>2} workers :", len(masters) + workers * len(worker))
'''),
        dict(label='3 · Under-replicated?', hint='Each block wants <code>dfs.replication</code> copies but can have at most one per DataNode. Find which setups would report under-replicated blocks.',
             code='''setups = [("pseudo, repl 1", 1, 1), ("pseudo, repl 3", 1, 3),
          ("3 DataNodes, repl 3", 3, 3), ("2 DataNodes, repl 3", 2, 3)]
for name, datanodes, repl in setups:
    copies = min(datanodes, repl)
    print(f"{name:20}: {copies} copies -> {'OK' if copies == repl else 'UNDER-REPLICATED'}")
'''),
        dict(label='4 · Build the workers file', hint='Fully distributed mode needs one worker host name per line in <code>etc/hadoop/workers</code>. Generate it for 4 workers named <code>worker1</code>…',
             code='''hosts = [f"worker{i}" for i in range(1, 5)]
workers_file = "\\n".join(hosts)
print(workers_file)
print("---", len(hosts), "lines")
'''),
        dict(label='5 · Spot the error', hint='This function says a fresh, unconfigured install is “pseudo-distributed”. Find and fix the default.',
             code='''def mode(conf):
    fs = conf.get("fs.defaultFS", "hdfs://localhost:9000")
    if fs.startswith("file:"):
        return "standalone"
    return "pseudo-distributed"

print("fresh unpack ->", mode({}))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

_script = open(os.path.join(HERE, 'which_mode.sh')).read()
PCRUN = dict(
    heading='Run it on your machine: which mode am I in?',
    intro='<p>This script asks Hadoop for its settings and lists the running daemons, then names the mode. Save it as <code>which_mode.sh</code> (Hadoop\'s <code>bin</code> must be on your <code>PATH</code>). The three outputs below are from real runs.</p>',
    items=[
        dict(title='Standalone: a fresh unpack', file='which_mode.sh',
             cmd=_script + '\n# In the terminal:\n#   bash which_mode.sh',
             output='''fs.defaultFS             : file:///
mapreduce.framework.name : local
daemons on this machine  : none
MODE: standalone (local files, no daemons)''',
             note='Nothing configured, nothing running. Jobs still work, inside one JVM, on local files.'),
        dict(title='Pseudo-distributed: after start-dfs.sh and start-yarn.sh', file='which_mode.sh',
             cmd='start-dfs.sh\nstart-yarn.sh\nbash which_mode.sh',
             output='''Starting namenodes on [localhost]
Starting datanodes
Starting secondary namenodes [vm]
Starting resourcemanager
Starting nodemanagers
fs.defaultFS             : hdfs://localhost:9000
mapreduce.framework.name : yarn
daemons on this machine  : DataNode NameNode NodeManager ResourceManager SecondaryNameNode
MODE: pseudo-distributed (every daemon on this machine)''',
             note='Five daemons on one machine. Your machine name will appear instead of <code>vm</code>.'),
        dict(title='Fully distributed: on the Docker practice cluster', file='which_mode.sh',
             cmd='docker cp which_mode.sh mpcluster-namenode-1:/tmp/\ndocker exec mpcluster-namenode-1 bash /tmp/which_mode.sh\ndocker cp which_mode.sh mpcluster-datanode-1:/tmp/\ndocker exec mpcluster-datanode-1 bash /tmp/which_mode.sh',
             output='''fs.defaultFS             : hdfs://namenode
mapreduce.framework.name : yarn
daemons on this machine  : NameNode
MODE: fully distributed (NameNode at namenode)
fs.defaultFS             : hdfs://namenode
mapreduce.framework.name : yarn
daemons on this machine  : DataNode
MODE: fully distributed (NameNode at namenode)''',
             note='Each container runs only its own role: the master container has just the NameNode, a worker container has just a DataNode. The cluster is set up in Lesson 4.3.'),
    ],
)

TRACE = dict(
    heading='Deciding the mode, one line at a time',
    intro='<p>Follow Riya\'s pseudo-distributed setting through the function and watch how the host name is cut out of the address.</p>',
    code='''fs = "hdfs://localhost:9000"
after = fs.split("//")[1]
host = after.split(":")[0]
if fs.startswith("file:"):
    mode = "standalone"
elif host == "localhost":
    mode = "pseudo-distributed"
else:
    mode = "fully distributed"
print(host, "->", mode)
''',
    notes={1: 'Input :: The value of fs.defaultFS from core-site.xml.',
           2: 'Cut :: Everything after <code>//</code>: <code>localhost:9000</code>.',
           3: 'Host :: Everything before the colon.',
           6: 'Decide :: The NameNode is on this same machine.'},
)

WORKED_INTRO = 'Three questions people really answer when choosing or checking a mode: what fits on a laptop, what a one-node cluster risks, and how to check that every node of a real cluster has the same configuration. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Learning · resources', title='Can my laptop run pseudo-distributed mode?',
         problem='<p>In pseudo-distributed mode, give each of the five daemons 1 GB of heap, keep 2 GB for the operating system and the WSL/IDE, and allow 1 GB per task container. For laptops with 8 GB and 16 GB of RAM, how many containers can run at once?</p>',
         inp='5 daemons × 1 GB · OS 2 GB · 1 GB per container · 8 GB and 16 GB',
         approach=['Fixed memory = daemons + OS.',
                   'Free memory = RAM − fixed.',
                   'Containers = whole GB left.'],
         code='''daemons, heap, os_gb, per_container = 5, 1, 2, 1
for ram in [8, 16]:
    free = ram - daemons * heap - os_gb
    print(f"{ram} GB laptop: {free} GB free -> {free // per_container} container(s) at once")
''', notes={3: 'Fixed :: 5 × 1 + 2 = 7 GB used before any job.'},
         tryit='With 8 GB, only one container fits, and every MapReduce job needs one for its ApplicationMaster, so no map task could start and the job would wait. Small heaps (512 MB) help on 8 GB machines.'),
    dict(level='i', tag='Risk · data safety', title='What does replication 1 really risk?',
         problem='<p>A team keeps 2 TB of test data on a pseudo-distributed node (replication 1, one disk). Assume a disk has a 2% chance of failing in a year. Compare the chance of losing data within a year with a 3-node cluster at replication 3, assuming failures are independent and a failed disk is replaced and re-replicated within a day.</p>',
         inp='2% yearly disk failure · one disk vs three copies · repair within 1 day',
         approach=['One copy: data is lost if that one disk fails: 2%.',
                   'Three copies: all three must fail within the same day of repair. Per-day failure chance = 2% / 365.',
                   'Approximate: first failure (about 3 × 2% in a year), then both others fail the same day.'],
         code='''p_year = 0.02
p_day = p_year / 365
one_copy = p_year
three_copies = 3 * p_year * (p_day ** 2)
print(f"replication 1: {one_copy:.2%} chance of loss per year")
print(f"replication 3: {three_copies:.8%} chance of loss per year")
print(f"about {one_copy / three_copies:,.0f} times safer")
''', notes={4: 'Model :: A rough estimate: a first failure, then two more within the repair window.'},
         tryit='This simple model ignores racks, correlated failures and slow repairs, which make real numbers worse. It still shows why production never uses replication 1 for data that matters.'),
    dict(level='a', tag='Admin · consistency', title='Do all nodes have the same configuration?',
         problem='<p>In fully distributed mode, every node must have the same core settings. A script collected <code>fs.defaultFS</code> and <code>dfs.replication</code> from four nodes. Find the nodes that differ from the majority.</p>',
         inp='nn1, dn1, dn3: hdfs://nn1:8020, 3 · dn2: hdfs://localhost:9000, 1',
         approach=['Build one key per node from the settings.',
                   'Count how many nodes share each key; the most common is the expected one.',
                   'Report every node whose key differs.'],
         code='''from collections import Counter
nodes = {"nn1": ("hdfs://nn1:8020", "3"), "dn1": ("hdfs://nn1:8020", "3"),
         "dn2": ("hdfs://localhost:9000", "1"), "dn3": ("hdfs://nn1:8020", "3")}
expected, count = Counter(nodes.values()).most_common(1)[0]
print("expected:", expected, f"({count} of {len(nodes)} nodes)")
for name, conf in nodes.items():
    if conf != expected:
        print("MISMATCH on", name, "->", conf)
''', notes={4: 'Majority :: <code>most_common(1)</code> returns the most frequent settings and their count.'},
         tryit='dn2 still has a pseudo-distributed config, so its DataNode would look for a NameNode on itself and never join. Cluster managers prevent this by pushing one configuration to every node.'),
]

QUIZ = mix([
    dict(q='After simply unpacking Hadoop and running an example job, which mode is it in?', options=['Fully distributed', 'Pseudo-distributed', 'Standalone (local)', 'High availability'], answer=2,
         why='With no configuration, fs.defaultFS is file:/// and mapreduce.framework.name is local: one JVM, local files.'),
    dict(q='Which setting most directly separates standalone from the other two modes?', options=['dfs.blocksize', 'fs.defaultFS', 'yarn.nodemanager.resource.memory-mb', 'hadoop.tmp.dir'], answer=1,
         why='file:/// means local files (standalone). hdfs://host:port means HDFS, as in pseudo and fully distributed modes.'),
    dict(q='In pseudo-distributed mode, how are the daemons run?', options=['All inside one JVM', 'Each daemon in its own JVM, all on one machine', 'On separate machines', 'Inside the browser'], answer=1,
         why='That is what makes it a real (one-node) cluster: NameNode, DataNode, ResourceManager and so on are separate processes.'),
    dict(q='Why is dfs.replication set to 1 in pseudo-distributed mode?', options=['To make it faster', 'There is only one DataNode, so a block cannot have more than one copy', 'Replication is not supported there', 'To save NameNode memory'], answer=1,
         why='With the default of 3 and only one DataNode, every block would be under-replicated.'),
    dict(q='In standalone mode, what does hadoop fs -ls / list?', options=['The HDFS root folder', 'The Linux root folder (/bin, /etc, /home …)', 'Nothing: it fails', 'The YARN queues'], answer=1,
         why='The default file system is the local one, so “/” is the Linux root.'),
    dict(q='Which mode is used for production clusters?', options=['Standalone', 'Pseudo-distributed', 'Fully distributed', 'Any of them'], answer=2,
         why='Only fully distributed mode spreads data and work over many machines and survives node failures.'),
    dict(q='What does the workers file contain in fully distributed mode?', options=['User names', 'One worker host name per line', 'Block IDs', 'The NameNode password'], answer=1,
         why='start-dfs.sh and start-yarn.sh read it to start DataNodes and NodeManagers on those hosts.'),
    dict(q='Which mode needs no SSH at all?', options=['Standalone', 'Pseudo-distributed', 'Fully distributed', 'All need SSH'], answer=0,
         why='Standalone starts no daemons, so the start scripts (which use SSH) are not used.'),
])

REVISION = [
    '<b>Standalone</b>: default; one JVM; local files (<code>file:///</code>); no daemons; for debugging.',
    '<b>Pseudo-distributed</b>: all daemons on one machine, each its own JVM; HDFS + YARN; replication 1; for learning.',
    '<b>Fully distributed</b>: masters and workers on separate machines; replication 3; for production.',
    'Mode settings: <code>fs.defaultFS</code>, <code>mapreduce.framework.name</code>, <code>dfs.replication</code>, <code>workers</code> file.',
    'Pseudo: <code>hdfs://localhost:9000</code>; fully: <code>hdfs://&lt;namenode-host&gt;:8020</code>.',
    'Check with <code>jps</code> and <code>hdfs getconf -confKey fs.defaultFS</code>.',
    '<code>hdfs namenode -format</code> once per new cluster: it wipes the namespace.',
    'Docker Compose gives a fully distributed cluster on one PC: each container is a node.',
]
FAQ = [
    ('What are the modes of Hadoop?', 'Standalone (local) mode: a single JVM with the local file system and no daemons, used for debugging. Pseudo-distributed mode: all Hadoop daemons run on one machine in separate JVMs with HDFS and YARN, used for learning and testing. Fully distributed mode: daemons run on separate master and worker machines, used in production.'),
    ('What is the default mode of Hadoop?', 'Standalone (local) mode. Without configuration, fs.defaultFS is file:/// and mapreduce.framework.name is local.'),
    ('What is the difference between standalone and pseudo-distributed mode?', 'Standalone runs everything inside one Java process on local files, with no HDFS or YARN. Pseudo-distributed runs the real daemons (NameNode, DataNode, ResourceManager, NodeManager…) as separate processes on one machine, so jobs use HDFS and YARN just as on a cluster.'),
    ('Which configuration files change between modes?', 'core-site.xml (fs.defaultFS), hdfs-site.xml (dfs.replication and storage folders), mapred-site.xml (mapreduce.framework.name=yarn) and yarn-site.xml (ResourceManager host, shuffle service), plus the workers file for fully distributed mode.'),
    ('Can I run fully distributed mode on one laptop?', 'Yes, with containers or virtual machines: each container or VM is a separate node with its own host name and IP. The Docker practice cluster in Lesson 4.3 does exactly this.'),
    ('Why do I need to format the NameNode?', 'Formatting creates an empty HDFS namespace (the fsimage and a new cluster ID) in the NameNode\'s storage folder. It is done once when creating a cluster; formatting again erases the namespace and makes existing DataNodes incompatible.'),
    ('Is pseudo-distributed mode fault tolerant?', 'No. There is one DataNode and one copy of each block, so a disk failure loses data and a crash stops everything.'),
]

PRACTICE_INTRO = 'Short exercises on reading settings, counting daemons and checking configurations, all runnable in the browser.'
PROBLEMS = [
    dict(level='easy', title='Local or HDFS?', stmt='For each fs.defaultFS value, print "local files" or "HDFS".', inp='file:/// · hdfs://localhost:9000 · hdfs://namenode',
         code='''for fs in ["file:///", "hdfs://localhost:9000", "hdfs://namenode"]:
    print(fs, "->", "local files" if fs.startswith("file:") else "HDFS")
''', explain='Only file:/// is the local disk; both hdfs:// values use HDFS.'),
    dict(level='easy', title='Port or default?', stmt='Print the NameNode port for hdfs://localhost:9000 and hdfs://namenode (the default RPC port is 8020).', inp='hdfs://localhost:9000 · hdfs://namenode',
         code='''for fs in ["hdfs://localhost:9000", "hdfs://namenode"]:
    hostport = fs.split("//")[1]
    port = hostport.split(":")[1] if ":" in hostport else "8020"
    print(fs, "-> port", port)
''', explain='9000 is written explicitly in the pseudo setup; without a port, Hadoop uses 8020.'),
    dict(level='easy', title='Name the daemons', stmt='Given the jps output of a pseudo-distributed machine, list the daemons (skip Jps itself).', inp='5584 SecondaryNameNode · 5283 NameNode · 6567 Jps · 6120 ResourceManager · 5384 DataNode · 6221 NodeManager',
         code='''jps = """5584 SecondaryNameNode
5283 NameNode
6567 Jps
6120 ResourceManager
5384 DataNode
6221 NodeManager"""
names = sorted(line.split()[1] for line in jps.splitlines() if not line.endswith(" Jps"))
print(len(names), "daemons:", ", ".join(names))
''', explain='5 daemons: DataNode, NameNode, NodeManager, ResourceManager, SecondaryNameNode (the real jps output from Part 4).'),
    dict(level='medium', title='Guess the mode from jps', stmt='Write a function that guesses the mode from the set of daemons on a machine: none → standalone; NameNode and DataNode together → pseudo-distributed; otherwise → part of a fully distributed cluster.', inp='{} · {NameNode, DataNode, …} · {DataNode, NodeManager}',
         code='''def guess(daemons):
    if not daemons:
        return "standalone"
    if {"NameNode", "DataNode"} <= daemons:
        return "pseudo-distributed"
    return "node of a fully distributed cluster"
for d in [set(), {"NameNode", "DataNode", "ResourceManager"}, {"DataNode", "NodeManager"}]:
    print(sorted(d), "->", guess(d))
''', explain='A worker of a real cluster runs only DataNode and NodeManager; seeing the NameNode and a DataNode together on one machine suggests pseudo mode (small real clusters sometimes do this too, so check fs.defaultFS).'),
    dict(level='medium', title='Raw disk for 3 copies', stmt='A team will store 4 TB of data. How much raw disk is needed with replication 1 (pseudo) and replication 3 (fully), keeping 25% of the disk free?', inp='4 TB · replication 1 and 3 · 25% free',
         code='''data = 4
for repl in [1, 3]:
    raw = data * repl / 0.75
    print(f"replication {repl}: {raw:.1f} TB raw disk")
''', explain='About 5.3 TB with one copy and 16 TB with three. Replication triples the disk you buy.'),
    dict(level='medium', title='Pseudo to fully: what to change', stmt='Given a pseudo-distributed configuration, produce the fully distributed one for a NameNode host nn1 and 3 workers.', inp='fs.defaultFS=hdfs://localhost:9000 · dfs.replication=1 · workers=localhost',
         code='''pseudo = {"fs.defaultFS": "hdfs://localhost:9000", "dfs.replication": "1", "workers": ["localhost"]}
fully = dict(pseudo)
fully["fs.defaultFS"] = "hdfs://nn1:8020"
fully["dfs.replication"] = "3"
fully["workers"] = ["worker1", "worker2", "worker3"]
for k in pseudo:
    print(f"{k:16}: {pseudo[k]}  ->  {fully[k]}")
''', explain='Three things change: the NameNode address, the replication factor and the workers list. The same files are then copied to every node.'),
    dict(level='business', title='Time saved by testing locally first', stmt='A developer\'s job has a bug found only after 3 attempts. Each cluster attempt takes 15 minutes (queue + run); a local-mode attempt on sample data takes 1 minute. How much time does testing locally first save if the 3 failing attempts are local and only the final run uses the cluster?', inp='3 failed attempts · 15 min on cluster · 1 min local · 1 final cluster run',
         code='''cluster_only = 4 * 15
local_first = 3 * 1 + 15
print(f"cluster only {cluster_only} min, local first {local_first} min, saved {cluster_only - local_first} min")
''', explain='60 minutes against 18: 42 minutes saved per bug, and the shared cluster is not wasted on broken jobs.'),
    dict(level='advanced', title='Find the misconfigured worker', stmt='Workers report the NameNode address they use. List the workers that will not join the cluster whose NameNode is hdfs://nn1:8020.', inp='w1: hdfs://nn1:8020 · w2: hdfs://localhost:9000 · w3: hdfs://nn1:8020 · w4: file:///',
         code='''expected = "hdfs://nn1:8020"
workers = {"w1": "hdfs://nn1:8020", "w2": "hdfs://localhost:9000",
           "w3": "hdfs://nn1:8020", "w4": "file:///"}
bad = [w for w, fs in workers.items() if fs != expected]
print("will not join:", bad)
''', explain='w2 looks for a NameNode on itself and w4 has no HDFS setting at all (standalone defaults), so neither registers with nn1.'),
]

SCN_INTRO = 'Interviewers use the modes to check whether you understand what a cluster really is, not just the names.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Learning · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“My job ran, so my Hadoop cluster works”</h4>
      <p class="scn__situation">A fresher says they installed Hadoop and ran the example job successfully. When asked, jps shows only “Jps”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you tell standalone mode from a real cluster?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The job ran in standalone mode: one JVM, local files, no HDFS or YARN.</li>
          <li>Proof: no daemons in <code>jps</code>, and <code>hdfs getconf -confKey fs.defaultFS</code> prints <code>file:///</code>.</li>
          <li>For a one-node cluster, set <code>fs.defaultFS=hdfs://localhost:9000</code>, <code>dfs.replication=1</code>, YARN settings, format the NameNode, then <code>start-dfs.sh</code> and <code>start-yarn.sh</code>.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · HDFS</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Every block is under-replicated on the test machine</h4>
      <p class="scn__situation">On a single-machine setup, <code>hdfs fsck /</code> reports all blocks as under-replicated.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you connect replication to the number of DataNodes?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Replication is probably still the default 3 while there is only one DataNode.</li>
          <li>Set <code>dfs.replication=1</code> in <code>hdfs-site.xml</code> for new files, and change existing files with <code>hdfs dfs -setrep -w 1 /path</code>.</li>
          <li>Explain that this is only acceptable for test data: one copy means no protection.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · cluster build</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A new DataNode never appears in the NameNode UI</h4>
      <p class="scn__situation">You add a fourth worker to a fully distributed cluster. Its DataNode process is running, but the NameNode still shows 3 live DataNodes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> a systematic check of configuration and connectivity.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>On the new node, check <code>hdfs getconf -confKey fs.defaultFS</code>: a leftover <code>localhost</code> value (pseudo config) is common.</li>
          <li>Check that the NameNode host name resolves and port 8020 is reachable from the worker.</li>
          <li>Read the DataNode log in <code>$HADOOP_HOME/logs</code> for errors such as “Incompatible clusterIDs” (an old data folder from another cluster).</li>
          <li>Make sure the host is in the <code>workers</code> file (and in any include file) and the configuration is the same as on other nodes.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Engineering · testing</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Which mode would you use for which stage?</h4>
      <p class="scn__situation">A team lead asks how you would test a new MapReduce job before it runs on the production cluster.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know the purpose of each mode?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Unit tests in local mode on small samples: fast feedback on logic.</li>
          <li>Integration tests on a one-node or mini cluster: real HDFS and YARN APIs, file formats and configuration.</li>
          <li>A run on a fully distributed test cluster with realistic data size, then production.</li>
          <li>Each stage catches different problems: logic, integration, then scale and performance.</li>
        </ul>
      </div></details>
    </article>
'''
