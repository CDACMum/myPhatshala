import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='07-capstone-project', lesson='01-build-a-mini-data-pipeline', n='7.1',
    module_label='Module 7 · Capstone Project',
    title='Capstone: build a mini data pipeline on your PC',
    desc='Capstone project for Big Data Fundamentals: build an end-to-end medallion pipeline on your own computer with Python and Parquet. Raw JSON lines to bronze Parquet partitioned by date, silver with deduplication, a data quality gate, quarantine and masked PII, gold business tables and a report, with idempotent re-runs. Includes row reconciliation, an append-vs-overwrite experiment, a map to Spark, Delta Lake and Airflow, extensions and a README template.',
    og_desc='Build a complete bronze-silver-gold pipeline on your laptop, prove it is idempotent, and turn it into a portfolio project.',
    minutes=45, level='Beginner → Advanced',
    lead='Everything from this course comes together in one program you can run. You will land three days of messy orders, store them as <b>Parquet partitioned by date</b>, clean them in a <b>silver</b> layer with a <b>quality gate</b> and masked phone numbers, build <b>gold</b> business tables, reconcile every row, break idempotency on purpose, and see how the same design runs on Spark, Delta Lake and Airflow.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Full capstone for your PC'],
)

RUN = dict(
    heading='The whole pipeline in miniature',
    intro='<p>This browser version uses only plain Python: raw records go through bronze, silver and gold as lists and dictionaries, with deduplication, a quality gate and masking. Then try the challenges: idempotent partitions, a new quality rule, a new gold table, a broken gate and a reconciliation check.</p>',
    code='''import hashlib
raw = [  # order_id, date, city, qty, price, phone
    ("A1", "10-19", "Pune", 1, 140, "9876543210"), ("A2", "10-19", "Thane", 2, 120, "9123456780"),
    ("A1", "10-19", "Pune", 1, 140, "9876543210"), ("A3", "10-19", None, 1, 220, "9988776655"),
    ("A4", "10-19", "Pune", 0, 60, "9090909090"), ("A5", "10-19", "Thane", 1, 220, "9811122233"),
]
bronze = {"10-19": list(raw)}                       # one partition per date

seen, silver, quarantine = set(), [], []
for oid, day, city, qty, price, phone in bronze["10-19"]:
    if oid in seen:
        continue                                    # duplicate from a retry
    seen.add(oid)
    if city is None or qty <= 0:
        quarantine.append(oid)
        continue
    key = hashlib.sha256(("salt:" + phone).encode()).hexdigest()[:8]
    silver.append((oid, day, city, qty * price, key))

gold = {}
for oid, day, city, amount, key in silver:
    gold[city] = gold.get(city, 0) + amount
print("silver:", len(silver), "| quarantine:", quarantine)
print("gold revenue by city:", gold)
''',
    anno=[
        ('    if oid in seen:', 'Deduplicate on the business key before anything else.'),
        ('    key = hashlib.sha256(("salt:" + phone).encode()).hexdigest()[:8]', 'Phones never reach silver; a salted hash keeps customers countable.'),
    ],
    tasks=[
        dict(label='1 · Run the pipeline', hint='Press <b>Run</b>. Check by hand: Pune 140, Thane 240 + 220 = 460. Which rows were dropped and why?', code=None),
        dict(label='2 · Overwrite vs append', hint='Run the “day” twice. Append doubles revenue; overwrite keeps it correct. Switch <code>MODE</code> and compare.',
             code='''MODE = "append"            # try "overwrite"
silver_day = [("A2", 240), ("A5", 220)]
table = {}
for run in range(2):          # e.g. a retry
    if MODE == "overwrite":
        table["10-19"] = list(silver_day)
    else:
        table.setdefault("10-19", []).extend(silver_day)
print(MODE, "->", sum(a for _, a in table["10-19"]))
'''),
        dict(label='3 · Add a quality rule', hint='Add a rule: price must be between 50 and 500. Add a bad row and see it quarantined.',
             code='''rows = [("A1", 140), ("A2", 9000), ("A3", 60), ("A4", 20)]
good, bad = [], []
for oid, price in rows:
    (good if 50 <= price <= 500 else bad).append(oid)
print("good", good, "| quarantine", bad)
'''),
        dict(label='4 · A new gold table', hint='Build revenue per dish from silver rows.',
             code='''silver = [("Veg thali", 140), ("Paneer roll", 240), ("Veg thali", 280), ("Poha", 60)]
gold = {}
for dish, amount in silver:
    gold[dish] = gold.get(dish, 0) + amount
print(sorted(gold.items(), key=lambda kv: kv[1], reverse=True))
'''),
        dict(label='5 · The quality gate (advanced)', hint='Stop the run if more than 2% of rows fail. Change <code>bad</code> to 500 and see it raise an error.',
             code='''total, bad = 21_279, 100
rate = bad / total
if rate > 0.02:
    raise RuntimeError(f"quality gate failed: {rate:.2%}")
print(f"gate passed: {rate:.2%} failed")
'''),
        dict(label='6 · Reconcile (advanced)', hint='Every raw row must be accounted for: raw = clean + duplicates + quarantined. Change one number to see the alarm.',
             code='''raw, dupes, quarantined, clean = 21_429, 150, 100, 21_179
diff = raw - dupes - quarantined - clean
print("reconciled" if diff == 0 else f"MISSING {diff} rows!")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: the full capstone pipeline',
    intro='<p>Install pyarrow once (<code>pip install pyarrow</code>), save this as <code>capstone_pipeline.py</code> in an empty folder and run it. It creates a <code>lake/</code> folder with raw, bronze, silver (orders and quarantine) and gold layers for three days, prints a report, then re-runs everything and proves the results are identical. Open the folders to see the partitions.</p>',
    items=[
        dict(title='Raw → bronze → silver → gold, then an idempotency test', file='capstone_pipeline.py',
             cmd=open(os.path.join(HERE, 'capstone_pipeline.py')).read() + '\n# In a terminal:  pip install pyarrow\n#                  python capstone_pipeline.py',
             output=open(os.path.join(HERE, 'capstone_pipeline.out')).read(),
             note='Recorded from a real run with Python 3.13 and pyarrow 26. Data is generated with a fixed seed per day, so your counts will match. It takes a few seconds on a normal laptop. Delete the lake/ folder any time; the script rebuilds it.'),
    ],
)

TRACE = dict(
    heading='Silver, one record at a time',
    intro='<p>Four raw records pass through deduplication and the quality check. Watch the seen set, the clean list and the quarantine fill up.</p>',
    code='''raw = [("A1", 1), ("A2", 0), ("A1", 1), ("A3", 2)]
seen, clean, bad = set(), [], []
for oid, qty in raw:
    if oid in seen:
        continue
    seen.add(oid)
    if qty > 0:
        clean.append(oid)
    else:
        bad.append(oid)
print("clean", clean, "bad", bad)
''',
    notes={4: 'Duplicate? :: A1 was already processed, so the retry is skipped.', 7: 'Quality :: Quantity must be positive.', 10: 'Quarantine :: Kept for review, not lost.'},
)

WORKED_INTRO = 'Four tasks you will meet while building and reviewing the capstone. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Partitions · paths', title='Build Hive-style partition paths',
         problem='<p>Generate the bronze folder path for each date in a list, in the <code>date=YYYY-MM-DD</code> format engines understand.</p>',
         inp='3 dates',
         approach=['Loop over dates.',
                   'Format the path with an f-string.',
                   'Print each path.'],
         code='''dates = ["2026-10-17", "2026-10-18", "2026-10-19"]
for d in dates:
    print(f"lake/bronze/orders/date={d}/part-0.parquet")
''', notes={3: 'Format :: column=value folders become a column when read.'},
         tryit='Partition by date and city: lake/bronze/orders/date=…/city=…/'),
    dict(level='i', tag='Silver · dedup by latest', title='Keep the latest version of each order',
         problem='<p>Sometimes duplicates are updates. Keep the record with the latest timestamp for each order_id.</p>',
         inp='(order_id, ts, status)',
         approach=['Track the best record per order_id in a dictionary.',
                   'Replace it when a later timestamp arrives.',
                   'Print the final records.'],
         code='''rows = [("A1", "10:00", "placed"), ("A2", "10:05", "placed"),
        ("A1", "10:20", "delivered"), ("A2", "10:01", "placed-old")]
latest = {}
for oid, ts, status in rows:
    if oid not in latest or ts > latest[oid][0]:
        latest[oid] = (ts, status)
print(latest)
''', notes={5: 'Newer wins :: Same logic as MERGE … WHEN MATCHED AND source.ts > target.ts.'},
         tryit='Two records have the same timestamp. Add a tiebreaker on status priority.'),
    dict(level='i', tag='Gold · aggregation', title='Daily revenue and order count by city',
         problem='<p>From silver rows, build a gold table of (date, city) → revenue and number of orders, sorted by revenue.</p>',
         inp='(date, city, amount) rows',
         approach=['Use a dictionary keyed by (date, city).',
                   'Add revenue and increment the count.',
                   'Sort by revenue, highest first.'],
         code='''rows = [("10-19", "Pune", 140), ("10-19", "Thane", 240), ("10-19", "Pune", 220), ("10-19", "Thane", 60)]
gold = {}
for day, city, amt in rows:
    rev, n = gold.get((day, city), (0, 0))
    gold[(day, city)] = (rev + amt, n + 1)
for key, (rev, n) in sorted(gold.items(), key=lambda kv: -kv[1][0]):
    print(key, "revenue", rev, "orders", n)
''', notes={4: 'Accumulate :: The same as GROUP BY date, city with SUM and COUNT.'},
         tryit='Add the average order value for each city.'),
    dict(level='a', tag='Reliability · idempotency test', title='Prove a step is idempotent',
         problem='<p>Write a test that runs a step twice on the same input and checks that the stored result is identical, for both an append step and an overwrite step.</p>',
         inp='a day of rows, two write functions',
         approach=['Write two versions of the step: append and overwrite.',
                   'Run each twice into a fresh store.',
                   'Compare the store after one run and after two.'],
         code='''day_rows = [("A1", 140), ("A2", 240)]
def write_append(store):
    store.setdefault("10-19", []).extend(day_rows)
def write_overwrite(store):
    store["10-19"] = list(day_rows)
for step in (write_append, write_overwrite):
    store = {}
    step(store); once = list(store["10-19"])
    step(store); twice = store["10-19"]
    print(step.__name__, "idempotent:", once == twice)
''', notes={7: 'Run twice :: An idempotent step leaves the same result after the second run.'},
         tryit='Turn this into a pytest test function that fails for the append version.'),
]

QUIZ = [
    dict(q='What is stored in the bronze layer of the capstone?', options=['Only aggregated revenue', 'The raw rows as Parquet, partitioned by date', 'Masked and deduplicated rows', 'The report text'], answer=1,
         why='Bronze keeps source data in a better format without changing its content.'),
    dict(q='Where are rows with qty 0 or a missing city sent?', options=['Deleted silently', 'Gold', 'A quarantine table', 'Back to raw'], answer=2,
         why='Quarantining keeps bad rows for review and fixing the source.'),
    dict(q='Why does the capstone delete and rewrite each date folder instead of appending?', options=['To save disk space', 'To make re-runs idempotent, so retries and backfills don’t duplicate data', 'Because Parquet can’t append', 'To make it slower'], answer=1,
         why='Partition overwrite gives identical results however many times a day is processed.'),
    dict(q='On 19 October there were 21,429 raw rows, 150 duplicates and 100 quarantined rows. How many clean rows?', options=['21,429', '21,279', '21,179', '21,329'], answer=2,
         why='21,429 − 150 − 100 = 21,179. Reconciliation should always add up.'),
    dict(q='Why are phone numbers replaced with salted hashes in silver?', options=['To compress them', 'So analysts can count customers without seeing phone numbers', 'Because Parquet can’t store strings', 'To speed up joins'], answer=1,
         why='Pseudonymous keys protect privacy while keeping customers countable and joinable.'),
    dict(q='What is the main benefit of folders named date=2026-10-19?', options=['They look neat', 'Engines read them as a column and can skip other dates', 'They encrypt the data', 'They remove duplicates'], answer=1,
         why='Hive-style partitions enable partition pruning.'),
    dict(q='In production, which tool would schedule the four steps with retries and backfills?', options=['Kafka', 'Apache Airflow', 'Parquet', 'pyarrow'], answer=1,
         why='An orchestrator such as Airflow runs tasks in order on a schedule with retries and backfills.'),
    dict(q='Which table format adds ACID commits and MERGE to the capstone’s Parquet folders?', options=['CSV', 'JSON', 'Delta Lake or Apache Iceberg', 'Excel'], answer=2,
         why='Table formats add a transaction log or metadata layer on top of Parquet files.'),
]

REVISION = [
    'Raw (unchanged) → bronze (Parquet by date) → silver (dedup, quality gate, quarantine, masked PII) → gold (business tables).',
    'Hive-style partitions: lake/bronze/orders/date=YYYY-MM-DD/ enable pruning and per-day rewrites.',
    'Idempotency: overwrite the date partition (or MERGE); never blind append. Prove it by re-running.',
    'Reconcile: raw = clean + duplicates + quarantined, for every day.',
    'Quality gate at 2%: continue and alert below it, stop above it.',
    'Production map: Kafka/exports, Spark, Delta/Iceberg, Airflow, monitoring, object storage.',
    'README: problem, diagram, how to run, reconciliation, decisions, results, limitations.',
]
FAQ = [
    ('What is a good capstone project for big data or data engineering?', 'An end-to-end pipeline that ingests realistic messy data, stores it in layers (bronze, silver, gold) using a columnar format partitioned by date, applies deduplication and data quality checks with quarantine, protects personal data, produces business tables, and is idempotent and reproducible. It should run with one command and have a README with architecture, results and decisions.'),
    ('Can I build a big data pipeline without a cluster?', 'Yes. The architecture matters more than the size: Python with pyarrow, DuckDB or Polars can process millions of rows on a laptop using the same layers, partitions and quality rules. You can later run the same design on Spark and cloud storage, and explain how it would scale in interviews.'),
    ('What is the medallion architecture?', 'A layered lakehouse design: bronze holds raw data in a better storage format, silver holds cleaned, deduplicated and conformed data, and gold holds aggregated, business-ready tables. Each layer is rebuilt from the previous one, which makes debugging and reprocessing straightforward.'),
    ('How do I make a data pipeline idempotent?', 'Design each step so that re-running it for the same input gives the same result: overwrite the output partition for the processed date, or use MERGE/upsert on a business key, deduplicate inputs, and avoid side effects such as blind appends or sending duplicate notifications. Test it by running the step twice and comparing outputs.'),
    ('What should a data engineering project README include?', 'The problem, an architecture diagram, exact steps to run, the data sources and quality rules, a row reconciliation or validation summary, key design decisions and trade-offs, the results, and limitations with next steps. Add screenshots or sample output and a test or CI badge if available.'),
]

PRACTICE_INTRO = 'Small exercises that extend the capstone. The last two are business-style reviews.'
PROBLEMS = [
    dict(level='easy', title='Partition path', stmt='Print the silver path for date 2026-10-20.', inp='2026-10-20',
         code='''print("lake/silver/orders/date=2026-10-20/part-0.parquet")
''', explain='Consistent paths make partitions easy to read and overwrite.'),
    dict(level='easy', title='Count duplicates', stmt='Print how many duplicates are in ["A", "B", "A", "C", "A"].', inp='IDs',
         code='''ids = ["A", "B", "A", "C", "A"]
print(len(ids) - len(set(ids)))
''', explain='Total minus unique = duplicates.'),
    dict(level='easy', title='Order amount', stmt='qty 3, price 140. Print the amount.', inp='3 × 140',
         code='''print(3 * 140)
''', explain='Derived columns such as amount are computed in silver.'),
    dict(level='medium', title='Failure rate', stmt='18,898 rows after dedup, 100 bad. Print the failure rate to two decimals and the gate decision at 2%.', inp='100 / 18,898',
         code='''r = 100 / 18_898
print(f"{r:.2%}", "continue" if r <= 0.02 else "stop")
''', explain='The gate protects gold from bad batches.'),
    dict(level='medium', title='Reconcile three days', stmt='Raw [20005, 18998, 21429], 150 dupes and 100 bad per day. Print total clean rows.', inp='as given',
         code='''print(sum(r - 150 - 100 for r in [20_005, 18_998, 21_429]))
''', explain='Matches the 59,682 orders in gold.'),
    dict(level='advanced', title='Indian number format', stmt='Print 1117740 with Indian digit grouping (11,17,740).', inp='1117740',
         code='''s = str(1117740)
head, tail = s[:-3], s[-3:]
parts = []
while len(head) > 2:
    parts.insert(0, head[-2:]); head = head[:-2]
print(",".join(([head] if head else []) + parts + [tail]))
''', explain='Lakh/crore grouping: last three digits, then pairs.'),
    dict(level='advanced', title='Latest status wins', stmt='From [("A1","10:00","placed"),("A1","10:30","delivered")], print the latest status.', inp='2 versions',
         code='''rows = [("A1", "10:00", "placed"), ("A1", "10:30", "delivered")]
print(max(rows, key=lambda r: r[1])[2])
''', explain='Upserts keep the most recent version of each key.'),
    dict(level='business', title='Revenue share', stmt='City revenue: Mumbai 11,17,740, Thane 11,05,820, Nashik 10,89,740, Pune 10,82,230. Print Mumbai’s share.', inp='4 cities',
         code='''rev = {"Mumbai": 1117740, "Thane": 1105820, "Nashik": 1089740, "Pune": 1082230}
print(f"{rev['Mumbai'] / sum(rev.values()):.1%}")
''', explain='Gold tables answer business questions like this instantly.'),
    dict(level='business', title='Storage estimate', stmt='In the capstone run, one day (about 20,000 rows) is about 2.9 MB as raw JSON and 0.4 MB as bronze Parquet. Print a year of each in MB and the compression ratio.', inp='2.9 MB vs 0.4 MB per day',
         code='''raw, parquet = 2.9, 0.4
print(f"raw {raw * 365:.0f} MB, bronze {parquet * 365:.0f} MB, {raw / parquet:.1f}x smaller")
''', explain='Measured file sizes from your own run make the best README evidence for choosing Parquet.'),
]

SCN_INTRO = 'Questions reviewers and interviewers ask about capstone projects. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
