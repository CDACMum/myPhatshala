import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='01-introduction', lesson='01-what-is-big-data-the-5-vs', n='1.1',
    module_label='Module 1 · Introduction',
    title='What is big data? The 5 Vs explained',
    desc='What big data really means, explained with the 5 Vs: Volume, Velocity, Variety, Veracity and Value. Real Indian examples (UPI, canteen orders, food delivery), animations, Python programs you can run, a line-by-line tracer, quiz and interview scenarios.',
    og_desc='Measure the 5 Vs of big data yourself with Python, and see why Excel and one computer stop being enough.',
    minutes=28, level='Beginner → Advanced',
    lead='Big data is not just “a very big file”. In this lesson you follow a ₹20 chai payment and see the five things that make data “big”: how much there is, how fast it arrives, how mixed it is, how trustworthy it is, and what it is worth. Then you measure all five on real data with Python, watch them light up during a midnight sale, and go deeper into peaks, value decay and the cost of keeping data.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Run on your PC'],
)

RUN = dict(
    heading='Measure the 5 Vs yourself',
    intro='<p>A tiny slice of the canteen\'s data: six payment records as JSON text, two photos and a review. The program measures each V. Read it first, then try the challenges, which include an Excel-limit calculator, a size converter and a record that breaks the program.</p>',
    code='''import json

# Six payment events, as they arrive from the app (JSON text)
events = [
    '{"id": "T1", "item": "chai", "amount": 20, "sec": 1}',
    '{"id": "T2", "item": "vada pav", "amount": 25, "sec": 1}',
    '{"id": "T3", "item": "chai", "amount": 20, "sec": 2}',
    '{"id": "T2", "item": "vada pav", "amount": 25, "sec": 1}',
    '{"id": "T4", "item": "samosa", "amount": -15, "sec": 2}',
    '{"id": "T5", "item": "chai", "amount": 20, "sec": 3}',
]
data = {"json": events, "image": ["chai.jpg", "menu.png"], "text": ["Best chai!"]}

# VOLUME: how much data?
size = sum(len(e) for e in events)
print("Volume  :", len(events), "records,", size, "bytes")

# VELOCITY: how fast does it arrive?
records = [json.loads(e) for e in events]
seconds = len({r["sec"] for r in records})
print("Velocity:", len(records) / seconds, "records per second")

# VARIETY: how many kinds of data?
print("Variety :", len(data), "kinds ->", ", ".join(data))

# VERACITY: how many records can we trust?
seen, clean, bad = set(), [], 0
for r in records:
    if r["id"] in seen or r["amount"] <= 0:
        bad += 1
        continue
    seen.add(r["id"])
    clean.append(r)
print("Veracity:", bad, "bad records out of", len(records))

# VALUE: what does the clean data tell us?
sales = {}
for r in clean:
    sales[r["item"]] = sales.get(r["item"], 0) + r["amount"]
print("Value   : income Rs", sum(sales.values()), "| best seller:", max(sales, key=sales.get))
''',
    anno=[
        ('json.loads(e)', 'Turns JSON text into a Python dictionary. Real pipelines do this millions of times per second, which is part of why velocity is hard.'),
        ('len({r["sec"] for r in records})', 'A <b>set</b> keeps only unique values, so this counts how many different seconds the records arrived in.'),
        ('r["id"] in seen', 'The retry sent <code>T2</code> twice. Without this check the income would be counted twice: a veracity problem.'),
        ('r["amount"] <= 0', 'A payment of −15 is impossible, so it is rejected instead of silently reducing the total.'),
        ('max(sales, key=sales.get)', 'Finds the item with the highest sales: a small example of turning data into a decision (value).'),
    ],
    tasks=[
        dict(label='1 · 5 Vs meter', hint='Press <b>Run</b>. Then add a seventh event with <code>"sec": 3</code> and watch Volume and Velocity change. Add <code>"audio": ["order.mp3"]</code> to <code>data</code> and Variety goes up.',
             code=None),
        dict(label='2 · When does Excel give up?', hint='<b>Predict first:</b> how many days of canteen orders fit in one Excel sheet? Then change <code>orders_per_day</code> to 3700 × 500 for a chain of 500 canteens.',
             code='''EXCEL_MAX_ROWS = 1_048_576      # rows in one Excel sheet
orders_per_day = 3700

days = EXCEL_MAX_ROWS // orders_per_day
print("One sheet holds", days, "days of orders")
print("That is about", round(days / 30, 1), "months")
print("One year needs", orders_per_day * 365, "rows")
'''),
        dict(label='3 · Bytes to TB', hint='This function keeps dividing by 1024 until the number is small. Try <code>human(10_000_000_000 * 250)</code>: one month of UPI-scale payment records.',
             code='''def human(n):
    units = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n = n / 1024
        i = i + 1
    return str(round(n, 2)) + " " + units[i]

print(human(250))                # one payment record
print(human(250 * 3700 * 365))   # canteen, one year
print(human(5 * 1024**4))        # 5 TB
'''),
        dict(label='4 · Find the bad records', hint='Real data has many kinds of problems. This program gives a reason for each rejected record. Add a record with <code>"item": ""</code> and a new rule that rejects it.',
             code='''records = [
    {"id": "T1", "payer": "riya", "amount": 20},
    {"id": "T2", "payer": "aman", "amount": 25},
    {"id": "T1", "payer": "riya", "amount": 20},
    {"id": "T3", "payer": None, "amount": 30},
    {"id": "T4", "payer": "neha", "amount": -10},
]
seen = set()
for r in records:
    if r["id"] in seen:
        print(r["id"], "-> rejected: duplicate")
    elif r["payer"] is None:
        print(r["id"], "-> rejected: missing payer")
    elif r["amount"] <= 0:
        print(r["id"], "-> rejected: invalid amount")
    else:
        print(r["id"], "-> OK")
    seen.add(r["id"])
'''),
        dict(label='5 · One broken record (predict!)', hint='<b>Predict first:</b> the last event was cut off by a network error. What happens? Read the error, then wrap <code>json.loads</code> in <code>try</code> / <code>except json.JSONDecodeError</code> so the program skips it and continues. Real pipelines must survive bad records.',
             code='''import json

events = [
    '{"id": "T1", "amount": 20}',
    '{"id": "T2", "amount": 25}',
    '{"id": "T3", "amount": 2',
]
total = 0
for e in events:
    r = json.loads(e)
    total = total + r["amount"]
    print("Read", r["id"], "running total", total)
print("Total:", total)
''', expect='error'),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: make a file Excel can\'t open',
    intro='<p>This program writes 15 lakh fake canteen orders to <code>orders.csv</code> (about 39 MB). Save it as <code>gen_orders.py</code> and run it with Python on your own computer. Then try opening the CSV in Excel. The second program reads the same file with Python in about two seconds. That is the point: <b>too big for Excel is not the same as big data</b>.</p>',
    items=[
        dict(title='Create 15 lakh rows', file='gen_orders.py',
             cmd=open(os.path.join(HERE, 'gen_orders.py')).read() + '\n# In a terminal:  python gen_orders.py',
             output='''Rows written : 1500000
File size    : 38.8 MB
Time taken   : 2.3 seconds
Excel limit  : 1048576 rows -> this file is too big for one sheet''',
             note='Output recorded from a real run. Your time will differ with your computer\'s speed; the row count and size will match. Opening this file in Excel shows “File not loaded completely” and keeps only the first 10,48,576 rows.'),
        dict(title='Read all 15 lakh rows with Python', file='read_orders.py',
             cmd=open(os.path.join(HERE, 'read_orders.py')).read() + '\n# In a terminal:  python read_orders.py',
             output='''Read 15 lakh rows in 2.1 seconds
poha       Rs 8,989,200
coffee     Rs 7,512,175
vada pav   Rs 7,485,075
chai       Rs 6,013,200
samosa     Rs 4,497,150''',
             note='Recorded from a real run. One ordinary computer handles this easily, so it is not big data. Make it 1,500 crore rows arriving every day and one computer is no longer enough. Lesson 1.2 shows exactly where it breaks.'),
    ],
)

TRACE = dict(
    heading='Cleaning payments, one line at a time',
    intro='<p>Veracity in action. Four records arrive: one is a duplicate caused by a retry, and one has an impossible amount. Step through and watch <code>seen</code>, <code>income</code> and the console. Objects #1 (the list) and #2–#5 (each record is a tuple) live on the heap.</p>',
    code='''records = [("T1", "chai", 20), ("T2", "samosa", 15),
           ("T1", "chai", 20), ("T3", "chai", -20)]
seen = set()
income = 0
for txn, item, amount in records:
    if txn in seen or amount <= 0:
        print("skip", txn)
        continue
    seen.add(txn)
    income = income + amount
print("Clean income: Rs", income)
''',
    notes={1: 'Data arrives :: Four records, each a tuple of (transaction id, item, amount).',
           3: 'Setup :: An empty <b>set</b> will remember every transaction id we have already counted.',
           (6, 3): 'Veracity check :: <code>T1</code> is already in <code>seen</code>: this is the retry duplicate.',
           (6, 4): 'Veracity check :: <code>T3</code> is new, but the amount −20 is impossible.',
           11: 'Value :: Only trustworthy records were added: 20 + 15 = 35 from 2 real orders. A blind sum (20 + 15 + 20 − 20) also gives 35 here by coincidence, but it would count 4 orders instead of 2. A total that looks right can still hide bad data.'},
)

WORKED_INTRO = 'Four problems, from beginner to advanced. Each program runs live, and each is traced so you can see how the data builds up in memory.'
EXAMPLES = [
    dict(level='b', tag='Retail · Volume', title='How much data does a supermarket chain create?',
         problem='<p>A supermarket chain has <b>2,000 stores</b>. Each store prints about <b>400 bills a day</b>, and each bill record is about <b>600 bytes</b>. How much bill data does one store create in a year, and how much does the whole chain create?</p>',
         inp='600 bytes × 400 bills × 365 days × 2000 stores',
         approach=['Multiply bytes per bill by bills per day and days per year for one store.',
                   'Multiply by the number of stores for the chain.',
                   'Convert bytes to MB (÷ 1024²) and GB (÷ 1024³) so the numbers are readable.'],
         code='''bytes_per_bill = 600
bills_per_day = 400
stores = 2000

one_store = bytes_per_bill * bills_per_day * 365
chain = one_store * stores
print("One store per year :", round(one_store / 1024**2, 1), "MB")
print("Whole chain per year:", round(chain / 1024**3, 1), "GB")
''', notes={5: 'Volume :: One store: 600 × 400 × 365 = 8,76,00,000 bytes.', 6: 'Volume :: The chain: 2,000 times more.'},
         tryit='Press <b>Run</b>. Then add clickstream data: the chain\'s app logs 50 events per bill at 300 bytes each. How fast does the total grow? This is how “small” data becomes big data.'),
    dict(level='b', tag='Media · Variety', title='Sort a folder by kind of data',
         problem='<p>A company\'s shared folder has files from many teams. Count how many files are <b>structured</b>, <b>semi-structured</b> and <b>unstructured</b>, using the file extension.</p>',
         inp='sales.csv, cctv.mp4, app_log.json, invoice.pdf, stock.csv, server.log, review.txt',
         approach=['Make a dictionary that maps known extensions to a kind.',
                   'For each file, take the part after the last dot.',
                   'Look it up; anything unknown counts as unstructured. Count each kind in another dictionary.'],
         code='''files = ["sales.csv", "cctv.mp4", "app_log.json", "invoice.pdf",
         "stock.csv", "server.log", "review.txt"]
kinds = {"csv": "structured", "json": "semi-structured", "log": "semi-structured"}

count = {}
for f in files:
    ext = f.split(".")[-1]
    kind = kinds.get(ext, "unstructured")
    count[kind] = count.get(kind, 0) + 1
print(count)
''', notes={3: 'Rules :: Known extensions and their kind. Everything else will be treated as unstructured.'},
         tryit='Add <code>"photo.jpg"</code> and <code>"orders.xml"</code>. Which kind should XML be? Add a rule for it.'),
    dict(level='i', tag='Food delivery · Velocity', title='Find the busiest minute',
         problem='<p>A food-delivery app logs the minute of every order. Find how many orders arrived in each minute, and the <b>peak minute</b>. Systems must be built for the peak, not the average.</p>',
         inp='13:00, 13:00, 13:01, 13:01, 13:01, 13:02',
         approach=['Count orders per minute in a dictionary.',
                   'Use <code>max</code> with <code>key=per_min.get</code> to find the minute with the highest count.',
                   'Compare the peak with the average.'],
         code='''times = ["13:00", "13:00", "13:01", "13:01", "13:01", "13:02"]
per_min = {}
for t in times:
    per_min[t] = per_min.get(t, 0) + 1
peak = max(per_min, key=per_min.get)
print("Orders per minute:", per_min)
print("Peak:", peak, "with", per_min[peak], "orders")
print("Average:", len(times) / len(per_min), "orders per minute")
''', notes={5: 'Velocity :: The peak minute. Servers must cope with this, not with the average.'},
         tryit='Add five more <code>"13:02"</code> orders. The average changes a little, but the peak jumps. That is why systems are sized for peaks.'),
    dict(level='a', tag='Fintech · capacity planning', title='How much storage will we need in five years?',
         problem='<p>A payments company adds <b>78 GB</b> of new records a day today, and the daily amount grows <b>40% a year</b>. Records are kept for at least five years. The platform keeps <b>3 copies</b> of every file for safety, and the Parquet format compresses the data about <b>4 times</b>. How much disk is needed at the end of each year?</p>',
         inp='78 GB/day, 40% growth, 3 copies, 4× compression, 5 years',
         approach=['Year 1 adds 78 × 365 GB. Each later year adds 40% more than the year before: multiply by 1.4 each time.',
                   'Keep a running total of raw data, because old data is not deleted within five years.',
                   'Stored size = raw total × copies ÷ compression. Convert GB to TB by dividing by 1024.'],
         code='''daily_gb = 78
growth = 0.40
copies = 3
compression = 4
raw_total = 0
for year in range(1, 6):
    added = daily_gb * 365 * (1 + growth) ** (year - 1)
    raw_total = raw_total + added
    stored = raw_total * copies / compression
    print(f"Year {year}: raw {raw_total / 1024:6.1f} TB -> disk {stored / 1024:6.1f} TB")
''', notes={7: 'Growth :: Each year adds 40% more than the year before. This is compound growth, like interest on a fixed deposit.', 9: 'Storage :: Copies multiply the size, compression divides it.'},
         tryit='Change <code>copies</code> to 2 and <code>compression</code> to 8 (a well-tuned columnar format). How much disk do you save in year 5? Then try 60% growth: capacity plans are very sensitive to the growth rate.'),
]

QUIZ = [
    dict(q='Which of these is the best definition of big data?', options=['Any file larger than 1 GB', 'Data too large, fast or varied for traditional single-machine tools to handle in acceptable time', 'Data stored in the cloud', 'Data that has more than one million rows'], answer=1,
         why='Big data is defined by the limits of traditional tools, not by one fixed size. A million rows is too many for Excel but easy for Python on one laptop.'),
    dict(q='Thousands of card payments arrive every second and each needs a fraud decision in about one second. Which V is this mainly about?', options=['Volume', 'Velocity', 'Variety', 'Value'], answer=1,
         why='<b>Velocity</b> is the speed at which data arrives and must be processed.'),
    dict(q='Which of these is semi-structured data?', options=['A MySQL table of employees', 'A JSON response from a mobile app', 'A CCTV video', 'A scanned PDF letter'], answer=1,
         why='JSON has labelled fields but no fixed table shape: <b>semi-structured</b>. Tables are structured; video and scanned PDFs are unstructured.'),
    dict(q='A dashboard shows more income than the bank statement because retries created duplicate records. Which V is the problem?', options=['Volume', 'Variety', 'Veracity', 'Velocity'], answer=2,
         why='<b>Veracity</b> is about trustworthiness and quality. Duplicates, missing and wrong values are veracity problems.'),
    dict(q='Which three Vs were in the original description of big data (2001)?', options=['Volume, Velocity, Variety', 'Volume, Veracity, Value', 'Velocity, Variety, Value', 'Variety, Veracity, Volume'], answer=0,
         why='Doug Laney described <b>Volume, Velocity and Variety</b>. Veracity and Value were added later.'),
    dict(q='How many bytes are in 1 GB (binary, as your computer counts)?', options=['1,000,000', '1,048,576', '1,073,741,824', '1,024'], answer=2,
         why='1 GB = 1024 × 1024 × 1024 = <b>1,073,741,824</b> bytes. 1,048,576 is 1 MB (and also Excel\'s row limit).'),
    dict(q='A college has 3,000 students\' marks in one table. Is it big data?', options=['Yes, because it is important data', 'Yes, because it has many columns', 'No, one database or spreadsheet handles it easily', 'No, because marks are numbers'], answer=2,
         why='It fits easily on one machine and normal tools handle it in milliseconds. Importance doesn\'t make data “big”.'),
    dict(q='An app gets 2,000 orders a minute on average, but 30,000 in the minute after a cricket final ends. What should the system be designed to handle?', options=['The average, 2,000 a minute', 'The peak, 30,000 a minute (with some headroom)', 'The median minute', 'Whatever the cheapest server can do'], answer=1,
         why='Systems are sized for the <b>peak</b>, not the average. Here the peak-to-average ratio is 15, so a system built for the average would fail exactly when most customers are using it.'),
    dict(q='Why do companies move old data to cheaper “cold” storage instead of keeping everything on fast disks?', options=['Old data becomes corrupted on fast disks', 'Its value falls with age, so cheaper storage keeps the cost below the value', 'The law forbids keeping old data on SSDs', 'Cold storage is faster'], answer=1,
         why='Value decays with age: a record is used constantly at first and rarely later. Moving it from hot to warm to cold storage keeps the cost in line with its value.'),
    dict(q='Order volumes jump on Diwali and drop in the monsoon; the same word means different things in different reviews. Which extra V describes this?', options=['Visualisation', 'Variability', 'Validity', 'Volatility of hardware'], answer=1,
         why='<b>Variability</b> means the rate or meaning of data changes over time. It is the most common “6th V”.'),
]

REVISION = [
    '<b>Big data</b> = too big, too fast or too varied for traditional single-machine tools.',
    '<b>Volume</b> (how much) · <b>Velocity</b> (how fast) · <b>Variety</b> (how mixed) · <b>Veracity</b> (how trustworthy) · <b>Value</b> (how useful).',
    'First 3 Vs: Doug Laney, 2001. Veracity and Value added later.',
    '<b>Structured</b> (tables) · <b>semi-structured</b> (JSON, logs, XML) · <b>unstructured</b> (photos, video, audio, free text).',
    'Units: KB → MB → GB → TB → PB → EB, each × 1024.',
    'Excel holds 10,48,576 rows per sheet. Too big for Excel ≠ big data.',
    'Rule of thumb: it is big data when you need <b>more than one machine</b> to store or process it in time.',
    'Engineers measure each V: TB and growth (volume), events per second and latency (velocity), sources and formats (variety), % bad records (veracity), money gained vs cost (value).',
    'Design for the <b>peak</b>, not the average. Peak-to-average ratio = peak rate ÷ average rate.',
    'Value falls with age: memory → hot → warm → cold → delete or anonymise when retention ends.',
    'Extra Vs: <b>Variability</b> (rate or meaning changes) and <b>Visualisation</b>.',
]
FAQ = [
    ('What is big data? Explain the 5 Vs with examples.', 'Big data is data whose size, speed or variety exceeds what traditional single-machine tools can handle in acceptable time. Volume: UPI\'s billions of monthly payments. Velocity: thousands of payments per second needing fraud checks. Variety: tables, JSON logs, photos and reviews together. Veracity: duplicate and broken records that must be cleaned. Value: the decisions the data enables, such as blocking fraud or planning stock.'),
    ('What is the difference between structured, semi-structured and unstructured data?', 'Structured data has a fixed schema of columns and types (SQL tables). Semi-structured data has labels or tags but a flexible shape (JSON, XML, logs). Unstructured data has no predefined model (images, video, audio, free text). Each needs different storage and processing.'),
    ('Is a 10 GB CSV file big data?', 'Usually not. A single modern machine can process 10 GB with tools like Python, Pandas (in chunks) or a database. It becomes big data when the size, arrival speed or processing deadline needs a cluster of machines.'),
    ('Why is veracity important?', 'Because wrong data leads to wrong decisions. Duplicates inflate totals, missing values bias averages and fake records hide fraud. Big data pipelines spend a lot of effort on validation, de-duplication and cleaning before analysis.'),
    ('Why can\'t traditional RDBMS handle big data well?', 'A traditional RDBMS usually runs on one server, so it is limited by that machine\'s disk, memory and CPU, and scaling up gets very expensive. It also expects a fixed schema, while big data includes semi-structured and unstructured data. Big data systems spread storage and processing across many cheaper machines.'),
]

FAQ.append(('Are there more than 5 Vs of big data?', 'Yes. Some authors add Variability (the rate or meaning of data changes over time), Visualisation (presenting huge data so people can understand it), Validity and Volatility, giving 7 or 10 Vs. Most syllabi and interviews expect the 5 Vs: Volume, Velocity, Variety, Veracity and Value. Mention Variability as the common sixth.'))
FAQ.append(('Why are systems designed for peak load and not average load?', 'Because customers arrive in bursts: festival sales, salary days, the end of a cricket match. If capacity matches the average, the system fails exactly when demand is highest. Engineers measure the peak-to-average ratio and design for the peak with some headroom, often scaling machines up automatically for known peaks.'))

PRACTICE_INTRO = 'Small programs about measuring and cleaning data. The last three are business tasks you could meet in a data engineering interview.'
PROBLEMS = [
    dict(level='easy', title='TB to GB', stmt='A company stores 5 TB of logs. Print how many GB that is (1 TB = 1024 GB).', inp='5 TB',
         code='tb = 5\nprint(tb * 1024, "GB")\n', explain='Each step up the unit ladder is × 1024.'),
    dict(level='easy', title='Count records and bytes', stmt='Given a list of three log lines, print how many records there are and their total size in bytes (one character = one byte here).', inp='3 log lines',
         code='''logs = ["08:01 INFO login riya", "08:02 INFO pay 20", "08:02 WARN retry"]
print("Records:", len(logs))
print("Bytes:", sum(len(x) for x in logs))
''', explain='<code>len</code> of a string is its number of characters; <code>sum</code> adds them up.'),
    dict(level='easy', title='Room left in Excel', stmt='A report already has 2,50,000 rows. How many more rows fit in one Excel sheet (limit 1,048,576)?', inp='250000',
         code='used = 250_000\nprint("Rows left:", 1_048_576 - used)\n', explain='Underscores in numbers are allowed in Python and make big numbers readable.'),
    dict(level='medium', title='Remove duplicate orders', stmt='Remove duplicate order ids but keep the first occurrence and the original order.', inp='T1, T2, T1, T3, T2',
         code='''orders = ["T1", "T2", "T1", "T3", "T2"]
seen, unique = set(), []
for o in orders:
    if o not in seen:
        seen.add(o)
        unique.append(o)
print(unique)
''', explain='The set gives fast “already seen?” checks; the list keeps the order.'),
    dict(level='medium', title='Count missing values', stmt='Count how many records are missing a <code>city</code> (the value is <code>None</code> or an empty string).', inp='4 customer records',
         code='''customers = [
    {"name": "Riya", "city": "Pune"},
    {"name": "Aman", "city": None},
    {"name": "Neha", "city": ""},
    {"name": "Kabir", "city": "Mumbai"},
]
missing = sum(1 for c in customers if not c["city"])
print("Missing city:", missing, "of", len(customers))
''', explain='Both <code>None</code> and <code>""</code> are “falsy”, so <code>not c["city"]</code> catches both.'),
    dict(level='advanced', title='Peak-to-average ratio', stmt='Orders per minute during one evening are given. Print the average, the peak and the peak-to-average ratio (one decimal place).', inp='[120, 135, 980, 140, 110, 1250, 130]',
         code='''per_minute = [120, 135, 980, 140, 110, 1250, 130]
average = sum(per_minute) / len(per_minute)
peak = max(per_minute)
print("Average:", round(average, 1))
print("Peak:", peak)
print("Peak-to-average ratio:", round(peak / average, 1))
''', explain='The ratio tells you how much spare capacity the system needs above the average. A ratio above 3 already means a system sized for the average will fail during the rush.'),
    dict(level='advanced', title='Data quality score', stmt='Check each payment record: a missing id, an amount of zero or less, and a repeated id are problems. Count each problem and print the percentage of good records.', inp='6 records',
         code='''records = [
    {"id": "T1", "amount": 20}, {"id": "T2", "amount": -5},
    {"id": "T1", "amount": 20}, {"id": None, "amount": 30},
    {"id": "T3", "amount": 45}, {"id": "T4", "amount": 15},
]
seen = set()
problems = {"missing id": 0, "bad amount": 0, "duplicate": 0}
good = 0
for r in records:
    if r["id"] is None:
        problems["missing id"] += 1
    elif r["amount"] <= 0:
        problems["bad amount"] += 1
    elif r["id"] in seen:
        problems["duplicate"] += 1
    else:
        seen.add(r["id"])
        good += 1
print(problems)
print(f"Quality score: {good / len(records) * 100:.0f}% good records")
''', explain='Each record is checked in order and counted under its first problem. Real pipelines publish this score every day so a sudden drop (for example, a broken app release) is noticed before anyone trusts the numbers.'),
    dict(level='business', title='Monthly cloud storage bill', stmt='A fintech stores 2.3 TB of new payment data every month and keeps all of it. Cloud storage costs Rs 1.80 per GB per month (illustrative). Print the bill for month 1 and month 12.', inp='2.3 TB per month, Rs 1.80/GB-month',
         code='''new_gb = 2.3 * 1024
rate = 1.80
for month in [1, 12]:
    stored = new_gb * month
    print("Month", month, ": Rs", round(stored * rate))
''', explain='Data accumulates, so the bill grows every month. This is why companies set retention rules: Volume has a cost, so it must create Value.'),
    dict(level='business', title='Average payments per second', stmt='A payments company processed 1,800 crore transactions last month (30 days). Print the average per second.', inp='18,000,000,000 in 30 days',
         code='''txns = 18_000_000_000
seconds = 30 * 24 * 3600
print(round(txns / seconds), "per second on average")
''', explain='30 × 24 × 3600 = 25,92,000 seconds in the month. Peaks are several times the average.'),
    dict(level='business', title='Busiest hour for staffing', stmt='A canteen logs the hour of each order. Print the hour with the most orders so the owner can put an extra person on the counter.', inp='hours: 8, 9, 13, 13, 16, 13, 8, 16, 13',
         code='''hours = [8, 9, 13, 13, 16, 13, 8, 16, 13]
count = {}
for h in hours:
    count[h] = count.get(h, 0) + 1
busiest = max(count, key=count.get)
print("Busiest hour:", busiest, "with", count[busiest], "orders")
''', explain='Count with a dictionary, then pick the key with the highest value. Data → decision is Value.'),
]

SCN_INTRO = 'Situations freshers and junior data engineers really face. Decide your answer first, then open the model answer.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Retail · tool choice</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Let's set up Hadoop for our sales data”</h4>
      <p class="scn__situation">A mid-sized retailer has 5 GB of sales data, growing by about 1 GB a year. A manager read about big data and wants to set up a Hadoop cluster. You are asked for your opinion.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you judge whether data is really “big”, instead of picking tools because they are popular?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>5 GB growing at 1 GB a year is <b>not big data</b>. One database server (PostgreSQL or MySQL) or Python with Pandas handles it comfortably, and reports will run in seconds.</p>
        <ul>
          <li>A cluster adds cost, setup and maintenance with no benefit at this size.</li>
          <li>Put the data in a proper database, index it, and build reports or a BI dashboard on top.</li>
          <li>Revisit if the data grows by orders of magnitude, for example if clickstream or real-time data is added.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid saying:</b> “More data tools are always better.” Use the simplest tool that meets the need.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Fintech · data quality</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>The dashboard shows more money than the bank</h4>
      <p class="scn__situation">The daily revenue dashboard shows ₹12.4 lakh, but the bank settlement says ₹11.9 lakh. Engineering says the app sometimes retries payments when the network is slow.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you recognise a veracity problem and know how to fix it at the source and in the pipeline?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>Retries are probably creating <b>duplicate records</b> for the same payment, so they are counted twice.</p>
        <ol>
          <li>Check for repeated transaction ids in the raw data for that day, and compare totals after removing them.</li>
          <li>De-duplicate in the pipeline on a unique key (transaction id) before calculating revenue.</li>
          <li>Fix the source: make the payment API <b>idempotent</b>, so a retry with the same id doesn't create a new record.</li>
          <li>Add a daily reconciliation check against the bank settlement that alerts when they differ.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> “adjusting” the dashboard number by hand without finding the cause.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · storage cost</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>“Keep everything forever, just in case”</h4>
      <p class="scn__situation">Your team stores every click from the app forever. The storage bill grows every month, and nobody has used clicks older than a year. Your lead asks what you would propose.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand that Volume has a cost and must be balanced against Value, and that personal data has legal limits?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>Data should be kept as long as it creates value or is legally required, and no longer.</p>
        <ul>
          <li>Agree a <b>retention policy</b> with the business: for example, raw clicks for 90 days, daily summaries for years.</li>
          <li>Move older data to cheaper <b>archive storage</b>, and compress it into columnar formats like Parquet.</li>
          <li>Remove or anonymise personal data that isn't needed. Privacy laws such as India's Digital Personal Data Protection Act, 2023 expect personal data not to be kept longer than necessary.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> deleting data without checking legal and audit requirements first.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Telecom · customer support</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Analysing call recordings with sales data</h4>
      <p class="scn__situation">The support head wants to know why customers cancel. The evidence is spread across a sales database (tables), chat transcripts (JSON) and call recordings (audio files). How would you bring them together?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you handle Variety: different shapes of data that must be linked?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>Store all three in a <b>data lake</b> in their raw form, then convert each into something that can be joined.</p>
        <ul>
          <li>Audio → text with a speech-to-text service, then text → topics or sentiment.</li>
          <li>Chat JSON → flatten into rows: customer id, time, message, topic.</li>
          <li>Join everything on <b>customer id</b> with the sales tables, and compare customers who cancelled with those who stayed.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> forcing audio and JSON into one rigid table before you know which fields matter.</p>
      </div></details>
    </article>'''
