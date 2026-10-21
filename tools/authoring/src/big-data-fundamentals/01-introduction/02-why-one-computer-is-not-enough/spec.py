import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='01-introduction', lesson='02-why-one-computer-is-not-enough', n='1.2',
    module_label='Module 1 · Introduction',
    title='Why one computer is not enough for big data',
    desc='The storage, memory, CPU, I/O and reliability limits of a single computer, vertical vs horizontal scaling, and why big data needs clusters. Real calculations, animations, Python simulations you can run, a memory test for your own PC, quiz and interview scenarios.',
    og_desc='Calculate exactly where one computer runs out of road: disk, RAM, CPU, I/O and failures. Then see why clusters win.',
    minutes=28, level='Beginner → Advanced',
    lead='A laptop handles lakhs of rows easily. Give it 2 TB and it fails in four different ways. This lesson measures each limit of a single computer with real numbers, compares scaling up with scaling out, and shows why big data systems are built from many ordinary machines. Then watch the bottleneck move as a real report is fixed step by step, and compare the cost of scaling up and scaling out as data grows.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Memory test for your PC'],
)

RUN = dict(
    heading='Calculate when one machine is too slow',
    intro='<p>The core big data calculation: how long does it take just to <b>read</b> the data, with 1 machine or many? Each machine has one hard disk reading about 200 MB per second, and reads only its own share. Then try the challenges: will the data fit, how often do disks fail, and how to split work.</p>',
    code='''def read_minutes(data_tb, machines, mb_per_sec=200):
    data_mb = data_tb * 1024 * 1024
    per_machine = data_mb / machines        # each machine reads only its share
    return per_machine / mb_per_sec / 60

data_tb = 2
for machines in [1, 5, 20, 100]:
    m = read_minutes(data_tb, machines)
    print(f"{machines:>3} machine(s): {m:6.1f} minutes")
''',
    anno=[
        ('def read_minutes(data_tb, machines, mb_per_sec=200):', '<code>mb_per_sec=200</code> is a default value: a typical hard disk. Pass another value to model an SSD.'),
        ('per_machine = data_mb / machines', 'The heart of scaling out: with the data spread evenly, each machine reads a smaller part, and all read <b>at the same time</b>.'),
        ('f"{machines:>3} machine(s): {m:6.1f} minutes"', 'Format codes: <code>&gt;3</code> right-aligns in 3 characters, <code>6.1f</code> shows one decimal place in 6 characters, so the columns line up.'),
    ],
    tasks=[
        dict(label='1 · Read time', hint='Press <b>Run</b>. Then change <code>data_tb</code> to 100 and add 1000 to the list of machines. Try <code>read_minutes(2, 1, 3000)</code> for an NVMe SSD.', code=None),
        dict(label='2 · Will it fit?', hint='<b>Predict first:</b> which wall does the laptop hit, disk or RAM or both? Then change the data to 200 GB. Does it fit now? Is it still big data?',
             code='''disk_gb, ram_gb = 512, 8
data_gb = 2048

rows = data_gb * 1024**3 // 300            # about 300 bytes per row in the file
ram_needed_gb = rows * 270 / 1024**3        # about 270 bytes per row as a Python object

print("Rows       :", f"{rows:,}")
print("Fits disk? :", data_gb <= disk_gb)
print("Fits RAM?  :", ram_needed_gb <= ram_gb, f"(needs about {ram_needed_gb:,.0f} GB)")
'''),
        dict(label='3 · Load vs stream', hint='The list keeps every value in memory; the generator makes one value at a time. Compare the peak memory. Your numbers may differ slightly by Python version.',
             code='''import tracemalloc

tracemalloc.start()
values = [i * 2 for i in range(1_000_000)]      # all in memory at once
total = sum(values)
print("List     : peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 1), "MB")
tracemalloc.stop()

tracemalloc.start()
total = sum(i * 2 for i in range(1_000_000))     # one value at a time
print("Generator: peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 3), "MB")
tracemalloc.stop()
'''),
        dict(label='4 · Failures are normal', hint='About 1–2% of hard disks fail each year. See how the chance of “at least one failure today” grows with the number of disks. At 10,000 disks, what does it become?',
             code='''p_day = 0.015 / 365        # chance that ONE disk fails on a given day

for n in [1, 100, 1000, 10000]:
    p_any = 1 - (1 - p_day) ** n
    print(f"{n:>6} disks: {p_any * 100:6.2f}% chance at least one fails today")
'''),
        dict(label='5 · Split the work', hint='This splits 10 files across 3 machines in turn (round robin). Change <code>machines</code> to 4. Lesson 1.3 shows what each machine does with its share.',
             code='''files = [f"part-{i:02}.csv" for i in range(10)]
machines = 3

plan = {m: [] for m in range(1, machines + 1)}
for i, f in enumerate(files):
    plan[i % machines + 1].append(f)

for m, its_files in plan.items():
    print("Machine", m, "reads", len(its_files), "files:", its_files)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: measure your machine\'s memory wall',
    intro='<p>How much RAM do records really take inside Python? This program builds 10 lakh small payment records in a list and measures the memory used with Python\'s built-in <code>tracemalloc</code>. Save it as <code>ram_test.py</code> and run it on your computer.</p>',
    items=[
        dict(title='How much RAM does one record need?', file='ram_test.py',
             cmd=open(os.path.join(HERE, 'ram_test.py')).read() + '\n# In a terminal:  python ram_test.py',
             output='''CPU cores : 2
Disk      : 10 GB total, 4 GB free
10 lakh records in a list use 256 MB of RAM
That is about 268 bytes per record
   10 crore records would need about 25 GB of RAM
1,000 crore records would need about 2,500 GB of RAM''',
             note='Recorded on a small cloud machine with Python 3.10. Your cores and disk will be different; the bytes per record will be close (it varies a little by Python version). A record of about 40 characters in a CSV becomes about 270 bytes as a Python object. That gap is why loading big data “into memory” fails long before the disk is full.'),
    ],
)

TRACE = dict(
    heading='Scaling out, one line at a time',
    intro='<p>Watch how the same function is called three times, once for each cluster size. Each call gets its own frame with its own <code>machines</code> and <code>per_machine</code>; the frame disappears when the function returns.</p>',
    code='''def read_minutes(total_gb, machines, gb_per_sec=0.2):
    per_machine = total_gb / machines
    return per_machine / gb_per_sec / 60

data_gb = 600
for m in [1, 10, 100]:
    t = read_minutes(data_gb, m)
    print(m, "machine(s):", round(t, 1), "min")
''',
    notes={1: 'Define :: <code>gb_per_sec=0.2</code> means 0.2 GB (200 MB) per second, one hard disk.',
           5: 'Data :: 600 GB to read.',
           (2, 1): 'One machine :: It must read all 600 GB itself.',
           (2, 2): 'Ten machines :: Each reads only 60 GB.',
           (2, 3): 'A hundred machines :: Each reads only 6 GB, at the same time as all the others.'},
)

WORKED_INTRO = 'Four decisions, from beginner to advanced. Three a data engineer actually makes: does the data fit, which kind of scaling is cheaper, and how many failures to plan for. Each program runs live and is traced in memory. The last one finds the bottleneck of a whole job.'
EXAMPLES = [
    dict(level='b', tag='Analytics · capacity check', title='Which walls will the laptop hit?',
         problem='<p>A laptop has a 512 GB disk and 8 GB RAM. A job needs to store 2,048 GB and, if loaded into Python, would need about 1,760 GB of RAM. Print which resources are a problem.</p>',
         inp='laptop: disk 512, ram 8 · job: disk 2048, ram 1760 (GB)',
         approach=['Put the laptop\'s capacity and the job\'s needs in two dictionaries with the same keys.',
                   'Loop over the keys and compare need with capacity.',
                   'Print a “wall” message when the need is bigger.'],
         code='''laptop = {"disk": 512, "ram": 8}
need = {"disk": 2048, "ram": 1760}

for part in laptop:
    if need[part] > laptop[part]:
        times = need[part] / laptop[part]
        print(part, "wall:", round(times), "times too small")
    else:
        print(part, "OK")
''', notes={4: 'Check :: Loop over each resource in turn.'},
         tryit='Add a <code>"cores"</code> entry: the laptop has 4, the job could use 64. Then try a server with disk 4096 and ram 512.'),
    dict(level='i', tag='IT budget · scaling', title='Scale up or scale out?',
         problem='<p>A team needs 256 CPU cores. One option is a single 256-core server. The other is a cluster of 16-core nodes at ₹2,50,000 each. Compare the cost (prices are illustrative).</p>',
         inp='needed 256 cores · servers {64: 12 lakh, 128: 35 lakh, 256: 1.1 crore} · node 16 cores at 2.5 lakh',
         approach=['Look up the price of the 256-core server.',
                   'Work out how many 16-core nodes give 256 cores.',
                   'Multiply by the node price and compare.'],
         code='''needed_cores = 256
big_servers = {64: 12_00_000, 128: 35_00_000, 256: 1_10_00_000}
node_cores, node_price = 16, 2_50_000

nodes = needed_cores // node_cores
print("Scale up : one server, Rs", big_servers[needed_cores] / 1_00_000, "lakh")
print("Scale out:", nodes, "nodes,   Rs", nodes * node_price / 1_00_000, "lakh")
''', notes={2: 'Prices :: Each doubling of cores costs about three times more: the steep curve of scaling up. (Illustrative figures.)'},
         tryit='Next year you need 512 cores. There is no 512-core server in the list. What does scaling out cost? This is the “ceiling” of scaling up.'),
    dict(level='i', tag='Data centre · reliability', title='How many disk failures should we plan for?',
         problem='<p>A cluster has <b>1,000 hard disks</b>. Around 1.5% of disks fail each year. How many failures should the team expect per year, and how often is that?</p>',
         inp='1000 disks, 1.5% fail per year',
         approach=['Multiply disks by the yearly failure rate.',
                   'Divide 365 days by that number to get the gap between failures.'],
         code='''disks = 1000
annual_failure_rate = 0.015

per_year = disks * annual_failure_rate
print("Expected failures per year:", per_year)
print("About one failure every", round(365 / per_year), "days")
''', notes={4: 'Expect :: 1,000 × 0.015 = 15 failures a year.'},
         tryit='Change <code>disks</code> to 20000, the size of a big company\'s storage. Failures become a daily event, so the software must handle them automatically.'),
    dict(level='a', tag='Performance engineering · bottleneck', title='Which resource limits the job?',
         problem='<p>A nightly job must read <b>600 GB</b>, do <b>48 core-hours</b> of calculation and send <b>120 GB</b> of results over the network. The server has disks that read <b>1,000 MB/s</b> in total, <b>16 cores</b> and a <b>1 Gbps</b> network (125 MB/s). Estimate how long each part takes if it runs alone, and name the bottleneck.</p>',
         inp='600 GB read · 48 core-hours · 120 GB send · 1000 MB/s · 16 cores · 125 MB/s',
         approach=['Disk time = data ÷ disk speed. Convert GB to MB by multiplying by 1024.',
                   'CPU time = core-hours ÷ cores.',
                   'Network time = data sent ÷ network speed.',
                   'When parts overlap, the slowest one sets the total time: that is the bottleneck.'],
         code='''disk_s = 600 * 1024 / 1000
cpu_s = 48 * 3600 / 16
net_s = 120 * 1024 / 125
times = {"disk": disk_s, "cpu": cpu_s, "network": net_s}
for part, sec in times.items():
    print(f"{part:8}: {sec / 60:6.1f} minutes")
bottleneck = max(times, key=times.get)
print("Bottleneck:", bottleneck)
''', notes={1: 'Disk :: 6,14,400 MB at 1,000 MB/s.', 2: 'CPU :: 48 core-hours spread over 16 cores.', 3: 'Network :: 1 Gbps is only about 125 MB/s.', 7: 'Result :: The part that takes longest limits the whole job.'},
         tryit='Upgrade the network to 10 Gbps (<code>1250</code> MB/s). Is the job faster now? Then give it 64 cores. Notice how the bottleneck moves, just like in Kabir\'s report.'),
]

QUIZ = [
    dict(q='Adding more RAM and a faster CPU to the same server is called:', options=['Horizontal scaling', 'Vertical scaling', 'Replication', 'Partitioning'], answer=1,
         why='Making one machine bigger is <b>vertical scaling</b> (scale up). Adding machines is horizontal scaling (scale out).'),
    dict(q='A Python script processing a 1 TB file shows the CPU only 25% busy on a 4-core laptop. The most likely reason is:', options=['The CPU is broken', 'A plain loop runs on one core, and the job is also waiting on the disk', 'Python cannot read files larger than 1 GB', 'The file is compressed'], answer=1,
         why='A normal Python loop uses one core (1 of 4 = 25%), and large jobs are often <b>I/O bound</b>: waiting for the disk.'),
    dict(q='Reading 100 TB from one disk at 200 MB/s takes about:', options=['9 minutes', '6 hours', '6 days', '6 months'], answer=2,
         why='100 × 1024 × 1024 MB ÷ 200 MB/s ≈ 5,24,288 seconds ≈ <b>6 days</b>. With 1,000 disks in parallel, about 9 minutes.'),
    dict(q='Which is a disadvantage of vertical scaling?', options=['It needs distributed software', 'It has a hard upper limit and cost rises steeply', 'It cannot run databases', 'It always needs more network bandwidth'], answer=1,
         why='There is always a largest machine you can buy, and top-end machines cost disproportionately more. It also remains a single point of failure.'),
    dict(q='Why do big data clusters keep copies of data on more than one node?', options=['To make files smaller', 'Because with many machines, failures are normal and data must survive them', 'Because one copy is slower to write', 'To use up spare disk space'], answer=1,
         why='With hundreds or thousands of disks, some fail regularly. Copies (replication) let the job continue on another node.'),
    dict(q='Why does loading a 40 GB CSV into a Python list often fail on a 64 GB machine?', options=['Python lists can hold at most 1 million items', 'Python objects take several times more memory than the raw file bytes', 'CSV files cannot be opened by Python', 'RAM is only used by the OS'], answer=1,
         why='Each row becomes Python objects with extra overhead. A ~40-byte row can take ~270 bytes in memory, so 40 GB of CSV may need hundreds of GB of RAM.'),
    dict(q='A group of connected computers working together as one system is called a:', options=['Kernel', 'Cluster', 'Container', 'Thread'], answer=1,
         why='A <b>cluster</b> is a set of networked machines (nodes) that work as one system.'),
    dict(q='A job reads data with the disk at 100% while the CPU sits at 15%. What will help the most?', options=['A CPU with more cores', 'Faster storage or spreading the data over more disks/machines', 'More RAM only', 'Rewriting the program in a different language'], answer=1,
         why='The job is <b>I/O bound</b>: the disk is the bottleneck. Faster or more disks (or more machines reading in parallel) help; a faster CPU would just wait.'),
    dict(q='Roughly how much slower is reading from an SSD than from RAM?', options=['About the same', 'About 10 times', 'About 1,000 times', 'About a million times'], answer=2,
         why='RAM access is around 100 nanoseconds, an SSD read around 100 microseconds: about <b>1,000 times</b> slower. A hard-disk seek is slower still.'),
    dict(q='Why is the cloud attractive for big data peaks such as Diwali sales?', options=['Cloud machines never fail', 'You can rent extra machines for the peak and return them after, paying only while you use them', 'Cloud data is always free', 'There is no network in the cloud'], answer=1,
         why='<b>Elasticity</b>: clusters grow and shrink with demand, so you don\'t pay all year for capacity needed one week.'),
]

REVISION = [
    'Time = data ÷ speed. The slowest resource is the <b>bottleneck</b>; fixing it moves the bottleneck elsewhere.',
    'RAM ≈ 100 ns, SSD ≈ 100 µs, HDD seek ≈ 10 ms, data-centre round trip ≈ 0.5 ms.',
    'Cloud <b>elasticity</b>: rent nodes for the peak, return them after.',
    'One computer has five walls: <b>storage</b>, <b>memory</b>, <b>CPU</b>, <b>I/O</b> (disk + network) and <b>reliability</b>.',
    'Hard disk ≈ 200 MB/s. 100 TB on one disk ≈ 6 days; on 1,000 disks in parallel ≈ 9 minutes.',
    '<b>Vertical scaling</b> (scale up): bigger machine. Simple, but steep cost, hard ceiling, single point of failure.',
    '<b>Horizontal scaling</b> (scale out): more machines. Grows far, survives failures, but needs distributed software.',
    'Python objects are much bigger than file bytes, so “load everything into memory” fails early. Stream instead.',
    'A plain loop uses one core. Big jobs are often <b>I/O bound</b>.',
    'With many machines, <b>failures are normal</b>: keep copies of data and re-run failed parts.',
]
FAQ = [
    ('What are the limitations of a single machine for processing big data?', 'Limited storage capacity, limited RAM (data larger than memory causes crashes or swapping), limited CPU cores (a single process uses one), limited I/O bandwidth (one disk reads a few hundred MB/s, so terabytes take hours), and it is a single point of failure. Scaling it up is expensive and has an upper limit.'),
    ('Differentiate vertical and horizontal scaling.', 'Vertical scaling adds CPU, RAM or disk to one machine: simple, no code change, but costly at the top end, limited by the largest machine, and still a single point of failure. Horizontal scaling adds more machines and splits data and work across them: cost grows roughly linearly, it can grow very large and tolerate node failures, but it needs distributed software and adds network and coordination complexity.'),
    ('What does “I/O bound” mean? Give an example.', 'A job is I/O bound when its speed is limited by reading or writing data rather than by calculation. Summing one column of a 2 TB file is I/O bound: the addition is trivial, but reading 2 TB from a disk at 200 MB/s takes about three hours.'),
    ('Why is commodity hardware used in big data clusters?', 'Ordinary servers are cheap and easy to replace. Instead of paying a large premium for one very reliable machine, clusters use many affordable machines and handle failures in software through replication and re-running tasks.'),
    ('Is scaling out always better than scaling up?', 'No. For data that fits comfortably on one machine, scaling up is simpler, cheaper to run and has no distributed-system complexity. Scale out when the data, the speed requirement or the reliability requirement goes beyond what one machine can deliver.'),
]

PRACTICE_INTRO = 'Capacity and time calculations that come up in real data platform planning. The last three are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Read time for 500 GB', stmt='How many minutes does it take to read 500 GB from a disk at 250 MB/s?', inp='500 GB, 250 MB/s',
         code='mb = 500 * 1024\nprint(round(mb / 250 / 60, 1), "minutes")\n', explain='500 GB = 5,12,000 MB; ÷ 250 MB/s = 2,048 s ≈ 34 minutes.'),
    dict(level='easy', title='How many disks?', stmt='Each disk holds 4 TB. How many disks are needed for 90 TB? (A part-full disk still counts.)', inp='90 TB, 4 TB per disk',
         code='import math\nprint(math.ceil(90 / 4), "disks")\n', explain='<code>math.ceil</code> rounds up: 22.5 becomes 23.'),
    dict(level='easy', title='Fits in RAM?', stmt='A 6 GB CSV is loaded into Python, where it takes about 5 times its file size. The machine has 16 GB RAM. Print whether it fits.', inp='6 GB file, ×5 overhead, 16 GB RAM',
         code='needed = 6 * 5\nprint("Needs", needed, "GB; fits?", needed <= 16)\n', explain='30 GB > 16 GB, so it won\'t fit even though the file itself is smaller than the RAM.'),
    dict(level='medium', title='Round-robin assignment', stmt='Assign 7 tasks to 3 workers in turn and print each worker\'s tasks.', inp='tasks T1..T7, 3 workers',
         code='''tasks = [f"T{i}" for i in range(1, 8)]
workers = {1: [], 2: [], 3: []}
for i, t in enumerate(tasks):
    workers[i % 3 + 1].append(t)
print(workers)
''', explain='<code>i % 3</code> cycles 0, 1, 2, 0, 1, 2 …, so tasks go to workers 1, 2, 3, 1, 2, 3 ….'),
    dict(level='medium', title='Speed-up and efficiency', stmt='A job takes 120 minutes on 1 machine and 10 minutes on 16 machines. Print the speed-up (old ÷ new time) and the efficiency (speed-up ÷ machines) as a percentage.', inp='120 min on 1, 10 min on 16',
         code='''speedup = 120 / 10
efficiency = speedup / 16 * 100
print("Speed-up:", speedup)
print("Efficiency:", efficiency, "%")
''', explain='Perfect scaling would give a speed-up of 16. Coordination and uneven splits usually cost something, here 25%.'),
    dict(level='advanced', title='Will it fit in RAM?', stmt='A CSV takes about 6 times its file size once loaded into pandas. For each file, print whether it fits in 16 GB of RAM (keeping 4 GB free for the operating system), and if not, how many chunks of equal size are needed so that each chunk fits.', inp='files: 1.5, 3, 9 GB · RAM 16 GB · reserve 4 GB',
         code='''import math
ram, reserve, blowup = 16, 4, 6
usable = ram - reserve
for size in [1.5, 3, 9]:
    need = size * blowup
    if need <= usable:
        print(f"{size} GB file needs {need} GB: fits")
    else:
        chunks = math.ceil(need / usable)
        print(f"{size} GB file needs {need} GB: use {chunks} chunks")
''', explain='Memory needed = file size × blow-up factor. When it exceeds usable RAM, split the file into ceil(need ÷ usable) chunks and process them one at a time, exactly what Kabir did in scenario 2.'),
    dict(level='advanced', title='Nodes needed per hour (autoscaling)', stmt='Each node handles 5,000 orders per second. Given the expected orders per second for each hour, print how many nodes to run in that hour (always at least 2, for safety) and the total node-hours for the day so far.', inp='[8000, 21000, 64000, 12000]',
         code='''import math
per_node = 5000
load = [8000, 21000, 64000, 12000]
node_hours = 0
for hour, rate in enumerate(load):
    nodes = max(2, math.ceil(rate / per_node))
    node_hours = node_hours + nodes
    print(f"hour {hour}: {rate:>6} orders/s -> {nodes} nodes")
print("Total node-hours:", node_hours)
''', explain='This is what cloud autoscaling does: capacity follows the load hour by hour, instead of running 13 nodes all day for the one peak hour.'),
    dict(level='business', title='Fit the nightly window', stmt='A bank\'s nightly job must read 30 TB within 2 hours. Each node reads 200 MB/s. What is the minimum number of nodes?', inp='30 TB, 2 hours, 200 MB/s per node',
         code='''import math
total_mb = 30 * 1024 * 1024
one_node_secs = total_mb / 200
nodes = math.ceil(one_node_secs / (2 * 3600))
print("Minimum nodes:", nodes)
''', explain='One node would need about 43.7 hours; to finish in 2 hours you need at least 22 nodes (in practice, more for safety and failures).'),
    dict(level='business', title='Same cost, faster answer', stmt='Cloud nodes cost Rs 40 per hour each. A report needs 25 node-hours of work. Compare 1 node for 25 hours with 50 nodes for half an hour.', inp='Rs 40/node-hour, 25 node-hours',
         code='''rate = 40
for nodes, hours in [(1, 25), (50, 0.5)]:
    print(nodes, "node(s) for", hours, "h -> Rs", round(nodes * hours * rate))
''', explain='Both cost Rs 1,000, but one finishes 50 times sooner. On pay-per-use clouds, scaling out often costs the same and saves time.'),
    dict(level='business', title='When do we outgrow one server?', stmt='Data is 2 TB today and grows 60% a year. One server can handle up to 20 TB. In which year does the data pass that limit?', inp='2 TB, +60% per year, limit 20 TB',
         code='''data, year = 2.0, 0
while data <= 20:
    data = data * 1.6
    year = year + 1
print("Year", year, ": about", round(data, 1), "TB")
''', explain='Growth compounds: 2 → 3.2 → 5.1 → 8.2 → 13.1 → 21.0. Planning for scale-out starts years before the limit.'),
]

SCN_INTRO = 'Questions about scaling that interviewers use to see whether you can reason with numbers. Decide your answer first, then open the model answer.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Banking · batch processing</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The nightly job now finishes after the bank opens</h4>
      <p class="scn__situation">The end-of-day reconciliation job ran in 3 hours two years ago. Transactions have tripled and it now takes 8 hours, finishing after 9 am. It runs on one large database server. What would you investigate and propose?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you find the bottleneck first, and do you know when to scale up versus scale out?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li><b>Measure first:</b> is the job limited by disk reads, CPU, memory (swapping) or locks in the database? Look at monitoring during the run.</li>
          <li><b>Quick wins:</b> process only the new day's data instead of rescanning history; add the right indexes; use columnar formats for reporting tables.</li>
          <li><b>If it's still growing:</b> a bigger server buys a year or two. For sustained growth, move the heavy batch work to a distributed engine like Spark on a cluster, reading data in parallel, so capacity grows by adding nodes.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid saying:</b> “Just buy a bigger server” or “Move everything to Hadoop” without measuring where the time goes.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Why not just buy one very powerful computer?”</h4>
      <p class="scn__situation">An interviewer asks you to argue why big data platforms use clusters of ordinary machines rather than one supercomputer-class server.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know the concrete limits, not just the slogan “big data needs clusters”?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Ceiling:</b> even the biggest server has a fixed maximum of disks, RAM and cores; data keeps growing.</li>
          <li><b>Cost curve:</b> top-end hardware costs far more per unit of power than ordinary servers.</li>
          <li><b>I/O:</b> a cluster reads from hundreds of disks in parallel; 100 TB in minutes instead of days.</li>
          <li><b>Reliability:</b> one machine is a single point of failure; a cluster with replicated data keeps running when a node dies.</li>
          <li><b>Elasticity:</b> in the cloud you can add nodes for a busy night and remove them after.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> claiming one big machine is always worse. For small and medium data it is simpler and often the right choice.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · performance</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>The script that takes hours at 25% CPU</h4>
      <p class="scn__situation">A colleague's Python script summarises 300 GB of order logs. It takes five hours, and the 4-core machine shows 25% CPU the whole time. They ask you to “make it use the whole CPU”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand serial loops, I/O bottlenecks and the options available before reaching for a cluster?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>25% on 4 cores means one core is busy: the loop is <b>serial</b>. It may also be waiting on the disk.</p>
        <ul>
          <li>Check read speed: 300 GB at ~200 MB/s is about 25 minutes of pure reading, so most of the 5 hours is Python processing.</li>
          <li>Split the files and process them with <code>multiprocessing</code> (one process per core), or use faster tools like Pandas/Polars on chunks or DuckDB.</li>
          <li>Store logs in a compressed columnar format (Parquet) so only needed columns are read.</li>
          <li>If the data keeps growing, run it on Spark across several machines.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> assuming more CPU alone fixes it without checking whether the disk is the bottleneck.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · design review</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>“Disks rarely fail, we don't need copies”</h4>
      <p class="scn__situation">In a design review for a 500-node storage cluster with 6 disks per node, a teammate proposes storing one copy of each file to save money, because “disks rarely fail”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you turn a small per-disk failure rate into a cluster-wide expectation?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>500 × 6 = 3,000 disks. At around 1.5% failing per year, that's about <b>45 failures a year</b>, nearly one a week. With a single copy, each failure loses data permanently.</p>
        <ul>
          <li>Keep multiple copies (HDFS defaults to 3) on different nodes and racks, or use erasure coding to save space while still surviving failures.</li>
          <li>Automate detection and re-copying of data from failed disks.</li>
          <li>Quote the trade-off: extra storage cost versus the cost of losing data and re-running jobs.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> judging reliability per disk instead of across the whole cluster.</p>
      </div></details>
    </article>'''
