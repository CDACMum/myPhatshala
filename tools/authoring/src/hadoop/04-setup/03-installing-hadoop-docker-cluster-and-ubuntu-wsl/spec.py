import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-setup', lesson='03-installing-hadoop-docker-cluster-and-ubuntu-wsl', n='4.3',
    module_label='Module 4 · Setup',
    title='Installing Hadoop: Ubuntu/WSL and a Docker cluster',
    desc='Install Apache Hadoop 3.5.0 two ways, both tested end to end: natively on Ubuntu or WSL in pseudo-distributed mode (download, SHA-512 check, environment, four site files, SSH, format, start, first job) and as a 3-DataNode cluster with Docker Compose and the official apache/hadoop image. Real outputs, the nine errors seen during testing with their fixes, a Python config generator, quiz and interview scenarios.',
    og_desc='A working Hadoop 3.5 cluster on your own laptop, two ways. Every command and error from a real run.',
    minutes=40, level='Beginner → Intermediate',
    lead='This is the hands-on lesson: by the end you will have a working Hadoop cluster. Path A installs Hadoop 3.5.0 by hand on Ubuntu or WSL, so you see every file and step. Path B starts one NameNode, three DataNodes and YARN in Docker containers, so you can watch replication and failures on a real multi-node cluster. Both paths were run start to finish for this lesson; the outputs and error messages are the real ones.',
    chips=['Tested end to end', 'Docker 3-node cluster', 'Error → fix table'],
)

RUN = dict(
    heading='Turn the Docker config file into Hadoop XML',
    intro='<p>The <code>apache/hadoop</code> image reads lines like <code>CORE-SITE.XML_fs.defaultFS=hdfs://namenode</code> and writes them into the right XML file. This program does the same, so you can see the XML your containers really use.</p>',
    code='''config = """CORE-SITE.XML_fs.defaultFS=hdfs://namenode
HDFS-SITE.XML_dfs.replication=3
YARN-SITE.XML_yarn.resourcemanager.hostname=resourcemanager
YARN-SITE.XML_yarn.nodemanager.aux-services=mapreduce_shuffle"""

files = {}
for line in config.splitlines():
    key, value = line.split("=", 1)
    filename, prop = key.split("_", 1)
    files.setdefault(filename.lower(), []).append((prop, value))

for filename, props in files.items():
    print(f"--- {filename}")
    print("<configuration>")
    for name, value in props:
        print(f"  <property><name>{name}</name><value>{value}</value></property>")
    print("</configuration>")
''',
    anno=[
        ('key, value = line.split("=", 1)', 'Split only at the <b>first</b> <code>=</code>: values such as <code>HADOOP_MAPRED_HOME=/opt/hadoop</code> contain another one.'),
        ('filename, prop = key.split("_", 1)', 'The file name is before the first underscore. Property names contain dots and sometimes underscores, so split only once.'),
        ('files.setdefault(filename.lower(), []).append((prop, value))', '<code>setdefault</code> creates an empty list the first time a file name appears, then keeps adding to it.'),
    ],
    tasks=[
        dict(label='1 · Generate the XML', hint='Press <b>Run</b>. Then add the line <code>MAPRED-SITE.XML_mapreduce.framework.name=yarn</code> and run again.', code=None),
        dict(label='2 · Values with “=” inside', hint='<b>Predict first:</b> what goes wrong if you split at every <code>=</code>? Compare the two results.',
             code='''line = "MAPRED-SITE.XML_yarn.app.mapreduce.am.env=HADOOP_MAPRED_HOME=/opt/hadoop"
print("split all :", line.split("="))
print("split once:", line.split("=", 1))
'''),
        dict(label='3 · Compare checksums', hint='<code>sha512sum -c</code> compares two fingerprints. Here a tiny change in the data changes the whole fingerprint. Try changing one letter.',
             code='''import hashlib
good = b"hadoop-3.5.0 release bytes"
bad = b"hadoop-3.5.0 release bytez"
published = hashlib.sha512(good).hexdigest()
for name, data in [("good download", good), ("damaged download", bad)]:
    mine = hashlib.sha512(data).hexdigest()
    print(f"{name:16}: {mine[:16]}… {'OK' if mine == published else 'FAILED'}")
'''),
        dict(label='4 · Which daemons are missing?', hint='After <code>start-dfs.sh</code> and <code>start-yarn.sh</code>, five daemons should run. This jps output is from a run where something went wrong. Which ones are missing?',
             code='''expected = {"NameNode", "DataNode", "SecondaryNameNode", "ResourceManager", "NodeManager"}
jps = """4865 NameNode
5304 Jps
5166 SecondaryNameNode
5687 ResourceManager"""
running = {line.split()[1] for line in jps.splitlines()}
print("missing:", sorted(expected - running))
'''),
        dict(label='5 · Spot the error', hint='This should write a property line, but the output has the file name stuck to the property. Fix the split.',
             code='''line = "HDFS-SITE.XML_dfs.replication=3"
key, value = line.split("=", 1)
filename, prop = key.split(".", 1)
print("file:", filename, "| property:", prop, "| value:", value)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: make the practice file and check Hadoop\'s answer',
    intro='<p>Path B uses <code>canteen_orders.csv</code>. This program creates it (the same file on every computer, because the random generator is seeded) and then counts the items with plain Python, so you can check the answer your Hadoop job gives. Save it as <code>make_canteen.py</code> in the <code>hadoop-cluster</code> folder and run it.</p>',
    items=[
        dict(title='Create canteen_orders.csv and count three items', file='make_canteen.py',
             cmd=open(os.path.join(HERE, 'make_canteen.py')).read() + '\n# In a terminal (in the hadoop-cluster folder):\n#   python3 make_canteen.py',
             output='''Wrote canteen_orders.csv: 300,000 orders, 4,692,009 bytes
 50021  samosa
 49986  vada pav
 49948  dosa''',
             note='These counts match the Hadoop job in Path B exactly (50021 samosa, 49986 vada pav, 49948 dosa). Checking a cluster result against a small independent calculation is a habit worth keeping.'),
    ],
)

TRACE = dict(
    heading='One config line becomes one XML property',
    intro='<p>Follow a single line of the Docker <code>config</code> file through the conversion and watch each variable.</p>',
    code='''line = "MAPRED-SITE.XML_mapreduce.map.env=HADOOP_MAPRED_HOME=/opt/hadoop"
key, value = line.split("=", 1)
filename, prop = key.split("_", 1)
filename = filename.lower()
xml = f"<property><name>{prop}</name><value>{value}</value></property>"
print(filename)
print(xml)
''',
    notes={2: 'Split once :: Everything after the first <code>=</code> is the value, even if it has another <code>=</code>.',
           3: 'File :: Before the first underscore: <code>MAPRED-SITE.XML</code>.',
           4: 'Name :: The real file name is lower case: <code>mapred-site.xml</code>.',
           5: 'Build :: One property element, ready to go inside <code>&lt;configuration&gt;</code>.'},
)

WORKED_INTRO = 'Three things people script during real installs: writing the site files from one table, checking an install stage by stage, and catching configuration mistakes before starting a cluster. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Install · automation', title='Write all four site files from one table',
         problem='<p>Instead of editing four XML files by hand, keep the pseudo-distributed settings in one Python dictionary and print each file. Use the settings from Path A, steps 4 and 5 (without the long whitelist).</p>',
         inp='core: fs.defaultFS · hdfs: dfs.replication · mapred: mapreduce.framework.name · yarn: aux-services',
         approach=['Map each file name to its properties.',
                   'Loop over files, then properties.',
                   'Print the XML in Hadoop\'s format.'],
         code='''site = {
    "core-site.xml": {"fs.defaultFS": "hdfs://localhost:9000"},
    "hdfs-site.xml": {"dfs.replication": "1"},
    "mapred-site.xml": {"mapreduce.framework.name": "yarn"},
    "yarn-site.xml": {"yarn.nodemanager.aux-services": "mapreduce_shuffle"},
}
for name, props in site.items():
    print(f"== {name}")
    print("<configuration>")
    for k, v in props.items():
        print(f"    <property><name>{k}</name><value>{v}</value></property>")
    print("</configuration>")
''', notes={7: 'Per file :: One <code>&lt;configuration&gt;</code> block per file.'},
         tryit='Add <code>"dfs.namenode.name.dir": "file:///home/riya/hadoop-data/namenode"</code> to hdfs-site. In real scripts the output is written to <code>$HADOOP_HOME/etc/hadoop/</code> instead of printed.'),
    dict(level='i', tag='Install · checks', title='Check an install stage by stage',
         problem='<p>A student sends the results of five checks from their install. Report the first stage that fails and the most likely fix, the way a support engineer would.</p>',
         inp='version OK · jps has NameNode, DataNode, SecondaryNameNode · safe mode OFF · yarn nodes 0 · job not run',
         approach=['List the stages in order, each with a test and a fix.',
                   'Walk through them; stop at the first failure.',
                   'Later stages can\'t be judged until earlier ones pass.'],
         code='''results = {"hadoop version": True, "HDFS daemons in jps": True,
           "safe mode OFF": True, "yarn node -list > 0": False,
           "example job": False}
fixes = {"hadoop version": "check PATH and HADOOP_HOME",
         "HDFS daemons in jps": "read logs/hadoop-*-namenode-*.log",
         "safe mode OFF": "hdfs dfsadmin -safemode wait",
         "yarn node -list > 0": "NodeManager unhealthy? check disk space and NM log",
         "example job": "check yarn-site and mapred-site"}
for stage, ok in results.items():
    print(f"{'PASS' if ok else 'FAIL'}  {stage}")
    if not ok:
        print("      fix:", fixes[stage])
        break
''', notes={9: 'Order :: Dictionaries keep insertion order, so stages are checked in sequence.'},
         tryit='This exact failure (0 nodes because the disk was over 90% full) happened while testing this lesson. Make "HDFS daemons in jps" False and see how the advice changes.'),
    dict(level='a', tag='Admin · config lint', title='Catch configuration mistakes before starting',
         problem='<p>Write a small checker for a planned configuration. Flag: replication larger than the number of DataNodes; NameNode or DataNode folders under <code>/tmp</code>; YARN without the <code>mapreduce_shuffle</code> service; MapReduce not set to <code>yarn</code>.</p>',
         inp='replication 3 · 1 DataNode · name.dir /tmp/… · aux-services missing · framework yarn',
         approach=['Write each rule as a condition and a message.',
                   'Evaluate all rules, not just the first.',
                   'Print every problem found, or “looks good”.'],
         code='''conf = {"dfs.replication": 3, "datanodes": 1,
        "dfs.namenode.name.dir": "file:///tmp/hadoop/name",
        "mapreduce.framework.name": "yarn"}
rules = [
    (conf["dfs.replication"] > conf["datanodes"], "replication is higher than the number of DataNodes"),
    ("/tmp/" in conf.get("dfs.namenode.name.dir", "/tmp/"), "NameNode metadata under /tmp may vanish on reboot"),
    (conf.get("yarn.nodemanager.aux-services") != "mapreduce_shuffle", "YARN has no mapreduce_shuffle service"),
    (conf.get("mapreduce.framework.name") != "yarn", "MapReduce will run locally, not on YARN"),
]
problems = [msg for bad, msg in rules if bad]
print("\\n".join("- " + p for p in problems) or "looks good")
''', notes={5: 'Rules :: Each rule is a pair: (is it wrong?, what to say).'},
         tryit='Fix the configuration until it prints “looks good”. Cluster managers run checks like these before every change.'),
]

QUIZ = mix([
    dict(q='What does sha512sum -c hadoop-3.5.0.tar.gz.sha512 check?', options=['That Java is installed', 'That the downloaded file matches the published fingerprint', 'That HDFS is healthy', 'That SSH works'], answer=1,
         why='A matching SHA-512 checksum means the download is complete and unchanged.'),
    dict(q='Why set JAVA_HOME in hadoop-env.sh even if ~/.bashrc already has it?', options=['hadoop-env.sh is faster', 'Daemons started by the scripts over SSH don\'t read ~/.bashrc', 'Hadoop ignores environment variables', 'It is needed only on Windows'], answer=1,
         why='Every Hadoop command and daemon reads hadoop-env.sh, whatever shell starts it.'),
    dict(q='When should you run hdfs namenode -format?', options=['Every time you start HDFS', 'Once, when creating a new cluster', 'After every job', 'When safe mode is on'], answer=1,
         why='Formatting creates a new, empty namespace. Running it again erases HDFS metadata.'),
    dict(q='Why does the Path A hdfs-site.xml set dfs.namenode.name.dir and dfs.datanode.data.dir?', options=['To make HDFS faster', 'To keep HDFS data out of /tmp, which may be emptied on reboot', 'Docker requires it', 'To enable replication'], answer=1,
         why='By default Hadoop stores data under /tmp/hadoop-<user>. Moving it makes the cluster survive restarts.'),
    dict(q='A job stays at “Running job” and yarn node -list shows Total Nodes:0. The most likely cause is:', options=['The input file is too small', 'No healthy NodeManager, e.g. its disk is over 90% full', 'The NameNode is in safe mode', 'The checksum failed'], answer=1,
         why='Without a healthy NodeManager, YARN has nowhere to run containers, so the job waits for ever.'),
    dict(q='What does docker compose down do to the HDFS data in the Path B cluster?', options=['Nothing, it is kept', 'It is deleted with the containers, because no volumes are used', 'It is copied to your PC', 'It moves to the NameNode'], answer=1,
         why='The data lived inside the containers. Use stop/start to keep it, or add volumes.'),
    dict(q='In the Docker config file, how is HDFS-SITE.XML_dfs.replication=3 used?', options=['It is ignored', 'The image writes dfs.replication=3 into hdfs-site.xml when the container starts', 'It sets an environment variable for Java only', 'It changes the Docker network'], answer=1,
         why='The apache/hadoop image converts FILE_property=value lines into the matching XML file.'),
    dict(q='“Output directory … already exists” when re-running an example job means:', options=['HDFS is corrupt', 'MapReduce never overwrites output; delete the folder or choose a new one', 'You must reformat the NameNode', 'The job succeeded'], answer=1,
         why='This protects earlier results. Remove it with hdfs dfs -rm -r output.'),
])

REVISION = [
    'Path A (native): download → <b>sha512sum -c</b> → unpack → <code>HADOOP_HOME</code>, <code>PATH</code> → <code>JAVA_HOME</code> in <b>hadoop-env.sh</b>.',
    'Site files: core (<code>fs.defaultFS</code>), hdfs (<code>dfs.replication=1</code>, storage dirs), mapred (<code>framework=yarn</code>), yarn (<code>mapreduce_shuffle</code>).',
    'SSH key for localhost → <b>format once</b> → <code>start-dfs.sh</code> → <code>start-yarn.sh</code> → <code>jps</code>.',
    'Check: <code>hadoop version</code> → <code>jps</code> → <code>safemode wait</code> → <code>yarn node -list</code> → example job.',
    'UIs: NameNode <code>:9870</code>, ResourceManager <code>:8088</code>.',
    'Path B (Docker): <code>docker-compose.yaml</code> + <code>config</code> → <code>docker compose up -d --scale datanode=3</code>.',
    'Docker: <b>stop/start keeps data, down deletes it</b> (no volumes).',
    'Errors: JAVA_HOME → hadoop-env.sh · publickey → SSH key · safe mode → wait · output exists → rm -r · 0 nodes → NM disk · MRAppMaster → HADOOP_MAPRED_HOME.',
]
FAQ = [
    ('What are the steps to install Hadoop on Ubuntu?', 'Install Java (JDK 17 for Hadoop 3.5) and SSH; download and verify the Hadoop tarball; extract it and set HADOOP_HOME and PATH; set JAVA_HOME in hadoop-env.sh; configure core-site.xml, hdfs-site.xml, mapred-site.xml and yarn-site.xml; set up passwordless SSH to localhost; format the NameNode; start HDFS and YARN with start-dfs.sh and start-yarn.sh; verify with jps, the web UIs and an example job.'),
    ('Can I install Hadoop on Windows?', 'For learning, install it inside WSL 2 (Ubuntu) using exactly the Path A steps, or run the Docker cluster with Docker Desktop. The web UIs are reachable from Windows at localhost:9870 and localhost:8088.'),
    ('How do I check that Hadoop is installed correctly?', 'hadoop version prints the version; jps lists NameNode, DataNode, SecondaryNameNode, ResourceManager and NodeManager; hdfs dfsadmin -report shows live DataNodes; yarn node -list shows RUNNING NodeManagers; the NameNode UI (9870) and ResourceManager UI (8088) open; and an example job such as grep or wordcount completes.'),
    ('Why is my NodeManager UNHEALTHY?', 'Usually a disk-health check: when a local or log directory is more than 90% full (the default threshold), the NodeManager marks it bad and reports itself unhealthy, so YARN schedules nothing there. Free disk space or, on a practice machine, raise yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-percentage.'),
    ('What is the official Hadoop Docker image?', 'The Apache Hadoop project publishes apache/hadoop images on Docker Hub (for example apache/hadoop:3.5.0). One image contains everything; the command decides which daemon a container runs, and environment variables become configuration.'),
    ('How do I stop Hadoop?', 'Run stop-yarn.sh and then stop-dfs.sh (and mapred --daemon stop historyserver if you started it). With Docker, docker compose stop keeps the containers and data; docker compose down removes them.'),
    ('Where are Hadoop logs?', 'In $HADOOP_HOME/logs by default, one file per daemon, for example hadoop-riya-namenode-&lt;host&gt;.log. In Docker, use docker compose logs namenode.'),
    ('Do I need to format the NameNode every time?', 'No. Only once, when creating a cluster. Re-formatting erases the namespace and gives HDFS a new cluster ID, so existing DataNodes refuse to join until their data folders are cleaned.'),
]

PRACTICE_INTRO = 'Exercises on the install itself: paths, configuration, checks and errors. All runnable in the browser.'
PROBLEMS = [
    dict(level='easy', title='Build the download URL', stmt='Print the download URL of the tarball and its checksum for version 3.5.0, using the pattern https://dlcdn.apache.org/hadoop/common/hadoop-V/hadoop-V.tar.gz.', inp='version = "3.5.0"',
         code='''v = "3.5.0"
url = f"https://dlcdn.apache.org/hadoop/common/hadoop-{v}/hadoop-{v}.tar.gz"
print(url)
print(url + ".sha512")
''', explain='The checksum file has the same name plus .sha512. Changing v is all it takes to install another release.'),
    dict(level='easy', title='Relative HDFS paths', stmt='In HDFS, a relative path is relative to /user/&lt;username&gt;. Print the full paths for user riya of input and output/part-r-00000.', inp='user riya · input · output/part-r-00000',
         code='''user = "riya"
for p in ["input", "output/part-r-00000"]:
    print(p, "->", f"/user/{user}/{p}")
''', explain='/user/riya/input and /user/riya/output/part-r-00000. That is why step 8 creates /user/riya first.'),
    dict(level='easy', title='Which UI on which port?', stmt='Print the URL of the NameNode and ResourceManager web UIs on localhost.', inp='NameNode 9870 · ResourceManager 8088',
         code='''for name, port in [("NameNode", 9870), ("ResourceManager", 8088)]:
    print(f"{name:16} http://localhost:{port}")
''', explain='http://localhost:9870 and http://localhost:8088, the same for Path A and Path B (which is why they cannot run together).'),
    dict(level='medium', title='Parse fsck', stmt='From the fsck line "len=4692009 Live_repl=3", print the block size in MB and the number of live replicas.', inp='len=4692009 Live_repl=3',
         code='''line = "len=4692009 Live_repl=3"
fields = dict(part.split("=") for part in line.split())
print(f"{int(fields['len']) / 1024 / 1024:.1f} MB, {fields['Live_repl']} live replicas")
''', explain='4.5 MB and 3 live replicas: the whole file fits in one block, stored on all three DataNodes.'),
    dict(level='medium', title='Disk check threshold', stmt='A NodeManager disk is 465 GB with 430 GB used. With the default 90% threshold, is it healthy? And with 99.5%?', inp='465 GB disk · 430 GB used · 90% and 99.5%',
         code='''used_pct = 430 / 465 * 100
for limit in [90, 99.5]:
    print(f"used {used_pct:.1f}% vs limit {limit}% -> {'healthy' if used_pct <= limit else 'UNHEALTHY'}")
''', explain='92.5% used: unhealthy with the default 90% limit, healthy with 99.5%. Typical of a student laptop full of downloads.'),
    dict(level='medium', title='Docker memory budget', stmt='Idle Hadoop daemons measured during testing used about 0.2–0.35 GB of RAM each; take 0.3 GB. The Docker cluster runs 6 containers and Docker Desktop is given 4 GB. How much is left for job containers, each needing 1 GB?', inp='6 × 0.3 GB · 4 GB · 1 GB per job container',
         code='''used = 6 * 0.3
left = 4 - used
print(f"daemons use {used:.1f} GB, {left:.1f} GB left -> {int(left // 1)} job container(s)")
''', explain='About 1.8 GB for the idle daemons and 2.2 GB left: room for only 2 job containers, and a MapReduce job needs one just for its ApplicationMaster. Give Docker 6–8 GB if you can.'),
    dict(level='business', title='Manual vs scripted install', stmt='A team installs 12 practice clusters a year for training batches. By hand: 45 minutes each. Docker Compose: 5 minutes each, plus 3 hours once to prepare the files. Hours saved in a year?', inp='12 installs · 45 min vs 5 min · 3 h setup',
         code='''manual = 12 * 45 / 60
compose = 3 + 12 * 5 / 60
print(f"manual {manual:.0f} h, compose {compose:.0f} h, saved {manual - compose:.0f} h")
''', explain='9 hours by hand against 4 with Compose: 5 hours saved in the first year, and every batch gets an identical cluster.'),
    dict(level='advanced', title='Diagnose from error text', stmt='Write a function that maps an error message to its fix, using keywords from the errors table, and test it on three real messages.', inp='JAVA_HOME … · Permission denied (publickey,password) · Output directory … already exists',
         code='''fixes = [("JAVA_HOME is not set", "set JAVA_HOME in etc/hadoop/hadoop-env.sh"),
         ("Permission denied (publickey", "set up passwordless SSH to the host"),
         ("already exists", "hdfs dfs -rm -r <output> or choose a new folder"),
         ("safe mode", "hdfs dfsadmin -safemode wait"),
         ("MRAppMaster", "set HADOOP_MAPRED_HOME / mapreduce.application.classpath")]
def diagnose(msg):
    return next((fix for key, fix in fixes if key in msg), "read the daemon log in $HADOOP_HOME/logs")
for m in ["localhost: ERROR: JAVA_HOME is not set and could not be found.",
          "riya@localhost: Permission denied (publickey,password).",
          "Output directory hdfs://localhost:9000/user/riya/output already exists"]:
    print(diagnose(m))
''', explain='Each message maps to its fix; anything unknown falls back to “read the log”. Support teams build runbooks on exactly this idea.'),
]

SCN_INTRO = 'Installation questions test whether you have really done it. Answer with the order of steps, the checks and the errors you met.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Install · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“My first job never finishes”</h4>
      <p class="scn__situation">A student's pseudo-distributed cluster shows all five daemons in jps, but the example job prints “Running job: job_…” and then nothing for ten minutes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know where YARN runs work, and how to check NodeManagers?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The job is waiting for a container. Run <code>yarn node -list -all</code>: if the NodeManager is missing or UNHEALTHY, nothing can run.</li>
          <li>Read the NodeManager log: a common message is <code>used space above threshold of 90.0%</code> (disk nearly full).</li>
          <li>Free disk space (or raise the threshold on a practice machine), restart YARN, and check that the node shows RUNNING.</li>
          <li>Also check the ResourceManager UI at port 8088 for the application's state and diagnostics.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Install · steps</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Walk me through installing Hadoop on a single machine”</h4>
      <p class="scn__situation">A common first-round interview question for data engineering roles.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the order of steps and whether you verify each one.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Java (JDK 17 for 3.5) and SSH; download the tarball and verify the SHA-512.</li>
          <li>Extract, set <code>HADOOP_HOME</code>/<code>PATH</code>, and <code>JAVA_HOME</code> in <code>hadoop-env.sh</code>.</li>
          <li>Configure the four site files (default FS, replication 1 and storage folders, MapReduce on YARN, shuffle service).</li>
          <li>Passwordless SSH, format the NameNode once, start HDFS and YARN, check <code>jps</code>, both web UIs and an example job.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Containers · data</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>“All our test data disappeared overnight”</h4>
      <p class="scn__situation">A team runs a Docker Compose Hadoop cluster for testing. After a laptop restart and <code>docker compose down</code> / <code>up</code>, HDFS is empty.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand container storage?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Without volumes, NameNode metadata and DataNode blocks live in the container's own file system, which <code>down</code> deletes.</li>
          <li>Use <code>docker compose stop</code>/<code>start</code> for pauses, or mount volumes for the name and data directories.</li>
          <li>For test data, keep a script that reloads it (put files, create tables), so a fresh cluster is ready in minutes.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · cluster ID</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>DataNode won't start after someone re-formatted the NameNode</h4>
      <p class="scn__situation">After <code>hdfs namenode -format</code> was run again on a test cluster, the DataNode exits at start-up. Its log mentions “Incompatible clusterIDs”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know what formatting changes?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Formatting created a new namespace with a new cluster ID; the DataNode's storage folder still has the old ID, so it refuses to join.</li>
          <li>On a test cluster whose data can be discarded: stop the DataNode, empty its <code>dfs.datanode.data.dir</code>, and start it again.</li>
          <li>On a real cluster: never re-format; restore the NameNode metadata from a backup instead. The old blocks are useless without the old namespace.</li>
        </ul>
      </div></details>
    </article>
'''
