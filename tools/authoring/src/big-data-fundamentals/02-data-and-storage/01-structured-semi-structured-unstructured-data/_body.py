import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
files = [('orders.csv', 'green', 'table'), ('app_events.json', 'blue', '{ }'), ('rider_gps.log', 'blue', 'log'),
         ('support_chats.txt', 'acc', 'Aa'), ('menu_photos/', 'acc', 'img'), ('invoices.pdf', 'acc', 'PDF')]
sc = box(14, 20, 150, 120, 'card') + t(89, 40, 'tiffingo_sample.zip', 9.5, bold=True, mono=True)
sc += ''.join(t(26, 60 + k * 14, f, 8.4, 'ink2', anchor='start', mono=True) for k, (f, _, _) in enumerate(files))
sc += arrow(170, 80, 206, 80, 'ink3', 2)
cols = [('Structured', 'green', ['orders.csv'], 'rows and columns'), ('Semi-structured', 'blue', ['app_events.json', 'rider_gps.log'], 'labels, flexible shape'),
        ('Unstructured', 'acc', ['support_chats.txt', 'menu_photos/', 'invoices.pdf'], 'no fixed model')]
for k, (name, tone, fl, sub) in enumerate(cols):
    x = 214 + k * 142
    sc += box(x, 20, 132, 120, tone) + t(x + 66, 40, name, 10, TXT[tone] if tone != 'acc' else 's-acc', bold=True) + t(x + 66, 54, sub, 8.4, 'ink2')
    sc += ''.join(t(x + 66, 78 + j * 16, f, 8.6, 'ink', mono=True) for j, f in enumerate(fl))
scene_svg = scene('A zip file with six files sorted into three groups: structured, semi-structured and unstructured.', sc,
                  'One company, one day, <tspan font-weight="700" class="s-acc">three very different shapes of data</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Kabir’s internship at TiffinGo starts next semester. To help him prepare, the data team sends a small practice dump: <code>tiffingo_sample.zip</code>. He unzips it on his laptop and finds six very different files. He tries to open all of them in Excel. Only one opens properly.</p>

{scene_svg}

K> Sir, the CSV opened fine. The JSON file is one giant line of brackets, the log file is just text, and there’s a folder of photos and a PDF. How do I put this into one table?
A> You don’t, at least not directly. You’ve just met the three shapes of data: <b>structured</b>, <b>semi-structured</b> and <b>unstructured</b>. Each needs a different way to store, read and query.
R> Sir, in Lesson 1.1 you said most new data is unstructured. So is the CSV the odd one out?
A> In volume, yes. Photos, videos, chats and documents are the biggest part of the world’s data. But most business reports still run on structured tables. A big part of a data engineer’s job is turning the messy shapes into tidy tables.
K> So the JSON and the logs are somewhere in between?
A> Exactly. They have labels but no fixed table shape. Today you’ll flatten a nested JSON order into rows, pull fields out of log lines, turn support chats into numbers, and see what happens when an app update quietly changes the shape of the data.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Three shapes of data at three levels
L1> A spice rack, a tiffin box and a grocery bag
      <ul>
        <li><b>Structured</b> is a spice rack: every jar has a fixed place and a printed label. You find turmeric instantly. Example: a marks sheet, a bank statement table.</li>
        <li><b>Semi-structured</b> is a tiffin box: each compartment is labelled (“dal”, “rice”), but one day there are three compartments and another day four. Example: a JSON message from an app.</li>
        <li><b>Unstructured</b> is a bag of groceries: everything is in there, but there are no labels. You must look at each item to know what it is. Example: a photo, a voice note, a free-text review.</li>
      </ul>
      <p><b>Quick test:</b> can you write column names for it without looking at every item? Yes → structured. Names exist but vary → semi-structured. No names at all → unstructured.</p>
L2> Schemas, nesting and how each shape is queried
      <ul>
        <li><b>Schema:</b> the description of fields and their types. Structured data has it <i>before</i> storing (schema-on-write); semi-structured data carries field names <i>inside</i> each record (self-describing); unstructured data has none.</li>
        <li><b>Nesting:</b> JSON can hold lists inside records (an order with three items). To analyse it in a table, you <b>flatten</b> it: one row per item, repeating the order fields.</li>
        <li><b>Logs</b> are text lines with a predictable pattern, so they are parsed into fields with split or regular expressions.</li>
        <li><b>Unstructured data</b> is made usable by adding <b>metadata</b> (file name, size, upload time, camera details) and by <b>extracting features</b>: words from text, labels from images, transcripts from audio.</li>
        <li><b>Query tools:</b> SQL for tables; JSON functions in databases, MongoDB queries or Spark for semi-structured; search engines (Elasticsearch, OpenSearch) and ML models for unstructured.</li>
      </ul>
L3> Schema drift, variant columns and embeddings
      <ul>
        <li><b>Schema drift:</b> semi-structured sources change silently: new keys, missing keys, renamed fields, a number arriving as text. Pipelines need schema checks and <b>data contracts</b> (an agreed schema between the team producing data and the team using it).</li>
        <li><b>Warehouses store JSON natively:</b> Snowflake’s <code>VARIANT</code>, BigQuery’s <code>JSON</code> and <code>STRUCT/ARRAY</code> types, and Spark’s <code>struct</code>, <code>array</code> and <code>map</code> columns let you query nested data without flattening everything first.</li>
        <li><b>Explode carefully:</b> flattening two independent arrays in one record multiplies rows (3 items × 2 coupons = 6 rows), which silently double-counts money.</li>
        <li><b>Unstructured data for AI:</b> text, images and audio are converted into <b>embeddings</b> (lists of numbers that capture meaning) and stored in vector indexes, so you can search “photos of burnt rotis” or “complaints about late delivery” by meaning.</li>
        <li><b>Size vs value:</b> unstructured data is the largest share of storage, but structured data often drives most decisions. Plan storage costs and processing effort for each shape separately.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Structured data</b> conforms to a predefined schema of rows and columns with fixed data types, such as tables in a relational database. <b>Semi-structured data</b> does not follow a fixed tabular schema but contains tags, keys or markers that separate fields and describe hierarchy, so each record is self-describing; examples are JSON, XML, YAML and log files. <b>Unstructured data</b> has no predefined data model or organisation, such as free text, images, audio, video and scanned documents, and must be processed (parsed, tagged or analysed) before it can be queried.',
    '<b>Structured</b>: neat rows and columns, every row the same shape. <b>Semi-structured</b>: every value has a label, but records can have different labels and lists inside them. <b>Unstructured</b>: no labels at all, like a photo or a paragraph of text. You have to look inside to find out what it says.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Schema', 'The list of fields and their data types: <code>order_id: int, city: text, amount: decimal</code>.'),
    ('Self-describing', 'Each record carries its own field names, like <code>{"city": "Pune"}</code>.'),
    ('Nested data', 'A record that contains another record or a list, such as an order containing a list of items.'),
    ('Flatten / explode', 'Turn nested data into flat rows, typically one row per item in a list.'),
    ('Parsing', 'Reading text and splitting it into fields, such as pulling the date and status code out of a log line.'),
    ('Metadata', 'Data about data: a photo’s size, format, upload time and location.'),
    ('Schema drift', 'When the shape of incoming data changes without warning.'),
    ('Embedding', 'A list of numbers that represents the meaning of a text, image or sound, used for AI search.'),
]) + '''

  <h3>Common formats of each shape</h3>
''' + facts([
    ('Structured', 'Database tables (MySQL, PostgreSQL, Oracle), CSV with a fixed header, spreadsheet tables, Parquet/ORC tables'),
    ('Semi-structured', 'JSON, XML, YAML, Avro and Protobuf messages, server and app logs, emails (headers + body), NoSQL documents'),
    ('Unstructured', 'Free text, PDFs and scanned documents, images (JPG, PNG), audio (MP3, WAV), video (MP4), CCTV feeds'),
]) + lv + '''
EXAM> Draw a three-column table: <b>definition, schema, examples, storage, tools to process, ease of analysis</b>. Give two examples of each kind from one business (for example, a bank: transactions table, mobile-app JSON logs, cheque images). That earns full marks on most “types of big data” questions.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Structured', 'Fixed columns and types. Easy to store, index and query with SQL. Bank transactions, orders, marks, inventory.', 'Rows and columns'),
    ('Semi-structured', 'Labels inside each record, shape can vary, can be nested. App events, API responses, server logs, sensor messages.', 'Keys and nesting'),
    ('Unstructured', 'No predefined fields. Needs extra processing (OCR, speech-to-text, image models, text analysis) before analysis.', 'No fixed model'),
]) + '''

  <h3>Side by side</h3>
''' + table(['', 'Structured', 'Semi-structured', 'Unstructured'], [
    ['<b>Schema</b>', 'Fixed, defined before storing', 'Flexible, inside each record', 'None'],
    ['<b>Example</b>', 'Orders table', 'App event JSON, logs', 'Review text, menu photos, call recordings'],
    ['<b>Stored in</b>', 'RDBMS, warehouse, Parquet tables', 'Document DBs (MongoDB), lake files, Kafka topics', 'Object storage (S3, ADLS, GCS), HDFS'],
    ['<b>Queried with</b>', 'SQL', 'JSON functions, Spark, MongoDB queries', 'Search engines, ML models, OCR, speech-to-text'],
    ['<b>Ease of analysis</b>', 'Easiest', 'Medium: parse and flatten first', 'Hardest: extract features first'],
    ['<b>Share of total volume</b>', 'Smallest', 'Large', 'Largest (most estimates put it at a big majority)'],
], minw=600) + '''

  <h3>Where data comes from</h3>
''' + table(['Source', 'What it produces', 'Usual shape'], [
    ['Business transactions', 'Orders, payments, invoices, bookings', 'Structured'],
    ['Machines and apps', 'Server logs, clickstreams, API responses', 'Semi-structured'],
    ['Sensors and IoT', 'GPS pings, smart-meter readings, temperature', 'Semi-structured (often time series)'],
    ['People', 'Reviews, chats, emails, social posts, photos, voice notes', 'Unstructured'],
    ['Documents', 'Scanned forms, contracts, invoices as PDF', 'Unstructured'],
]) + '''
TIP> The same fact can arrive in all three shapes: “order O1043 cost ₹420” can be a row in a table, a field in a JSON event, and a sentence in a customer’s complaint email. Good pipelines link them with a common key such as the order id.'''

# ---------------------------------------------------------------- steps
c1 = '''import csv, io
text = "order_id,city,amount\\nO1043,Pune,420\\nO1044,Mumbai,250\\n"
for row in csv.DictReader(io.StringIO(text)):
    print(row["order_id"], row["city"], int(row["amount"]))'''
c2 = '''import json
event = json.loads('{"order_id": "O1043", "city": "Pune", "items": [{"dish": "thali", "qty": 1, "price": 220}, {"dish": "lassi", "qty": 2, "price": 100}]}')
for item in event["items"]:
    print(event["order_id"], item["dish"], item["qty"] * item["price"])'''
c3 = '''line = "2026-10-19 13:02:11 rider=R77 order=O1043 lat=18.5204 lon=73.8567 status=PICKED"
parts = line.split()
fields = dict(p.split("=") for p in parts[2:])
print(parts[0], parts[1], fields["order"], fields["status"])'''
c4 = '''review = "Thali was great but the delivery was very late and the lassi was warm"
words = review.lower().split()
labels = [w for w in ["late", "cold", "warm", "great", "spilled"] if w in words]
print("labels:", labels)'''
steps = stepper([
    ('Structured: one row per order',
     code('python', 'read_csv.py', c1, run_code(c1)),
     'Every row has the same three columns, and the types are known. This is the easiest shape: load it into a database and query it with SQL.'),
    ('Semi-structured: an order with a list inside',
     code('python', 'read_json.py', c2, run_code(c2)),
     'The JSON carries its own field names and contains a nested <code>items</code> list. Looping over the list <b>flattens</b> it into one row per item, ready for a table.'),
    ('Semi-structured: a log line with a pattern',
     code('python', 'parse_log.py', c3, run_code(c3)),
     'A log line is text, but it follows a pattern: date, time, then <code>key=value</code> pairs. Splitting by spaces and <code>=</code> turns it into fields.'),
    ('Unstructured: a free-text review',
     code('python', 'review_labels.py', c4, run_code(c4)),
     'The review has no fields. Here a simple keyword list extracts labels; real systems use language models to detect sentiment and topics. The result is structured: <code>order_id, label</code>.'),
    ('Unstructured: a photo of the food',
     '<p>A 3 MB photo arrives with the review. It is stored as a file in object storage, and a row of <b>metadata</b> is saved: file path, size, upload time, order id. An image model can add labels such as “thali, spilled”.</p>',
     'The photo itself never goes into a table. Its <b>path and labels</b> do, so analysts can count “spilled food” complaints by kitchen.'),
    ('Link everything by order id',
     '<p>Now all shapes can be joined: the order row, its items from JSON, the rider’s pickup time from logs, the review labels and the photo metadata, all keyed by <code>O1043</code>.</p>',
     'This is the daily work of a data engineer: bring every shape into a structured, joinable form without losing the raw originals.'),
])

# ---------------------------------------------------------------- two-view animation
def ph(year_or_title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, year_or_title, 9.4, bold=True) + inner)


see = [
    ph('Your order', ''.join(t(138, 70 + k * 18, d, 8.4, anchor='start') + t(222, 70 + k * 18, p, 8.4, anchor='end', bold=True) for k, (d, p) in enumerate([('Thali × 1', '₹220'), ('Lassi × 2', '₹200')])) + fill(138, 112, 84, 1, 'grey') + t(138, 128, 'Total', 9, anchor='start', bold=True) + t(222, 128, '₹420', 9, anchor='end', bold=True) + fill(140, 160, 80, 22, 'acc', rx=11) + t(180, 175, 'PLACE ORDER', 8.4, extra=' style="fill:#fff"', bold=True)),
    ph('Order confirmed', '<circle cx="180" cy="90" r="20" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M171 90l6 6 12-12" style="stroke:var(--green);stroke-width:3;fill:none"/>' + t(180, 134, 'Order O1043', 9, bold=True) + t(180, 150, 'Annapurna Kitchen', 8.4, 'ink2')),
    ph('Rider on the way', '<path d="M140 150 Q170 80 220 70" style="fill:none;stroke:var(--blue);stroke-width:2;stroke-dasharray:4 3"/><circle cx="220" cy="70" r="6" style="fill:var(--green)"/><circle cx="160" cy="118" r="7" style="fill:var(--track)"/>' + t(180, 180, 'Arriving in 12 min', 8.6, 'blue', bold=True)),
    ph('Rate your order', t(180, 70, '★★★☆☆', 14, extra=' style="fill:#E0A100"') + box(136, 82, 88, 44, 'blue', rx=4) + t(142, 96, '“Great thali, but', 7.4, anchor='start') + t(142, 108, 'very late and the', 7.4, anchor='start') + t(142, 120, 'lassi was warm”', 7.4, anchor='start') + fill(150, 134, 60, 40, 'acc', rx=4, opacity=.5) + t(180, 192, '+ photo', 8.4, 'ink2')),
    ph('Help', box(134, 58, 80, 30, 'card', rx=10) + t(174, 77, 'Lassi spilled!', 7.8) + box(146, 96, 80, 30, 'green', rx=10) + t(186, 115, 'Sorry! ₹100 refund', 7.6) + box(134, 134, 80, 22, 'card', rx=10) + t(174, 149, 'Thanks', 7.8)),
    ph('Your month', t(180, 72, '23 orders', 12, bold=True) + t(180, 92, 'Favourite: Thali', 8.6, 'ink2') + ''.join(fill(144 + k * 18, 160 - h, 12, h, 'acc') for k, h in enumerate([20, 34, 28, 50]))),
]
behind = [
    t(180, 24, 'Structured row', 10.5, 'green', bold=True) + box(14, 40, 332, 70, 'card') + ''.join(t(20 + k * 82, 60, h, 8.6, 'ink3', anchor='start', bold=True) for k, h in enumerate(['order_id', 'kitchen', 'city', 'amount'])) + fill(14, 68, 332, 1, 'grey') + ''.join(t(20 + k * 82, 90, v, 9, anchor='start', mono=True) for k, v in enumerate(['O1043', 'K11', 'Pune', '420'])) + t(180, 140, 'Fixed columns, fixed types.', 9.5, 'ink2') + t(180, 158, 'Goes straight into the orders table.', 9.5, 'ink2'),
    t(180, 24, 'Semi-structured event (JSON)', 10.5, 'blue', bold=True) + '<rect x="14" y="36" width="332" height="128" rx="8" class="s-board"/>' + ''.join(t(24, 56 + k * 15, ln, 8.4, anchor='start', mono=True, extra=' style="fill:#9FD3B8"') for k, ln in enumerate(['{"order_id": "O1043",', ' "user": {"id": "U9", "app": "5.2"},', ' "items": [', '   {"dish": "thali", "qty": 1},', '   {"dish": "lassi", "qty": 2}],', ' "coupon": null}'])) + t(180, 190, 'Labels inside, with a list nested in it.', 9.5, 'ink2'),
    t(180, 24, 'Semi-structured log lines', 10.5, 'blue', bold=True) + '<rect x="14" y="36" width="332" height="96" rx="8" class="s-board"/>' + ''.join(t(22, 56 + k * 16, ln, 7.8, anchor='start', mono=True, extra=' style="fill:#9FD3B8"') for k, ln in enumerate(['13:02:11 rider=R77 lat=18.5204 lon=73.8567', '13:02:16 rider=R77 lat=18.5211 lon=73.8559', '13:02:21 rider=R77 lat=18.5219 lon=73.8551', '… one line every 5 seconds per rider'])) + t(180, 160, 'Same pattern on every line: parse into fields.', 9.5, 'ink2') + t(180, 178, 'Thousands of riders → lakhs of lines an hour.', 9.5, 'ink2'),
    t(180, 24, 'Unstructured review + photo', 10.5, 'acc', bold=True) + box(14, 38, 160, 80, 'acc') + t(94, 60, '“Great thali, but', 8.6) + t(94, 74, 'very late and the', 8.6) + t(94, 88, 'lassi was warm”', 8.6) + box(186, 38, 160, 80, 'acc') + fill(226, 50, 80, 50, 'acc', rx=4, opacity=.45) + t(266, 112, 'IMG_2231.jpg · 3 MB', 8, 'ink2') + arrow(180, 124, 180, 140, 'ink3') + box(14, 144, 332, 40, 'green') + t(180, 162, 'extracted: sentiment = mixed · labels = late, warm', 8.6, bold=True) + t(180, 176, 'photo → s3://…/IMG_2231.jpg (metadata row)', 8.4, 'ink2'),
    t(180, 24, 'Unstructured chat → structured ticket', 10.5, 'acc', bold=True) + box(14, 40, 150, 90, 'card') + t(89, 62, 'Lassi spilled!', 8.6) + t(89, 80, 'Sorry! ₹100 refund', 8.6) + t(89, 98, 'Thanks', 8.6) + arrow(170, 85, 196, 85, 'ink3') + box(200, 40, 146, 90, 'green') + ''.join(t(208, 60 + k * 16, ln, 8.2, anchor='start', mono=True) for k, ln in enumerate(['order: O1043', 'topic: spilled', 'refund: 100', 'resolved: yes'])) + t(180, 160, 'A language model labels each chat.', 9.5, 'ink2'),
    t(180, 24, 'Everything joined by order_id', 10.5, 'green', bold=True) + label_box(130, 40, 100, 30, ['O1043'], 'green', 10) + ''.join(label_box(x, 100, 76, 36, [n], tone, 8.6) + arrow(x + 38, 98, 180, 72, 'ink3', 1.2) for x, n, tone in [(10, 'order row', 'green'), (94, 'items (JSON)', 'blue'), (190, 'rider logs', 'blue'), (274, 'review + chat', 'acc')]) + t(180, 170, 'One customer view built from three shapes.', 9.5, 'ink2') + t(180, 186, 'Raw originals kept in the lake.', 9.5, 'ink2'),
]
see_caps = ['Riya builds an order: one thali and two lassis, ₹420 in total.',
            'The app confirms order O1043 from Annapurna Kitchen.',
            'A rider picks it up and the map shows him moving towards her.',
            'She gives three stars, writes a short review and adds a photo.',
            'She tells support the lassi spilled and gets a ₹100 refund.',
            'At the end of the month the app shows her favourite dish and how often she ordered.']
behind_caps = ['The order becomes one <b>structured</b> row: same columns as every other order.',
               'The app also sends a <b>semi-structured</b> JSON event with nested user details and a list of items.',
               'The rider’s phone writes a <b>log line</b> every five seconds: text with a fixed pattern of key=value pairs.',
               'The review text and the photo are <b>unstructured</b>. The text is analysed for labels; the photo is stored as a file with a metadata row.',
               'The support chat is free text too. A model turns it into a structured ticket: topic, refund, resolved.',
               'All shapes are linked by <code>order_id</code>, giving one complete view of the order. The raw files are kept for reprocessing.']
two = anim_two('One order, three shapes', 'What Riya sees, and what the data looks like', 'Riya ordering food in an app',
               'The structured, semi-structured and unstructured data created by the order', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: flatten JSON
js = ['{"order_id": "O1043", "city": "Pune",', ' "items": [', '   {"dish": "thali", "qty": 1, "price": 220},', '   {"dish": "lassi", "qty": 2, "price": 100},', '   {"dish": "gulab jamun", "qty": 1, "price": 60}],', ' "coupon": null}']
def jsonbox(hl=None):
    o = '<rect x="10" y="10" width="340" height="100" rx="8" class="s-board"/>'
    for k, ln in enumerate(js):
        col = '#F5C77E' if (hl and k in hl) else '#9FD3B8'
        o += t(18, 28 + k * 14, ln, 8.2, anchor='start', mono=True, extra=f' style="fill:{col}"')
    return o
def tbl(rows, hdr=('order_id', 'city', 'dish', 'qty', 'price', 'coupon'), y=124):
    xs = [16, 74, 124, 214, 248, 290]
    o = ''.join(t(x, y, h, 7.8, 'ink3', anchor='start', bold=True) for x, h in zip(xs, hdr)) + fill(14, y + 4, 332, 1, 'grey')
    for r, row in enumerate(rows):
        o += ''.join(t(x, y + 18 + r * 14, v, 8, anchor='start', mono=True) for x, v in zip(xs, row))
    return o
R3 = [('O1043', 'Pune', 'thali', '1', '220', 'null'), ('O1043', 'Pune', 'lassi', '2', '100', 'null'), ('O1043', 'Pune', 'gulab jamun', '1', '60', 'null')]
fr = [
    jsonbox() + cap('A nested JSON order: three items inside one record.', 'A table needs one value per cell. How do we get there?', 'blue', y=124, h=44),
    jsonbox({0}) + tbl([('O1043', 'Pune', '', '', '', '')]) + t(180, 188, 'Step 1: copy the top-level fields.', 9.2, bold=True),
    jsonbox({1, 2, 3, 4}) + tbl(R3[:3]) + t(180, 188, 'Step 2: explode the items list: one row per item.', 9.2, bold=True) + t(180, 202, 'Order fields repeat on every row.', 8.6, 'ink2'),
    jsonbox({5}) + tbl(R3) + t(180, 188, 'Step 3: missing or null values become NULL.', 9.2, bold=True) + t(180, 202, 'Never invent a value that wasn’t sent.', 8.6, 'ink2'),
    tbl(R3, y=24) + box(10, 84, 340, 52, 'green') + t(180, 104, 'Order total = 1×220 + 2×100 + 1×60 = ₹480', 9.4, bold=True) + t(180, 122, 'Sum qty × price per order_id. Don’t add a repeated order total per row!', 8.6, 'ink2') + cap('Now SQL works: revenue per dish, per city, per day.', 'The raw JSON is still kept in the lake for reprocessing.', 'card', y=150, h=44),
]
s1 = anim_one('Real-time scenario 1', 'Flatten a nested order into a table',
              'TiffinGo’s app sends every order as nested JSON. The finance dashboard needs a flat table. Watch the three steps every pipeline uses, and the classic mistake to avoid at the end.',
              'JSON → rows', 'A nested JSON order flattened into three table rows', fr,
              ['A JSON order holds a list of three items. A table cell can hold only one value, so the list must be turned into rows.',
               '<b>Copy</b> the top-level fields (order id and city) that apply to the whole order.',
               '<b>Explode</b> the <code>items</code> list: one row per item, repeating the order fields on each row.',
               'Keep missing or null fields as <b>NULL</b>. The coupon was not used, so it stays empty; never fill in a guess.',
               'Now ordinary SQL works. Compute totals from item rows (qty × price). If an order-level total were repeated on every row, summing it would triple-count the order.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: chats -> numbers
cats = [('payment failed', 'red'), ('late delivery', 'acc'), ('wrong item', 'blue'), ('refund status', 'violet'), ('other', 'grey')]
def chart(vals, hl=None):
    o = t(14, 22, 'chats per minute by topic', 9, 'ink2', anchor='start')
    for k, ((n, c), v) in enumerate(zip(cats, vals)):
        y = 34 + k * 22
        o += t(14, y + 11, n, 8.6, anchor='start') + '<rect x="110" y="%d" width="200" height="14" rx="4" class="s-card2"/>' % y
        w = min(200, v // 5)
        if w: o += fill(110, y, w, 14, c if c != 'grey' else 'grey')
        o += t(346, y + 11, str(v), 8.6, anchor='end', bold=True)
    return o
fr2 = [
    ''.join(box(14 + (k % 4) * 86, 14 + (k // 4) * 34, 78, 26, 'card', rx=10) + t(53 + (k % 4) * 86, 31 + (k // 4) * 34, m, 7.6) for k, m in enumerate(['money gone!', 'where is my food??', 'paid twice?', 'UPI debited', 'order not placed', 'refund when?', 'payment stuck', 'app says failed']))
    + cap('20:14 · chats jump from 60 to 1,000 a minute.', 'Free text, many languages, typos. No one can read them all.', 'amber', y=96, h=44) + t(180, 170, 'Unstructured data, arriving fast.', 9.2, 'ink2'),
    box(14, 14, 150, 70, 'card') + t(89, 36, '“paisa kat gaya,', 8.6) + t(89, 50, 'order nahi aaya”', 8.6) + t(89, 70, '(Hinglish)', 8, 'ink3') + arrow(170, 49, 196, 49, 'ink3') + box(200, 14, 146, 70, 'green') + t(273, 40, 'topic: payment failed', 8.6, bold=True) + t(273, 58, 'language: hi-en', 8.4) + t(273, 74, 'confidence: 0.94', 8.4)
    + cap('A language model labels each chat with a topic.', 'Unstructured text becomes a structured row.', 'blue', y=100, h=44),
    chart([620, 140, 60, 120, 60]) + cap('Count labelled chats per minute: payment failures dominate.', '', 'blue', y=150, h=34),
    chart([620, 140, 60, 120, 60]) + '<rect x="108" y="32" width="204" height="18" rx="5" style="fill:none;stroke:#D64545;stroke-width:2.5"/>' + cap('Alert: payment-failed chats are 10× normal.', 'Engineers check the payment gateway: one bank is timing out.', 'red', y=150, h=44),
    chart([90, 150, 60, 260, 60]) + cap('Gateway switched; failures fall. Refund questions rise next,', 'so the app shows an automatic “refund in 2 hours” banner.', 'green', y=150, h=44),
]
s2 = anim_one('Real-time scenario 2', 'Outage night: turning 1,000 chats a minute into numbers',
              'At 20:14 support chats explode. Nobody can read a thousand messages a minute. Watch unstructured text become a structured count that tells engineers exactly what broke.',
              'Unstructured → structured, live', 'Support chats labelled by a model and counted per topic to detect an outage', fr2,
              ['Chats suddenly jump from about 60 to 1,000 a minute. They are free text in English, Hindi and Hinglish, full of typos.',
               'Each chat goes through a language model that outputs a topic, the language and a confidence score: structured fields from unstructured text.',
               'The labelled chats are counted per topic every minute. “Payment failed” is far above everything else.',
               'An alert fires because payment-failure chats are ten times their normal level. Engineers find one bank’s gateway timing out.',
               'Traffic is moved to another gateway, failures drop, and refund questions rise, so the app shows a banner instead of agents answering each one. (Numbers are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): schema drift
def ev(x, y, title, lines, tone):
    o = box(x, y, 164, 86, tone) + t(x + 82, y + 16, title, 8.8, bold=True)
    o += ''.join(t(x + 8, y + 34 + k * 14, ln, 8, anchor='start', mono=True) for k, ln in enumerate(lines))
    return o
v4 = ['"amount": 420', '"city": "Pune"', '"items": [...]']
v5 = ['"amount": "₹420"', '"city_name": "Pune"', '"items": [...]']
fr3 = [
    ev(10, 12, 'App 5.1 event', v4, 'green') + ev(186, 12, 'App 5.2 event (new)', v5, 'amber') + cap('Tuesday: an app update silently changes two fields.', 'amount is now text with ₹, and city was renamed.', 'amber', y=112, h=44),
    ev(10, 12, 'App 5.1 event', v4, 'green') + ev(186, 12, 'App 5.2 event (new)', v5, 'red') + box(10, 110, 340, 40, 'red') + t(180, 128, 'Pipeline: int("₹420") → error · city → NULL', 9, 'red', bold=True) + t(180, 142, '40% of orders dropped or missing a city', 8.6) + t(180, 180, 'Wednesday 9 am: revenue on the dashboard is down 40%. Panic.', 9, bold=True),
    box(10, 12, 340, 70, 'blue') + t(180, 32, 'Schema check before loading', 9.6, 'blue', bold=True) + t(180, 50, 'expected: amount = number · city = text (required)', 8.6, mono=True) + t(180, 66, 'found: amount = text · city missing · city_name new', 8.6, mono=True)
    + cap('Fix 1: compare each batch with the expected schema.', 'Drift is caught in minutes, before the dashboard updates.', 'blue', y=100, h=44),
    label_box(10, 14, 160, 50, ['Good rows', '→ silver table'], 'green', 9.4) + label_box(190, 14, 160, 50, ['Bad rows', '→ quarantine table'], 'red', 9.4) + t(180, 90, 'Nothing is lost, nothing wrong is published.', 9.4, bold=True)
    + cap('Fix 2: quarantine rows that fail, keep the rest flowing.', 'An alert goes to the team that owns the app.', 'blue', y=110, h=44),
    box(10, 12, 340, 84, 'green') + t(180, 32, 'Data contract: orders_event v2', 9.8, 'green', bold=True) + ''.join(t(24, 52 + k * 14, ln, 8.4, anchor='start', mono=True) for k, ln in enumerate(['amount: number (paise) · required', 'city: text · required · renamed only with notice', 'new fields: allowed, optional'])) + cap('Fix 3: a data contract agreed by app and data teams,', 'checked in CI before an app release ships.', 'green', y=110, h=44),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Schema drift: the app update that broke the dashboard',
              'Semi-structured data is flexible, which is also its danger. Watch a small app change silently break a pipeline, and the three defences real teams use.',
              'When the shape changes', 'An app update changes JSON fields, a pipeline breaks, and schema checks, quarantine and a data contract fix it', fr3,
              ['A new app version starts sending <code>amount</code> as text with a rupee sign and renames <code>city</code> to <code>city_name</code>. Nobody tells the data team.',
               'The pipeline fails to convert “₹420” to a number and finds no <code>city</code>. Many orders are dropped or lose their city, and the morning dashboard shows revenue down 40%.',
               '<b>Schema check:</b> every incoming batch is compared with the expected schema (types and required fields). The drift is caught before anything is published.',
               '<b>Quarantine:</b> rows that fail go to a separate table for inspection, while good rows keep flowing. The owning team gets an alert.',
               '<b>Data contract:</b> the app and data teams agree the event schema, version it, and check it automatically before an app release. Renames need notice; new optional fields are fine.'])

realworld = '''  <p>Three live scenarios: flattening nested JSON into a table, turning a flood of support chats into numbers during an outage, and an advanced one about an app update that silently changes the data.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Where each shape shows up at work</h3>
''' + usecase('<rect x="16" y="20" width="88" height="50" rx="6" class="s-soft-green" style="stroke:var(--green)"/><path d="M16 36h88M16 52h88M46 20v50M76 20v50" style="stroke:var(--green)"/>',
              '1. Banks: structured core, unstructured edges', 'Account and transaction tables are strictly structured. Around them sit cheque images, KYC documents (scanned Aadhaar and PAN copies), call-centre recordings and emails, which are processed with OCR and speech-to-text before analysis.', ['Cheque image', '*OCR → fields', 'Transactions table']) + usecase(
    '<text x="60" y="40" text-anchor="middle" font-size="16" font-weight="700" class="s-blue mono">{ }</text><text x="60" y="64" text-anchor="middle" font-size="9" class="s-ink">clickstream</text>',
    '2. Shopping apps: oceans of JSON events', 'Every view, search, add-to-cart and checkout is a JSON event with nested product lists. They are streamed through Kafka, stored raw in the lake, and flattened into tables for funnel and recommendation analysis.', ['App events', '*Flatten in Spark', 'Funnel tables']) + usecase(
    '<rect x="20" y="22" width="80" height="46" rx="6" class="s-board"/><text x="60" y="42" text-anchor="middle" font-size="8" class="mono" style="fill:#9FD3B8">GET /pay 500</text><text x="60" y="56" text-anchor="middle" font-size="8" class="mono" style="fill:#9FD3B8">GET /menu 200</text>',
    '3. Every tech company: logs for monitoring', 'Servers write millions of log lines an hour. They are parsed into fields (time, service, status code, latency) and searched in tools like Elasticsearch/OpenSearch or a log platform to find errors in seconds.', ['Log lines', '*Parse + index', 'Error dashboard']) + usecase(
    '<circle cx="40" cy="45" r="18" class="s-soft-acc" style="stroke:var(--track)"/><path d="M70 30h34M70 45h34M70 60h24" style="stroke:var(--track);stroke-width:3"/>',
    '4. Hospitals and insurance: documents and images', 'Discharge summaries, prescriptions, lab reports and X-rays are unstructured. Insurers extract fields from claim documents to speed up approvals, while keeping the originals for audit.', ['Claim PDFs', '*Extract fields', 'Approval queue'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Six files, and only one opens in Excel', story)
        + part(2, 'definition', 'Definition', 'Structured, semi-structured and unstructured data', definition)
        + part(3, 'types', 'Types and ways to use it', 'Three shapes, compared', types)
        + part(4, 'steps', 'Step by step', 'One food order in every shape', steps)
        + part(5, 'animation', 'See it happen', 'One order: what Riya sees, and what the data looks like', '  <p>Step through the six frames. Left: Riya ordering food. Right: the shape of the data each moment creates.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: working with every shape', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Data engineering · ingestion', 'Fresher', 'Load a JSON API into the warehouse',
            'A partner sends orders through an API as JSON. Each order has a nested list of items and an optional coupon object. Your manager wants revenue per dish in the warehouse by tomorrow.',
            'do you know how to land, flatten and validate semi-structured data?',
            '<ol><li>Land the raw JSON as-is in the lake (bronze) so you can always reprocess.</li><li>Define the target tables: <code>orders</code> (one row per order) and <code>order_items</code> (one row per item, with <code>order_id</code>).</li><li>Explode <code>items</code> into <code>order_items</code>; keep the coupon fields as nullable columns.</li><li>Validate types and required fields; send failing rows to a quarantine table.</li><li>Compute revenue from <code>order_items</code> (qty × price), not from a repeated order total.</li></ol>',
            'flattening straight into one wide table and summing a repeated order-level amount.')
        + scn('Analytics · unstructured', '1–3 years', 'What are customers complaining about?',
              'You have 2 lakh free-text reviews from the last month in English, Hindi and Hinglish. The product head wants the top five complaint themes by city.',
              'can you turn unstructured text into a structured, trustworthy result?',
              '<ul><li>Store the raw reviews with order id, city and date (metadata).</li><li>Clean the text (lower-case, remove emojis or map them, normalise common spellings).</li><li>Classify each review into themes with a language model or a trained classifier; record the label and a confidence score.</li><li>Check a random sample by hand to measure accuracy before trusting the numbers.</li><li>Aggregate counts per theme per city, and show example reviews behind each number.</li></ul>',
              'counting single keywords like “bad” and presenting it as insight without checking accuracy.')
        + scn('Reliability · schema drift', '1–3 years', 'Revenue dropped 40% overnight',
              'The morning dashboard shows revenue down 40%, but the business team says orders were normal. An app release went out yesterday.',
              'do you suspect the data before the business, and know how to prevent it next time?',
              '<p>First, compare raw event counts with orders in the database: if raw counts are normal, the pipeline lost data. Check rejected and quarantined rows and diff the event schema before and after the release; you are likely to find a renamed or retyped field. Fix the parser to handle both versions, backfill the affected day from the raw zone, and publish a corrected dashboard. To prevent repeats: schema checks on every batch, quarantine instead of silent drops, alerts on row-count changes, and a versioned data contract checked before app releases.</p>',
              'telling leadership that revenue fell, or patching the dashboard by hand.')
        + scn('Design · storage choice', 'Fresher', 'Where should each kind of data live?',
              'A new ed-tech start-up has student records, quiz-attempt events from the app, lecture videos and doubt-chat messages. They ask you where to store each.',
              'can you match each shape to sensible storage?',
              '<ul><li><b>Student records</b> (structured, updated often) → a relational database such as PostgreSQL.</li><li><b>Quiz events</b> (semi-structured, high volume) → a stream (Kafka) into the data lake as JSON, then flattened Parquet tables for analysis.</li><li><b>Lecture videos</b> (unstructured, huge) → object storage plus a CDN for streaming; a metadata table for titles, durations and tags.</li><li><b>Doubt chats</b> (unstructured text) → stored raw, labelled by topic, and searchable through a search engine.</li></ul>',
              'putting videos inside database tables, or forcing every event into a fixed table schema on day one.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
