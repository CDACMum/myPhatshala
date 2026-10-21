import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Explore a small cluster',
    intro='<p>Two racks, three DataNodes in each, and master nodes at the top. A 1 GB file is already stored. Pink dots are <b>heartbeats</b>: every node tells the NameNode “I am alive” every 3 seconds.</p>',
    racks=2, nodes=3, features=['upload'],
    preload=[dict(name='upi_txns_2025.csv', sizeMB=1024)],
    **{'try': [
        dict(text='Find the two <b>ToR switches</b> and the <b>core switch</b>. Which wires does a heartbeat from DN5 travel on?'),
        dict(text='Choose 300 MB and press <b>Upload to HDFS</b>. Watch each block travel Client → core → ToR → node.', on='upload-done'),
        dict(text='Open <b>NameNode metadata</b>: is any block stored on only one rack? (Answer: no. Lesson 1.4 explains why.)'),
    ]},
)))

META = dict(
    module='01-foundations', lesson='01-server-node-rack-and-data-centre', n='1.1',
    module_label='Module 1 · Foundations: before Hadoop',
    title='Server, node, rack and data centre',
    desc='What a server, node, rack and data centre are, what is inside a Hadoop worker node, how racks are wired with ToR and core switches, and why the rack matters to Hadoop. With animations, a cluster playground, Python you can run, quiz and interview scenarios.',
    og_desc='Hall, rack, server: the physical building blocks of every Hadoop cluster, and why the rack matters.',
    minutes=22, level='Beginner → Intermediate',
    lead='Before Hadoop, meet the hardware it runs on. This lesson walks through a data centre: servers stacked in racks, a switch on top of each rack, core switches joining the racks. You will see what is inside a typical Hadoop worker node, why traffic inside a rack is cheaper than traffic between racks, and why Hadoop treats a rack as one unit that can fail.',
    chips=['Cluster Playground', 'Runs in your browser (Python)', 'Check your own PC'],
)

RUN = dict(
    heading='Describe a cluster in Python',
    intro='<p>A cluster is just data about machines: which nodes exist, which rack each is on, and what each one has. Here is a small cluster as a Python dictionary, and its total capacity. Then try the challenges.</p>',
    code='''cluster = {
    "/rack1": [{"name": "dn1", "cores": 32, "ram": 256, "disk_tb": 144},
               {"name": "dn2", "cores": 32, "ram": 256, "disk_tb": 144}],
    "/rack2": [{"name": "dn3", "cores": 32, "ram": 256, "disk_tb": 144},
               {"name": "dn4", "cores": 64, "ram": 512, "disk_tb": 192}],
}

nodes = [n for rack in cluster.values() for n in rack]
print("Racks :", len(cluster))
print("Nodes :", len(nodes))
print("Cores :", sum(n["cores"] for n in nodes))
print("RAM   :", sum(n["ram"] for n in nodes), "GB")
print("Disk  :", sum(n["disk_tb"] for n in nodes), "TB raw")
''',
    anno=[
        ('cluster = {', 'A dictionary: the key is the rack name, the value is the list of nodes in that rack. Hadoop stores its view of the cluster in a similar tree.'),
        ('nodes = [n for rack in cluster.values() for n in rack]', 'A list comprehension with two <code>for</code>s: for every rack, take every node. It flattens the racks into one list of nodes.'),
        ('sum(n["cores"] for n in nodes)', 'Add up one field across all nodes. The same pattern gives RAM and disk.'),
    ],
    tasks=[
        dict(label='1 · Cluster totals', hint='Press <b>Run</b>. Then add a third rack <code>"/rack3"</code> with two more nodes and run again.', code=None),
        dict(label='2 · Which rack?', hint='<b>Predict first:</b> what does this print for <code>dn3</code> and for <code>dn9</code>? Hadoop gives an unknown host the rack <code>/default-rack</code>.',
             code='''rack_of = {"dn1": "/rack1", "dn2": "/rack1", "dn3": "/rack2", "dn4": "/rack2"}

def find_rack(host):
    return rack_of.get(host, "/default-rack")

for h in ["dn3", "dn9"]:
    print(h, "->", find_rack(h))
print("dn1 and dn2 same rack?", find_rack("dn1") == find_rack("dn2"))
'''),
        dict(label='3 · Copy time', hint='How long does a 10 GB copy take at 25 Gbps? And when 40 servers share a 400 Gbps uplink? Change <code>servers_sending</code> to 10 and 80.',
             code='''gb = 10
port_gbps = 25
uplink_gbps = 400
servers_sending = 40

def seconds(gb, gbps):
    return gb * 8 / gbps            # bytes to bits: multiply by 8

alone = seconds(gb, port_gbps)
share = min(port_gbps, uplink_gbps / servers_sending)
print(f"Alone            : {alone:.1f} s")
print(f"Shared uplink    : {seconds(gb, share):.1f} s (each gets {share:.0f} Gbps)")
'''),
        dict(label='4 · Fill a rack', hint='A 42U rack keeps 2U for the switch and cables. How many 2U servers fit by space? How many by power (10 kW, 450 W each)? The smaller number wins.',
             code='''rack_u, reserved_u, server_u = 42, 2, 2
rack_watts, server_watts = 10_000, 450

by_space = (rack_u - reserved_u) // server_u
by_power = rack_watts // server_watts
print("By space:", by_space, "servers")
print("By power:", by_power, "servers")
print("You can install:", min(by_space, by_power))
'''),
        dict(label='5 · Spot the error', hint='This crashes. Read the error, then fix it two ways: add the missing host, or use <code>.get()</code> with a default like task 2.',
             expect='error',
             code='''rack_of = {"dn1": "/rack1", "dn2": "/rack1", "dn3": "/rack2"}
hosts = ["dn1", "dn3", "dn4"]
for h in hosts:
    print(h, "is on", rack_of[h])
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: look at your computer as a node',
    intro='<p>An administrator\'s first question about any node is: how many cores, how much RAM, how much disk? This program answers it for your computer (Windows, macOS or Linux) and compares it with a typical Hadoop worker node. Save it as <code>node_report.py</code> and run it.</p>',
    items=[
        dict(title='How does your machine compare with a worker node?', file='node_report.py',
             cmd=open(os.path.join(HERE, 'node_report.py')).read() + '\n# In a terminal:  python node_report.py',
             output='''Host name : vm
OS        : Linux
CPU cores : 2
RAM       : 7.8 GB
Disk      : 0.25 TB

One typical worker node equals about:
  16 of your machines in CPU cores
  33 of your machines in RAM
  585 of your machines in disk''',
             note='Recorded on a small cloud machine (2 cores, 8 GB RAM, 256 GB disk). On a laptop you will see your own numbers. The disk gap is the biggest: Hadoop worker nodes are built to hold a lot of data, with many disks each.'),
    ],
)

TRACE = dict(
    heading='Counting a cluster, one line at a time',
    intro='<p>Watch the loop visit each rack, then each node inside it, adding up the cores. Notice the dictionary and the lists appear as numbered objects.</p>',
    code='''racks = {"/rack1": [32, 32], "/rack2": [64]}
total = 0
for rack, cores in racks.items():
    for c in cores:
        total = total + c
    print(rack, "done, running total", total)
print("Cluster cores:", total)
''',
    notes={1: 'Data :: Each rack maps to a list of core counts, one number per node.',
           (3, 1): 'Outer loop :: First rack: <code>/rack1</code>.',
           (3, 2): 'Outer loop :: Next rack: <code>/rack2</code>.'},
)

WORKED_INTRO = 'Three calculations that cluster and data-centre teams do in real life: an inventory, usable storage, and how many servers a rack can really take. Each program runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Operations · inventory', title='How big is each rack?',
         problem='<p>The operations team has a list of servers with their rack and number of cores. Print how many nodes and cores each rack has.</p>',
         inp='dn1 r1 32, dn2 r1 32, dn3 r2 32, dn4 r2 64, dn5 r2 32',
         approach=['Start with an empty dictionary for the result.',
                   'For each server, create the rack entry if it is new, then add one node and its cores.',
                   'Print one line per rack.'],
         code='''servers = [("dn1", "r1", 32), ("dn2", "r1", 32), ("dn3", "r2", 32),
           ("dn4", "r2", 64), ("dn5", "r2", 32)]
racks = {}
for name, rack, cores in servers:
    if rack not in racks:
        racks[rack] = [0, 0]
    racks[rack][0] += 1
    racks[rack][1] += cores
for rack, (n, c) in racks.items():
    print(rack, ":", n, "nodes,", c, "cores")
''', notes={3: 'Result :: An empty dictionary will hold [nodes, cores] for each rack.'},
         tryit='Add a server <code>("dn6", "r3", 48)</code>. A new rack appears automatically.'),
    dict(level='i', tag='Storage planning · capacity', title='How much data can the cluster really hold?',
         problem='<p>A cluster has 20 worker nodes with 12 disks of 12 TB each. HDFS keeps <b>3 copies</b> of every block, and the team keeps <b>25%</b> of space free for temporary files and growth. How much data can the business actually store?</p>',
         inp='20 nodes · 12 disks × 12 TB · replication 3 · 25% headroom',
         approach=['Raw capacity = nodes × disks × disk size.',
                   'Keep 25% free: multiply by 0.75.',
                   'Divide by 3 because every block is stored three times.'],
         code='''nodes, disks, disk_tb = 20, 12, 12
replication, headroom = 3, 0.25

raw = nodes * disks * disk_tb
usable = raw * (1 - headroom)
data = usable / replication
print("Raw disk      :", raw, "TB")
print("After headroom:", usable, "TB")
print("Business data :", data, "TB")
''', notes={5: 'Raw :: 20 × 12 × 12 TB.', 7: 'Copies :: Each TB of business data uses 3 TB of disk.'},
         tryit='What if the team used replication 2? Why might they still say no? (Hint: Lesson 1.4.)'),
    dict(level='a', tag='Data centre · rack planning', title='Space, power or switch ports: what limits a rack?',
         problem='<p>A 42U rack keeps 2U for the ToR switch and cable management. Servers are 2U, draw 450 W each, and need one switch port each. The rack has a 9 kW power budget and the switch has 48 ports. How many servers can go in, and which limit is reached first?</p>',
         inp='42U − 2U · 2U servers · 9,000 W, 450 W each · 48 ports',
         approach=['Work out the limit from each resource separately.',
                   'Store them in a dictionary.',
                   'The smallest limit is the real one; <code>min</code> with <code>key=</code> finds its name.'],
         code='''limits = {
    "space": (42 - 2) // 2,
    "power": 9000 // 450,
    "ports": 48,
}
for what, n in limits.items():
    print(f"{what:6}: {n} servers")
binding = min(limits, key=limits.get)
print("Limit reached first:", binding, "->", limits[binding], "servers")
''', notes={1: 'Limits :: One dictionary, three independent limits.', 7: 'Decide :: <code>min(limits, key=limits.get)</code> returns the key whose value is smallest.'},
         tryit='Switch to 1U servers that draw 350 W. Which limit wins now? Many real racks are limited by power, not space.'),
]

QUIZ = mix([
    dict(q='In a Hadoop cluster, one server that is part of the cluster is called a:', options=['Rack', 'Node', 'Switch', 'Region'], answer=1,
         why='Each machine in a cluster is a <b>node</b>. Racks hold many nodes.'),
    dict(q='What does the ToR switch connect?', options=['All data centres in a country', 'All the servers inside one rack, and the rack to the core network', 'The CPU to the RAM', 'Only the master nodes'], answer=1,
         why='The <b>top-of-rack</b> switch links every server in its rack and has uplinks to the core (spine) switches.'),
    dict(q='Why is traffic between two nodes in the same rack usually faster than between racks?', options=['Same-rack nodes share a CPU', 'It goes only through the ToR switch and avoids the shared, oversubscribed uplinks', 'Racks are always in different cities', 'Cross-rack data is encrypted twice'], answer=1,
         why='Same-rack traffic stays inside one switch. Cross-rack traffic must use uplinks that are shared by all servers in the rack.'),
    dict(q='A ToR switch has 48 ports of 25 Gbps to servers and 4 uplinks of 100 Gbps. The oversubscription ratio is:', options=['1 : 1', '2 : 1', '3 : 1', '12 : 1'], answer=2,
         why='Down: 48 × 25 = 1,200 Gbps. Up: 4 × 100 = 400 Gbps. 1,200 ÷ 400 = <b>3 : 1</b>.'),
    dict(q='Why do Hadoop worker nodes usually use plain disks (JBOD) instead of RAID?', options=['RAID is not supported by Linux', 'HDFS already keeps copies on other nodes, and separate disks can be read in parallel', 'JBOD disks never fail', 'RAID is only for laptops'], answer=1,
         why='HDFS replicates blocks across nodes, so RAID inside a worker adds cost without much benefit, and independent disks give more parallel read speed.'),
    dict(q='Why does Hadoop care which rack a node is in?', options=['To show the rack colour in the web UI', 'A rack can fail as a unit (power or switch), and cross-rack bandwidth is limited', 'Each rack runs a different version of Hadoop', 'Racks decide the file names'], answer=1,
         why='The rack is both a <b>failure domain</b> and a <b>bandwidth boundary</b>, so HDFS and the scheduler use it when placing data and tasks.'),
    dict(q='If no rack-topology script is configured, Hadoop puts every node in:', options=['/rack1', '/default-rack', '/unknown', 'no rack, and refuses to start'], answer=1,
         why='Without a topology script, every node is in <code>/default-rack</code>, so Hadoop cannot spread copies across racks.'),
    dict(q='1U, the height unit of a rack, is:', options=['1 cm', '1.75 inches (4.445 cm)', '1 foot', 'One server, whatever its size'], answer=1,
         why='1U = 1.75 inches. A 42U rack is about 2 metres tall including its frame.'),
])

REVISION = [
    '<b>Server</b>: computer that runs 24×7 for others. In a cluster it is a <b>node</b>.',
    '<b>Rack</b>: cabinet (often 42U) of 20–40 servers with shared power and a <b>ToR switch</b>.',
    '<b>Data centre</b>: building with many racks, backup power, cooling, security and core switches.',
    'Typical worker node: 32–64 cores, 128–512 GB RAM, 8–24 plain disks, 10–25 Gbps network.',
    'Masters (NameNode, ResourceManager) get safer hardware; workers (DataNode, NodeManager) get many disks and cores.',
    'Same rack: through one switch, full speed. Across racks: through shared, <b>oversubscribed</b> uplinks.',
    'A rack is a <b>failure domain</b>: HDFS keeps copies on at least two racks.',
    'Hadoop learns racks from a topology script (<code>net.topology.script.file.name</code>); otherwise <code>/default-rack</code>.',
]
FAQ = [
    ('What is the difference between a server and a node?', 'A server is any computer that serves others over a network. A node is a server (or VM) when it is a member of a cluster. All Hadoop nodes are servers; not every server is a Hadoop node.'),
    ('What is a rack, and why is it important in Hadoop?', 'A rack is a cabinet holding many servers with shared power and a top-of-rack switch. It matters because all servers in a rack can fail together (switch or power failure) and because bandwidth between racks is limited. HDFS places block replicas on more than one rack, and the scheduler prefers nodes on the same rack as the data.'),
    ('What hardware would you choose for a Hadoop worker node?', 'Many CPU cores, enough RAM for the tasks that will run (128–512 GB is common), many large plain hard disks in JBOD (not RAID), and a 10–25 Gbps network card. Masters need more RAM, RAID-protected disks for metadata and redundant power instead.'),
    ('What is oversubscription?', 'When the total bandwidth of a switch\'s server ports is larger than its uplink bandwidth. For example 48 × 25 Gbps down and 4 × 100 Gbps up is 3:1. If all servers send traffic out of the rack at once, each gets only a fraction of its port speed.'),
    ('How does Hadoop know which rack a node is on?', 'An administrator configures a topology script or class (net.topology.script.file.name) that maps host names or IP addresses to rack paths like /dc1/rack1. Without it, all nodes are placed in /default-rack.'),
]

PRACTICE_INTRO = 'Quick calculations about servers, racks and networks. The last ones are the kind of planning a platform team does before buying hardware.'
PROBLEMS = [
    dict(level='easy', title='Rack height in centimetres', stmt='1U is 4.445 cm. How tall, in centimetres, is the usable space of a 42U rack?', inp='42U, 1U = 4.445 cm',
         code='print(round(42 * 4.445, 1), "cm")\n', explain='42 × 4.445 = 186.7 cm. With the frame, top and wheels, a 42U rack is about 2 metres tall.'),
    dict(level='easy', title='Raw capacity of one node', stmt='A node has 12 disks of 16 TB. What is its raw capacity in TB?', inp='12 disks × 16 TB',
         code='print(12 * 16, "TB")\n', explain='Raw capacity is just disks × size. Usable capacity is lower (replication and free space), as in worked example 2.'),
    dict(level='easy', title='Bits and bytes', stmt='A network link is 10 Gbps (gigabits per second). How many GB (gigabytes) per second is that?', inp='10 Gbps',
         code='print(10 / 8, "GB per second")\n', explain='8 bits make 1 byte, so divide by 8: 10 Gbps = 1.25 GB/s. Network speeds are quoted in bits, disk speeds in bytes.'),
    dict(level='medium', title='Oversubscription ratio', stmt='A ToR switch has 40 servers on 25 Gbps ports and 4 uplinks of 100 Gbps. Print the ratio as “N : 1”.', inp='40 × 25 Gbps, 4 × 100 Gbps',
         code='''down = 40 * 25
up = 4 * 100
print(f"{down / up:g} : 1")
''', explain='1,000 ÷ 400 = 2.5. When every server sends out of the rack at once, each gets 25 ÷ 2.5 = 10 Gbps.'),
    dict(level='medium', title='Group hosts by rack', stmt='Given a host-to-rack map, print the hosts of each rack in sorted order.', inp='{"dn3": "/r2", "dn1": "/r1", "dn4": "/r2", "dn2": "/r1", "dn5": "/r3"}',
         code='''rack_of = {"dn3": "/r2", "dn1": "/r1", "dn4": "/r2", "dn2": "/r1", "dn5": "/r3"}
by_rack = {}
for host, rack in rack_of.items():
    by_rack.setdefault(rack, []).append(host)
for rack in sorted(by_rack):
    print(rack, sorted(by_rack[rack]))
''', explain='<code>setdefault</code> creates an empty list the first time a rack appears. This reverse map (rack → hosts) is how you check that a cluster is balanced across racks.'),
    dict(level='medium', title='Same rack or not?', stmt='Write a function <code>hops(a, b)</code> that returns 0 if a and b are the same host, 2 if they are on the same rack, and 4 otherwise. Test it on (dn1, dn1), (dn1, dn2) and (dn1, dn3).', inp='rack_of = {dn1: r1, dn2: r1, dn3: r2}',
         code='''rack_of = {"dn1": "r1", "dn2": "r1", "dn3": "r2"}

def hops(a, b):
    if a == b:
        return 0
    if rack_of[a] == rack_of[b]:
        return 2
    return 4

for a, b in [("dn1", "dn1"), ("dn1", "dn2"), ("dn1", "dn3")]:
    print(a, b, "->", hops(a, b), "hops")
''', explain='Hadoop uses a very similar “network distance”: 0 for the same node, 2 for the same rack, 4 for another rack in the same data centre.'),
    dict(level='business', title='How many racks to buy?', stmt='The business needs to store 900 TB of data. Each node has 144 TB raw, HDFS keeps 3 copies, and 25% is kept free. A rack takes 18 nodes. How many nodes and racks are needed?', inp='900 TB data · 144 TB/node · ×3 · 25% free · 18 nodes/rack',
         code='''import math
data_tb = 900
raw_needed = data_tb * 3 / 0.75
nodes = math.ceil(raw_needed / 144)
racks = math.ceil(nodes / 18)
print("Raw disk needed:", raw_needed, "TB")
print("Nodes:", nodes, "Racks:", racks)
''', explain='Work backwards from business data: × 3 copies, ÷ 0.75 for headroom, ÷ node size, then round up. Lesson 1.3 adds growth and CPU to this.'),
    dict(level='business', title='Power bill for one rack', stmt='A rack has 18 servers drawing 450 W each, running all year. Cooling adds 50% on top. Electricity costs Rs 9 per kWh. What is the yearly cost?', inp='18 × 450 W · +50% cooling · 24×365 h · Rs 9/kWh',
         code='''kw = 18 * 450 / 1000
kw_with_cooling = kw * 1.5
kwh_year = kw_with_cooling * 24 * 365
print(f"Power: {kw_with_cooling:.2f} kW")
print(f"Cost per year: Rs {kwh_year * 9 / 1e5:.1f} lakh")
''', explain='About Rs 9.6 lakh a year for one rack, before rent, staff and hardware. Running a cluster has real costs, so teams size it carefully (figures are illustrative).'),
]

SCN_INTRO = 'Situations about hardware and racks that interviewers describe to see whether you understand the physical side of a cluster.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · reliability</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>A whole rack lost power, and some data was unavailable</h4>
      <p class="scn__situation">During maintenance, the power strip of rack 4 failed and all 20 nodes in it went offline at once. Some HDFS files became unreadable even though only one rack was down. What was probably wrong in the setup?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know that a rack is a failure domain and that HDFS needs to be told about racks?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>With correct rack awareness, HDFS stores each block's copies on <b>at least two racks</b>, so losing one rack never loses all copies. If files became unreadable, the cluster most likely had <b>no topology script</b>: every node was in <code>/default-rack</code>, so all three copies of some blocks happened to be in rack 4.</p>
        <ul>
          <li>Configure <code>net.topology.script.file.name</code> to map hosts to racks, and restart the NameNode.</li>
          <li>Check with <code>hdfs dfsadmin -printTopology</code>, then run <code>hdfs fsck</code> to find blocks whose replicas are all on one rack.</li>
          <li>Let HDFS re-replicate those blocks so they span racks.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid saying:</b> “Increase replication to 5.” More copies on the same rack still fail together.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Infrastructure · hardware choice</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>RAID 5 on every worker node?</h4>
      <p class="scn__situation">A hardware vendor proposes RAID 5 controllers on all 60 worker nodes “for safety”. Your manager asks if that is a good idea for a Hadoop cluster.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know why Hadoop workers use JBOD and where RAID still belongs?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>HDFS already protects data by replicating blocks across nodes and racks, so RAID on workers mostly duplicates protection and costs disk space and money.</li>
          <li>Independent disks (JBOD) let the DataNode read and write many disks in parallel; RAID 5 adds write overhead and long rebuilds.</li>
          <li>If one JBOD disk fails, the DataNode can keep running on its other disks (with a configured tolerance) and HDFS re-copies the lost blocks.</li>
          <li><b>But</b> master nodes holding NameNode metadata should use RAID (for example mirrored disks) plus redundant power.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> saying RAID is useless everywhere. It is still the right choice for masters and many databases.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · performance</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Jobs are slow every night, but CPUs are idle</h4>
      <p class="scn__situation">Nightly jobs on a 200-node cluster have become slow. Monitoring shows CPU at 30% and disks lightly used, but the ToR uplinks are at 100% during the jobs. What is happening and what would you do?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you read network symptoms and connect them to oversubscription and data locality?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>The jobs are <b>network bound</b> on the rack uplinks: lots of data is moving between racks. Possible causes: tasks not running where their data is (poor locality), a big shuffle between stages, or a rack topology that is misconfigured.</p>
        <ol>
          <li>Check the job counters for data-local vs rack-local vs off-rack tasks (Module 8).</li>
          <li>Verify the topology script; a wrong map makes the scheduler think nodes are local when they are not.</li>
          <li>Reduce shuffle volume (combiners, filtering early, better formats like Parquet).</li>
          <li>Long term: more or faster uplinks (lower oversubscription).</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “add more nodes”. More nodes behind the same uplinks can make it worse.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Startup · architecture</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Buy racks or rent cloud machines?</h4>
      <p class="scn__situation">A 30-person fintech startup expects its data to grow from 2 TB to 50 TB in two years and wants to “build a Hadoop cluster”. The founder asks whether to buy servers and rent rack space, or use the cloud.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you weigh on-premises, colocation and cloud sensibly instead of having one fixed answer?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Start in the cloud:</b> no upfront hardware, a managed Hadoop/Spark service, pay per hour, grow as data grows. The team stays small.</li>
          <li>Store data in cloud object storage and run clusters only when jobs need them, to save cost.</li>
          <li>Check regulatory needs: financial data may need to stay in India, which Indian cloud regions support.</li>
          <li>Revisit on-premises or colocation later if the load becomes large and steady, where owning hardware can be cheaper.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> recommending a big on-prem cluster for 2 TB, or claiming the cloud is always cheaper at any scale.</p>
      </div></details>
    </article>'''
