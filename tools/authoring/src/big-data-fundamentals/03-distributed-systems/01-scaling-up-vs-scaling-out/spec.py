import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='03-distributed-systems', lesson='01-scaling-up-vs-scaling-out', n='3.1',
    module_label='Module 3 · Distributed Systems Concepts',
    title='Scaling up vs scaling out (and back-of-envelope estimation)',
    desc='Vertical vs horizontal scaling in depth: stateless vs stateful services, load balancers, autoscaling, read replicas, headroom, the Universal Scalability Law, Little\'s law and tail latency, plus a step-by-step back-of-envelope estimation method for requests, storage, bandwidth and servers. Diwali-night animations and a capacity estimator for your PC.',
    og_desc='How many servers for 10 crore orders on Diwali day? Learn to estimate in two minutes, and see why some systems scale out easily and others don\'t.',
    minutes=30, level='Beginner → Advanced',
    lead='“10 crore orders on Diwali day: how much storage and how many servers?” In this lesson you learn to answer questions like this in two minutes with round numbers, and go deeper into <b>scaling up</b> versus <b>scaling out</b>: why stateless services scale easily, how autoscaling follows the festival curve, and why 64 machines can be slower than 32.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Capacity estimator for your PC'],
)

RUN = dict(
    heading='A back-of-envelope calculator',
    intro='<p>Change the assumptions at the top and run. The program turns “orders per day” into peak orders per second, storage per year and the number of servers. Then try the challenges: compare scaling up and out, simulate autoscaling, use Little\'s law, see the Universal Scalability Law and the tail-latency effect.</p>',
    code='''import math

orders_per_day = 10_00_00_000   # 10 crore
peak_factor = 5
kb_per_order = 1
copies = 3
per_server = 400                # orders/s one API server handles
target_load = 0.6               # keep 40% headroom

avg = orders_per_day / 86_400
peak = avg * peak_factor
gb_day = orders_per_day * kb_per_order / 1024 / 1024
tb_year = gb_day * 365 / 1024 * copies
servers = math.ceil(peak / (per_server * target_load))

print(f"average   : {avg:,.0f} orders/s")
print(f"peak      : {peak:,.0f} orders/s")
print(f"storage   : {gb_day:,.0f} GB/day, {tb_year:,.0f} TB/year with {copies} copies")
print(f"servers   : {servers} at {target_load:.0%} target load")
''',
    anno=[
        ('avg = orders_per_day / 86_400', 'Per day ÷ 86,400 seconds = per second. In your head, divide by 1 lakh.'),
        ('peak = avg * peak_factor', 'Size for the busiest hour, never the average.'),
        ('servers = math.ceil(peak / (per_server * target_load))', 'Round up, and plan for each server to run at only 60% so spikes and failures are absorbed.'),
    ],
    tasks=[
        dict(label='1 · Estimate', hint='Press <b>Run</b>. Then change to 25 crore orders a day and a peak factor of 8 (a mega sale). How many servers now?', code=None),
        dict(label='2 · Up or out?', hint='Compare the cost of meeting a capacity with one big server or several small ones. Prices are illustrative. Ask for 512 units: what happens to scale-up?',
             code='''big = {64: 10, 128: 28, 256: 80}      # capacity units -> lakh rupees per year
small_unit, small_price = 32, 3        # one small node: 32 units, 3 lakh per year
for need in [64, 128, 256]:
    nodes = -(-need // small_unit)     # ceiling division
    print(f"need {need:3}: scale up Rs {big[need]:3} lakh | scale out {nodes} nodes Rs {nodes * small_price} lakh")
'''),
        dict(label='3 · Autoscaler', hint='Each hour, choose the number of servers so CPU stays near 60%. Each server handles 400 orders/s at 100%. Change the minimum to 4.',
             code='''import math
load = [1200, 2500, 4800, 6000, 3500, 900]   # orders/s each hour
MIN, MAX = 3, 40
for hour, rate in enumerate(load):
    servers = min(MAX, max(MIN, math.ceil(rate / (400 * 0.6))))
    cpu = rate / (servers * 400) * 100
    print(f"hour {hour}: {rate:5} orders/s -> {servers:2} servers, CPU {cpu:4.0f}%")
'''),
        dict(label='4 · Little\'s law', hint='Requests in the system = arrival rate × time inside. If the database slows from 50 ms to 400 ms, how many connections are busy? Try different rates.',
             code='''rate = 5000                       # requests per second
for ms in [50, 100, 200, 400]:
    in_flight = rate * ms / 1000
    print(f"{ms:3} ms per request -> {in_flight:5.0f} requests in flight")
'''),
        dict(label='5 · Scalability law (advanced)', hint='Throughput with N nodes = N / (1 + a(N-1) + bN(N-1)). Find the best N. Set b = 0 (no coordination): does the curve still turn down?',
             code='''a, b = 0.03, 0.0008
best = max(range(1, 129), key=lambda n: n / (1 + a * (n - 1) + b * n * (n - 1)))
for n in [1, 8, 16, 32, 64, 128]:
    x = n / (1 + a * (n - 1) + b * n * (n - 1))
    print(f"{n:3} nodes -> {x:5.1f}x")
print("best number of nodes:", best)
'''),
        dict(label='6 · Tail latency (advanced)', hint='One page calls N servers in parallel. Each is slow 1% of the time. What fraction of pages are slow? Try 2% slowness.',
             code='''p_slow = 0.01
for n in [1, 10, 50, 100, 200]:
    print(f"fan-out {n:3}: {(1 - (1 - p_slow) ** n) * 100:5.1f}% of pages hit a slow server")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: an estimate calibrated by your own CPU',
    intro='<p>Good estimates start from a measurement. This program first measures how many order events one core of your computer can parse and validate in a second, then uses that number to estimate the cores, nodes and storage needed for 10 crore orders a day. Only the standard library is used. Save it as <code>capacity_estimator.py</code> and run it.</p>',
    items=[
        dict(title='Measure, then estimate', file='capacity_estimator.py',
             cmd=open(os.path.join(HERE, 'capacity_estimator.py')).read() + '\n# In a terminal:  python capacity_estimator.py',
             output=open(os.path.join(HERE, 'capacity_estimator.out')).read(),
             note='Recorded from a real run with Python 3.13 on a cloud machine; your measured rate will differ. The surprising result, a single node, is the lesson: parsing JSON is cheap, so for this workload the real limits are storage (hundreds of TB a year), network, databases and reliability, not CPU. That is why you estimate every resource, not just one.'),
    ],
)

TRACE = dict(
    heading='An autoscaler deciding, one line at a time',
    intro='<p>For three hours of traffic, the autoscaler picks enough servers to keep each one at about 60% load, never fewer than 2. Watch <code>servers</code> follow the load up and down.</p>',
    code='''import math
load = [1000, 4800, 1500]
history = []
for rate in load:
    servers = max(2, math.ceil(rate / 240))
    history.append(servers)
print(history)
''',
    notes={2: 'Load :: Orders per second in three different hours.',
           5: 'Decide :: 240 = 400 orders/s per server × 60% target load. Never go below 2 servers.'},
)

WORKED_INTRO = 'Four scaling and estimation problems, from a first estimate to choosing the best cluster size. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Interview · estimation', title='Requests per second from daily users',
         problem='<p>An app has 2 crore daily users. Each opens it 5 times a day and makes 8 API calls per visit. The evening peak is 4 times the average. Estimate average and peak requests per second.</p>',
         inp='2 crore users × 5 visits × 8 calls, peak 4×',
         approach=['Requests per day = users × visits × calls.',
                   'Average per second = per day ÷ 86,400.',
                   'Peak = average × peak factor.'],
         code='''users, visits, calls, peak_factor = 2_00_00_000, 5, 8, 4
per_day = users * visits * calls
avg = per_day / 86_400
print(f"requests/day: {per_day / 1e7:.0f} crore")
print(f"average: {avg:,.0f}/s  peak: {avg * peak_factor:,.0f}/s")
''', notes={2: 'Per day :: 2 crore × 5 × 8 = 80 crore requests.'},
         tryit='The marketing team expects a festival with 3 crore users and a peak factor of 10. Re-run with those numbers.'),
    dict(level='i', tag='Capacity planning · storage', title='Storage for a year, with growth and copies',
         problem='<p>A service stores 120 GB of new data per day today, growing 5% per month. Data is kept 1 year with 3 copies. How much raw storage is needed at the end of the year?</p>',
         inp='120 GB/day, +5% per month, 12 months, 3 copies',
         approach=['Loop month by month; daily volume grows 5% each month.',
                   'Add 30 days of data per month to the running total.',
                   'Multiply the year\'s total by the number of copies.'],
         code='''daily_gb = 120
total_gb = 0
for month in range(12):
    total_gb = total_gb + daily_gb * 30
    daily_gb = daily_gb * 1.05
print(f"data for the year: {total_gb / 1024:.1f} TB")
print(f"with 3 copies   : {total_gb * 3 / 1024:.1f} TB")
print(f"daily volume at year end: {daily_gb:.0f} GB")
''', notes={5: 'Growth :: Each month\'s daily volume is 5% bigger than the last.'},
         tryit='Change growth to 10% a month. How much bigger is the year-end total?'),
    dict(level='i', tag='Operations · autoscaling', title='How many servers each hour, and the saving',
         problem='<p>Each server handles 500 requests/s; keep load at 60% and at least 3 servers. Given hourly traffic, compute servers per hour and compare total server-hours with running the peak count all day.</p>',
         inp='6 hourly loads',
         approach=['Servers per hour = max(3, ceil(load ÷ (500 × 0.6))).',
                   'Add up server-hours.',
                   'Compare with peak servers × 6 hours.'],
         code='''import math
load = [800, 2400, 7200, 9000, 4000, 900]
per_hour = [max(3, math.ceil(r / 300)) for r in load]
print("servers per hour:", per_hour)
print("autoscaled server-hours:", sum(per_hour))
print("fixed at peak          :", max(per_hour) * len(load))
''', notes={3: 'Decide :: 300 = 500 × 0.6. The minimum keeps a safety margin even at night.'},
         tryit='New servers take 10 minutes to start. Change the rule to use the next hour\'s load (look ahead) so capacity is ready in time.'),
    dict(level='a', tag='Performance · USL', title='Pick the best cluster size from a fitted model',
         problem='<p>Load tests were fitted to the Universal Scalability Law with a = 0.03 and b = 0.0008; one node does 10 jobs per minute. Each node costs Rs 50 per hour. Among the candidate sizes, find the fastest cluster and the cheapest cost per 1,000 jobs.</p>',
         inp='sizes 8, 16, 32, 48, 64 · a = 0.03 · b = 0.0008 · Rs 50/node-hour',
         approach=['Throughput(N) = 10 × N ÷ (1 + a(N−1) + bN(N−1)) jobs per minute.',
                   'Cost per 1,000 jobs = (N × 50 per hour) ÷ (jobs per hour) × 1,000.',
                   'Track the best size for speed and for cost separately.'],
         code='''a, b, per_node, price = 0.03, 0.0008, 10, 50
fastest, cheapest = None, None
for n in [8, 16, 32, 48, 64]:
    jobs_min = per_node * n / (1 + a * (n - 1) + b * n * (n - 1))
    cost_1000 = n * price / (jobs_min * 60) * 1000
    print(f"{n:2} nodes: {jobs_min:5.1f} jobs/min, Rs {cost_1000:6.1f} per 1,000 jobs")
    if fastest is None or jobs_min > fastest[1]:
        fastest = (n, jobs_min)
    if cheapest is None or cost_1000 < cheapest[1]:
        cheapest = (n, cost_1000)
print("fastest:", fastest[0], "nodes | cheapest per job:", cheapest[0], "nodes")
''', notes={4: 'Model :: The USL formula: contention a and coherence b slow each added node.', 5: 'Cost :: Node-hours divided by jobs per hour.'},
         tryit='Set <code>b = 0</code> (no coordination cost). Does the fastest size change? Why is the cheapest size usually smaller than the fastest?'),
]

QUIZ = [
    dict(q='Replacing a database server with a bigger one that has more CPU and RAM is:', options=['Horizontal scaling', 'Vertical scaling', 'Sharding', 'Load balancing'], answer=1,
         why='Making one machine bigger is <b>vertical scaling</b> (scale up).'),
    dict(q='Why do stateless API servers scale out easily?', options=['They use less electricity', 'Any copy can serve any request, so you just add copies behind a load balancer', 'They never fail', 'They don\'t need a network'], answer=1,
         why='No request depends on data held in one server\'s memory, so servers are interchangeable.'),
    dict(q='Roughly how many seconds are in a day, for quick estimates?', options=['10,000', '1 lakh (86,400)', '10 lakh', '1 crore'], answer=1,
         why='86,400 seconds ≈ 1 lakh, so “per day ÷ 1 lakh” gives “per second”.'),
    dict(q='10 crore orders a day at about 1 KB each is roughly how much data per day?', options=['1 GB', '10 GB', '100 GB', '10 TB'], answer=2,
         why='1 crore × 1 KB ≈ 10 GB, so 10 crore ≈ 100 GB (about 95 GB exactly).'),
    dict(q='Users report empty carts after the app moved from one server to five. The most likely cause is:', options=['The database is full', 'Carts were stored in each server\'s memory (stateful servers)', 'The network is too fast', 'Too few users'], answer=1,
         why='Requests now land on servers that never saw the cart. Move sessions and carts to a shared store such as Redis.'),
    dict(q='Little\'s law says the number of requests in a system equals:', options=['Arrival rate ÷ time inside', 'Arrival rate × time each request spends inside', 'Servers × CPU', 'Peak ÷ average'], answer=1,
         why='L = λW. At 5,000/s and 0.2 s each, about 1,000 requests are in flight.'),
    dict(q='According to the Universal Scalability Law, why can adding nodes reduce throughput?', options=['Nodes get tired', 'Coordination between nodes grows faster than the work added', 'Load balancers stop working above 32 nodes', 'It can\'t; throughput always rises'], answer=1,
         why='The coherence term grows with every pair of nodes, so beyond a point the cost of keeping them in agreement wins.'),
    dict(q='A page calls 100 servers in parallel; each is slow 1% of the time. About what share of pages is slow?', options=['1%', '10%', '37%', '63%'], answer=3,
         why='1 − 0.99<sup>100</sup> ≈ 0.63. Fan-out makes rare slowness common, which is why large systems track p99 latency.'),
]

REVISION = [
    '<b>Scale up</b> = bigger machine (simple, ceiling, single point of failure). <b>Scale out</b> = more machines + load balancer.',
    '<b>Stateless</b> tiers scale out by adding copies; move state to Redis/databases. Databases: scale up → read replicas → shard.',
    'Autoscale on CPU/queue/RPS with min and max; pre-scale for known peaks; keep 30–50% <b>headroom</b>.',
    'Estimation recipe: per day → ÷ 1 lakh → × peak factor → × size → ÷ per-machine capacity. State assumptions.',
    'Handy: 1 crore × 1 KB ≈ 10 GB; 1 Gbps ≈ 125 MB/s; 1 year ≈ 3 crore seconds.',
    '<b>Little\'s law</b>: L = λW. <b>USL</b>: contention (α) and coherence (β) limit scaling.',
    'Fan-out amplifies tail latency: 1 − (1 − p)<sup>N</sup>. Watch p99, not the average.',
]
FAQ = [
    ('Differentiate vertical and horizontal scaling.', 'Vertical scaling adds resources (CPU, RAM, disk) to a single machine; it is simple and needs no code changes, but cost rises steeply, there is a hard upper limit and the machine remains a single point of failure. Horizontal scaling adds more machines and spreads the load with a load balancer or data partitioning; it scales much further and tolerates failures, but requires stateless services or distributed data design. Real systems usually combine both.'),
    ('What is a back-of-envelope estimation and why is it useful?', 'A quick calculation using rounded numbers and stated assumptions to estimate load (requests per second), storage, bandwidth and machine count. It shows early whether a design is feasible, which resource is likely to be the bottleneck and roughly what it will cost, before any detailed work. It is a standard part of system-design interviews.'),
    ('How do you scale a database?', 'First optimise queries and indexes and scale the server up to a sensible size. Add caching for hot reads and read replicas for read-heavy workloads. When writes or data size outgrow one machine, partition (shard) the data across servers by a key, or move to a distributed database designed for horizontal scaling.'),
    ('What is autoscaling?', 'Automatically adjusting the number of running instances based on metrics such as CPU utilisation, request rate or queue length, within configured minimum and maximum limits. It keeps performance steady during peaks and saves cost during quiet periods; for predictable peaks, teams schedule scale-ups in advance because new instances take time to start.'),
    ('Why doesn\'t doubling the machines always halve the time?', 'Because part of the work can\'t be parallelised (Amdahl\'s law), machines wait on shared resources (contention), and they must communicate and coordinate (coherence), which grows with the number of machines. The Universal Scalability Law models these effects; beyond an optimal size, adding machines can even reduce throughput.'),
]

PRACTICE_INTRO = 'Estimation and scaling exercises. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Per day to per second', stmt='Convert 4 crore events per day into events per second.', inp='4 crore/day',
         code='''print(round(4_00_00_000 / 86_400))
''', explain='Divide by the 86,400 seconds in a day (≈ 1 lakh).'),
    dict(level='easy', title='Peak rate', stmt='The average is 1,200 requests/s and the peak factor is 6. Print the peak.', inp='1200, 6',
         code='''print(1200 * 6)
''', explain='Systems are sized for the peak.'),
    dict(level='easy', title='Daily storage', stmt='5 crore records a day at 2 KB each. Print GB per day.', inp='5 crore × 2 KB',
         code='''print(round(5_00_00_000 * 2 / 1024 / 1024), "GB")
''', explain='KB ÷ 1024 = MB, ÷ 1024 again = GB.'),
    dict(level='medium', title='Servers with headroom', stmt='Peak is 9,000 requests/s; one server handles 500/s; target load 60%. Print servers needed.', inp='9000, 500, 0.6',
         code='''import math
print(math.ceil(9000 / (500 * 0.6)))
''', explain='Divide by the usable capacity per server, then round up.'),
    dict(level='medium', title='Bandwidth', stmt='At peak, 20,000 events/s of 1.5 KB each arrive. Print MB/s and Mbps.', inp='20,000 × 1.5 KB',
         code='''mb = 20000 * 1.5 / 1024
print(round(mb, 1), "MB/s =", round(mb * 8), "Mbps")
''', explain='Multiply MB/s by 8 to get megabits per second, the unit network links use.'),
    dict(level='advanced', title='Connection pool size', stmt='At peak, 3,000 queries/s each take 40 ms in the database. How many connections are busy on average? Add 50% safety.', inp='3000/s, 40 ms',
         code='''busy = 3000 * 0.040
print("busy:", busy, "| pool with 50% safety:", round(busy * 1.5))
''', explain='Little\'s law (L = λW) sizes connection pools and thread pools.'),
    dict(level='advanced', title='Slow pages from fan-out', stmt='A search page queries 40 shards in parallel; each shard is slow 0.5% of the time. What percentage of pages are slow?', inp='40 shards, 0.5%',
         code='''print(round((1 - (1 - 0.005) ** 40) * 100, 1), "%")
''', explain='Even rare slowness becomes common with fan-out; techniques like hedged requests send a backup request after a short delay.'),
    dict(level='business', title='Autoscaling vs fixed fleet', stmt='Peak needs 40 servers for 4 hours a day; the other 20 hours need 10. A server costs Rs 30 per hour. Compare the daily cost of a fixed 40-server fleet with autoscaling.', inp='40 × 4 h + 10 × 20 h',
         code='''fixed = 40 * 24 * 30
auto = (40 * 4 + 10 * 20) * 30
print("fixed: Rs", fixed, "| autoscaled: Rs", auto, "| saving:", round((1 - auto / fixed) * 100), "%")
''', explain='Elastic capacity is one of the biggest cost benefits of the cloud. (Prices are illustrative.)'),
    dict(level='business', title='Cost per thousand orders', stmt='Infrastructure costs Rs 18 lakh a month for 9 crore orders. After growth it costs Rs 30 lakh for 18 crore orders. Print the cost per 1,000 orders before and after.', inp='18 lakh / 9 crore, 30 lakh / 18 crore',
         code='''for cost, orders in [(18_00_000, 9_00_00_000), (30_00_000, 18_00_00_000)]:
    print(f"Rs {cost / orders * 1000:.2f} per 1,000 orders")
''', explain='Good scaling lowers the unit cost as volume grows, even when the total bill rises.'),
]

SCN_INTRO = 'Scaling and estimation questions from interviews and production incidents. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
