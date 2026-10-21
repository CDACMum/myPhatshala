import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='07-big-data-at-indian-scale', n='4.7',
    module_label='Module 4 · The Ecosystem',
    title='Big data at Indian scale: UPI, IRCTC, live cricket and sale days',
    desc='Case studies of big data at Indian scale: UPI payments (24 billion a month), IRCTC Tatkal rush (37,410 tickets a minute), live cricket streaming (5.9 crore concurrent viewers) and e-commerce sale days. Learn to convert headline numbers into TPS and peaks, and the techniques behind them: waiting rooms, rate limiting, idempotency, caching, CDNs, partitioning and streaming analytics. Animations and a load estimator for your PC.',
    og_desc='How do UPI, IRCTC and live cricket streams survive crores of users? Turn headline numbers into TPS and learn the patterns behind them.',
    minutes=30, level='Beginner → Advanced',
    lead='UPI moves around 80 crore payments a day, IRCTC has sold over 37,000 tickets in a single minute, and 5.9 crore people once watched the same cricket final at the same moment. In this lesson you turn those <b>headline numbers into requests per second</b>, follow one UPI payment through the network, watch a <b>waiting room</b> tame the Tatkal rush, see why a retry must never debit twice, and learn how live streams reach crores of phones.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Load estimator for your PC'],
)

RUN = dict(
    heading='Turn headline numbers into engineering numbers',
    intro='<p>A few published figures are converted into average transactions per second and a design peak. Then try the challenges: peak ratios, event volumes, waiting-room maths, CDN bandwidth and hot keys.</p>',
    code='''figures = {                          # (count, seconds it covers)
    "UPI, Sep 2026 (month)": (24.07e9, 30 * 86_400),
    "IRCTC record day":      (18.4e5, 86_400),
    "IRCTC peak minute":     (37_410, 60),
}
PEAK_RATIO = 3                       # assumption for daily or monthly averages

for name, (count, seconds) in figures.items():
    tps = count / seconds
    print(f"{name:22}: {tps:8,.0f} per second")
print(f"UPI design peak at x{PEAK_RATIO}: {24.07e9 / (30 * 86_400) * PEAK_RATIO:,.0f} TPS")
''',
    anno=[
        ('    tps = count / seconds', 'Every design starts here: divide a total by the seconds it covers.'),
        ('PEAK_RATIO = 3                       # assumption for daily or monthly averages', 'Averages hide peaks. A peak minute is already a peak, so the ratio is applied only to long averages.'),
    ],
    tasks=[
        dict(label='1 · Average and peak', hint='Press <b>Run</b>. Change <code>PEAK_RATIO</code> to 5. Notice that the IRCTC peak minute is much busier than its record-day average.', code=None),
        dict(label='2 · Event volume', hint='Each UPI transaction creates about 10 events of 1 KB across systems. Estimate TB per day and per year, with 3 copies. Try 2 KB events.',
             code='''txn_per_day = 24.07e9 / 30
events_per_txn, kb = 10, 1
tb_per_day = txn_per_day * events_per_txn * kb / 1e9
print(f"{tb_per_day:.1f} TB/day, {tb_per_day * 3:.1f} TB/day with 3 copies")
print(f"{tb_per_day * 3 * 365 / 1000:.1f} PB a year with 3 copies")
'''),
        dict(label='3 · Waiting room maths', hint='Users arrive at a rate; the system admits at a fixed rate. How long until the queue is empty? Try 50,000 arrivals.',
             code='''arrivals, arrival_seconds, admit_rate = 30_000, 60, 250
clear_time = max(arrival_seconds, arrivals / admit_rate)
print(f"queue empty after {clear_time:.0f} s")
print(f"peak queue length about {arrivals - admit_rate * arrival_seconds:,} users")
'''),
        dict(label='4 · CDN bandwidth', hint='Bandwidth = viewers × bitrate. Compare all viewers at 2.5 Mbps with a mix where 40% drop to 0.8 Mbps on weak networks.',
             code='''viewers = 5.9e7
full = viewers * 2.5 / 1e6
mixed = (viewers * 0.6 * 2.5 + viewers * 0.4 * 0.8) / 1e6
print(f"all at 2.5 Mbps : {full:,.0f} Tbps")
print(f"adaptive mix    : {mixed:,.0f} Tbps")
'''),
        dict(label='5 · Hot key (advanced)', hint='Searches are partitioned by train number across 8 servers. One popular train gets 30% of all searches. Print the load on the busiest server. Then split the hot train across 4 servers.',
             code='''total, servers, hot_share = 40_000, 8, 0.30
hot = total * hot_share
others = (total - hot) / servers
print("busiest server, hot train on one:", round(others + hot))
print("busiest server, hot split in 4  :", round(others + hot / 4))
print("perfectly even                  :", total // servers)
'''),
        dict(label='6 · Idempotency (advanced)', hint='A retried payment carries the same ID. Run it, then remove the <code>if</code> check and see the double debit.',
             code='''balance, seen = 5000, set()
def debit(txn_id, amount):
    global balance
    if txn_id in seen:
        return "already processed"
    seen.add(txn_id)
    balance -= amount
    return "debited"
print(debit("7781", 500), balance)
print(debit("7781", 500), balance)   # retry after a timeout
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: India-scale load and a Tatkal waiting room',
    intro='<p>This program converts published UPI, IRCTC and live-streaming figures into per-second load and bandwidth, then simulates a virtual waiting room: 30,000 users arrive in one minute and are admitted at 250 per second. Change the arrival count or admit rate and run it again. Save it as <code>indian_scale.py</code>.</p>',
    items=[
        dict(title='From headlines to TPS, and a waiting room', file='indian_scale.py',
             cmd=open(os.path.join(HERE, 'indian_scale.py')).read() + '\n# In a terminal:  python indian_scale.py',
             output=open(os.path.join(HERE, 'indian_scale.out')).read(),
             note='Recorded from a real run with Python 3.13. The figures are published numbers (see Sources); the 2.5 Mbps bitrate and the 250-per-second admit rate are assumptions for illustration, not IRCTC or Hotstar settings.'),
    ],
)

TRACE = dict(
    heading='Admitting a rush, one user at a time',
    intro='<p>Five users arrive almost together; the system admits one every 2 seconds. Watch each user’s admit time and wait being calculated.</p>',
    code='''arrivals = [0, 0, 1, 1, 2]
gap = 2
next_free = 0
waits = []
for t in arrivals:
    start = max(t, next_free)
    waits.append(start - t)
    next_free = start + gap
print(waits, "max wait:", max(waits))
''',
    notes={6: 'Admit :: A user starts at their arrival time or when the next slot is free, whichever is later.',
           7: 'Wait :: Time spent in the queue instead of on the servers.',
           8: 'Next slot :: The admit rate is fixed, so the next slot moves forward by the gap.'},
)

WORKED_INTRO = 'Four estimation and design calculations from India-scale systems. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Estimation · TPS', title='Per-second load from a daily figure',
         problem='<p>IRCTC’s record day was 18.4 lakh tickets. Find the average tickets per second, and compare it with the record minute of 37,410 tickets.</p>',
         inp='18.4 lakh per day · 37,410 per minute',
         approach=['Average per second = daily total ÷ 86,400.',
                   'Peak per second = peak minute ÷ 60.',
                   'Ratio = peak ÷ average.'],
         code='''day_total, peak_minute = 18_40_000, 37_410
avg = day_total / 86_400
peak = peak_minute / 60
print(f"average {avg:.0f}/s, peak {peak:.0f}/s, ratio {peak / avg:.0f}x")
''', notes={4: 'Ratio :: The peak is many times the daily average: design for the peak.'},
         tryit='IRCTC plans to handle over 1 lakh bookings a minute. What is that per second, and how many times today’s peak?'),
    dict(level='i', tag='Capacity · servers', title='How many servers for the UPI peak?',
         problem='<p>Average UPI load is about 9,300 TPS. Design for 4× peak and keep 30% headroom. Each application server safely handles 800 TPS. How many servers, and how many with one full data centre out (two equal sites)?</p>',
         inp='9,300 TPS, 4× peak, 30% headroom, 800 TPS/server, 2 sites',
         approach=['Design load = average × peak ratio × (1 + headroom).',
                   'Servers = load ÷ per-server capacity, rounded up.',
                   'If one of two sites can fail, each site must carry the full load.'],
         code='''import math
design = 9_300 * 4 * 1.3
servers = math.ceil(design / 800)
print(f"design load {design:,.0f} TPS -> {servers} servers")
print(f"survive one site down -> {servers} per site, {servers * 2} in total")
''', notes={3: 'Round up :: You cannot run part of a server.'},
         tryit='Use three sites, each able to carry half the load. How many servers in total now?'),
    dict(level='i', tag='Payments · idempotency', title='Count the double debits that idempotency prevents',
         problem='<p>A log of payment requests includes retries with the same transaction ID. Count the unique payments, the retries, and the amount that would have been wrongly debited without idempotency.</p>',
         inp='(txn_id, amount) pairs',
         approach=['Track IDs already processed in a set.',
                   'A repeated ID is a retry: count it and its amount.',
                   'Unique IDs are the real payments.'],
         code='''log = [("a1", 120), ("a2", 500), ("a1", 120), ("a3", 80), ("a2", 500), ("a2", 500)]
seen, retries, saved = set(), 0, 0
for txn, amount in log:
    if txn in seen:
        retries += 1
        saved += amount
    else:
        seen.add(txn)
print(len(seen), "payments,", retries, "retries, Rs", saved, "not double-debited")
''', notes={4: 'Retry :: Same ID seen before: return the old result, debit nothing.'},
         tryit='Add a timestamp and treat the same ID after 24 hours as an error to investigate, not a retry.'),
    dict(level='a', tag='Live streaming · capacity', title='Plan CDN capacity for a final',
         problem='<p>Expect 6 crore concurrent viewers. Viewers watch at 0.8, 1.5, 2.5 or 4 Mbps in shares 20%, 35%, 35%, 10%. Each CDN provider can deliver up to 60 Tbps for this event. How many providers are needed with 25% spare, and what share of viewers is lost if one provider fails?</p>',
         inp='6 crore viewers, bitrate mix, 60 Tbps per CDN, 25% spare',
         approach=['Average bitrate = Σ share × bitrate.',
                   'Peak Tbps = viewers × average bitrate.',
                   'Providers = ceil(peak × 1.25 ÷ 60); a failure removes 60 Tbps.'],
         code='''import math
mix = {0.8: 0.20, 1.5: 0.35, 2.5: 0.35, 4.0: 0.10}
avg_mbps = sum(b * s for b, s in mix.items())
peak_tbps = 6e7 * avg_mbps / 1e6
cdns = math.ceil(peak_tbps * 1.25 / 60)
left = (cdns - 1) * 60
print(f"avg {avg_mbps:.2f} Mbps, peak {peak_tbps:.0f} Tbps, CDNs needed {cdns}")
print(f"one CDN down: {left} Tbps, covers {min(1, left / peak_tbps) * 100:.0f}% at full quality")
''', notes={4: 'Bandwidth :: Viewers × average bitrate.', 5: 'Spare :: Headroom for surprises and failover.'},
         tryit='If one CDN fails, players can drop everyone to 0.8 Mbps. Would the remaining CDNs then cover all viewers?'),
]

QUIZ = [
    dict(q='UPI handled about 24 billion transactions in a 30-day month. What is the approximate average per second?', options=['About 93', 'About 930', 'About 9,300', 'About 93,000'], answer=2,
         why='24 billion ÷ (30 × 86,400 seconds) ≈ 9,300 per second.'),
    dict(q='Why do systems design for the peak rather than the average?', options=['Peaks are rare and can be ignored', 'Traffic is uneven; the busiest moments can be many times the average and that is when failures hurt most', 'Averages are hard to calculate', 'Peaks are cheaper'], answer=1,
         why='Tatkal, festival evenings and match finishes create load many times the average.'),
    dict(q='What does a virtual waiting room do during a booking rush?', options=['Deletes extra users', 'Admits users to the system at a safe rate and holds the rest in a fair queue', 'Speeds up the database', 'Books tickets for everyone'], answer=1,
         why='It turns an overload into a predictable wait, protecting the booking core.'),
    dict(q='A payment request is retried after a timeout. What prevents a double debit?', options=['A faster network', 'An idempotency key: the same unique transaction ID on the retry', 'Deleting the first request', 'Caching the balance'], answer=1,
         why='The server recognises the ID and returns the earlier result instead of debiting again.'),
    dict(q='What carries most of the load when crores watch the same live match?', options=['The origin server alone', 'Content delivery networks caching video segments near viewers', 'The payment gateway', 'A single database'], answer=1,
         why='CDN edges serve identical segments to many viewers, so the origin serves each only a few times.'),
    dict(q='What is adaptive bitrate streaming?', options=['Charging viewers by bitrate', 'The player switches between quality levels depending on network conditions', 'Compressing video once a day', 'Streaming only in HD'], answer=1,
         why='Lower quality instead of freezing keeps viewers watching on weak networks or during congestion.'),
    dict(q='One popular train receives 30% of all searches and overloads one partition. What is this problem called?', options=['Cold start', 'Hot key (hot partition)', 'Split brain', 'Data skewless'], answer=1,
         why='Caching, splitting the hot key or replicating it spreads the load.'),
    dict(q='During a sale, the site slows down. What should be switched off first?', options=['Checkout', 'Payment', 'Non-essential features like recommendations or reviews widgets', 'Order database'], answer=2,
         why='Graceful degradation protects the critical path (cart, checkout, payment) by shedding extras.'),
]

REVISION = [
    'Design in per-second units: total ÷ seconds. UPI ≈ 24 billion/month ≈ 9,300 TPS average (Sep 2026).',
    'Plan for the <b>peak</b> (peak-to-average ratio) plus headroom; pre-scale for known events.',
    'Separate the critical path (pay, book, play, order) from extras; queue or switch off extras under load.',
    'Waiting rooms and rate limits turn overload into fair waits.',
    'Payments: strong consistency, <b>idempotency keys</b>, reversals and daily reconciliation.',
    'Live streaming: segments + adaptive bitrate + multi-CDN; 5.9 crore concurrent peak (2023 final).',
    'Hot keys break even partitioning; every event also feeds streams and the lake for fraud, dashboards and audit.',
]
FAQ = [
    ('How does UPI handle so many transactions?', 'UPI connects payment apps and banks through NPCI’s central switch, which routes each request to the right banks. Scale comes from horizontally scaled, replicated systems at NPCI and at banks, short and well-defined messages, unique transaction IDs that make retries safe, timeouts with reversal flows, and daily settlement and reconciliation. Detailed internal designs are not fully public.'),
    ('Why does the IRCTC site slow down at Tatkal time?', 'Tatkal booking opens at fixed times (10 am for AC classes, 11 am for non-AC), so a very large number of users arrive within seconds for limited seats. The peak is many times the daily average. Systems handle it with queues or waiting rooms, rate limits, caching of availability and fares, bot controls and capacity upgrades; IRCTC has announced plans to handle over one lakh bookings a minute.'),
    ('How do streaming apps handle crores of concurrent viewers?', 'Video is encoded into short segments at multiple bitrates and delivered through content delivery networks with servers close to viewers, often several CDNs at once. Capacity is reserved before big events, players adapt quality to network conditions, and non-essential features can be switched off. Player events stream into analytics for quality monitoring and ad delivery.'),
    ('What is idempotency and why is it important in payments?', 'An operation is idempotent if doing it more than once has the same effect as doing it once. In payments, each request carries a unique ID; if a timeout causes a retry, the server recognises the ID and returns the original result rather than debiting again. It makes retries, which are unavoidable in distributed systems, safe.'),
    ('How do you estimate load in a system design interview?', 'Start from users or a published total, convert to per-second averages (divide by 86,400 for a day), apply a peak-to-average ratio from experience or history, add headroom, and estimate data size per request and per day. State every assumption clearly and round sensibly; interviewers care more about the reasoning than exact numbers.'),
]

PRACTICE_INTRO = 'Estimation and design problems based on Indian systems. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Daily to per second', stmt='A system handles 50 crore requests a day. Print the average requests per second.', inp='50 crore/day',
         code='''print(round(50e7 / 86_400))
''', explain='Divide by 86,400 seconds in a day.'),
    dict(level='easy', title='Peak minute to per second', stmt='37,410 tickets were booked in one minute. Print tickets per second.', inp='37,410/min',
         code='''print(round(37_410 / 60))
''', explain='A peak minute already reflects peak load; just divide by 60.'),
    dict(level='easy', title='Crore to number', stmt='Print 5.9 crore as a plain number with commas.', inp='5.9 crore',
         code='''print(f"{int(5.9e7):,}")
''', explain='1 crore = 10 million, so 5.9 crore = 59 million.'),
    dict(level='medium', title='Design peak', stmt='Average is 12,000 TPS. Design for 4× peak with 25% headroom. Print the design TPS.', inp='12,000, 4×, 25%',
         code='''print(int(12_000 * 4 * 1.25))
''', explain='Peak ratio first, then headroom on top.'),
    dict(level='medium', title='Queue clear time', stmt='45,000 users arrive in 60 s; 300 are admitted per second. Print when the queue empties.', inp='45,000, 60 s, 300/s',
         code='''print(max(60, 45_000 / 300), "seconds")
''', explain='The queue cannot clear before the last arrival, nor faster than the admit rate allows.'),
    dict(level='advanced', title='Event storage', stmt='9,300 TPS, 8 events per transaction, 1.2 KB each, 3 replicas. Print TB per day.', inp='as given',
         code='''print(round(9_300 * 86_400 * 8 * 1.2e3 * 3 / 1e12, 1), "TB/day")
''', explain='Rate × seconds × events × size × copies.'),
    dict(level='advanced', title='Remove duplicate retries', stmt='Given IDs ["t1","t2","t1","t3","t2"], print the unique IDs in first-seen order.', inp='list of IDs',
         code='''ids = ["t1", "t2", "t1", "t3", "t2"]
print(list(dict.fromkeys(ids)))
''', explain='dict.fromkeys keeps first occurrences in order; this is deduplication by ID.'),
    dict(level='business', title='Sale-day capacity', stmt='Last year’s sale peaked at 1.8 lakh orders per minute. Growth is 35%. Plan with 30% headroom. Print orders per second to design for.', inp='1.8 lakh/min, +35%, +30%',
         code='''print(round(1.8e5 * 1.35 * 1.3 / 60))
''', explain='Grow last year’s peak, add headroom, convert to per second.'),
    dict(level='business', title='Cost of downtime', stmt='A platform processes Rs 29.37 lakh crore a month. Print the average value flowing per minute in crore.', inp='Rs 29.37 lakh crore/month',
         code='''per_min = 29.37e12 / (30 * 24 * 60)
print(f"Rs {per_min / 1e7:,.0f} crore per minute")
''', explain='This is why payment systems invest heavily in availability.'),
]

SCN_INTRO = 'Questions about India-scale systems from interviews and real projects. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
