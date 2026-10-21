import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='01-introduction', lesson='03-distributed-computing-basics', n='1.3',
    module_label='Module 1 · Introduction',
    title='Distributed computing basics for big data',
    desc='How distributed computing works: partitioning, parallel processing, data locality, aggregation, master and workers, replication and fault tolerance. Exam-evaluation analogy, animations, Python simulations of a mini cluster, a multi-core program for your PC, quiz and interview scenarios.',
    og_desc='Build a tiny cluster in Python: split the data, process in parallel, survive a failure and combine the results correctly.',
    minutes=30, level='Beginner → Advanced',
    lead='Hadoop, Spark and Kafka all rest on one simple pattern: split the data, process the pieces at the same time on many machines, and combine the small results, while surviving machines that fail. This lesson builds that pattern step by step in Python you can run, and shows the traps that make distributed answers wrong.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Multi-core program for your PC'],
)

RUN = dict(
    heading='A tiny cluster in Python',
    intro='<p>Twelve canteen orders, three “machines”. The program <b>partitions</b> the data, lets each machine count only its own block, then <b>combines</b> the partial counts. On a real cluster the three counts would run at the same time on different computers. Then try the challenges: real parallel speed-up, a failure, Amdahl\'s law, a straggler and the average-of-averages trap.</p>',
    code='''orders = ["chai", "samosa", "chai", "vada pav", "chai", "poha",
          "samosa", "chai", "coffee", "chai", "samosa", "poha"]
machines = 3

# 1. PARTITION: split the data into one block per machine
size = len(orders) // machines
blocks = [orders[i * size:(i + 1) * size] for i in range(machines)]

# 2. PROCESS: each machine counts only its own block
def count_block(block):
    counts = {}
    for item in block:
        counts[item] = counts.get(item, 0) + 1
    return counts

partials = [count_block(b) for b in blocks]
for i, p in enumerate(partials, 1):
    print("Machine", i, "->", p)

# 3. COMBINE: merge the small partial results
total = {}
for p in partials:
    for item, n in p.items():
        total[item] = total.get(item, 0) + n
print("Final     ->", total)
''',
    anno=[
        ('orders[i * size:(i + 1) * size]', 'Slicing gives machine 1 items 0–3, machine 2 items 4–7, machine 3 items 8–11: one <b>partition</b> each.'),
        ('def count_block(block):', 'The same small function is sent to every machine. Shipping code to the data is <b>data locality</b>.'),
        ('partials = [count_block(b) for b in blocks]', 'Here the calls run one after another. On a cluster each call runs on a different node at the same time.'),
        ('total[item] = total.get(item, 0) + n', 'Counts combine by adding. That is why counting is the classic first distributed program.'),
    ],
    tasks=[
        dict(label='1 · Mini cluster', hint='Press <b>Run</b>. Then set <code>machines = 4</code> and then <code>2</code>. The partial results change; the final answer doesn\'t. That is the promise of distributed computing.', code=None),
        dict(label='2 · Serial vs parallel', hint='Each “task” waits 1 second, like a worker reading a block from a slow disk. Run four tasks one after another, then four at the same time with threads. Times are approximate.',
             code='''import time
from concurrent.futures import ThreadPoolExecutor

def task(n):
    time.sleep(1)               # pretend to read a block from disk
    return n * 10

start = time.time()
results = [task(n) for n in range(4)]
print("Serial  :", results, f"{time.time() - start:.1f} s")

start = time.time()
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(task, range(4)))
print("Parallel:", results, f"{time.time() - start:.1f} s")
'''),
        dict(label='3 · A worker fails', hint='Worker 2 fails while processing its block. The master re-runs only that block on a worker that holds a copy. Change <code>failed = 2</code> to <code>failed = 1</code>.',
             code='''blocks = {1: [5, 3, 8], 2: [6, 1, 4], 3: [7, 2, 9]}
replica_of = {1: 3, 2: 1, 3: 2}        # block -> another worker holding a copy
failed = 2

results = {}
for worker, data in blocks.items():
    if worker == failed:
        print("Worker", worker, "failed!")
        continue
    results[worker] = sum(data)
    print("Worker", worker, "sum =", results[worker])

backup = replica_of[failed]
results[failed] = sum(blocks[failed])
print("Re-ran block", failed, "on worker", backup, "sum =", results[failed])
print("Total:", sum(results.values()))
'''),
        dict(label="4 · Amdahl's law", hint='If 10% of a job can\'t be split (setup, the final combine), there is a limit to the speed-up however many machines you add. Try <code>p = 0.99</code>.',
             code='''p = 0.90                      # fraction of the job that runs in parallel

for n in [1, 2, 10, 100, 1000]:
    speedup = 1 / ((1 - p) + p / n)
    print(f"{n:>5} machines: speed-up {speedup:5.2f}x")
print("Limit:", round(1 / (1 - p), 1), "x, even with infinite machines")
'''),
        dict(label='5 · The straggler', hint='A job finishes only when its <b>slowest</b> task finishes. Compare an even split with a skewed one where one block is much bigger.',
             code='''def job_time(block_sizes, secs_per_mb=0.01):
    times = [size * secs_per_mb for size in block_sizes]
    return max(times)                 # all run in parallel; wait for the slowest

even = [250, 250, 250, 250]
skewed = [100, 100, 100, 700]
print("Even split  :", job_time(even), "s")
print("Skewed split:", job_time(skewed), "s  <- one straggler")
'''),
        dict(label='6 · Average-of-averages trap', hint='<b>Predict first:</b> is the average of the two stores\' averages the true average? Fix it by sending <code>(total, count)</code> from each store and dividing once at the end.',
             code='''store_a = [100, 100, 100, 100, 100, 100, 100, 100]   # 8 small bills
store_b = [1000, 1000]                              # 2 big bills

avg_a = sum(store_a) / len(store_a)
avg_b = sum(store_b) / len(store_b)
print("Average of averages:", (avg_a + avg_b) / 2)

all_bills = store_a + store_b
print("True average       :", sum(all_bills) / len(all_bills))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: use all your CPU cores',
    intro='<p>A plain Python loop uses one core. This program counts prime numbers below 20 lakh, first on one core, then split into blocks and run on <b>all your cores</b> with <code>multiprocessing</code>. It is a real parallel program on one machine, using the same split–process–combine pattern a cluster uses across machines. Save it as <code>use_all_cores.py</code>.</p>',
    items=[
        dict(title='Split the work across cores', file='use_all_cores.py',
             cmd=open(os.path.join(HERE, 'use_all_cores.py')).read() + '\n# In a terminal:  python use_all_cores.py',
             output='''Serial   (1 core) : 148933 primes in 7.0 s
Parallel (2 cores): 148933 primes in 4.9 s
Speed-up: 1.4x
Parallel, 16 small blocks: 148933 primes in 4.4 s, speed-up 1.6x''',
             note='Recorded on a small 2-core cloud machine. On a 4- or 8-core laptop the speed-up will be larger, and your times will differ. Notice two real-world lessons: the answer is identical every time, and the speed-up is less than the number of cores, partly because bigger numbers take longer to test, so the last block is a <b>straggler</b>. Many smaller blocks balance the work better.'),
    ],
)

TRACE = dict(
    heading='Partition, count, combine, one line at a time',
    intro='<p>The mini cluster with six orders and two machines. Watch <code>count_block()</code> get its own frame for each block and return a small dictionary, then watch the partial results merge into <code>total</code>.</p>',
    code='''orders = ["chai", "poha", "chai", "chai", "samosa", "poha"]
blocks = [orders[0:3], orders[3:6]]

def count_block(block):
    counts = {}
    for item in block:
        counts[item] = counts.get(item, 0) + 1
    return counts

partials = [count_block(b) for b in blocks]
total = {}
for p in partials:
    for item, n in p.items():
        total[item] = total.get(item, 0) + n
print(total)
''',
    notes={1: 'Data :: Six orders in one list.',
           2: 'Partition :: Two blocks of three orders: one for each machine.',
           4: 'Define :: This small function is what gets shipped to every machine.',
           11: 'Combine :: Start an empty result.',
           15: 'Result :: Same answer as counting all six on one machine.'},
)

WORKED_INTRO = 'Four problems, from beginner to advanced: splitting fairly, combining correctly, recovering from failures and fixing a skewed partition. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Platform · partitioning', title='Split records into near-equal blocks',
         problem='<p>Split 10 records across 3 machines so that block sizes differ by at most one. (Plain slicing with <code>10 // 3</code> would leave one record out.)</p>',
         inp='records R1..R10, 3 machines',
         approach=['Use <code>divmod(10, 3)</code> to get the base size (3) and the remainder (1).',
                   'The first “remainder” blocks get one extra record.',
                   'Track the start position as you cut each block.'],
         code='''records = [f"R{i}" for i in range(1, 11)]
machines = 3

base, extra = divmod(len(records), machines)
blocks, start = [], 0
for m in range(machines):
    size = base + (1 if m < extra else 0)
    blocks.append(records[start:start + size])
    start = start + size
for m, b in enumerate(blocks, 1):
    print("Machine", m, ":", b)
''', notes={4: 'Plan :: 10 ÷ 3 = 3 remainder 1, so one block gets 4 records and two get 3.'},
         tryit='Change to 11 records and 4 machines. Balanced blocks avoid stragglers.'),
    dict(level='i', tag='Retail · aggregation', title='The correct distributed average',
         problem='<p>Two stores compute their bills locally. Store A has 8 bills of ₹100, store B has 2 bills of ₹1,000. Combine their results to get the true average bill.</p>',
         inp='A: 8 × 100 · B: 2 × 1000',
         approach=['Each store sends back <b>(sum, count)</b>, not its average.',
                   'Add all the sums and all the counts.',
                   'Divide once at the end.'],
         code='''store_a = [100] * 8
store_b = [1000] * 2

partials = [(sum(s), len(s)) for s in [store_a, store_b]]
total_sum = sum(p[0] for p in partials)
total_count = sum(p[1] for p in partials)
print("Partials:", partials)
print("True average:", total_sum / total_count)
''', notes={4: 'Partial results :: Each store sends a small pair (sum, count). Pairs can be added correctly; averages cannot.'},
         tryit='Work out <code>(100 + 1000) / 2</code> yourself: that wrong answer (550) is what averaging the averages gives.'),
    dict(level='i', tag='Cluster manager · fault tolerance', title='Reassign failed tasks',
         problem='<p>Four tasks were sent to workers. Task T3 failed. The master must find failed tasks and give them to a healthy worker, without re-running tasks that succeeded.</p>',
         inp='T1 done, T2 done, T3 failed, T4 done · healthy workers W1, W2',
         approach=['Keep the status of every task in a dictionary.',
                   'Loop over the tasks; skip finished ones.',
                   'Give each failed task to the next healthy worker and mark it done after the retry.'],
         code='''status = {"T1": "done", "T2": "done", "T3": "failed", "T4": "done"}
healthy = ["W1", "W2"]

retries = 0
for task, state in status.items():
    if state == "failed":
        worker = healthy[retries % len(healthy)]
        print("Retrying", task, "on", worker)
        status[task] = "done"
        retries = retries + 1
print("All done:", all(s == "done" for s in status.values()))
''', notes={5: 'Scan :: The master checks every task\'s state.'},
         tryit='Mark T1 as failed too. Both are retried, on different workers, and the finished tasks are never redone.'),
    dict(level='a', tag='Data platform · skew', title='Detect a hot key and salt it',
         problem='<p>Orders are partitioned by city. Mumbai\'s partition is far bigger than the rest, so one task runs six times longer. Measure the skew (largest ÷ average), then split the hot key into 6 sub-keys and show the new largest partition.</p>',
         inp='Pune 2, Delhi 2, Chennai 2, Kolkata 2, Mumbai 12 (GB)',
         approach=['Average size = total ÷ number of partitions. Skew ratio = largest ÷ average.',
                   'Build a new dictionary. For the hot city, add sub-keys <code>Mumbai-0</code> … <code>Mumbai-5</code>, each with one sixth of the data.',
                   'Copy every other city unchanged, then compare the largest partition before and after.'],
         code='''sizes = {"Pune": 2, "Delhi": 2, "Chennai": 2, "Kolkata": 2, "Mumbai": 12}
average = sum(sizes.values()) / len(sizes)
hot = max(sizes, key=sizes.get)
print("Hot key:", hot, "| skew ratio:", sizes[hot] / average)

salt = 6
parts = {}
for city, gb in sizes.items():
    if city == hot:
        for i in range(salt):
            parts[f"{city}-{i}"] = gb / salt
    else:
        parts[city] = gb
print("Partitions now:", len(parts), "| largest:", max(parts.values()), "GB")
''', notes={4: 'Skew :: A ratio of 3 means the hot task takes about 3 times the average task. The job waits for it.', 11: 'Salting :: Each sub-key gets one sixth of Mumbai. Their results are added together at the end.'},
         tryit='Change <code>salt</code> to 3. Is Mumbai still the bottleneck? Then make Delhi 9 GB: now two keys are hot. How would you change the program to salt every key bigger than twice the average?'),
]

QUIZ = [
    dict(q='Which order best describes the basic distributed processing pattern?', options=['Combine → partition → process', 'Partition → process in parallel → combine', 'Process → partition → combine', 'Replicate → delete → combine'], answer=1,
         why='Split the data, process the pieces in parallel, then aggregate the partial results.'),
    dict(q='“Move computation to data” is called:', options=['Replication', 'Data locality', 'Sharding', 'Caching'], answer=1,
         why='<b>Data locality</b>: run the task on the node that already stores the data, so big data doesn\'t cross the network.'),
    dict(q='Store A averages ₹100 over 8 bills; store B averages ₹1,000 over 2 bills. What is the true average bill?', options=['₹550', '₹280', '₹1,100', '₹100'], answer=1,
         why='(8×100 + 2×1000) ÷ 10 = 2,800 ÷ 10 = <b>₹280</b>. Averaging the averages (₹550) is wrong when group sizes differ.'),
    dict(q='How does a master node usually notice that a worker has died?', options=['The worker sends an email', 'The worker stops sending regular heartbeats', 'The user reports it', 'The data becomes smaller'], answer=1,
         why='Workers send periodic <b>heartbeats</b>. Missing several in a row means the worker is treated as dead and its tasks are rescheduled.'),
    dict(q='If 10% of a job must run serially, the maximum speed-up with unlimited machines is:', options=['10×', '100×', 'Unlimited', '2×'], answer=0,
         why='Amdahl\'s law: maximum speed-up = 1 ÷ (serial fraction) = 1 ÷ 0.1 = <b>10×</b>.'),
    dict(q='One task takes 10 minutes while all others take 1 minute. When does the job finish?', options=['After about 1 minute', 'After the average task time', 'After about 10 minutes', 'Immediately'], answer=2,
         why='Parallel tasks finish only when the slowest one finishes. That slow task is a <b>straggler</b>, often caused by skewed data.'),
    dict(q='Which is an example of a master–worker system?', options=['BitTorrent', 'Spark (driver and executors)', 'Cassandra', 'Email between two friends'], answer=1,
         why='Spark\'s driver plans and schedules; executors do the work. HDFS (NameNode/DataNodes) is another example. Cassandra and BitTorrent are peer-to-peer.'),
    dict(q='One task in a Spark job takes 40 minutes while 199 others take 3 minutes, because one customer id has far more rows than the rest. What is this called?', options=['Replication', 'Data skew (the slow task is a straggler)', 'Data locality', 'A heartbeat failure'], answer=1,
         why='One hot key makes one partition huge: <b>data skew</b>. Salting the key or choosing a better partition key spreads the work.'),
    dict(q='A worker stops sending heartbeats. Why can\'t the master be sure it has crashed?', options=['Heartbeats are encrypted', 'A silent worker may be crashed, overloaded or just cut off from the network, and these look the same from outside', 'The master never checks heartbeats', 'Workers only send heartbeats at the end'], answer=1,
         why='This is <b>partial failure</b>. A timeout can\'t tell slow from dead, so systems re-run the task and make outputs <b>idempotent</b> so duplicates don\'t matter.'),
    dict(q='Which of these is one of the “fallacies of distributed computing”?', options=['Machines have clocks', 'The network is reliable', 'Data can be split', 'Tasks can run in parallel'], answer=1,
         why='Assuming <b>the network is reliable</b> (or that latency is zero, or bandwidth infinite) is a classic mistake. Real networks drop, delay and duplicate messages.'),
]

REVISION = [
    '<b>Heartbeats</b> + timeouts detect failed workers; failed tasks are re-run on a node with a replica.',
    '<b>Data skew</b>: one hot key makes one huge partition (a straggler). Fix with salting or a better key; slow machines get <b>speculative</b> backup tasks.',
    'Retries mean a task can run twice, so outputs must be <b>idempotent</b> (commit one attempt per task).',
    '<b>Distributed computing</b>: many networked nodes work on parts of one job in parallel and combine the results.',
    'Pattern: <b>partition → process in parallel → aggregate</b>.',
    '<b>Data locality</b>: send the small program to the big data, not the reverse.',
    '<b>Master–worker</b> (HDFS, Spark, YARN) vs <b>peer-to-peer</b> (Cassandra).',
    '<b>Fault tolerance</b>: heartbeats detect failures; replicas let failed tasks re-run elsewhere.',
    'Combine carefully: sums and counts add up; <b>average of averages is wrong</b>; distinct counts need sets.',
    '<b>Stragglers</b>: the job waits for the slowest task. <b>Amdahl\'s law</b>: speed-up ≤ 1 ÷ serial fraction.',
]
FAQ = [
    ('What is distributed computing? How is it different from parallel computing on one machine?', 'Parallel computing runs parts of a task at the same time, often on cores sharing one machine\'s memory. Distributed computing spreads the task across separate computers connected by a network, each with its own memory and disk, coordinating by messages. It scales further and survives machine failures, but must deal with network delays and partial failures.'),
    ('Explain data locality and why it matters in Hadoop.', 'Data locality means scheduling a task on the node that already stores its data block. Network bandwidth across a cluster is much scarcer than local disk bandwidth, so moving a few kilobytes of code instead of gigabytes of data saves time and avoids congestion. Hadoop\'s scheduler prefers node-local, then rack-local, then remote placement.'),
    ('How does a distributed system handle the failure of a node?', 'Workers send heartbeats to a coordinator. When heartbeats stop, the node is marked dead. Its data is still available because blocks are replicated on other nodes, and its unfinished tasks are re-run on nodes holding those replicas. Tasks are designed to be idempotent so re-running them doesn\'t corrupt results.'),
    ("What is Amdahl's law?", 'It gives the maximum speed-up from parallelising a job: speed-up = 1 ÷ ((1 − p) + p ÷ n), where p is the parallel fraction and n the number of processors. The serial part sets a hard limit: if 5% is serial, the job can never run more than 20× faster.'),
    ('What are the main challenges of distributed systems?', 'Partial failures (some nodes fail while others work), network latency and lost messages, keeping replicas consistent, uneven work (skew and stragglers), coordinating many nodes, and combining partial results correctly. Frameworks like Hadoop and Spark handle much of this for the programmer.'),
]

FAQ.append(('What is data skew and how do you fix it?', 'Data skew happens when one partition key has far more data than others, so one task runs much longer and the whole job waits for it. Fixes include salting the hot key (splitting it into several sub-keys and combining their results later), choosing a partition key with more even values, handling the hot keys separately (for example, broadcasting a small table in a join), and in Spark enabling adaptive query execution, which can split skewed partitions automatically.'))

PRACTICE_INTRO = 'Split–process–combine exercises. The last three are business tasks about time, cost and correctness.'
PROBLEMS = [
    dict(level='easy', title='Chunks of three', stmt='Split the list 1 to 8 into chunks of at most 3 items.', inp='[1..8]',
         code='''nums = list(range(1, 9))
chunks = [nums[i:i + 3] for i in range(0, len(nums), 3)]
print(chunks)
''', explain='<code>range(0, 8, 3)</code> gives start positions 0, 3, 6; the last chunk is shorter.'),
    dict(level='easy', title='Merge two partial counts', stmt='Machine 1 counted <code>{"chai": 4, "poha": 1}</code> and machine 2 counted <code>{"chai": 2, "samosa": 3}</code>. Print the combined counts.', inp='two dictionaries',
         code='''p1 = {"chai": 4, "poha": 1}
p2 = {"chai": 2, "samosa": 3}
total = dict(p1)
for item, n in p2.items():
    total[item] = total.get(item, 0) + n
print(total)
''', explain='Copy the first result, then add the second item by item.'),
    dict(level='easy', title='Total from partial sums', stmt='Four workers returned partial sums 1200, 950, 1430 and 880. Print the total.', inp='[1200, 950, 1430, 880]',
         code='print("Total:", sum([1200, 950, 1430, 880]))\n', explain='Sums combine by adding: the simplest kind of aggregation.'),
    dict(level='medium', title='Global maximum from local maximums', stmt='Each machine finds the largest bill in its block. Combine them to get the largest bill overall.', inp='blocks [120, 450, 80], [990, 30], [300, 710]',
         code='''blocks = [[120, 450, 80], [990, 30], [300, 710]]
local_max = [max(b) for b in blocks]
print("Local:", local_max)
print("Global max:", max(local_max))
''', explain='Max of maxes is correct (unlike average of averages), so each node only needs to send one number.'),
    dict(level='medium', title="Amdahl's law", stmt='95% of a job can run in parallel. Print the speed-up on 20 machines and the limit.', inp='p = 0.95, n = 20',
         code='''p, n = 0.95, 20
print("Speed-up:", round(1 / ((1 - p) + p / n), 2))
print("Limit:", round(1 / (1 - p)), "x")
''', explain='Even 5% serial work caps the speed-up at 20×; on 20 machines you get about 10×.'),
    dict(level='advanced', title='Which workers are dead?', stmt='The master marks a worker as dead if its last heartbeat is more than 30 seconds old. Given the last heartbeat time of each worker and the current time, print the dead workers and the tasks to re-run.', inp='now = 1000 s',
         code='''now = 1000
last_beat = {"W1": 998, "W2": 990, "W3": 955, "W4": 999, "W5": 960}
tasks = {"W1": [1, 2], "W2": [3], "W3": [4, 5], "W4": [6], "W5": [7]}
TIMEOUT = 30
dead = [w for w, t in last_beat.items() if now - t > TIMEOUT]
rerun = [task for w in dead for task in tasks[w]]
print("Dead workers:", dead)
print("Tasks to re-run:", rerun)
''', explain='W3 has been silent 45 s and W5 40 s, both over the 30 s timeout. Their tasks are re-scheduled on healthy workers that hold replicas of the same blocks.'),
    dict(level='advanced', title='Commit one attempt per task', stmt='Because of retries, the same task can report results more than once. Keep only the first result for each task id, and print the correct total.', inp='results (task, attempt, orders)',
         code='''results = [(1, "a", 120), (2, "a", 95), (3, "a", 140),
           (3, "b", 140), (4, "a", 80), (2, "b", 95)]
committed = {}
for task, attempt, orders in results:
    if task not in committed:
        committed[task] = (attempt, orders)
naive = sum(r[2] for r in results)
correct = sum(o for _, o in committed.values())
print("Naive total  :", naive)
print("Correct total:", correct)
''', explain='Adding every report counts tasks 2 and 3 twice. Committing one attempt per task makes retries harmless: this is the idempotent output idea from scenario 3.'),
    dict(level='business', title='Copy the data or move the code?', stmt='A job needs 500 GB that sits on another node. The network gives 10 Gbps (about 1,250 MB/s). Print the copy time in minutes. Sending the 10 KB program takes well under a second.', inp='500 GB, 1250 MB/s',
         code='''mb = 500 * 1024
print("Copying data:", round(mb / 1250 / 60, 1), "minutes")
''', explain='About 7 minutes of a fully busy link for one block. Data locality avoids this entirely.'),
    dict(level='business', title='When does the job finish?', stmt='Six tasks run on six workers at the same time. Their times are 4, 5, 4, 21, 5 and 4 minutes. Print the job time and the average task time.', inp='[4, 5, 4, 21, 5, 4]',
         code='''times = [4, 5, 4, 21, 5, 4]
print("Job time:", max(times), "minutes")
print("Average task:", round(sum(times) / len(times), 1), "minutes")
''', explain='The straggler (21 min) decides the job time, not the average (7.2 min). Fix the skew or run a backup copy of the slow task.'),
    dict(level='business', title='Distinct customers across stores', stmt='Three stores report the customer ids they served. Print the number of <b>distinct</b> customers overall. (Adding the three counts would be wrong.)', inp='store ids with overlaps',
         code='''stores = [{"C1", "C2", "C3"}, {"C2", "C4"}, {"C1", "C4", "C5"}]
print("Sum of counts (wrong):", sum(len(s) for s in stores))
print("Distinct customers   :", len(set().union(*stores)))
''', explain='Customers who visit several stores would be counted more than once. Combine the sets, then count.'),
]

SCN_INTRO = 'Distributed-computing problems that show up in real jobs and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
