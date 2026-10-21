import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-setup', lesson='01-prerequisites-linux-java-and-ssh', n='4.1',
    module_label='Module 4 · Setup',
    title='Prerequisites: Linux, Java and SSH',
    desc='What a machine needs before Hadoop 3.5 will start: a Linux environment (Ubuntu, WSL 2, a VM or Docker), Java 17 with JAVA_HOME set, and SSH with passwordless keys. Tested install commands, a real prerequisite-check script with before and after output, the three classic start-up errors, and how companies standardise this with images and automation.',
    og_desc='Linux, Java 17 and SSH: the three legs Hadoop stands on. Tested commands, real outputs and the errors everyone hits first.',
    minutes=24, level='Beginner',
    lead='Hadoop is a set of Java programs that run on Linux and start each other over SSH. Miss any one of those three and nothing starts. This lesson prepares a fresh Ubuntu or WSL machine step by step, checks it with a real script (shown before and after), and explains the three error messages beginners see most often, so that installing Hadoop in Lesson 4.3 goes smoothly.',
    chips=['Tested on Ubuntu 24.04', 'Real terminal output', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='A prerequisite checker in Python',
    intro='<p>Real tools such as Ambari and Cloudera Manager run host checks before installing anything. This small version reads facts about a machine (here typed in as a dictionary) and reports what is missing. Run it, then try the challenges.</p>',
    code='''machine = {
    "os": "Ubuntu 24.04.5 LTS",
    "java": 'openjdk version "17.0.20.1" 2026-08-18',
    "java_home": "/usr/lib/jvm/java-17-openjdk-amd64",
    "ram_gb": 7.8,
    "disk_free_gb": 19,
    "ssh_server": True,
    "passwordless_ssh": False,
}

def java_major(line):
    version = line.split('"')[1]          # 17.0.20.1
    first = version.split(".")[0]          # 17
    return int(first)

problems = []
if java_major(machine["java"]) < 17:
    problems.append("Hadoop 3.5 needs Java 17")
if not machine["java_home"]:
    problems.append("JAVA_HOME is not set")
if machine["ram_gb"] < 8:
    problems.append("less than 8 GB RAM: run fewer daemons")
if machine["disk_free_gb"] < 10:
    problems.append("less than 10 GB free disk")
if not machine["ssh_server"]:
    problems.append("install openssh-server")
if not machine["passwordless_ssh"]:
    problems.append("set up passwordless SSH keys")

print("Java major version:", java_major(machine["java"]))
for p in problems:
    print("FIX:", p)
print("Ready!" if not problems else f"{len(problems)} thing(s) to fix")
''',
    anno=[
        ('"java": \'openjdk version "17.0.20.1" 2026-08-18\',', 'This is the exact first line that <code>java -version</code> printed on our test machine.'),
        ('version = line.split(\'"\')[1]          # 17.0.20.1', 'Splitting on the double quote gives three pieces; the version is the middle one.'),
        ('first = version.split(".")[0]          # 17', 'The major version is the part before the first dot. (Old Java 8 printed <code>1.8.0_…</code>; challenge 3 handles that.)'),
        ('if machine["ram_gb"] < 8:', '7.8 GB shows up as “less than 8” because the operating system reserves a little memory. Hadoop still runs; you just run fewer things at once.'),
        ('print("Ready!" if not problems else f"{len(problems)} thing(s) to fix")', 'An empty list counts as False in Python, so <code>not problems</code> means “nothing to fix”.'),
    ],
    tasks=[
        dict(label='1 · Check the machine', hint='Press <b>Run</b>. Then change <code>"passwordless_ssh"</code> to <code>True</code> and run again.', code=None),
        dict(label='2 · Which Java for which Hadoop?', hint='<b>Predict first:</b> which of these Java versions can run Hadoop 3.4 servers, and which can run Hadoop 3.5 servers?',
             code='''supported = {"3.4": [8, 11], "3.5": [17]}     # server-side runtime
for java in [8, 11, 17, 21]:
    ok = [h for h, javas in supported.items() if java in javas]
    where = "Hadoop " + ", ".join(ok) + " servers" if ok else "no servers (Hadoop 3.5 clients only)"
    print(f"Java {java:>2}: {where}")
'''),
        dict(label='3 · Old-style version strings', hint='Java 8 prints <code>openjdk version "1.8.0_412"</code>, so the simple parser says “1”. Fix <code>java_major</code> so that a version starting with <code>1.</code> uses the second number.',
             code='''def java_major(line):
    version = line.split('"')[1]
    return int(version.split(".")[0])

for line in ['openjdk version "17.0.20.1" 2026-08-18',
             'openjdk version "1.8.0_412"',
             'openjdk version "11.0.24" 2024-07-16']:
    print(java_major(line), "<-", line)
'''),
        dict(label='4 · Read a JAVA_HOME', hint='JAVA_HOME must be the folder <i>above</i> <code>bin/java</code>. Given the real path of the java program, work it out.',
             code='''java_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
parts = java_path.split("/")
java_home = "/".join(parts[:-2])
print("export JAVA_HOME=" + java_home)
'''),
        dict(label='5 · Spot the error', hint='This checker says every machine is ready, even one with no Java at all. Find the bug.',
             code='''machine = {"java": "", "java_home": ""}
problems = []
if machine["java"] == None:
    problems.append("install Java")
if machine["java_home"] == None:
    problems.append("set JAVA_HOME")
print(problems or "Ready!")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

_before = '''== Operating system
"Ubuntu 24.04.5 LTS"
== CPU cores
2
== Memory
7.8Gi total, 7.1Gi available
== Free disk in HOME
19G free
== Java
NOT INSTALLED
== JAVA_HOME
not set
== SSH client
NOT INSTALLED
== SSH server
NOT INSTALLED
== Passwordless SSH to localhost
NOT YET (set up keys in Lesson 4.3)'''
_after = '''== Operating system
"Ubuntu 24.04.5 LTS"
== CPU cores
2
== Memory
7.8Gi total, 7.1Gi available
== Free disk in HOME
19G free
== Java
openjdk version "17.0.20.1" 2026-08-18
== JAVA_HOME
/usr/lib/jvm/java-17-openjdk-amd64
== SSH client
installed
== SSH server
installed
== Passwordless SSH to localhost
OK'''

PCRUN = dict(
    heading='Run it on your machine: is it ready for Hadoop?',
    intro='<p>This shell script checks everything from Part 4 in one go. Save it in your Ubuntu or WSL home folder as <code>check_prereqs.sh</code> and run it before and after the install steps. Both outputs below are from a real run on a fresh Ubuntu 24.04 machine.</p>',
    items=[
        dict(title='Before: a fresh Ubuntu 24.04', file='check_prereqs.sh',
             cmd=open(os.path.join(HERE, 'check_prereqs.sh')).read() + '\n# In the Ubuntu / WSL terminal:\n#   bash check_prereqs.sh',
             output=_before,
             note='A brand-new Ubuntu has no Java and no SSH. The memory and disk lines will show your own machine\'s numbers.'),
        dict(title='After: the steps from Part 4 done', file='check_prereqs.sh',
             cmd='sudo apt install -y openjdk-17-jdk-headless openssh-server openssh-client\nsource ~/.bashrc\nsudo service ssh start\n# keys from Lesson 4.3, then:\nbash check_prereqs.sh',
             output=_after,
             note='Every line is now green. The last line needs the SSH keys from Lesson 4.3; it is included here so you can re-use the same script later. Your Java patch number may be newer than 17.0.20.1.'),
    ],
)

TRACE = dict(
    heading='Reading a version string, one step at a time',
    intro='<p>Follow the real <code>java -version</code> line through the parser and watch each variable change in memory.</p>',
    code='''line = 'openjdk version "17.0.20.1" 2026-08-18'
pieces = line.split('"')
version = pieces[1]
major = int(version.split(".")[0])
needed = 17
if major >= needed:
    print("Java", major, "is fine for Hadoop 3.5")
else:
    print("Java", major, "is too old")
''',
    notes={1: 'Input :: The exact text Java printed on the test machine.',
           2: 'Split :: Three pieces: before the quote, the version, after the quote.',
           3: 'Pick :: Index 1 is the middle piece.',
           4: 'Convert :: Text “17” becomes the number 17 so it can be compared.',
           6: 'Decide :: 17 ≥ 17, so the check passes.'},
)

WORKED_INTRO = 'Three jobs a Hadoop admin really does before installing: checking a list of machines, sizing memory for the daemons, and generating the environment lines every node needs. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Admin · host check', title='Which lab machines are ready?',
         problem='<p>A college lab has four machines. Each needs Java 17 or newer, at least 8 GB RAM and 20 GB of free disk to join the Hadoop practice cluster. List which are ready and what each of the others is missing.</p>',
         inp='lab1: Java 17, 16 GB, 120 GB · lab2: Java 11, 16 GB, 80 GB · lab3: Java 17, 4 GB, 50 GB · lab4: Java 21, 32 GB, 10 GB',
         approach=['Store each machine as a tuple of (java, ram, disk).',
                   'Check the three rules and collect what fails.',
                   'Print “ready” or the list of problems.'],
         code='''machines = {"lab1": (17, 16, 120), "lab2": (11, 16, 80),
            "lab3": (17, 4, 50), "lab4": (21, 32, 10)}
for name, (java, ram, disk) in machines.items():
    missing = []
    if java < 17: missing.append("Java 17")
    if ram < 8: missing.append("RAM")
    if disk < 20: missing.append("disk")
    print(f"{name}: {'ready' if not missing else 'needs ' + ', '.join(missing)}")
''', notes={4: 'Collect :: Start each machine with an empty list of problems.'},
         tryit='lab4 has Java 21. Hadoop 3.5 supports 21 on the client side only; would you use it as a DataNode? (Servers need JDK 17.)'),
    dict(level='i', tag='Admin · memory sizing', title='Will the daemons fit in RAM?',
         problem='<p>A pseudo-distributed setup runs NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager and the JobHistory Server on one 8 GB laptop. Each daemon is given a 1 GB Java heap, the operating system needs 2 GB, and each task container needs 1 GB. How many containers can run at once?</p>',
         inp='8 GB RAM · 6 daemons × 1 GB · OS 2 GB · 1 GB per container',
         approach=['Add up daemon heaps and the OS.',
                   'Subtract from total RAM.',
                   'Whole containers that fit = floor(left / 1 GB).'],
         code='''ram = 8
daemons = ["NameNode", "DataNode", "SecondaryNameNode",
           "ResourceManager", "NodeManager", "JobHistoryServer"]
used = len(daemons) * 1 + 2          # heaps + OS
left = ram - used
containers = int(left // 1)
print(f"Daemons + OS use {used} GB, {left} GB left -> {containers} containers at a time")
''', notes={5: 'Fixed cost :: Six daemons and the OS, before any job runs.'},
         tryit='With 0 containers left, a submitted job would wait for ever. Try ram = 16. This is why 8 GB is the practical minimum and 16 GB is comfortable.'),
    dict(level='a', tag='Automation · config', title='Generate the environment lines for every node',
         problem='<p>A team sets up 5 worker nodes. Each node\'s <code>~/.bashrc</code> needs JAVA_HOME, HADOOP_HOME and a PATH line, and the Java folder differs by CPU type: <code>amd64</code> on Intel/AMD machines, <code>arm64</code> on ARM machines. Generate the lines for each node from a table, the way automation tools do.</p>',
         inp='w1–w3: amd64 · w4–w5: arm64 · Hadoop in /opt/hadoop-3.5.0',
         approach=['Keep the per-node difference (CPU type) in data.',
                   'Build the lines from one template.',
                   'Print them per node so they can be copied or pushed by a tool.'],
         code='''nodes = {"w1": "amd64", "w2": "amd64", "w3": "amd64",
         "w4": "arm64", "w5": "arm64"}
template = ("export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-{arch}\\n"
            "export HADOOP_HOME=/opt/hadoop-3.5.0\\n"
            "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin")
for name, arch in nodes.items():
    print(f"# {name}")
    print(template.format(arch=arch))
''', notes={6: 'Template :: One text with a hole; <code>format</code> fills it per node.'},
         tryit='Add a node "w6": "arm64". In real companies this table lives in Ansible inventory or a container image, so no one types these lines by hand.'),
]

QUIZ = mix([
    dict(q='Which Java version do Hadoop 3.5 servers (NameNode, DataNode…) require?', options=['Java 8', 'Java 11', 'JDK 17', 'Any version'], answer=2,
         why='Hadoop 3.5 moved the server side to JDK 17; clients can use 17 or 21. Hadoop 3.3 and 3.4 run on Java 8 or 11.'),
    dict(q='What should JAVA_HOME point to?', options=['The java program itself, e.g. …/bin/java', 'The Java installation folder, e.g. /usr/lib/jvm/java-17-openjdk-amd64', 'Your home folder', 'The Hadoop folder'], answer=1,
         why='JAVA_HOME is the folder that contains bin/java. Hadoop adds bin/java itself.'),
    dict(q='Why do Hadoop\'s start scripts need SSH, even on one machine?', options=['To download Hadoop', 'start-dfs.sh logs in to each worker listed (even localhost) to start its daemon', 'SSH encrypts HDFS blocks', 'Java needs SSH'], answer=1,
         why='The scripts use SSH to run commands on every host in the workers file. On one machine that host is localhost.'),
    dict(q='You see “localhost: ERROR: JAVA_HOME is not set and could not be found.” even though java -version works. Why?', options=['Java is broken', 'Commands started over SSH do not read your interactive shell settings, so set JAVA_HOME in hadoop-env.sh', 'The disk is full', 'Hadoop needs Java 8'], answer=1,
         why='A non-interactive SSH session may not load ~/.bashrc. Setting JAVA_HOME in etc/hadoop/hadoop-env.sh fixes it for every daemon.'),
    dict(q='“Permission denied (publickey,password)” during start-dfs.sh means:', options=['HDFS permissions are wrong', 'Passwordless SSH to the host is not set up', 'Java is missing', 'The NameNode is in safe mode'], answer=1,
         why='The script tried to SSH in without a password and failed. Create a key and add it to ~/.ssh/authorized_keys.'),
    dict(q='On Windows, the recommended way to practise Hadoop is:', options=['Run Hadoop directly on Windows', 'WSL 2 with Ubuntu, or Docker', 'Only on a rented cloud cluster', 'Inside a browser'], answer=1,
         why='Hadoop is built and tested for Linux. WSL 2 gives a real Ubuntu on Windows; Docker gives ready images.'),
    dict(q='Which package provides the java command on Ubuntu without a desktop GUI?', options=['openjdk-17-jre-gui', 'openjdk-17-jdk-headless', 'java-desktop', 'hadoop-java'], answer=1,
         why='“headless” means no graphical libraries, which servers don\'t need. The JDK also includes tools such as jps.'),
    dict(q='What does the jps command (part of the JDK) show?', options=['Java packages installed', 'The Java processes running, such as NameNode and DataNode', 'Your Java licence', 'Network ports'], answer=1,
         why='jps lists running JVMs by class name. It is the quickest check that Hadoop daemons started.'),
])

REVISION = [
    'Hadoop needs three things: <b>Linux</b>, <b>Java</b> and <b>SSH</b>.',
    'Java: Hadoop <b>3.5 servers need JDK 17</b> (clients 17 or 21); Hadoop 3.3/3.4 run on Java 8 or 11.',
    '<code>JAVA_HOME</code> = the folder <i>above</i> <code>bin/java</code>, e.g. <code>/usr/lib/jvm/java-17-openjdk-amd64</code>.',
    'Set JAVA_HOME in <code>~/.bashrc</code> <b>and</b> in <code>etc/hadoop/hadoop-env.sh</code> (SSH sessions skip your shell settings).',
    'SSH: start scripts log in to every host in <code>workers</code>, even <code>localhost</code>. Keys must be passwordless.',
    'Windows: use <b>WSL 2 + Ubuntu</b> or <b>Docker</b>. Linux PC: Ubuntu LTS directly.',
    'Install: <code>sudo apt install -y openjdk-17-jdk-headless openssh-server openssh-client wget</code>.',
    'Practical minimum: 8 GB RAM (16 GB comfortable), ~20 GB free disk.',
    'Check with <code>java -version</code>, <code>echo $JAVA_HOME</code>, <code>ssh localhost</code>, and <code>jps</code> after start-up.',
]
FAQ = [
    ('Can Hadoop run on Windows?', 'Hadoop can be built for Windows, but it needs extra native files (winutils) and is not how companies run it. For learning, use WSL 2 with Ubuntu or Docker on Windows; in production, Hadoop runs on Linux.'),
    ('Which Java should I install for Hadoop?', 'Match the Hadoop version. Hadoop 3.5 requires JDK 17 on the server side (clients may use 17 or 21). Hadoop 3.3 and 3.4 support Java 8 and 11 at runtime. Check the “Hadoop Java Versions” page on the Apache wiki for the version you install.'),
    ('Why does Hadoop need SSH?', 'Only the convenience start and stop scripts (start-dfs.sh, start-yarn.sh) use it: they SSH into every host listed in the workers file to start or stop the daemons. Daemons can also be started on each node directly with “hdfs --daemon start datanode”, which is what service managers and containers do.'),
    ('What is the difference between the JDK and the JRE?', 'The JRE only runs Java programs. The JDK adds development and diagnostic tools such as javac, jps and jstack. Install the JDK: jps is used constantly to check Hadoop daemons, and some tools need javac.'),
    ('How do I find JAVA_HOME on Ubuntu?', 'Run readlink -f $(which java). It prints something like /usr/lib/jvm/java-17-openjdk-amd64/bin/java; JAVA_HOME is that path without the final /bin/java.'),
    ('How much RAM do I need to practise Hadoop?', '8 GB is a practical minimum for a single-machine (pseudo-distributed) setup with small jobs; 16 GB is comfortable. Each daemon is a separate Java process with its own heap, and each task runs in its own container.'),
    ('Why “headless” Java?', 'The headless package leaves out graphical (desktop) libraries. Servers have no screen, so headless is smaller and has fewer security updates to track.'),
    ('How do companies prepare hundreds of nodes?', 'They do not type commands by hand. A standard operating-system image, configuration management (Ansible, Puppet, Chef) or a cluster manager (Cloudera Manager, Ambari historically) installs the same Java, users, SSH keys, limits and settings on every node, and runs host checks before adding a node.'),
]

PRACTICE_INTRO = 'Small, practical exercises around versions, paths, memory and checks. Each can be run in the browser.'
PROBLEMS = [
    dict(level='easy', title='Strip /bin/java', stmt='Given the path /usr/lib/jvm/java-17-openjdk-amd64/bin/java, print JAVA_HOME.', inp='/usr/lib/jvm/java-17-openjdk-amd64/bin/java',
         code='p = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"\nprint(p.removesuffix("/bin/java"))\n', explain='JAVA_HOME is /usr/lib/jvm/java-17-openjdk-amd64: the folder that contains bin/java.'),
    dict(level='easy', title='Major version', stmt='Print the major version from the line openjdk version "17.0.20.1" 2026-08-18.', inp='openjdk version "17.0.20.1" 2026-08-18',
         code='line = \'openjdk version "17.0.20.1" 2026-08-18\'\nprint(int(line.split(\'"\')[1].split(".")[0]))\n', explain='17: the text between the quotes is 17.0.20.1, and the part before the first dot is 17.'),
    dict(level='easy', title='Java for the version', stmt='Write a function that returns the server-side Java versions for Hadoop "3.4" and "3.5".', inp='"3.4" · "3.5"',
         code='''def java_for(hadoop):
    return {"3.3": [8, 11], "3.4": [8, 11], "3.5": [17]}[hadoop]
print("3.4 ->", java_for("3.4"))
print("3.5 ->", java_for("3.5"))
''', explain='Hadoop 3.4 runs on Java 8 or 11; Hadoop 3.5 servers require JDK 17.'),
    dict(level='medium', title='Parse free -h', stmt='The memory line from free -h is "Mem: 7.8Gi 512Mi 6.9Gi 2.0Mi 418Mi 7.1Gi". Print the total and available values (columns 2 and 7).', inp='Mem: 7.8Gi 512Mi 6.9Gi 2.0Mi 418Mi 7.1Gi',
         code='''cols = "Mem: 7.8Gi 512Mi 6.9Gi 2.0Mi 418Mi 7.1Gi".split()
print("total", cols[1], "available", cols[6])
''', explain='total 7.8Gi, available 7.1Gi. Python counts from 0, so column 2 is index 1 and column 7 is index 6, exactly what the awk in check_prereqs.sh prints.'),
    dict(level='medium', title='Check a bashrc', stmt='Given the lines of a ~/.bashrc, report which of JAVA_HOME, HADOOP_HOME and PATH are exported.', inp='export JAVA_HOME=… · alias ll=…',
         code='''bashrc = ["alias ll='ls -l'",
          "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"]
for var in ["JAVA_HOME", "HADOOP_HOME", "PATH"]:
    found = any(l.startswith(f"export {var}=") for l in bashrc)
    print(var, "set" if found else "MISSING")
''', explain='JAVA_HOME is set; HADOOP_HOME and PATH are missing. Add them as in Part 4, step 4.'),
    dict(level='medium', title='Free-disk rule', stmt='A machine has 19 GB free. The Hadoop 3.5.0 download (0.6 GB) plus the unpacked folder (1.3 GB) plus at least 10 GB for HDFS data and logs are needed. Is there enough space, and how much is left over?', inp='19 GB free · 0.6 + 1.3 + 10 GB',
         code='''need = 0.6 + 1.3 + 10
print(f"need {need:.1f} GB, enough: {19 >= need}, spare {19 - need:.1f} GB")
''', explain='About 11.9 GB is needed, so 19 GB is enough with about 7.1 GB to spare. (The sizes are from the real 3.5.0 tarball and its unpacked folder.)'),
    dict(level='business', title='Setup time saved by automation', stmt='Setting up one node by hand takes 45 minutes. An automated image takes 2 hours to build once and 5 minutes per node. For 40 nodes, how many hours does automation save?', inp='45 min/node by hand · 2 h + 5 min/node automated · 40 nodes',
         code='''by_hand = 40 * 45 / 60
auto = 2 + 40 * 5 / 60
print(f"by hand {by_hand:.1f} h, automated {auto:.1f} h, saved {by_hand - auto:.1f} h")
''', explain='By hand 30 h, automated about 5.3 h: about 24.7 hours saved, and every node is identical, which matters more than the time.'),
    dict(level='advanced', title='Mixed-version cluster check', stmt='An upgrade plan to Hadoop 3.5 lists nodes and their Java versions. Print the nodes that would fail to start as servers and those that may only be clients.', inp='nn1: 17 · dn1: 11 · dn2: 17 · edge1: 21',
         code='''nodes = {"nn1": ("server", 17), "dn1": ("server", 11),
         "dn2": ("server", 17), "edge1": ("client", 21)}
for name, (role, java) in nodes.items():
    ok = java == 17 if role == "server" else java in (17, 21)
    print(f"{name:6} {role:6} Java {java}: {'OK' if ok else 'UPGRADE JAVA'}")
''', explain='Only dn1 (a server on Java 11) must be upgraded before moving to 3.5. The edge node on Java 21 is fine as a client.'),
]

SCN_INTRO = 'Setup problems are a favourite in support and admin interviews: the interviewer shows an error and asks what you would check.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · troubleshooting</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“java -version works, but start-dfs.sh says JAVA_HOME is not set”</h4>
      <p class="scn__situation">A new team member runs start-dfs.sh and gets “localhost: ERROR: JAVA_HOME is not set and could not be found.” three times. In the same terminal, java -version prints Java 17.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know that the daemons are started through SSH sessions that may not read your shell settings?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>java being on the PATH is not the same as JAVA_HOME being set, and the start script runs commands over SSH, which may not load ~/.bashrc.</li>
          <li>Find the folder with <code>readlink -f $(which java)</code> and remove <code>/bin/java</code>.</li>
          <li>Set <code>export JAVA_HOME=…</code> in <code>$HADOOP_HOME/etc/hadoop/hadoop-env.sh</code>, so every daemon gets it.</li>
          <li>Re-run start-dfs.sh and confirm with <code>jps</code>.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Admin · SSH</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Permission denied (publickey,password)”</h4>
      <p class="scn__situation">start-dfs.sh prints “localhost: Permission denied (publickey,password).” for the NameNode, DataNode and SecondaryNameNode.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand passwordless SSH and the files involved?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The script tried to log in to localhost without a password and was refused.</li>
          <li>Check the SSH server is running (<code>sudo service ssh status</code>).</li>
          <li>Create a key with <code>ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa</code> and append the public key to <code>~/.ssh/authorized_keys</code>; set <code>chmod 600</code> on that file.</li>
          <li>Test with <code>ssh localhost true</code>: it must return without asking anything.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform · upgrade</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Planning a move from Hadoop 3.4 to 3.5</h4>
      <p class="scn__situation">Your company runs Hadoop 3.4 on Java 11 across 60 nodes and wants to upgrade to 3.5.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know that 3.5 changes the Java requirement, and do you plan for it?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Hadoop 3.5 servers require JDK 17, so Java must be upgraded on every server node first; clients can use 17 or 21.</li>
          <li>Check every application and library that runs inside the cluster (UDFs, custom jars, Spark/Hive versions) for Java 17 compatibility.</li>
          <li>Upgrade a test cluster first, then roll out with the standard image or configuration management, so no node is missed.</li>
          <li>Keep a rollback plan and run host checks before and after.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Learning · environment</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“I only have a Windows laptop. How do I practise?”</h4>
      <p class="scn__situation">A student with an 8 GB Windows laptop asks how to set up Hadoop for practice.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you suggest a realistic, low-cost setup?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Install WSL 2 with Ubuntu 24.04 (<code>wsl --install -d Ubuntu-24.04</code>); it is a real Linux kernel on Windows.</li>
          <li>Inside Ubuntu, install JDK 17 and SSH, set JAVA_HOME, and run Hadoop in pseudo-distributed mode.</li>
          <li>With 8 GB, keep jobs small and stop daemons you are not using; Docker images are an alternative if Docker Desktop is available.</li>
          <li>Native Windows Hadoop is not worth the trouble for learning.</li>
        </ul>
      </div></details>
    </article>
'''
