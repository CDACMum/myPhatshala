import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='05-data-pipelines-and-orchestration', n='4.5',
    module_label='Module 4 · The Ecosystem',
    title='Data pipelines and orchestration (Apache Airflow basics)',
    desc='Data pipelines and orchestration explained: DAGs, tasks, operators and sensors, scheduling with cron, dependencies, retries and alerts, logical dates and data intervals, backfills, idempotent tasks, incremental loads, late data and quality gates, with Apache Airflow examples and a mini orchestrator you run on your PC.',
    og_desc='Why did Sunday\'s revenue show ₹0? Learn how Airflow-style orchestration, retries, backfills and idempotent tasks keep data pipelines trustworthy.',
    minutes=30, level='Beginner → Advanced',
    lead='Scripts that run on a timer will happily publish zeros when an earlier step fails. In this lesson you learn how <b>orchestration</b> with tools like <b>Apache Airflow</b> turns separate jobs into a reliable <b>pipeline</b>: a DAG of tasks with dependencies, retries, alerts and quality gates. You\'ll watch a 2 am failure recover by itself, backfill a week safely and handle data that arrives days late.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Mini orchestrator on your PC'],
)

RUN = dict(
    heading='A pipeline as a DAG, run in order',
    intro='<p>The pipeline is a dictionary of tasks and the tasks each depends on. The program finds a valid order (a topological sort), runs each task for one logical date, retries a flaky step, and stops downstream tasks if something fails for good. Then try the challenges: parallel branches, quality gates, idempotent publishing, backfills and incremental loads.</p>',
    code='''dag = {"extract": [], "validate": ["extract"], "transform": ["validate"], "publish": ["transform"]}
attempts_needed = {"extract": 2}            # extract fails once, then works
RETRIES = 3

def order(dag):
    done, out = set(), []
    while len(out) < len(dag):
        for t, deps in dag.items():
            if t not in done and all(d in done for d in deps):
                out.append(t); done.add(t)
    return out

logical_date = "2026-10-19"
for task in order(dag):
    for attempt in range(1, RETRIES + 1):
        if attempt >= attempts_needed.get(task, 1):
            print(f"{logical_date} {task:9} success (attempt {attempt})")
            break
        print(f"{logical_date} {task:9} failed, retrying")
    else:
        print(f"{task} failed for good: downstream skipped, alert sent")
        break
''',
    anno=[
        ('dag = {"extract": [], "validate": ["extract"], "transform": ["validate"], "publish": ["transform"]}', 'Each task lists its upstream tasks. That is all an orchestrator needs to know the order.'),
        ('if t not in done and all(d in done for d in deps):', 'A task is ready only when every task it depends on has finished.'),
        ('for attempt in range(1, RETRIES + 1):', 'Retries handle temporary failures such as timeouts without waking anyone up.'),
        ('    else:', 'The <code>for … else</code> runs only if no attempt succeeded: stop the pipeline instead of running on missing data.'),
    ],
    tasks=[
        dict(label='1 · Run the DAG', hint='Press <b>Run</b>. Then set <code>attempts_needed = {"extract": 5}</code> so retries are not enough. What happens to the downstream tasks?', code=None),
        dict(label='2 · Parallel branches', hint='Two tasks that both depend only on extract can run at the same time. Group tasks into “waves” that can run in parallel. Add a task <code>email</code> that depends on both reports.',
             code='''dag = {"extract": [], "clean_orders": ["extract"], "clean_riders": ["extract"],
       "report_orders": ["clean_orders"], "report_riders": ["clean_riders"]}
done, wave_no = set(), 1
while len(done) < len(dag):
    wave = [t for t, deps in dag.items() if t not in done and all(d in done for d in deps)]
    print(f"wave {wave_no}: {wave}")
    done.update(wave)
    wave_no += 1
'''),
        dict(label='3 · Quality gate', hint='Stop publishing if any check fails. Change one amount to negative, or make today\'s row count less than half of yesterday\'s.',
             code='''today = [120, 340, 90, 410, 75]
yesterday_count = 6
checks = {
    "not empty": len(today) > 0,
    "no negative amounts": all(a >= 0 for a in today),
    "volume not collapsed": len(today) >= yesterday_count * 0.5,
}
for name, ok in checks.items():
    print(f"{name:22} {'pass' if ok else 'FAIL'}")
print("-> publish" if all(checks.values()) else "-> stop, alert, show 'data delayed'")
'''),
        dict(label='4 · Append vs overwrite', hint='Run the same day twice with each publish style and compare the totals.',
             code='''append_table, overwrite_table = [], {}
def publish_append(day, revenue):
    append_table.append((day, revenue))
def publish_overwrite(day, revenue):
    overwrite_table[day] = revenue
for run in range(2):                       # a retry or manual re-run
    publish_append("2026-10-19", 850)
    publish_overwrite("2026-10-19", 850)
print("append total   :", sum(r for _, r in append_table))
print("overwrite total:", sum(overwrite_table.values()))
'''),
        dict(label='5 · Backfill (advanced)', hint='Generate one run per logical date for a date range, each processing only its own day. Change the range to the whole of October.',
             code='''import datetime
start, end = datetime.date(2026, 10, 13), datetime.date(2026, 10, 19)
day = start
while day <= end:
    print(f"run for logical date {day}: read date={day}, overwrite date={day}")
    day += datetime.timedelta(days=1)
'''),
        dict(label='6 · Incremental load (advanced)', hint='Load only rows changed since the last successful run (a high-water mark). Add a row updated at 10:45 and run again.',
             code='''source = [("O1", "10:05"), ("O2", "10:20"), ("O3", "10:31"), ("O4", "10:40")]
watermark = "10:20"                       # last value loaded successfully
new_rows = [r for r in source if r[1] > watermark]
print("rows to load:", new_rows)
if new_rows:
    watermark = max(r[1] for r in new_rows)
print("new watermark:", watermark)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a tiny orchestrator with retries and backfills',
    intro='<p>This program defines a four-task DAG, runs it in dependency order for a logical date, retries a flaky extract step, and publishes one JSON file per day into a <code>warehouse</code> folder. Then it backfills three days <b>twice</b> to prove that re-running is safe. Only the standard library is used. Save it as <code>mini_orchestrator.py</code> and run it.</p>',
    items=[
        dict(title='DAG order, retries, idempotent backfill', file='mini_orchestrator.py',
             cmd=open(os.path.join(HERE, 'mini_orchestrator.py')).read() + '\n# In a terminal:  python mini_orchestrator.py',
             output=open(os.path.join(HERE, 'mini_orchestrator.out')).read(),
             note='Recorded from a real run with Python 3.13; the random seed makes it repeatable. Open the <code>warehouse</code> folder after running: there is exactly one file per day, even though the backfill ran twice. To try real Airflow, install it with Docker using the official quick-start, or use a managed service, and put the DAG shown in the Definition section into its <code>dags</code> folder.'),
    ],
)

TRACE = dict(
    heading='Finding the run order, one line at a time',
    intro='<p>Three tasks are listed out of order. Watch the loop pick a task only when everything it depends on is already done.</p>',
    code='''dag = {"publish": ["transform"], "extract": [], "transform": ["extract"]}
done = []
while len(done) < len(dag):
    for task, deps in dag.items():
        if task not in done and all(d in done for d in deps):
            done.append(task)
print(done)
''',
    notes={1: 'DAG :: Written out of order on purpose.',
           5: 'Ready? :: A task can run only when all its upstream tasks are done.'},
)

WORKED_INTRO = 'Four pipeline problems, from ordering tasks to sizing a backfill. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Scheduling · cron', title='Read a cron schedule',
         problem='<p>Airflow schedules are often cron expressions with five fields: minute, hour, day of month, month, day of week. Explain three schedules in words.</p>',
         inp='0 1 * * * · 30 */4 * * * · 0 9 * * 1',
         approach=['Split each expression into its five fields.',
                   'Translate the minute and hour fields; <code>*</code> means every, <code>*/4</code> means every 4.',
                   'Day of week 1 means Monday.'],
         code='''def explain(expr):
    minute, hour, dom, month, dow = expr.split()
    when = f"minute {minute}"
    when += ", every 4 hours" if hour == "*/4" else f", hour {hour}"
    when += ", on Mondays" if dow == "1" else ", every day"
    return when
for e in ["0 1 * * *", "30 */4 * * *", "0 9 * * 1"]:
    print(f"{e:13} -> {explain(e)}")
''', notes={2: 'Fields :: Five space-separated parts, in a fixed order.'},
         tryit='Write the cron for “at 6:15 am on the 1st of every month” and add support for the day-of-month field.'),
    dict(level='i', tag='Pipeline design · dependencies', title='Which tasks can run in parallel?',
         problem='<p>A DAG has a common extract, two independent cleaning branches and a final report that needs both. Group tasks into waves that can run at the same time, and find the shortest total time if each task takes the given minutes.</p>',
         inp='extract 10, clean_orders 20, clean_riders 5, report 8 (minutes)',
         approach=['A task can start when all its upstream tasks are done.',
                   'Each wave takes as long as its slowest task.',
                   'Total time = sum of wave times.'],
         code='''dag = {"extract": [], "clean_orders": ["extract"], "clean_riders": ["extract"], "report": ["clean_orders", "clean_riders"]}
minutes = {"extract": 10, "clean_orders": 20, "clean_riders": 5, "report": 8}
done, total = set(), 0
while len(done) < len(dag):
    wave = [t for t, deps in dag.items() if t not in done and all(d in done for d in deps)]
    total += max(minutes[t] for t in wave)
    print("wave:", wave)
    done.update(wave)
print("shortest total:", total, "minutes (vs", sum(minutes.values()), "one by one)")
''', notes={5: 'Wave :: Every task whose dependencies are all finished.', 6: 'Time :: A wave lasts as long as its slowest task.'},
         tryit='clean_orders is the bottleneck. If you split it into two parallel 10-minute tasks, what is the new total?'),
    dict(level='i', tag='Reliability · retries', title='How long can retries delay a pipeline?',
         problem='<p>A task retries up to 4 times with exponential backoff starting at 2 minutes (2, 4, 8, 16). Each attempt takes 3 minutes. What is the worst-case time before it finally fails, and does it still meet a 2-hour window?</p>',
         inp='4 retries, backoff 2 min doubling, 3 min per attempt',
         approach=['There is one first attempt plus 4 retries: 5 attempts.',
                   'Add the waiting time between attempts: 2 + 4 + 8 + 16.',
                   'Compare the total with the time window.'],
         code='''retries, first_delay, attempt_min = 4, 2, 3
delays = [first_delay * 2 ** i for i in range(retries)]
worst = (retries + 1) * attempt_min + sum(delays)
print("delays between attempts:", delays)
print("worst case before failing:", worst, "minutes")
print("fits a 2-hour window" if worst <= 120 else "too slow for the window")
''', notes={2: 'Backoff :: Each wait doubles, giving the source more time to recover.'},
         tryit='Allow 6 retries. Is that still a good idea for a pipeline that must finish by 7 am?'),
    dict(level='a', tag='Operations · backfill', title='Plan a safe backfill',
         problem='<p>A bug affected 45 days. Each daily run takes 12 minutes, the cluster can run 6 days in parallel without hurting nightly jobs, and runs must finish before the 1 am nightly start, with 6 hours available. Plan the backfill.</p>',
         inp='45 days, 12 min per run, 6 parallel, 6 hours',
         approach=['Batches = days ÷ parallel runs, rounded up.',
                   'Time = batches × minutes per run.',
                   'If it doesn\'t fit, split across nights.'],
         code='''import math
days, per_run, parallel, window_min = 45, 12, 6, 6 * 60
batches = math.ceil(days / parallel)
needed = batches * per_run
nights = math.ceil(needed / window_min)
print("batches:", batches, "| minutes needed:", needed)
print("nights required:", nights)
''', notes={3: 'Batches :: Six logical dates run at the same time.'},
         tryit='The backfill must also rebuild a monthly summary that depends on all 45 days. Where in the plan does that run go?'),
]

QUIZ = [
    dict(q='What is the main thing an orchestrator does that a plain cron job doesn\'t?', options=['Runs Python code', 'Enforces dependencies between tasks, with retries, alerts and run history', 'Stores data', 'Compresses files'], answer=1,
         why='Cron starts jobs by the clock only; an orchestrator runs a task only after its upstream tasks succeed and manages failures.'),
    dict(q='In Apache Airflow, a pipeline is defined as a:', options=['Spreadsheet', 'DAG (directed acyclic graph) of tasks', 'Kafka topic', 'Database table'], answer=1,
         why='A DAG lists tasks and the one-way dependencies between them, with no loops.'),
    dict(q='What does the cron schedule 0 1 * * * mean?', options=['Every minute', 'At 1:00 every day', 'On the 1st of every month', 'Every hour'], answer=1,
         why='Minute 0, hour 1, every day of every month: 1:00 am daily.'),
    dict(q='A task can be re-run for the same date and always gives the same result. This property is called:', options=['Idempotency', 'Replication', 'Partitioning', 'Latency'], answer=0,
         why='Idempotent tasks (for example, overwriting a date partition) make retries and backfills safe.'),
    dict(q='Re-running a load step doubled a day\'s revenue. The most likely cause is:', options=['The scheduler is slow', 'The load appends rows instead of overwriting or merging', 'The DAG has a cycle', 'Too many retries'], answer=1,
         why='Appending adds the same rows again. Overwrite the partition or MERGE on a key.'),
    dict(q='What is a backfill?', options=['Deleting old data', 'Running a pipeline for past logical dates', 'Adding more workers', 'Filling null values'], answer=1,
         why='Backfills reprocess history, for example after a bug fix or a new column.'),
    dict(q='The Airflow run with logical date 19 October starts at 1 am on 20 October. Why?', options=['A bug in Airflow', 'A daily run starts after its data interval (19 October) is complete', 'Time zones are ignored', 'It was retried'], answer=1,
         why='The logical date marks the period of data processed; the run starts once that period has ended.'),
    dict(q='Which task type waits for a condition, such as a file arriving in S3?', options=['Operator', 'Sensor', 'Executor', 'Scheduler'], answer=1,
         why='A <b>sensor</b> waits until a condition is true before downstream tasks run.'),
]

REVISION = [
    '<b>Pipeline</b> = automated steps from source to destination. <b>Orchestration</b> = scheduling + dependencies + retries + alerts + history.',
    'Airflow: <b>DAG</b> of tasks; operators (do work), sensors (wait), scheduler (decides), executor (runs).',
    'Cron <code>0 1 * * *</code> = 1:00 daily. Each run has a <b>logical date</b> / data interval.',
    '<b>Idempotent</b> tasks: overwrite date partitions or MERGE; never blind appends.',
    '<b>Backfill</b> past dates safely only if tasks are idempotent and use the logical date, not now().',
    'Quality gates before publish; alerts and “data delayed” instead of wrong numbers.',
    'Incremental loads (watermarks), reprocessing windows for late data; Airflow orchestrates, Spark/SQL/dbt do the heavy work.',
]
FAQ = [
    ('What is a data pipeline?', 'A data pipeline is an automated sequence of steps that moves data from one or more sources to destinations, typically extracting, validating, transforming and loading it, so that it is available in a usable form (for example, a daily revenue table for dashboards). Pipelines can be batch (scheduled) or streaming (continuous).'),
    ('What is Apache Airflow and what are its main components?', 'Apache Airflow is an open-source platform for authoring, scheduling and monitoring workflows as DAGs written in Python. Its main components are the scheduler (creates runs and decides which tasks are ready), the executor and workers (run tasks), the metadata database (stores run and task state), the web server/UI (monitoring and manual actions), and DAG files containing tasks built from operators and sensors.'),
    ('What does idempotent mean in data pipelines and why is it important?', 'An idempotent task produces the same result no matter how many times it runs for the same input or logical date. It is important because tasks are retried after failures, re-run manually and backfilled; without idempotency these would duplicate or corrupt data. Common techniques are overwriting date partitions, MERGE/upsert on keys and deduplication.'),
    ('What is the difference between scheduling and orchestration?', 'Scheduling only starts jobs at given times. Orchestration also manages dependencies between tasks, passes parameters such as logical dates, retries failures, enforces timeouts and SLAs, alerts on problems, records history and supports backfills across many systems.'),
    ('How do you handle late-arriving data in batch pipelines?', 'Process data by event date into date partitions, and have each run reprocess a window of recent days (for example the last 3 days) using idempotent overwrites or MERGE, so late records are included. Use sensors or completeness markers to wait for sources, and monitor how late data typically arrives to choose the window.'),
]

PRACTICE_INTRO = 'Pipeline and orchestration exercises. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Upstream tasks', stmt='Print the upstream tasks of “report”.', inp='DAG of 4 tasks',
         code='''dag = {"extract": [], "clean": ["extract"], "enrich": ["extract"], "report": ["clean", "enrich"]}
print(dag["report"])
''', explain='The report waits for both branches.'),
    dict(level='easy', title='Partition path for a date', stmt='Build the output path for logical date 2026-10-19.', inp='2026-10-19',
         code='''ds = "2026-10-19"
print(f"s3://lake/gold/revenue/date={ds}/")
''', explain='Every run writes only its own date partition.'),
    dict(level='easy', title='Runs per year', stmt='How many runs does a DAG scheduled every 4 hours create in a year?', inp='every 4 hours',
         code='''print(24 // 4 * 365)
''', explain='6 runs a day for 365 days.'),
    dict(level='medium', title='Failed tasks and their victims', stmt='If “clean” fails, print every task that can\'t run (all its downstream tasks).', inp='DAG of 5 tasks',
         code='''dag = {"extract": [], "clean": ["extract"], "enrich": ["clean"], "report": ["enrich"], "audit": ["extract"]}
failed = {"clean"}
changed = True
while changed:
    changed = False
    for t, deps in dag.items():
        if t not in failed and any(d in failed for d in deps):
            failed.add(t); changed = True
print(sorted(failed - {"clean"}))
''', explain='Failure spreads down the DAG; “audit” still runs because it doesn\'t depend on “clean”.'),
    dict(level='medium', title='Watermark load', stmt='Load rows with id greater than the last loaded id (42) and print the new watermark.', inp='ids [40, 41, 43, 44, 47]',
         code='''ids = [40, 41, 43, 44, 47]
last = 42
new = [i for i in ids if i > last]
print("load:", new, "| new watermark:", max(new))
''', explain='Incremental loads read only new data, which keeps nightly runs short.'),
    dict(level='advanced', title='Detect a DAG cycle', stmt='A DAG must have no cycles. Print whether the graph has one.', inp='a → b → c → a',
         code='''graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
def has_cycle(g):
    visiting, done = set(), set()
    def visit(n):
        if n in visiting:
            return True
        if n in done:
            return False
        visiting.add(n)
        found = any(visit(m) for m in g[n])
        visiting.discard(n); done.add(n)
        return found
    return any(visit(n) for n in g)
print("cycle!" if has_cycle(graph) else "no cycle")
''', explain='Airflow refuses DAGs with cycles, because no valid order exists.'),
    dict(level='advanced', title='Reprocessing window', stmt='Each daily run reprocesses the last 3 days. For run date 2026-10-19, print the dates it overwrites.', inp='2026-10-19, window 3',
         code='''import datetime
run = datetime.date(2026, 10, 19)
print([str(run - datetime.timedelta(days=d)) for d in range(3)])
''', explain='Late data from the previous two days is picked up safely because each day is overwritten.'),
    dict(level='business', title='Meeting the 8 am SLA', stmt='The pipeline starts at 1:00. Tasks take 25, 40, 70 and 15 minutes in sequence. Worst case, extract also needs 2 retries of 25 minutes each with 10-minute waits. Does it finish by 8:00?', inp='25, 40, 70, 15 min',
         code='''normal = 25 + 40 + 70 + 15
worst = normal + 2 * (25 + 10)
for name, m in [("normal", normal), ("worst", worst)]:
    end = 60 + m          # minutes after midnight
    print(f"{name}: done at {end // 60}:{end % 60:02d}", "OK" if end <= 8 * 60 else "LATE")
''', explain='SLA planning uses the worst case, including retries.'),
    dict(level='business', title='Cost of a wrong dashboard', stmt='A wrong revenue number leads to 3 hours of investigation by 5 people at Rs 1,500 per hour each, about twice a month. A quality-gate project costs Rs 1.2 lakh once. How many months to pay back?', inp='5 × 3 h × Rs 1,500 × 2 per month',
         code='''monthly_cost = 5 * 3 * 1500 * 2
print("cost per month:", monthly_cost)
print("payback months:", round(1_20_000 / monthly_cost, 1))
''', explain='Quality gates are cheap compared with the cost of decisions made on wrong data.'),
]

SCN_INTRO = 'Pipeline and orchestration questions from real teams and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
