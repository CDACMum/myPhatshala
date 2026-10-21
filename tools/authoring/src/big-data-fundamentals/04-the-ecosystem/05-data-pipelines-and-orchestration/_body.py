import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = ''
tasks = [('extract', 'blue'), ('validate', 'violet'), ('transform', 'acc'), ('publish', 'green'), ('dashboard', 'green')]
for k, (n, tone) in enumerate(tasks):
    x = 14 + k * 124
    sc += label_box(x, 52, 100, 46, [n, ['1:00 am', '1:20 am', '1:25 am', '2:10 am', '9:00 am'][k]], tone, 9.6)
    if k < 4:
        sc += arrow(x + 102, 75, x + 122, 75, 'ink3', 2)
sc += t(320, 30, 'One DAG: each task runs only after the one before it succeeds', 10, 'acc', bold=True)
sc += t(320, 124, 'retries · alerts · backfills · one run per day', 9, 'ink2')
scene_svg = scene('A pipeline of five tasks, extract, validate, transform, publish and dashboard, run in order every night.', sc,
                  'Five scripts on a timer are not a pipeline. <tspan font-weight="700" class="s-acc">Dependencies, retries and alerts</tspan> make it one.')

story = f'''  <div class="story">
    <p class="narration">Monday, 9 am. TiffinGo’s city managers open the revenue dashboard: Sunday shows ₹0. Kabir’s nightly scripts ran on a timer, as always: extract at 1:00, transform at 1:30, publish at 2:00. But on Sunday the extract hit a timeout and failed. The transform ran anyway on empty input, and the publish step proudly wrote zeros.</p>

{scene_svg}

K> Sir, every script “succeeded” except the first one. The timer started each one on time, but nobody told the transform that its input was missing.
A> That’s the difference between <b>scheduling</b> and <b>orchestration</b>, Kabir. A timer only knows the clock. An orchestrator knows that “transform” depends on “extract”, waits for it, retries it if it fails, and alerts a human instead of publishing nonsense.
R> Is that what Airflow does? It’s in almost every data engineering job post.
A> Yes. In Apache Airflow you describe the pipeline as a <b>DAG</b>, a graph of tasks with arrows for dependencies, and Airflow runs it on a schedule, once per day of data, keeping a history of every run.
K> And Sunday’s zeros? Can I fix them?
A> With a <b>backfill</b>: re-run the pipeline for Sunday after fixing things. If your tasks are <b>idempotent</b>, running them again gives the same correct result instead of duplicates. Today you’ll see retries rescue a 2 am failure, backfill a week safely, and learn why Airflow cares about a run’s <i>logical date</i> more than the clock.
  </div>'''

# ---------------------------------------------------------------- definition
airflow_code = '''from datetime import datetime, timedelta
from airflow.sdk import dag, task      # Airflow 2.x: from airflow.decorators import dag, task

@dag(schedule="0 1 * * *",                         # every day at 1:00 am
     start_date=datetime(2026, 10, 1),
     catchup=False,
     default_args={"retries": 3, "retry_delay": timedelta(minutes=5)})
def daily_orders():

    @task
    def extract(ds=None):                           # ds = the logical date, e.g. "2026-10-19"
        return f"s3://lake/bronze/orders/date={ds}/"

    @task
    def validate(path):
        ...                                         # row counts, nulls, negative amounts
        return path

    @task
    def transform(path):
        ...                                         # submit a Spark job: bronze -> silver -> gold

    transform(validate(extract()))

daily_orders()'''
lv = '''
LEVELS> Pipelines and orchestration at three levels
L1> A recipe, a cook and a kitchen manager
      <ul>
        <li>A <b>pipeline</b> is a recipe: steps in order. Buy vegetables → wash → chop → cook → serve.</li>
        <li><b>Dependencies:</b> you can’t chop before the vegetables arrive. In data, you can’t transform before you extract.</li>
        <li>A timer (cron) is an alarm that says “start chopping at 7:30”, even if the vegetables never came.</li>
        <li>An <b>orchestrator</b> (Airflow) is a kitchen manager: it starts each step only when the previous one is done, tries again if the shop was closed, and tells the owner if dinner will be late, instead of serving an empty plate.</li>
      </ul>
L2> Airflow building blocks
      <ul>
        <li><b>DAG</b>: the pipeline as a directed acyclic graph of tasks, written in Python, with a schedule.</li>
        <li><b>Task / operator</b>: one step (run SQL, call an API, submit a Spark job, run Python). <b>Sensors</b> wait for something, such as a file landing in S3.</li>
        <li><b>Scheduler and executor</b>: the scheduler decides which tasks are ready; the executor runs them on workers.</li>
        <li><b>Logical date (data interval)</b>: each run processes one period of data, for example 19 October, even if it actually runs at 1 am on 20 October or a week later during a backfill.</li>
        <li><b>Retries, timeouts and alerts</b> are settings, not code you write each time.</li>
        <li><b>Airflow orchestrates; it doesn’t crunch:</b> heavy work runs in Spark, a warehouse or dbt; Airflow tells them when to run and checks the result.</li>
        <li>Similar tools: Dagster, Prefect, Azure Data Factory, AWS Step Functions, and managed Airflow (Amazon MWAA, Google Cloud Composer, Astronomer).</li>
      </ul>
L3> Idempotency, backfills and reliability
      <ul>
        <li><b>Idempotent tasks:</b> running a task twice for the same logical date gives the same result. Write by <b>overwriting the date partition</b> (or MERGE on keys), never by blind appends.</li>
        <li><b>Backfill:</b> re-run past logical dates after a bug fix or a new column. Only possible cleanly if tasks are idempotent and parameterised by date, not by “now”.</li>
        <li><b>Incremental loads:</b> process only new or changed data (by date partition or a watermark column such as <code>updated_at</code>) instead of everything every night.</li>
        <li><b>Late data:</b> events can arrive days late. Common fix: each run also reprocesses the last N days, which is safe because tasks are idempotent.</li>
        <li><b>Quality gates:</b> row-count, null and range checks between tasks stop bad data from being published (Great Expectations, dbt tests, Soda).</li>
        <li><b>Operations:</b> SLAs and alerts for late pipelines, lineage to see what depends on what, and keeping DAG files light so the scheduler stays fast.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>data pipeline</b> is a sequence of automated steps that moves data from sources to destinations, transforming and validating it on the way (for example extract → validate → transform → load). <b>Orchestration</b> is the automated coordination of those steps: scheduling runs, enforcing <b>dependencies</b>, passing parameters such as the logical date, handling <b>retries</b> and timeouts, alerting on failure and recording run history. In <b>Apache Airflow</b>, a pipeline is defined in Python as a <b>DAG</b> (directed acyclic graph) of tasks.',
    'A pipeline is a chain of jobs that turns raw data into something useful, like yesterday’s revenue table. An orchestrator such as Airflow runs the chain in the right order, waits when a step isn’t ready, retries steps that fail, and alerts people when something is really wrong.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('DAG', 'Directed acyclic graph: tasks joined by one-way arrows, with no loops.'),
    ('Task / operator', 'One step in a DAG; an operator is a template for a kind of step (Python, SQL, Spark, Bash).'),
    ('Sensor', 'A task that waits for a condition, such as a file arriving or another DAG finishing.'),
    ('Schedule', 'When runs are created, often written as cron: <code>0 1 * * *</code> = 1:00 every day.'),
    ('Logical date', 'The period of data a run is responsible for, independent of when it actually runs.'),
    ('Backfill', 'Running a pipeline for past logical dates.'),
    ('Idempotent', 'Gives the same result however many times it is run for the same input.'),
    ('Incremental load', 'Processing only new or changed data since the last run.'),
]) + '''

  <h3>An Airflow DAG (example)</h3>
  <p>This is what the daily orders pipeline looks like in Airflow 3 using the TaskFlow style. It is shown for reading; it needs an Airflow installation to run.</p>
  ''' + code('python', 'dags/daily_orders.py', airflow_code) + lv + '''
EXAM> Define a data pipeline and orchestration, draw a small DAG (extract → validate → transform → load), and explain <b>scheduling, dependencies, retries, backfill and idempotency</b>. Name Apache Airflow with its parts: DAG, operator, sensor, scheduler, executor.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Batch ETL / ELT pipelines', 'Run on a schedule (hourly, nightly) over a period of data: extract from sources, load to the lake or warehouse, transform with Spark, SQL or dbt.', 'Scheduled'),
    ('Streaming pipelines', 'Run continuously: Kafka → stream processor → sinks. Still need orchestration for deployments, backfills and checks.', 'Always on'),
    ('Event-triggered pipelines', 'Start when something happens: a file lands, an upstream DAG finishes, an API is called.', 'On demand'),
    ('ML pipelines', 'Prepare features, train, evaluate and deploy models on a schedule or when data drifts.', 'Train + serve'),
]) + '''

  <h3>Cron vs an orchestrator</h3>
''' + table(['', 'Cron / timer scripts', 'Orchestrator (Airflow, Dagster…)'], [
    ['<b>Dependencies</b>', 'None: each script starts by the clock', 'Task waits for upstream tasks to succeed'],
    ['<b>Failures</b>', 'Silent unless you build alerts', 'Retries, timeouts, alerts, marked failed in the UI'],
    ['<b>Backfills</b>', 'Manual, error-prone', 'Built in: run past logical dates'],
    ['<b>History</b>', 'Log files, if any', 'Every run, task, attempt and duration recorded'],
    ['<b>Parameters</b>', 'Usually “today”', 'Logical date passed to every task'],
    ['<b>Best for</b>', 'One small independent job', 'Multi-step pipelines across systems'],
]) + '''
TIP> Write every task as a function of the logical date: “process orders for <code>{ds}</code> and overwrite <code>date={ds}</code>”. That one habit makes retries, re-runs and backfills safe, and it is the most common thing interviewers check in pipeline design questions.'''

# ---------------------------------------------------------------- steps
c1 = '''dag = {"extract": [], "validate": ["extract"], "transform": ["validate"],
       "publish": ["transform"], "email_report": ["publish"]}
done, order = set(), []
while len(order) < len(dag):
    for task, deps in dag.items():
        if task not in done and all(d in done for d in deps):
            order.append(task); done.add(task)
print(" -> ".join(order))'''
c2 = '''import datetime
logical = datetime.date(2026, 10, 19)
path = f"s3://lake/bronze/orders/date={logical}/"
print("this run reads and writes only:", path)'''
c3 = '''rows = [120, 340, -90, 410]
checks = {"has rows": len(rows) > 0, "no negative amounts": all(r >= 0 for r in rows)}
print(checks, "-> PUBLISH" if all(checks.values()) else "-> STOP and alert")'''
c4 = '''partitions = {}
def publish(day, revenue):
    partitions[day] = revenue          # overwrite the day’s partition
publish("2026-10-19", 850); publish("2026-10-19", 850)   # re-run
print(partitions, "total:", sum(partitions.values()))'''
steps = stepper([
    ('Draw the DAG',
     code('python', 'dag_order.py', c1, run_code(c1)),
     'Each task lists what it depends on; the orchestrator works out a valid order (a topological sort) and runs independent tasks in parallel when it can.'),
    ('Parameterise by logical date',
     code('python', 'logical_date.py', c2, run_code(c2)),
     'The 19 October run reads and writes only 19 October’s partition, whether it runs at 1 am on the 20th or during a backfill next month.'),
    ('Extract with retries',
     '<p>The source API sometimes times out at night. The extract task is set to <code>retries=3</code> with a 5-minute delay (often growing each time: exponential backoff).</p>',
     'Most night-time failures are temporary: a busy API, a network blip, a restarting database. Retries turn them into short delays instead of morning emergencies.'),
    ('Validate before publishing',
     code('python', 'quality_gate.py', c3, run_code(c3)),
     'A quality gate between transform and publish stops impossible data (a negative amount, zero rows, a sudden 90% drop) and alerts someone. Publishing nothing is better than publishing wrong numbers.'),
    ('Publish idempotently',
     code('python', 'idempotent.py', c4, run_code(c4)),
     'Overwriting the date partition means a retry or a re-run produces the same result. With appends, every re-run would add the day’s revenue again.'),
    ('Monitor, alert, backfill',
     '<p>Airflow records every run. If Sunday failed, an alert goes out, the dashboard shows “data delayed”, and once fixed, the team clears and re-runs Sunday: a one-day backfill.</p>',
     'Good pipelines are judged on the bad days: how fast failures are noticed, how clearly they are reported and how safely they are repaired.'),
])

# ---------------------------------------------------------------- two-view animation
def laptop(title, inner):
    return ('<rect x="40" y="20" width="280" height="168" rx="10" class="s-board"/><rect x="50" y="32" width="260" height="144" rx="4" class="s-card2"/><path d="M24 198h312l-12 14H36z" style="fill:#2B3A34"/>' + t(180, 48, title, 9.4, bold=True) + inner)
def dash(sun, note, tone='ink'):
    o = ''.join(fill(70 + k * 34, 150 - h, 22, h, 'acc') for k, h in enumerate([50, 62, 58, 70, 66, 80]))
    o += (fill(70 + 6 * 34, 150 - sun, 22, sun, 'green') if sun else '') + t(81 + 6 * 34, 162, 'Sun', 7.6, 'ink3')
    return o + t(180, 70, note, 9, tone, bold=True)
see = [
    laptop('Revenue dashboard', dash(0, 'Sunday: updating overnight…', 'ink2')),
    laptop('Revenue dashboard', dash(0, 'Sunday: updating overnight…', 'ink2')),
    laptop('Revenue dashboard', dash(0, 'Sunday: updating overnight…', 'ink2')),
    laptop('Revenue dashboard', dash(0, 'Sunday: updating overnight…', 'ink2')),
    laptop('Revenue dashboard', dash(84, 'Sunday: ₹38.4 lakh', 'green')),
    laptop('Revenue dashboard', dash(84, 'Fresh at 9:00 am · checks passed', 'green')),
]
def dag_view(states, clock, note):
    names = ['extract', 'validate', 'transform', 'publish']
    o = t(180, 22, clock, 10, bold=True, mono=True)
    for k, (n, st) in enumerate(zip(names, states)):
        x = 10 + k * 88
        tone = {'wait': 'card', 'run': 'blue', 'ok': 'green', 'fail': 'red', 'retry': 'amber'}[st]
        lab = {'wait': 'waiting', 'run': 'running', 'ok': 'success', 'fail': 'failed', 'retry': 'retry 2/3'}[st]
        o += label_box(x, 44, 80, 46, [n, lab], tone, 9)
        if k < 3:
            o += arrow(x + 81, 67, x + 87, 67, 'ink3', 1.6)
    return o + t(180, 120, note, 9, 'ink2')
behind = [
    dag_view(['run', 'wait', 'wait', 'wait'], '01:00 · scheduler starts run for 2026-10-19', 'Logical date = Sunday. Extract starts; the rest wait.'),
    dag_view(['fail', 'wait', 'wait', 'wait'], '01:04 · extract fails: API timeout', 'Downstream tasks do NOT start on missing input.'),
    dag_view(['retry', 'wait', 'wait', 'wait'], '01:09 · automatic retry after 5 min', 'The source is back; attempt 2 succeeds.'),
    dag_view(['ok', 'ok', 'run', 'wait'], '01:25 · validate passed, transform running', 'Row counts and amounts checked; Spark job submitted.'),
    dag_view(['ok', 'ok', 'ok', 'ok'], '02:10 · publish overwrote date=2026-10-19', 'Idempotent: a re-run would give the same table.'),
    dag_view(['ok', 'ok', 'ok', 'ok'], '09:00 · run marked success', 'History, durations and logs saved for every task.'),
]
see_caps = ['Sunday night: the dashboard shows the week, with Sunday “updating overnight”.',
            'Nothing visible changes for the managers while the pipeline works.',
            'Still waiting, as expected at this hour.',
            'Still updating.',
            'By morning Sunday’s revenue appears: ₹38.4 lakh.',
            'At 9 am the managers see fresh numbers, with a note that the quality checks passed.']
behind_caps = ['At 1:00 the scheduler creates the run for logical date 19 October (Sunday). Extract starts; the other tasks wait for it.',
               'Extract fails with an API timeout. Unlike Kabir’s timer scripts, the orchestrator does not start validate or transform on missing data.',
               'After a 5-minute retry delay, extract runs again and succeeds.',
               'Validate checks row counts, nulls and amounts; transform submits the Spark job.',
               'Publish overwrites the 19 October partition, so any re-run gives the same result.',
               'The run is marked successful, with every attempt, duration and log stored for later. (Times are illustrative.)']
two = anim_two('A night in Airflow', 'What the managers see, and what the orchestrator does', 'A revenue dashboard waiting for Sunday’s numbers and then showing them',
               'An Airflow DAG run with a failed extract, an automatic retry and successful downstream tasks', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: hard failure, alerts
def mini(states):
    names = ['extract', 'validate', 'transform', 'publish']
    o = ''
    for k, (n, st) in enumerate(zip(names, states)):
        x = 10 + k * 88
        tone = {'wait': 'card', 'ok': 'green', 'fail': 'red', 'skip': 'card', 'retry': 'amber'}[st]
        lab = {'wait': 'waiting', 'ok': 'success', 'fail': 'failed', 'skip': 'upstream failed', 'retry': 'retrying'}[st]
        o += label_box(x, 36, 80, 44, [n, lab], tone, 8.8)
    return o
fr1 = [
    mini(['retry', 'wait', 'wait', 'wait']) + t(180, 22, 'Diwali night: source database under heavy load', 9.4, 'red', bold=True) + cap('Extract fails, retries at 5, 10 and 20 minutes', '(exponential backoff).', 'amber', y=100, h=44),
    mini(['fail', 'skip', 'skip', 'skip']) + t(180, 22, 'All retries used: extract FAILED', 9.4, 'red', bold=True) + cap('Downstream tasks are marked “upstream failed”.', 'Nothing wrong is published.', 'red', y=100, h=44),
    mini(['fail', 'skip', 'skip', 'skip']) + label_box(60, 96, 240, 52, ['#data-alerts · on-call paged', 'daily_orders · extract failed · 02:41'], 'red', 9) + cap('An alert reaches the on-call engineer with a link to logs.', '', 'amber', y=160, h=34),
    mini(['fail', 'skip', 'skip', 'skip']) + label_box(60, 96, 240, 52, ['Dashboard banner', '“Sunday data delayed, ETA 11 am”'], 'blue', 9) + cap('Managers see “delayed”, not “₹0”. Trust is kept.', '', 'blue', y=160, h=34),
    mini(['ok', 'ok', 'ok', 'ok']) + t(180, 22, '10:20 · source fixed, task cleared and re-run', 9.4, 'green', bold=True) + cap('The engineer clears the failed task; it and everything', 'downstream re-run for Sunday. Done by 11.', 'green', y=100, h=44),
]
s1 = anim_one('Real-time scenario 1', 'A failure that retries can’t fix',
              'Retries fix most night-time hiccups. But on Diwali night the source database is overloaded for hours. Watch how a well-built pipeline fails safely and recovers.',
              'Failing safely', 'A DAG whose extract task fails after retries, with alerts, a dashboard banner and a re-run', fr1,
              ['The extract task fails and retries with growing delays (5, 10, 20 minutes), giving the busy source time to recover.',
               'After the last retry it is marked <b>failed</b>, and every downstream task is marked “upstream failed” instead of running on missing data.',
               'An alert with a link to the logs pages the on-call engineer.',
               'The dashboard shows “Sunday data delayed” instead of a wrong ₹0, so managers don’t make decisions on bad numbers.',
               'When the source is healthy, the engineer clears the failed task. It and all downstream tasks re-run for Sunday’s logical date, and the numbers are published.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: backfill append vs overwrite
days = ['10-13', '10-14', '10-15', '10-16', '10-17', '10-18', '10-19']
def week(vals, tone='green', label=''):
    o = t(14, 22, label, 9.2, 'ink2', anchor='start')
    for k, (d, v) in enumerate(zip(days, vals)):
        x = 14 + k * 48
        h = round(v / 2)
        o += fill(x, 140 - h, 36, h, tone if not isinstance(tone, list) else tone[k], rx=3) + t(x + 18, 152, d, 7.4, 'ink3') + t(x + 18, 134 - h, str(v), 7.6, 'ink', bold=True)
    return o
good = [38, 41, 39, 44, 42, 47, 51]
buggy = [30, 33, 31, 35, 34, 38, 41]
fr2 = [
    week(buggy, 'red', 'Revenue (₹ lakh) published last week, with a currency-conversion bug') + cap('A bug under-counted wallet payments for 7 days.', 'The fix is merged. Now repair the past.', 'red', y=166, h=44),
    week(good, 'blue', 'Backfill: re-run the DAG for logical dates 10-13 … 10-19') + cap('Airflow runs the fixed pipeline once per logical date,', 'each reading and writing only its own day.', 'blue', y=166, h=44),
    week([b + g for b, g in zip(buggy, good)], 'red', 'If publish APPENDED rows…') + cap('Old wrong rows + new right rows: every day doubled.', 'Totals are now worse than before.', 'red', y=166, h=44),
    week(good, 'green', 'Publish OVERWRITES each date partition') + cap('Each day is replaced by its corrected value.', 'Re-running again changes nothing: idempotent.', 'green', y=166, h=44),
    week(good, 'green', 'Downstream tables re-run automatically') + cap('Weekly and monthly summaries that depend on these', 'days are cleared and re-run too, in dependency order.', 'green', y=166, h=44),
]
s2 = anim_one('Real-time scenario 2', 'Backfilling a week after a bug fix',
              'A bug under-counted wallet payments for seven days. The code is fixed; now the past must be repaired. Watch why idempotent tasks make a backfill safe, and appends make it a disaster.',
              'Backfill', 'Seven daily revenue bars re-computed by a backfill, with appending and with overwriting', fr2,
              ['For seven days, a conversion bug published revenue that was too low. The fix is now in the code.',
               'A <b>backfill</b> re-runs the fixed DAG for each logical date from 13 to 19 October, each run touching only its own day.',
               'If the publish step <b>appended</b> rows, the corrected rows would be added on top of the wrong ones, roughly doubling every day.',
               'Because publish <b>overwrites</b> each date partition, each day is replaced by its correct value, and running the backfill twice changes nothing.',
               'Tables built from these days (weekly and monthly summaries) are re-run too, in dependency order. (Figures are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): logical date + late data
def timeline(marks, note1, note2, tone='blue', extra=''):
    o = '<path d="M20 70h320" class="s-line"/>' + ''.join(f'<path d="M{20 + k * 64} 64v12" class="s-line"/>' + t(20 + k * 64, 92, d, 7.8, 'ink3') for k, d in enumerate(['Sun 00:00', 'Mon 00:00', 'Mon 01:00', 'Tue 00:00', 'Wed 00:00', 'Thu']))
    return o + marks + extra + cap(note1, note2, tone, y=150, h=44)
fr3 = [
    timeline(fill(20, 54, 64, 12, 'acc', rx=3, opacity=.6) + t(52, 48, 'data interval: Sunday', 8.4, 'acc', bold=True), 'The run for logical date Sunday covers Sunday’s data:', 'from Sun 00:00 to Mon 00:00.', 'blue'),
    timeline(fill(20, 54, 64, 12, 'acc', rx=3, opacity=.6) + '<circle cx="148" cy="70" r="6" style="fill:var(--blue)"/>' + t(148, 48, 'runs Mon 01:00', 8.4, 'blue', bold=True), 'It actually runs Monday 1 am, once the day is complete.', 'Tasks use the logical date, never “today”.', 'blue'),
    timeline(fill(20, 54, 64, 12, 'acc', rx=3, opacity=.6) + '<circle cx="230" cy="70" r="6" style="fill:#D64545"/>' + t(230, 48, 'Tue: 1,200 late Sunday orders', 8.4, 'red', bold=True), 'Phones that were offline upload Sunday orders on Tuesday.', 'Sunday’s published numbers are now too low.', 'red'),
    timeline(fill(20, 54, 64, 12, 'green', rx=3, opacity=.7) + '<circle cx="276" cy="70" r="6" style="fill:var(--green)"/>' + t(276, 48, 'Wed run: redo Mon–Tue + Sun', 8.4, 'green', bold=True), 'Fix: each daily run also reprocesses the previous 3 days.', 'Safe only because tasks overwrite their partitions.', 'green'),
    timeline(fill(20, 54, 64, 12, 'green', rx=3, opacity=.7), 'Plus a sensor: the run waits until the source says', '“Sunday is complete” before extracting.', 'green', extra=label_box(110, 100, 140, 30, ['sensor: _SUCCESS file'], 'violet', 8.6)),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Logical dates, late data and sensors',
              'Real data doesn’t arrive on time. Orders from phones that were offline can show up days later. Watch how logical dates, a reprocessing window and a sensor keep daily numbers correct.',
              'Time in pipelines', 'A timeline of a daily run, its data interval, late-arriving data and a reprocessing window', fr3,
              ['Each run is responsible for one <b>data interval</b>. The run with logical date Sunday covers all of Sunday, midnight to midnight.',
               'It actually starts on Monday at 1 am, once Sunday is complete. Every task uses the logical date, so the same run gives the same answer if repeated later.',
               'On Tuesday, phones that were offline upload 1,200 orders that happened on Sunday. Sunday’s published revenue is now too low.',
               'A common fix: every daily run also re-processes the last three days. Because tasks overwrite their date partitions, re-processing is safe and late data is absorbed.',
               'A <b>sensor</b> can also make a run wait until the source signals that a day is complete (for example a <code>_SUCCESS</code> marker file) before extracting.'])

realworld = '''  <p>Three live scenarios: a failure that retries can’t fix, a week-long backfill after a bug, and an advanced look at logical dates and late-arriving data.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Where orchestration runs every day</h3>
''' + usecase('<rect x="14" y="30" width="22" height="30" rx="4" style="fill:var(--blue)"/><rect x="48" y="30" width="22" height="30" rx="4" style="fill:var(--track)"/><rect x="82" y="30" width="22" height="30" rx="4" style="fill:var(--green)"/><path d="M36 45h12M70 45h12" style="stroke:var(--ink);stroke-width:2"/>',
              '1. Nightly business reporting', 'Most companies run hundreds of nightly DAGs: copy yesterday’s data from app databases, build silver and gold tables in Spark or dbt, check quality and refresh dashboards before offices open.', ['App DBs', '*Airflow DAGs', 'Morning dashboards']) + usecase(
    '<circle cx="60" cy="45" r="26" class="s-soft-violet" style="stroke:var(--violet);stroke-width:2"/><text x="60" y="50" text-anchor="middle" font-size="11" font-weight="700" class="s-violet">ML</text>',
    '2. Machine-learning retraining', 'Recommendation and fraud models are retrained on a schedule: build features, train, evaluate against the current model, and deploy only if better, all as one orchestrated pipeline.', ['Features', '*Train → evaluate', 'Deploy if better']) + usecase(
    '<rect x="16" y="22" width="88" height="46" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="50" text-anchor="middle" font-size="9" class="s-blue mono">RBI / GST</text>',
    '3. Regulatory and finance reports', 'Banks, NBFCs and e-commerce firms produce daily and monthly regulatory and tax reports with strict deadlines. Orchestrators track SLAs and alert long before a deadline is missed.', ['Ledgers', '*Checked pipeline', 'Filed on time']) + usecase(
    '<path d="M16 45h88" style="stroke:var(--green);stroke-width:3"/><circle cx="30" cy="45" r="7" style="fill:var(--green)"/><circle cx="60" cy="45" r="7" style="fill:var(--green)"/><circle cx="90" cy="45" r="7" style="fill:var(--green)"/>',
    '4. Keeping streaming systems healthy', 'Even real-time platforms need scheduled jobs: compacting small files, reprocessing late data, rebuilding aggregates, and running data-quality checks on stream outputs.', ['Stream output', '*Scheduled maintenance', 'Clean tables'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Monday 9 am: Sunday’s revenue is ₹0', story)
        + part(2, 'definition', 'Definition', 'What are data pipelines and orchestration?', definition)
        + part(3, 'types', 'Types and ways to use it', 'Kinds of pipelines, and cron vs an orchestrator', types)
        + part(4, 'steps', 'Step by step', 'Building a reliable daily pipeline', steps)
        + part(5, 'animation', 'See it happen', 'One night: what the managers see, and what Airflow does', '  <p>Step through the six frames. Left: the dashboard the managers will open. Right: the DAG run behind it, including a failure and a retry.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: pipelines on bad days', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Pipeline design', 'Fresher', 'Design a daily sales pipeline',
            'Orders live in a PostgreSQL database. Finance wants yesterday’s revenue by city on a dashboard by 8 am every day.',
            'can you design a simple, reliable, orchestrated pipeline?',
            '<ol><li>Airflow DAG scheduled at 1 am, parameterised by the logical date.</li><li><b>Extract</b> yesterday’s orders (by <code>updated_at</code>) to the lake as <code>bronze/orders/date=…</code>.</li><li><b>Validate</b>: row count vs the source, no negative amounts, no null cities.</li><li><b>Transform</b> to a gold table <code>revenue_by_city</code>, overwriting that date’s partition.</li><li><b>Publish</b> to the dashboard; on failure, retries then an alert and a “delayed” banner.</li><li>Add an SLA alert if not done by 7 am.</li></ol>',
            'a cron job per script with no dependencies or checks.')
        + scn('Reliability · idempotency', '1–3 years', 'Re-running a job doubled the numbers',
              'A failed job was re-run manually and the monthly revenue report now shows twice the real amount for that day.',
              'do you understand idempotency and how to make pipelines safe to re-run?',
              '<p>The load step appends rows, so each run adds the day again. Make the task idempotent: write to a date partition and overwrite it (<code>INSERT OVERWRITE</code> or replace the folder), or use <code>MERGE</code> on a unique key. Deduplicate the affected day, then re-run once more to prove nothing changes. Add a check that compares row counts with the source.</p>',
              'asking people to “be careful not to run it twice”.')
        + scn('Airflow · concepts', '1–3 years', 'Why does the 19 Oct run happen on 20 Oct?',
              'A new teammate is confused: the DAG run labelled 2026-10-19 started at 1 am on 20 October, and their task that uses <code>datetime.now()</code> processed the wrong day.',
              'do you understand logical dates and data intervals?',
              '<p>In Airflow, a run’s logical date marks the start of the data interval it processes. A daily run for 19 October can only start after the interval ends, so it runs on 20 October. Tasks must use the run’s logical date (<code>ds</code>, <code>data_interval_start</code>) rather than <code>now()</code>, so that retries and backfills process the intended day.</p>',
              'changing the schedule to run “earlier” or hard-coding yesterday’s date.')
        + scn('Architecture · tools', 'Fresher', '“Should Spark run inside Airflow?”',
              'A teammate wants to load a 200 GB dataset into a Python task inside Airflow because “Airflow already runs Python”.',
              'do you know what an orchestrator is for?',
              '<p>No. Airflow should coordinate work, not do heavy processing. Its workers are sized for many small tasks, and big in-memory work there will crash workers and slow the scheduler. Use Airflow to submit a Spark job (on Databricks, EMR, Dataproc or Kubernetes), a warehouse SQL statement or a dbt run, wait for it, check the result and move on.</p>',
              'scaling Airflow workers to hundreds of GB of RAM to process data in tasks.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
