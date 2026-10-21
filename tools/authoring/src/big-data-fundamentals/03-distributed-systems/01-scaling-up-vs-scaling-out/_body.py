import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = box(14, 16, 290, 124, 'card') + t(159, 36, 'Interview question', 10, 'acc', bold=True)
sc += t(159, 62, '“TiffinGo expects 10 crore orders', 10, 'ink', bold=True) + t(159, 78, 'on Diwali day. How much storage and', 10, 'ink', bold=True) + t(159, 94, 'how many servers will we need?”', 10, 'ink', bold=True)
sc += t(159, 124, 'No calculator. Five minutes.', 9, 'ink2')
sc += arrow(310, 78, 340, 78, 'ink3', 2)
lines = ['10 crore ÷ 1 lakh s/day ≈ 1,000 orders/s', 'peak × 5 → 5,000 orders/s', '1 KB each → ≈ 100 GB/day', '≈ 35 TB a year, ×3 copies ≈ 100 TB', 'nodes = peak ÷ per-node rate + headroom']
sc += box(346, 16, 280, 124, 'green') + ''.join(t(358, 38 + k * 21, ln, 9, 'ink', anchor='start', mono=True) for k, ln in enumerate(lines))
scene_svg = scene('An interview question about Diwali-day capacity, answered with five lines of rough arithmetic.', sc,
                  'Big numbers become easy with <tspan font-weight="700" class="s-acc">round numbers and a recipe</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Kabir is preparing for TiffinGo’s full-time interview, which follows the internship. A senior shared the question they always ask: <i>“We expect 10 crore orders on Diwali day. How much storage and how many servers do we need?”</i> Kabir freezes. He doesn’t know the exact answer.</p>

{scene_svg}

K> Sir, how can anyone answer that without data? I'd need weeks of measurements.
A> Nobody expects the exact number, Kabir. They want to see you <b>estimate</b>: round numbers, clear assumptions, and arithmetic you can do on paper. Engineers call it a <b>back-of-envelope</b> estimate.
R> Like guessing how many samosas the canteen needs for the college fest?
A> Exactly that. How many students, how many will come, how many samosas each, plus some extra. Here: how many orders, how fast at the peak, how big each one is, how much one machine can handle.
K> And once we know we need more than one machine?
A> Then you choose between a bigger machine, <b>scaling up</b>, and more machines, <b>scaling out</b>. You met both in Lesson 1.2. Today we go deeper: why some services scale out easily and others don’t, how autoscaling follows the Diwali curve, and why adding machines can sometimes make a system <i>slower</i>.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Scaling and estimation at three levels
L1> A bigger jug or more stalls
      <ul>
        <li><b>Scaling up (vertical):</b> the lemonade stall buys a bigger jug and a faster juicer. Simple, but there is a biggest jug, and if the one stall closes, nobody gets lemonade.</li>
        <li><b>Scaling out (horizontal):</b> open more stalls and send customers to whichever is free. Needs a person at the gate (a <b>load balancer</b>), but you can keep adding stalls.</li>
        <li><b>Estimation recipe:</b> (1) how many things per day, (2) divide by about 1 lakh seconds for “per second”, (3) multiply by a peak factor, (4) multiply by size for storage, (5) divide by what one machine handles for machine count.</li>
      </ul>
      <p><b>Handy facts:</b> a day has 86,400 seconds, call it 1 lakh. 1 crore = 10<sup>7</sup>. 1 KB × 1 crore ≈ 10 GB.</p>
L2> Stateless services, load balancers and autoscaling
      <ul>
        <li><b>Stateless vs stateful:</b> a stateless service keeps nothing between requests (any server can answer any request), so it scales out by adding copies. A stateful one (a database, a cache, a session held in memory) must split or copy its data first, which is much harder.</li>
        <li><b>Move state out:</b> keep sessions in Redis and data in databases, so web and API servers stay stateless.</li>
        <li><b>Load balancer:</b> spreads requests across servers (round robin, least connections) and stops sending traffic to unhealthy ones.</li>
        <li><b>Scaling databases:</b> read replicas for read-heavy traffic, then <b>sharding</b> (splitting data across machines, Lesson 3.2) when writes outgrow one machine.</li>
        <li><b>Autoscaling:</b> add or remove machines based on a metric (CPU above 60%, queue length, requests per second), with a minimum and maximum. Scale up early for known peaks; new machines take minutes to start.</li>
        <li><b>Headroom:</b> plan to run at 50–70% of capacity, so a spike or a failed machine doesn’t push you over the edge.</li>
      </ul>
L3> Why scaling out has limits
      <ul>
        <li><b>Universal Scalability Law (Neil Gunther):</b> throughput with N machines ≈ N ÷ (1 + α(N−1) + βN(N−1)). α is <b>contention</b> (waiting for a shared resource, like Amdahl’s serial part); β is <b>coherence</b> (machines talking to each other to stay in agreement). With β &gt; 0, adding machines beyond a point <i>reduces</i> throughput.</li>
        <li><b>Little’s law:</b> items in the system = arrival rate × time each spends inside (L = λW). At 5,000 requests/s and 200 ms each, about 1,000 requests are in flight at any moment, which sizes thread pools and connections.</li>
        <li><b>Tail latency at scale:</b> if one request fans out to 100 servers and each is slow 1% of the time, 1 − 0.99<sup>100</sup> ≈ 63% of requests hit at least one slow server. Large systems watch p99 latency, not the average.</li>
        <li><b>Cost per unit:</b> measure cost per thousand orders, not just total cost; good scaling keeps it flat or falling as volume grows.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Scalability</b> is the ability of a system to handle increasing load by adding resources while maintaining acceptable performance. <b>Vertical scaling</b> (scaling up) increases the capacity of a single machine; <b>horizontal scaling</b> (scaling out) adds more machines and distributes load among them, typically behind a load balancer. A <b>back-of-envelope estimate</b> is a quick, approximate calculation of load, storage, bandwidth and machine count using rounded numbers and explicit assumptions, used to judge the feasibility and scale of a design.',
    'Scaling means keeping a system fast as more people use it. You can buy a bigger machine (scale up) or add more machines (scale out). A back-of-envelope estimate is quick, rough arithmetic with round numbers that tells you roughly how big the system must be.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Throughput', 'Work done per second: orders per second, events per second, MB per second.'),
    ('QPS / TPS', 'Queries (or transactions) per second.'),
    ('Peak factor', 'How many times busier the busiest period is than the average.'),
    ('Stateless service', 'A service that keeps no data between requests, so any copy can serve any request.'),
    ('Load balancer', 'A component that spreads incoming requests across many servers.'),
    ('Autoscaling', 'Automatically adding or removing servers based on load.'),
    ('Headroom', 'Spare capacity kept free for spikes and failures.'),
    ('p99 latency', 'The response time that 99% of requests beat; the slowest 1% are slower.'),
]) + '''

  <h3>Numbers for quick estimates</h3>
''' + facts([
    ('Seconds in a day', '86,400 ≈ 1 lakh (10<sup>5</sup>) · seconds in a year ≈ 3 crore (3 × 10<sup>7</sup>)'),
    ('Indian units', '1 lakh = 10<sup>5</sup> · 1 crore = 10<sup>7</sup> · 10 lakh = 1 million · 100 crore = 1 billion'),
    ('Sizes', '1 crore × 1 KB ≈ 10 GB · 1 crore × 1 MB ≈ 10 TB'),
    ('Bandwidth', '1 Gbps ≈ 125 MB/s ≈ 10 TB per day if fully used'),
    ('Typical record sizes', 'payment or order row: 0.25–1 KB · app event: 0.5–2 KB · photo: 2–5 MB'),
    ('Safe target load', 'plan for 50–70% utilisation at peak'),
]) + lv + '''
EXAM> For “vertical vs horizontal scaling”, give the definition, a comparison table (<b>cost, limit, failure impact, complexity, examples</b>) and one example each (a bigger database server; adding web servers behind a load balancer). For estimation questions, always <b>write your assumptions first</b>, then show each step with units.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Vertical (scale up)', 'Bigger CPU, more RAM, faster disks on one machine. No code changes. Hits a ceiling; single point of failure.', 'Bigger machine'),
    ('Horizontal (scale out)', 'More identical machines behind a load balancer. Near-linear growth for stateless work; needs distributed design for data.', 'More machines'),
    ('Diagonal', 'Scale up each node to a sensible size, then scale out with many of them. What most real clusters do.', 'Both'),
    ('Elastic (autoscaling)', 'The number of machines follows demand automatically: more at 8 pm on Diwali, fewer at 4 am.', 'Follows demand'),
]) + '''

  <h3>Side by side</h3>
''' + table(['', 'Scale up (vertical)', 'Scale out (horizontal)'], [
    ['<b>How</b>', 'Bigger machine', 'More machines + load balancer'],
    ['<b>Limit</b>', 'Largest machine available', 'Practically very high (coordination limits it)'],
    ['<b>Cost curve</b>', 'Rises steeply at the top end', 'Roughly linear with machines'],
    ['<b>Failure</b>', 'One machine down = outage', 'One of many down = reduced capacity'],
    ['<b>Code changes</b>', 'Usually none', 'Stateless design, data partitioning'],
    ['<b>Easy for</b>', 'Databases, legacy apps', 'Web/API servers, Spark, Kafka, Cassandra'],
    ['<b>Elasticity</b>', 'Resize needs a restart', 'Add/remove nodes while running'],
]) + '''
TIP> In interviews, say both: “I would first scale up the database to a sensible size and add read replicas; the stateless API tier scales out behind a load balancer; when writes outgrow one database, I would shard.” That shows you know when each approach fits.'''

# ---------------------------------------------------------------- steps (estimation walk-through)
c1 = '''orders_per_day = 10_00_00_000          # 10 crore
avg_per_s = orders_per_day / 1_00_000    # ~1 lakh seconds in a day
peak_per_s = avg_per_s * 5               # Diwali dinner peak
print("average:", avg_per_s, "orders/s | peak:", peak_per_s, "orders/s")'''
c2 = '''orders_per_day = 10_00_00_000
kb_per_order = 1
gb_per_day = orders_per_day * kb_per_order / 1024 / 1024
tb_per_year = gb_per_day * 365 / 1024
print(f"{gb_per_day:.0f} GB/day, {tb_per_year:.0f} TB/year, {tb_per_year * 3:.0f} TB with 3 copies")'''
c3 = '''peak_per_s = 5000
per_node = 400            # orders/s one API server can handle (measured)
target_load = 0.6         # keep 40% headroom
import math
print("API servers at peak:", math.ceil(peak_per_s / (per_node * target_load)))'''
c4 = '''peak_per_s, kb = 5000, 1
mb_per_s = peak_per_s * kb / 1024
print(f"incoming: {mb_per_s:.1f} MB/s = {mb_per_s * 8:.0f} Mbps")'''
c5 = '''arrival = 5000          # requests per second
time_inside = 0.2       # seconds each request spends in the system
print("requests in flight:", int(arrival * time_inside))'''
steps = stepper([
    ('Write your assumptions',
     '<p>10 crore orders on Diwali day · peak hour is 5× the average · each order record ≈ 1 KB · one API server handles ≈ 400 orders/s (from a load test) · keep 3 copies of data.</p>',
     'Assumptions first, out loud. If one is wrong, the interviewer (or your manager) can correct it and the rest of the calculation still stands.'),
    ('Orders per second, average and peak',
     code('python', 'rate.py', c1, run_code(c1)),
     'Dividing by about 1 lakh seconds turns “per day” into “per second”. Systems must handle the <b>peak</b>, not the average.'),
    ('Storage per day and per year',
     code('python', 'storage.py', c2, run_code(c2)),
     'About 95 GB a day is manageable; the yearly total with copies, around 100 TB, is what drives cost. Add indexes, logs and events and the real figure is several times larger.'),
    ('Servers at the peak',
     code('python', 'servers.py', c3, run_code(c3)),
     'Divide the peak by what one server handles at the target load. The API tier is stateless, so these servers scale out behind a load balancer.'),
    ('Network bandwidth',
     code('python', 'bandwidth.py', c4, run_code(c4)),
     'Order data alone is small for the network. Images, app events and replication traffic usually dominate bandwidth, so estimate them separately.'),
    ('Concurrency with Little’s law',
     code('python', 'littles_law.py', c5, run_code(c5)),
     'At the peak about 1,000 requests are in progress at once. That sizes database connection pools and thread counts: too few and requests queue, too many and the database is overwhelmed.'),
])

# ---------------------------------------------------------------- two-view animation (autoscaling)
def ph(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
times = ['6:00 pm', '7:30 pm', '8:00 pm', '8:30 pm', '9:30 pm', '11:30 pm']
see_msgs = [('Diwali offers!', 'Order in 30 s'), ('Busy evening', 'still 30 s'), ('Very busy!', 'still fast'), ('Peak dinner', 'checkout 1.2 s'), ('Orders flowing', 'all smooth'), ('Happy Diwali', 'quiet night')]
see = [ph(times[k], t(180, 86, a, 10.5, bold=True) + t(180, 108, b, 9, 'green', bold=True) + '<circle cx="180" cy="150" r="16" class="s-soft-acc" style="stroke:var(--track);stroke-width:2"/>' + t(180, 155, '🪔' if False else '✦', 12, 'acc')) for k, (a, b) in enumerate(see_msgs)]
load = [20, 45, 80, 100, 55, 15]
nodes = [10, 16, 32, 40, 24, 10]
cpu = [45, 72, 64, 62, 55, 40]
def behind_frame(k):
    o = t(180, 22, f'{times[k]} · {nodes[k]} API servers', 10, bold=True)
    pts = ' '.join(f'{30 + i * 60},{150 - load[i]}' for i in range(k + 1))
    o += '<path d="M30 150h320" class="s-line"/>' + (f'<polyline points="{pts}" style="fill:none;stroke:var(--track);stroke-width:2.5"/>' if k else '') + f'<circle cx="{30 + k * 60}" cy="{150 - load[k]}" r="5" style="fill:var(--track)"/>'
    o += t(34, 40, 'orders per second', 8, 'ink3', anchor='start')
    for i in range(nodes[k]):
        o += fill(30 + (i % 20) * 16, 160 + (i // 20) * 14, 12, 10, 'green', rx=2)
    col = 'red' if cpu[k] > 70 else 'green'
    o += t(346, 40, f'CPU {cpu[k]}%', 9, col, anchor='end', bold=True)
    return o
behind = [behind_frame(k) for k in range(6)]
see_caps = ['6 pm: Diwali offers are live; Riya can order in about 30 seconds.',
            '7:30 pm: the app is busier, but nothing feels different to her.',
            '8 pm: very busy, still fast.',
            '8:30 pm: the dinner peak; checkout still takes about a second.',
            '9:30 pm: orders keep flowing smoothly.',
            '11:30 pm: a quiet night; the festival rush is over.']
behind_caps = ['Normal evening load runs on 10 API servers at 45% CPU.',
               'Orders double; CPU crosses 70%, so the autoscaler starts adding servers (16 so far). New servers take a few minutes to boot, which is why teams pre-scale for known peaks.',
               'The autoscaler has added more servers: 32 now share the load, and CPU is back near the 60% target.',
               'At the peak, 40 stateless servers behind the load balancer handle the traffic. The database tier was scaled up and given read replicas the day before.',
               'Load falls and the autoscaler removes servers gradually (24), keeping a safety margin.',
               'Back to 10 servers. The company paid for 40 servers only for the hours it needed them. (Numbers are illustrative.)']
two = anim_two('Autoscaling on Diwali night', 'What Riya sees, and what the autoscaler does', 'The app on Diwali evening, staying fast as traffic rises and falls',
               'Orders per second rising and falling, with the number of API servers following', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: the estimate (10 crore orders/day)
rows = [('Orders per day', '10 crore', '10⁸'),
        ('Average per second', '÷ 1 lakh', '≈ 1,000 /s'),
        ('Peak (× 5)', '× 5', '≈ 5,000 /s'),
        ('Storage per day', '× 1 KB', '≈ 95 GB'),
        ('Per year, 3 copies', '× 365 × 3', '≈ 100 TB'),
        ('API servers', '÷ (400 × 0.6)', '21')]
def est(n):
    o = t(180, 20, 'Back-of-envelope: 10 crore orders on Diwali day', 9.6, 'acc', bold=True)
    for k, (a, op, r) in enumerate(rows):
        y = 34 + k * 22
        on = k < n
        o += box(14, y, 332, 18, 'green' if k == n - 1 else 'card', rx=4) if on else ''
        if on:
            o += t(22, y + 13, a, 8.8, anchor='start', bold=True) + t(200, y + 13, op, 8.6, 'ink2', mono=True) + t(338, y + 13, r, 8.8, 'ink', anchor='end', bold=True)
    return o
fr1 = [est(1) + cap('Start with the business number and write it down.', '', 'card', y=176, h=34),
       est(3) + cap('Per second ≈ per day ÷ 1 lakh. Then apply the peak factor.', '', 'blue', y=176, h=34),
       est(4) + cap('Storage = count × size. 1 crore × 1 KB ≈ 10 GB.', '', 'blue', y=176, h=34),
       est(5) + cap('A year with 3 copies ≈ 100 TB: a real cost item.', '', 'blue', y=176, h=34),
       est(6) + cap('Servers = peak ÷ (capacity per server × target load).', '', 'green', y=176, h=34)]
s1 = anim_one('Real-time scenario 1', 'Estimating Diwali day in two minutes',
              'Watch Kabir answer the interview question line by line. Every step is simple arithmetic with round numbers; the skill is the order of the steps and writing down the assumptions.',
              'The estimation recipe', 'A table of estimation steps for 10 crore orders a day', fr1,
              ['Write the given number: 10 crore orders on the day.',
               'Divide by about 1 lakh seconds: around 1,000 orders per second on average, and about 5,000 per second at the dinner peak.',
               'Multiply by the record size: at 1 KB per order, about 95 GB a day.',
               'Over a year, with three copies for safety, that is roughly 100 TB, which tells you storage is a cost to plan for.',
               'Servers: 5,000 per second ÷ (400 per server × 60% target load) ≈ 21 API servers at peak. Say the assumptions aloud so they can be challenged.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: stateful vs stateless
def servers(n, sess=None, lb=True, redis=False):
    o = (label_box(140, 20, 80, 30, ['load balancer'], 'acc', 8.8) if lb else '')
    for i in range(n):
        step = 300 // max(n, 1)
        w = min(70, step - 8)
        x = 30 + i * step
        o += label_box(x, 80, w, 40, [f'API {i + 1}'] + ([sess[i]] if sess and sess[i] else []), 'card', 8.8) + arrow(180, 52, x + w // 2, 78, 'ink3', 1.2)
    if redis:
        o += label_box(110, 136, 140, 30, ['Redis: sessions'], 'red', 8.8)
    return o
fr2 = [
    servers(1, ['Riya’s cart']) + cap('One server keeps Riya’s cart in its own memory.', 'Works fine… until we add servers.', 'card', y=150, h=44),
    servers(3, ['Riya’s cart', '', '']) + t(180, 140, 'next request → API 2: “your cart is empty?!”', 9, 'red', bold=True) + cap('Added servers: the load balancer sends her next tap', 'to API 2, which has never seen her cart.', 'red', y=150, h=44),
    servers(3, ['Riya’s cart', '', '']) + t(180, 140, 'sticky sessions: Riya always → API 1', 9, 'acc', bold=True) + cap('Quick fix: sticky sessions. But if API 1 dies,', 'her cart dies with it, and load gets uneven.', 'amber', y=150, h=44),
    servers(3, redis=True) + arrow(65, 122, 140, 138, 'ink3', 1.2) + arrow(180, 122, 180, 136, 'ink3', 1.2) + arrow(295, 122, 220, 138, 'ink3', 1.2) + cap('Proper fix: move the cart to Redis. Every API server', 'is now stateless; any of them can serve any tap.', 'green', y=172, h=44),
    servers(5, redis=True) + cap('Now scaling out is just “add more copies”.', 'Servers can die or be added at any time.', 'green', y=172, h=44),
]
s2 = anim_one('Real-time scenario 2', 'Why Riya’s cart vanished when we added servers',
              'Scaling out is easy only for stateless services. Watch what happens to a cart stored in a server’s memory when a second and third server are added.',
              'Stateful vs stateless', 'API servers behind a load balancer, first keeping carts in memory, then in Redis', fr2,
              ['With one server, keeping Riya’s cart in that server’s memory works perfectly.',
               'Two more servers are added. The load balancer sends her next tap to API 2, which has no idea what is in her cart. The cart appears empty.',
               'A quick fix is <b>sticky sessions</b>: always route Riya to API 1. But if API 1 restarts, the cart is lost, and some servers end up much busier than others.',
               'The real fix is to move the state out: carts live in Redis, so every API server is <b>stateless</b> and any server can handle any request.',
               'Now scaling out is simply adding identical copies, and servers can be replaced or removed at any time without losing anything.'])

# ---------------------------------------------------------------- scenario 3 (advanced): USL
import math
alpha, beta = 0.03, 0.0008
def usl(n):
    return n / (1 + alpha * (n - 1) + beta * n * (n - 1))
Ns = [1, 8, 16, 32, 48, 64]
Xs = [usl(n) for n in Ns]
mx = max(usl(n) for n in range(1, 80))
def px(n):
    return 34 + n / 64 * 300
def py(x):
    return 160 - x / 14 * 126
curve = ' '.join(f'{px(n):.1f},{py(usl(n)):.1f}' for n in range(1, 65))
lin = f'{px(1):.1f},{py(1):.1f} {px(14):.1f},{py(14):.1f}'
static3 = ('<path d="M34 160h306M34 160V24" class="s-line"/>' + t(36, 20, 'throughput (× one node)', 8.2, 'ink3', anchor='start') + t(340, 152, 'nodes →', 8.2, 'ink3', anchor='end')
           + ''.join(t(px(n), 174, str(n), 7.8, 'ink3') for n in [8, 16, 32, 48, 64]) + f'<polyline points="{lin}" style="fill:none;stroke:var(--line);stroke-width:1.5;stroke-dasharray:4 3"/>'
           + t(px(14) + 6, py(14) + 4, 'perfect scaling', 7.8, 'ink3', anchor='start'))
def pt(i, col='acc'):
    n, x = Ns[i], Xs[i]
    return f'<circle cx="{px(n):.1f}" cy="{py(x):.1f}" r="5" style="fill:{FILL[col]}"/>' + t(px(n), py(x) - 9, f'{x:.1f}×', 8.4, col, bold=True)
part_curve = lambda upto: f'<polyline points="{" ".join(f"{px(n):.1f},{py(usl(n)):.1f}" for n in range(1, upto + 1))}" style="fill:none;stroke:var(--track);stroke-width:2.5"/>'
fr3 = [
    part_curve(8) + pt(1) + cap(f'8 nodes: {Xs[1]:.1f}× faster. Not 8×, because of', 'waiting on shared resources (contention).', 'blue', y=178, h=36),
    part_curve(16) + pt(2) + cap(f'16 nodes: about {Xs[2]:.0f}×. The gap to perfect grows.', '', 'blue', y=178, h=36),
    part_curve(32) + pt(3) + cap(f'32 nodes: about {Xs[3]:.0f}×, near the peak. Nodes spend', 'much of their time talking to each other.', 'amber', y=178, h=36),
    part_curve(64) + pt(5, 'red') + cap('64 nodes: slower than 32! Coordination grows', 'with every pair of nodes (coherence cost).', 'red', y=178, h=36),
    part_curve(64) + pt(3, 'green') + cap('Fix: less sharing. Partition data so nodes work', 'independently; avoid global locks and chatty syncs.', 'green', y=178, h=36),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'When 64 machines are slower than 32',
              'Adding machines is not free: they wait for shared resources and must talk to each other to stay in agreement. The Universal Scalability Law shows the effect. Watch throughput as a job grows from 8 to 64 nodes.',
              'Universal Scalability Law', 'Throughput versus number of nodes, rising, peaking and then falling', fr3,
              [f'With 8 nodes the job runs about {Xs[1]:.1f} times faster than on one node. Some time is lost waiting for shared resources such as one database or one lock: <b>contention</b>.',
               f'With 16 nodes, about {Xs[2]:.0f} times faster. Each extra node adds less than the one before.',
               f'Around 32 nodes the curve peaks near {Xs[3]:.0f}×. The nodes now spend a lot of time exchanging messages to stay consistent.',
               f'With 64 nodes throughput falls to about {Xs[5]:.0f}×: slower than 32. The cost of every node coordinating with every other node grows faster than the work added: <b>coherence</b>.',
               'The fix is design, not hardware: partition data so nodes work independently, remove global locks, batch messages and avoid chatty synchronisation. (Curve uses α = 0.03, β = 0.0008 for illustration.)'],
              static=static3)

realworld = '''  <p>Three live scenarios: a two-minute capacity estimate, a cart that vanishes when servers are added, and an advanced look at why more machines can mean less speed.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Scaling decisions at real companies</h3>
''' + usecase('<path d="M14 70 Q40 66 60 40 T106 20" style="fill:none;stroke:var(--track);stroke-width:3"/><rect x="14" y="74" width="92" height="6" rx="2" style="fill:var(--green)"/>',
              '1. Sale days and cricket finals: pre-scaling', 'Shopping and streaming apps scale out days in advance of known peaks (festive sales, IPL finals), run load tests at several times the expected traffic, and keep autoscaling as a safety net.', ['Forecast peak', '*Load test + pre-scale', 'Autoscale on the day']) + usecase(
    '<rect x="16" y="22" width="40" height="46" rx="4" class="s-soft-blue" style="stroke:var(--blue)"/><rect x="64" y="22" width="18" height="46" rx="3" style="fill:var(--blue);opacity:.5"/><rect x="88" y="22" width="18" height="46" rx="3" style="fill:var(--blue);opacity:.5"/>',
    '2. Databases: scale up, add replicas, then shard', 'A start-up’s single PostgreSQL server is first moved to a larger machine, then given read replicas for reports, and only when writes outgrow it is the data sharded or moved to a distributed database.', ['Bigger DB', '*Read replicas', 'Sharding']) + usecase(
    '<circle cx="30" cy="45" r="10" style="fill:var(--green)"/><circle cx="60" cy="45" r="10" style="fill:var(--green)"/><circle cx="90" cy="45" r="10" style="fill:var(--green)"/>',
    '3. Spark clusters that grow per job', 'Data platforms start a cluster for a nightly job, let it autoscale from a few nodes to dozens while the heavy step runs, and shut it down afterwards, because storage lives separately in object storage.', ['Job starts', '*Autoscale workers', 'Cluster shuts down']) + usecase(
    '<text x="60" y="40" text-anchor="middle" font-size="11" font-weight="700" class="s-acc mono">Q = ?</text><text x="60" y="62" text-anchor="middle" font-size="9" class="s-ink">≈ 5,000/s</text>',
    '4. System-design interviews', 'Most data and backend interviews include an estimation step: users, requests per second, storage per year, bandwidth and machine count, with stated assumptions. The method matters more than the exact number.', ['Assumptions', '*Round-number maths', 'Design choices'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', '“How many servers for Diwali?”', story)
        + part(2, 'definition', 'Definition', 'Scalability and back-of-envelope estimation', definition)
        + part(3, 'types', 'Types and ways to use it', 'Four ways to scale', types)
        + part(4, 'steps', 'Step by step', 'A complete estimate for 10 crore orders a day', steps)
        + part(5, 'animation', 'See it happen', 'Diwali night: what Riya sees, and what the autoscaler does', '  <p>Step through the six frames. Left: the app as Riya experiences it. Right: orders per second and the number of servers behind it.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: scaling in practice', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('System design · estimation', 'Fresher', 'Estimate storage for a photo feature',
            'A food app will let users attach up to 2 photos to each review. 50 lakh reviews are written a day and 20% include photos. Estimate storage per year.',
            'can you structure an estimate with clear assumptions and units?',
            '<p>Assume 1.5 photos per review that has photos, 3 MB per photo, plus 2 thumbnails of 100 KB. Photos per day = 50 lakh × 20% × 1.5 = 15 lakh. Storage per day ≈ 15 lakh × 3.2 MB ≈ 4.6 TB. Per year ≈ 1.7 PB before replication (object storage handles durability internally). Then discuss: compress or resize images, move old photos to cheaper tiers, serve through a CDN.</p>',
            'jumping to a number without assumptions, or forgetting thumbnails and tiers.')
        + scn('Scaling · architecture', '1–3 years', 'The API is slow at 8 pm every day',
              'A delivery app’s API slows down every evening. Adding more API servers didn’t help.',
              'do you find the real bottleneck before scaling?',
              '<ol><li>Check where time goes: API CPU, database CPU and connections, cache hit ratio, external calls.</li><li>If the database is the bottleneck, more API servers just add more database connections and make it worse.</li><li>Fixes: cache hot reads, add read replicas, tune slow queries and indexes, pool connections, scale the database up; shard if writes are the limit.</li><li>Then autoscale the stateless tier with a sensible maximum.</li></ol>',
              'adding servers blindly; scaling the wrong tier.')
        + scn('Reliability · statelessness', '1–3 years', 'Users get logged out randomly',
              'After moving from one server to five behind a load balancer, users complain of random logouts and empty carts.',
              'do you recognise in-memory session state?',
              '<p>Sessions and carts are stored in each server’s memory, so requests landing on another server don’t find them. Move session state to a shared store (Redis) or use signed tokens (JWT) for authentication, and store carts in Redis or the database. Avoid relying on sticky sessions, which break when servers restart and unbalance load.</p>',
              'increasing session timeouts or pinning all users to one server.')
        + scn('Performance · advanced', '3+ years', 'Doubling the cluster made the job slower',
              'A distributed job ran in 40 minutes on 50 nodes. On 100 nodes it took 55 minutes.',
              'do you understand contention and coordination costs?',
              '<p>Look for shared bottlenecks (one metadata service, one database, a global lock, a single reducer) and coordination overhead (shuffles that grow with node count, many small tasks, frequent synchronisation). Measure stage by stage. Fixes include fewer, larger partitions, reducing shuffles (broadcast small tables, pre-partition data), removing global locks, and choosing the node count near the measured optimum rather than “as many as possible”.</p>',
              'assuming linear scaling and adding even more nodes.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written', [round(x, 1) for x in Xs], round(mx, 1))
