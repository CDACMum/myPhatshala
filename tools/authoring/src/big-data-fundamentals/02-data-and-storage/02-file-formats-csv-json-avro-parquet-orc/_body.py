import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = box(14, 22, 190, 112, 'card') + t(109, 42, 'orders.csv · 10 GB', 10, bold=True, mono=True)
sc += ''.join(t(26, 62 + k * 14, ln, 8.2, 'ink2', anchor='start', mono=True) for k, ln in enumerate(['O1,Pune,thali,220,…', 'O2,Thane,dosa,150,…', 'O3,Pune,chai,20,…', '… 12 crore rows']))
sc += t(109, 126, 'load time: 4 min, every time', 8.6, 'red', bold=True)
sc += arrow(212, 78, 250, 78, 'ink3', 2) + t(231, 66, 'rewrite', 8.2, 'ink3')
sc += box(258, 22, 368, 112, 'green')
for k, (c, w) in enumerate([('order_id', 60), ('city', 50), ('dish', 56), ('amount', 60), ('day', 56)]):
    x = 272 + k * 70
    hl = c in ('city', 'amount')
    sc += fill(x, 64, 60, 42, 'green' if hl else 'grey', rx=4, opacity=None if hl else .6) + t(x + 30, 58, c, 8.4, 'green' if hl else 'ink3', bold=hl, mono=True)
sc += t(442, 40, 'orders.parquet · 1.8 GB · columns stored together', 9, bold=True, extra='')
sc += t(442, 124, 'query reads only city + amount: 4 seconds', 8.6, 'green', bold=True)
scene_svg = scene('A 10 GB CSV that takes four minutes to load, rewritten as a 1.8 GB Parquet file where a query reads only two columns in four seconds.', sc,
                  'Same data, different layout on disk: <tspan font-weight="700" class="s-acc">sixty times less waiting</tspan>.')

story = f'''  <div class="story">
    <p class="narration">For his practice project Kabir now has a bigger file: ten months of TiffinGo orders, a 10 GB CSV. Every time he restarts his notebook, loading it takes four minutes. He asks a senior engineer at TiffinGo for help. The reply is one line: <i>“Convert it to Parquet.”</i> He does, and the same question now takes four seconds.</p>

{scene_svg}

K> Sir, it’s the same data. How can a different file type make it sixty times faster? Is Parquet some kind of magic?
A> No magic, Kabir, just a smarter layout. A CSV stores data <b>row by row</b> as plain text. Parquet stores it <b>column by column</b>, in binary, compressed, with a small index at the end. Your question needed only two of the columns, so it read only those two.
R> Then why does anyone still use CSV?
A> Because anyone can open a CSV, even in Notepad. Every format is a trade-off between being easy for people, fast to write, fast to read and safe when the data changes. Today you’ll meet the five formats you’ll see in every big data job: <b>CSV</b>, <b>JSON</b>, <b>Avro</b>, <b>Parquet</b> and <b>ORC</b>.
K> And how do I choose?
A> One question first: will this file be <i>written</i> one record at a time, or <i>read</i> many times by analysts? You’ll see why that question decides almost everything.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> File formats at three levels
L1> Five ways to keep a register
      <ul>
        <li><b>CSV</b> is a handwritten register: one line per order, values separated by commas. Anyone can read it, but there are no data types and no rules.</li>
        <li><b>JSON</b> is the same register where every value carries a label: <code>"city": "Pune"</code>. Clear, but the labels repeat on every line, so files get big.</li>
        <li><b>Avro</b> is a printed form book: the form template (the <b>schema</b>) is printed once on the first page, and each record just fills in the boxes in compact binary.</li>
        <li><b>Parquet</b> and <b>ORC</b> reorganise the register by column: all dates on one page, all cities on the next, all amounts on another. To add up amounts, you open just one page.</li>
      </ul>
      <p><b>Simple rule:</b> sharing a small file with a person → CSV. Sending messages between apps → JSON or Avro. Storing big tables for analysis → Parquet (or ORC).</p>
L2> Row vs column, text vs binary, compression and splitting
      <ul>
        <li><b>Row-oriented</b> (CSV, JSON, Avro): a whole record is stored together. Great for writing one record at a time and reading whole records.</li>
        <li><b>Column-oriented</b> (Parquet, ORC): each column is stored together. Great for analytics that read a few columns of many rows; values in one column are similar, so they compress far better.</li>
        <li><b>Text vs binary:</b> CSV and JSON are text (numbers stored as characters); Avro, Parquet and ORC are binary with real data types (an int takes 4 bytes, not 6 characters).</li>
        <li><b>Schema:</b> CSV has none (just a header); JSON has field names but no types; Avro, Parquet and ORC store the full schema inside the file.</li>
        <li><b>Compression codecs:</b> <i>gzip</i> squeezes most but is slow; <i>snappy</i> and <i>lz4</i> are fast with moderate savings; <i>zstd</i> is a good balance and increasingly the default.</li>
        <li><b>Splittable:</b> a cluster wants to split a big file into pieces for many workers. A gzipped CSV cannot be split (it must be read from the start); Avro, Parquet and ORC are designed to be split.</li>
      </ul>
L3> Inside Parquet and ORC, and schema evolution
      <ul>
        <li><b>Parquet layout:</b> a file holds <b>row groups</b> (often around 128 MB); each row group holds one <b>column chunk</b> per column; chunks are divided into <b>pages</b>. A <b>footer</b> at the end stores the schema and statistics (min, max, null count) for every chunk.</li>
        <li><b>Predicate pushdown:</b> for <code>WHERE day = '2026-10-19'</code>, the engine reads the footer first and skips every row group whose min–max range can’t contain that date. Sorting data by commonly filtered columns makes skipping far more effective.</li>
        <li><b>Encodings:</b> <i>dictionary</i> (store “Pune” once, then small numbers), <i>run-length</i> (“Pune × 5,000”), <i>bit-packing</i> and <i>delta</i> encoding for sorted numbers or timestamps. Compression is applied on top.</li>
        <li><b>ORC</b> (from the Hive world) uses <b>stripes</b> with light indexes and optional bloom filters; Parquet is the more common default in Spark and the cloud.</li>
        <li><b>Avro schema evolution:</b> readers and writers each have a schema. Adding a field with a <b>default</b> is safe; removing or renaming without an alias breaks old readers. Kafka teams enforce these rules with a <b>Schema Registry</b>.</li>
        <li><b>Table formats are not file formats:</b> Delta Lake, Iceberg and Hudi store data <i>as</i> Parquet files and add a transaction log on top (Lesson 4.3).</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>file format</b> defines how records are encoded as bytes in a file: the layout (row-oriented or column-oriented), the encoding (text or binary), whether a schema is stored, and which compression is applied. <b>CSV</b> and <b>JSON</b> are human-readable, row-oriented text formats. <b>Avro</b> is a row-oriented binary format that stores its schema with the data and supports schema evolution. <b>Parquet</b> and <b>ORC</b> are column-oriented binary formats with embedded schemas, per-column compression and statistics that let query engines read only the needed columns and skip irrelevant data.',
    'A file format is the way data is laid out inside a file. CSV and JSON are plain text you can read yourself. Avro is compact binary that remembers its own structure. Parquet and ORC store each column separately and compress it, so analytics tools can read just the parts they need, much faster.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Row-oriented', 'All values of one record are stored next to each other.'),
    ('Column-oriented (columnar)', 'All values of one column are stored next to each other.'),
    ('Serialization', 'Turning data in memory into bytes for a file or network message (and back: deserialization).'),
    ('Compression codec', 'The algorithm used to shrink the bytes: gzip, snappy, zstd, lz4.'),
    ('Splittable', 'A file that can be cut into pieces and processed by many workers in parallel.'),
    ('Row group / stripe', 'A large block of rows inside a Parquet / ORC file, with stored statistics.'),
    ('Predicate pushdown', 'Using file statistics to skip data that can’t match a filter, before reading it.'),
    ('Schema evolution', 'Changing a schema over time (adding or removing fields) without breaking old data or readers.'),
]) + '''

  <h3>The five formats in one line each</h3>
''' + facts([
    ('CSV', 'Plain text, comma-separated, header row. No types, no schema. Universal, but large and slow for big data.'),
    ('JSON', 'Plain text with field names and nesting. Used by web APIs and app events. Even larger than CSV.'),
    ('Avro', 'Binary, row-oriented, schema stored in the file (Apache, 2009). The usual choice for Kafka messages.'),
    ('Parquet', 'Binary, columnar (Twitter and Cloudera, 2013, based on Google’s Dremel). The default for analytics in Spark, lakes and lakehouses.'),
    ('ORC', 'Binary, columnar (built for Hive, 2013). Excellent compression; common in Hadoop and Hive platforms.'),
]) + lv + '''
EXAM> For a 5- or 10-mark question, make a table comparing CSV, JSON, Avro, Parquet and ORC on <b>row vs columnar, text vs binary, schema, compression, splittable and best use</b>. Then explain with one example why columnar formats are faster for analytical queries (read fewer columns + better compression + skipping with statistics).'''

# ---------------------------------------------------------------- types
types = cards([
    ('CSV', 'Simple text rows. Best for small exports, spreadsheets and sharing with people.', 'Row · text'),
    ('JSON', 'Labelled, nested text. Best for APIs, app events and configuration.', 'Row · text'),
    ('Avro', 'Compact binary rows with a stored schema. Best for streaming (Kafka) and writing records one by one.', 'Row · binary'),
    ('Parquet', 'Compressed columns with statistics. Best for analytics, data lakes and lakehouse tables.', 'Column · binary'),
    ('ORC', 'Compressed columns with indexes. Best for Hive and Hadoop-based warehouses.', 'Column · binary'),
]) + '''

  <h3>Side by side</h3>
''' + table(['', 'CSV', 'JSON', 'Avro', 'Parquet', 'ORC'], [
    ['<b>Layout</b>', 'Row', 'Row', 'Row', 'Column', 'Column'],
    ['<b>Encoding</b>', 'Text', 'Text', 'Binary', 'Binary', 'Binary'],
    ['<b>Schema in file</b>', 'No (header only)', 'Field names, no types', 'Yes', 'Yes', 'Yes'],
    ['<b>Nested data</b>', 'No', 'Yes', 'Yes', 'Yes', 'Yes'],
    ['<b>Compression</b>', 'Whole file (gzip)', 'Whole file', 'Per block', 'Per column, very good', 'Per column, very good'],
    ['<b>Splittable</b>', 'Yes, but not when gzipped', 'JSON lines: yes', 'Yes', 'Yes', 'Yes'],
    ['<b>Human-readable</b>', 'Yes', 'Yes', 'No', 'No', 'No'],
    ['<b>Best for</b>', 'Small exports', 'APIs, events', 'Kafka, writes', 'Analytics, lakes', 'Hive warehouses'],
], minw=640) + '''
TIP> In real platforms formats are used together: apps send <b>JSON</b>, Kafka carries <b>Avro</b>, the raw zone keeps the original files, and cleaned tables are stored as <b>Parquet</b> (often inside Delta Lake or Iceberg). Choose by job, not by fashion.'''

# ---------------------------------------------------------------- steps
c1 = '''rows = [("O1", "Pune", 220), ("O2", "Pune", 150), ("O3", "Thane", 20)]
csv_text = "id,city,amount\\n" + "".join(f"{i},{c},{a}\\n" for i, c, a in rows)
json_text = "".join(f'{{"id": "{i}", "city": "{c}", "amount": {a}}}\\n' for i, c, a in rows)
print("CSV bytes :", len(csv_text))
print("JSON bytes:", len(json_text))'''
c2 = '''rows = [("O1", "Pune", 220), ("O2", "Pune", 150), ("O3", "Thane", 20)]
print("Row layout   :", [v for r in rows for v in r])
columns = list(zip(*rows))
print("Column layout:", columns)'''
c3 = '''city = ["Pune", "Pune", "Thane", "Pune", "Mumbai", "Pune"]
dictionary = sorted(set(city))
codes = [dictionary.index(c) for c in city]
print("dictionary:", dictionary)
print("codes     :", codes)'''
c4 = '''city_sorted = ["Mumbai", "Pune", "Pune", "Pune", "Pune", "Thane"]
runs = []
for c in city_sorted:
    if runs and runs[-1][0] == c:
        runs[-1][1] += 1
    else:
        runs.append([c, 1])
print(runs)'''
c5 = '''row_groups = [("2026-10-01", "2026-10-10"), ("2026-10-11", "2026-10-20"), ("2026-10-21", "2026-10-31")]
want = "2026-10-19"
for i, (lo, hi) in enumerate(row_groups):
    print(f"row group {i}: min {lo} max {hi} ->", "READ" if lo <= want <= hi else "skip")'''
steps = stepper([
    ('Text formats repeat a lot',
     code('python', 'csv_vs_json.py', c1, run_code(c1)),
     'JSON repeats every field name on every row, so it is much bigger than CSV for the same data. Both store numbers as characters, so <code>220</code> takes three bytes of text instead of a compact binary number.'),
    ('Row layout vs column layout',
     code('python', 'layout.py', c2, run_code(c2)),
     'A row format keeps each order together. A columnar format keeps each <b>column</b> together. To total the amounts, the columnar file reads one short run of numbers instead of every value of every row.'),
    ('Dictionary encoding',
     code('python', 'dictionary.py', c3, run_code(c3)),
     'A column has few distinct cities, so Parquet stores each name once and replaces values with small numbers. This only works well because similar values sit together in one column.'),
    ('Run-length encoding loves sorted data',
     code('python', 'rle.py', c4, run_code(c4)),
     'When the column is sorted, repeated values become runs: “Pune × 4” instead of four copies. Sorting large tables by common filters (city, date) can shrink them dramatically.'),
    ('Statistics let engines skip data',
     code('python', 'skip.py', c5, run_code(c5)),
     'The Parquet footer stores the min and max of each column for every row group. A query for 19 October reads only the one row group whose range contains that date. This is <b>predicate pushdown</b>.'),
    ('The schema travels with the file',
     '<p>Avro, Parquet and ORC store the column names and types inside the file. Spark, Hive, BigQuery or pandas can open it and know immediately that <code>amount</code> is an integer and <code>day</code> is a date.</p>',
     'No guessing types from text, no broken loads because someone typed “N/A” in a number column. A stored schema is one of the biggest practical benefits of the binary formats.'),
])

# ---------------------------------------------------------------- two-view animation
def laptop(inner, title):
    return ('<rect x="40" y="16" width="280" height="170" rx="10" class="s-board"/><rect x="50" y="28" width="260" height="146" rx="4" class="s-card2"/>'
            '<path d="M24 196h312l-12 14H36z" style="fill:#2B3A34"/>' + t(180, 44, title, 9.4, bold=True) + inner)
q = t(60, 68, "SELECT SUM(amount) FROM orders", 8.4, 'blue', anchor='start', mono=True) + t(60, 82, "WHERE city = 'Pune'", 8.4, 'blue', anchor='start', mono=True) + t(60, 96, "AND day = '2026-10-19'", 8.4, 'blue', anchor='start', mono=True)
def prog(p, col, label):
    return '<rect x="60" y="120" width="240" height="14" rx="5" class="s-card2"/>' + (fill(60, 120, round(240 * p), 14, col, rx=5) if p else '') + t(180, 154, label, 8.8, 'ink2')
see = [
    laptop(q + t(180, 150, 'Same question, two files.', 8.8, 'ink2'), 'Kabir’s notebook'),
    laptop(q + prog(.25, 'red', 'orders.csv: reading… 2.5 of 10 GB'), 'Query on CSV'),
    laptop(q + prog(1, 'red', 'Done in 4 min 05 s · Rs 7,42,180'), 'Query on CSV'),
    laptop(q + prog(.05, 'green', 'orders.parquet: reading footer…'), 'Query on Parquet'),
    laptop(q + prog(.6, 'green', 'reading 3 columns of 1 row group'), 'Query on Parquet'),
    laptop(q + prog(1, 'green', 'Done in 4 s · Rs 7,42,180 (same answer)'), 'Query on Parquet'),
]
def grid(read_cols=None, read_groups=None, all_read=False, footer=False, skip=False):
    o = ''
    names = ['order_id', 'city', 'dish', 'amount', 'day']
    for c, n in enumerate(names):
        o += t(70 + c * 56, 38, n, 7.8, 'ink3', mono=True)
    for g in range(4):
        y = 46 + g * 34
        o += t(18, y + 18, f'RG{g}', 8, 'ink3', anchor='start', bold=True)
        for c in range(5):
            x = 46 + c * 56
            on = all_read or (read_cols and c in read_cols and read_groups and g in read_groups)
            col = 'red' if all_read else 'green'
            o += fill(x, y, 48, 28, col if on else 'grey', rx=3, opacity=None if on else (.25 if skip and not (read_groups and g in read_groups) else .55))
    if footer:
        o += fill(46, 186, 272, 16, 'acc', rx=3) + t(182, 198, 'footer: schema + min/max per row group', 8, extra=' style="fill:#fff"', bold=True)
    return o
behind = [
    t(180, 22, 'Same 12 crore orders, two layouts', 10, bold=True) + box(14, 40, 158, 120, 'card') + t(93, 58, 'CSV: rows of text', 9, bold=True) + ''.join(t(22, 78 + k * 14, ln, 7.6, anchor='start', mono=True) for k, ln in enumerate(['O1,Pune,thali,220,10-19', 'O2,Thane,dosa,150,10-02', 'O3,Pune,chai,20,10-19', '…'])) + box(188, 40, 158, 120, 'green') + t(267, 58, 'Parquet: columns', 9, bold=True) + ''.join(fill(200 + k * 28, 70, 22, 76, 'green', rx=3, opacity=.7) for k in range(5)) + t(180, 186, 'CSV 10 GB of text · Parquet 1.8 GB binary', 9, 'ink2'),
    grid(all_read=True) + t(180, 22, 'CSV: every byte must be read and parsed', 9.6, 'red', bold=True),
    grid(all_read=True) + t(180, 22, '10 GB read · 12 crore rows parsed from text', 9.6, 'red', bold=True),
    grid(footer=True) + t(180, 22, 'Parquet: read the small footer first', 9.6, 'green', bold=True),
    grid(read_cols={1, 3, 4}, read_groups={2}, footer=True, skip=True) + t(180, 22, 'Skip 3 row groups · read 3 of 5 columns', 9.6, 'green', bold=True),
    grid(read_cols={1, 3, 4}, read_groups={2}, footer=True, skip=True) + t(180, 22, '≈ 150 MB read instead of 10 GB', 9.6, 'green', bold=True),
]
see_caps = ['Kabir writes one question: total amount for Pune on 19 October. He will run it on the CSV and on the Parquet copy.',
            'On the CSV the progress bar crawls: a quarter of the 10 GB file read so far.',
            'Four minutes later the CSV query finishes.',
            'On the Parquet file, the first thing that happens is a quick read of the file’s footer.',
            'Then the bar jumps: only a small part of the file is read.',
            'Four seconds, and exactly the same answer.']
behind_caps = ['The same orders stored two ways: CSV as rows of text, Parquet as compressed binary columns.',
               'With CSV there is no way to skip anything: every row, every column, is read and parsed from text.',
               'All 10 GB pass through the disk and CPU to answer a question about one city on one day.',
               'Parquet’s footer holds the schema and the min and max of every column in every row group: a few kilobytes.',
               'Only one row group can contain 19 October, so three are skipped. Only city, amount and day are read.',
               'Roughly 150 MB is read instead of 10 GB. Less reading, plus no text parsing, gives the huge speed-up. (Sizes and times are illustrative.)']
two = anim_two('CSV vs Parquet', 'One query: what Kabir sees, and what the disk reads', 'Kabir running the same query on a CSV file and a Parquet file',
               'The bytes each format must read from disk to answer the query', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: size race (real numbers from formats_race.out)
sizes = [('CSV', 6.76, 'acc'), ('JSON lines', 17.44, 'red'), ('CSV.gz', 1.29, 'blue'), ('Avro', 1.37, 'violet'), ('Parquet', 1.53, 'green'), ('ORC', 0.92, 'green')]
def race(n, note=''):
    rows = []
    for k, (name, mb, col) in enumerate(sizes):
        if k < n:
            rows.append((name, mb / 17.44 * 100, col, f'{mb:.2f} MB'))
        else:
            rows.append((name, 0, col, ''))
    return t(14, 22, 'Same 2 lakh orders, file size on disk', 9.2, 'ink2', anchor='start') + bars(rows, x=100, y=32, w=200, gap=20)
fr1 = [
    race(1) + cap('CSV: plain text, 6.76 MB. Our baseline.', '', 'card', y=164, h=34),
    race(2) + cap('JSON lines: 2.6× bigger. Field names repeat every row.', '', 'red', y=164, h=34),
    race(3) + cap('Gzipped CSV: 19% of the size, but not splittable', 'and still text: every row must be decompressed and parsed.', 'blue', y=158, h=46),
    race(5) + cap('Avro and Parquet: binary with real types and a schema.', 'Both around a fifth of the CSV.', 'green', y=158, h=46),
    race(6) + cap('ORC: smallest here, 13.6% of the CSV.', 'Querying 2 columns, Parquet was about 13× faster.', 'green', y=158, h=46),
]
s1 = anim_one('Real-time scenario 1', 'The size race: one table, six files',
              'These are real numbers from the program in “Run it on your PC” below: 2 lakh random orders written in six formats. Watch the file sizes appear one by one.',
              'Same data, six formats', 'Bar chart of file sizes for the same data in CSV, JSON, gzipped CSV, Avro, Parquet and ORC', fr1,
              ['The CSV file is 6.76 MB. Every number and date is stored as text characters.',
               'JSON lines is 17.44 MB, about 2.6 times the CSV, because every row repeats every field name.',
               'Gzip shrinks the CSV to 19% of its size, but a gzipped CSV can’t be split across workers and must still be decompressed and parsed as text.',
               'Avro (1.37 MB) and Parquet (1.53 MB) are binary formats with real types and an embedded schema.',
               'ORC is the smallest at 13.6% of the CSV. On this random data the columnar formats don’t beat gzip on size, but for a query on two columns Parquet read only those columns and was about 13 times faster. On real, sorted data the columnar formats usually win on both. (Exact sizes vary slightly with library versions.)'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: Avro + schema registry
def node(x, y, w, lines, tone):
    return label_box(x, y, w, 46, lines, tone, 9)
fr2 = [
    node(10, 40, 100, ['Order app', 'producer'], 'blue') + node(130, 40, 100, ['Kafka topic', 'orders'], 'acc') + node(250, 40, 100, ['Billing job', 'consumer'], 'green') + arrow(112, 63, 128, 63) + arrow(232, 63, 248, 63)
    + box(70, 110, 220, 44, 'card') + t(180, 128, 'Schema v1: order_id, city, amount', 8.6, mono=True) + t(180, 144, 'stored in the Schema Registry', 8.4, 'ink2') + t(180, 190, 'Each Avro message carries a small schema id, not the schema.', 8.8, 'ink2'),
    node(10, 40, 100, ['Order app', 'v2'], 'blue') + node(130, 40, 100, ['Kafka topic', 'orders'], 'acc') + node(250, 40, 100, ['Billing job', 'still v1'], 'green') + arrow(112, 63, 128, 63) + arrow(232, 63, 248, 63)
    + box(40, 110, 280, 44, 'green') + t(180, 128, 'v2 adds: coupon (default = null)', 8.8, mono=True, bold=True) + t(180, 144, 'Registry: compatible ✓', 8.6, 'green', bold=True) + t(180, 190, 'Old consumers simply ignore the new field.', 8.8, 'ink2'),
    node(10, 40, 100, ['Analytics job', 'reads v2'], 'violet') + node(130, 40, 100, ['old message', 'written in v1'], 'card') + arrow(128, 63, 112, 63)
    + box(40, 110, 280, 44, 'green') + t(180, 128, 'old v1 message has no coupon', 8.8, bold=True) + t(180, 144, 'reader fills the default: coupon = null', 8.6, mono=True) + t(180, 190, 'New readers can read old data too.', 8.8, 'ink2'),
    node(10, 40, 100, ['Order app', 'v3 (wrong)'], 'red') + node(130, 40, 100, ['Schema', 'Registry'], 'acc') + arrow(112, 63, 128, 63)
    + box(40, 110, 280, 44, 'red') + t(180, 128, 'v3 removes amount (no default)', 8.8, mono=True, bold=True) + t(180, 144, 'Registry: INCOMPATIBLE ✗ · publish refused', 8.6, 'red', bold=True) + t(180, 190, 'The mistake is stopped before any message is sent.', 8.8, 'ink2'),
    t(180, 30, 'Safe schema changes in Avro', 10.5, 'acc', bold=True) + box(20, 44, 320, 110, 'card')
    + ''.join(t(34, 66 + k * 20, ln, 8.8, 'green' if ln.startswith('✓') else 'red', anchor='start', bold=True) for k, ln in enumerate(['✓ add a field with a default', '✓ remove a field that had a default', '✓ rename using an alias', '✗ remove a required field', '✗ change a field’s type (e.g. int → string)']))
    + t(180, 186, 'Rules are checked automatically on every new version.', 8.8, 'ink2'),
]
s2 = anim_one('Real-time scenario 2', 'Kafka + Avro: changing a message without breaking anyone',
              'TiffinGo’s order app sends Avro messages through Kafka to several consumers. Watch a safe change go through and an unsafe one get stopped by the Schema Registry.',
              'Schema evolution in practice', 'An Avro schema evolving safely through a schema registry', fr2,
              ['The producer writes Avro messages to a Kafka topic. The schema (version 1) is stored once in a <b>Schema Registry</b>; each message carries only a small schema id.',
               'Version 2 adds a <code>coupon</code> field with a default of null. The registry checks compatibility and allows it. The billing job, still on version 1, ignores the new field.',
               'A new analytics job reads with version 2. When it reads an old version-1 message, Avro fills in the default, so new readers can read old data.',
               'A careless version 3 removes the required <code>amount</code> field. The registry rejects it as incompatible, so no broken messages ever reach consumers.',
               'The rules to remember: add fields with defaults, remove only fields that had defaults, rename with aliases, never remove required fields or change types in place.'])

# ---------------------------------------------------------------- scenario 3 (advanced): sorting + row group skipping
months = ['01–31', '02–30', '01–31', '03–29']
def rgs(ranges, read, label=True):
    o = ''
    for g, (lo, hi) in enumerate(ranges):
        y = 34 + g * 30
        on = g in read
        o += box(14, y, 210, 24, 'red' if on and len(read) > 1 else ('green' if on else 'card'), rx=4)
        o += t(24, y + 16, f'row group {g}: day min {lo} max {hi}', 8.4, anchor='start', mono=True)
        if label: o += t(342, y + 16, 'READ' if on else 'skip', 8.8, 'red' if on and len(read) > 1 else ('green' if on else 'ink3'), anchor='end', bold=True)
    return o
unsorted = [('10-01', '10-31')] * 4
sorted_ = [('10-01', '10-08'), ('10-09', '10-16'), ('10-17', '10-24'), ('10-25', '10-31')]
fr3 = [
    t(180, 22, "Query: WHERE day = '2026-10-19'", 9.6, 'blue', bold=True, mono=True) + rgs(unsorted, {0, 1, 2, 3}) + cap('Unsorted data: every row group spans the whole month.', 'min/max can’t rule any out, so all 4 are read.', 'red', y=162, h=46),
    t(180, 22, 'Rewrite the table sorted by day', 9.6, 'acc', bold=True) + rgs(sorted_, set(), False) + cap('Same rows, sorted before writing.', 'Each row group now covers about one week.', 'blue', y=162, h=46),
    t(180, 22, "Query: WHERE day = '2026-10-19'", 9.6, 'blue', bold=True, mono=True) + rgs(sorted_, {2}) + cap('Only row group 2 can contain 19 October.', '3 of 4 skipped without reading: 75% less I/O.', 'green', y=162, h=46),
    t(180, 22, 'Bonus: sorted columns compress better', 9.6, 'acc', bold=True) + bars([('day (unsorted)', 100, 'red', '100%'), ('day (sorted)', 6, 'green', '~6%'), ('city (unsorted)', 100, 'red', '100%'), ('city (sorted)', 30, 'green', '~30%')], x=130, y=40, w=170, gap=24)
    + cap('Runs of equal values → run-length + dictionary encoding.', '(Illustrative ratios; real gains depend on the data.)', 'green', y=150, h=46),
    t(180, 22, 'Sort by what you filter by', 9.6, 'acc', bold=True) + box(14, 36, 332, 110, 'card') + ''.join(t(26, 58 + k * 20, ln, 8.8, anchor='start') for k, ln in enumerate(['• partition folders by day (Lesson 4.3)', '• inside a partition, sort or cluster by city', '• target row groups of ~128 MB, files of 128 MB–1 GB', '• table formats: Z-order / clustering does this for you']))
    + cap('Layout decisions often matter more than more machines.', '', 'blue', y=160, h=34),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Inside Parquet: why sorting makes queries skip data',
              'Parquet can skip row groups using min/max statistics, but only if the data is laid out well. Watch the same query on an unsorted and a sorted file.',
              'Statistics and sort order', 'Parquet row groups with min and max statistics, unsorted and sorted by day', fr3,
              ['In an unsorted file, orders from every day are mixed into every row group, so each group’s min and max cover the whole month. The engine must read all four.',
               'The table is rewritten sorted by day. The rows are the same; only their order changes, so each row group now covers about a week.',
               'For 19 October, the footer statistics show that only row group 2 can match. The other three are skipped without reading a byte of their data.',
               'Sorting also puts equal values next to each other, so dictionary and run-length encoding shrink the columns much more.',
               'The practical rules: partition by the main filter (often date), sort or cluster within it by the next filter, and keep row groups and files large. Lakehouse table formats offer clustering and Z-ordering to do this automatically.'])

realworld = '''  <p>Three live scenarios: a size race between six formats using real numbers, Kafka messages evolving safely with Avro and a Schema Registry, and an advanced look at how sort order lets Parquet skip data.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Which format, where</h3>
''' + usecase('<rect x="16" y="24" width="88" height="44" rx="6" class="s-soft-acc" style="stroke:var(--track)"/><text x="60" y="51" text-anchor="middle" font-size="11" font-weight="700" class="s-acc">.csv</text>',
              '1. Government open data and bank statements: CSV', 'Portals publishing public datasets and banks letting you download statements use CSV (or Excel), because anyone can open it. Data teams convert it to Parquet as soon as it lands.', ['CSV download', '*Convert once', 'Parquet table']) + usecase(
    '<text x="60" y="52" text-anchor="middle" font-size="18" font-weight="700" class="s-blue mono">{ }</text>',
    '2. Mobile apps and web APIs: JSON', 'Payment apps, food-delivery apps and partner APIs exchange JSON because every language can read it. High-volume flows often switch to Avro or Protobuf to save bandwidth.', ['App', '*JSON over HTTPS', 'API / Kafka']) + usecase(
    '<path d="M20 45h80" style="stroke:var(--violet);stroke-width:4"/><circle cx="35" cy="45" r="7" style="fill:var(--violet)"/><circle cx="60" cy="45" r="7" style="fill:var(--violet)"/><circle cx="85" cy="45" r="7" style="fill:var(--violet)"/>',
    '3. Event streams: Avro with a Schema Registry', 'Companies running Kafka at scale commonly use Avro (or Protobuf) with a schema registry so that dozens of producer and consumer teams can change messages safely.', ['Producer', '*Avro + registry', 'Many consumers']) + usecase(
    '<rect x="20" y="20" width="14" height="50" rx="3" style="fill:var(--green)"/><rect x="40" y="20" width="14" height="50" rx="3" style="fill:var(--green);opacity:.7"/><rect x="60" y="20" width="14" height="50" rx="3" style="fill:var(--green);opacity:.5"/><rect x="80" y="20" width="14" height="50" rx="3" style="fill:var(--green);opacity:.3"/>',
    '4. Lakes, lakehouses and cloud warehouses: Parquet', 'Spark jobs, Delta Lake and Iceberg tables, and external tables in BigQuery, Snowflake, Redshift and Athena all read Parquet. Pay-per-scan engines charge less because fewer bytes are read.', ['Raw files', '*Parquet / Delta / Iceberg', 'SQL + ML'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Four minutes or four seconds?', story)
        + part(2, 'definition', 'Definition', 'What is a file format?', definition)
        + part(3, 'types', 'Types and ways to use it', 'CSV, JSON, Avro, Parquet and ORC compared', types)
        + part(4, 'steps', 'Step by step', 'What happens inside each format', steps)
        + part(5, 'animation', 'See it happen', 'One query: what Kabir sees, and what the disk reads', '  <p>Step through the six frames. Left: Kabir running the same query on two files. Right: how much of each file is actually read.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: formats at work', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Data platform · design', 'Fresher', 'Choose formats for a new pipeline',
            'An app sends order events. They go through Kafka, land in a lake, and analysts query them daily. Your lead asks which file format to use at each step.',
            'do you choose formats by job rather than by habit?',
            '<ul><li><b>App → backend:</b> JSON, because it is easy for mobile developers.</li><li><b>Kafka:</b> Avro (or Protobuf) with a Schema Registry: compact, typed and safe to evolve.</li><li><b>Raw zone:</b> keep messages as received (Avro or JSON) for replay.</li><li><b>Analytics tables:</b> Parquet (in Delta Lake or Iceberg), partitioned by date, compressed with snappy or zstd.</li><li><b>Exports to business users:</b> CSV or Excel, generated from the Parquet tables.</li></ul>',
            'using CSV everywhere because it is familiar, or Parquet for single-message streaming.')
        + scn('Performance · cost', '1–3 years', 'The Athena bill is too high',
              'Analysts query 40 TB of gzipped CSV logs with a pay-per-scan engine. Each dashboard refresh costs a lot and takes minutes.',
              'do you know how format and layout change cost and speed?',
              '<ol><li>Convert the logs to <b>Parquet</b> with snappy or zstd: typically several times smaller, and queries read only the columns they need.</li><li><b>Partition</b> by date (and perhaps region) so queries scan only the days they ask for.</li><li>Sort or cluster within partitions by common filters to improve min/max skipping.</li><li>Compact small files into files of a few hundred MB.</li><li>Measure bytes scanned before and after; it often drops by 90% or more.</li></ol>',
              'buying more compute or caching results without fixing the storage layout.')
        + scn('Streaming · reliability', '1–3 years', 'A field removal broke three consumers',
              'A producer team removed a field from their Kafka messages. Three downstream jobs crashed at night.',
              'do you understand schema evolution and how to enforce it?',
              '<p>Move to Avro (or Protobuf) with a <b>Schema Registry</b> and set a compatibility mode such as BACKWARD or FULL. The registry then rejects incompatible schemas at publish time. Teach producers the rules: add fields with defaults, remove only optional fields, never change types in place. Add the compatibility check to the producer’s CI pipeline, and give consumers time to upgrade before removing anything.</p>',
              'asking every team to “be careful” without an automated check.')
        + scn('Fundamentals · interview', 'Fresher', '“Why is Parquet faster than CSV?”',
              'A classic interview question, often followed by “when would you not use Parquet?”',
              'can you explain the mechanism, and its limits?',
              '<p>Parquet is <b>columnar</b>, so a query reads only the columns it needs; it is <b>binary with types</b>, so there is no text parsing; each column is <b>compressed and encoded</b> (dictionary, run-length) very efficiently; and <b>min/max statistics</b> let engines skip row groups. It is not ideal for writing one record at a time (streaming), for frequent single-row updates without a table format, for tiny files, or when people need to open the file directly, where CSV or JSON is friendlier.</p>',
              'saying “because it is compressed” and stopping there.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
