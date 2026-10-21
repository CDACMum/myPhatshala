#!/usr/bin/env python3
"""Build the Hadoop course's extra pages: courses/hadoop/playground/ and courses/hadoop/glossary/.
usage: python3 tools/authoring/src/hadoop/extras.py [SITE_ROOT]"""
import os, sys, json, html
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
UP = '../../../'
COLOR = '#B45309'
SITE = 'https://myphatshala.in'


def shell(slug, title, desc, minutes, h1, lead, main, extra_head='', extra_js=''):
    url = f'{SITE}/courses/hadoop/{slug}/'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | MyPhatshala</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)} · MyPhatshala">
<meta property="og:description" content="{E(desc)}">
<link rel="icon" href="{UP}assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{UP}assets/css/style.css">
<link rel="stylesheet" href="{UP}assets/css/lesson.css">
{extra_head}
<script src="{UP}assets/js/config.js"></script>
<script>try {{ const t = localStorage.getItem("mp-theme"); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}</script>
</head>
<body style="--track:{COLOR}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{UP}" aria-label="MyPhatshala home"><img src="{UP}assets/img/logo.svg" width="34" height="34" alt=""><span>My<b>Phatshala</b></span></a>
    <nav class="nav" aria-label="Main">
      <a href="{UP}#tracks">All courses</a>
      <a href="../">Apache Hadoop syllabus</a>
      <button class="theme-btn" id="theme-btn" aria-label="Toggle dark mode"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
    </nav>
  </div>
</header>
<main id="main">
<section class="lesson-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{UP}">Home</a><span>›</span><a href="{UP}#track-big-data">Big Data Engineering</a><span>›</span><a href="../">Apache Hadoop</a><span>›</span><b>{E(h1)}</b></nav>
    <h1>{E(h1)}</h1>
    <p class="lead">{lead}</p>
    <div class="lesson-meta"><span>Apache Hadoop</span><span>⏱ {minutes} min</span><span>Free · no sign-up</span></div>
  </div>
</section>
<div class="wrap" style="padding-top:8px;padding-bottom:40px">
{main}
<div class="ad-slot" data-slot="bottom"></div>
</div>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div><h4>MyPhatshala</h4><p>Free programming and IT lessons that show what happens behind the screen.</p></div>
    <div><h4>Learn</h4><a href="{UP}#tracks">All courses</a><a href="../">Apache Hadoop syllabus</a></div>
    <div><h4>Site</h4><a href="{UP}about.html">About</a><a href="{UP}contact.html">Contact</a><a href="{UP}privacy.html">Privacy policy</a><a href="{UP}disclaimer.html">Disclaimer</a></div>
    <div class="copyright">© MyPhatshala. All lesson content, diagrams and animations are original. Please do not copy without permission.</div>
  </div>
</footer>
{extra_js}
<script src="{UP}assets/js/ads.js"></script>
<script src="{UP}assets/js/site.js"></script>
</body>
</html>
'''


def csim(cfg):
    return '<div class="csim"><script type="application/json">' + json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/') + '</script></div>'


# ------------------------------------------------------------------ playground
PG_MAIN = f'''<div class="ad-slot" data-slot="top"></div>
<section class="part">
  <h2>The full cluster</h2>
  <p>Three racks of three DataNodes, a client (edge node), two NameNodes (active and standby) and a ResourceManager. Everything you can do in the lessons is switched on here. Use the checklist as a guided tour, or just experiment.</p>
  {csim(dict(
    title='Cluster Playground: everything on',
    racks=3, nodes=3,
    features=['upload', 'fail', 'job', 'locality', 'chaos', 'ha', 'fsck'],
    preload=[dict(name='upi_txns_2025.csv', sizeMB=1024)],
    **{'try': [
        dict(text='Upload a 2 GB file with 128 MB blocks. Count the blocks and check that each has copies on two racks.', on='upload-done'),
        dict(text='Run the word count job. Note the data-local count in the Event log.', on='job-done'),
        dict(text='Untick “Move code to data” and run it again. Compare the two runs in <b>Job runs</b>.', on='job-done-nolocal'),
        dict(text='Click a DataNode to stop it, then <b>⏩ Skip to timeout</b> and watch re-replication.', on='rereplicated'),
        dict(text='Press <b>Stop active NameNode</b>. The standby takes over (High Availability).', on='nn-failover'),
        dict(text='Stop a whole rack plus one more node, skip to the timeout and run <b>hdfs fsck /</b>.', on='fsck'),
    ]},
  ))}
</section>
<section class="part">
  <h2>What each part of the picture means</h2>
  <div class="terms">
    <div class="term"><b>Client (edge node)</b><span>Where users run <code>hdfs</code> and <code>hadoop jar</code> commands. Not a DataNode, so the first replica of an upload goes to any node.</span></div>
    <div class="term"><b>NameNode</b><span>The HDFS master. Knows every file, its blocks and where each replica is (the metadata table on the right).</span></div>
    <div class="term"><b>Standby NameNode</b><span>Shown when High Availability is on. Takes over automatically if the active one fails.</span></div>
    <div class="term"><b>ResourceManager</b><span>The YARN master. Hands out containers for map and reduce tasks.</span></div>
    <div class="term"><b>Core switch / ToR switch</b><span>The network. Packets moving between racks pass through the core switch.</span></div>
    <div class="term"><b>DataNode box</b><span>A worker node. Coloured squares are block replicas (number = block of the file). The two bars at the bottom are task containers.</span></div>
    <div class="term"><b>Pink dots</b><span>Heartbeats from DataNodes to the NameNode, every 3 seconds (shown at 1× speed).</span></div>
    <div class="term"><b>Green / amber / red bars</b><span>Map tasks that are node-local / rack-local / off-rack. Violet bars are reducers.</span></div>
  </div>
  <p class="muted">Defaults follow real Hadoop: 128 MB blocks, replication 3, rack-aware placement, heartbeat every 3 seconds, a DataNode declared dead after 10 minutes 30 seconds. Transfer and task times are simplified, and some things that take minutes in a real cluster (such as noticing a lost task) happen immediately here.</p>
</section>
<section class="part">
  <h2>Lessons that use the playground</h2>
  <ul class="plain">
    <li><a href="../01-foundations/01-server-node-rack-and-data-centre/">1.1 Server, node, rack and data centre</a>: the pieces of a cluster</li>
    <li><a href="../01-foundations/02-what-is-a-cluster-masters-and-workers/">1.2 What is a cluster? Masters and workers</a>: break a worker during a job</li>
    <li><a href="../01-foundations/03-scale-out-in-practice/">1.3 Scale out in practice</a>: 3 vs 6 vs 9 nodes</li>
    <li><a href="../01-foundations/04-failures-are-normal/">1.4 Failures are normal</a>: how much can you break?</li>
    <li><a href="../01-foundations/05-move-the-code-not-the-data/">1.5 Move the code, not the data</a>: locality on and off</li>
    <li><a href="../02-why-hadoop/01-the-problem-hadoop-solved/">2.1 The problem Hadoop solved</a>: store, process, survive</li>
    <li><a href="../02-why-hadoop/03-how-hadoop-solved-each-problem/">2.3 How Hadoop solved each problem</a>: test every fix</li>
    <li><a href="../02-why-hadoop/04-hadoop-1-2-and-3-what-changed/">2.4 Hadoop 1, 2 and 3</a>: NameNode failover</li>
    <li><a href="../03-how-a-cluster-works/01-hadoop-architecture-hdfs-yarn-mapreduce-and-common/">3.1 Hadoop architecture</a>: spot the daemons</li>
    <li><a href="../03-how-a-cluster-works/02-the-life-of-a-file-and-a-job-end-to-end/">3.2 The life of a file and a job</a>: follow the Event log</li>
    <li><a href="../03-how-a-cluster-works/03-node-roles-master-worker-edge-and-gateway/">3.3 Node roles</a>: break each role</li>
    <li><a href="../04-setup/02-standalone-pseudo-distributed-and-fully-distributed-modes/">4.2 Standalone, pseudo and fully distributed</a>: one node, then many</li>
    <li><a href="../04-setup/04-configuration-files-and-web-uis/">4.4 Configuration files and web UIs</a>: block size and replication per file</li>
    <li><a href="../05-hdfs-architecture/01-namenode-and-datanode/">5.1 NameNode and DataNode</a>: metadata here, data there</li>
    <li><a href="../05-hdfs-architecture/02-blocks/">5.2 Blocks</a>: same file, different block sizes</li>
    <li><a href="../05-hdfs-architecture/03-replication-and-rack-awareness/">5.3 Replication and rack awareness</a>: replicas across racks</li>
    <li><a href="../05-hdfs-architecture/05-heartbeats-and-block-reports/">5.5 Heartbeats and block reports</a>: silence means dead</li>
  </ul>
</section>'''

# ------------------------------------------------------------------ glossary
# (term, group, meaning html, lesson link or '')
L11 = '../01-foundations/01-server-node-rack-and-data-centre/'
L12 = '../01-foundations/02-what-is-a-cluster-masters-and-workers/'
L13 = '../01-foundations/03-scale-out-in-practice/'
L14 = '../01-foundations/04-failures-are-normal/'
L15 = '../01-foundations/05-move-the-code-not-the-data/'
L21 = '../02-why-hadoop/01-the-problem-hadoop-solved/'
L22 = '../02-why-hadoop/02-from-google-s-papers-to-apache-hadoop/'
L23 = '../02-why-hadoop/03-how-hadoop-solved-each-problem/'
L24 = '../02-why-hadoop/04-hadoop-1-2-and-3-what-changed/'
L31 = '../03-how-a-cluster-works/01-hadoop-architecture-hdfs-yarn-mapreduce-and-common/'
L32 = '../03-how-a-cluster-works/02-the-life-of-a-file-and-a-job-end-to-end/'
L33 = '../03-how-a-cluster-works/03-node-roles-master-worker-edge-and-gateway/'
L34 = '../03-how-a-cluster-works/04-when-not-to-use-hadoop/'
L41 = '../04-setup/01-prerequisites-linux-java-and-ssh/'
L42 = '../04-setup/02-standalone-pseudo-distributed-and-fully-distributed-modes/'
L43 = '../04-setup/03-installing-hadoop-docker-cluster-and-ubuntu-wsl/'
L44 = '../04-setup/04-configuration-files-and-web-uis/'
L51 = '../05-hdfs-architecture/01-namenode-and-datanode/'
L52 = '../05-hdfs-architecture/02-blocks/'
L53 = '../05-hdfs-architecture/03-replication-and-rack-awareness/'
L54 = '../05-hdfs-architecture/04-fsimage-edit-log-and-checkpointing/'
L55 = '../05-hdfs-architecture/05-heartbeats-and-block-reports/'
L56 = '../05-hdfs-architecture/06-safe-mode/'
L61 = '../06-hdfs-operations/01-how-a-file-is-written-the-write-pipeline/'
L62 = '../06-hdfs-operations/02-how-a-file-is-read/'
L63 = '../06-hdfs-operations/03-hdfs-shell-commands/'
L64 = '../06-hdfs-operations/04-admin-commands-dfsadmin-fsck-and-balancer/'
L65 = '../06-hdfs-operations/05-the-hdfs-java-api/'
TERMS = [
    ('Server', 'Hardware and clusters', 'A computer built to run all day and serve other computers over a network.', L11),
    ('Node', 'Hardware and clusters', 'One server (or VM) that is a member of a cluster.', L11),
    ('Rack', 'Hardware and clusters', 'A cabinet of 20–40 servers sharing power and a top-of-rack switch. A failure domain and a bandwidth boundary.', L11),
    ('ToR switch', 'Hardware and clusters', '“Top of rack” switch that connects the servers in one rack and links the rack to the core network.', L11),
    ('Core (spine) switch', 'Hardware and clusters', 'Large switch connecting all the racks. Cross-rack traffic goes through it.', L11),
    ('Oversubscription', 'Hardware and clusters', 'When a switch\'s server ports add up to more bandwidth than its uplinks, for example 3 : 1.', L11),
    ('Commodity hardware', 'Hardware and clusters', 'Ordinary, affordable servers. Hadoop tolerates their failures in software.', L11),
    ('JBOD', 'Hardware and clusters', '“Just a bunch of disks”: separate disks without RAID, the usual choice for DataNodes.', L11),
    ('Cluster', 'Hardware and clusters', 'Networked nodes that work together as one system.', L12),
    ('Master node', 'Hardware and clusters', 'Coordinates the cluster: keeps metadata, tracks health, assigns work. NameNode, ResourceManager.', L12),
    ('Worker node', 'Hardware and clusters', 'Stores data and runs tasks. Usually runs a DataNode and a NodeManager.', L12),
    ('Edge (gateway) node', 'Hardware and clusters', 'The node where users log in and submit jobs; runs client tools only.', L12),
    ('Heartbeat', 'Hardware and clusters', 'Regular “I am alive” message from a worker to its master. HDFS: every 3 seconds.', L12),
    ('Shared-nothing', 'Hardware and clusters', 'Each node has its own CPU, RAM and disks; nodes share only the network.', L12),
    ('Single point of failure (SPOF)', 'Hardware and clusters', 'A part whose failure stops the whole system, such as a master with no standby.', L12),
    ('Horizontal scaling (scale out)', 'Sizing and operations', 'Adding more nodes rather than making one machine bigger.', L13),
    ('Replication factor', 'HDFS', 'How many copies of each block HDFS keeps. Default 3 (<code>dfs.replication</code>).', L13),
    ('Headroom', 'Sizing and operations', 'Free space kept on purpose (often 20–30%) so the cluster never runs full.', L13),
    ('Balancer', 'HDFS', 'Tool that moves blocks from full DataNodes to emptier ones (<code>hdfs balancer</code>).', L64),
    ('Wave', 'MapReduce', 'One round of tasks when there are more tasks than container slots.', L13),
    ('Fault tolerance', 'Sizing and operations', 'Continuing to work correctly when some parts fail.', L14),
    ('Re-replication', 'HDFS', 'Making new copies of blocks that lost replicas, until each is back to its replication factor.', L14),
    ('Under-replicated block', 'HDFS', 'A block with fewer live replicas than its replication factor.', L14),
    ('Missing block', 'HDFS', 'A block with no live replica at all. Files using it cannot be read.', L14),
    ('Checksum', 'HDFS', 'A small value computed from data to detect corruption. HDFS uses CRC32C per 512 bytes.', L62),
    ('Straggler', 'MapReduce', 'A task or node that is alive but much slower than the rest.', L14),
    ('Speculative execution', 'MapReduce', 'Running a backup copy of a slow task elsewhere; the first to finish wins.', L14),
    ('Data locality', 'MapReduce', 'Running a task on, or near, the node that holds its input block.', L15),
    ('Node-local (data-local)', 'MapReduce', 'Task runs on a node holding a replica of its input. Network distance 0.', L15),
    ('Rack-local', 'MapReduce', 'Task runs on another node in the same rack as its data. Distance 2.', L15),
    ('Off-rack', 'MapReduce', 'Task runs in a different rack from its data. Distance 4.', L15),
    ('Delay scheduling', 'YARN', 'Waiting briefly for a slot on a node with the data before running the task elsewhere.', L15),
    ('Shuffle', 'MapReduce', 'Moving map outputs across the network to the reducers, sorted by key.', L15),
    ('HDFS', 'HDFS', 'Hadoop Distributed File System: stores big files as blocks replicated across DataNodes.', ''),
    ('NameNode', 'HDFS', 'The HDFS master: file names, directories, permissions and the location of every block.', L12),
    ('DataNode', 'HDFS', 'HDFS worker that stores block replicas on its local disks and serves reads and writes.', L12),
    ('Block', 'HDFS', 'The unit HDFS stores: a file is cut into blocks of 128 MB by default (the last one can be smaller).', L52),
    ('Block report', 'HDFS', 'A DataNode\'s full list of the blocks on its disks, sent at start-up and periodically.', L12),
    ('fsimage and edit log', 'HDFS', 'The NameNode\'s saved metadata: a full snapshot (fsimage) plus a log of every change since (edits).', L54),
    ('Secondary NameNode', 'HDFS', 'Merges the edit log into the fsimage (checkpointing). It is <b>not</b> a standby and cannot take over.', L54),
    ('Standby NameNode', 'HDFS', 'In High Availability, a second NameNode kept up to date that takes over if the active one fails.', ''),
    ('Safe mode', 'HDFS', 'Read-only state of the NameNode at start-up while it waits for enough block reports.', L56),
    ('Rack awareness', 'HDFS', 'HDFS knowing which rack each node is on (from a topology script), so replicas span racks.', L11),
    ('MapReduce', 'MapReduce', 'Programming model and engine: map tasks process input splits in parallel, reduce tasks combine the results.', ''),
    ('Input split', 'MapReduce', 'The piece of input one map task processes; usually one block, but it is a logical range, not the block itself.', L15),
    ('Mapper / Reducer', 'MapReduce', 'User code that turns input records into key–value pairs (map) and combines all values for a key (reduce).', ''),
    ('Combiner', 'MapReduce', 'An optional “mini reducer” run on map output before the shuffle, to send less data.', ''),
    ('YARN', 'YARN', 'Yet Another Resource Negotiator: Hadoop\'s cluster resource manager since Hadoop 2.', L12),
    ('ResourceManager', 'YARN', 'The YARN master: tracks free resources and grants containers to applications.', L12),
    ('NodeManager', 'YARN', 'YARN worker on each node: launches and monitors containers.', L12),
    ('ApplicationMaster', 'YARN', 'One per job: asks for containers and manages that job\'s tasks and retries.', L12),
    ('Container', 'YARN', 'A slice of a node\'s memory and CPU in which one task runs.', L12),
    ('Hadoop Common', 'History and versions', 'Shared libraries, configuration and tools used by every other Hadoop module.', L23),
    ('Schema-on-read', 'History and versions', 'Store raw data as it is and apply structure when reading it (Hive, Spark).', L23),
    ('Write once, read many', 'HDFS', 'HDFS files are written once (and can be appended) but not edited in the middle.', L21),
    ('GFS', 'History and versions', 'The Google File System (paper, 2003): the design HDFS is based on.', L22),
    ('Apache Nutch', 'History and versions', 'Open-source web search engine by Doug Cutting and Mike Cafarella where Hadoop\'s code began.', L22),
    ('JobTracker', 'History and versions', 'Hadoop 1 master that did both resource management and task scheduling for every job. Replaced by YARN.', L24),
    ('TaskTracker', 'History and versions', 'Hadoop 1 worker daemon that ran tasks in fixed map and reduce slots.', L24),
    ('Slot', 'History and versions', 'Hadoop 1\'s fixed place for one map task or one reduce task, never both.', L24),
    ('HDFS Federation', 'HDFS', 'Several independent NameNodes, each managing part of the namespace, sharing the DataNodes.', L24),
    ('JournalNodes (QJM)', 'HDFS', 'An odd-sized group of nodes storing the NameNode edit log, so the standby stays in sync (HA).', L24),
    ('Erasure coding', 'HDFS', 'Data plus parity cells (for example RS-6-3) instead of full copies: about 1.5× storage. Hadoop 3.', L24),
    ('Daemon', 'Hardware and clusters', 'A long-running background program. Every Hadoop component (NameNode, DataNode…) is a Java daemon.', L31),
    ('jps', 'Sizing and operations', 'JDK command listing running Java processes: the quickest check of which Hadoop daemons are up.', L31),
    ('fs.defaultFS', 'HDFS', 'Setting in core-site.xml that tells clients and daemons where the NameNode is, e.g. hdfs://nn1:8020.', L31),
    ('JobHistory Server', 'MapReduce', 'Keeps logs and counters of finished MapReduce jobs (web UI on port 19888).', L31),
    ('ZKFC', 'HDFS', 'ZooKeeper Failover Controller: watches a NameNode and triggers automatic failover in HA.', L31),
    ('Write pipeline', 'HDFS', 'The chain client → DN1 → DN2 → DN3 through which each block is written, with acks flowing back.', L61),
    ('Packet', 'HDFS', 'A 64 KB piece of a block sent through the write pipeline and acknowledged by every DataNode.', L32),
    ('Lease', 'HDFS', 'A write lock the NameNode gives one client, so only one writer works on a file at a time.', L32),
    ('Output committer', 'MapReduce', 'Moves successful task output into the final directory and writes the _SUCCESS marker.', L32),
    ('_SUCCESS', 'MapReduce', 'Empty file written into a job\'s output directory when the job completes successfully.', L32),
    ('Utility node', 'Hardware and clusters', 'Runs supporting services: ZooKeeper, Hive Metastore, HiveServer2, Oozie, cluster manager.', L33),
    ('Gateway node', 'Hardware and clusters', 'Another name for an edge node: client tools and configs, no core daemons.', L33),
    ('OLTP vs OLAP', 'Sizing and operations', 'OLTP: many small fast reads/writes (databases). OLAP: big scans for analysis (warehouses, Hive, Spark).', L34),
    ('TCO', 'Sizing and operations', 'Total cost of ownership: hardware, software, people, power, space and downtime over the years.', L34),
    ('WSL 2', 'Setup and configuration', 'Windows Subsystem for Linux: a real Ubuntu inside Windows, the easiest way to practise Hadoop on a Windows PC.', L41),
    ('JAVA_HOME', 'Setup and configuration', 'Environment variable pointing to the Java folder (above bin/java). Set it in hadoop-env.sh so every daemon finds Java.', L41),
    ('Passwordless SSH', 'Setup and configuration', 'Key-based login without a password; the start scripts use it to start daemons on every host, even localhost.', L41),
    ('Standalone mode', 'Setup and configuration', 'Default mode: one JVM, local files (file:///), no daemons. For debugging logic.', L42),
    ('Pseudo-distributed mode', 'Setup and configuration', 'Every daemon on one machine in its own JVM, with HDFS (replication 1) and YARN. For learning.', L42),
    ('Fully distributed mode', 'Setup and configuration', 'Masters and workers on separate machines (or containers), replication 3. Production.', L42),
    ('workers file', 'Setup and configuration', 'etc/hadoop/workers: one worker host per line, read by start-dfs.sh and start-yarn.sh.', L42),
    ('NameNode format', 'Setup and configuration', 'hdfs namenode -format: creates an empty namespace and a new cluster ID. Once per cluster; again erases HDFS.', L43),
    ('Cluster ID', 'Setup and configuration', 'ID created by formatting. DataNodes with a different one refuse to join (“Incompatible clusterIDs”).', L43),
    ('apache/hadoop image', 'Setup and configuration', 'Official Docker image of Hadoop; FILE_property=value environment lines become XML settings.', L43),
    ('*-site.xml', 'Setup and configuration', 'Your configuration files in etc/hadoop (core, hdfs, yarn, mapred). They override the defaults.', L44),
    ('*-default.xml', 'Setup and configuration', 'Built-in defaults for every property, packaged inside Hadoop\'s jars.', L44),
    ('final property', 'Setup and configuration', '&lt;final&gt;true&lt;/final&gt;: configuration files loaded later (such as a job.xml) cannot override it.', L44),
    ('-D option', 'Setup and configuration', 'Sets a property for one command or job, e.g. hdfs dfs -D dfs.replication=2 -put …', L44),
    ('/conf and /jmx', 'Setup and configuration', 'Web endpoints of every daemon: the settings in use (with source) and live metrics as JSON.', L44),
    ('Web UI ports', 'Setup and configuration', 'NameNode 9870, DataNode 9864, ResourceManager 8088, NodeManager 8042, JobHistory 19888.', L44),
    ('Block map', 'HDFS', 'NameNode\'s in-memory map from each block to the DataNodes holding it; rebuilt from block reports, never saved.', L51),
    ('blk_ and .meta files', 'HDFS', 'A replica on a DataNode disk: blk_N holds the bytes, blk_N_genstamp.meta the checksums (4 B per 512 B).', L51),
    ('Block pool', 'HDFS', 'All blocks of one namespace (BP-…); a folder on every DataNode. Federation gives each NameNode its own.', L51),
    ('RecordReader', 'MapReduce', 'Turns a split\'s bytes into records; finishes a record crossing the split end and skips a partial first line.', L52),
    ('Topology script', 'HDFS', 'Script named by net.topology.script.file.name that prints a rack for each DataNode IP or host.', L53),
    ('Over-/mis-replicated', 'HDFS', 'Over: more replicas than the target (extras deleted). Mis: enough replicas but all in one rack.', L53),
    ('setrep', 'HDFS', 'hdfs dfs -setrep [-w] N path: change a file\'s replication factor (and wait).', L53),
    ('Transaction ID (txid)', 'HDFS', 'Number given to every namespace change in the edit log; fsimage_N contains changes up to N.', L54),
    ('Checkpoint', 'HDFS', 'Merging fsimage + edit log into a new fsimage (SecondaryNameNode, Standby NameNode or saveNamespace).', L54),
    ('oiv / oev', 'HDFS', 'Offline Image Viewer and Offline Edits Viewer: read fsimage and edits files as text/XML.', L54),
    ('Stale DataNode', 'HDFS', 'No heartbeat for 30 s: still live, but can be avoided for reads and writes.', L55),
    ('Incremental block report', 'HDFS', 'Small report of replicas a DataNode received or deleted since its last report.', L55),
    ('triggerBlockReport', 'HDFS', 'hdfs dfsadmin -triggerBlockReport host:9867 makes a DataNode send a full block report now.', L55),
    ('Safe mode threshold', 'HDFS', 'int(total blocks × 0.999) must have a reported replica, then a 30 s extension, before safe mode ends.', L56),
    ('Packet', 'HDFS', 'Unit of the write pipeline: about 64 KB, i.e. 126 chunks of 512 bytes, each with a 4-byte checksum.', L61),
    ('Generation stamp', 'HDFS', 'Version number of a block (blk_N_GS); bumped when a pipeline is recovered, so stale replicas can be recognised.', L61),
    ('Pipeline recovery', 'HDFS', 'When a DataNode fails mid-write, the client rebuilds the pipeline with the survivors and a new generation stamp, then keeps writing.', L61),
    ('Network distance', 'HDFS', 'Hops between client and replica in the topology: 0 same node, 2 same rack, 4 other rack. Reads go to the nearest replica.', L62),
    ('Short-circuit read', 'HDFS', 'A client on the same machine reads the block file directly from local disk (dfs.client.read.shortcircuit, off by default).', L62),
    ('Hedged read', 'HDFS', 'If a read is slow, start a second read on another replica and use whichever finishes first.', L62),
    ('Corrupt replica', 'HDFS', 'A replica whose checksum does not match; the reader reports it (reportBadBlocks) and the NameNode replaces it.', L62),
    ('hdfs dfs', 'HDFS', 'The HDFS shell (FsShell): Linux-like commands such as -ls, -put, -cat, -mv, -rm on Hadoop file systems.', L63),
    ('Trash', 'HDFS', '/user/&lt;name&gt;/.Trash: where -rm moves files when fs.trash.interval &gt; 0 (it is 0, off, by default).', L63),
    ('getmerge', 'HDFS', 'hdfs dfs -getmerge dir local.csv: concatenates every file in an HDFS folder into one local file.', L63),
    ('dfsadmin', 'HDFS', 'hdfs dfsadmin: admin client for the NameNode (-report, -refreshNodes, -safemode, -printTopology…).', L64),
    ('fsck', 'HDFS', 'hdfs fsck path: health report of files and blocks (missing, corrupt, under-replicated); read-only by default.', L64),
    ('Decommissioning', 'HDFS', 'Retiring a DataNode safely: list it in dfs.hosts.exclude, run -refreshNodes, wait for Decommissioned.', L64),
    ('Maintenance mode', 'HDFS', 'Planned short downtime for a DataNode without copying away all its blocks.', L64),
    ('FileSystem API', 'HDFS', 'org.apache.hadoop.fs.FileSystem: the Java API (create, open, listStatus, rename, delete…) used by all Hadoop clients.', L65),
    ('WebHDFS', 'HDFS', 'REST API for HDFS on the NameNode (port 9870); data requests are redirected to DataNodes (port 9864).', L65),
    ('HttpFS', 'HDFS', 'A gateway server offering the WebHDFS API that streams data itself, so clients need to reach only one host.', L65),
    ('hflush / hsync', 'HDFS', 'Output-stream calls: hflush makes written data visible to readers; hsync also forces it to disk on the DataNodes.', L65),
    ('DistCp', 'Sizing and operations', 'Distributed copy: copies large data sets between or within clusters using MapReduce.', ''),
]
CONFUSED = [
    ('Block vs input split', 'A <b>block</b> is how HDFS physically stores bytes (128 MB pieces). An <b>input split</b> is the logical piece one map task reads; it normally matches a block, but a record that crosses a block boundary is read whole by one split.'),
    ('NameNode vs ResourceManager', 'Both are masters, of different things. The <b>NameNode</b> manages <i>storage</i> (files and blocks). The <b>ResourceManager</b> manages <i>compute</i> (memory and CPU for jobs).'),
    ('DataNode vs NodeManager', 'Both run on a worker. The <b>DataNode</b> stores blocks; the <b>NodeManager</b> runs task containers. Running both on one machine is what makes data locality possible.'),
    ('Secondary NameNode vs Standby NameNode', 'The <b>Secondary</b> only merges the edit log into the fsimage. It cannot replace a failed NameNode. The <b>Standby</b> (HA) is a hot spare that takes over automatically.'),
    ('ResourceManager vs ApplicationMaster', 'The <b>ResourceManager</b> serves the whole cluster and hands out containers. An <b>ApplicationMaster</b> serves one job and decides which of its tasks run in those containers.'),
    ('Replication vs backup', '<b>Replication</b> keeps live copies to survive hardware failure; deletes and bad writes reach every copy. A <b>backup</b> or snapshot is a separate point-in-time copy you can restore.'),
    ('Node-local vs rack-local', '<b>Node-local</b>: the task runs on a machine holding its block. <b>Rack-local</b>: on another machine in the same rack, so data crosses only the rack switch.'),
    ('Dead vs stale DataNode', 'A <b>dead</b> node has been silent past the timeout (≈10.5 min) and its replicas are re-created elsewhere. A <b>stale</b> node has missed heartbeats for a shorter time (30 s by default) and can be avoided for reads and writes without being declared dead.'),
    ('Standalone vs pseudo-distributed', '<b>Standalone</b> runs a job inside one Java process on local files; no daemons. <b>Pseudo-distributed</b> runs every daemon (NameNode, DataNode, ResourceManager…) as a separate process on one machine, with real HDFS and YARN.'),
    ('core-default.xml vs core-site.xml', '<b>core-default.xml</b> holds Hadoop\'s built-in defaults inside the jars; never edit it. <b>core-site.xml</b> in etc/hadoop is where you override the values you need.'),
    ('Decommission vs stopping a DataNode', '<b>Decommissioning</b> copies every block away first, then marks the node Decommissioned: no moment with fewer replicas. <b>Stopping</b> it is treated as a failure: HDFS waits until the node is declared dead (≈10.5 min) before re-replicating.'),
    ('hdfs dfs -mv vs -cp', '<b>-mv</b> only renames in the NameNode, so it is instant for any size. <b>-cp</b> reads and rewrites every byte through the client (5.6 s vs 1.9 s for 403 MB in our lab).'),
    ('docker compose stop vs down', '<b>stop</b> pauses the containers and keeps their disks, so HDFS data survives. <b>down</b> deletes the containers, and without volumes the data goes with them.'),
]


def glossary_main():
    groups = []
    for t in TERMS:
        if t[1] not in groups:
            groups.append(t[1])
    body = ''
    for g in groups:
        items = sorted([t for t in TERMS if t[1] == g], key=lambda x: x[0].lower())
        body += f'<h3 class="gl-group">{E(g)}</h3>\n<div class="terms gl-terms">\n'
        for name, _, meaning, link in items:
            more = f' <a class="gl-link" href="{link}">Lesson →</a>' if link else ' <small class="muted">· later module</small>'
            body += f'  <div class="term" data-q="{E((name + " " + meaning).lower())}"><b>{E(name)}</b><span>{meaning}{more}</span></div>\n'
        body += '</div>\n'
    conf = ''.join(f'<details><summary>{E(a)}</summary><p>{b}</p></details>\n' for a, b in CONFUSED)
    return f'''<div class="ad-slot" data-slot="top"></div>
<section class="part">
  <label class="search gl-search">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
    <input id="gl-q" type="search" placeholder="Search terms, e.g. block, rack, container…" aria-label="Search the glossary">
  </label>
  <p class="muted" id="gl-count"></p>
  <h2>Often confused</h2>
  <div class="faq">
{conf}  </div>
  <h2>All terms</h2>
{body}</section>'''


GL_CSS = '''<style>
.gl-search{display:flex;align-items:center;gap:8px;max-width:520px;padding:10px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);margin:6px 0}
.gl-search svg{width:18px;height:18px;color:var(--ink-3);flex:none}
.gl-search input{border:0;outline:0;background:none;font:inherit;color:var(--ink);width:100%}
.gl-group{margin-top:22px}
.gl-terms .term b{font-family:var(--font-body)}
.gl-link{font-weight:700;white-space:nowrap}
</style>'''
GL_JS = '''<script>
(function () {
  const q = document.getElementById("gl-q"), terms = Array.from(document.querySelectorAll(".gl-terms .term")), cnt = document.getElementById("gl-count");
  const groups = Array.from(document.querySelectorAll(".gl-group"));
  function run() {
    const s = q.value.trim().toLowerCase(); let n = 0;
    terms.forEach(t => { const on = !s || t.dataset.q.includes(s); t.hidden = !on; if (on) n++; });
    groups.forEach(g => { const box = g.nextElementSibling; g.hidden = box.querySelectorAll(".term:not([hidden])").length === 0; box.hidden = g.hidden; });
    cnt.textContent = s ? n + " matching term" + (n === 1 ? "" : "s") : terms.length + " terms";
  }
  q.addEventListener("input", run); run();
})();
</script>'''


def main():
    pg = shell('playground', 'Hadoop Cluster Playground: interactive simulator', 'An interactive simulator of a small Hadoop cluster: upload files to HDFS, see blocks and replicas on racks, stop DataNodes and NameNodes, watch re-replication and failover, and run a MapReduce job with and without data locality.', 15,
               'Cluster Playground', 'A small Hadoop cluster that runs in your browser. Upload files and watch HDFS split and replicate them, break nodes and racks, fail over the NameNode, and run a MapReduce job with and without data locality. Nothing is installed and nothing can break for real.',
               PG_MAIN, extra_head=f'<link rel="stylesheet" href="{UP}assets/css/cluster-sim.css">', extra_js=f'<script src="{UP}assets/js/cluster-sim.js"></script>')
    gl = shell('glossary', "Who's who: Hadoop glossary", 'Plain-English Hadoop glossary: racks, nodes, NameNode, DataNode, blocks, splits, YARN, containers, data locality and more, with the pairs of terms students most often confuse.', 10,
               "Who's who: Hadoop glossary", f'Every Hadoop term used in this course in one or two plain sentences, grouped by topic and searchable. Start with <b>Often confused</b>: the pairs of terms that trip up most students and interview candidates. {len(TERMS)} terms so far; the list grows with each module.',
               glossary_main(), extra_head=GL_CSS, extra_js=GL_JS)
    for slug, h in [('playground', pg), ('glossary', gl)]:
        out = os.path.join(ROOT, 'courses', 'hadoop', slug, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(h)
        print('wrote', os.path.relpath(out, ROOT), f'({len(h) // 1024} KB)')


if __name__ == '__main__':
    main()
