import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='03-data-lake-vs-data-warehouse', n='4.3',
    module_label='Module 4 · The Ecosystem',
    title='Data lake vs data warehouse (and the lakehouse)',
    desc='Data lake vs data warehouse vs lakehouse: schema-on-read vs schema-on-write, ETL vs ELT, bronze/silver/gold zones, star schema, Parquet, partitioning and the data swamp. Beginner to Advanced, real-time animations, Python simulations and a mini lake + SQL warehouse you build on your PC.',
    og_desc='Library or godown? Build a tiny data lake and warehouse in Python and see when each one wins, and why lakehouses exist.',
    minutes=28, level='Beginner → Advanced',
    lead='Finance wants one trusted number; data scientists want every raw click, review and photo. A <b>data warehouse</b> serves the first, a <b>data lake</b> the second, and a <b>lakehouse</b> tries to serve both from one copy of data. In this lesson you watch a messy record get refined from bronze to gold, see a lake turn into a swamp, and build a small lake and warehouse on your own computer.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Mini lake + SQL on your PC'],
)

RUN = dict(
    heading='Schema-on-write vs schema-on-read',
    intro='<p>The same four order rows go to two places. The <b>warehouse</b> checks every row against a schema before storing it; the <b>lake</b> stores everything as it is. Later, someone reads the lake and applies their own rules. Compare which rows survive where. Then try the challenges: medallion zones, a star schema, columnar storage, partitions and schema changes.</p>',
    code='''rows = [
    {"order_id": 1, "kitchen": "K11", "amount": 120},
    {"order_id": 2, "kitchen": "K12", "amount": "250"},                    # text, not a number
    {"order_id": 3, "kitchen": "K13", "amount": -90},                      # impossible value
    {"order_id": 4, "kitchen": "K11", "amount": 120, "coupon": "LUNCH20"}, # new column
]
SCHEMA = {"order_id": int, "kitchen": str, "amount": int}

def warehouse_load(row):                    # schema-on-WRITE: check before saving
    extra = set(row) - set(SCHEMA)
    if extra:
        return f"REJECTED: unknown column {sorted(extra)}"
    for col, typ in SCHEMA.items():
        if not isinstance(row[col], typ):
            return f"REJECTED: {col} is not {typ.__name__}"
    if row["amount"] <= 0:
        return "REJECTED: amount must be > 0"
    return "stored"

lake = []
def lake_store(row):                        # schema-on-READ: store anything now
    lake.append(row)
    return "stored as-is"

for r in rows:
    print(f"order {r['order_id']}: warehouse -> {warehouse_load(r):36} lake -> {lake_store(r)}")

# Later, an analyst READS the lake and applies a schema for their own question
revenue = sum(int(r["amount"]) for r in lake if int(r["amount"]) > 0)
print("Revenue read from the lake (cleaned while reading): Rs", revenue)
''',
    anno=[
        ('SCHEMA = {"order_id": int, "kitchen": str, "amount": int}', 'The warehouse\'s contract: exactly these columns, with these types.'),
        ('extra = set(row) - set(SCHEMA)', 'A new <code>coupon</code> column is rejected: strict schemas protect quality but make change slower.'),
        ('lake.append(row)', 'The lake keeps every row, even broken ones. Nothing is lost, but nothing is checked either.'),
        ('int(r["amount"]) for r in lake if int(r["amount"]) > 0', 'Schema-on-read: the reader converts types and filters bad rows <b>at query time</b>, for this question only.'),
    ],
    tasks=[
        dict(label='1 · Write vs read', hint='Press <b>Run</b>. Then add <code>"coupon"</code> to <code>SCHEMA</code> as <code>str</code>. Why does order 4 still fail? (Hint: rows without a coupon.) This is the schema-evolution problem.', code=None),
        dict(label='2 · Medallion zones', hint='Bronze keeps raw rows, silver de-duplicates and fixes types, gold aggregates. Add an order for K13 and see it flow through all three.',
             code='''bronze = [
    {"order_id": 1, "kitchen": "K11", "amount": "120"},
    {"order_id": 2, "kitchen": "K12", "amount": "250"},
    {"order_id": 2, "kitchen": "K12", "amount": "250"},       # duplicate
    {"order_id": 3, "kitchen": "K11", "amount": "90"},
]
silver, seen = [], set()
for r in bronze:
    if r["order_id"] not in seen:
        seen.add(r["order_id"])
        silver.append({**r, "amount": int(r["amount"])})
gold = {}
for r in silver:
    gold[r["kitchen"]] = gold.get(r["kitchen"], 0) + r["amount"]
print("bronze:", len(bronze), "rows")
print("silver:", len(silver), "rows")
print("gold  :", gold)
'''),
        dict(label='3 · Star schema', hint='A fact table of orders and a dimension table of kitchens. Join them to get revenue by city. Add a <code>dim_date</code> dictionary and report revenue by weekday too.',
             code='''fact_orders = [("K11", 120), ("K12", 250), ("K13", 90), ("K11", 140), ("K12", 60)]
dim_kitchen = {"K11": {"name": "Annapurna", "city": "Pune"},
               "K12": {"name": "Spice Box", "city": "Pune"},
               "K13": {"name": "Udupi Corner", "city": "Mumbai"}}

by_city = {}
for kitchen, amount in fact_orders:
    city = dim_kitchen[kitchen]["city"]          # the join
    by_city[city] = by_city.get(city, 0) + amount
print(by_city)
'''),
        dict(label='4 · Rows vs columns', hint='A query needs 2 of 20 columns. A row format reads whole rows; a columnar format reads only the needed columns. Try a query that needs 5 columns.',
             code='''rows, columns = 10_000_000, 20
bytes_per_value = 8
needed = 2

row_format = rows * columns * bytes_per_value
columnar = rows * needed * bytes_per_value
print("Row format (CSV) reads :", row_format / 1024**3, "GB")
print("Columnar (Parquet) reads:", columnar / 1024**3, "GB")
print("Saving:", columns // needed, "times less data")
'''),
        dict(label='5 · Partition pruning', hint='Files are stored in one folder per day. A query for 3 days only opens those folders. Change the query to a whole month.',
             code='''import datetime
start = datetime.date(2026, 1, 1)
folders = [f"date={start + datetime.timedelta(days=d)}" for d in range(365)]
wanted = {"date=2026-10-17", "date=2026-10-18", "date=2026-10-19"}

scanned = [f for f in folders if f in wanted]
print("Folders in table:", len(folders))
print("Folders scanned :", len(scanned), scanned)
'''),
        dict(label='6 · Schema evolution (advanced)', hint='New rows have a <code>coupon</code> column; old ones don\'t. Table formats like Delta and Iceberg handle this by adding the column and filling old rows with null. Add a second new column.',
             code='''old_rows = [{"order_id": 1, "amount": 120}, {"order_id": 2, "amount": 250}]
new_rows = [{"order_id": 3, "amount": 90, "coupon": "LUNCH20"}]

columns = []
for r in old_rows + new_rows:
    for c in r:
        if c not in columns:
            columns.append(c)
table = [{c: r.get(c) for c in columns} for r in old_rows + new_rows]
print("Schema:", columns)
for row in table:
    print(row)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: build a mini lake and a SQL warehouse',
    intro='<p>This program creates a real folder-based data lake (<code>lake/bronze</code>, <code>lake/silver</code>), then a real SQL warehouse using <b>SQLite</b>, which comes built into Python. The warehouse table has a <code>CHECK</code> rule, so it rejects the impossible order at load time, while the lake kept it. Save it as <code>mini_lake.py</code> in an empty folder and run it; then open the folders it creates.</p>',
    items=[
        dict(title='Bronze → silver → SQL warehouse', file='mini_lake.py',
             cmd=open(os.path.join(HERE, 'mini_lake.py')).read() + '\n# In a terminal:  python mini_lake.py',
             output=open(os.path.join(HERE, 'mini_lake.out')).read(),
             note='Recorded from a real run with Python 3.10 and its built-in SQLite. The wording of the rejection message can differ slightly with older SQLite versions. Notice: the bronze file still contains all 5 raw events including the duplicate and the −90 order, silver fixed types and removed the duplicate but did not judge the −90 amount, and only the warehouse\'s schema-on-write rule stopped it. Mumbai has no revenue because its only order was rejected.'),
    ],
)

TRACE = dict(
    heading='Bronze to gold, one line at a time',
    intro='<p>Three raw rows (one duplicate) move through the zones. Watch the <code>seen</code> set block the duplicate, the amount change from text to a number in silver, and the gold dictionary fill up.</p>',
    code='''bronze = [("O1", "Pune", "120"), ("O2", "Pune", "250"), ("O2", "Pune", "250")]
seen, silver = set(), []
for oid, city, amount in bronze:
    if oid in seen:
        continue
    seen.add(oid)
    silver.append((oid, city, int(amount)))
gold = {}
for oid, city, amount in silver:
    gold[city] = gold.get(city, 0) + amount
print(gold)
''',
    notes={1: 'Bronze :: Raw rows, exactly as received: a duplicate and amounts stored as text.',
           2: 'Silver setup :: <code>seen</code> remembers order ids already kept.',
           (4, 3): 'Duplicate :: O2 is already in <code>seen</code>, so this copy is skipped.',
           8: 'Gold :: An aggregate table, ready for the finance dashboard.'},
)

WORKED_INTRO = 'Four tasks a data engineer does with lakes and warehouses, from deciding where data goes to estimating query savings. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Platform design · first step', title='Where should each dataset go?',
         problem='<p>Route each dataset to the lake, the warehouse or both. Rules: unstructured data → lake only; structured data needed for reports → both (raw in lake, clean in warehouse); everything else → lake.</p>',
         inp='orders (structured, report), clicks (semi), reviews (unstructured), photos (unstructured), payments (structured, report)',
         approach=['Describe each dataset with its kind and whether reports need it.',
                   'Apply the rules in order with if/elif.',
                   'Print the destination.'],
         code='''datasets = [("orders", "structured", True), ("clicks", "semi", False),
            ("reviews", "unstructured", False), ("photos", "unstructured", False),
            ("payments", "structured", True)]
for name, kind, for_reports in datasets:
    if kind == "unstructured":
        where = "lake"
    elif kind == "structured" and for_reports:
        where = "lake (raw) + warehouse (clean)"
    else:
        where = "lake"
    print(f"{name:9} -> {where}")
''', notes={4: 'Rule 1 :: Images and free text don\'t fit warehouse tables.'},
         tryit='Add “rider GPS pings” (semi-structured). The logistics team now wants a weekly distance report from them. Where should a clean copy go?'),
    dict(level='i', tag='Data engineering · silver zone', title='Keep the latest version of each record',
         problem='<p>The bronze zone receives order <b>updates</b>: the same order can appear several times as its status changes. Silver must keep only the latest version of each order (by update time).</p>',
         inp='O1 placed@10, O1 delivered@40, O2 placed@15, O1 refunded@90, O2 delivered@50',
         approach=['Walk through the bronze rows.',
                   'Keep a dictionary order_id → latest row.',
                   'Replace the stored row whenever a newer one appears.'],
         code='''bronze = [("O1", "placed", 10), ("O1", "delivered", 40), ("O2", "placed", 15),
          ("O1", "refunded", 90), ("O2", "delivered", 50)]
latest = {}
for oid, status, ts in bronze:
    if oid not in latest or ts > latest[oid][1]:
        latest[oid] = (status, ts)
for oid, (status, ts) in latest.items():
    print(oid, status, "at", ts)
''', notes={5: 'Upsert :: Insert if new, update if newer. Table formats call this MERGE.'},
         tryit='Add an older update for O2 (“placed” at 5) at the end. Does it overwrite the newer status? It shouldn\'t.'),
    dict(level='i', tag='BI · star schema', title='Revenue by city and weekday from a star schema',
         problem='<p>The fact table stores (kitchen, date_key, amount). Dimension tables give each kitchen\'s city and each date_key\'s weekday. Produce revenue per (city, weekday).</p>',
         inp='5 facts, 3 kitchens, 2 dates',
         approach=['Look up the city in <code>dim_kitchen</code> and the weekday in <code>dim_date</code> for each fact.',
                   'Use the pair (city, weekday) as a dictionary key.',
                   'Add up the amounts.'],
         code='''fact = [("K11", 1, 120), ("K12", 1, 250), ("K13", 2, 90), ("K11", 2, 140), ("K12", 2, 60)]
dim_kitchen = {"K11": "Pune", "K12": "Pune", "K13": "Mumbai"}
dim_date = {1: "Sat", 2: "Sun"}

result = {}
for kitchen, date_key, amount in fact:
    key = (dim_kitchen[kitchen], dim_date[date_key])
    result[key] = result.get(key, 0) + amount
for (city, day), revenue in sorted(result.items()):
    print(city, day, revenue)
''', notes={7: 'Join :: Two lookups turn ids into business words.'},
         tryit='Add <code>dim_date</code> entries for 3 and 4 (Mon, Tue) and facts for those days.'),
    dict(level='a', tag='Cost optimisation · file layout', title='How much does layout save on a pay-per-scan engine?',
         problem='<p>A table holds 365 days × 3 GB of CSV. A query needs one month (31 days) and 2 of 20 columns. Parquet compresses to one third. At Rs 400 per TB scanned (illustrative), what does the query cost with each layout?</p>',
         inp='365 × 3 GB, 31 days, 2/20 columns, compression 3×, Rs 400/TB',
         approach=['CSV, no partitions: everything is scanned.',
                   'Partitioned CSV: only 31 days.',
                   'Partitioned Parquet: 31 days × 2/20 columns ÷ 3 compression.'],
         code='''day_gb, rate_per_tb = 3, 400
layouts = {
    "CSV, one folder":       365 * day_gb,
    "CSV, by date":          31 * day_gb,
    "Parquet, by date":      31 * day_gb * (2 / 20) / 3,
}
for name, gb in layouts.items():
    print(f"{name:18} scans {gb:7.1f} GB  costs Rs {gb / 1024 * rate_per_tb:7.2f}")
''', notes={2: 'Layouts :: Same data, three ways of storing it.'},
         tryit='Run this query 500 times a day from a dashboard. Multiply each cost by 500 × 30 to see the monthly difference.'),
]

QUIZ = [
    dict(q='Beginner: Which stores raw images, JSON logs and tables together in their original format?', options=['Data warehouse', 'Data lake', 'OLTP database', 'Spreadsheet'], answer=1,
         why='A data lake stores raw data of any format; a warehouse stores structured, cleaned tables.'),
    dict(q='Beginner: Finance needs a trusted, repeatable monthly revenue report. The best source is…', options=['Raw files in the lake', 'Curated warehouse (or gold) tables', 'Kafka topics', 'Application logs'], answer=1,
         why='Curated warehouse or gold tables are cleaned, checked and modelled for exactly these questions.'),
    dict(q='Beginner: A data lake with no catalogue, owners or quality checks is called a…', options=['Lakehouse', 'Data mart', 'Data swamp', 'Data mesh'], answer=2,
         why='Without metadata and governance, a lake becomes a <b>data swamp</b>.'),
    dict(q='Intermediate: “Check the structure before storing; reject rows that don\'t fit” describes…', options=['Schema-on-read', 'Schema-on-write', 'Partitioning', 'Replication'], answer=1,
         why='Warehouses enforce the schema at load time: <b>schema-on-write</b>.'),
    dict(q='Intermediate: In a star schema, the table holding order amounts and keys is the…', options=['Dimension table', 'Fact table', 'Staging table', 'Lookup cache'], answer=1,
         why='Facts hold measurable events (amounts, quantities) and keys to dimensions such as kitchen and date.'),
    dict(q='Intermediate: Which medallion zone is never edited and keeps data exactly as received?', options=['Bronze', 'Silver', 'Gold', 'Platinum'], answer=0,
         why='<b>Bronze</b> is the raw zone, kept so everything can be reprocessed.'),
    dict(q='Advanced: Why are Parquet files faster than CSV for analytics?', options=['They are always smaller than 1 MB', 'They are columnar and compressed, so queries read only needed columns', 'They store data as images', 'They cannot be partitioned'], answer=1,
         why='Columnar layout plus compression and per-column statistics mean far fewer bytes are read.'),
    dict(q='Advanced: What do Delta Lake and Apache Iceberg add to files in a lake?', options=['A web interface', 'ACID transactions, schema evolution and time travel', 'Automatic image recognition', 'Streaming from Kafka only'], answer=1,
         why='Open table formats keep a transaction log over Parquet files, giving warehouse-like features: the lakehouse.'),
]

REVISION = [
    '<b>Warehouse:</b> structured, cleaned, schema-on-write, fast trusted SQL, for business reporting.',
    '<b>Lake:</b> any format, raw, schema-on-read, cheapest storage, for exploration and ML.',
    '<b>Lakehouse:</b> lake storage + table formats (Delta, Iceberg, Hudi): ACID, MERGE, schema evolution, time travel.',
    '<b>ETL</b> (transform before loading) vs <b>ELT</b> (load raw, transform inside the platform).',
    'Zones: <b>bronze</b> (raw) → <b>silver</b> (clean) → <b>gold</b> (business-ready).',
    '<b>Star schema:</b> fact table + dimension tables. Formats: CSV/JSON (simple), Avro (streams), Parquet/ORC (analytics).',
    'No catalogue = <b>data swamp</b>. Partition + columnar formats = far less data scanned.',
]
FAQ = [
    ('Differentiate a data lake and a data warehouse.', 'A data warehouse stores structured, cleaned and integrated data in a predefined schema (schema-on-write), optimised for SQL reporting and BI, at higher storage cost. A data lake stores raw data of any format (structured, semi-structured, unstructured) in native form on cheap storage, applying structure when read (schema-on-read). Warehouses serve business analysts with trusted numbers; lakes serve data engineers and scientists exploring raw data and training models.'),
    ('What is schema-on-read vs schema-on-write?', 'Schema-on-write defines and enforces the structure before data is stored, rejecting non-conforming rows; queries are fast and data is trusted, but changes are slower. Schema-on-read stores data as-is and applies a structure at query time; it is flexible and keeps everything, but every reader must handle quality issues.'),
    ('What is a lakehouse?', 'An architecture that adds warehouse capabilities (ACID transactions, schema enforcement and evolution, updates and deletes, time travel, performance optimisations and governance) on top of low-cost lake storage, using open table formats such as Delta Lake, Apache Iceberg or Apache Hudi. It lets BI and machine learning use one copy of the data.'),
    ('What is the medallion architecture?', 'A way of organising a lake or lakehouse in zones of increasing quality: bronze holds raw data as ingested, silver holds cleaned, de-duplicated and conformed data, and gold holds aggregated, business-ready tables for reporting.'),
    ('What is a star schema?', 'A dimensional model with a central fact table containing measurable events and foreign keys, surrounded by dimension tables describing them (date, product, customer, location). It simplifies and speeds up analytical queries and is the standard design for data warehouses.'),
]

PRACTICE_INTRO = 'Storage and modelling exercises, from file counting to schema evolution. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Count files by format', stmt='Count the files in a lake listing by extension.', inp='a.json, b.json, c.parquet, d.jpg, e.parquet, f.parquet',
         code='''files = ["a.json", "b.json", "c.parquet", "d.jpg", "e.parquet", "f.parquet"]
count = {}
for f in files:
    ext = f.rsplit(".", 1)[1]
    count[ext] = count.get(ext, 0) + 1
print(count)
''', explain='<code>rsplit(".", 1)</code> splits once from the right, giving the extension.'),
    dict(level='easy', title='Required columns present?', stmt='A warehouse needs order_id, kitchen and amount. Print whether each incoming row has all of them.', inp='3 rows',
         code='''required = {"order_id", "kitchen", "amount"}
rows = [{"order_id": 1, "kitchen": "K1", "amount": 9},
        {"order_id": 2, "amount": 5},
        {"order_id": 3, "kitchen": "K2", "amount": 7, "note": "x"}]
for r in rows:
    print(r["order_id"], "OK" if required <= set(r) else "MISSING " + str(required - set(r)))
''', explain='<code>required &lt;= set(r)</code> checks that every required column is present (extra columns are allowed here).'),
    dict(level='easy', title='Lake vs warehouse storage cost', stmt='Storing 50 TB costs Rs 1,800 per TB-month in a lake and Rs 2,300 per TB-month in a warehouse (illustrative). Print the monthly cost of each.', inp='50 TB',
         code='''tb = 50
print("Lake      : Rs", tb * 1800)
print("Warehouse : Rs", tb * 2300)
''', explain='Raw history usually stays in the cheaper lake; only curated tables go to the warehouse.'),
    dict(level='medium', title='Build partition paths', stmt='Given order dates, print the folder each order belongs to, using the pattern <code>orders/date=YYYY-MM-DD/</code>.', inp='2026-10-19, 2026-10-20',
         code='''for d in ["2026-10-19", "2026-10-20", "2026-10-19"]:
    print(f"orders/date={d}/")
''', explain='Hive-style <code>key=value</code> folder names let engines skip partitions they don\'t need.'),
    dict(level='medium', title='Latest status per order', stmt='Keep only the latest status of each order (higher version wins).', inp='(O1,v1,placed), (O1,v2,delivered), (O2,v1,placed)',
         code='''updates = [("O1", 1, "placed"), ("O1", 2, "delivered"), ("O2", 1, "placed")]
latest = {}
for oid, version, status in updates:
    if oid not in latest or version > latest[oid][0]:
        latest[oid] = (version, status)
print({oid: s for oid, (v, s) in latest.items()})
''', explain='This is an upsert: what MERGE INTO does in a lakehouse table.'),
    dict(level='advanced', title='Merge two schemas', stmt='Rows from an old and a new app version have different columns. Print the merged column list and the rows with missing values as None.', inp='old: id, amount · new: id, amount, coupon',
         code='''rows = [{"id": 1, "amount": 120}, {"id": 2, "amount": 90, "coupon": "C10"}]
cols = []
for r in rows:
    cols += [c for c in r if c not in cols]
print(cols)
for r in rows:
    print([r.get(c) for c in cols])
''', explain='Schema evolution: add new columns and fill old rows with null instead of failing the load.'),
    dict(level='advanced', title='The small-files problem', stmt='A streaming job wrote 50,000 files of 100 KB each. How many 128 MB files would hold the same data after compaction?', inp='50,000 × 100 KB, target 128 MB',
         code='''import math
total_kb = 50_000 * 100
target_kb = 128 * 1024
print("Total:", round(total_kb / 1024 / 1024, 2), "GB")
print("After compaction:", math.ceil(total_kb / target_kb), "files")
''', explain='Every file has opening overhead; thousands of tiny files slow queries. Table formats run compaction to fix this.'),
    dict(level='business', title='Revenue by city (star schema)', stmt='Using the fact and dimension below, print revenue by city.', inp='facts: K1 300, K2 200, K1 100 · K1 in Pune, K2 in Nashik',
         code='''facts = [("K1", 300), ("K2", 200), ("K1", 100)]
dim = {"K1": "Pune", "K2": "Nashik"}
rev = {}
for k, amt in facts:
    rev[dim[k]] = rev.get(dim[k], 0) + amt
print(rev)
''', explain='The same join a BI tool sends to the warehouse when you drag “city” onto a chart.'),
    dict(level='business', title='Retention plan', stmt='Bronze grows 200 GB/day and is kept 90 days; gold grows 2 GB/day and is kept 3 years. Print the steady-state size of each in TB.', inp='bronze 200 GB × 90 d · gold 2 GB × 1095 d',
         code='''bronze_tb = 200 * 90 / 1024
gold_tb = 2 * 1095 / 1024
print("Bronze:", round(bronze_tb, 1), "TB")
print("Gold  :", round(gold_tb, 1), "TB")
''', explain='Raw data is large but often kept for a shorter time; small curated tables can be kept for years.'),
]

SCN_INTRO = 'Lake and warehouse decisions you will face in real teams. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
