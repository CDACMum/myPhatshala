import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Spot the daemons',
    intro='<p>The boxes at the top are master daemons; each DataNode box is a worker that also runs a NodeManager (its two container bars).</p>',
    racks=2, nodes=3, features=['upload', 'job', 'ha'],
    preload=[dict(name='app_logs.json', sizeMB=1024)],
    **{'try': [
        dict(text='Find the <b>NameNode</b> (HDFS master) and the <b>ResourceManager</b> (YARN master). Which one shows the file count?'),
        dict(text='Upload a file: the client talks to the NameNode for <i>where</i>, but the data packets go straight to DataNodes.', on='upload-done'),
        dict(text='Run the job: containers (green bars) appear inside the workers\' NodeManagers.', on='job-done'),
        dict(text='Stop the active NameNode: the ZKFC + standby pair takes over.', on='nn-failover'),
    ]},
)))

META = dict(
    module='03-how-a-cluster-works', lesson='01-hadoop-architecture-hdfs-yarn-mapreduce-and-common', n='3.1',
    module_label='Module 3 · How one Hadoop cluster works',
    title='Hadoop architecture: HDFS, YARN, MapReduce and Common',
    desc='Hadoop\'s layered architecture daemon by daemon: NameNode, DataNode, Secondary NameNode, JournalNodes, ZKFC, ResourceManager, NodeManager, ApplicationMaster and JobHistory Server, where each runs, how they talk, their Hadoop 3 default ports, and the four configuration files. With a start-up animation, a playground, Python you can run, quiz and interview scenarios.',
    og_desc='Hadoop is a team of Java daemons. Meet each one, its job, its port and the config file that controls it.',
    minutes=26, level='Beginner → Advanced',
    lead='Hadoop is not one program. It is a team of long-running Java processes, called daemons, spread across master and worker machines, held together by four XML configuration files. This lesson opens up a real cluster layer by layer: which daemon runs where, what it does, how it talks to the others and on which port, so that the output of <code>jps</code> and the web UIs make sense at a glance.',
    chips=['Daemon and port table', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Read a Hadoop configuration file',
    intro='<p>Every Hadoop setting lives in XML files like this <code>hdfs-site.xml</code>. This program reads it the way Hadoop does and turns it into a dictionary. Then try the challenges: find the NameNode, plan which daemons go on which host, and catch a configuration mistake.</p>',
    code='''import xml.etree.ElementTree as ET

hdfs_site = """<configuration>
  <property><name>dfs.replication</name><value>3</value></property>
  <property><name>dfs.namenode.name.dir</name><value>/data/nn</value></property>
  <property><name>dfs.datanode.data.dir</name><value>/data/1/dn,/data/2/dn</value></property>
  <property><name>dfs.blocksize</name><value>134217728</value></property>
</configuration>"""

conf = {p.findtext("name"): p.findtext("value")
        for p in ET.fromstring(hdfs_site).iter("property")}

print("Replication :", conf["dfs.replication"])
print("Block size  :", int(conf["dfs.blocksize"]) // 1024 // 1024, "MB")
print("DataNode disks:", conf["dfs.datanode.data.dir"].split(","))
''',
    anno=[
        ('ET.fromstring(hdfs_site).iter("property")', 'Parse the XML and visit every <code>&lt;property&gt;</code> element, as Hadoop\'s <code>Configuration</code> class does.'),
        ('conf = {p.findtext("name"): p.findtext("value") ...}', 'A dictionary comprehension: property name → value. All values are strings.'),
        ('int(conf["dfs.blocksize"]) // 1024 // 1024', '134217728 bytes = 128 MB, the Hadoop 2/3 default.'),
    ],
    tasks=[
        dict(label='1 · Read hdfs-site.xml', hint='Press <b>Run</b>. Then change the replication to 2 and add a third data directory.', code=None),
        dict(label='2 · Where is the NameNode?', hint='<b>Predict first:</b> what host and port does this <code>fs.defaultFS</code> point to? Change it to <code>hdfs://localhost:9000</code> (common in tutorials).',
             code='''from urllib.parse import urlparse
default_fs = "hdfs://nn1.tiffingo.in:8020"
u = urlparse(default_fs)
print("scheme:", u.scheme, "| NameNode host:", u.hostname, "| RPC port:", u.port)
'''),
        dict(label='3 · Which daemons on which host?', hint='Build the expected <code>jps</code> list for each host from its roles. Add an HA master with "journalnode".',
             code='''daemons = {"hdfs-master": ["NameNode", "SecondaryNameNode"],
           "yarn-master": ["ResourceManager"], "history": ["JobHistoryServer"],
           "worker": ["DataNode", "NodeManager"]}
hosts = {"master1": ["hdfs-master", "yarn-master", "history"],
         "w1": ["worker"], "w2": ["worker"]}
for host, roles in hosts.items():
    print(host, "->", [d for r in roles for d in daemons[r]])
'''),
        dict(label='4 · Is anything missing?', hint='Compare what should run with what <code>jps</code> shows on each worker. Then make w3 healthy.',
             code='''expected = {"DataNode", "NodeManager"}
jps = {"w1": {"DataNode", "NodeManager"}, "w2": {"DataNode"}, "w3": set()}
for host, running in jps.items():
    missing = expected - running
    print(host, "OK" if not missing else f"MISSING {sorted(missing)}")
'''),
        dict(label='5 · Spot the error', hint='This tries to compute the block size in MB but crashes. All configuration values are strings. Fix it.',
             expect='error',
             code='''conf = {"dfs.blocksize": "134217728", "dfs.replication": "3"}
print(conf["dfs.blocksize"] / 1024 / 1024, "MB")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Merging configuration files, one line at a time',
    intro='<p>Hadoop loads default settings first and then the site files, so later files override earlier ones. Watch the <code>conf</code> dictionary change as each layer is applied.</p>',
    code='''defaults = {"dfs.replication": "3", "dfs.blocksize": "134217728"}
site = {"dfs.replication": "2"}
job = {"dfs.blocksize": "268435456"}

conf = {}
for layer in [defaults, site, job]:
    conf.update(layer)
print(conf)
''',
    notes={1: 'Defaults :: Built into Hadoop (hdfs-default.xml).', 2: 'Site :: The cluster\'s own hdfs-site.xml.', 3: 'Job :: A setting passed for one job, e.g. <code>-D dfs.blocksize=…</code>.'},
)

WORKED_INTRO = 'Three tasks a new platform engineer is given in the first week: audit which daemons run where, check a cluster\'s port plan, and size the master\'s memory. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Operations · health check', title='Which nodes are missing a daemon?',
         problem='<p>A script collects <code>jps</code> output from every node. Masters must run NameNode and ResourceManager; workers must run DataNode and NodeManager. Print each node\'s missing daemons.</p>',
         inp='master1: NameNode, ResourceManager · w1: DataNode, NodeManager · w2: DataNode · w3: NodeManager',
         approach=['Store the expected daemons per role as sets.',
                   'For each node, subtract what is running from what is expected.',
                   'Print the node only if something is missing.'],
         code='''expected = {"master": {"NameNode", "ResourceManager"}, "worker": {"DataNode", "NodeManager"}}
nodes = {"master1": ("master", {"NameNode", "ResourceManager"}),
         "w1": ("worker", {"DataNode", "NodeManager"}),
         "w2": ("worker", {"DataNode"}),
         "w3": ("worker", {"NodeManager"})}
for name, (role, running) in nodes.items():
    missing = expected[role] - running
    if missing:
        print(name, "missing", sorted(missing))
''', notes={7: 'Check :: Set difference: expected minus running.'},
         tryit='w2 has no NodeManager: it stores data but runs no tasks, so jobs reading its blocks lose locality. w3 has no DataNode: its blocks are unavailable. Which is more urgent?'),
    dict(level='i', tag='Security · firewall plan', title='Which ports must be open on each kind of node?',
         problem='<p>Using the Hadoop 3 default ports, print the ports each kind of node must open: an HDFS+YARN master and a worker. Mark web UIs separately so security can restrict them to the admin network.</p>',
         inp='master daemons: NameNode, ResourceManager · worker daemons: DataNode, NodeManager',
         approach=['Map each daemon to its ports, tagging web UIs.',
                   'For each node type, collect the ports of its daemons.',
                   'Print service ports and web UI ports separately.'],
         code='''ports = {"NameNode": [(8020, "rpc"), (9870, "web")],
         "ResourceManager": [(8030, "rpc"), (8031, "rpc"), (8032, "rpc"), (8088, "web")],
         "DataNode": [(9866, "data"), (9867, "rpc"), (9864, "web")],
         "NodeManager": [(8042, "web"), (13562, "shuffle")]}
for node, ds in {"master": ["NameNode", "ResourceManager"], "worker": ["DataNode", "NodeManager"]}.items():
    svc = sorted(p for d in ds for p, kind in ports[d] if kind != "web")
    web = sorted(p for d in ds for p, kind in ports[d] if kind == "web")
    print(f"{node:6}: service {svc} | web UI {web}")
''', notes={5: 'Plan :: One line per node type.'},
         tryit='Add the JournalNode (8485 rpc, 8480 web) to the master list for an HA cluster.'),
    dict(level='a', tag='Capacity · NameNode', title='How much heap does the NameNode need?',
         problem='<p>A common rule of thumb is that the NameNode needs roughly <b>1 GB of heap per million</b> files, directories and blocks, plus headroom. A cluster has <b>40 million files</b> averaging <b>1.5 blocks</b> each and <b>3 million directories</b>. Estimate the heap, add 30% headroom, and round up to the next 8 GB.</p>',
         inp='40 M files × 1.5 blocks · 3 M directories · ~1 GB per million objects · +30%',
         approach=['Objects = files + blocks + directories.',
                   'Heap ≈ objects in millions × 1 GB.',
                   'Add 30%, then round up to a multiple of 8 GB.'],
         code='''import math
files, dirs = 40_000_000, 3_000_000
blocks = files * 1.5
objects_m = (files + blocks + dirs) / 1e6
heap = objects_m * 1.0 * 1.3
print(f"Objects: {objects_m:.0f} million")
print(f"Heap with headroom: {heap:.0f} GB -> set {math.ceil(heap / 8) * 8} GB")
''', notes={4: 'Objects :: Every file, directory and block is an object in NameNode memory.'},
         tryit='If the same data were stored in files 10 times bigger (4 million files), how much heap would be needed? This is why the small-files problem is really a NameNode-memory problem.'),
]

QUIZ = mix([
    dict(q='Which daemon stores the HDFS namespace and the location of every block?', options=['DataNode', 'NameNode', 'NodeManager', 'JobHistory Server'], answer=1,
         why='The <b>NameNode</b> holds all file-system metadata in memory. DataNodes store the blocks themselves.'),
    dict(q='Which two daemons normally run on every worker node?', options=['NameNode and ResourceManager', 'DataNode and NodeManager', 'JournalNode and ZKFC', 'JobHistory Server and ZooKeeper'], answer=1,
         why='A worker stores blocks (<b>DataNode</b>) and runs containers (<b>NodeManager</b>), which makes data locality possible.'),
    dict(q='Which configuration property tells clients where the NameNode is?', options=['dfs.replication', 'fs.defaultFS in core-site.xml', 'yarn.resourcemanager.hostname', 'mapreduce.framework.name'], answer=1,
         why='<code>fs.defaultFS</code>, for example <code>hdfs://nn1:8020</code>, sets the default file system for every client and daemon.'),
    dict(q='When a client reads a file from HDFS, where does the data come from?', options=['Through the NameNode', 'Directly from the DataNodes that hold the blocks', 'From the ResourceManager', 'From ZooKeeper'], answer=1,
         why='The NameNode only returns block locations; the bytes come straight from DataNodes. Masters stay out of the data path.'),
    dict(q='On Hadoop 3, the YARN ResourceManager web UI is by default on port:', options=['9870', '8088', '50070', '19888'], answer=1,
         why='<b>8088</b> (unchanged since Hadoop 2). 9870 is the NameNode UI, 19888 the JobHistory UI.'),
    dict(q='What does the JobHistory Server do?', options=['Runs MapReduce tasks', 'Keeps counters, logs and details of finished MapReduce jobs', 'Stores HDFS blocks', 'Elects the active NameNode'], answer=1,
         why='Once a job\'s ApplicationMaster exits, the <b>JobHistory Server</b> is where you see its history (web UI on 19888).'),
    dict(q='Which setting enables the MapReduce shuffle service inside each NodeManager?', options=['dfs.replication', 'yarn.nodemanager.aux-services = mapreduce_shuffle', 'fs.defaultFS', 'mapreduce.job.reduces'], answer=1,
         why='Without the <code>mapreduce_shuffle</code> aux service, reducers cannot fetch map outputs and MapReduce jobs fail.'),
    dict(q='Which command lists the Hadoop daemons running on the current machine?', options=['hdfs dfs -ls', 'jps', 'yarn top', 'hadoop version'], answer=1,
         why='<code>jps</code> (from the JDK) lists running Java processes by class name: NameNode, DataNode, NodeManager…'),
])

REVISION = [
    'Hadoop = a team of Java <b>daemons</b>, not one program.',
    'HDFS: <b>NameNode</b> (metadata, 8020 RPC, 9870 UI) + <b>DataNodes</b> (blocks, 9866/9867/9864).',
    'HA helpers: <b>JournalNodes</b> (8485), <b>ZKFC</b> (8019), <b>ZooKeeper</b> (2181). Non-HA: Secondary NameNode (9868).',
    'YARN: <b>ResourceManager</b> (8032/8030/8031, UI 8088) + <b>NodeManagers</b> (UI 8042, shuffle 13562).',
    'MapReduce: one <b>ApplicationMaster</b> per job in a container; <b>JobHistory Server</b> (19888) for finished jobs.',
    'Worker = DataNode + NodeManager (locality). Masters stay out of the data path.',
    'Config: <code>core-site.xml</code> (fs.defaultFS), <code>hdfs-site.xml</code>, <code>yarn-site.xml</code>, <code>mapred-site.xml</code>, <code>workers</code>.',
    'Start order: <code>start-dfs.sh</code> → safe mode exit → <code>start-yarn.sh</code> → history server. Check with <code>jps</code>.',
]
FAQ = [
    ('What are the daemons in a Hadoop cluster?', 'HDFS: NameNode, DataNodes, and either a Secondary NameNode (non-HA) or a standby NameNode with JournalNodes and ZKFailoverControllers (HA). YARN: ResourceManager and NodeManagers (optionally a Timeline Server). MapReduce: a per-job MRAppMaster running in a container and the JobHistory Server. ZooKeeper is a separate service used for HA.'),
    ('Why does the NameNode not handle file data?', 'Keeping the master out of the data path means it only answers small metadata requests (open, create, block locations), while the large data transfers happen directly between clients and DataNodes in parallel. This lets one NameNode serve thousands of DataNodes without becoming a bandwidth bottleneck.'),
    ('What is in core-site.xml, hdfs-site.xml, yarn-site.xml and mapred-site.xml?', 'core-site.xml: settings shared by all components, most importantly fs.defaultFS. hdfs-site.xml: HDFS settings such as dfs.replication, dfs.blocksize, NameNode and DataNode directories, HA settings. yarn-site.xml: ResourceManager address, NodeManager resources, aux-services, scheduler. mapred-site.xml: mapreduce.framework.name=yarn and MapReduce tuning such as memory and the number of reducers.'),
    ('How do you check whether Hadoop daemons are running?', 'Run jps on each node to see the Java processes; use hdfs dfsadmin -report for live and dead DataNodes; yarn node -list for NodeManagers; and open the web UIs (NameNode 9870, ResourceManager 8088). If a daemon is missing, read its log in $HADOOP_HOME/logs.'),
    ('Why do DataNode and NodeManager run on the same machine?', 'So that tasks launched by the NodeManager can read blocks stored by the local DataNode. This co-location is what makes data locality, and therefore Hadoop\'s performance, possible.'),
]

PRACTICE_INTRO = 'Small programs about daemons, ports and configuration: the things you check every day on a real cluster.'
PROBLEMS = [
    dict(level='easy', title='Port to service', stmt='Given a port number, print which Hadoop 3 service uses it. Test with 9870, 8088 and 19888.', inp='[9870, 8088, 19888]',
         code='''service = {9870: "NameNode web UI", 8088: "ResourceManager web UI", 19888: "JobHistory web UI",
           8020: "NameNode RPC", 9864: "DataNode web UI"}
for p in [9870, 8088, 19888]:
    print(p, "->", service[p])
''', explain='Memorise these five ports: they come up in every installation and troubleshooting session.'),
    dict(level='easy', title='Count daemons in a cluster', stmt='A cluster has 2 master nodes (each running 3 daemons) and 40 workers (each running 2). How many daemon processes in total?', inp='2 × 3 + 40 × 2',
         code='print(2 * 3 + 40 * 2, "daemons")\n', explain='86 long-running processes, each with its own log file and memory settings.'),
    dict(level='easy', title='Block size from bytes', stmt='Convert the dfs.blocksize values 134217728 and 268435456 to MB.', inp='["134217728", "268435456"]',
         code='''for v in ["134217728", "268435456"]:
    print(v, "=", int(v) // (1024 * 1024), "MB")
''', explain='128 MB and 256 MB. Hadoop also accepts values like <code>128m</code> or <code>256m</code> in configuration.'),
    dict(level='medium', title='Parse fs.defaultFS', stmt='From these fs.defaultFS values, print host and port. If no port is given, HDFS uses 8020.', inp='["hdfs://nn1:8020", "hdfs://localhost:9000", "hdfs://mycluster"]',
         code='''from urllib.parse import urlparse
for v in ["hdfs://nn1:8020", "hdfs://localhost:9000", "hdfs://mycluster"]:
    u = urlparse(v)
    print(v, "->", u.hostname, u.port or 8020)
''', explain='<code>hdfs://mycluster</code> with no port is how HA clusters are addressed: <code>mycluster</code> is a logical name that maps to both NameNodes in hdfs-site.xml.'),
    dict(level='medium', title='Override order', stmt='Apply configuration layers in order (defaults, site, job) and print the final replication and block size.', inp='defaults {repl 3, block 128m} · site {repl 2} · job {block 256m}',
         code='''layers = [{"dfs.replication": "3", "dfs.blocksize": "128m"},
          {"dfs.replication": "2"},
          {"dfs.blocksize": "256m"}]
conf = {}
for layer in layers:
    conf.update(layer)
print(conf)
''', explain='Later layers win. Administrators can mark a property <code>&lt;final&gt;true&lt;/final&gt;</code> in site files so jobs cannot override it.'),
    dict(level='medium', title='Live vs dead DataNodes', stmt='Given each DataNode\'s seconds since last heartbeat, print live and dead counts using the 630-second rule.', inp='{dn1: 2, dn2: 700, dn3: 1, dn4: 640, dn5: 3}',
         code='''last = {"dn1": 2, "dn2": 700, "dn3": 1, "dn4": 640, "dn5": 3}
dead = [n for n, s in last.items() if s > 630]
print("Live:", len(last) - len(dead), "| Dead:", len(dead), dead)
''', explain='This is the number at the top of the NameNode web UI and of <code>hdfs dfsadmin -report</code>.'),
    dict(level='business', title='Memory budget for a worker', stmt='A worker has 256 GB RAM. Reserve 8 GB for the OS, 4 GB for the DataNode and 2 GB for the NodeManager. How much can YARN offer to containers, and how many 4 GB containers fit?', inp='256 GB · OS 8 · DN 4 · NM 2 · containers 4 GB',
         code='''total, os_gb, dn, nm = 256, 8, 4, 2
yarn_gb = total - os_gb - dn - nm
print("yarn.nodemanager.resource.memory-mb =", yarn_gb * 1024)
print("4 GB containers per node:", yarn_gb // 4)
''', explain='242 GB for YARN, 60 containers of 4 GB. Giving YARN all the memory starves the daemons and the OS; Module 11 covers tuning.'),
    dict(level='business', title='Master heap budget', stmt='The NameNode needs about 1 GB per million objects. The cluster has 120 million objects and grows 25% a year. What heap is needed now and in 2 years (with 30% headroom)?', inp='120 M objects · +25%/year · +30%',
         code='''objects_m = 120
for year in [0, 2]:
    need = objects_m * 1.25 ** year * 1.3
    print(f"Year {year}: ~{need:.0f} GB NameNode heap")
''', explain='About 156 GB now and 244 GB in two years. Very large heaps make Java garbage collection pauses longer, one reason teams use federation or compact small files.'),
]

SCN_INTRO = 'Architecture questions in interviews are usually practical: what runs where, how they talk, and what you check when something breaks.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Jobs never use one of the workers</h4>
      <p class="scn__situation">The HDFS UI shows 10 live DataNodes, but the YARN UI shows only 9 active NodeManagers. Jobs never run tasks on worker <code>w7</code>.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know that storage and compute are separate daemons on the same node?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li>On <code>w7</code>, run <code>jps</code>: the DataNode is running but the NodeManager isn't (or it is unhealthy).</li>
          <li>Read the NodeManager log under <code>$HADOOP_HOME/logs</code>: common causes are a wrong <code>yarn.resourcemanager.hostname</code>, a full local disk (marked unhealthy), or a memory setting larger than the machine.</li>
          <li>Fix and start it: <code>yarn --daemon start nodemanager</code>, then confirm with <code>yarn node -list</code>.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> restarting the whole cluster for one missing daemon.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Does all data go through the NameNode?”</h4>
      <p class="scn__situation">The interviewer says: “If the NameNode is the master, surely every byte you read passes through it, right?”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand why masters stay out of the data path?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No. The client asks the NameNode only for <b>metadata</b>: which blocks make up the file and which DataNodes hold them.</li>
          <li>The client then reads (or writes) the bytes <b>directly</b> from the DataNodes, choosing the closest replica.</li>
          <li>This keeps the NameNode's work small and lets thousands of clients transfer data in parallel. The same is true of YARN: the ResourceManager hands out containers but never touches job data.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> drawing data arrows through the NameNode in an architecture diagram.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · configuration</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Spark on the edge node can't find HDFS</h4>
      <p class="scn__situation">A data scientist installs Spark on a new edge node. <code>spark.read.csv("/data/sales")</code> fails with “File does not exist” even though <code>hdfs dfs -ls /data/sales</code> works on other nodes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know how clients find the cluster?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Spark doesn't know the cluster: without <code>core-site.xml</code>, the default file system is the local disk (<code>file:///</code>), so <code>/data/sales</code> is looked up locally.</li>
          <li>Copy the cluster's <code>core-site.xml</code>, <code>hdfs-site.xml</code> and <code>yarn-site.xml</code> to the edge node and point <code>HADOOP_CONF_DIR</code> (and Spark) at them, or use a full URI like <code>hdfs://nn1:8020/data/sales</code>.</li>
          <li>In a managed cluster, add the node as a “gateway” host so the manager keeps the client configuration in sync.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> copying the data to the edge node.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Infrastructure · design</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Put the NameNode and ResourceManager on one server?</h4>
      <p class="scn__situation">To save money on a new 30-node cluster, someone proposes running the NameNode, ResourceManager, JobHistory Server and also a DataNode on one master server.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand the resource needs and failure impact of master daemons?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>For small clusters, NameNode + ResourceManager + JobHistory on one well-equipped master is common and acceptable.</li>
          <li>But <b>not a DataNode/NodeManager on the master</b>: tasks would compete with the NameNode for memory and disk, and a runaway task could slow or crash the master.</li>
          <li>Separate the masters as the cluster grows (NameNode heap needs grow with files), and add HA (a second master, JournalNodes on three machines) when uptime matters.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> treating master servers like ordinary workers.</p>
      </div></details>
    </article>'''
