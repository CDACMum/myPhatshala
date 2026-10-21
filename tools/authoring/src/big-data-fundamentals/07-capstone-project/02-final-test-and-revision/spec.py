import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='07-capstone-project', lesson='02-final-test-and-revision', n='7.2',
    module_label='Module 7 · Capstone Project',
    title='Final test, cheat sheet and exam questions: Big Data Fundamentals',
    desc='Revise all of Big Data Fundamentals: a one-page course map, cheat sheets of numbers and comparisons (scale up vs out, row vs columnar, lake vs warehouse, batch vs streaming, MapReduce vs Spark, CP vs AP, ETL vs ELT), how to write 2-, 5- and 10-mark answers, estimation practice, 2-mark and 5-mark questions with model answers, a 50-mark practice paper generator for your PC and a 25-question final test.',
    og_desc='The whole Big Data Fundamentals course on one page, exam answer patterns, a practice-paper generator and a 25-question final test.',
    minutes=45, level='Beginner → Advanced',
    lead='This is the last lesson of the course. You get the <b>whole course on one page</b>, cheat sheets of numbers and comparisons, the pattern for <b>2-, 5- and 10-mark answers</b>, an estimation question solved for full marks, an integrated case answered with every module, <b>question banks with model answers</b>, a practice-paper generator for your PC and a <b>25-question final test</b>.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', '25-question final test'],
)

RUN = dict(
    heading='Flashcards for the whole course',
    intro='<p>A small flashcard program picks terms from every module and shows their meanings. Then try the challenges: estimation drills, unit conversions, a spaced-repetition schedule, a self-scoring quiz and Indian number formatting.</p>',
    code='''import random
cards = {
    "Veracity": "quality and trustworthiness of data (Module 1)",
    "Parquet": "columnar, compressed file format for analytics (Module 2)",
    "Consistent hashing": "ring placement so adding a node moves ~1/N of keys (Module 3)",
    "Replication factor": "number of copies of each block or partition, often 3 (Module 3)",
    "Shuffle": "moving rows between executors so equal keys meet (Module 4)",
    "Consumer group": "consumers sharing a Kafka topic's partitions (Module 4)",
    "Idempotent": "re-running gives the same result (Modules 4 and 7)",
    "Data fiduciary": "organisation deciding why and how personal data is processed (Module 5)",
}
random.seed(7)
for term in random.sample(list(cards), 4):
    print(f"{term:20} -> {cards[term]}")
''',
    anno=[
        ('random.seed(7)', 'Change the seed to get a different set of cards.'),
        ('for term in random.sample(list(cards), 4):', 'Try to say the meaning before reading it.'),
    ],
    tasks=[
        dict(label='1 · Flashcards', hint='Press <b>Run</b>. Add five cards of your own from lessons you find hard.', code=None),
        dict(label='2 · Estimation drill', hint='Convert daily totals to per-second rates. Try 50 crore requests a day.',
             code='''for name, per_day in [("orders", 50e5), ("payments", 80e7), ("page views", 300e7)]:
    print(f"{name:10}: {per_day / 86_400:>10,.0f} per second")
'''),
        dict(label='3 · Storage with replication', hint='Yearly storage = daily size × 365 × replicas. Change replicas to 2 and retention to 3 years.',
             code='''gb_per_day, replicas, years = 500, 3, 1
tb = gb_per_day * 365 * years * replicas / 1000
print(f"{tb:,.0f} TB")
'''),
        dict(label='4 · Spaced revision plan', hint='Print the dates to revise each module again after 1, 3 and 7 days.',
             code='''from datetime import date, timedelta
start = date(2026, 10, 21)
for gap in (1, 3, 7):
    print("revise on", start + timedelta(days=gap))
'''),
        dict(label='5 · Self-scoring quiz (advanced)', hint='Change the answers in <code>mine</code> and see your score.',
             code='''key = {"HDFS block (MB)": 128, "Replication factor": 3, "Seconds per day": 86400, "Quorum W for N=3": 2}
mine = {"HDFS block (MB)": 128, "Replication factor": 3, "Seconds per day": 86400, "Quorum W for N=3": 1}
score = sum(mine[q] == a for q, a in key.items())
print(f"{score}/{len(key)}", [q for q in key if mine[q] != key[q]])
'''),
        dict(label='6 · Lakh and crore (advanced)', hint='Convert numbers to lakh or crore for answers. Try 24,07,00,00,000.',
             code='''def indian(n):
    if n >= 1e7:
        return f"{n / 1e7:,.2f} crore"
    if n >= 1e5:
        return f"{n / 1e5:.2f} lakh"
    return f"{n:,}"
for n in [37_410, 18_40_000, 5.9e7, 24.07e9]:
    print(n, "->", indian(n))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: generate a 50-mark practice paper',
    intro='<p>This program builds a practice paper from a bank of course questions: five 2-mark, four 5-mark and two 10-mark questions, 50 marks in all. Change <code>SEED</code> for a new paper, and set <code>SHOW_KEY = True</code> to print answer hints after you have attempted it. Save it as <code>exam_paper.py</code>.</p>',
    items=[
        dict(title='A new practice paper every time you change the seed', file='exam_paper.py',
             cmd=open(os.path.join(HERE, 'exam_paper.py')).read() + '\n# In a terminal:  python exam_paper.py',
             output=open(os.path.join(HERE, 'exam_paper.out')).read(),
             note='Recorded from a real run with Python 3.13 using seed 2026. Add your university’s past questions to the bank to make it even more useful. Write answers on paper in 2 hours, then compare with the lessons.'),
    ],
)

TRACE = dict(
    heading='Scoring a test, question by question',
    intro='<p>Four answers are compared with a key. Watch the score build up and the topics to revise being collected.</p>',
    code='''key = ["b", "c", "a", "d"]
mine = ["b", "a", "a", "d"]
topics = ["CAP", "Parquet", "Kafka", "Spark"]
score, revise = 0, []
for k, m, topic in zip(key, mine, topics):
    if k == m:
        score += 1
    else:
        revise.append(topic)
print(score, "/", len(key), "revise:", revise)
''',
    notes={6: 'Check :: Compare your answer with the key.', 9: 'Revise :: Wrong answers point to the lessons to revisit.'},
)

WORKED_INTRO = 'Four exam-style calculations and comparisons from across the course. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Module 1 · scale', title='How long to read 10 TB on one disk vs 100 machines?',
         problem='<p>A disk reads 200 MB/s. How long does one machine take to scan 10 TB, and how long do 100 machines take if the data is split evenly?</p>',
         inp='10 TB, 200 MB/s, 100 machines',
         approach=['Convert 10 TB to MB (decimal: × 1,000,000).',
                   'Time = size ÷ speed; convert to hours.',
                   'Divide by 100 for parallel machines.'],
         code='''mb = 10 * 1_000_000
one = mb / 200 / 3600
print(f"1 machine: {one:.1f} hours")
print(f"100 machines: {one * 60 / 100:.1f} minutes")
''', notes={3: 'Serial :: One disk becomes the bottleneck.', 4: 'Parallel :: Splitting work across machines is the core idea of big data.'},
         tryit='Each machine has 4 disks reading in parallel. Recalculate.'),
    dict(level='i', tag='Module 3 · partitioning', title='Keys moved when adding a server: mod-N vs consistent hashing',
         problem='<p>1,000 keys are placed with hash mod 4. A fifth server is added. Count how many keys change server with mod-N, and compare with the ideal for consistent hashing (about 1/5).</p>',
         inp='1,000 keys, 4 → 5 servers',
         approach=['Server = key mod N before and after.',
                   'Count keys whose server changes.',
                   'Compare with 1,000 ÷ 5 = 200.'],
         code='''moved = sum(1 for k in range(1000) if k % 4 != k % 5)
print("mod-N moved:", moved, f"({moved / 10:.0f}%)")
print("consistent hashing ideal: about", 1000 // 5)
''', notes={1: 'Mod-N :: Changing N reshuffles most keys.'},
         tryit='Go from 10 to 11 servers. What percentage moves with mod-N?'),
    dict(level='i', tag='Module 3 · quorums', title='Which quorum settings guarantee reading the latest write?',
         problem='<p>With N = 3 replicas, list every (W, R) pair from 1 to 3 and mark which satisfy R + W > N.</p>',
         inp='N = 3',
         approach=['Loop over W and R from 1 to 3.',
                   'Check R + W > N.',
                   'Print strong or eventual.'],
         code='''N = 3
for W in range(1, 4):
    for R in range(1, 4):
        kind = "strong" if R + W > N else "eventual"
        print(f"W={W} R={R}: {kind}")
''', notes={4: 'Overlap :: If R + W > N, every read set overlaps the latest write set.'},
         tryit='Which strong setting gives the fastest writes? Which gives the fastest reads?'),
    dict(level='a', tag='Modules 2 and 4 · cost', title='Scan cost: CSV vs partitioned Parquet',
         problem='<p>A 40 TB CSV table is queried 300 times a day on a pay-per-scan engine at ₹450 per TB (illustrative). With Parquet, the data shrinks to 8 TB; queries read 1 of 365 date partitions and 2 of 20 columns. Compare monthly costs.</p>',
         inp='40 TB CSV vs 8 TB Parquet, pruning, 300 queries/day',
         approach=['CSV: every query scans 40 TB.',
                   'Parquet: 8 TB × (1/365) × (2/20) per query.',
                   'Monthly cost = TB per query × queries × 30 × price.'],
         code='''price, q = 450, 300 * 30
csv_tb = 40
pq_tb = 8 * (1 / 365) * (2 / 20)
for name, tb in [("CSV", csv_tb), ("Parquet + partitions", pq_tb)]:
    print(f"{name:22}: {tb:9.4f} TB/query, Rs {tb * q * price:14,.0f}/month")
print(f"saving: {(1 - pq_tb / csv_tb) * 100:.3f}%")
''', notes={3: 'Pruning :: Partitions cut rows, columnar files cut columns, compression cuts size.'},
         tryit='Queries read 7 days instead of 1. How much does the monthly Parquet cost change?'),
]

QUIZ = [
    dict(q='Which V describes the trustworthiness of data?', options=['Volume', 'Velocity', 'Veracity', 'Variety'], answer=2, why='Veracity is about quality and trust. (Lesson 1.1)'),
    dict(q='Why is one machine not enough for 10 TB scanned daily in minutes?', options=['Machines cannot store 10 TB', 'A single disk’s read speed makes the scan take hours; parallel machines divide the time', 'Python is slow', 'Networks are faster than disks'], answer=1, why='At 200 MB/s, 10 TB takes about 14 hours on one disk. (Lesson 1.2)'),
    dict(q='Which is semi-structured data?', options=['A bank transactions table', 'JSON API responses', 'A CCTV video', 'A scanned image'], answer=1, why='JSON has keys and nesting but a flexible schema. (Lesson 2.1)'),
    dict(q='Which file format is columnar?', options=['CSV', 'JSON', 'Avro', 'Parquet'], answer=3, why='Parquet and ORC are columnar; Avro is row-based. (Lesson 2.2)'),
    dict(q='Object storage such as Amazon S3 is best described as:', options=['A relational database', 'Flat storage of objects with keys and metadata, accessed over HTTP APIs', 'A disk partition', 'A message queue'], answer=1, why='It is the foundation of cloud data lakes. (Lesson 2.3)'),
    dict(q='Cassandra is an example of which NoSQL type?', options=['Key-value', 'Document', 'Wide-column', 'Graph'], answer=2, why='Cassandra is a wide-column store. (Lesson 2.4)'),
    dict(q='Scaling out means:', options=['Buying a bigger server', 'Adding more machines', 'Deleting data', 'Using faster disks'], answer=1, why='Horizontal scaling adds nodes. (Lesson 3.1)'),
    dict(q='Adding a server with hash mod N typically moves:', options=['About 1/N of keys', 'Most keys', 'No keys', 'Exactly half'], answer=1, why='Consistent hashing moves only about 1/N. (Lesson 3.2)'),
    dict(q='With N=3 replicas, which setting guarantees reading the latest write?', options=['W=1, R=1', 'W=2, R=2', 'W=1, R=2', 'W=0, R=3'], answer=1, why='R + W > N: 2 + 2 > 3. (Lesson 3.3)'),
    dict(q='During a network partition, a payments system should usually prefer:', options=['Availability over consistency', 'Consistency over availability', 'Neither', 'Speed over both'], answer=1, why='Wrong balances are worse than a short delay: CP. (Lesson 3.4)'),
    dict(q='In HDFS, which component stores file metadata?', options=['DataNode', 'NameNode', 'ResourceManager', 'Hive'], answer=1, why='The NameNode keeps metadata; DataNodes store blocks. (Module 4)'),
    dict(q='Why is Spark usually faster than MapReduce?', options=['It uses more disks', 'It keeps intermediate data in memory and plans a DAG of stages', 'It only works on small data', 'It skips shuffles'], answer=1, why='MapReduce writes to disk between steps. (Module 4)'),
    dict(q='In Kafka, messages are ordered:', options=['Across the whole topic', 'Within a partition', 'Across all topics', 'Never'], answer=1, why='Use the same key to keep related events in one partition. (Module 4)'),
    dict(q='What does a lakehouse table format such as Delta Lake add to Parquet files?', options=['Images', 'ACID transactions, schema enforcement and time travel', 'Faster networks', 'Encryption keys'], answer=1, why='A transaction log on top of Parquet files. (Module 4)'),
    dict(q='What makes a daily pipeline idempotent?', options=['Appending each run', 'Overwriting the date partition or MERGE on keys', 'Running it at night', 'Using more memory'], answer=1, why='Re-runs then give the same result. (Lesson 4.5 and capstone)'),
    dict(q='On serverless SQL engines billed per TB scanned, the biggest saving usually comes from:', options=['Bigger fonts', 'Columnar formats, partitions and selecting only needed columns', 'More users', 'Longer queries'], answer=1, why='Less data scanned means a lower bill. (Lesson 4.6)'),
    dict(q='Where must payment-system data of Indian payment operators be stored under the RBI’s 2018 direction?', options=['Anywhere', 'Only in India', 'Only in Singapore', 'Only on paper'], answer=1, why='Region choice is a compliance decision. (Lesson 4.6)'),
    dict(q='UPI processed about 24 billion transactions in September 2026. The average per second is about:', options=['930', '9,300', '93,000', '9.3 lakh'], answer=1, why='24e9 ÷ (30 × 86,400) ≈ 9,300. (Lesson 4.7)'),
    dict(q='What protects a booking system during a Tatkal-style rush?', options=['Deleting users', 'A virtual waiting room and rate limiting', 'Turning off the database', 'Bigger images'], answer=1, why='Admit at a safe rate; queue the rest. (Lesson 4.7)'),
    dict(q='Duplicate order_ids violate which data quality dimension?', options=['Timeliness', 'Uniqueness', 'Validity', 'Accuracy'], answer=1, why='Each key should appear once. (Lesson 5.1)'),
    dict(q='Under the DPDP Rules, a detailed breach report must reach the Data Protection Board within:', options=['24 hours', '72 hours', '30 days', '1 year'], answer=1, why='Intimation without delay; detailed report within 72 hours. (Lesson 5.1)'),
    dict(q='Who mainly builds and maintains data pipelines?', options=['Data analyst', 'Data engineer', 'Data scientist', 'UX designer'], answer=1, why='Engineers build pipelines; analysts and scientists use the data. (Lesson 6.1)'),
    dict(q='Which resume bullet is strongest?', options=['Responsible for ETL', 'Worked with many tools', 'Reduced a PySpark job from 3 h to 25 min by fixing skew', 'Passionate learner'], answer=2, why='Action + tool + measurable result. (Lesson 6.2)'),
    dict(q='For amounts 900, 610, 610, 450, RANK() gives:', options=['1, 2, 3, 4', '1, 2, 2, 3', '1, 2, 2, 4', '1, 1, 2, 3'], answer=2, why='RANK leaves a gap after ties; DENSE_RANK gives 1, 2, 2, 3. (Lesson 6.3)'),
    dict(q='In the capstone, 21,429 raw rows had 150 duplicates and 100 quarantined rows. Clean rows?', options=['21,179', '21,279', '21,329', '21,429'], answer=0, why='21,429 − 150 − 100 = 21,179. (Lesson 7.1)'),
]

REVISION = [
    'Four questions: what/where (Modules 1–2) · how to spread (3) · which tools (4) · how to trust (5); then careers (6–7).',
    'Numbers: 86,400 s/day · 1 crore = 100 lakh · HDFS 128 MB × 3 · R + W > N · UPI ≈ 9,300 TPS avg (Sept 2026).',
    'Comparisons: up vs out · row vs columnar · lake vs warehouse vs lakehouse · batch vs streaming · MapReduce vs Spark · CP vs AP · ETL vs ELT.',
    'Five diagrams: HDFS · Spark · Kafka · consistent hashing ring · bronze-silver-gold.',
    'Answer patterns: 2 marks = definition + example; 5 = + diagram + points; 10 = + table, case, limitations.',
    'Estimation: totals → per second → peak (state the ratio) → storage × replicas × retention.',
    'Practise with timed papers; revise on day 1, 3 and 7; fix weak lessons using their quizzes and FAQs.',
]
FAQ = [
    ('What are the most important topics in Big Data for exams?', 'The 5 Vs and the need for distributed systems; data types and file formats; HDFS, YARN and MapReduce; Spark architecture; NoSQL types and the CAP theorem; partitioning and replication; Kafka and stream processing; data lakes, warehouses and lakehouses; cloud services for big data; and data quality, governance and privacy. Practise diagrams for HDFS, Spark, Kafka and pipelines.'),
    ('How do I write a 10-mark answer in a Big Data exam?', 'Use five parts: a precise definition, a labelled diagram, explanation in numbered points, a real example (preferably with numbers, such as UPI or IRCTC figures) and a comparison table or advantages and limitations. Underline key terms and keep each point short.'),
    ('How should I revise Big Data Fundamentals in one week?', 'Day 1: course map and cheat sheets. Days 2–4: two modules a day, redrawing diagrams and taking each lesson’s quiz. Day 5: question banks and estimation practice. Day 6: a timed 50-mark practice paper. Day 7: weak areas and the final test.'),
    ('Is Hadoop still important to learn?', 'Its ideas are: distributed storage with replication, moving computation to data, resource management and table metadata. Many exams still test HDFS, YARN and MapReduce, and many companies still run or migrate Hadoop clusters, but new projects mostly use Spark, cloud object storage and lakehouse formats.'),
    ('What should I study after Big Data Fundamentals?', 'Go deeper in the Big Data Engineering track: SQL and data modelling, PySpark in practice, Kafka and stream processing, a cloud data platform, lakehouse formats and orchestration with Airflow. Extend your capstone at each step and follow the roadmap in Lesson 6.2.'),
]

PRACTICE_INTRO = 'Mixed problems from every module. The last two are business-style estimates.'
PROBLEMS = [
    dict(level='easy', title='Seconds in a week', stmt='Print the number of seconds in a week.', inp='7 days',
         code='''print(7 * 86_400)
''', explain='Per-second thinking starts with time units.'),
    dict(level='easy', title='Crore to lakh', stmt='Print how many lakh are in 5.9 crore.', inp='5.9 crore',
         code='''print(round(5.9 * 100, 1), "lakh")
''', explain='1 crore = 100 lakh.'),
    dict(level='easy', title='HDFS blocks', stmt='How many 128 MB blocks does a 1 GB file (1,024 MB) need? Print blocks and stored copies at replication 3.', inp='1,024 MB',
         code='''import math
b = math.ceil(1024 / 128)
print(b, "blocks,", b * 3, "block copies")
''', explain='Files are split into blocks; each block is replicated.'),
    dict(level='medium', title='Quorum check', stmt='N=5, W=3, R=2. Print whether reads are guaranteed to see the latest write.', inp='N=5, W=3, R=2',
         code='''print(3 + 2 > 5)
''', explain='R + W must exceed N; 5 is not greater than 5.'),
    dict(level='medium', title='Mod-N movement', stmt='Count how many of keys 0–999 change server going from 10 to 11 servers with mod-N.', inp='10 → 11',
         code='''print(sum(1 for k in range(1000) if k % 10 != k % 11))
''', explain='Most keys move, which is why consistent hashing exists.'),
    dict(level='advanced', title='Peak TPS', stmt='80 crore transactions a day, peak 4× average. Print the design peak TPS.', inp='80 crore, 4×',
         code='''print(round(80e7 / 86_400 * 4))
''', explain='Totals → average → peak.'),
    dict(level='advanced', title='Parquet saving', stmt='CSV 6.76 MB vs Parquet 1.53 MB (Lesson 2.2 results). Print how many times smaller Parquet is.', inp='6.76 vs 1.53',
         code='''print(round(6.76 / 1.53, 1), "x smaller")
''', explain='Columnar compression is a recurring theme across the course.'),
    dict(level='business', title='Yearly storage', stmt='500 GB of new data a day, 3 replicas, kept 2 years. Print PB.', inp='500 GB/day',
         code='''print(round(500 * 365 * 2 * 3 / 1e6, 2), "PB")
''', explain='Retention and replication multiply storage quickly.'),
    dict(level='business', title='Cost per query', stmt='A query scans 22 GB at Rs 450 per TB (illustrative). Print the cost in rupees.', inp='22 GB',
         code='''print(round(22 / 1000 * 450, 2))
''', explain='Small per-query costs add up across thousands of queries.'),
]

SCN_INTRO = 'Exam, viva and next-step questions. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
