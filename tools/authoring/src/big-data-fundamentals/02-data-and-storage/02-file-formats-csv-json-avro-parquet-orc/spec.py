import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='02-data-and-storage', lesson='02-file-formats-csv-json-avro-parquet-orc', n='2.2',
    module_label='Module 2 · Data and Storage',
    title='File formats for big data: CSV, JSON, Avro, Parquet and ORC',
    desc='CSV vs JSON vs Avro vs Parquet vs ORC explained: row vs columnar storage, text vs binary, schemas, compression codecs (gzip, snappy, zstd), splittable files, dictionary and run-length encoding, row groups, predicate pushdown and Avro schema evolution with a Schema Registry. Real size comparison you can run on your PC.',
    og_desc='Why is Parquet 60 times faster than CSV for analytics? See what each format does on disk, and race all five on your own PC.',
    minutes=30, level='Beginner → Advanced',
    lead='The same 10 GB of orders can take four minutes or four seconds to query, depending only on the file format. In this lesson you see how <b>CSV</b>, <b>JSON</b>, <b>Avro</b>, <b>Parquet</b> and <b>ORC</b> lay data out on disk, why columnar formats are so fast for analytics, how Avro lets Kafka messages change safely, and why sorting a table can make queries skip most of it.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Six-format race on your PC'],
)

RUN = dict(
    heading='Row storage vs column storage',
    intro='<p>The same small table is stored row by row and column by column. The program counts how many values each layout must read to answer “total amount for Pune”. Then try the challenges: text vs binary size, dictionary encoding, compression of sorted data, min/max skipping and Avro-style schema evolution.</p>',
    code='''orders = [
    ("O1", "Pune", "thali", 220, "10-19"),
    ("O2", "Thane", "dosa", 150, "10-19"),
    ("O3", "Pune", "chai", 20, "10-20"),
    ("O4", "Mumbai", "lassi", 90, "10-20"),
]
columns = ["order_id", "city", "dish", "amount", "day"]

# Row layout: whole records stored together
row_file = [value for row in orders for value in row]
# Column layout: each column stored together
col_file = {name: [row[i] for row in orders] for i, name in enumerate(columns)}

# Question: total amount for Pune
row_reads = len(row_file)                                   # must read every value
col_reads = len(col_file["city"]) + len(col_file["amount"])  # only 2 columns
total = sum(a for c, a in zip(col_file["city"], col_file["amount"]) if c == "Pune")

print("Values read, row layout   :", row_reads)
print("Values read, column layout:", col_reads)
print("Total for Pune: Rs", total)
''',
    anno=[
        ('row_file = [value for row in orders for value in row]', 'A row format (CSV, JSON, Avro) writes record after record: O1, Pune, thali, 220, …'),
        ('col_file = {name: [row[i] for row in orders] for i, name in enumerate(columns)}', 'A columnar format (Parquet, ORC) keeps each column together: all cities, then all amounts, and so on.'),
        ('col_reads = len(col_file["city"]) + len(col_file["amount"])  # only 2 columns', 'The query touches only <code>city</code> and <code>amount</code>, so a columnar engine reads 2 of the 5 columns.'),
    ],
    tasks=[
        dict(label='1 · Row vs column', hint='Press <b>Run</b>. Add 6 more orders: how do both counts grow? Then change the question to need 3 columns.', code=None),
        dict(label='2 · Text vs binary', hint='The number 4,25,000 as text takes one byte per digit; as a 4-byte binary integer it always takes 4 bytes. Try bigger numbers and see where binary wins.',
             code='''import struct
for n in [7, 220, 425000, 2147483000]:
    text = str(n).encode()
    binary = struct.pack("<i", n)        # 4-byte integer, as in Avro/Parquet
    print(f"{n:>12}: text {len(text)} bytes, binary {len(binary)} bytes")
'''),
        dict(label='3 · Dictionary encoding', hint='A city column with few distinct values becomes a small dictionary plus codes. Add more rows of the same cities: the dictionary doesn\'t grow.',
             code='''city = ["Pune", "Pune", "Thane", "Pune", "Mumbai", "Pune", "Thane", "Pune"]
dictionary = sorted(set(city))
codes = [dictionary.index(c) for c in city]
raw_bytes = sum(len(c) for c in city)
encoded_bytes = sum(len(c) for c in dictionary) + len(codes)   # 1 byte per code
print("dictionary:", dictionary)
print("codes     :", codes)
print("bytes raw :", raw_bytes, "-> encoded:", encoded_bytes)
'''),
        dict(label='4 · Sorted data compresses better', hint='zlib (the algorithm inside gzip) compresses the same column sorted and unsorted. Change the number of rows.',
             code='''import random, zlib
random.seed(1)
cities = [random.choice(["Pune", "Thane", "Mumbai", "Nashik"]) for _ in range(5000)]
unsorted_bytes = ",".join(cities).encode()
sorted_bytes = ",".join(sorted(cities)).encode()
print("raw size          :", len(unsorted_bytes))
print("compressed, mixed :", len(zlib.compress(unsorted_bytes)))
print("compressed, sorted:", len(zlib.compress(sorted_bytes)))
'''),
        dict(label='5 · Skip with min/max (advanced)', hint='Each row group stores the min and max of the <code>amount</code> column. Count how many row groups a query <code>amount &gt; 800</code> must read. Try <code>&gt; 400</code>.',
             code='''row_groups = [[120, 340, 90, 410], [880, 920, 760, 990], [40, 60, 75, 30], [500, 650, 810, 700]]
stats = [(min(g), max(g)) for g in row_groups]
threshold = 800
must_read = [i for i, (lo, hi) in enumerate(stats) if hi > threshold]
print("stats (min, max):", stats)
print("row groups to read:", must_read, "of", len(row_groups))
'''),
        dict(label='6 · Schema evolution (advanced)', hint='Like Avro: a reader with a newer schema reads old records and fills in defaults. Add a field <code>"rating"</code> with default 0.',
             code='''reader_schema = {"order_id": None, "amount": None, "coupon": "NONE"}   # field -> default
old_records = [{"order_id": "O1", "amount": 220}, {"order_id": "O2", "amount": 150}]
new_records = [{"order_id": "O3", "amount": 90, "coupon": "LUNCH20"}]

for rec in old_records + new_records:
    row = {f: rec.get(f, default) for f, default in reader_schema.items()}
    print(row)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: race six file formats',
    intro='<p>This program creates 2 lakh random orders and writes them as CSV, gzipped CSV, JSON lines, Avro, Parquet and ORC, then compares file sizes and answers one question from CSV and from Parquet. First install two libraries: <code>pip install pyarrow fastavro</code>. Save the program as <code>formats_race.py</code> in an empty folder and run it.</p>',
    items=[
        dict(title='Six formats, one table', file='formats_race.py',
             cmd=open(os.path.join(HERE, 'formats_race.py')).read() + '\n# In a terminal:\n#   pip install pyarrow fastavro\n#   python formats_race.py',
             output=open(os.path.join(HERE, 'formats_race.out')).read(),
             note='Recorded from a real run with Python 3.13, pyarrow 26 and fastavro 1.13. Sizes can differ slightly with other library versions, and the speed-up depends on your machine. The data is random, which is the hardest case for compression; real business data (sorted dates, repeated cities) usually compresses much better in Parquet and ORC. Open the <code>formats</code> folder and try opening each file in Notepad: only the CSV and JSON are readable.'),
    ],
)

TRACE = dict(
    heading='Dictionary encoding, one line at a time',
    intro='<p>A city column is encoded the way Parquet does it: each new city is added to the dictionary once, and every value becomes a small code. Watch the dictionary stop growing while the codes list keeps growing.</p>',
    code='''column = ["Pune", "Thane", "Pune", "Pune", "Thane"]
dictionary = []
codes = []
for city in column:
    if city not in dictionary:
        dictionary.append(city)
    codes.append(dictionary.index(city))
print(dictionary, codes)
''',
    notes={1: 'Column :: Values of one column, stored together in a columnar file.',
           6: 'New value :: Only the first time a city appears is it added to the dictionary.',
           7: 'Code :: Each value is replaced by its position in the dictionary.'},
)

WORKED_INTRO = 'Four format decisions, from choosing a format to estimating what min/max statistics save. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Platform design · choosing', title='Pick a format for each job',
         problem='<p>Apply simple rules to choose a format: exports for people → CSV; messages between services → Avro (JSON if the partner can\'t use Avro); tables for analytics → Parquet.</p>',
         inp='monthly report for finance, Kafka order events, partner webhook, lake orders table',
         approach=['Describe each job by who reads it.',
                   'Use if/elif rules to pick a format.',
                   'Print the choice and the reason.'],
         code='''jobs = [("monthly report for finance", "people"), ("Kafka order events", "services"),
        ("partner webhook", "partner"), ("lake orders table", "analytics")]
for job, reader in jobs:
    if reader == "people":
        fmt, why = "CSV", "opens anywhere"
    elif reader == "services":
        fmt, why = "Avro", "compact, typed, schema registry"
    elif reader == "partner":
        fmt, why = "JSON", "every language reads it"
    else:
        fmt, why = "Parquet", "columnar, compressed, skippable"
    print(f"{job:27} -> {fmt:8} ({why})")
''', notes={3: 'Rule 1 :: People open files in Excel; give them CSV.'},
         tryit='Add “ML training data read many times by Spark” and “a config file edited by hand”. Which formats fit?'),
    dict(level='i', tag='Storage · estimation', title='How much bigger is JSON than CSV?',
         problem='<p>Build the CSV line and the JSON line for the same records, measure their sizes, and print how much bigger JSON is for 1 crore records.</p>',
         inp='3 sample records, scale to 1 crore',
         approach=['Make the CSV header plus one line per record.',
                   'Make one JSON object per line with <code>json.dumps</code>.',
                   'Compare average bytes per record and scale up.'],
         code='''import json
records = [{"order_id": "O1", "city": "Pune", "amount": 220},
           {"order_id": "O2", "city": "Thane", "amount": 150},
           {"order_id": "O3", "city": "Mumbai", "amount": 90}]
csv_bytes = sum(len(f"{r['order_id']},{r['city']},{r['amount']}\\n") for r in records)
json_bytes = sum(len(json.dumps(r) + "\\n") for r in records)
per_csv, per_json = csv_bytes / 3, json_bytes / 3
n = 1_00_00_000
print(f"CSV : {per_csv:.1f} bytes/record -> {per_csv * n / 1024**3:.2f} GB")
print(f"JSON: {per_json:.1f} bytes/record -> {per_json * n / 1024**3:.2f} GB")
print(f"JSON is {per_json / per_csv:.1f}x bigger")
''', notes={5: 'CSV :: Just the values and commas.', 6: 'JSON :: Field names and quotes repeat on every record.'},
         tryit='Add two more fields (<code>"dish"</code> and <code>"day"</code>) to every record. Does the ratio grow or shrink?'),
    dict(level='i', tag='Performance · compression', title='Sorted vs unsorted: measure the difference',
         problem='<p>Compress the same column of 10,000 values with zlib, once in random order and once sorted, and report both compression ratios.</p>',
         inp='10,000 cities in random order',
         approach=['Generate the column with a fixed random seed so results repeat.',
                   'Join the values into bytes and compress with <code>zlib.compress</code>.',
                   'Ratio = original size ÷ compressed size.'],
         code='''import random, zlib
random.seed(3)
col = ["Pune", "Thane", "Mumbai", "Nashik", "Nagpur"] * 2000
random.shuffle(col)
for label, values in [("random order", col), ("sorted", sorted(col))]:
    raw = "\\n".join(values).encode()
    packed = zlib.compress(raw)
    print(f"{label:12}: {len(raw)} -> {len(packed)} bytes, ratio {len(raw) / len(packed):.0f}x")
''', notes={6: 'Compress :: The same bytes in a different order compress very differently.'},
         tryit='Try 50 distinct city names instead of 5. Which order helps more now?'),
    dict(level='a', tag='Query engine · predicate pushdown', title='How many bytes does min/max skipping save?',
         problem='<p>A Parquet file has 12 row groups of 128 MB, one per month, with min and max <code>day</code> stored in the footer. A query asks for 3 days in October. How many MB are read with and without skipping?</p>',
         inp='12 row groups × 128 MB, query 2026-10-17 to 2026-10-19',
         approach=['Build the min/max range for each month.',
                   'A row group must be read if its range overlaps the query range.',
                   'Compare bytes read with bytes in the whole file.'],
         code='''import calendar
groups = []
for m in range(1, 13):
    last = calendar.monthrange(2026, m)[1]
    groups.append((f"2026-{m:02d}-01", f"2026-{m:02d}-{last}"))
q_lo, q_hi = "2026-10-17", "2026-10-19"
to_read = [i for i, (lo, hi) in enumerate(groups) if lo <= q_hi and hi >= q_lo]
print("Row groups read:", to_read)
print("MB read with skipping:", len(to_read) * 128)
print("MB read without      :", len(groups) * 128)
''', notes={6: 'Overlap :: Two ranges overlap when each starts before the other ends.'},
         tryit='Ask for 2026-09-28 to 2026-10-03. How many row groups now? Then imagine the file is not sorted by day: every group would span the whole year.'),
]

QUIZ = [
    dict(q='Which of these formats is column-oriented?', options=['CSV', 'JSON', 'Avro', 'Parquet'], answer=3,
         why='<b>Parquet</b> (and ORC) store each column together. CSV, JSON and Avro are row-oriented.'),
    dict(q='Which format is most commonly used for Kafka messages together with a Schema Registry?', options=['CSV', 'Avro', 'ORC', 'Excel'], answer=1,
         why='<b>Avro</b> is compact, row-oriented and supports schema evolution, which suits streaming one record at a time.'),
    dict(q='Why can\'t a large gzipped CSV file be split across many workers?', options=['Gzip files are encrypted', 'Gzip must be decompressed from the start, so there are no safe split points', 'CSV files cannot be compressed', 'Workers can\'t read text'], answer=1,
         why='A plain gzip stream has no independent blocks, so one worker must read it from the beginning. Avro, Parquet and ORC are splittable by design.'),
    dict(q='A query reads 2 columns out of 50 in a large table. Which layout reads the least data?', options=['CSV', 'JSON lines', 'Parquet', 'Plain text log'], answer=2,
         why='A columnar format reads only the 2 needed columns; row formats must read all 50.'),
    dict(q='What does Parquet store in its footer that allows predicate pushdown?', options=['A copy of every row', 'The schema and min/max statistics for each column chunk', 'The password', 'The query history'], answer=1,
         why='Engines read the footer first and skip row groups whose min–max range can\'t match the filter.'),
    dict(q='Which Avro schema change is safe for existing readers?', options=['Removing a required field', 'Changing a field from int to string', 'Adding a new field with a default value', 'Renaming a field without an alias'], answer=2,
         why='Adding a field with a <b>default</b> is backward compatible: readers fill the default for old records.'),
    dict(q='Storing “Pune” once and replacing every occurrence with a small number is called:', options=['Run-length encoding', 'Dictionary encoding', 'Hashing', 'Partitioning'], answer=1,
         why='<b>Dictionary encoding</b>. Run-length encoding instead stores repeated values as (value, count).'),
    dict(q='Why does sorting a table before writing Parquet often make queries faster?', options=['Sorted files are always smaller than 1 MB', 'Row groups get narrow min/max ranges, so more can be skipped, and runs compress better', 'Sorting removes duplicate rows', 'Parquet cannot store unsorted data'], answer=1,
         why='Sorted data gives each row group a tight range of values (better skipping) and long runs of equal values (better compression).'),
]

REVISION = [
    '<b>Row-oriented</b>: CSV, JSON, Avro. <b>Column-oriented</b>: Parquet, ORC.',
    '<b>Text</b>: CSV, JSON (readable, large, no types). <b>Binary</b>: Avro, Parquet, ORC (compact, typed, schema inside).',
    'Use: CSV for people, JSON for APIs, <b>Avro</b> for Kafka/streams, <b>Parquet</b> for analytics and lakes, ORC for Hive.',
    'Codecs: gzip (small, slow), snappy/lz4 (fast), zstd (balanced). Gzipped CSV is <b>not splittable</b>.',
    'Parquet: row groups → column chunks → pages; footer with schema + min/max → <b>predicate pushdown</b>.',
    'Encodings: dictionary, run-length, bit-packing, delta. Sorting improves skipping and compression.',
    'Avro evolution: add fields with defaults; never remove required fields or change types. Enforce with a Schema Registry.',
]
FAQ = [
    ('Compare CSV, JSON, Avro, Parquet and ORC.', 'CSV and JSON are row-oriented text formats: human-readable and universal, but large, untyped and slow to parse; JSON supports nesting. Avro is a row-oriented binary format with an embedded schema and strong schema-evolution support, ideal for streaming and Kafka. Parquet and ORC are column-oriented binary formats with embedded schemas, per-column compression and encodings, and statistics for skipping data; they are best for analytical queries in lakes, lakehouses and warehouses. Parquet is the common default in Spark and the cloud; ORC is popular in Hive.'),
    ('Why are columnar formats better for analytics?', 'Analytical queries usually read a few columns of many rows. Columnar formats read only those columns, store values of one type together so they compress and encode very well, and keep statistics per block so whole blocks can be skipped. Row formats must read and parse every column of every row.'),
    ('When should you not use Parquet?', 'When writing or reading single records with low latency (streaming messages, OLTP), when data is tiny, when frequent row-level updates are needed without a table format like Delta or Iceberg, and when people need to open files directly. Use Avro, JSON, a database or CSV in those cases.'),
    ('What does “splittable” mean and why does it matter?', 'A splittable file can be divided into independent pieces that different workers process in parallel. Big data engines rely on this for speed. Avro, Parquet, ORC and uncompressed or block-compressed text are splittable; a single large gzip file is not, so one worker must read it all.'),
    ('What is predicate pushdown?', 'Pushing a query\'s filter conditions down to the storage layer so that data which cannot match is skipped before being read. In Parquet and ORC, the engine compares the filter with min/max statistics in the file metadata and skips whole row groups or stripes, and with partitioned tables it skips whole folders.'),
]

PRACTICE_INTRO = 'Format and encoding exercises. The last two are business tasks about storage cost and query cost.'
PROBLEMS = [
    dict(level='easy', title='Row to columns', stmt='Turn a list of rows into a dictionary of columns.', inp='(O1, Pune, 220), (O2, Thane, 150)',
         code='''rows = [("O1", "Pune", 220), ("O2", "Thane", 150)]
names = ["id", "city", "amount"]
cols = {n: [r[i] for r in rows] for i, n in enumerate(names)}
print(cols)
''', explain='This is the reorganisation a columnar format does when it writes data.'),
    dict(level='easy', title='Bytes of a CSV line', stmt='Print the number of bytes in the CSV line and in the JSON version of the same record.', inp='O1, Pune, 220',
         code='''import json
csv_line = "O1,Pune,220\\n"
json_line = json.dumps({"id": "O1", "city": "Pune", "amount": 220}) + "\\n"
print(len(csv_line), len(json_line))
''', explain='Field names and quotes make JSON larger than CSV.'),
    dict(level='easy', title='Pick a codec', stmt='Print the codec for each need: fastest → snappy, smallest → gzip, balanced → zstd.', inp='fastest, smallest, balanced',
         code='''codec = {"fastest": "snappy", "smallest": "gzip", "balanced": "zstd"}
for need in ["fastest", "smallest", "balanced"]:
    print(need, "->", codec[need])
''', explain='A simple lookup; in real projects zstd is increasingly the default.'),
    dict(level='medium', title='Run-length encode', stmt='Encode the sorted column as (value, count) pairs.', inp='A A A B B C A A',
         code='''col = ["A", "A", "A", "B", "B", "C", "A", "A"]
runs = []
for v in col:
    if runs and runs[-1][0] == v:
        runs[-1] = (v, runs[-1][1] + 1)
    else:
        runs.append((v, 1))
print(runs)
''', explain='Runs break when the value changes; sorting first would merge the two runs of A.'),
    dict(level='medium', title='Decode a dictionary column', stmt='Rebuild the original column from a dictionary and codes.', inp='dictionary [Mumbai, Pune, Thane], codes [1,1,2,0,1]',
         code='''dictionary = ["Mumbai", "Pune", "Thane"]
codes = [1, 1, 2, 0, 1]
print([dictionary[c] for c in codes])
''', explain='Readers reverse the encoding by looking each code up in the dictionary.'),
    dict(level='advanced', title='Row groups that match a filter', stmt='Given min/max of amount per row group, print the groups a query for amount between 500 and 600 must read.', inp='(100,450), (480,700), (20,90), (590,990)',
         code='''stats = [(100, 450), (480, 700), (20, 90), (590, 990)]
lo, hi = 500, 600
print([i for i, (a, b) in enumerate(stats) if a <= hi and b >= lo])
''', explain='A group is read only if its [min, max] range overlaps the query range.'),
    dict(level='advanced', title='Compatible schema change?', stmt='A new schema adds and removes fields. Print “compatible” only if every removed field had a default and every added field has a default.', inp='old: id, amount, note(default) · new: id, amount, coupon(default)',
         code='''old = {"id": None, "amount": None, "note": ""}      # field -> default (None = required)
new = {"id": None, "amount": None, "coupon": "NONE"}
removed = [f for f in old if f not in new]
added = [f for f in new if f not in old]
ok = all(old[f] is not None for f in removed) and all(new[f] is not None for f in added)
print("removed:", removed, "added:", added)
print("compatible" if ok else "INCOMPATIBLE")
''', explain='A simplified version of the checks a Schema Registry runs for full compatibility.'),
    dict(level='business', title='Storage saving from Parquet', stmt='The lake holds 80 TB of CSV. Parquet stores it in about a quarter of the space. Storage costs Rs 1,800 per TB per month. Print the yearly saving.', inp='80 TB, 25%, Rs 1,800/TB-month',
         code='''csv_tb = 80
parquet_tb = csv_tb * 0.25
saving = (csv_tb - parquet_tb) * 1800 * 12
print("Parquet size:", parquet_tb, "TB")
print("Yearly saving: Rs", int(saving))
''', explain='Format choice is also a cost decision, before even counting faster queries.'),
    dict(level='business', title='Pay-per-scan query cost', stmt='A dashboard query runs 300 times a day. On CSV it scans 600 GB; on partitioned Parquet it scans 4 GB. At Rs 400 per TB scanned, print the monthly cost of each.', inp='600 GB vs 4 GB, 300/day, Rs 400/TB',
         code='''runs = 300 * 30
for name, gb in [("CSV", 600), ("Parquet", 4)]:
    cost = gb / 1024 * 400 * runs
    print(f"{name:8} Rs {cost:,.0f} per month")
''', explain='Engines that bill per byte scanned reward columnar formats and partitioning directly. (Rates are illustrative.)'),
]

SCN_INTRO = 'Format decisions you will face in real data teams. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
