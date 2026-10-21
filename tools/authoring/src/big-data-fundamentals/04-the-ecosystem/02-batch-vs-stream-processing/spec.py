import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='02-batch-vs-stream-processing', n='4.2',
    module_label='Module 4 · The Ecosystem',
    title='Batch vs stream processing: now or later?',
    desc='Batch vs stream processing explained with live cricket scores, UPI fraud checks and food-delivery orders: latency, throughput, tumbling, sliding and session windows, event time, watermarks, late data and delivery guarantees. Beginner to Advanced, real-time animations, Python simulations and a live stream you can run on your PC.',
    og_desc='Live score or tomorrow\'s newspaper? Learn when to process data as a stream and when as a batch, with real-time animations and runnable Python.',
    minutes=28, level='Beginner → Advanced',
    lead='Your live score updates within a second of every ball; tomorrow\'s newspaper has the full scorecard. Both come from the same data, processed in two different ways. This lesson shows when to use <b>batch</b> and when to use <b>stream</b> processing, how windows turn an endless stream into answers, and how real systems deal with events that arrive late.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Live stream on your PC'],
)

RUN = dict(
    heading='The same orders, processed two ways',
    intro='<p>Six orders arrive during the day. The <b>stream</b> job updates its answer with every event; the <b>batch</b> job waits for the complete list and answers once. Compare when each answer is available. Then try windows, a fraud rule, late events and duplicates in the challenges.</p>',
    code='''orders = [  # (minute, kitchen, amount)
    (1, "K12", 120), (1, "K11", 90), (2, "K12", 250),
    (3, "K12", 180), (3, "K13", 60), (4, "K12", 140),
]

# STREAM: update the answer as each event arrives
def stream_job(events):
    total = 0
    for minute, kitchen, amount in events:
        total = total + amount
        print(f"[stream  @ minute {minute}] +{amount:>3} from {kitchen} -> running total Rs {total}")

# BATCH: wait until all data is collected, then process it in one go
def batch_job(all_orders):
    total = sum(amount for _, _, amount in all_orders)
    busiest = max(set(k for _, k, _ in all_orders),
                  key=lambda k: sum(a for _, kk, a in all_orders if kk == k))
    print(f"[batch   @ end of day] {len(all_orders)} orders, Rs {total}, busiest kitchen {busiest}")

stream_job(orders)
batch_job(orders)
''',
    anno=[
        ('for minute, kitchen, amount in events:', 'The stream job never sees “all” the data. It handles one event, updates its <b>state</b> (<code>total</code>) and moves on.'),
        ('print(f"[stream  @ minute {minute}] ...', 'An answer is available after <b>every</b> event: low latency.'),
        ('total = sum(amount for _, _, amount in all_orders)', 'The batch job has the complete, <b>bounded</b> data, so it can answer harder questions in one pass, like “which kitchen was busiest overall?”'),
    ],
    tasks=[
        dict(label='1 · Stream vs batch', hint='Press <b>Run</b>. Add an order at minute 5. The stream prints a new line at once; the batch answer only changes when you re-run the whole job.', code=None),
        dict(label='2 · Runs per over', hint='A <b>tumbling window</b> of 6 balls. Each ball is in exactly one over. Change the window to 3 balls (half-overs).',
             code='''balls = [6, 1, 1, 1, 0, 0,   1, "W", 2, 1, 2, 4,   1, 1, 1, 6, 0, 0]
WINDOW = 6

runs = 0
for i, b in enumerate(balls, 1):
    if b != "W":
        runs = runs + b
    if i % WINDOW == 0:                 # window closes: emit its result
        print("Over", i // WINDOW, "->", runs, "runs")
        runs = 0
'''),
        dict(label='3 · Fraud rule', hint='A <b>sliding window</b>: for every new payment, count payments in the previous 120 seconds. Change the rule to 3 payments and see when it fires.',
             code='''payments = [0, 25, 51, 70, 91, 115, 300, 320]   # seconds since 10:00:00
LIMIT, WINDOW = 4, 120

recent = []
for t in payments:
    recent = [p for p in recent if t - p < WINDOW] + [t]
    status = "BLOCK" if len(recent) > LIMIT else "ok"
    print(f"t={t:>3}s  payments in last 2 min: {len(recent)}  {status}")
'''),
        dict(label='4 · Sessions', hint='A <b>session window</b> ends after a gap of more than 30 minutes. How many visits did this shopper make? Change the gap to 60.',
             code='''clicks = [10, 12, 15, 21, 70, 74, 140, 141, 143]   # minutes after 9:00
GAP = 30

sessions, current = [], [clicks[0]]
for t in clicks[1:]:
    if t - current[-1] > GAP:
        sessions.append(current)
        current = [t]
    else:
        current.append(t)
sessions.append(current)
for i, s in enumerate(sessions, 1):
    print(f"Visit {i}: {len(s)} clicks, {s[-1] - s[0]} minutes long")
'''),
        dict(label='5 · Late events (advanced)', hint='Events arrive out of order. The watermark is the largest event time seen minus <code>ALLOWED</code>. An event older than the watermark is “too late”. Try <code>ALLOWED = 5</code>.',
             code='''# (event_time, arrival order) - minute 58 arrives after minute 62!
events = [55, 56, 59, 61, 58, 62, 50]
ALLOWED = 3                               # minutes we are willing to wait

max_seen = 0
for t in events:
    max_seen = max(max_seen, t)
    watermark = max_seen - ALLOWED
    verdict = "TOO LATE (side table)" if t < watermark else "counted"
    print(f"event at {t}  watermark {watermark}  -> {verdict}")
'''),
        dict(label='6 · Duplicates (advanced)', hint='With <b>at-least-once</b> delivery, a retry can deliver the same event twice. Keeping the ids already seen gives an <b>exactly-once</b> result. Remove the <code>if</code> check and compare totals.',
             code='''deliveries = [("T1", 120), ("T2", 90), ("T2", 90), ("T3", 250), ("T1", 120)]

seen, total = set(), 0
for txn, amount in deliveries:
    if txn in seen:
        print("duplicate", txn, "ignored")
        continue
    seen.add(txn)
    total = total + amount
print("Total:", total)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a live score stream in your terminal',
    intro='<p>This program generates a “live” ball every 0.3 seconds and processes it as a <b>stream</b>: the score updates immediately, and a 6-ball tumbling window closes at the end of every over. After the last ball it prints a <b>batch</b> summary computed from the complete data. Save it as <code>live_score.py</code> and watch it scroll.</p>',
    items=[
        dict(title='Watch a stream being processed', file='live_score.py',
             cmd=open(os.path.join(HERE, 'live_score.py')).read() + '\n# In a terminal:  python live_score.py',
             output=open(os.path.join(HERE, 'live_score.out')).read(),
             note='Recorded from a real run. The balls are the same every time (the random generator is seeded); the timings in the first column will differ slightly on your computer. Notice that each line appears 0.3 s after the previous one, as a real stream would, while the batch summary appears only at the very end.'),
    ],
)

TRACE = dict(
    heading='A tumbling window, one event at a time',
    intro='<p>Orders arrive with the minute they happened. The stream job keeps a running <code>total</code> for the current minute; when an event from a <b>new</b> minute arrives, the old window closes and its result is printed. Watch <code>window</code> and <code>total</code> in the frame.</p>',
    code='''events = [(1, 120), (1, 90), (2, 250), (3, 180), (3, 60)]
window, total = None, 0
for minute, amount in events:
    if window is not None and minute != window:
        print("minute", window, "->", total)
        total = 0
    window = minute
    total = total + amount
print("minute", window, "->", total)
''',
    notes={1: 'Stream :: Five order events, each with its minute and amount.',
           2: 'State :: The processor remembers only the current window and its running total.',
           (5, 1): 'Window closes :: An event from minute 2 arrived, so minute 1 is complete. Emit its result.',
           9: 'Stream ends :: Only in this demo; a real stream never ends, so the last window would close on a timer or watermark.'},
)

WORKED_INTRO = 'Four problems from first-week analyst to streaming engineer. Each runs live and is traced line by line.'
EXAMPLES = [
    dict(level='b', tag='Product team · design choice', title='Batch or stream? Decide from the deadline',
         problem='<p>For each use case, the business says how old the answer may be (in seconds) before it becomes useless. Classify each: under 60 seconds → stream; otherwise → batch.</p>',
         inp='fraud check 1 s · live score 2 s · salary 86400 s · monthly bill 604800 s · surge price 30 s · sales report 21600 s',
         approach=['Store each use case with its maximum acceptable age.',
                   'Loop over them and compare with 60 seconds.',
                   'Print the choice.'],
         code='''needs = {"fraud check": 1, "live score": 2, "salary": 86400,
         "monthly bill": 604800, "surge price": 30, "sales report": 21600}
for use_case, max_age in needs.items():
    choice = "STREAM" if max_age < 60 else "batch"
    print(f"{use_case:13} {choice}")
''', notes={1: 'Requirement :: Each value is “how many seconds old can the answer be?”'},
         tryit='Add “OTP delivery” (5 s) and “annual tax statement”. Where would you draw the line for a hospital monitor alert?'),
    dict(level='i', tag='Sports app · tumbling window', title='Runs per over from ball-by-ball events',
         problem='<p>A sports app receives one event per ball. Produce the runs in each over (a 6-ball tumbling window) and the over with the most runs.</p>',
         inp='12 balls: 6,1,1,1,0,0, 1,W,2,1,2,4',
         approach=['Walk through the balls, adding runs (a wicket adds 0).',
                   'Every 6th ball, the window closes: save the over\'s runs and reset.',
                   'Find the best over with <code>max</code>.'],
         code='''balls = [6, 1, 1, 1, 0, 0, 1, "W", 2, 1, 2, 4]
overs, runs = [], 0
for i, b in enumerate(balls, 1):
    runs = runs + (0 if b == "W" else b)
    if i % 6 == 0:
        overs.append(runs)
        runs = 0
print("Runs per over:", overs)
print("Best over:", overs.index(max(overs)) + 1)
''', notes={5: 'Window :: Every 6th ball closes the current over.'},
         tryit='Extras (wides) don\'t count as balls in cricket. Add a <code>"wd"</code> event worth 1 run that does not move the ball count.'),
    dict(level='i', tag='Bank · sliding window', title='Flag a card used too often',
         problem='<p>For each card payment, count how many payments the same card made in the last 60 seconds. Flag any payment where the count exceeds 3.</p>',
         inp='times (s): 0, 10, 20, 30, 45, 200',
         approach=['Keep a list of recent payment times for the card.',
                   'For each new payment, drop times older than 60 s, then add the new one.',
                   'Flag if the list is longer than 3.'],
         code='''times = [0, 10, 20, 30, 45, 200]
recent = []
for t in times:
    recent = [r for r in recent if t - r < 60]
    recent.append(t)
    flag = "FLAG" if len(recent) > 3 else "ok"
    print(t, len(recent), flag)
''', notes={4: 'Slide :: Old payments leave the window as time moves on.'},
         tryit='At 200 s the window is almost empty again. Change the limit to 2 and see which payments are flagged.'),
    dict(level='a', tag='Streaming engineer · late data', title='Count orders per 10-minute window with a watermark',
         problem='<p>Order events arrive out of order. Count orders per 10-minute window by <b>event time</b>, using a watermark of “largest event time seen minus 5 minutes”. Events behind the watermark go to a late list.</p>',
         inp='event times (minute): 1, 4, 12, 8, 15, 3, 22',
         approach=['Track the largest event time seen; the watermark is that minus 5.',
                   'If an event is older than the watermark, it is late: keep it aside.',
                   'Otherwise add it to its window: <code>(t // 10) * 10</code>.'],
         code='''events = [1, 4, 12, 8, 15, 3, 22]
counts, late, max_seen = {}, [], 0
for t in events:
    max_seen = max(max_seen, t)
    if t < max_seen - 5:
        late.append(t)
        continue
    w = (t // 10) * 10
    counts[w] = counts.get(w, 0) + 1
print("Windows:", counts)
print("Late:", late)
''', notes={5: 'Watermark :: Anything older than (largest seen − 5) is treated as too late.'},
         tryit='Event 8 arrived after 12 but within 5 minutes, so it was counted. Event 3 was too late. Change the allowed delay to 15 and compare.'),
]

QUIZ = [
    dict(q='Beginner: Which of these needs stream processing?', options=['Monthly salary calculation', 'Blocking a fraudulent card payment', 'Annual tax statement', 'Yesterday\'s sales report'], answer=1,
         why='A fraud decision is useless if it arrives after the money has left, so it must be made in real time.'),
    dict(q='Beginner: Batch processing works on data that is…', options=['Unbounded and arriving continuously', 'Bounded: a finite set collected over a period', 'Only from sensors', 'Always smaller than 1 GB'], answer=1,
         why='Batch jobs process a bounded dataset, such as yesterday\'s files, usually on a schedule.'),
    dict(q='Beginner: Latency means…', options=['How many events per second are processed', 'How long after an event its result is available', 'How much disk space is used', 'How many machines are in the cluster'], answer=1,
         why='Latency is delay. Throughput is events per second.'),
    dict(q='Intermediate: “Runs scored in each over” is which kind of window?', options=['Sliding', 'Session', 'Tumbling', 'Global'], answer=2,
         why='Overs are fixed-size, non-overlapping groups of 6 balls: a <b>tumbling</b> window.'),
    dict(q='Intermediate: “Number of payments by this card in the last 2 minutes, checked at every payment” is a…', options=['Tumbling window', 'Sliding window', 'Session window', 'Batch job'], answer=1,
         why='The window moves with time and overlaps previous windows: a <b>sliding</b> window.'),
    dict(q='Intermediate: Spark Structured Streaming by default processes data as…', options=['One event at a time with no batching', 'Small micro-batches every few seconds (or less)', 'One nightly batch', 'It cannot process streams'], answer=1,
         why='Spark Structured Streaming uses <b>micro-batches</b> by default; Flink processes event at a time.'),
    dict(q='Advanced: An order made at 18:58 reaches the system at 19:02. Its event time is…', options=['19:02', '18:58', 'The watermark', '00:00'], answer=1,
         why='Event time is when it happened (18:58); processing time is when it was handled (19:02).'),
    dict(q='Advanced: Which guarantee may count some events twice?', options=['At-most-once', 'At-least-once', 'Exactly-once', 'None of them'], answer=1,
         why='At-least-once retries until success, so a retry can deliver duplicates; results must be de-duplicated or idempotent.'),
]

REVISION = [
    '<b>Batch:</b> bounded data, scheduled, high latency, high throughput, simpler. <b>Stream:</b> unbounded, continuous, low latency, needs state.',
    'Decide by: <b>how old can the answer be before it is useless?</b>',
    'Windows: <b>tumbling</b> (fixed, no overlap) · <b>sliding</b> (overlapping, recent) · <b>session</b> (ends after a gap).',
    '<b>Event time</b> = when it happened; <b>processing time</b> = when it was handled. Group by event time.',
    '<b>Watermark</b> = how long to wait for late events; a trade-off between speed and completeness.',
    'Guarantees: at-most-once (loss), at-least-once (duplicates), exactly-once (neither).',
    'Tools: batch → Spark, Hive, dbt + Airflow · stream → Kafka + Flink, Kafka Streams, Spark Structured Streaming.',
]
FAQ = [
    ('Differentiate batch processing and stream processing.', 'Batch processes a bounded dataset collected over time, on a schedule, with high throughput and latency of minutes to hours (daily reports, billing, model training). Stream processing handles unbounded data continuously as events arrive, with latency of milliseconds to seconds, keeping state and using windows (fraud detection, live dashboards, alerts). Batch is simpler and cheaper; stream is faster but harder to build and operate.'),
    ('What are windows in stream processing? Explain their types.', 'Windows divide an endless stream into finite groups for calculation. Tumbling windows are fixed-size and non-overlapping (orders per minute). Sliding windows are fixed-size but overlap, moving forward in small steps (payments in the last 5 minutes, every 30 seconds). Session windows grow with activity and close after a gap of inactivity (a user\'s visit).'),
    ('What is the difference between event time and processing time?', 'Event time is when an event actually occurred, recorded at the source. Processing time is when the system processes it. Network delays and offline devices make them differ, so correct aggregations group by event time and use watermarks to handle late events.'),
    ('What is a watermark?', 'A watermark is the stream processor\'s estimate that all events up to a certain event time have arrived, usually the maximum event time seen minus an allowed delay. When the watermark passes the end of a window, the window is finalised; events arriving later are handled by an allowed-lateness policy.'),
    ('What is micro-batching?', 'Processing a stream as a series of very small batches, every few seconds or less, as Spark Structured Streaming does by default. It reuses batch machinery and gives good throughput with near-real-time latency; event-at-a-time engines like Flink can reach lower latency.'),
]

PRACTICE_INTRO = 'Window and latency exercises, from easy to advanced. The last two are business decisions about cost and service levels.'
PROBLEMS = [
    dict(level='easy', title='Classify by latency', stmt='Print “stream” if the required latency is under 10 seconds, else “batch”, for 2, 3600 and 0.5 seconds.', inp='[2, 3600, 0.5]',
         code='''for need in [2, 3600, 0.5]:
    print(need, "->", "stream" if need < 10 else "batch")
''', explain='The required latency decides the style, not the size of the data.'),
    dict(level='easy', title='Throughput', stmt='A stream processed 9,00,000 events in 5 minutes. Print events per second.', inp='900000 events, 300 s',
         code='print(900000 / 300, "events per second")\n', explain='Throughput = events ÷ seconds.'),
    dict(level='easy', title='Hourly batch size', stmt='An app produces 2,500 events per second. How many events does one hourly batch contain?', inp='2500 events/s',
         code='print(f"{2500 * 3600:,} events per hourly batch")\n', explain='Batch size grows with the interval; that is why batch jobs need many machines.'),
    dict(level='medium', title='10-minute tumbling windows', stmt='Given order minutes, count orders in each 10-minute window (0, 10, 20 …).', inp='[1, 3, 9, 12, 15, 27, 28, 29]',
         code='''minutes = [1, 3, 9, 12, 15, 27, 28, 29]
counts = {}
for m in minutes:
    w = (m // 10) * 10
    counts[w] = counts.get(w, 0) + 1
print(counts)
''', explain='<code>(m // 10) * 10</code> maps each minute to the start of its window.'),
    dict(level='medium', title='Moving average of 3 readings', stmt='For each temperature reading, print the average of the last 3 readings (a sliding window of size 3).', inp='[30, 32, 34, 40, 41]',
         code='''temps = [30, 32, 34, 40, 41]
for i in range(len(temps)):
    window = temps[max(0, i - 2):i + 1]
    print(temps[i], "-> avg of last 3:", round(sum(window) / len(window), 1))
''', explain='Each window overlaps the previous one: a sliding window.'),
    dict(level='advanced', title='Count sessions', stmt='Click times are given in minutes. A session ends after a gap of more than 20 minutes. Print the number of sessions.', inp='[0, 5, 8, 40, 42, 90]',
         code='''clicks = [0, 5, 8, 40, 42, 90]
sessions = 1
for prev, cur in zip(clicks, clicks[1:]):
    if cur - prev > 20:
        sessions = sessions + 1
print("Sessions:", sessions)
''', explain='Each gap larger than the limit starts a new session window.'),
    dict(level='advanced', title='At-least-once to exactly-once', stmt='The same event ids may be delivered more than once. Print the number of unique events and how many duplicates were dropped.', inp='[e1, e2, e2, e3, e1, e4]',
         code='''events = ["e1", "e2", "e2", "e3", "e1", "e4"]
unique = []
for e in events:
    if e not in unique:
        unique.append(e)
print("Unique:", len(unique), "| duplicates dropped:", len(events) - len(unique))
''', explain='De-duplicating by a unique id turns at-least-once delivery into exactly-once results.'),
    dict(level='business', title='Always-on stream vs nightly batch', stmt='A stream job needs 4 nodes running 24 hours a day; a nightly batch needs 20 nodes for 2 hours. A node costs Rs 30 per hour. Print the monthly (30-day) cost of each (illustrative).', inp='Rs 30/node-hour',
         code='''stream = 4 * 24 * 30 * 30
batch = 20 * 2 * 30 * 30
print("Stream: Rs", stream)
print("Batch : Rs", batch)
''', explain='Streams cost money every hour. Pay for real time only where it creates real value.'),
    dict(level='business', title='Did we meet the 1-second promise?', stmt='The bank promises a fraud decision within 1,000 ms. Given decision times, print the percentage that met the promise.', inp='[80, 95, 120, 1500, 70, 90, 2100, 85]',
         code='''times_ms = [80, 95, 120, 1500, 70, 90, 2100, 85]
ok = sum(1 for t in times_ms if t <= 1000)
print(round(ok / len(times_ms) * 100), "% within 1 second")
''', explain='Streaming systems are judged by latency targets (SLAs), usually measured as percentages like this.'),
]

SCN_INTRO = 'Situations where choosing batch or stream, or handling time correctly, is the real test. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
