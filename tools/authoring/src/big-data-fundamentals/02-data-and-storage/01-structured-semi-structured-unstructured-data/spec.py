import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='02-data-and-storage', lesson='01-structured-semi-structured-unstructured-data', n='2.1',
    module_label='Module 2 · Data and Storage',
    title='Structured, semi-structured and unstructured data',
    desc='Structured, semi-structured and unstructured data explained with a food-delivery order: schemas, JSON nesting and flattening, log parsing, metadata, turning text into labels, schema drift and data contracts. Beginner to Advanced, real-time animations, Python you can run in the browser and on your PC.',
    og_desc='One food order creates a table row, a nested JSON event, log lines, a review and a photo. Learn to handle all three shapes of data.',
    minutes=28, level='Beginner → Advanced',
    lead='A single food order creates a neat table row, a nested JSON event, log lines from the rider\'s phone, a free-text review and a photo. These are the three shapes of data: <b>structured</b>, <b>semi-structured</b> and <b>unstructured</b>. In this lesson you flatten JSON into rows, parse logs, turn chats into numbers during an outage, and see how an app update can silently break a pipeline.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'All three shapes on your PC'],
)

RUN = dict(
    heading='Sort records by shape, and read each one',
    intro='<p>Four records arrive at a data platform. The program decides the shape of each and prints a short summary. Then try the challenges: flatten nested JSON, parse a log line, label free text and catch schema drift.</p>',
    code='''import json

records = [
    ("table_row", ("O1043", "Pune", 420)),
    ("json", '{"order_id": "O1043", "items": [{"dish": "thali"}, {"dish": "lassi"}]}'),
    ("log", "13:02:11 rider=R77 status=PICKED"),
    ("text", "Thali was great but the lassi was warm"),
]

for kind, value in records:
    if kind == "table_row":
        print("STRUCTURED     :", value, "-> 3 fixed columns")
    elif kind == "json":
        event = json.loads(value)
        print("SEMI-STRUCTURED:", list(event), "-> keys inside the record,", len(event["items"]), "nested items")
    elif kind == "log":
        fields = dict(p.split("=") for p in value.split()[1:])
        print("SEMI-STRUCTURED:", fields, "-> parsed from a pattern")
    else:
        print("UNSTRUCTURED   :", len(value.split()), "words, no fields until we extract some")
''',
    anno=[
        ('event = json.loads(value)', '<code>json.loads</code> turns JSON text into Python dictionaries and lists. The field names come from the data itself.'),
        ('fields = dict(p.split("=") for p in value.split()[1:])', 'Split the line by spaces, skip the time, then split each <code>key=value</code> pair. This is log parsing.'),
        ('print("UNSTRUCTURED   :", len(value.split()), "words, no fields until we extract some")', 'Plain text has no fields. All we can do without extra work is count words.'),
    ],
    tasks=[
        dict(label='1 · Sort by shape', hint='Press <b>Run</b>. Add a fifth record: <code>("text", "Rider was rude")</code>. Then add a JSON record with three items.', code=None),
        dict(label='2 · Flatten JSON', hint='Explode the <code>items</code> list into one row per item, repeating the order fields. Add a <code>"coupon"</code> key to only one order: print <code>None</code> where it is missing.',
             code='''import json
orders = [
    '{"order_id": "O1", "city": "Pune", "items": [{"dish": "thali", "qty": 1, "price": 220}, {"dish": "lassi", "qty": 2, "price": 100}]}',
    '{"order_id": "O2", "city": "Mumbai", "items": [{"dish": "dosa", "qty": 1, "price": 150}]}',
]
rows = []
for text in orders:
    o = json.loads(text)
    for item in o["items"]:
        rows.append((o["order_id"], o["city"], item["dish"], item["qty"] * item["price"]))
for r in rows:
    print(r)
print("Revenue:", sum(r[3] for r in rows))
'''),
        dict(label='3 · Parse logs', hint='Count lines per status and find the slowest request. Add a line with <code>status=FAILED</code>.',
             code='''logs = [
    "13:02:11 order=O1 status=PLACED ms=120",
    "13:02:15 order=O2 status=PAY_FAILED ms=3020",
    "13:02:19 order=O3 status=PLACED ms=95",
    "13:02:22 order=O4 status=PLACED ms=210",
]
count, slowest = {}, None
for line in logs:
    f = dict(p.split("=") for p in line.split()[1:])
    count[f["status"]] = count.get(f["status"], 0) + 1
    if slowest is None or int(f["ms"]) > int(slowest["ms"]):
        slowest = f
print(count)
print("Slowest:", slowest)
'''),
        dict(label='4 · Text → labels', hint='Turn free-text reviews into structured labels with keyword lists. Add a “spilled” keyword list and a review that mentions it.',
             code='''reviews = ["Food was cold and late", "Loved the thali!", "Late again, rider rude", "Perfect lassi"]
topics = {"late": ["late", "delay"], "cold": ["cold", "warm"], "rude": ["rude"]}
for r in reviews:
    words = r.lower().replace("!", "").replace(",", "").split()
    labels = [t for t, keys in topics.items() if any(k in words for k in keys)]
    print(f"{r:28} -> {labels or ['praise']}")
'''),
        dict(label='5 · Schema drift (advanced)', hint='Compare a new event with the expected schema: report missing fields, new fields and wrong types. Change <code>"amount"</code> back to a number and run again.',
             code='''expected = {"order_id": str, "amount": int, "city": str}
event = {"order_id": "O9", "amount": "₹420", "city_name": "Pune"}

missing = [k for k in expected if k not in event]
extra = [k for k in event if k not in expected]
wrong_type = [k for k in expected if k in event and not isinstance(event[k], expected[k])]
print("Missing :", missing)
print("New     :", extra)
print("Bad type:", wrong_type)
print("ACCEPT" if not (missing or wrong_type) else "QUARANTINE")
'''),
        dict(label='6 · Explode trap (advanced)', hint='An order has 3 items and 2 coupons. Exploding both lists together creates 6 rows, and summing the price double-counts. Compare the wrong and right totals.',
             code='''order = {"id": "O7", "items": [("thali", 220), ("lassi", 100), ("jamun", 60)], "coupons": ["A", "B"]}
wrong = [(order["id"], d, p, c) for d, p in order["items"] for c in order["coupons"]]
print("Rows after exploding both lists:", len(wrong))
print("Wrong total:", sum(r[2] for r in wrong))
print("Right total:", sum(p for _, p in order["items"]))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: create and read all three shapes',
    intro='<p>This program creates a <code>sample_data</code> folder with a CSV (structured), a JSON-lines file and a log file (semi-structured) and a text file of reviews (unstructured). Then it reads each one the right way: <code>csv</code>, <code>json</code>, a regular expression and simple text analysis. Only the Python standard library is used. Save it as <code>three_shapes.py</code> in an empty folder and run it, then open the files it creates.</p>',
    items=[
        dict(title='Create and read structured, semi-structured and unstructured files', file='three_shapes.py',
             cmd=open(os.path.join(HERE, 'three_shapes.py')).read() + '\n# In a terminal:  python three_shapes.py',
             output=open(os.path.join(HERE, 'three_shapes.out')).read(),
             note='Recorded from a real run with Python 3.13 (any Python 3.8+ gives the same output). Notice that the JSON flattening turned 2 events into 3 item rows and filled the missing coupon with <code>None</code>, the regular expression pulled five fields out of each log line, and the reviews became a structured label.'),
    ],
)

TRACE = dict(
    heading='Flattening a nested order, one line at a time',
    intro='<p>An order with two items becomes two flat rows. Watch the inner loop run once per item and the <code>rows</code> list grow, with the order id repeated on each row.</p>',
    code='''order = {"id": "O1043", "items": [["thali", 220], ["lassi", 200]]}
rows = []
for dish, amount in order["items"]:
    rows.append((order["id"], dish, amount))
total = 0
for r in rows:
    total = total + r[2]
print(rows, total)
''',
    notes={1: 'Nested :: One record that contains a list of items.',
           4: 'Explode :: The order id is copied onto each item row.',
           7: 'Total :: Summing item amounts gives the correct order total.'},
)

WORKED_INTRO = 'Four tasks a data engineer does with mixed data, from sorting files by shape to catching schema drift. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Data platform · intake', title='Sort a folder by shape of data',
         problem='<p>A shared folder has files from many teams. Count how many are structured, semi-structured and unstructured, based on the extension.</p>',
         inp='sales.csv, events.json, app.log, cctv.mp4, invoice.pdf, stock.parquet, review.txt, config.xml',
         approach=['Map each known extension to a shape.',
                   'Take the text after the last dot of each file name.',
                   'Count with a dictionary; unknown extensions count as unstructured.'],
         code='''files = ["sales.csv", "events.json", "app.log", "cctv.mp4", "invoice.pdf",
         "stock.parquet", "review.txt", "config.xml"]
shape_of = {"csv": "structured", "parquet": "structured",
            "json": "semi-structured", "log": "semi-structured", "xml": "semi-structured"}
count = {}
for f in files:
    shape = shape_of.get(f.rsplit(".", 1)[1], "unstructured")
    count[shape] = count.get(shape, 0) + 1
print(count)
''', notes={6: 'Shape :: <code>get</code> returns the default “unstructured” for any extension not in the map.'},
         tryit='Add <code>"photo.jpg"</code>, <code>"call.mp3"</code> and <code>"orders.avro"</code>. Which shape is Avro? (It stores a schema with the data: semi-structured, often treated as structured in practice.)'),
    dict(level='i', tag='Data engineering · flattening', title='Turn nested JSON orders into item rows',
         problem='<p>Each order is JSON with a list of items. Produce one row per item with order id, city, dish and line total, then print revenue per dish.</p>',
         inp='2 orders with 3 items in total',
         approach=['Parse each JSON string with <code>json.loads</code>.',
                   'Loop over the nested items and build one row per item.',
                   'Group the rows by dish and add the line totals.'],
         code='''import json
raw = ['{"id": "O1", "city": "Pune", "items": [{"dish": "thali", "qty": 1, "price": 220}, {"dish": "lassi", "qty": 2, "price": 100}]}',
       '{"id": "O2", "city": "Mumbai", "items": [{"dish": "thali", "qty": 2, "price": 220}]}']
per_dish = {}
for text in raw:
    o = json.loads(text)
    for it in o["items"]:
        line_total = it["qty"] * it["price"]
        per_dish[it["dish"]] = per_dish.get(it["dish"], 0) + line_total
print(per_dish)
''', notes={5: 'Parse :: JSON text becomes a dictionary with a list inside.', 7: 'Line total :: Quantity × price for this one item.'},
         tryit='Add a third order with a <code>"coupon": "LUNCH20"</code> key and 20% off its total. Use <code>o.get("coupon")</code> so orders without a coupon still work.'),
    dict(level='i', tag='Operations · logs', title='Error rate per minute from server logs',
         problem='<p>Parse log lines into minute and level, then print how many requests and errors happened in each minute and the error percentage.</p>',
         inp='6 log lines over 2 minutes',
         approach=['Split each line: the first part is the time, the second the level.',
                   'Use the first five characters of the time (HH:MM) as the minute.',
                   'Count totals and errors per minute in two dictionaries.'],
         code='''logs = ["13:02:11 INFO", "13:02:40 ERROR", "13:02:55 INFO",
        "13:03:05 ERROR", "13:03:20 ERROR", "13:03:41 INFO"]
total, errors = {}, {}
for line in logs:
    time, level = line.split()
    minute = time[:5]
    total[minute] = total.get(minute, 0) + 1
    if level == "ERROR":
        errors[minute] = errors.get(minute, 0) + 1
for m in total:
    print(m, total[m], "requests,", round(errors.get(m, 0) / total[m] * 100), "% errors")
''', notes={5: 'Minute :: Slicing “13:02:11” to “13:02” groups all lines of the same minute.'},
         tryit='Add an alert: print “ALERT” for any minute where errors are more than 50%.'),
    dict(level='a', tag='Reliability · schema drift', title='Validate a batch of events against a schema',
         problem='<p>A batch of JSON events must match the expected schema. Send each event to <b>accept</b> or <b>quarantine</b>, and summarise the problems found.</p>',
         inp='expected: order_id (str), amount (int), city (str) · 4 events',
         approach=['For each event, find missing keys and keys with the wrong type.',
                   'If any problem exists, quarantine the event and record why.',
                   'Count each kind of problem across the batch.'],
         code='''expected = {"order_id": str, "amount": int, "city": str}
batch = [{"order_id": "O1", "amount": 420, "city": "Pune"},
         {"order_id": "O2", "amount": "250", "city": "Pune"},
         {"order_id": "O3", "amount": 180},
         {"order_id": "O4", "amount": 90, "city": "Thane", "coupon": "X"}]
accepted, quarantined, problems = [], [], {}
for e in batch:
    issues = [f"missing {k}" for k in expected if k not in e]
    issues += [f"bad type {k}" for k in expected if k in e and not isinstance(e[k], expected[k])]
    for i in issues:
        problems[i] = problems.get(i, 0) + 1
    (quarantined if issues else accepted).append(e["order_id"])
print("Accepted   :", accepted)
print("Quarantined:", quarantined)
print("Problems   :", problems)
''', notes={8: 'Check 1 :: Required fields that are absent.', 9: 'Check 2 :: Fields present but with the wrong type, such as a number sent as text.', 12: 'Route :: One expression chooses which list to append to.'},
         tryit='Event O4 has an extra <code>coupon</code> key and is accepted. Should new fields be allowed? Add a rule that only reports them as warnings.'),
]

QUIZ = [
    dict(q='Which of these is semi-structured data?', options=['A MySQL table of employees', 'A JSON event from a mobile app', 'A CCTV video', 'A scanned cheque image'], answer=1,
         why='JSON carries field names inside each record but has no fixed table shape: <b>semi-structured</b>.'),
    dict(q='A server log line “13:02:11 order=O1 status=PLACED” is best described as:', options=['Structured', 'Semi-structured', 'Unstructured', 'Not data'], answer=1,
         why='It is text, but with a predictable pattern of key=value pairs that can be parsed into fields: semi-structured.'),
    dict(q='What does “flattening” nested JSON mean?', options=['Compressing it', 'Turning nested lists into flat rows, usually one row per item', 'Deleting nested fields', 'Converting it to an image'], answer=1,
         why='Flattening (or exploding) produces one row per item, repeating the parent fields, so tables and SQL can use it.'),
    dict(q='How is unstructured data such as photos usually made searchable in a data platform?', options=['By putting the image bytes in a table column', 'By storing the file in object storage and adding metadata and extracted labels', 'By converting it to CSV', 'It cannot be searched'], answer=1,
         why='The file stays in object storage; a metadata row (path, size, time, labels from a model) is what analysts query.'),
    dict(q='Which shape of data usually makes up the largest share of all data stored?', options=['Structured', 'Semi-structured', 'Unstructured', 'All are equal'], answer=2,
         why='Video, images, audio and documents are large and numerous, so <b>unstructured</b> data is the biggest share by volume.'),
    dict(q='After an app update, “amount” arrives as the text “₹420” instead of the number 420. This is an example of:', options=['Data skew', 'Schema drift', 'Replication', 'Partitioning'], answer=1,
         why='A change in field types or names without warning is <b>schema drift</b>. Schema checks and data contracts catch it.'),
    dict(q='An order with 3 items and 2 coupons is exploded on both lists in one step. How many rows result?', options=['3', '5', '6', '2'], answer=2,
         why='Exploding two independent lists multiplies them: 3 × 2 = 6 rows, which can double-count money if you sum prices.'),
    dict(q='What is a data contract?', options=['A legal agreement to buy data', 'An agreed, versioned schema between the team producing data and the teams using it', 'A database licence', 'A backup policy'], answer=1,
         why='A data contract fixes field names, types and rules for changes, and is checked automatically before releases.'),
]

REVISION = [
    '<b>Structured</b>: fixed schema, rows and columns (SQL tables, CSV). Easiest to query.',
    '<b>Semi-structured</b>: labels inside each record, flexible and nested (JSON, XML, logs, Avro). Parse and flatten.',
    '<b>Unstructured</b>: no data model (text, images, audio, video, PDFs). Add metadata and extract features.',
    'Flatten / explode nested lists into one row per item; never sum a repeated parent value.',
    'Logs are parsed with split or regular expressions; text becomes labels with keywords or language models.',
    '<b>Schema drift</b> = fields change silently. Defend with schema checks, quarantine tables and <b>data contracts</b>.',
    'Warehouses store JSON natively (VARIANT, JSON, STRUCT/ARRAY); AI search uses embeddings of unstructured data.',
]
FAQ = [
    ('Differentiate structured, semi-structured and unstructured data with examples.', 'Structured data follows a fixed schema of rows and columns with defined types, for example a bank transactions table. Semi-structured data has tags or keys that describe fields but no fixed table shape, and records can be nested or vary, for example JSON app events, XML files or server logs. Unstructured data has no predefined model, for example images, videos, audio recordings, scanned PDFs and free-text reviews. Structured data is queried directly with SQL; semi-structured data is parsed and flattened; unstructured data needs feature extraction (OCR, speech-to-text, NLP, image models) before analysis.'),
    ('Is a CSV file always structured?', 'Usually yes, when it has a consistent header and every row has the same columns and types. A CSV with inconsistent columns, embedded free text or mixed types behaves more like semi-structured data and needs validation before loading.'),
    ('Why is semi-structured data popular in big data?', 'It is flexible: producers can add fields without changing a central schema, nested data maps naturally to real objects (an order with items), and formats like JSON are easy for applications to produce. The trade-off is that consumers must handle missing, new and changed fields.'),
    ('How do you process unstructured data at scale?', 'Store the raw files in object storage, record metadata for each file, then run extraction jobs in parallel (for example with Spark or a cloud service): OCR for documents, speech-to-text for audio, image classification for photos and language models for text. Save the extracted fields as structured tables linked by ids, and keep the originals for reprocessing.'),
    ('What is schema drift and how do you handle it?', 'Schema drift is an unannounced change in the structure of incoming data, such as a renamed field, a new field or a changed type. Handle it with schema validation on every batch, quarantine tables for failing records, alerts on row counts and nulls, parsers that accept known versions, and versioned data contracts agreed with the producing team.'),
]

PRACTICE_INTRO = 'Exercises on reading, flattening and validating mixed data. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Count JSON keys', stmt='Print the keys of a JSON order and how many there are.', inp='{"id": "O1", "city": "Pune", "amount": 420}',
         code='''import json
o = json.loads('{"id": "O1", "city": "Pune", "amount": 420}')
print(list(o), len(o))
''', explain='<code>json.loads</code> returns a dictionary; <code>list(o)</code> gives its keys.'),
    dict(level='easy', title='Shape of each value', stmt='For each value, print “structured row” for a tuple, “semi-structured” for a dict and “unstructured” for a string.', inp='(1, "Pune"), {"a": 1}, "nice food"',
         code='''for v in [(1, "Pune"), {"a": 1}, "nice food"]:
    if isinstance(v, tuple):
        print(v, "-> structured row")
    elif isinstance(v, dict):
        print(v, "-> semi-structured")
    else:
        print(v, "-> unstructured")
''', explain='<code>isinstance</code> checks the type of each value.'),
    dict(level='easy', title='Read a CSV text', stmt='Read the CSV text and print the total amount.', inp='id,amount / O1,120 / O2,80',
         code='''import csv, io
text = "id,amount\\nO1,120\\nO2,80\\n"
rows = list(csv.DictReader(io.StringIO(text)))
print("Total:", sum(int(r["amount"]) for r in rows))
''', explain='<code>csv.DictReader</code> uses the header row as keys; values arrive as text, so convert with <code>int</code>.'),
    dict(level='medium', title='Flatten items', stmt='Print one line per item: order id, dish, qty.', inp='{"id": "O5", "items": [{"dish": "dosa", "qty": 2}, {"dish": "chai", "qty": 1}]}',
         code='''order = {"id": "O5", "items": [{"dish": "dosa", "qty": 2}, {"dish": "chai", "qty": 1}]}
for it in order["items"]:
    print(order["id"], it["dish"], it["qty"])
''', explain='Loop over the nested list and repeat the parent id on each line.'),
    dict(level='medium', title='Parse key=value logs', stmt='Turn each log line into a dictionary and print the riders who picked orders.', inp='3 lines',
         code='''lines = ["rider=R1 status=PICKED", "rider=R2 status=WAITING", "rider=R3 status=PICKED"]
picked = []
for ln in lines:
    f = dict(p.split("=") for p in ln.split())
    if f["status"] == "PICKED":
        picked.append(f["rider"])
print(picked)
''', explain='Each <code>key=value</code> pair becomes a dictionary entry.'),
    dict(level='advanced', title='Keys across versions', stmt='Events from two app versions have different keys. Print keys common to both, keys only in v1 and keys only in v2.', inp='v1: id, amount, city · v2: id, amount, city_name, coupon',
         code='''v1 = {"id", "amount", "city"}
v2 = {"id", "amount", "city_name", "coupon"}
print("Common :", sorted(v1 & v2))
print("Only v1:", sorted(v1 - v2))
print("Only v2:", sorted(v2 - v1))
''', explain='Set operations quickly show renamed (city → city_name) and new (coupon) fields.'),
    dict(level='advanced', title='Null rate per field', stmt='For each field, print the percentage of records where it is missing or None.', inp='4 records',
         code='''records = [{"id": 1, "city": "Pune", "coupon": None}, {"id": 2, "city": None},
           {"id": 3, "city": "Thane", "coupon": "X"}, {"id": 4}]
fields = ["id", "city", "coupon"]
for f in fields:
    missing = sum(1 for r in records if r.get(f) is None)
    print(f"{f:7} {missing / len(records) * 100:.0f}% missing")
''', explain='A sudden jump in a null rate is often the first sign of schema drift.'),
    dict(level='business', title='Storage by shape', stmt='A company stores 2 TB of tables, 30 TB of JSON logs and 400 TB of images and video. Print the percentage of each.', inp='2, 30, 400 TB',
         code='''sizes = {"structured": 2, "semi-structured": 30, "unstructured": 400}
total = sum(sizes.values())
for k, v in sizes.items():
    print(f"{k:16} {v / total * 100:5.1f}%")
''', explain='Unstructured data dominates storage, even when most reports come from the small structured share.'),
    dict(level='business', title='Complaint share', stmt='Out of reviews labelled by a model, print the share of each complaint type among complaints only.', inp='late 420, cold 180, wrong item 90, praise 1310',
         code='''labels = {"late": 420, "cold": 180, "wrong item": 90, "praise": 1310}
complaints = {k: v for k, v in labels.items() if k != "praise"}
total = sum(complaints.values())
for k, v in sorted(complaints.items(), key=lambda x: -x[1]):
    print(f"{k:10} {v / total * 100:.0f}%")
''', explain='Text has become numbers a manager can act on: most complaints are about late delivery.'),
]

SCN_INTRO = 'Situations with mixed data that come up in real teams and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
