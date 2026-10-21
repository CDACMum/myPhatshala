import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='01-introduction', lesson='04-a-short-history-of-big-data', n='1.4',
    module_label='Module 1 · Introduction',
    title='A short history of big data: from one server to the lakehouse',
    desc='The history of big data explained simply: the 1997 origin of the term, the 3 Vs, Google\'s GFS, MapReduce and Bigtable papers, Hadoop, Hive, NoSQL, Kafka, Spark, cloud warehouses, the lakehouse and AI. Five eras, the forces behind them, animations, Python programs, quiz and interview questions.',
    og_desc='Why does every big data tool exist? Follow 25 years of history, from one big database to Hadoop, Spark, Kafka, the cloud and the lakehouse.',
    minutes=25, level='Beginner → Advanced',
    lead='Hadoop, Hive, Spark, Kafka, Delta Lake… each tool was built because the one before it hit a wall. In this lesson you follow five eras in about twenty-five years, see what users saw and what engineers built in each, watch the same question get answered in five eras, and learn why in-memory processing replaced MapReduce. After this, the whole ecosystem will make sense as one story.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Timeline program for your PC'],
)

RUN = dict(
    heading='A timeline you can query',
    intro='<p>The milestones of big data are stored as a list of tuples: (year, event, era). The program prints the timeline and counts the events in each era. Change it, then try the challenges: find gaps between a paper and its open-source copy, sort events, and follow the “family tree” of tools.</p>',
    code='''timeline = [
    (2003, "GFS paper", "Google papers"),
    (2004, "MapReduce paper", "Google papers"),
    (2006, "Hadoop starts", "Hadoop era"),
    (2008, "Hive open-sourced", "Hadoop era"),
    (2011, "Kafka open-sourced", "Specialised tools"),
    (2014, "Spark 1.0", "Specialised tools"),
    (2012, "Redshift announced", "Cloud"),
    (2019, "Delta Lake open-sourced", "Lakehouse"),
]

for year, event, era in sorted(timeline):
    print(year, "-", event)

per_era = {}
for year, event, era in timeline:
    per_era[era] = per_era.get(era, 0) + 1
print("Events per era:", per_era)
''',
    anno=[
        ('(2003, "GFS paper", "Google papers"),', 'Each milestone is a tuple: (year, event, era). Tuples keep related values together.'),
        ('for year, event, era in sorted(timeline):', '<code>sorted</code> orders tuples by their first item, the year, so the 2012 entry moves into place.'),
        ('per_era[era] = per_era.get(era, 0) + 1', 'The counting pattern: start at 0 for a new era, add 1 each time.'),
    ],
    tasks=[
        dict(label='1 · Timeline', hint='Press <b>Run</b>. Then add <code>(2016, "UPI launched", "Cloud")</code> and run again. Where does it appear?', code=None),
        dict(label='2 · Paper to open source', hint='Each Google paper was copied as open source a few years later. Print the gap for each pair. Add Dynamo (2007) → Cassandra (2008).',
             code='''pairs = [("GFS", 2003, "HDFS", 2006),
         ("MapReduce", 2004, "Hadoop MapReduce", 2006),
         ("Bigtable", 2006, "HBase", 2008)]
for paper, p_year, clone, c_year in pairs:
    print(f"{paper:10} ({p_year}) -> {clone} ({c_year}): {c_year - p_year} years")
gaps = [c - p for _, p, _, c in pairs]
print("Average gap:", sum(gaps) / len(gaps), "years")
'''),
        dict(label='3 · Which era?', hint='Write a function that returns the era for any year. Test 1999, 2005, 2013 and 2024. Add a "Cloud" era for 2012–2018.',
             code='''def era(year):
    if year < 2003:
        return "One big database"
    elif year < 2009:
        return "Google papers and Hadoop"
    elif year < 2019:
        return "Specialised tools and cloud"
    else:
        return "Lakehouse and AI"

for y in [1999, 2005, 2013, 2024]:
    print(y, "->", era(y))
'''),
        dict(label='4 · Problem → tool', hint='Each tool was created to solve a problem. Look up which tool fixes each problem. Add “analysts know SQL, not Java”.',
             code='''solved_by = {
    "files too big for one disk": "HDFS",
    "process blocks in parallel": "MapReduce",
    "repeated steps too slow on disk": "Spark",
    "need events in real time": "Kafka",
    "lake files need updates and transactions": "Delta Lake / Iceberg",
}
problems = ["need events in real time", "files too big for one disk", "repeated steps too slow on disk"]
for p in problems:
    print(f"{p:35} -> {solved_by[p]}")
'''),
        dict(label='5 · Family tree (advanced)', hint='Each tool records what inspired it. Follow the chain back from HBase to the original paper. Then try Cassandra, which has two parents: change the program to handle a list of parents.',
             code='''inspired_by = {
    "HBase": "Bigtable",
    "Bigtable": "GFS",
    "Hive": "Hadoop MapReduce",
    "Hadoop MapReduce": "MapReduce paper",
}
tool = "HBase"
chain = [tool]
while tool in inspired_by:
    tool = inspired_by[tool]
    chain.append(tool)
print(" <- ".join(chain))
'''),
        dict(label='6 · Disk vs memory (advanced)', hint='An iterative job has 10 steps. MapReduce writes and re-reads 200 GB on disk between steps at 1 GB/s (with 3 copies on write); Spark keeps it in memory. Estimate the extra time spent on disk. Change the number of steps.',
             code='''steps, data_gb = 10, 200
disk_gb_per_s = 1
copies = 3
write_s = data_gb * copies / disk_gb_per_s
read_s = data_gb / disk_gb_per_s
between = steps - 1
extra = between * (write_s + read_s)
print("Disk time between steps:", extra / 60, "minutes")
print("Spark keeps the data in memory, so this time mostly disappears.")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: your life on the big data timeline',
    intro='<p>This program prints the milestones grouped by era, with a small text bar, and tells you how old you were at each one. Save it as <code>history_timeline.py</code>, change <code>BORN</code> to your birth year, and run it.</p>',
    items=[
        dict(title='The timeline, grouped by era', file='history_timeline.py',
             cmd=open(os.path.join(HERE, 'history_timeline.py')).read() + '\n# In a terminal:  python history_timeline.py',
             output=open(os.path.join(HERE, 'history_timeline.out')).read(),
             note='Recorded from a real run with Python 3.13 and <code>BORN = 2006</code>. Your output changes with your birth year. The bar length grows by one <code>#</code> every two years after 1995, so later events have longer bars.'),
    ],
)

TRACE = dict(
    heading='Paper to open source, one line at a time',
    intro='<p>The program works out how many years passed between each Google paper and its open-source copy, and keeps the longest gap. Watch <code>longest</code> change only when a bigger gap appears.</p>',
    code='''papers = {"GFS": 2003, "MapReduce": 2004, "Bigtable": 2006}
clones = {"GFS": 2006, "MapReduce": 2006, "Bigtable": 2008}
longest = 0
for name in papers:
    gap = clones[name] - papers[name]
    if gap > longest:
        longest = gap
print("Longest gap:", longest, "years")
''',
    notes={1: 'Data :: The year each paper was published.',
           2: 'Data :: The year its open-source version (HDFS, Hadoop MapReduce, HBase) appeared.',
           3: 'Setup :: Start with 0 so the first real gap is always bigger.'},
)

WORKED_INTRO = 'Four small programs about the history, from grouping events by decade to walking a family tree of tools. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Revision · timeline', title='Group milestones by decade',
         problem='<p>Group these milestone years by decade (1990s, 2000s, 2010s, 2020s) and print how many fall in each.</p>',
         inp='1997, 2001, 2003, 2004, 2006, 2008, 2011, 2014, 2016, 2019, 2023',
         approach=['The decade of a year is <code>year // 10 * 10</code> (2014 → 2010).',
                   'Count with a dictionary.',
                   'Print the decades in order.'],
         code='''years = [1997, 2001, 2003, 2004, 2006, 2008, 2011, 2014, 2016, 2019, 2023]
per_decade = {}
for y in years:
    decade = y // 10 * 10
    per_decade[decade] = per_decade.get(decade, 0) + 1
for d in sorted(per_decade):
    print(f"{d}s: {per_decade[d]} milestones")
''', notes={4: 'Decade :: Integer division drops the last digit: 2014 // 10 = 201, × 10 = 2010.'},
         tryit='Add 2024 and 2026. Which decade has the most milestones so far?'),
    dict(level='i', tag='History · lag', title='How long did the open-source world take to catch up?',
         problem='<p>For each research paper, find the gap to its open-source version, then print the average gap and the pair with the shortest gap.</p>',
         inp='GFS 2003→HDFS 2006 · MapReduce 2004→Hadoop 2006 · Bigtable 2006→HBase 2008 · Dynamo 2007→Cassandra 2008',
         approach=['Store each pair as a tuple (paper, paper year, clone, clone year).',
                   'Compute the gap for each and keep a list.',
                   'Use <code>min</code> with a key to find the shortest gap.'],
         code='''pairs = [("GFS", 2003, "HDFS", 2006), ("MapReduce", 2004, "Hadoop", 2006),
         ("Bigtable", 2006, "HBase", 2008), ("Dynamo", 2007, "Cassandra", 2008)]
gaps = [c_year - p_year for _, p_year, _, c_year in pairs]
print("Gaps:", gaps)
print("Average:", sum(gaps) / len(gaps), "years")
fastest = min(pairs, key=lambda p: p[3] - p[1])
print("Fastest copy:", fastest[0], "->", fastest[2])
''', notes={3: 'Gaps :: A list comprehension unpacks each tuple and subtracts the years.'},
         tryit='Add Dremel (2010) → Apache Drill (2012). Does the average change?'),
    dict(level='i', tag='Architecture · choosing tools', title='Match each requirement to the era that solved it',
         problem='<p>A team lists its needs. For each need, print the tool family that was invented for it and the year it appeared.</p>',
         inp='store 500 TB of files, live order events, fast ML training loops, SQL for analysts',
         approach=['Keep a dictionary need → (tool, year).',
                   'Loop over the team\'s needs and look each one up.',
                   'Sort the result by year to see the order the problems were solved in.'],
         code='''solution = {
    "store 500 TB of files": ("HDFS / object storage", 2006),
    "SQL for analysts": ("Hive, later cloud warehouses", 2008),
    "live order events": ("Kafka", 2011),
    "fast ML training loops": ("Spark", 2014),
}
needs = ["live order events", "store 500 TB of files", "fast ML training loops", "SQL for analysts"]
answers = sorted((solution[n][1], n, solution[n][0]) for n in needs)
for year, need, tool in answers:
    print(f"{year}: {need:24} -> {tool}")
''', notes={8: 'Sort :: Tuples sort by their first item, the year.'},
         tryit='Add the need “update and delete rows in lake files” solved by Delta Lake (2019).'),
    dict(level='a', tag='Ecosystem · family tree', title='Find every tool descended from one paper',
         problem='<p>Each tool lists the tools or papers that inspired it (some have two parents). Find <b>all</b> descendants of the Bigtable paper, at any depth.</p>',
         inp='HBase ← Bigtable · Cassandra ← Bigtable, Dynamo · ScyllaDB ← Cassandra · DynamoDB ← Dynamo',
         approach=['Store parents as lists: <code>{"Cassandra": ["Bigtable", "Dynamo"], …}</code>.',
                   'Start a “to visit” list with the paper. Repeatedly take one item and find every tool whose parents include it.',
                   'Add new descendants to the result and to the list to visit (this is breadth-first search).'],
         code='''parents = {"HBase": ["Bigtable"], "Cassandra": ["Bigtable", "Dynamo"],
           "ScyllaDB": ["Cassandra"], "DynamoDB": ["Dynamo"]}
start = "Bigtable"
to_visit = [start]
found = []
while to_visit:
    current = to_visit.pop(0)
    for tool, ps in parents.items():
        if current in ps and tool not in found:
            found.append(tool)
            to_visit.append(tool)
print("Descended from", start, ":", found)
''', notes={6: 'Visit :: Take the oldest item first, so the search spreads level by level.', 9: 'New :: A tool is recorded once, even if it is reachable in two ways.'},
         tryit='Change <code>start</code> to <code>"Dynamo"</code>. Which tools appear, and why is Cassandra in both answers?'),
]

QUIZ = [
    dict(q='Which Google paper described storing huge files as replicated blocks on many cheap machines?', options=['Bigtable (2006)', 'Google File System (2003)', 'Dremel (2010)', 'MapReduce (2004)'], answer=1,
         why='The <b>Google File System</b> paper (2003) inspired HDFS. MapReduce (2004) was about processing; Bigtable (2006) about tables.'),
    dict(q='Hadoop was created as an open-source implementation of which ideas?', options=['Dynamo and Dremel', 'GFS and MapReduce', 'SQL and Oracle', 'Kafka and Spark'], answer=1,
         why='Hadoop = <b>HDFS</b> (from GFS) + <b>MapReduce</b>. YARN was added later for resource management.'),
    dict(q='Which company created Hive so that analysts could use SQL on Hadoop?', options=['Google', 'Facebook', 'LinkedIn', 'Netflix'], answer=1,
         why='Hive was built at <b>Facebook</b> and open-sourced in 2008. Kafka came from LinkedIn; Iceberg from Netflix.'),
    dict(q='Kafka was originally created at:', options=['LinkedIn', 'Yahoo!', 'Amazon', 'UC Berkeley'], answer=0,
         why='Kafka was built at <b>LinkedIn</b> and open-sourced in 2011. Spark came from UC Berkeley\'s AMPLab.'),
    dict(q='Why is Spark much faster than MapReduce for machine-learning loops?', options=['It uses a different programming language', 'It keeps intermediate data in memory instead of writing it to disk after every step', 'It never needs a cluster', 'It skips fault tolerance'], answer=1,
         why='MapReduce writes each step\'s output to HDFS; Spark keeps it <b>in memory</b> and recovers lost pieces using lineage.'),
    dict(q='What does “separation of storage and compute” in cloud platforms mean?', options=['Data is stored on paper', 'Data stays in cheap object storage, and processing power is rented separately only when needed', 'Each user has a separate computer', 'Storage and compute are in different countries'], answer=1,
         why='You keep petabytes cheaply in object storage and pay for compute only while queries run. Each can scale independently.'),
    dict(q='Who first described the 3 Vs of big data, and when?', options=['Doug Cutting, 2006', 'Doug Laney, 2001', 'Jeff Dean, 2004', 'NASA, 1997'], answer=1,
         why='Analyst <b>Doug Laney</b> described Volume, Velocity and Variety in <b>2001</b>. NASA researchers used the term “big data” in 1997.'),
    dict(q='Which open table formats are at the heart of the lakehouse idea?', options=['CSV and JSON', 'Delta Lake, Apache Iceberg and Apache Hudi', 'HDFS and YARN', 'MySQL and Oracle'], answer=1,
         why='Delta Lake, Iceberg and Hudi add transactions, updates and time travel to files in a lake.'),
]

REVISION = [
    'Term “big data”: NASA researchers, 1997. The 3 Vs: Doug Laney, 2001.',
    'Google papers: <b>GFS</b> (2003) → HDFS · <b>MapReduce</b> (2004) → Hadoop MapReduce · <b>Bigtable</b> (2006) → HBase. Amazon <b>Dynamo</b> (2007) → Cassandra (with Bigtable).',
    '<b>Hadoop</b> (2006, Doug Cutting and Mike Cafarella, backed by Yahoo!; named after a toy elephant). Apache top-level 2008.',
    '<b>Hive</b> (Facebook, SQL on Hadoop) · <b>Kafka</b> (LinkedIn, 2011) · <b>Spark</b> (UC Berkeley, 2009; Apache top-level 2014).',
    'Cloud: S3 (2006), BigQuery, Redshift, Snowflake. Storage and compute separated; pay per use.',
    'Lakehouse: Delta Lake, Iceberg, Hudi over object storage. One copy for BI, streaming and ML.',
    'Forces: cheap storage, commodity clusters, phones and cheap data, the cloud, AI.',
]
FAQ = [
    ('Explain the evolution of big data technologies.', 'Before 2000 data lived in single relational databases and warehouses that scaled up. Google\'s GFS (2003) and MapReduce (2004) papers showed how to store and process data on clusters of commodity machines; Hadoop (2006) implemented them as open source. Hive added SQL, and NoSQL stores (HBase, Cassandra, MongoDB) served fast look-ups. Spark brought in-memory processing and Kafka real-time streams. Cloud platforms separated storage from compute (S3, BigQuery, Redshift, Snowflake). Today lakehouses use open table formats (Delta Lake, Iceberg, Hudi) to serve BI, streaming and ML from one copy of the data.'),
    ('Why was Hadoop named Hadoop?', 'Doug Cutting named it after his son\'s toy elephant, which is why the logo is a yellow elephant.'),
    ('What problems of MapReduce did Spark solve?', 'MapReduce writes intermediate results to disk between steps, is hard to program (low-level map and reduce functions), and is slow for iterative and interactive work. Spark keeps intermediate data in memory, plans whole multi-step jobs as a DAG, recovers lost data through lineage, and offers high-level APIs (DataFrames, SQL, streaming, MLlib).'),
    ('Is Hadoop dead?', 'Hadoop MapReduce is rarely used for new work, but HDFS, YARN and Hive still run in many enterprises, and their ideas live on in Spark, cloud object storage and lakehouses. Many companies are migrating from on-premises Hadoop to cloud or lakehouse platforms, so the knowledge remains useful.'),
    ('What is the lakehouse and how is it different from earlier architectures?', 'Earlier platforms kept raw data in a lake and a separate, cleaned copy in a warehouse. A lakehouse stores data once in open formats on cheap object storage and adds a table layer (Delta Lake, Iceberg, Hudi) that provides transactions, schema enforcement, updates and time travel, so the same tables serve BI, streaming and machine learning.'),
]

PRACTICE_INTRO = 'Small programs built around the timeline. The last two are business tasks about technology decisions.'
PROBLEMS = [
    dict(level='easy', title='Years since a milestone', stmt='Print how many years have passed between each milestone and 2026.', inp='GFS 2003, Hadoop 2006, Kafka 2011, Spark 2014',
         code='''milestones = {"GFS": 2003, "Hadoop": 2006, "Kafka": 2011, "Spark": 2014}
for name, year in milestones.items():
    print(name, 2026 - year, "years ago")
''', explain='A dictionary maps each name to its year; subtract from the current year.'),
    dict(level='easy', title='Earliest and latest', stmt='Print the earliest and latest milestone years from the list.', inp='[2011, 2003, 2019, 2006, 2014]',
         code='''years = [2011, 2003, 2019, 2006, 2014]
print("Earliest:", min(years))
print("Latest:", max(years))
''', explain='<code>min</code> and <code>max</code> work on any list of numbers.'),
    dict(level='easy', title='Name the creator', stmt='Look up which organisation created each tool and print it.', inp='Hive, Kafka, Spark, Iceberg',
         code='''created_at = {"Hive": "Facebook", "Kafka": "LinkedIn", "Spark": "UC Berkeley", "Iceberg": "Netflix"}
for tool in ["Hive", "Kafka", "Spark", "Iceberg"]:
    print(f"{tool} was created at {created_at[tool]}")
''', explain='Dictionary look-up by key.'),
    dict(level='medium', title='Events in a range', stmt='Print only the events between 2005 and 2015 (inclusive), in year order.', inp='6 events',
         code='''events = [(2019, "Delta Lake"), (2006, "Hadoop"), (2003, "GFS"),
          (2011, "Kafka"), (2014, "Spark 1.0"), (2008, "Hive")]
for year, name in sorted(events):
    if 2005 <= year <= 2015:
        print(year, name)
''', explain='Sort the tuples by year, then filter with a chained comparison.'),
    dict(level='medium', title='Tools per era', stmt='Given each tool\'s year, count how many belong to each era: before 2009, 2009–2018, 2019 onwards.', inp='Hadoop 2006, Hive 2008, Kafka 2011, Spark 2014, Snowflake 2015, Delta 2019, Iceberg 2018',
         code='''tools = {"Hadoop": 2006, "Hive": 2008, "Kafka": 2011, "Spark": 2014,
         "Snowflake": 2015, "Delta": 2019, "Iceberg": 2018}
eras = {"Hadoop era": 0, "Specialised + cloud": 0, "Lakehouse": 0}
for name, y in tools.items():
    if y < 2009:
        eras["Hadoop era"] += 1
    elif y < 2019:
        eras["Specialised + cloud"] += 1
    else:
        eras["Lakehouse"] += 1
print(eras)
''', explain='An if/elif chain puts each year into exactly one bucket.'),
    dict(level='advanced', title='Follow the chain of inspiration', stmt='Each tool points to the one that inspired it. Print the chain from Delta Lake back to the start.', inp='Delta Lake ← Hive tables ← Hadoop ← GFS',
         code='''inspired_by = {"Delta Lake": "Hive tables", "Hive tables": "Hadoop", "Hadoop": "GFS"}
tool = "Delta Lake"
chain = [tool]
while tool in inspired_by:
    tool = inspired_by[tool]
    chain.append(tool)
print(" <- ".join(chain))
''', explain='A while loop follows links until a tool has no recorded parent.'),
    dict(level='advanced', title='Disk round-trips saved', stmt='An iterative job has 8 steps. MapReduce writes 100 GB with 3 copies and reads it back between every pair of steps, at 2 GB/s. Print the total disk time in minutes that Spark avoids by keeping the data in memory.', inp='8 steps, 100 GB, 3 copies, 2 GB/s',
         code='''steps, gb, copies, speed = 8, 100, 3, 2
per_gap = (gb * copies + gb) / speed
total = (steps - 1) * per_gap
print("Seconds per gap:", per_gap)
print("Minutes saved:", round(total / 60, 1))
''', explain='Between each pair of steps MapReduce writes (with copies) and reads the data. 7 gaps × 200 s ≈ 23 minutes of pure disk time.'),
    dict(level='business', title='Buy a bigger server or rent the cloud?', stmt='A big server costs Rs 90 lakh and lasts 5 years. The same work in the cloud costs Rs 1,200 per hour, and the job runs 4 hours a day. Compare the 5-year cost.', inp='Rs 90 lakh · Rs 1,200/hour × 4 h/day × 365 × 5',
         code='''server = 90_00_000
cloud = 1200 * 4 * 365 * 5
print("Server, 5 years: Rs", server)
print("Cloud, 5 years : Rs", cloud)
print("Cheaper:", "cloud" if cloud < server else "server")
''', explain='Pay-per-use wins when machines would otherwise sit idle most of the day. If the job ran 24 hours a day, the answer could flip.'),
    dict(level='business', title='Migration progress', stmt='A bank is moving 120 Hive jobs from Hadoop to a lakehouse. It moves 8 jobs a week. How many weeks until done, and what percentage is done after 6 weeks?', inp='120 jobs, 8 per week',
         code='''import math
jobs, per_week = 120, 8
print("Weeks needed:", math.ceil(jobs / per_week))
print("Done after 6 weeks:", round(6 * per_week / jobs * 100), "%")
''', explain='<code>math.ceil</code> rounds up, because a part-week still counts as a week.'),
]

SCN_INTRO = 'History questions that interviewers use to test real understanding. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
