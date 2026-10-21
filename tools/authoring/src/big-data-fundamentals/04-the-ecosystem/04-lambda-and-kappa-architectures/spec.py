import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='04-lambda-and-kappa-architectures', n='4.4',
    module_label='Module 4 · The Ecosystem',
    title='Lambda and Kappa architectures explained',
    desc='Lambda architecture (batch, speed and serving layers) and Kappa architecture (one stream path with log replay) explained with a Diwali sale dashboard: why live and final numbers differ, how views are merged, how to replay Kafka after a bug, and how to choose. Beginner to Advanced, real-time animations, Python simulations and a replay demo for your PC.',
    og_desc='Live counter says ₹2.31 crore, finance says ₹2.24 crore. Learn how Lambda merges both, how Kappa replays a log, and which to choose.',
    minutes=28, level='Beginner → Advanced',
    lead='During a big sale, the CEO wants live numbers; the next morning, finance wants exact ones. The <b>Lambda architecture</b> runs a fast stream path and an accurate batch path and merges them. The <b>Kappa architecture</b> keeps only the stream and fixes history by replaying the event log. This lesson builds both in Python, shows them working on sale night, and teaches you how architects choose.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Log replay on your PC'],
)

RUN = dict(
    heading='Lambda in miniature: batch view + speed view',
    intro='<p>An append-only list of events plays the master dataset. Last night\'s batch job computed an exact view up to a cut-off; the speed layer keeps a running total for everything after it. The query adds the two. Then, in the challenges, replay the log Kappa-style, watch two codebases drift, and size a log for replay.</p>',
    code='''# The master dataset: every event ever, append-only (sale = +, refund = -)
master = [("O1", 120, "sale"), ("O2", 250, "sale"), ("O3", 90, "sale"),
          ("O2", 250, "refund"), ("O4", 300, "sale"),          # up to last night
          ("O5", 140, "sale"), ("O6", 60, "sale")]             # arrived today

def revenue(events):
    total = 0
    for order, amount, kind in events:
        total += -amount if kind == "refund" else amount
    return total

CUTOFF = 5                                 # last night's batch job processed events 0-4

batch_view = revenue(master[:CUTOFF])      # BATCH LAYER: exact, recomputed nightly
speed_view = revenue(master[CUTOFF:])      # SPEED LAYER: only events since the batch run

print("Batch view (till last night):", batch_view)
print("Speed view (today, live)    :", speed_view)
print("Query answer = batch + speed:", batch_view + speed_view)

# A new event arrives: only the speed view changes, instantly
master.append(("O4", 300, "refund"))
speed_view = revenue(master[CUTOFF:])
print("After a refund arrives      :", batch_view + speed_view)
''',
    anno=[
        ('master = [...]', 'The <b>master dataset</b> is only ever appended to. Corrections (like a refund) are new events, not edits.'),
        ('batch_view = revenue(master[:CUTOFF])', 'The batch layer recomputes from <b>all</b> raw events up to the cut-off. Accurate, but only as fresh as its last run.'),
        ('speed_view = revenue(master[CUTOFF:])', 'The speed layer handles only the recent tail, so it can update within seconds.'),
        ('batch_view + speed_view', 'The <b>serving layer</b>\'s job: merge the two views into one answer.'),
    ],
    tasks=[
        dict(label='1 · Merge views', hint='Press <b>Run</b>. Then simulate tonight\'s batch run: set <code>CUTOFF = len(master)</code> before computing the views. The speed view becomes 0 and the answer is unchanged.', code=None),
        dict(label='2 · Kappa replay', hint='Version 1 of the stream job counted refunds as sales (a bug). Kappa fixes history by replaying the whole log through version 2. Write a version 3 that also ignores orders under ₹100 and replay again.',
             code='''log = [("O1", 120, "sale"), ("O2", 250, "sale"), ("O2", 250, "refund"),
       ("O3", 90, "sale"), ("O4", 300, "sale"), ("O4", 300, "refund")]

def v1(total, e):                        # buggy: refunds added as sales
    return total + e[1]

def v2(total, e):                        # fixed: refunds subtract
    return total - e[1] if e[2] == "refund" else total + e[1]

def replay(job, events, from_offset=0):
    total = 0
    for e in events[from_offset:]:
        total = job(total, e)
    return total

print("v1 (live, buggy)    :", replay(v1, log))
print("v2 (replayed from 0):", replay(v2, log))
'''),
        dict(label='3 · Two codebases drift', hint='In Lambda the same metric is written twice. Here finance updated the batch rule to exclude test orders, but the stream code wasn\'t changed. Fix the stream function so both agree.',
             code='''events = [("O1", 120, False), ("T9", 500, True), ("O2", 250, False), ("T10", 300, True)]
#                     (order, amount, is_test_order)

def batch_revenue(evts):                  # updated last week
    return sum(a for o, a, test in evts if not test)

def stream_revenue(evts):                 # forgotten!
    return sum(a for o, a, test in evts)

print("Batch says :", batch_revenue(events))
print("Stream says:", stream_revenue(events))
print("Difference :", stream_revenue(events) - batch_revenue(events))
'''),
        dict(label='4 · Batch catches up', hint='When the nightly batch runs, its view covers more events and the speed layer drops what the batch now owns. Move the cut-off forward and watch where each event is counted.',
             code='''events = list(range(1, 11))               # 10 events, each worth 1
for cutoff in [4, 7, 10]:
    batch = sum(events[:cutoff])
    speed = sum(events[cutoff:])
    print(f"cutoff {cutoff:>2}: batch {batch:>2} + speed {speed:>2} = {batch + speed}")
'''),
        dict(label='5 · Size the log (advanced)', hint='Kappa needs the log to keep enough history to replay. How much storage do 90 days of order events need, and how long would a replay take? Change the retention to 365 days.',
             code='''events_per_day = 2_000_000
bytes_per_event = 400
retention_days = 90
replay_speed = 50_000                     # events per second when replaying

stored_gb = events_per_day * bytes_per_event * retention_days / 1024**3
replay_hours = events_per_day * retention_days / replay_speed / 3600
print(f"Log size for {retention_days} days: {stored_gb:,.0f} GB (x3 with replication)")
print(f"Full replay takes about {replay_hours:.1f} hours")
'''),
        dict(label='6 · Blue-green switch (advanced)', hint='Job v2 replays from offset 0 at 50,000 events/s while new events arrive at 300/s. When does it catch up with live? Try a slower replay speed.',
             code='''backlog = 30 * 24 * 3600 * 300            # 30 days of events at 300 per second
live_rate, replay_rate = 300, 50_000

lag, minutes = backlog, 0
while lag > 0:
    lag = lag - (replay_rate - live_rate) * 60
    minutes = minutes + 1
print(f"Backlog: {backlog:,} events")
print(f"v2 catches up after about {minutes} minutes; then switch readers to v2")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a real log file, replayed',
    intro='<p>This program writes an append-only log file (<code>orders.log</code>), one JSON event per line with an offset, just like a Kafka partition. It then shows <b>Kappa</b> (a buggy v1 job, then a fixed v2 replayed from offset 0) and <b>Lambda</b> (batch view up to offset 4 plus speed view after it). Save it as <code>replay_log.py</code>, run it, and open <code>orders.log</code> to see the events.</p>',
    items=[
        dict(title='Kappa replay and Lambda merge on one log', file='replay_log.py',
             cmd=open(os.path.join(HERE, 'replay_log.py')).read() + '\n# In a terminal:  python replay_log.py',
             output=open(os.path.join(HERE, 'replay_log.out')).read(),
             note='Recorded from a real run; your output will be identical. Both architectures give the same correct answer (₹410) from the same log. The speed view is negative because a ₹300 refund arrived after the batch run, a reminder that real-time views hold whatever happened recently, including corrections.'),
    ],
)

TRACE = dict(
    heading='A serving-layer query, one line at a time',
    intro='<p>The batch view was computed overnight; the speed layer adds today\'s events one by one. Watch <code>speed</code> change with each event while <code>batch</code> stays fixed, and the query merge them at the end.</p>',
    code='''batch = 510                       # computed at 02:00 from all raw events
today = [140, 60, -300]           # events since the batch run (a refund is negative)

speed = 0
for amount in today:
    speed = speed + amount
    print("live answer:", batch + speed)

print("final answer:", batch + speed)
''',
    notes={1: 'Batch view :: Exact up to last night. It will not change until the next batch run.',
           2: 'Recent events :: Only these are handled by the speed layer.',
           4: 'Speed view :: Starts at zero after every batch run.',
           (7, 3): 'Refund :: The live answer can go down: corrections are events too.'},
)

WORKED_INTRO = 'Four problems on merging views, catching up, code drift and replay planning. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Dashboard · serving layer', title='Combine yesterday\'s exact total with today\'s live total',
         problem='<p>The batch view says the season\'s revenue till last night is ₹18.40 crore. The speed layer has today\'s events: ₹1.12 crore so far, then two more updates of ₹0.80 crore and ₹0.39 crore. Print the dashboard number after each update.</p>',
         inp='batch 18.40 cr · today: 1.12, +0.80, +0.39 (cr)',
         approach=['Keep the batch view fixed.',
                   'Add each live update to the speed view.',
                   'Print batch + speed after every update.'],
         code='''batch_cr = 18.40
speed_cr = 1.12
print("dashboard:", round(batch_cr + speed_cr, 2), "cr")
for update in [0.80, 0.39]:
    speed_cr = speed_cr + update
    print("dashboard:", round(batch_cr + speed_cr, 2), "cr")
''', notes={1: 'Batch view :: Fixed until tonight\'s run.'},
         tryit='Add a refund of −0.05. The dashboard number drops: the speed layer reflects corrections too.'),
    dict(level='i', tag='Platform · batch catch-up', title='Move events from the speed view to the batch view',
         problem='<p>Events have offsets 0–9. Last night\'s batch covered offsets 0–5. Tonight\'s batch covers 0–9. Show which offsets each layer is responsible for, before and after.</p>',
         inp='offsets 0–9, cut-off 6 then 10',
         approach=['The batch layer owns offsets below the cut-off.',
                   'The speed layer owns offsets from the cut-off onwards.',
                   'Print both lists for each cut-off.'],
         code='''offsets = list(range(10))
for cutoff in [6, 10]:
    batch = [o for o in offsets if o < cutoff]
    speed = [o for o in offsets if o >= cutoff]
    print("cutoff", cutoff, "| batch:", batch, "| speed:", speed)
''', notes={2: 'Each run :: The cut-off moves forward every time the batch job finishes.'},
         tryit='Every event is counted exactly once, either in batch or in speed. What would go wrong if both counted offset 6?'),
    dict(level='i', tag='Lambda pitfall · consistency', title='Detect drift between batch and stream logic',
         problem='<p>The same day\'s events are processed by the batch code and by the stream code. Finance\'s rule says orders cancelled within 5 minutes are not sales. Find whether the two implementations disagree and by how much.</p>',
         inp='events with minutes-until-cancel (None = not cancelled)',
         approach=['Implement both functions as they exist in production.',
                   'Run both on the same events.',
                   'Report the difference, which should be zero.'],
         code='''events = [(120, None), (250, 3), (90, None), (300, 20), (60, 2)]

def batch_logic(evts):            # follows the new rule
    return sum(a for a, cancel in evts if cancel is None or cancel > 5)

def stream_logic(evts):           # still the old rule: every order counts
    return sum(a for a, cancel in evts)

b, s = batch_logic(events), stream_logic(events)
print("batch:", b, "| stream:", s, "| drift:", s - b)
''', notes={9: 'Compare :: Running both on the same data is a common automated check in Lambda systems.'},
         tryit='Update <code>stream_logic</code> to the new rule. A unified engine would let you write it once instead.'),
    dict(level='a', tag='Kappa · capacity planning', title='Can we replay 90 days before the morning meeting?',
         problem='<p>A rule change must be applied to 90 days of history. The log holds 3 million events per day. The replay job processes 80,000 events per second, and new events arrive at 40 per second. Will it catch up within 8 hours?</p>',
         inp='3,000,000/day × 90 days · replay 80,000/s · live 40/s · budget 8 h',
         approach=['Backlog = events per day × days.',
                   'The replay closes the gap at (replay speed − live speed) per second.',
                   'Compare the hours needed with the 8-hour budget.'],
         code='''backlog = 3_000_000 * 90
net_speed = 80_000 - 40
hours = backlog / net_speed / 3600
print(f"Backlog: {backlog:,} events")
print(f"Catch-up time: {hours:.2f} hours")
print("Fits in 8 hours?", hours <= 8)
''', notes={2: 'Net speed :: New events keep arriving during the replay, so subtract them.'},
         tryit='Increase the history to 365 days. Would you add more parallel consumers (Kafka partitions) or go back to a batch recompute?'),
]

QUIZ = [
    dict(q='Beginner: The three layers of the Lambda architecture are…', options=['Ingest, store, visualise', 'Batch, speed and serving', 'Bronze, silver and gold', 'Map, shuffle and reduce'], answer=1,
         why='Lambda = <b>batch layer</b> (accurate), <b>speed layer</b> (fresh) and <b>serving layer</b> (merges them).'),
    dict(q='Beginner: In Lambda, which layer gives the freshest (seconds-old) answer?', options=['Batch layer', 'Speed layer', 'Master dataset', 'Archive'], answer=1,
         why='The speed layer processes recent events in real time.'),
    dict(q='Beginner: What is the main idea of the Kappa architecture?', options=['Use only batch jobs', 'Use one stream-processing path and replay the log to reprocess', 'Store data only in a warehouse', 'Run two copies of every job'], answer=1,
         why='Kappa removes the batch layer: one streaming codebase, with the event log as the source of truth for replays.'),
    dict(q='Intermediate: How does a Lambda serving layer answer a query?', options=['It uses only the batch view', 'It uses only the speed view', 'It merges the batch view and the real-time view', 'It asks the user to wait for tomorrow'], answer=2,
         why='Query result = batch view (up to the last run) + real-time view (since then).'),
    dict(q='Intermediate: What happens to the speed layer\'s results for a period once the batch layer has processed it?', options=['They are kept forever', 'They are discarded; the batch view replaces them', 'They are added again', 'They are sent to the master dataset'], answer=1,
         why='Real-time views are temporary; the exact batch view supersedes them.'),
    dict(q='Intermediate: The biggest practical drawback of Lambda is…', options=['It cannot handle real-time data', 'The same business logic must be built and kept consistent in two systems', 'It needs no storage', 'It only works on one machine'], answer=1,
         why='Two codebases (batch and stream) for the same metrics must stay in sync; drift causes mismatched numbers.'),
    dict(q='Advanced: What must be true for Kappa-style reprocessing to work?', options=['The log must retain enough history to replay', 'There must be a nightly batch job', 'All events must be smaller than 1 KB', 'The warehouse must be deleted first'], answer=0,
         why='Replay needs the events: long retention (often with tiered storage) is a requirement of Kappa.'),
    dict(q='Advanced: Which reduces Lambda\'s duplicate-code problem without fully adopting Kappa?', options=['Writing more unit tests only', 'Unified engines that run the same code in batch and streaming modes (Flink, Spark Structured Streaming, Beam)', 'Turning off the speed layer at night', 'Using CSV files'], answer=1,
         why='Unified engines let one implementation serve both the batch recompute and the live stream.'),
]

REVISION = [
    '<b>Lambda</b> = batch layer (exact, hours old) + speed layer (fresh, approximate) + serving layer (merge).',
    'Query = <b>batch view + real-time view</b>; real-time views are discarded once batch catches up.',
    'Lambda drawback: <b>two codebases</b> for the same logic, which can drift apart.',
    '<b>Kappa</b> = append-only log + one stream job + serving store; reprocess by <b>replaying</b> the log.',
    'Kappa needs long <b>retention</b>, fast replay, exactly-once sinks; switch versions blue-green.',
    'Lambda: Nathan Marz (2011). Kappa: Jay Kreps (2014).',
    'Modern practice: unified engines and lakehouse tables blend both ideas. Choose per use case.',
]
FAQ = [
    ('Explain the Lambda architecture with a diagram.', 'Incoming data is sent to two paths. The batch layer appends it to an immutable master dataset and periodically recomputes batch views over all data (accurate but high-latency). The speed layer processes only recent data in real time to produce real-time views (low-latency, approximate). The serving layer stores both and answers queries by merging them. When the batch layer catches up, the corresponding real-time views are discarded.'),
    ('What is the Kappa architecture and how is it different from Lambda?', 'Kappa uses a single stream-processing path over an append-only, replayable log (such as Kafka with long retention). There is no separate batch layer: to fix bugs or compute new metrics, a new version of the stream job replays the log from the beginning into a new output, and readers switch to it once it catches up. This avoids maintaining two codebases, at the cost of relying on long retention and robust streaming.'),
    ('What are the advantages and disadvantages of Lambda?', 'Advantages: accurate results from full recomputation, low-latency views from the speed layer, and robustness, since batch recomputation corrects any errors. Disadvantages: duplicated logic in two systems, more operational complexity, and possible inconsistencies between batch and real-time results.'),
    ('When would you choose Kappa over Lambda?', 'When the processing logic can be expressed as stream jobs, the event log can retain enough history to replay, logic changes are frequent, and the team wants one codebase. Lambda (or a batch component) remains useful when recomputation needs heavy historical joins, very long history, or complex batch-only tools such as large model training.'),
    ('What is the role of the serving layer?', 'It stores precomputed batch views and real-time views in a database built for fast reads (for example Cassandra, HBase, Druid or a warehouse) and answers application and dashboard queries by combining them, so users get complete and up-to-date results with low latency.'),
]

PRACTICE_INTRO = 'Exercises on views, replays and planning, from easy to advanced, ending with two business decisions.'
PROBLEMS = [
    dict(level='easy', title='Merge two views', stmt='The batch view is 9,450 orders and the real-time view is 312 orders. Print the total the dashboard shows.', inp='9450 + 312',
         code='batch, speed = 9450, 312\nprint("Dashboard:", batch + speed)\n', explain='The serving layer\'s core operation: batch view + real-time view.'),
    dict(level='easy', title='Which layer answers?', stmt='For each requirement, print which Lambda layer provides it.', inp='“seconds-old count”, “exact last month”, “combined answer”',
         code='''needs = {"seconds-old count": "speed layer", "exact last month": "batch layer",
         "combined answer": "serving layer"}
for need, layer in needs.items():
    print(f"{need:18} -> {layer}")
''', explain='Fresh = speed, exact = batch, merged = serving.'),
    dict(level='easy', title='Log storage for retention', stmt='An app produces 5 lakh events a day of 500 bytes each. How many GB does a 30-day log need (one copy)?', inp='500000 × 500 B × 30',
         code='print(round(500_000 * 500 * 30 / 1024**3, 2), "GB")\n', explain='Retention size = events per day × size × days. Multiply by the replication factor for real storage.'),
    dict(level='medium', title='Speed view after the cut-off', stmt='Event times are given in hours. The batch ran at hour 24. Sum only the amounts the speed layer handles (time ≥ 24).', inp='(20,100), (23,50), (24,70), (26,30)',
         code='''events = [(20, 100), (23, 50), (24, 70), (26, 30)]
cutoff = 24
print("Speed view:", sum(a for t, a in events if t >= cutoff))
''', explain='Everything before the cut-off belongs to the batch view; counting it twice would be a bug.'),
    dict(level='medium', title='How wrong was the live number?', stmt='The live counter showed ₹2.31 crore; the batch result is ₹2.24 crore. Print the difference as a percentage of the batch result.', inp='2.31 vs 2.24',
         code='''live, exact = 2.31, 2.24
print(round((live - exact) / exact * 100, 1), "% higher than exact")
''', explain='Speed-layer results are useful for decisions but are not the final, audited number.'),
    dict(level='advanced', title='Replay with corrected logic', stmt='Replay the log with the corrected rule (refunds subtract) and compare with the buggy total (refunds add).', inp='sale 500, refund 200, sale 300, refund 100',
         code='''log = [(500, "sale"), (200, "refund"), (300, "sale"), (100, "refund")]
buggy = sum(a for a, k in log)
fixed = sum(-a if k == "refund" else a for a, k in log)
print("Buggy:", buggy, "| Fixed after replay:", fixed)
''', explain='Because the log keeps every event, the corrected logic can recompute history exactly.'),
    dict(level='advanced', title='When can we switch?', stmt='Job v2 starts 2 crore events behind live. It processes 40,000 events/s while new events arrive at 500/s. Print the minutes until it catches up.', inp='backlog 20,000,000; 40,000/s vs 500/s',
         code='''backlog = 20_000_000
minutes = backlog / (40_000 - 500) / 60
print(round(minutes, 1), "minutes until v2 catches up")
''', explain='Only when the new version has caught up do you switch readers to its output (blue-green).'),
    dict(level='business', title='The cost of two codebases', stmt='Each new metric takes 3 days to build in batch and 4 days in streaming. A unified engine needs 5 days once. For 12 metrics a year, print the engineer-days for Lambda and for unified.', inp='12 metrics',
         code='''metrics = 12
print("Lambda (two codebases):", metrics * (3 + 4), "days")
print("Unified engine        :", metrics * 5, "days")
''', explain='Duplicate implementation is Lambda\'s hidden running cost (numbers illustrative).'),
    dict(level='business', title='Does the replay fit the window?', stmt='A full replay takes 6.5 hours and must finish between 22:00 and 06:00. Print whether it fits and how much buffer remains.', inp='6.5 h vs 8 h window',
         code='''replay_h, window_h = 6.5, 8
print("Fits:", replay_h <= window_h, "| buffer:", window_h - replay_h, "hours")
''', explain='Replay time is a real constraint in Kappa designs; plan capacity so replays finish in time.'),
]

SCN_INTRO = 'Architecture questions asked in data engineering interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
