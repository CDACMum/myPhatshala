import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Block size and replication are per file',
    intro='<p>Each upload uses the <b>Block</b> and <b>Replication</b> values chosen next to the button, like <code>-D dfs.blocksize=…</code> and <code>-D dfs.replication=…</code> on <code>hdfs dfs -put</code>. Compare files in the <b>NameNode metadata</b> tab.</p>',
    racks=2, nodes=3, features=['upload', 'fail', 'fsck'],
    **{'try': [
        dict(text='Upload a <b>1 GB</b> file with <b>128 MB</b> blocks and replication <b>3</b>: count its blocks.', on='upload-done'),
        dict(text='Upload another 1 GB file with <b>256 MB</b> blocks: half as many blocks for the NameNode to track.', on='upload-done'),
        dict(text='Upload one with <b>Replication 1</b>, then stop the node holding one of its blocks.', on='node-stop'),
        dict(text='Run <b>hdfs fsck /</b>: only the replication-1 file is damaged.', on='fsck'),
    ]},
)))

META = dict(
    module='04-setup', lesson='04-configuration-files-and-web-uis', n='4.4',
    module_label='Module 4 · Setup',
    title='Configuration files and web UIs',
    desc='How Hadoop configuration works: built-in *-default.xml files, the four *-site.xml files, env scripts and workers, per-command -D overrides, what “final” really protects, and how to see the value a daemon is using with hdfs getconf and the /conf page. The web UIs and ports (9870, 9864, 8088, 8042, 19888), /jmx metrics, real outputs and screenshots from a running Hadoop 3.5.0 cluster, a playground, quiz and interview scenarios.',
    og_desc='Defaults, site files, -D and final: which value wins, and how to check it on a live cluster. Plus the web UIs you will use every day.',
    minutes=28, level='Beginner → Intermediate',
    lead='Every Hadoop behaviour you will tune later, from replication to task memory, is a configuration property. This lesson explains the layers those properties come from, which value wins, and how to ask a running daemon what it is really using. It also tours the web UIs and the /conf and /jmx endpoints that engineers open first when something looks wrong. All outputs and screenshots are from a real Hadoop 3.5.0 cluster.',
    chips=['Real cluster output', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Merge configuration layers like Hadoop does',
    intro='<p>This program loads three layers in order (defaults, site file, command line) and keeps the last value for each property, unless an earlier layer marked it <i>final</i> and the later layer is a file. It also records the source, like the <code>/conf</code> page.</p>',
    code='''layers = [
    ("hdfs-default.xml", "file", {"dfs.replication": "3", "dfs.blocksize": "134217728"}, set()),
    ("hdfs-site.xml", "file", {"dfs.replication": "1"}, {"dfs.replication"}),
    ("job.xml", "file", {"dfs.replication": "5", "dfs.blocksize": "268435456"}, set()),
]

conf, source, final = {}, {}, set()
for name, kind, props, finals in layers:
    for key, value in props.items():
        if key in final and kind == "file":
            print(f"ignored {key}={value} from {name} (final)")
            continue
        conf[key], source[key] = value, name
    final |= finals

for key in conf:
    print(f"{key:16} = {conf[key]:>10}  [{source[key]}]")
''',
    anno=[
        ('("hdfs-site.xml", "file", {"dfs.replication": "1"}, {"dfs.replication"}),', 'The site file sets replication to 1 and marks it final (the last item is the set of final names).'),
        ('if key in final and kind == "file":', 'A later <b>file</b> cannot override a final property. (Values set directly, like <code>-D</code>, are not files: try challenge 2.)'),
        ('final |= finals', 'Finals are added only after the layer is loaded, so they protect against <i>later</i> layers.'),
    ],
    tasks=[
        dict(label='1 · Merge the layers', hint='Press <b>Run</b>. Why is the job\'s block size accepted but its replication ignored?', code=None),
        dict(label='2 · A direct -D setting', hint='<b>Predict first:</b> a direct setting (<code>kind="set"</code>) arrives after the final site file. Which replication wins? This matches the real test in Part 4.',
             code='''conf, final = {"dfs.replication": "3"}, {"dfs.replication"}
for kind, key, value in [("file", "dfs.replication", "4"), ("set", "dfs.replication", "2")]:
    if key in final and kind == "file":
        print("ignored", value, "from a file (final)")
    else:
        conf[key] = value
        print("now", conf[key], "via", kind)
'''),
        dict(label='3 · Expand ${…} variables', hint='Defaults refer to other properties, like <code>file://${hadoop.tmp.dir}/dfs/name</code>. Expand them as Hadoop does when the value is used.',
             code='''import re
conf = {"user.name": "riya", "hadoop.tmp.dir": "/tmp/hadoop-${user.name}",
        "dfs.namenode.name.dir": "file://${hadoop.tmp.dir}/dfs/name"}
def get(key):
    return re.sub(r"\\$\\{([^}]+)\\}", lambda m: get(m.group(1)), conf[key])
print(get("dfs.namenode.name.dir"))
'''),
        dict(label='4 · Bytes to MB', hint='<code>getconf</code> prints <code>134217728</code> for the block size. Convert block sizes in bytes to MB.',
             code='''for b in [134217728, 268435456, 1048576]:
    print(f"{b:>10} bytes = {b // (1024 * 1024)} MB")
'''),
        dict(label='5 · Spot the error', hint='This merge should let the site file override the default, but the default wins. Fix the order.',
             code='''defaults = {"dfs.replication": "3"}
site = {"dfs.replication": "1"}
conf = {}
for layer in [site, defaults]:
    conf.update(layer)
print("dfs.replication =", conf["dfs.replication"])
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a configuration report from a live NameNode',
    intro='<p>With your cluster from Lesson 4.3 running, this program reads the NameNode\'s <code>/conf</code> page and reports how many settings come from each file, plus the value and source of four important ones. Save it as <code>conf_report.py</code> and run it on the same computer.</p>',
    items=[
        dict(title='Where do the NameNode\'s 1,752 settings come from?', file='conf_report.py',
             cmd=open(os.path.join(HERE, 'conf_report.py')).read() + '\n# In a terminal:\n#   python3 conf_report.py',
             output='''1752 properties loaded
  542  hdfs-default.xml
  523  yarn-default.xml
  376  core-default.xml
  194  mapred-default.xml
   89  hdfs-rbf-default.xml
   17  programmatically
    5  yarn-site.xml
    4  mapred-site.xml
    2  hdfs-site.xml

fs.defaultFS             = hdfs://namenode   [programmatically]
dfs.replication          = 3   [hdfs-site.xml]
dfs.blocksize            = 134217728   [hdfs-default.xml]
dfs.namenode.name.dir    = file://${hadoop.tmp.dir}/dfs/name   [hdfs-default.xml]''',
             note='Real output from the Docker practice cluster. Two surprises worth knowing: <code>fs.defaultFS</code> shows “programmatically” because the NameNode sets it itself at start-up from its own address, and <code>/conf</code> shows <code>${…}</code> variables unexpanded. On Path A your numbers and sources will differ slightly.'),
    ],
)

TRACE = dict(
    heading='Which value wins, one line at a time',
    intro='<p>Follow <code>dfs.replication</code> through three layers and watch <code>conf</code> and <code>src</code> change in memory.</p>',
    code='''conf, src = {}, {}
conf["dfs.replication"], src["dfs.replication"] = "3", "hdfs-default.xml"
conf["dfs.replication"], src["dfs.replication"] = "3", "hdfs-site.xml"
conf["dfs.replication"], src["dfs.replication"] = "2", "-D (client)"
print(conf["dfs.replication"], "from", src["dfs.replication"])
''',
    notes={2: 'Default :: Always loaded first, from inside the jar.',
           3: 'Site :: Same number, but now the source is the site file.',
           4: 'Client :: The command-line value is applied last, so it wins.'},
)

WORKED_INTRO = 'Three everyday configuration tasks: turning human-friendly sizes into the bytes Hadoop expects, finding differences between two nodes\' configurations, and sizing YARN memory for a worker. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Admin · units', title='Write block sizes the way Hadoop stores them',
         problem='<p>A team wants 64 MB, 128 MB and 256 MB block sizes for three data sets. Print the byte values to put in <code>dfs.blocksize</code>, and how many blocks a 10 GB file would have with each.</p>',
         inp='64, 128, 256 MB · 10 GB file',
         approach=['1 MB = 1024 × 1024 bytes.',
                   'Blocks = ceil(file size / block size).',
                   'Print both.'],
         code='''import math
file_mb = 10 * 1024
for mb in [64, 128, 256]:
    print(f"{mb:>3} MB = {mb * 1024 * 1024:>9} bytes -> {math.ceil(file_mb / mb)} blocks")
''', notes={4: 'Bytes :: <code>dfs.blocksize</code> also accepts <code>128m</code>, but getconf and fsck show bytes.'},
         tryit='Fewer, bigger blocks mean less NameNode memory and fewer map tasks, but less parallelism. Module 5 returns to this trade-off.'),
    dict(level='i', tag='Admin · drift', title='Find configuration drift between two nodes',
         problem='<p>Jobs fail only on one worker. Compare the settings collected from a good node and the bad node and print every property whose value differs or exists on only one side.</p>',
         inp='good: replication 3, NM memory 8192, aux mapreduce_shuffle · bad: replication 3, NM memory 2048, no aux',
         approach=['Take the union of property names.',
                   'For each, compare values (missing counts as a difference).',
                   'Print the differences in a table.'],
         code='''good = {"dfs.replication": "3", "yarn.nodemanager.resource.memory-mb": "8192",
        "yarn.nodemanager.aux-services": "mapreduce_shuffle"}
bad = {"dfs.replication": "3", "yarn.nodemanager.resource.memory-mb": "2048"}
for key in sorted(good.keys() | bad.keys()):
    g, b = good.get(key, "(missing)"), bad.get(key, "(missing)")
    if g != b:
        print(f"{key:38} good={g:18} bad={b}")
''', notes={4: 'Union :: <code>|</code> on key views gives every name that appears on either side.'},
         tryit='The missing shuffle service alone makes every reduce on that node fail. This is why identical configuration on all nodes matters.'),
    dict(level='a', tag='Capacity · YARN memory', title='How much memory should YARN offer on a worker?',
         problem='<p>A worker has 128 GB RAM. Reserve 8 GB for the operating system, 4 GB for the DataNode and 2 GB for the NodeManager. Set <code>yarn.nodemanager.resource.memory-mb</code> to the rest, and work out how many 4 GB containers fit. (The practice cluster\'s UI showed the default of 8 GB per node.)</p>',
         inp='128 GB RAM · OS 8 · DataNode 4 · NodeManager 2 · 4 GB containers',
         approach=['Subtract the reserved memory.',
                   'Convert to MB for the property.',
                   'Containers = YARN memory // container size.'],
         code='''ram_gb, reserved = 128, {"OS": 8, "DataNode": 4, "NodeManager": 2}
yarn_gb = ram_gb - sum(reserved.values())
print("yarn.nodemanager.resource.memory-mb =", yarn_gb * 1024)
print("4 GB containers per node:", yarn_gb // 4)
''', notes={2: 'Reserve :: Memory YARN must not hand out to containers.'},
         tryit='Leave the property unset and YARN uses its default (8 GB in the practice cluster UI): a 128 GB server would run only 2 containers of 4 GB. Untuned defaults waste most of the hardware.'),
]

QUIZ = mix([
    dict(q='Which file normally overrides hdfs-default.xml?', options=['core-default.xml', 'hdfs-site.xml', 'workers', 'log4j.properties'], answer=1,
         why='Site files are loaded after the defaults, so their values win.'),
    dict(q='Where is fs.defaultFS normally set?', options=['hdfs-site.xml', 'core-site.xml', 'yarn-site.xml', 'workers'], answer=1,
         why='core-site.xml holds settings shared by all components, including the default file system.'),
    dict(q='What does hdfs getconf -confKey dfs.blocksize print on a default install?', options=['128', '128 MB', '134217728', '64m'], answer=2,
         why='The default is 134217728 bytes, i.e. 128 MB.'),
    dict(q='A client runs hdfs dfs -D dfs.replication=2 -put a.csv /data/. What happens?', options=['The cluster default changes to 2', 'Only a.csv is written with 2 replicas', 'The command fails because the site file says 3', 'All existing files change to 2'], answer=1,
         why='-D applies to that command only. Replication is a per-file setting chosen by the writing client.'),
    dict(q='What does <final>true</final> on a property in a site file do?', options=['Makes the property impossible to change in any way', 'Stops later configuration files (e.g. a job.xml) from overriding it', 'Encrypts the value', 'Deletes the default'], answer=1,
         why='Final protects against later resources. In the real test, a direct -D setting still applied.'),
    dict(q='Which port is the ResourceManager web UI by default?', options=['9870', '8088', '8042', '19888'], answer=1,
         why='NameNode 9870, ResourceManager 8088, NodeManager 8042, JobHistory 19888.'),
    dict(q='You add a property to yarn-site.xml but nothing changes. Most likely:', options=['XML is case-insensitive', 'The daemons were not restarted (or the file was not copied to every node)', 'YARN ignores site files', 'You must reformat the NameNode'], answer=1,
         why='Daemons read configuration at start-up. Change, distribute, then restart.'),
    dict(q='Which endpoint shows the settings a running daemon uses, with their source file?', options=['/logs', '/conf', '/stacks', '/static'], answer=1,
         why='/conf lists every property, its value, whether it is final, and its source.'),
])

REVISION = [
    'Layers: <b>*-default.xml</b> (in jars) → <b>*-site.xml</b> (etc/hadoop) → <b>-D / code</b>. Later wins.',
    '<b>final</b>: later configuration <i>files</i> cannot override it (e.g. job.xml). A direct <code>-D</code> still applied in our test.',
    'core-site: <code>fs.defaultFS</code> · hdfs-site: replication, block size, dirs · yarn-site: RM host, NM memory, shuffle · mapred-site: framework.',
    '<code>hadoop-env.sh</code>: <code>JAVA_HOME</code>, heap · <code>workers</code>: worker hosts · <code>capacity-scheduler.xml</code>: queues.',
    'Check values: <code>hdfs getconf -confKey &lt;name&gt;</code> and the daemon\'s <code>/conf</code> page (shows source).',
    'Replication and block size are <b>per file</b>, chosen by the writer; change existing files with <code>hdfs dfs -setrep</code>.',
    'UIs: NN <b>9870</b> · DN <b>9864</b> · SNN 9868 · RM <b>8088</b> · NM <b>8042</b> · JHS <b>19888</b>. Endpoints: <code>/conf</code>, <code>/jmx</code>, <code>/logs</code>.',
    'Edit → copy to all nodes → restart. Editing alone changes nothing in running daemons.',
]
FAQ = [
    ('What are the main configuration files in Hadoop?', 'core-site.xml (common settings such as fs.defaultFS), hdfs-site.xml (HDFS: replication, block size, storage folders, addresses), yarn-site.xml (YARN: ResourceManager host, NodeManager resources, auxiliary services), mapred-site.xml (MapReduce: framework, task memory, history server), plus hadoop-env.sh, yarn-env.sh and mapred-env.sh for environment variables, and workers for the list of worker hosts.'),
    ('What is the difference between core-default.xml and core-site.xml?', 'core-default.xml ships inside Hadoop\'s jars and holds the default for every core property; it is read-only reference. core-site.xml is your file in etc/hadoop that overrides the defaults you want to change.'),
    ('What is a final property in Hadoop?', 'A property marked &lt;final&gt;true&lt;/final&gt; cannot be overridden by configuration resources loaded later, for example the job.xml of a submitted job. Administrators use it to protect cluster-wide values. It does not stop a program from setting the value directly in its own configuration object.'),
    ('How do I check the value of a configuration property?', 'Use hdfs getconf -confKey &lt;name&gt; for the merged value seen by the client, or open http://&lt;daemon-host&gt;:&lt;port&gt;/conf to see what a running daemon uses, including the source file.'),
    ('What are the default web UI ports in Hadoop 3?', 'NameNode 9870, SecondaryNameNode 9868, DataNode 9864, ResourceManager 8088, NodeManager 8042, MapReduce JobHistory Server 19888. (Hadoop 2 used 50070 for the NameNode and 50075 for DataNodes.)'),
    ('Do I need to restart Hadoop after changing configuration?', 'Usually yes: daemons read site files at start-up. Some changes can be refreshed without a restart, for example hdfs dfsadmin -refreshNodes for include/exclude lists and yarn rmadmin -refreshQueues for scheduler queues. Client-side settings take effect on the next command.'),
    ('Can I change the replication of an existing file?', 'Yes, with hdfs dfs -setrep &lt;n&gt; &lt;path&gt; (-w waits for completion). Changing dfs.replication in hdfs-site.xml only affects files written afterwards by clients that use that file.'),
]

PRACTICE_INTRO = 'Exercises on reading, converting and checking configuration values. Each one runs in the browser.'
PROBLEMS = [
    dict(level='easy', title='Which file?', stmt='Print which site file each property belongs in.', inp='fs.defaultFS · dfs.replication · yarn.resourcemanager.hostname · mapreduce.framework.name',
         code='''prefix = {"fs.": "core-site.xml", "dfs.": "hdfs-site.xml",
          "yarn.": "yarn-site.xml", "mapreduce.": "mapred-site.xml"}
for key in ["fs.defaultFS", "dfs.replication", "yarn.resourcemanager.hostname", "mapreduce.framework.name"]:
    print(key, "->", next(f for p, f in prefix.items() if key.startswith(p)))
''', explain='The prefix usually tells you the file: fs → core, dfs → hdfs, yarn → yarn, mapreduce → mapred. (A few exceptions exist, such as hadoop.* in core-site.)'),
    dict(level='easy', title='Port lookup', stmt='Print the web UI URL of each daemon on host nn1 (masters) or w1 (workers).', inp='NameNode, ResourceManager on nn1 · DataNode, NodeManager on w1',
         code='''uis = [("NameNode", "nn1", 9870), ("ResourceManager", "nn1", 8088),
       ("DataNode", "w1", 9864), ("NodeManager", "w1", 8042)]
for name, host, port in uis:
    print(f"{name:16} http://{host}:{port}")
''', explain='Four URLs you will open often; the JobHistory Server adds 19888 when it is running.'),
    dict(level='easy', title='Read a stat line', stmt='Parse the real line "2 134217728 4692009 copy2.csv" (replication, block size, bytes, name).', inp='2 134217728 4692009 copy2.csv',
         code='''r, block, size, name = "2 134217728 4692009 copy2.csv".split()
print(f"{name}: {r} replicas, {int(block) // 2**20} MB blocks, {int(size) / 2**20:.1f} MB")
''', explain='copy2.csv: 2 replicas, 128 MB blocks, 4.5 MB of data.'),
    dict(level='medium', title='Blocks for each block size', stmt='The 4,692,009-byte canteen file was written with 128 MB and 1 MB blocks. How many blocks in each case? (fsck reported 5 for 1 MB.)', inp='4,692,009 bytes · 134217728 and 1048576',
         code='''import math
for block in [134217728, 1048576]:
    print(block, "->", math.ceil(4692009 / block), "block(s)")
''', explain='1 block with 128 MB and 5 blocks with 1 MB, matching the real fsck output.'),
    dict(level='medium', title='Override order', stmt='Apply defaults, then site, then -D options, and print the final values.', inp='defaults {replication 3, blocksize 128m} · site {replication 2} · -D {blocksize 256m}',
         code='''conf = {}
for layer in [{"dfs.replication": "3", "dfs.blocksize": "128m"},
              {"dfs.replication": "2"},
              {"dfs.blocksize": "256m"}]:
    conf.update(layer)
print(conf)
''', explain='Replication 2 (from the site file) and block size 256m (from -D). Each property is decided separately.'),
    dict(level='medium', title='Parse a property line', stmt='Extract the name, value and source from a real /conf line.', inp='&lt;property&gt;&lt;name&gt;dfs.replication&lt;/name&gt;&lt;value&gt;3&lt;/value&gt;…&lt;source&gt;hdfs-site.xml&lt;/source&gt;',
         code='''import re
line = "<property><name>dfs.replication</name><value>3</value><final>false</final><source>hdfs-site.xml</source>"
fields = dict(re.findall(r"<(name|value|final|source)>([^<]*)</", line))
print(fields)
''', explain='name dfs.replication, value 3, final false, source hdfs-site.xml: the same fields conf_report.py reads.'),
    dict(level='business', title='Cost of the 90% disk rule', stmt='A 20-node cluster has 12 disks of 4 TB per node. The NodeManager disk check marks a disk bad above 90% use. How much raw capacity (TB) sits in that last 10% across the cluster?', inp='20 nodes × 12 × 4 TB · 10%',
         code='''raw_tb = 20 * 12 * 4
print(f"raw {raw_tb} TB, top 10% = {raw_tb * 0.10:.0f} TB")
''', explain='96 TB of 960 TB. That headroom is deliberate: full disks cause failed tasks and slow writes, so admins alert well before 90%.'),
    dict(level='advanced', title='Unit-aware sizes', stmt='Many properties accept units (k, m, g, t). Convert "128m", "1g", "512k" and "134217728" to bytes.', inp='128m · 1g · 512k · 134217728',
         code='''def to_bytes(v):
    units = {"k": 1, "m": 2, "g": 3, "t": 4}
    if v[-1].lower() in units:
        return int(v[:-1]) * 1024 ** units[v[-1].lower()]
    return int(v)
for v in ["128m", "1g", "512k", "134217728"]:
    print(f"{v:>10} -> {to_bytes(v):,} bytes")
''', explain='128m = 134,217,728; 1g = 1,073,741,824; 512k = 524,288; and a plain number is already bytes.'),
]

SCN_INTRO = 'Configuration questions are about reasoning: where does a value come from, and how do you prove it?'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · config</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“I changed dfs.replication to 2 but files still have 3 copies”</h4>
      <p class="scn__situation">An admin edited hdfs-site.xml on the NameNode host. New uploads from the edge node still show replication 3 and old files are unchanged.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> client-side vs server-side settings.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Replication is chosen by the <b>writing client</b> per file. The edge node still has its own hdfs-site.xml with 3.</li>
          <li>Update and distribute the configuration to clients (and all nodes); verify with <code>hdfs getconf -confKey dfs.replication</code> on the edge node.</li>
          <li>Existing files keep their replication; change them with <code>hdfs dfs -setrep -w 2 /path</code> if needed.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“How do you know which value a daemon is using?”</h4>
      <p class="scn__situation">Two engineers disagree about the NodeManager memory setting on a worker.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know how to check instead of guessing?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Open <code>http://&lt;worker&gt;:8042/conf</code>: it shows the value the running NodeManager loaded, and its source file.</li>
          <li>Compare with the file on disk; if they differ, the daemon was not restarted after the change.</li>
          <li>The ResourceManager Nodes page also shows each node's total memory and vcores.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform · governance</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Users keep overriding a cluster setting in their jobs</h4>
      <p class="scn__situation">Some teams submit jobs with very large task memory, starving others. The platform team wants to stop job configurations from overriding certain values.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> what final does and does not do, and the right tools for limits.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Mark cluster-wide values <code>final</code> in the site files on the nodes, so a job's <code>job.xml</code> cannot override them there.</li>
          <li>Know its limit: a client can still set a value directly in its own process, so final is not a security control.</li>
          <li>Enforce limits on the server side: YARN's maximum allocation (<code>yarn.scheduler.maximum-allocation-mb</code>) and queue capacities in the scheduler.</li>
          <li>Monitor usage per queue and review exceptions.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · monitoring</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Set up basic monitoring for a new cluster</h4>
      <p class="scn__situation">A small company has just built a Hadoop cluster and has no monitoring yet.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know where the metrics come from and what matters?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Collect metrics from each daemon's <code>/jmx</code> endpoint (or a Prometheus exporter that reads it).</li>
          <li>Alert on: dead DataNodes, missing or under-replicated blocks, HDFS capacity, safe mode, NodeManagers lost or unhealthy, queue usage and failed applications.</li>
          <li>Dashboards for trends (capacity growth, job durations) and links to the NameNode and ResourceManager UIs for investigation.</li>
        </ul>
      </div></details>
    </article>
'''
