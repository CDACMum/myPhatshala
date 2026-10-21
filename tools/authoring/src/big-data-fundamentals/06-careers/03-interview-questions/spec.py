import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-careers', lesson='03-interview-questions', n='6.3',
    module_label='Module 6 · Careers',
    title='Big data and data engineering interview questions with answers',
    desc='The most common data engineering interview questions with model answers: SQL (joins, window functions, deduplication, second highest), Python, big data concepts (5 Vs, ETL vs ELT, lake vs warehouse vs lakehouse, Parquet, partitioning, CAP), Spark (shuffles, skew, broadcast joins, repartition vs coalesce), Kafka and streaming, data modelling (star schema, SCD type 2), pipeline design and behavioural questions. Animations, a scoring rubric and SQL practice for your PC.',
    og_desc='SQL, Spark, Kafka, modelling, design and HR: the data engineering interview questions you will actually be asked, with model answers.',
    minutes=40, level='Beginner → Advanced',
    lead='Most data engineering interviews ask the same core questions in different words. In this lesson you learn <b>how to answer any technical question</b> (clarify, assume, solve, test, trade off), watch an answer being scored on a rubric, solve the classic <b>top-N-per-group SQL</b> question on real data, debug a slow Spark job aloud, run a <b>45-minute design round</b>, and practise with a <b>question bank of model answers</b>.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'SQL practice for your PC'],
)

RUN = dict(
    heading='Practise SQL interview questions in your browser',
    intro='<p>Python’s built-in <code>sqlite3</code> runs real SQL. The program creates a small orders table with a duplicate row and answers a classic question. Then try the challenges: deduplication, ranking functions, running totals, LAG and a Python counting question.</p>',
    code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (order_id TEXT, city TEXT, amount INT);
INSERT INTO orders VALUES ('O1','Pune',320), ('O2','Pune',450), ('O3','Thane',610),
  ('O4','Pune',150), ('O5','Thane',610), ('O6','Pune',900), ('O2','Pune',450);
""")
# Q: total revenue per city, counting each order once
sql = """SELECT city, SUM(amount) FROM (SELECT DISTINCT * FROM orders)
         GROUP BY city ORDER BY city"""
for row in db.execute(sql):
    print(row)
''',
    anno=[
        ('sql = """SELECT city, SUM(amount) FROM (SELECT DISTINCT * FROM orders)', 'Deduplicate first: O2 was loaded twice and would inflate Pune’s total.'),
        ('db = sqlite3.connect(":memory:")', 'An in-memory database: nothing to install, perfect for practice.'),
    ],
    tasks=[
        dict(label='1 · Revenue per city', hint='Press <b>Run</b>. Remove <code>DISTINCT</code> and see Pune’s total grow by the duplicate 450.', code=None),
        dict(label='2 · Find duplicates', hint='Classic question: which order_ids appear more than once?',
             code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE o (id TEXT); INSERT INTO o VALUES ('O1'),('O2'),('O2'),('O3'),('O3'),('O3');")
print(db.execute("SELECT id, COUNT(*) FROM o GROUP BY id HAVING COUNT(*) > 1").fetchall())
'''),
        dict(label='3 · ROW_NUMBER vs RANK vs DENSE_RANK', hint='See how each function treats the tie at 610.',
             code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE s (name TEXT, amt INT); INSERT INTO s VALUES ('A',900),('B',610),('C',610),('D',450);")
sql = """SELECT name, amt, ROW_NUMBER() OVER w, RANK() OVER w, DENSE_RANK() OVER w
         FROM s WINDOW w AS (ORDER BY amt DESC)"""
for r in db.execute(sql):
    print(r)
'''),
        dict(label='4 · Running total', hint='SUM() OVER (ORDER BY day) adds up revenue day by day.',
             code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE d (day TEXT, rev INT); INSERT INTO d VALUES ('10-01',770),('10-02',760),('10-03',1710);")
for r in db.execute("SELECT day, rev, SUM(rev) OVER (ORDER BY day) FROM d"):
    print(r)
'''),
        dict(label='5 · Day-over-day change (advanced)', hint='LAG gives the previous row’s value. Compute change from the previous day.',
             code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE d (day TEXT, rev INT); INSERT INTO d VALUES ('10-01',770),('10-02',760),('10-03',1710);")
sql = "SELECT day, rev, rev - LAG(rev) OVER (ORDER BY day) AS change FROM d"
for r in db.execute(sql):
    print(r)
'''),
        dict(label='6 · Python round (advanced)', hint='A common Python question: the top 2 most frequent cities in a list of orders, without pandas.',
             code='''from collections import Counter
orders = ["Pune", "Thane", "Pune", "Nashik", "Pune", "Thane"]
print(Counter(orders).most_common(2))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: five classic SQL interview questions',
    intro='<p>This program builds an orders table (with a duplicate row, as real data often has) and runs five classic questions: second highest amount, duplicates, top 2 per city with ties, a running total and customers active on several days. Try writing each query yourself before reading the solution. Save it as <code>sql_interview.py</code>.</p>',
    items=[
        dict(title='Second highest, duplicates, top-N, running total, repeat customers', file='sql_interview.py',
             cmd=open(os.path.join(HERE, 'sql_interview.py')).read() + '\n# In a terminal:  python sql_interview.py',
             output=open(os.path.join(HERE, 'sql_interview.out')).read(),
             note='Recorded from a real run with Python 3.13 and its built-in SQLite (window functions need SQLite 3.25 or newer, included in all recent Python versions). The same SQL works in PostgreSQL, Spark SQL, BigQuery and most warehouses with small changes.'),
    ],
)

TRACE = dict(
    heading='Deduplicating records, step by step',
    intro='<p>A favourite interview task in Python: keep the latest record per order ID. Watch the dictionary keep only the newest version of each order.</p>',
    code='''records = [("O1", 1, "placed"), ("O2", 1, "placed"),
           ("O1", 2, "delivered"), ("O2", 2, "cancelled")]
latest = {}
for oid, version, status in records:
    if oid not in latest or version > latest[oid][0]:
        latest[oid] = (version, status)
print(latest)
''',
    notes={5: 'Newer? :: Keep a record only if it is the first or has a higher version.', 6: 'Store :: The dictionary holds one entry per order ID.'},
)

WORKED_INTRO = 'Four interview problems across SQL, Python and Spark thinking. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Python · strings', title='Is it a palindrome? (ignore case and spaces)',
         problem='<p>A common warm-up in online tests. Check whether a phrase reads the same forwards and backwards, ignoring case and spaces.</p>',
         inp='"Nitin", "Data Engineer"',
         approach=['Lower-case and remove spaces.',
                   'Compare the string with its reverse.',
                   'Test both examples.'],
         code='''def is_pal(s):
    clean = s.lower().replace(" ", "")
    return clean == clean[::-1]
for s in ["Nitin", "Data Engineer"]:
    print(s, "->", is_pal(s))
''', notes={2: 'Normalise :: Make the comparison fair before checking.', 3: 'Reverse :: [::-1] reverses a string.'},
         tryit='Also ignore punctuation, so “Was it a car or a cat I saw?” counts as a palindrome.'),
    dict(level='i', tag='SQL · consecutive days', title='Customers who ordered on consecutive days',
         problem='<p>Using LAG, find customers who placed orders on two consecutive days.</p>',
         inp='(customer, day number)',
         approach=['Deduplicate to one row per customer per day.',
                   'LAG(day) over each customer’s days gives the previous day.',
                   'Keep rows where day − previous = 1.'],
         code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""CREATE TABLE o (c TEXT, d INT);
INSERT INTO o VALUES ('Asha',1),('Asha',2),('Ravi',1),('Ravi',3),('Zoya',5),('Zoya',6),('Zoya',6);""")
sql = """SELECT DISTINCT c FROM (
  SELECT c, d, LAG(d) OVER (PARTITION BY c ORDER BY d) AS prev FROM (SELECT DISTINCT c, d FROM o))
WHERE d - prev = 1"""
print(db.execute(sql).fetchall())
''', notes={5: 'LAG :: The previous day for the same customer.'},
         tryit='Find customers with three consecutive days. Hint: use LAG twice or compare with LAG(d, 2).'),
    dict(level='i', tag='Python · grouping', title='Average order value per city without pandas',
         problem='<p>Given (city, amount) pairs, compute the average per city using only the standard library, as many interviews require.</p>',
         inp='5 (city, amount) pairs',
         approach=['Keep a running sum and count per city in dictionaries.',
                   'Divide at the end.',
                   'Round for display.'],
         code='''from collections import defaultdict
rows = [("Pune", 320), ("Thane", 610), ("Pune", 450), ("Pune", 900), ("Thane", 200)]
total, count = defaultdict(int), defaultdict(int)
for city, amt in rows:
    total[city] += amt
    count[city] += 1
print({c: round(total[c] / count[c], 1) for c in total})
''', notes={5: 'Accumulate :: One pass, constant memory per city: the same idea Spark uses for aggregation.'},
         tryit='Also return the city with the highest average.'),
    dict(level='a', tag='Spark thinking · skew', title='Detect a skewed key before the job runs',
         problem='<p>Before a big join, sample the keys. Flag any key holding more than 10% of rows, and estimate how many salt buckets would bring it to about the average partition size.</p>',
         inp='key counts, 50 partitions',
         approach=['Total rows and each key’s share.',
                   'Flag keys above 10%.',
                   'Salt buckets ≈ key rows ÷ average rows per partition.'],
         code='''import math
counts = {"M001": 3_00_000, "M002": 40_000, "M003": 35_000, "TEST": 6_00_000, "M004": 25_000}
total, partitions = sum(counts.values()), 50
avg = total / partitions
for key, n in counts.items():
    share = n / total
    if share > 0.10:
        print(f"{key}: {share:.0%} of rows -> salt into {math.ceil(n / avg)} buckets")
''', notes={4: 'Average :: Rows per partition if data were perfectly even.', 7: 'Skew :: Hot keys get split across several partitions by salting.'},
         tryit='The TEST key is test data. What is the better fix than salting it?'),
]

QUIZ = [
    dict(q='Which clause filters groups after aggregation?', options=['WHERE', 'HAVING', 'ORDER BY', 'LIMIT'], answer=1,
         why='HAVING works on groups, so it can use aggregates such as COUNT(*) > 1.'),
    dict(q='For amounts 900, 610, 610, 450, what does DENSE_RANK give?', options=['1, 2, 3, 4', '1, 2, 2, 4', '1, 2, 2, 3', '1, 1, 2, 3'], answer=2,
         why='Ties share a rank and no number is skipped. RANK would give 1, 2, 2, 4.'),
    dict(q='A Spark stage has one task taking 40× longer than the others. The most likely cause is:', options=['Too much memory', 'Data skew on a key', 'Too few columns', 'Parquet files'], answer=1,
         why='A single straggler task usually processes a much larger partition caused by a hot key.'),
    dict(q='Which Spark operation causes a shuffle?', options=['filter', 'select', 'groupBy', 'withColumn'], answer=2,
         why='groupBy is a wide transformation: rows with the same key must move to the same partition.'),
    dict(q='In Kafka, ordering is guaranteed:', options=['Across the whole topic', 'Within a partition', 'Across all topics', 'Never'], answer=1,
         why='Use the same key for events that must stay in order so they go to the same partition.'),
    dict(q='What makes a daily pipeline idempotent?', options=['Appending every run', 'Overwriting or merging the date partition so re-runs give the same result', 'Running it twice', 'Using more workers'], answer=1,
         why='Overwrite-by-partition or MERGE on keys prevents duplicates when a run is repeated.'),
    dict(q='SCD type 2 handles a customer moving from Pune to Mumbai by:', options=['Overwriting the city', 'Inserting a new row with validity dates and keeping the old one', 'Deleting the customer', 'Ignoring the change'], answer=1,
         why='Type 2 keeps history; type 1 overwrites.'),
    dict(q='In a design round, what should you do first?', options=['Draw Kafka', 'Clarify requirements and estimate scale', 'Pick a cloud', 'Write code'], answer=1,
         why='Requirements and estimates decide whether you need streaming, which storage, and how much capacity.'),
]

REVISION = [
    'Answer structure: clarify → assume → solve simply → test edge cases → scale and trade-offs → summarise.',
    'SQL must-knows: joins, WHERE vs HAVING, dedup with ROW_NUMBER, ROW_NUMBER/RANK/DENSE_RANK, LAG/LEAD, running totals.',
    'Python: dicts/sets/Counter, chunked file reading, generators, error handling, no-pandas grouping.',
    'Spark: driver/executors, lazy evaluation, narrow vs wide, shuffles, broadcast joins, skew, repartition vs coalesce.',
    'Kafka: partitions, offsets, consumer groups, ordering per key, delivery semantics, watermarks.',
    'Modelling: star schema, facts/dimensions, SCD 1 vs 2; pipelines: idempotent, incremental, CDC, backfills.',
    'Design rounds: requirements, estimates, architecture, failures, cost and governance; STAR for behavioural.',
]
FAQ = [
    ('What are the most common data engineering interview questions?', 'SQL problems with joins, aggregation and window functions (top-N per group, duplicates, running totals); Python data-handling questions; concepts such as ETL vs ELT, data lake vs warehouse, Parquet and partitioning; Spark questions on shuffles, partitions, joins and skew; Kafka basics; data modelling with star schemas and slowly changing dimensions; a pipeline design scenario; and questions about your projects and behaviour.'),
    ('How should I prepare for a data engineering interview in 30 days?', 'Practise SQL daily (window functions especially), revise Python data structures and file handling, review Spark and Kafka concepts with diagrams, practise two or three design scenarios with a fixed structure, prepare a two-minute project story and five STAR stories, and do mock interviews where you explain your thinking aloud.'),
    ('What Spark questions are asked in interviews?', 'Typical questions cover the driver and executors, lazy evaluation, transformations and actions, narrow and wide dependencies, shuffles, partitioning and repartition versus coalesce, broadcast joins, handling data skew, caching, adaptive query execution, file formats and debugging slow or failing jobs using the Spark UI.'),
    ('How do I answer a system design question for data pipelines?', 'Clarify requirements (latency, volume, history, correctness, consumers), estimate scale with simple arithmetic, propose an architecture from ingestion to storage, processing and serving, explain failure handling (retries, idempotency, late data, reconciliation), and discuss cost, security and governance, ending with a short summary and possible improvements.'),
    ('What if I don’t know the answer to an interview question?', 'Say so honestly, then reason from what you do know, relate it to a similar tool or concept, and describe how you would find out. Interviewers value clear reasoning and honesty over confident guessing.'),
]

PRACTICE_INTRO = 'Interview-style problems in Python and SQL. The last two are business-flavoured design questions.'
PROBLEMS = [
    dict(level='easy', title='Reverse words', stmt='Print the words of "big data is fun" in reverse order.', inp='"big data is fun"',
         code='''print(" ".join("big data is fun".split()[::-1]))
''', explain='Split, reverse the list, join.'),
    dict(level='easy', title='Second largest', stmt='Print the second largest distinct number in [5, 9, 9, 3, 7].', inp='list',
         code='''print(sorted(set([5, 9, 9, 3, 7]))[-2])
''', explain='Remove duplicates first so a tie for the maximum doesn’t count twice.'),
    dict(level='easy', title='Count with HAVING', stmt='With SQLite, print the cities with more than 1 order from [Pune, Pune, Thane].', inp='3 rows',
         code='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE o (c TEXT); INSERT INTO o VALUES ('Pune'),('Pune'),('Thane');")
print(db.execute("SELECT c FROM o GROUP BY c HAVING COUNT(*) > 1").fetchall())
''', explain='HAVING filters after grouping.'),
    dict(level='medium', title='First non-repeating character', stmt='Print the first character that appears only once in "aabbcdc".', inp='"aabbcdc"',
         code='''from collections import Counter
s = "aabbcdc"
c = Counter(s)
print(next(ch for ch in s if c[ch] == 1))
''', explain='Count first, then scan in order.'),
    dict(level='medium', title='Merge two sorted lists', stmt='Merge [1, 4, 7] and [2, 3, 8] into one sorted list without calling sort.', inp='two sorted lists',
         code='''a, b, out, i, j = [1, 4, 7], [2, 3, 8], [], 0, 0
while i < len(a) and j < len(b):
    if a[i] <= b[j]:
        out.append(a[i]); i += 1
    else:
        out.append(b[j]); j += 1
print(out + a[i:] + b[j:])
''', explain='The merge step of merge sort; external sorting in big data works the same way.'),
    dict(level='advanced', title='Latest status per order', stmt='From [("O1",1,"placed"),("O1",3,"delivered"),("O1",2,"shipped")], print the status with the highest version.', inp='versioned records',
         code='''r = [("O1", 1, "placed"), ("O1", 3, "delivered"), ("O1", 2, "shipped")]
print(max(r, key=lambda x: x[1])[2])
''', explain='The same logic as ROW_NUMBER() ... ORDER BY version DESC = 1, or a MERGE in a lakehouse.'),
    dict(level='advanced', title='Sessionise clicks', stmt='Click times (minutes) [0, 5, 12, 50, 52, 120]. A new session starts after a gap over 30. Print the number of sessions.', inp='times',
         code='''t = [0, 5, 12, 50, 52, 120]
print(1 + sum(1 for a, b in zip(t, t[1:]) if b - a > 30))
''', explain='Sessionisation is a common streaming and SQL interview problem (LAG + gap rule).'),
    dict(level='business', title='Estimate for a design round', stmt='50 lakh orders a day, 2 KB each, kept 3 years, 3 copies. Print storage in TB.', inp='as given',
         code='''print(round(50e5 * 2e3 * 365 * 3 * 3 / 1e12, 1), "TB")
''', explain='Quick estimates like this anchor every design discussion.'),
    dict(level='business', title='Peak throughput', stmt='Lunch (12–2 pm) carries 40% of 50 lakh daily orders. Print average orders per second in that window.', inp='40% in 2 hours',
         code='''print(round(50e5 * 0.40 / (2 * 3600)))
''', explain='Peak windows, not daily averages, decide capacity.'),
]

SCN_INTRO = 'More interview situations to practise. Say your answer aloud first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
