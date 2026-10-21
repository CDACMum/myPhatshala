import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
layers = [('raw', 'JSON lines', 'card'), ('bronze', 'Parquet by date', 'amber'), ('silver', 'clean · dedup · masked', 'blue'), ('gold', 'business tables', 'green'), ('report', 'revenue by city', 'violet')]
sc = ''
for k, (a, b, tone) in enumerate(layers):
    x = 14 + k * 124
    sc += box(x, 34, 110, 84, tone) + t(x + 55, 64, a, 11, bold=True) + t(x + 55, 90, b, 8.2, 'ink2')
    if k < 4:
        sc += arrow(x + 111, 76, x + 123, 76, 'ink3', 1.6)
sc += t(320, 20, 'capstone_pipeline.py · runs on your laptop in seconds', 9.4, 'acc', bold=True)
scene_svg = scene('The capstone pipeline: raw JSON lines become bronze Parquet partitioned by date, then cleaned silver tables, then gold business tables and a report.', sc,
                  'Every idea from the course, <tspan font-weight="700" class="s-acc">in one pipeline you can run</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Kabir’s full-time interview at TiffinGo ends with a surprise: “Before the offer, show us a small pipeline you built yourself, end to end, on your own laptop.” Riya, who has followed every lesson with him, wants to build one too for her portfolio. Arjun Sir gives them both the same brief.</p>

{scene_svg}

A> Three days of order data. Land it raw, store it as Parquet partitioned by date, clean it with quality checks, mask phone numbers, build gold tables, print a report. And it must be safe to run twice.
R> On a laptop? I thought big data needs a cluster.
A> The <i>design</i> is what matters, Riya. Bronze, silver, gold, partitions, a quality gate, idempotent writes: these are exactly what you’d build on Spark and a cloud lake. You’ll just run it with Python and Parquet first, and swap the engine later.
K> What will the reviewers look at?
A> Whether it runs with one command, whether the numbers are right and explained, whether bad data is handled, whether a re-run creates duplicates, and whether your README explains the decisions. Today you’ll build it step by step, run it, break it on purpose, and see how each piece maps to production tools.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> The capstone at three levels
L1> Build it and run it
      <ul>
      <li>Generate three days of raw orders with realistic problems (duplicates, missing cities, zero quantities).</li>
      <li>Store raw data as files, then as Parquet in folders named <code>date=YYYY-MM-DD</code> (bronze).</li>
      <li>Clean it (silver): remove duplicates, quarantine bad rows, replace phone numbers with keys.</li>
      <li>Summarise it (gold): revenue by city per day and revenue by dish, then print a report.</li>
      </ul>
L2> Make it reliable
      <ul>
      <li><b>Idempotency:</b> each step overwrites its own date partition, so re-running gives identical results.</li>
      <li><b>Quality gate:</b> the run stops if more than 2% of rows fail checks; quarantined rows are kept for review.</li>
      <li><b>Repeatability:</b> fixed random seeds per day, so anyone can reproduce your numbers.</li>
      <li><b>Logging:</b> each step logs row counts, so a reviewer can follow where rows went.</li>
      <li><b>README:</b> problem, architecture diagram, how to run, results, decisions and limitations.</li>
      </ul>
L3> Take it towards production
      <ul>
      <li>Swap pyarrow for <b>PySpark</b> or <b>DuckDB</b>; store tables in <b>Delta Lake</b> or <b>Iceberg</b> for ACID MERGE and time travel.</li>
      <li>Schedule each step as a task in an <b>Airflow</b> DAG with retries, backfills and alerts.</li>
      <li>Ingest from <b>Kafka</b> instead of files for a streaming bronze layer; keep the batch gold for finance.</li>
      <li>Move storage to object storage (S3, ADLS, GCS or local MinIO), add tests and CI, data contracts and cost notes.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>capstone project</b> is an end-to-end project that integrates the skills of a course into one working system. Here it is a <b>batch data pipeline</b> implementing the <b>medallion architecture</b>: raw ingestion, a <b>bronze</b> layer of source data in a columnar format partitioned by date, a <b>silver</b> layer of deduplicated, validated and privacy-protected records, and a <b>gold</b> layer of aggregated business tables, with a <b>data quality gate</b>, <b>idempotent</b> partition overwrites and reproducible outputs.',
    'You build a small but complete data pipeline on your own computer: messy raw data goes in, clean trustworthy business numbers come out, and running it again never creates duplicates. It uses the same design real companies use, only smaller.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Medallion architecture', 'Bronze (raw), silver (clean), gold (business-ready) layers in a lake or lakehouse.'),
    ('Partition overwrite', 'Replacing one partition (one date folder) completely on each run, which makes the step idempotent.'),
    ('Quarantine table', 'Where rows that fail quality checks are kept for review instead of being dropped silently.'),
    ('Reproducibility', 'Anyone running the same code on the same inputs gets the same outputs.'),
    ('pyarrow', 'The Python library for Apache Arrow tables and Parquet files, used here as a small local engine.'),
    ('Hive-style partitions', 'Folders named <code>column=value</code> (for example <code>date=2026-10-19</code>) that engines read as a column.'),
    ('Backfill', 'Re-running the pipeline for past dates, safe only when steps are idempotent.'),
    ('README', 'The front page of the project: what, why, how to run, results and decisions.'),
]) + '''

  <h3>The brief</h3>
''' + facts([
    ('Input', '3 days of food-delivery orders as JSON lines, about 20,000 rows a day, with duplicates, missing cities and invalid quantities'),
    ('Output', 'Gold tables: revenue and order count by city per day; revenue by dish; plus a printed report'),
    ('Rules', 'Quality gate at 2%; no raw phone numbers after bronze; identical results on re-run; one command to run'),
    ('Tools', 'Python 3 and pyarrow (<code>pip install pyarrow</code>); optional: DuckDB, PySpark, Airflow for extensions'),
]) + lv + '''
EXAM> Describe an end-to-end pipeline using the <b>medallion architecture</b>: the purpose of each layer, the <b>data quality</b> checks in silver, how <b>partitioning</b> and <b>idempotent overwrites</b> make re-runs safe, and how the design maps to <b>Spark, Delta Lake and Airflow</b> in production.'''

# ---------------------------------------------------------------- types
types = table(['Layer', 'Folder', 'What happens', 'Course lessons used'], [
    ['<b>Raw</b>', '<code>lake/raw/</code>', 'The app’s export lands unchanged as JSON lines', '2.1 data types · 2.2 file formats'],
    ['<b>Bronze</b>', '<code>lake/bronze/orders/date=…/</code>', 'Same rows, stored as Parquet, one folder per date', '2.2 Parquet · 3.2 partitioning'],
    ['<b>Silver</b>', '<code>lake/silver/orders/date=…/</code>', 'Deduplicated, validated, phones replaced by keys; bad rows to quarantine', '5.1 quality and privacy · 4.5 idempotency'],
    ['<b>Gold</b>', '<code>lake/gold/</code>', 'Revenue by city per day; revenue by dish', '4.x lakehouse and SQL engines'],
    ['<b>Report</b>', 'terminal output', 'The numbers a manager would read', '1.1 value from data'],
], minw=680) + '''

  <h3>How reviewers grade a capstone</h3>
''' + cards([
    ('Runs first time', 'One command, clear requirements, fixed seeds, no hard-coded personal paths.', '20%'),
    ('Correct and explained', 'Row counts reconcile at every step; numbers are checked and described in the README.', '30%'),
    ('Reliable', 'Quality gate, quarantine, idempotent re-runs, sensible errors.', '30%'),
    ('Communicated', 'README with architecture, decisions, limitations and next steps; clean code.', '20%'),
]) + '''
TIP> Write the README <b>while</b> you build, not after. Each time you make a decision (“overwrite the partition instead of appending”), add one line explaining why. That list becomes your best interview material.'''

# ---------------------------------------------------------------- steps
c1 = '''day = "2026-10-19"
print(f"lake/bronze/orders/date={day}/part-0.parquet")'''
c2 = '''ids = ["A", "B", "A", "C", "B"]
seen, keep = set(), []
for i in ids:
    if i not in seen:
        seen.add(i); keep.append(i)
print(keep, "removed", len(ids) - len(keep))'''
c3 = '''rows, bad = 21_429 - 150, 100
print(f"failure rate {bad / rows:.2%}", "-> continue" if bad / rows <= 0.02 else "-> STOP")'''
steps = stepper([
    ('Extract: land the raw data',
     '<p><code>extract(day)</code> writes one JSON-lines file per day into <code>lake/raw/</code>, with duplicates, missing cities and zero quantities, exactly like a real export.</p>',
     'Keeping raw data unchanged means you can always rebuild every later layer if a bug is found.'),
    ('Bronze: Parquet partitioned by date',
     code('python', 'bronze_path.py', c1, run_code(c1)),
     'Columnar files compress well and read fast; date folders let later steps and queries touch only the days they need. The folder is deleted and rewritten each run, so it is idempotent.'),
    ('Silver: deduplicate',
     code('python', 'dedup.py', c2, run_code(c2)),
     'Retries create duplicate orders. Keeping the first occurrence of each order_id removes them; in Spark or Delta you would use dropDuplicates or MERGE.'),
    ('Silver: quality gate and masking',
     code('python', 'gate.py', c3, run_code(c3)),
     'Rows with qty ≤ 0 or no city go to quarantine. Above 2% the pipeline stops. Phone numbers become salted-hash customer keys, so analysts never see them.'),
    ('Gold: business tables',
     '<p><code>gold()</code> reads all silver partitions, groups by date and city and by dish, and writes two small Parquet tables for dashboards.</p>',
     'Gold tables are small, fast and named in business language, the only layer most users ever query.'),
    ('Prove it: re-run and compare',
     '<p>The script runs the whole pipeline a second time and checks that the gold table is identical.</p>',
     'This one check demonstrates idempotency, the property interviewers ask about most for pipelines.'),
])

# ---------------------------------------------------------------- two-view animation: terminal vs lake folder
def term(lines, hl=None):
    o = '<rect x="14" y="14" width="332" height="186" rx="8" style="fill:#1E2A24"/>' + t(28, 32, '$ python capstone_pipeline.py', 8.6, 'acc', anchor='start', mono=True, extra=' style="fill:#E8C07A"')
    for k, s in enumerate(lines):
        o += t(28, 52 + k * 16, s, 7.8, anchor='start', mono=True, extra=' style="fill:#9FE0B8"' if k == hl else ' style="fill:#E6EDE9"')
    return o
L = ['[extract] 2026-10-17: 20,005 raw rows', '[silver ] 19,755 clean, 150 dup, 100 bad', '[extract] 2026-10-18: 18,998 raw rows', '[silver ] 18,748 clean, 150 dup, 100 bad',
     '[extract] 2026-10-19: 21,429 raw rows', '[silver ] 21,179 clean, 150 dup, 100 bad', '[gold   ] 59,682 orders -> 2 gold tables', 'Gold identical after re-run: True']
see = [term(L[:1], 0), term(L[:2], 1), term(L[:6], 5), term(L[:7], 6), term(L[:7] + ['Mumbai 11,17,740 · Thane 11,05,820 …'], 7), term(L[:7] + ['re-run …', L[7]], 8)]
def tree(items, note):
    o = ''
    for k, (depth, name, tone) in enumerate(items):
        o += t(24 + depth * 16, 30 + k * 15, ('▸ ' if '/' in name and not name.endswith(('.parquet', '.jsonl')) else '· ') + name, 8, tone, anchor='start', mono=True)
    return o + t(180, 206, note, 8.4, 'ink2')
base = [(0, 'lake/', 'ink')]
r1 = [(1, 'raw/', 'ink'), (2, 'orders_2026-10-17.jsonl', 'acc')]
b1 = [(1, 'bronze/orders/', 'ink'), (2, 'date=2026-10-17/', 'amber'), (3, 'part-0.parquet', 'amber')]
s1_ = [(1, 'silver/', 'ink'), (2, 'orders/date=2026-10-17/', 'blue'), (2, 'quarantine/date=2026-10-17/', 'red')]
behind = [
    tree(base + r1, 'Day 1 raw file written: 20,005 JSON lines.'),
    tree(base + r1 + b1 + s1_, 'Bronze Parquet, then silver orders and quarantine for day 1.'),
    tree(base + [(1, 'raw/  (3 files)', 'acc'), (1, 'bronze/orders/  date=17, 18, 19', 'amber'), (1, 'silver/orders/  date=17, 18, 19', 'blue'), (1, 'silver/quarantine/  date=17, 18, 19', 'red')], 'All three days in every layer, one folder per date.'),
    tree(base + [(1, 'raw/  (3 files)', 'acc'), (1, 'bronze/orders/  date=17, 18, 19', 'amber'), (1, 'silver/…  date=17, 18, 19', 'blue'), (1, 'gold/', 'green'), (2, 'daily_city_revenue.parquet', 'green'), (2, 'dish_revenue.parquet', 'green')], 'Gold reads all silver partitions and writes 2 small tables.'),
    tree(base + [(1, 'gold/daily_city_revenue.parquet', 'green'), (2, 'date | city | amount_sum | count', 'ink2'), (2, '2026-10-19 | Mumbai | 1117740 | 5352', 'ink2')], 'The report reads gold only: small, fast, business language.'),
    tree(base + [(1, 'bronze/orders/date=2026-10-17/', 'amber'), (2, 'deleted and rewritten', 'ink2'), (1, 'silver/orders/date=2026-10-17/', 'blue'), (2, 'deleted and rewritten', 'ink2'), (1, 'still 14 files in total', 'green')], 'Re-run overwrites each partition: no duplicates, same totals.'),
]
see_caps = ['Kabir runs the script. Day 1’s raw export is extracted: 20,005 rows.', 'Silver for day 1: 19,755 clean rows, 150 duplicates removed, 100 quarantined.', 'All three days processed.',
            'Gold built from 59,682 clean orders.', 'The report prints revenue by city.', 'The pipeline runs again and confirms identical gold output.']
behind_caps = ['A JSON-lines file appears in lake/raw/. Raw data is kept exactly as received.',
               'The day is written to bronze as Parquet under date=2026-10-17, then cleaned into silver; failing rows go to a separate quarantine partition.',
               'Every layer now has one folder per date. A later query for one day reads only that folder.',
               'The gold step reads all silver partitions together and writes two small business tables.',
               'The report and any dashboard read only gold tables, which are tiny compared with raw data.',
               'Re-running deletes and rewrites each partition instead of appending, so the lake still has 14 files and the totals are unchanged: idempotency in practice.']
two = anim_two('Running the capstone', 'What Kabir sees in the terminal, and what appears in the lake folder', 'The capstone pipeline’s terminal output line by line',
               'The lake folder filling with raw, bronze, silver, quarantine and gold files', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: row reconciliation (real numbers from capstone_pipeline.out)
def recon(n, note1, note2, tone):
    stages = [('raw', 21_429, 'card'), ('− duplicates', 150, 'amber'), ('− quarantined', 100, 'red'), ('= silver', 21_179, 'blue')]
    o = t(14, 22, 'Day 2026-10-19: where every row went', 9, 'ink2', anchor='start')
    for k, (lab, v, tn) in enumerate(stages[:n]):
        o += label_box(14 + k * 84, 36, 78, 52, [lab, f'{v:,}'], tn, 9)
    return o + cap(note1, note2, tone, y=110, h=44)
fr1 = [
    recon(1, 'Day 3 arrives: 21,429 raw rows,', 'including retries and broken records.', 'blue'),
    recon(2, 'Dedup on order_id removes 150 duplicates', '(the same orders sent twice by retries).', 'amber'),
    recon(3, '100 rows fail checks (qty 0 or no city):', '0.47% of rows, below the 2% gate. Quarantined.', 'red'),
    recon(4, '21,429 − 150 − 100 = 21,179 clean rows.', 'Every row is accounted for.', 'green'),
    recon(4, 'Across 3 days: 59,682 clean orders in gold.', 'Reconciliation like this belongs in your README.', 'green'),
]
s1 = anim_one('Real-time scenario 1', 'Account for every row',
              'These figures come from the program in “Run it on your PC” below. Reviewers trust pipelines whose row counts add up at every step. Watch one day reconcile.',
              'Row reconciliation', 'Raw rows reduced by duplicates and quarantined rows to the clean silver count for one day', fr1,
              ['On 19 October the export has 21,429 rows, including duplicates from retries and some broken records.',
               'Deduplicating on order_id removes 150 rows.',
               '100 rows fail the quality checks, 0.47% of the remaining rows, so the gate lets the run continue and the rows are kept in quarantine.',
               '21,429 − 150 − 100 = 21,179 clean rows in silver: every row is accounted for.',
               'Over three days, 59,682 clean orders reach gold. A small table like this in the README shows a reviewer you understand your data.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: append bug vs overwrite
def runs(rev, note1, note2, tone, label):
    o = t(14, 22, 'Gold revenue for 2026-10-19 after each run (₹)', 9, 'ink2', anchor='start')
    o += bars([(f'run {k + 1}', v / (3 * true_rev) * 100, 'red' if v > true_rev else 'green', f'₹{v / 1e5:.1f} L') for k, v in enumerate(rev)], x=90, y=34, w=200, gap=22)
    o += t(180, 120, label, 9.4, 'red' if 'append' in label else 'green', bold=True)
    return o + cap(note1, note2, tone, y=134, h=44)
true_rev = 4_395_530
fr2 = [
    runs([true_rev], 'Run 1: revenue for 19 October is about ₹44 lakh.', 'Correct.', 'blue', 'mode: append'),
    runs([true_rev, true_rev * 2], 'Airflow retries the task after a timeout.', 'With append, the day is written twice: ₹88 lakh.', 'red', 'mode: append'),
    runs([true_rev, true_rev * 2, true_rev * 3], 'A backfill runs it again: ₹1.3 crore.', 'The dashboard is now three times wrong.', 'red', 'mode: append'),
    runs([true_rev, true_rev, true_rev], 'Same three runs with partition overwrite:', 'the date folder is replaced each time.', 'green', 'mode: overwrite partition'),
    runs([true_rev, true_rev, true_rev], 'Retries and backfills are now safe.', 'In Delta: replaceWhere or MERGE on order_id.', 'green', 'mode: overwrite partition'),
]
s2 = anim_one('Real-time scenario 2', 'Break it on purpose: append vs overwrite',
              'The fastest way to understand idempotency is to break it. Change the write to append and watch retries and backfills multiply revenue.',
              'Idempotent writes', 'Gold revenue tripling with append mode across retries, but staying correct with partition overwrite', fr2,
              ['The first run writes 19 October’s silver and gold data: about ₹44 lakh of revenue (₹43.96 lakh, the sum of the four cities in the report).',
               'An orchestrator retries the task after a timeout. If the step appends, the same day’s rows are written again and revenue doubles.',
               'A backfill re-runs the day once more. The dashboard now shows three times the real figure, with no error anywhere.',
               'With partition overwrite (the capstone’s design: delete the date folder, then write), each run replaces the day completely.',
               'Retries and backfills become safe. In Delta Lake you would use <code>replaceWhere</code> for a date or <code>MERGE</code> on order_id; in Iceberg, overwrite-partitions or MERGE.'])

# ---------------------------------------------------------------- scenario 3 (advanced): from laptop to production
pairs = [('JSON files in lake/raw', 'Kafka topic / app export to object storage'), ('pyarrow on a laptop', 'PySpark on Databricks, EMR or Dataproc'),
         ('Parquet folders', 'Delta Lake / Iceberg (ACID, MERGE)'), ('for day in DATES', 'Airflow DAG: daily schedule, retries, backfill'),
         ('print() logs', 'Logs, metrics, alerts; data quality tool'), ('local lake/ folder', 'S3 / ADLS / GCS (or MinIO locally)')]
def prod(n, note1, note2, tone):
    o = t(90, 20, 'Your capstone', 9.4, 'blue', bold=True) + t(270, 20, 'Production', 9.4, 'green', bold=True)
    for k, (a, b) in enumerate(pairs[:n]):
        y = 30 + k * 18
        o += t(14, y + 10, a, 7.8, anchor='start', mono=True) + arrow(150, y + 6, 166, y + 6, 'ink3', 1.2) + t(170, y + 10, b, 7.8, 'green', anchor='start')
    return o + cap(note1, note2, tone, y=146, h=44)
fr3 = [
    prod(2, 'The same design, scaled: files become a stream', 'or cloud export; pyarrow becomes Spark.', 'blue'),
    prod(3, 'Parquet folders become Delta or Iceberg tables,', 'adding ACID commits, MERGE and time travel.', 'acc'),
    prod(4, 'The for-loop over dates becomes an Airflow DAG', 'with one task per layer, retries and backfills.', 'violet'),
    prod(6, 'Logs become metrics and alerts; the laptop folder', 'becomes object storage with access controls.', 'amber'),
    prod(6, 'Nothing in the design changes: bronze, silver,', 'gold, quality gate, idempotent writes.', 'green'),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'From your laptop to a production lakehouse',
              'Reviewers often ask: “How would this work at 1,000 times the data?” Watch each part of the capstone map to its production equivalent.',
              'Scaling the design', 'Each capstone component mapped to production tools: Kafka, Spark, Delta or Iceberg, Airflow, monitoring and object storage', fr3,
              ['Raw JSON files become a Kafka topic or an export landing in object storage; pyarrow becomes PySpark on a managed cluster.',
               'Plain Parquet folders become Delta Lake or Iceberg tables, adding ACID commits, MERGE for upserts, schema enforcement and time travel.',
               'The loop over dates becomes an Airflow DAG with tasks for bronze, silver and gold, retries, alerts and backfills by date.',
               'Print statements become structured logs, metrics and alerts, and quality checks move into a tool such as Great Expectations or dbt tests. The local folder becomes S3, ADLS or GCS with IAM.',
               'The architecture itself does not change, which is exactly why this capstone is a strong portfolio piece: it proves you understand the design, not just one tool.'])

realworld = '''  <p>Three live scenarios: reconciling every row of one day (real numbers from the program below), breaking idempotency on purpose, and an advanced map from the capstone to production tools.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Extend your capstone</h3>
''' + usecase('<rect x="20" y="24" width="80" height="44" rx="8" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="51" text-anchor="middle" font-size="11" font-weight="700" class="s-blue">SQL</text>',
              '1. Query the lake with DuckDB', 'Install DuckDB and run SQL directly on the Parquet folders: <code>SELECT city, SUM(amount) FROM \'lake/silver/orders/*/*.parquet\' GROUP BY city</code>.', ['Parquet files', '*DuckDB SQL', 'Ad-hoc answers']) + usecase(
    '<circle cx="34" cy="46" r="12" style="fill:var(--acc);opacity:.6"/><circle cx="86" cy="46" r="12" style="fill:var(--acc);opacity:.6"/><path d="M46 46h28" style="stroke:var(--ink3);stroke-width:2"/>',
    '2. Rewrite silver in PySpark', 'Replace the pyarrow code with Spark DataFrames: <code>dropDuplicates</code>, <code>filter</code>, <code>withColumn</code>, <code>partitionBy("date")</code>. Compare speed and code.', ['Bronze', '*Spark DataFrames', 'Silver']) + usecase(
    '<path d="M20 60 L45 30 L70 50 L100 25" style="fill:none;stroke:var(--violet);stroke-width:3"/>',
    '3. Orchestrate with Airflow', 'Turn extract, bronze, silver and gold into four tasks in a daily DAG with retries and a backfill for October.', ['Schedule', '*DAG with 4 tasks', 'Retries + backfill']) + usecase(
    '<rect x="22" y="26" width="76" height="40" rx="6" class="s-soft-green" style="stroke:var(--green)"/><path d="M36 46l10 10 18-18" style="fill:none;stroke:var(--green);stroke-width:3"/>',
    '4. Add tests and CI', 'Write pytest tests for dedup, the quality gate and masking; run them on every push with GitHub Actions; add the badge to your README.', ['Code', '*pytest + CI', 'Trust']) + '''

  <h3>README template for your capstone</h3>
''' + table(['Section', 'What to write'], [
    ['<b>Problem</b>', 'One paragraph: daily food-delivery orders need trustworthy revenue reporting.'],
    ['<b>Architecture</b>', 'Diagram: raw → bronze → silver (+ quarantine) → gold → report, with tools.'],
    ['<b>How to run</b>', '<code>pip install pyarrow</code> then <code>python capstone_pipeline.py</code>; expected output.'],
    ['<b>Data and quality</b>', 'Row reconciliation table per day; quality rules and the 2% gate.'],
    ['<b>Decisions</b>', 'Why Parquet, why date partitions, why overwrite, why hashed keys.'],
    ['<b>Results</b>', 'Revenue by city and dish; run time.'],
    ['<b>Limitations and next steps</b>', 'Single machine, no ACID tables, no scheduler: how you would add Spark, Delta, Airflow.'],
], minw=560)

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Show us something you built', story)
        + part(2, 'definition', 'Definition', 'The capstone: a mini lakehouse pipeline', definition)
        + part(3, 'types', 'Types and ways to use it', 'Layers, folders and grading', types)
        + part(4, 'steps', 'Step by step', 'Building the pipeline', steps)
        + part(5, 'animation', 'See it happen', 'One run: the terminal, and the lake folder', '  <p>Step through the six frames. Left: the terminal output. Right: files appearing in the lake.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: reconcile, break and scale', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Capstone review', 'Fresher', '“Walk me through your pipeline.”',
            'A reviewer opens your capstone repository and asks for a two-minute walkthrough.',
            'can you explain design and data flow clearly?',
            '<p>Problem → layers → numbers → decisions: “Three days of orders land as JSON in raw. Bronze stores them as Parquet partitioned by date. Silver removes 150 duplicates a day by order_id, quarantines about 0.5% invalid rows behind a 2% gate and replaces phones with hashed keys. Gold has revenue by city and dish. Every step overwrites its date partition, so re-runs are identical; the script proves it by re-running. Next I’d move to Delta Lake and Airflow.”</p>',
            'reading the code line by line.')
        + scn('Reliability', '1–3 years', '“What happens if the silver step fails halfway?”',
              'The reviewer asks about partial failures.',
              'do you understand atomicity and recovery?',
              '<p>In the capstone, a failed write may leave a partly written folder, but the next run deletes and rewrites that date, so it self-heals. In production, write to a temporary location and move atomically, or use Delta Lake or Iceberg, where a commit is atomic: readers see the old version until the new one is complete. Orchestrator retries are safe because the step is idempotent.</p>',
              'saying “it won’t fail”.')
        + scn('Scale', '1–3 years', '“What if each day had 50 crore rows?”',
              'The reviewer asks how the design changes at 25,000 times the volume.',
              'can you separate design from engine?',
              '<p>The layers, partitioning, quality gate and idempotent writes stay. Changes: run on Spark with many partitions instead of one Python process; dedup with <code>dropDuplicates</code> or MERGE; use Delta or Iceberg tables; partition by date (and maybe city) with file compaction; read silver incrementally for gold; store in object storage; add monitoring and cost controls.</p>',
              'proposing a different architecture for every tool.')
        + scn('Privacy', 'Fresher', '“Why hash phone numbers instead of deleting them?”',
              'The reviewer asks about the customer_key column.',
              'can you explain pseudonymisation and its limits?',
              '<p>Analysts need to count distinct and repeat customers without seeing phone numbers. A salted hash gives the same key for the same phone, so joins and counts work. It is pseudonymisation, not anonymisation: with the salt someone could re-identify customers, so the salt must be secret (a secrets manager, not the code) and access to bronze, which still has phones, must be restricted.</p>',
              'claiming hashing makes the data anonymous.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
