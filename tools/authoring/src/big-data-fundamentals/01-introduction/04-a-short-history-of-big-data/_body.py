import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story scene
pts = [(40, '1997', 'term “big data”'), (120, '2003', 'GFS paper'), (190, '2004', 'MapReduce'), (260, '2006', 'Hadoop · S3'),
       (330, '2011', 'Kafka'), (400, '2014', 'Spark 1.0'), (470, '2016', 'UPI · Jio'), (540, '2019', 'Delta Lake'), (598, 'today', 'lakehouse · AI')]
sc = '<path d="M24 78h600" style="stroke:var(--track);stroke-width:3"/>'
for i, (x, y, l) in enumerate(pts):
    up = i % 2 == 0
    sc += f'<circle cx="{x}" cy="78" r="6" style="fill:var(--track)"/>'
    sc += t(x, 58 if up else 104, y, 11, 'acc', bold=True)
    sc += t(x, 44 if up else 118, l, 9, 'ink2')
scene_svg = scene('A timeline from 1997 to today: the term big data, the Google papers, Hadoop, Kafka, Spark, UPI and Jio, Delta Lake and the lakehouse.',
                  sc, 'Each tool was invented to solve <tspan font-weight="700" class="s-acc">one problem the previous tools could not</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Riya is filling in the syllabus tracker for the Big Data track: Hadoop, Hive, Spark, Kafka, Delta Lake, Airflow… She stops and asks the question every beginner asks: <i>why are there so many tools, and why do they have such strange names?</i></p>

{scene_svg}

R> Sir, why is it called <b>Hadoop</b>? It sounds like a cartoon.
A> Almost. Doug Cutting, one of its creators, named it after his young son’s toy elephant. That’s why the logo is a yellow elephant.
K> And Kafka? TiffinGo’s tech blog mentions it everywhere.
A> Jay Kreps at LinkedIn named it after the writer Franz Kafka, because it is a system built for writing. The names are fun. The <i>reasons</i> the tools exist are what matter.
R> What do you mean by reasons?
A> Each tool was built because the tool before it hit a wall. Google couldn’t fit the web on one machine, so it wrote the GFS and MapReduce papers. MapReduce was slow for repeated steps, so Spark appeared. Nightly batches were too late, so Kafka and streaming arrived. Learn the story once, and the whole ecosystem makes sense.
K> So history is actually a map of the ecosystem?
A> Exactly, Kabir. Today we walk through five eras in about twenty-five years, and see what users saw and what engineers built in each one.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> The history at three levels
L1> Five eras in one breath
      <ol>
        <li><b>Before 2000, one big database:</b> companies kept data in one powerful server (Oracle, IBM DB2, mainframes) and built data warehouses for reports.</li>
        <li><b>2003–2008, the Google papers and Hadoop:</b> Google showed how to store and process the whole web on thousands of cheap machines. Hadoop copied the idea as free, open-source software.</li>
        <li><b>2008–2014, more tools for more jobs:</b> SQL on Hadoop (Hive), NoSQL databases (HBase, Cassandra, MongoDB), streaming (Kafka) and faster in-memory processing (Spark).</li>
        <li><b>2010s, the cloud:</b> rent storage (Amazon S3) and warehouses (BigQuery, Redshift, Snowflake) by the hour instead of buying servers.</li>
        <li><b>Today, the lakehouse and AI:</b> one copy of data in open formats (Delta Lake, Iceberg) serving reports, streaming and machine learning, increasingly queried in plain language.</li>
      </ol>
L2> Who built what, and why
      <ul>
        <li><b>Google GFS (2003):</b> a file system that splits huge files into large blocks and keeps 3 copies on different cheap machines. Became <b>HDFS</b>.</li>
        <li><b>Google MapReduce (2004):</b> a way to process those blocks in parallel (map), then group and combine results (reduce), with automatic re-runs on failure. Became <b>Hadoop MapReduce</b>.</li>
        <li><b>Google Bigtable (2006):</b> a giant sorted table spread across machines. Inspired <b>HBase</b> and, with Amazon’s Dynamo paper (2007), <b>Cassandra</b>.</li>
        <li><b>Facebook Hive (2008):</b> analysts knew SQL, not Java, so Hive turned SQL into MapReduce jobs.</li>
        <li><b>LinkedIn Kafka (2011):</b> a durable log that many systems can publish to and read from in real time.</li>
        <li><b>UC Berkeley Spark (2009, Apache top-level 2014):</b> keeps data in memory between steps, so repeated steps and machine learning run far faster than MapReduce.</li>
        <li><b>Netflix Iceberg, Uber Hudi, Databricks Delta Lake (2017–2019):</b> table formats that give files in a lake database-like features.</li>
      </ul>
L3> The forces behind each shift
      <ul>
        <li><b>Hardware economics:</b> disk prices per GB fell by more than a million times between 1980 and the 2010s, so keeping everything became cheaper than deciding what to throw away.</li>
        <li><b>Commodity clusters beat big iron:</b> many ordinary servers plus software that expects failure (replication, re-execution) cost far less than one fault-tolerant supercomputer.</li>
        <li><b>Disk vs memory:</b> as RAM got cheaper, engines moved intermediate results from disk (MapReduce) to memory (Spark), trading memory for 10–100× faster iterative jobs.</li>
        <li><b>Separation of storage and compute:</b> cloud object storage plus on-demand compute let teams scale each independently and pay per use. This is why modern warehouses and lakehouses look the way they do.</li>
        <li><b>Latency expectations:</b> users went from accepting next-day reports to expecting live dashboards and instant fraud checks, which pushed streaming (Kafka, Flink) into the mainstream.</li>
        <li><b>Regulation and trust:</b> privacy laws (Europe’s GDPR in 2018, India’s DPDP Act in 2023) made governance, lineage and deletion first-class requirements.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'Modern big data technology traces back to <b>Google’s research papers</b> on the <b>Google File System</b> (2003), <b>MapReduce</b> (2004) and <b>Bigtable</b> (2006), which described how to store and process web-scale data on clusters of commodity machines that tolerate failure. Open-source implementations such as <b>Apache Hadoop</b> (2006) spread the approach, followed by <b>NoSQL</b> databases, <b>SQL-on-Hadoop</b>, <b>stream processing</b> (Kafka), <b>in-memory processing</b> (Spark), <b>cloud data warehouses</b> and, most recently, the <b>lakehouse</b>.',
    'Around 2003 Google had more data than any one computer could hold, so it worked out how to use thousands of cheap computers together and published how. Others copied the idea for free (Hadoop). Every big data tool since then was built to fix a weakness of the ones before it.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Research paper', 'A public write-up of how a system works. Google, Amazon and others published papers that the open-source world then implemented.'),
    ('Open source', 'Software whose code is free to use, read and change, usually managed by a foundation such as Apache.'),
    ('Apache Software Foundation', 'The non-profit that hosts Hadoop, Spark, Kafka, Hive, Cassandra, Iceberg and hundreds of other projects.'),
    ('Commodity hardware', 'Ordinary, inexpensive servers instead of special fault-tolerant machines.'),
    ('In-memory processing', 'Keeping data in RAM between steps instead of writing it to disk each time.'),
    ('Separation of storage and compute', 'Storing data in one place (object storage) and renting processing power separately, only when needed.'),
    ('Lakehouse', 'Lake storage plus table formats that add database features (transactions, updates, time travel).'),
]) + '''

  <h3>Milestones to remember</h3>
''' + facts([
    ('1997', 'NASA researchers Michael Cox and David Ellsworth use the term “big data” for datasets too large for memory and disk'),
    ('2001', 'Analyst Doug Laney describes Volume, Velocity and Variety (the 3 Vs)'),
    ('2003 · 2004 · 2006', 'Google publishes the GFS, MapReduce and Bigtable papers'),
    ('2006', 'Hadoop starts (Doug Cutting, Mike Cafarella; strongly backed by Yahoo!). Amazon launches S3 and EC2'),
    ('2008', 'Hadoop becomes a top-level Apache project; Facebook open-sources Hive and Cassandra'),
    ('2011', 'LinkedIn open-sources Kafka'),
    ('2014', 'Spark becomes a top-level Apache project and reaches version 1.0'),
    ('2016', 'India launches UPI (NPCI) and Jio’s cheap mobile data brings crores of new users online'),
    ('2019 →', 'Delta Lake is open-sourced; Iceberg and Hudi mature; the “lakehouse” idea spreads'),
]) + lv + '''
EXAM> For “Explain the evolution of big data technologies”, write the eras in order with one tool and one reason each: <b>RDBMS/warehouse → GFS + MapReduce (Hadoop: HDFS, MapReduce) → NoSQL and Hive → Spark (in-memory) and Kafka (streaming) → cloud warehouses → lakehouse</b>. Mention the 2003/2004/2006 Google papers by name.'''

# ---------------------------------------------------------------- types
types = cards([
    ('1. One big database (to ~2003)', 'Everything in a powerful relational database, plus a separate data warehouse for reports. Scale up when it gets slow.', 'Scale up'),
    ('2. Hadoop era (2006–2012)', 'HDFS stores huge files across cheap machines; MapReduce processes them in parallel in nightly batches.', 'Batch on clusters'),
    ('3. Specialised tools (2008–2015)', 'Hive for SQL, HBase/Cassandra/MongoDB for fast look-ups, Kafka for streams, Spark for fast processing.', 'Right tool per job'),
    ('4. Cloud era (2012 →)', 'Object storage plus warehouses rented by the hour (BigQuery, Redshift, Snowflake). No servers to manage.', 'Pay per use'),
    ('5. Lakehouse and AI (2019 →)', 'Open table formats over cheap storage serve BI, streaming and ML from one copy; AI assistants write the queries.', 'One copy, many uses'),
]) + '''

  <h3>The famous papers and what they became</h3>
''' + table(['Paper (year)', 'Problem it solved', 'Open-source descendant'], [
    ['Google File System (2003)', 'Store files bigger than any disk, on machines that fail', '<b>HDFS</b>'],
    ['MapReduce (2004)', 'Process those files in parallel without writing distributed code by hand', '<b>Hadoop MapReduce</b> (later Spark, Flink)'],
    ['Bigtable (2006)', 'Fast reads and writes on a table with billions of rows', '<b>HBase</b>, and partly Cassandra'],
    ['Amazon Dynamo (2007)', 'A shopping cart that is always available, even during failures', '<b>Cassandra</b>, Riak, DynamoDB'],
    ['Google Dremel (2010)', 'Interactive SQL over huge nested data in seconds', '<b>BigQuery</b>, Apache Drill, ideas in Parquet'],
    ['Spark / RDD paper (2012)', 'Fast repeated computations with fault tolerance', '<b>Apache Spark</b>'],
]) + '''
TIP> A pattern worth noticing: big companies hit a wall first, publish a paper or open-source their tool, and the rest of the industry adopts it a few years later. Watching what large platforms build today is a good hint of what you’ll use tomorrow.'''

# ---------------------------------------------------------------- steps
steps = stepper([
    ('2000: one server and a nightly report',
     '<p>A bank keeps every transaction in one large Oracle database. A data warehouse is loaded each night, and managers read reports the next morning.</p>',
     'It works while data is gigabytes. When it grows, the only answer is a bigger, far costlier server. That is <b>scaling up</b>, and it has a ceiling.'),
    ('2003–2004: Google writes down its secret',
     '<p>Google’s index of the web is far too big for any server. Its engineers store files as 64 MB blocks with 3 copies across thousands of cheap machines (GFS), and process them with two simple functions, <code>map</code> and <code>reduce</code>.</p>',
     'The key ideas: <b>expect failure</b>, <b>move code to data</b>, and let a framework handle splitting, scheduling and retries. Google published both papers.'),
    ('2006–2008: Hadoop makes it free',
     '<p>Doug Cutting and Mike Cafarella build an open-source version for their web-search project. Yahoo! hires Cutting and runs it at huge scale. It becomes <b>Apache Hadoop</b>: HDFS + MapReduce.</p>',
     'Now any company can run a cluster on ordinary servers. Facebook adds <b>Hive</b> so analysts can write SQL instead of Java MapReduce code.'),
    ('2009–2014: faster and more varied',
     '<p>MapReduce writes to disk after every step, so jobs with many steps are slow. <b>Spark</b> keeps data in memory. <b>Kafka</b> carries events in real time. NoSQL databases serve apps that need millisecond look-ups.</p>',
     'The single “Hadoop stack” becomes an <b>ecosystem</b> of specialised tools, each solving one weakness of the original.'),
    ('2012 onwards: rent, don’t buy',
     '<p>Instead of running their own clusters, companies store data in cloud object storage and query it with warehouses billed by usage: BigQuery, Redshift, Snowflake.</p>',
     'Storage and compute are <b>separated</b>: keep petabytes cheaply, and rent 100 machines for 10 minutes when a query needs them.'),
    ('Today: one copy for everything, and AI on top',
     '<p>Table formats (Delta Lake, Iceberg, Hudi) add transactions and updates to files in the lake. The same tables feed dashboards, streaming jobs and ML models, and AI assistants turn questions into SQL.</p>',
     'This is the <b>lakehouse</b>. Under the hood, it still uses the 2003 ideas: blocks, copies, parallel tasks and re-running failed work.'),
])

# ---------------------------------------------------------------- two-view animation
eras = [('2000', 'Web portal'), ('2004', 'Search'), ('2008', 'Social feed'), ('2012', 'Smartphone apps'), ('2016', 'UPI · cheap 4G'), ('Today', 'AI assistant')]


def phone(inner, year):
    return (f'<rect x="120" y="22" width="120" height="200" rx="16" class="s-board"/><rect x="128" y="38" width="104" height="168" rx="6" class="s-card2"/>'
            + t(180, 16, year, 11, 'acc', bold=True) + inner)


see = [
    '<rect x="70" y="30" width="220" height="150" rx="8" class="s-board"/><rect x="78" y="46" width="204" height="126" rx="4" class="s-card2"/>'
    + t(180, 22, '2000', 11, 'acc', bold=True) + t(180, 66, 'Welcome to MyPortal', 10, bold=True)
    + ''.join(fill(92, 78 + k * 18, 176, 10, 'grey') for k in range(4)) + t(180, 200, 'A desktop web page, refreshed by hand', 9, 'ink2'),
    '<rect x="70" y="30" width="220" height="150" rx="8" class="s-board"/><rect x="78" y="46" width="204" height="126" rx="4" class="s-card2"/>'
    + t(180, 22, '2004', 11, 'acc', bold=True) + box(98, 62, 164, 20, 'blue', rx=10) + t(180, 76, 'cheap flights to Goa', 8.6, 'ink')
    + ''.join(t(96, 104 + k * 18, f'Result {k + 1} · relevant page', 8.4, 'blue', anchor='start') for k in range(3))
    + t(180, 200, 'Billions of pages searched in 0.3 s', 9, 'ink2'),
    phone(''.join(box(136, 50 + k * 50, 88, 42, 'card') + fill(142, 56 + k * 50, 14, 14, 'acc') + fill(162, 58 + k * 50, 54, 6, 'grey') + fill(142, 76 + k * 50, 74, 6, 'grey') for k in range(3)), '2008')
    + t(180, 240, 'Friends’ posts, likes, photos', 9, 'ink2'),
    phone(''.join(fill(140 + (k % 3) * 30, 54 + (k // 3) * 32, 22, 22, ['acc', 'blue', 'green', 'violet', 'red', 'amber'][k % 6], rx=6) for k in range(9)), '2012')
    + t(180, 240, 'An app for everything, all day', 9, 'ink2'),
    phone(t(180, 70, 'Paid ₹20', 12, bold=True) + '<circle cx="180" cy="104" r="18" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M171 104l6 6 12-12" style="stroke:var(--green);stroke-width:3;fill:none"/>'
          + t(180, 148, 'UPI · 2 seconds', 9, 'green', bold=True) + t(180, 172, '4G video · 1 GB/day', 8.6, 'ink2'), '2016')
    + t(180, 240, 'Crores of new users, all online', 9, 'ink2'),
    phone(box(134, 50, 92, 34, 'blue', rx=8) + t(180, 64, 'Which city ordered', 7.8) + t(180, 76, 'most this week?', 7.8)
          + box(134, 94, 92, 46, 'green', rx=8) + t(180, 110, 'Pune: 41,200', 8.2, 'green', bold=True) + t(180, 124, 'Mumbai: 38,900', 8.2) + t(180, 170, 'answer in seconds', 8.4, 'ink2'), 'Today')
    + t(180, 240, 'Ask in plain language', 9, 'ink2'),
]
behind = [
    label_box(110, 50, 140, 70, ['One big server', 'Oracle / DB2', 'scale up = buy bigger'], 'blue', 10)
    + box(110, 140, 140, 40, 'card') + t(180, 164, 'Nightly data warehouse load', 8.6) + t(180, 210, 'Gigabytes. Reports next morning.', 9.5, 'ink2'),
    ''.join(fill(30 + c * 30, 40 + r * 26, 22, 18, 'green', rx=3) for r in range(3) for c in range(10))
    + t(180, 132, 'GFS: 64 MB blocks × 3 copies', 9.5, bold=True) + t(180, 150, 'MapReduce: map → shuffle → reduce', 9.5, bold=True)
    + t(180, 186, 'Thousands of cheap machines.', 9.5, 'ink2') + t(180, 202, 'Failure is normal; tasks re-run.', 9.5, 'ink2'),
    label_box(20, 40, 150, 56, ['Hadoop', 'HDFS + MapReduce', '(open source, 2006)'], 'acc', 10) + label_box(190, 40, 150, 56, ['Hive', 'SQL → MapReduce', '(Facebook, 2008)'], 'violet', 10)
    + label_box(20, 110, 150, 56, ['HBase · Cassandra', 'NoSQL look-ups', '(2008)'], 'blue', 10) + label_box(190, 110, 150, 56, ['Yahoo! clusters', 'thousands of nodes', 'nightly batches'], 'card', 10)
    + t(180, 196, 'The ecosystem begins.', 9.5, 'ink2'),
    label_box(20, 40, 150, 60, ['Spark', 'in-memory steps', '10–100× faster loops'], 'acc', 10) + label_box(190, 40, 150, 60, ['Kafka', 'real-time event log', '(LinkedIn, 2011)'], 'green', 10)
    + label_box(20, 116, 320, 50, ['Cloud: S3 storage + warehouses by the hour', 'BigQuery · Redshift · Snowflake'], 'blue', 10)
    + t(180, 196, 'Batch + streaming + cloud.', 9.5, 'ink2'),
    label_box(20, 36, 320, 46, ['Streams everywhere', 'every payment, click and ride is an event'], 'green', 10)
    + label_box(20, 94, 150, 56, ['Storage', 'object storage, PB', 'cheap, always on'], 'blue', 10) + label_box(190, 94, 150, 56, ['Compute', 'rented per query', 'scales to the peak'], 'acc', 10)
    + t(180, 186, 'Storage and compute separated.', 9.5, 'ink2'),
    label_box(20, 36, 320, 46, ['Lakehouse tables (Delta · Iceberg · Hudi)', 'one copy of data, with transactions'], 'acc', 10)
    + label_box(20, 96, 100, 46, ['BI', 'dashboards'], 'blue', 9.5) + label_box(130, 96, 100, 46, ['Streaming', 'live'], 'green', 9.5) + label_box(240, 96, 100, 46, ['AI / ML', 'models, chat'], 'violet', 9.5)
    + t(180, 176, 'Underneath: still blocks, copies,', 9.5, 'ink2') + t(180, 192, 'parallel tasks and re-runs from 2003.', 9.5, 'ink2'),
]
see_caps = ['<b>2000:</b> people visit websites on desktop computers. Pages change slowly.',
            '<b>2004:</b> a search box answers from billions of web pages in a fraction of a second.',
            '<b>2008:</b> social feeds: every like, post and photo is new data, all day.',
            '<b>2012:</b> smartphones put an app for everything in every pocket.',
            '<b>2016:</b> in India, UPI makes payments instant and cheap 4G brings crores of people online at once.',
            '<b>Today:</b> you ask a question in plain language and get an answer from huge data in seconds.']
behind_caps = ['One powerful database server, plus a data warehouse loaded every night. To grow, buy a bigger server.',
               'Google’s answer: GFS stores 64 MB blocks with 3 copies on thousands of cheap machines; MapReduce processes them in parallel and re-runs failed tasks.',
               'Hadoop brings the same ideas to everyone for free. Hive adds SQL; HBase and Cassandra add fast look-ups.',
               'Spark keeps data in memory for speed, Kafka carries events live, and the cloud lets teams rent storage and warehouses.',
               'Everything becomes a stream of events. Storage and compute are separated, so each can grow on its own.',
               'Lakehouse tables serve dashboards, streaming and AI from one copy of data. Underneath, the 2003 ideas still do the work.']
two = anim_two('From one server to the lakehouse', 'What users saw, and what engineers built', 'What users saw in each era',
               'The data systems engineers built in each era', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- real-time scenarios
# Scenario 1: the same question in five eras
q_static = box(10, 8, 340, 30, 'card') + t(180, 27, 'Question: orders per city yesterday, from a 10 TB table', 9.6, bold=True)
eras5 = [
    ('2000 · one database', 'SQL on one big server', 'Query runs all night; often killed for', 'blocking the morning business. Answer: maybe tomorrow.', 'red', '~10+ hours', 6),
    ('2008 · Hadoop MapReduce', '≈ 150 lines of Java (map + reduce)', 'Runs on 200 cheap nodes in parallel.', 'Writes to disk between steps. Answer in about an hour.', 'amber', '~1 hour', 40),
    ('2014 · Spark', '3 lines: read · groupBy · count', 'Same cluster, data kept in memory.', 'Answer in a few minutes.', 'acc', '~5 minutes', 120),
    ('2018 · cloud warehouse', 'SELECT city, COUNT(*) … GROUP BY city', 'No cluster to manage; billed per query.', 'Answer in seconds.', 'green', '~20 seconds', 260),
    ('Today · lakehouse + AI', '“Which city ordered most yesterday?”', 'An assistant writes the SQL; the', 'lakehouse runs it over open tables.', 'green', 'seconds', 300),
]
fr1 = []
for i, (era, how, a, b, col, tm, w) in enumerate(eras5):
    f = t(180, 58, era, 11, 'acc', bold=True) + box(30, 68, 300, 26, 'blue' if i < 4 else 'violet', rx=6) + t(180, 85, how, 9, 'ink', mono=(i in (2, 3)))
    f += t(30, 118, 'time to answer', 8.4, 'ink3', anchor='start') + '<rect x="30" y="124" width="300" height="12" rx="4" class="s-card2"/>' + fill(30, 124, w, 12, col)
    f += t(330, 118, tm, 9, 'ink', anchor='end', bold=True)
    f += cap(a, b, 'card', y=152, h=44)
    fr1.append(f)
s1 = anim_one('Real-time scenario 1', 'The same question in five eras',
              'TiffinGo-sized data: a 10 TB orders table. The manager asks the simplest question: how many orders per city yesterday? Watch how the work, the code and the waiting time change across the eras. The bar shows how long the wait feels (longer bar = faster answer).',
              'One question, 25 years', 'The same question answered in five eras with different tools and times', fr1,
              ['<b>2000:</b> on one big database, scanning 10 TB with a GROUP BY can take all night, and DBAs often stop such queries because they slow the live business.',
               '<b>2008:</b> with Hadoop, an engineer writes a MapReduce program in Java. It runs on hundreds of cheap machines and finishes in about an hour, writing to disk between the map and reduce steps.',
               '<b>2014:</b> with Spark, the same job is three lines (read, group, count) and data stays in memory: minutes.',
               '<b>2018:</b> in a cloud warehouse it is one SQL statement, with no servers to manage, billed by data scanned: seconds.',
               '<b>Today:</b> the manager types the question in plain language; an AI assistant writes the SQL, and the lakehouse runs it. (All times are illustrative.)'],
              hid='animated-example', static=q_static)

# Scenario 2: four forces
forces = [
    ('Force 1 · storage became nearly free', 'Disk cost per GB fell more than a million times', 'from 1980 to the 2010s. Keeping everything got', 'cheaper than deciding what to delete → volume.', 'blue'),
    ('Force 2 · cheap clusters beat big servers', 'Software that expects failure lets thousands of', 'ordinary machines replace one costly supercomputer.', '→ scale out instead of scale up.', 'green'),
    ('Force 3 · phones and cheap data', 'Smartphones, and in India cheap 4G from 2016,', 'put crores of people online all day. Every tap is', 'an event → velocity and variety.', 'acc'),
    ('Force 4 · the cloud', 'Rent 100 machines for 10 minutes. No buying,', 'no data-centre. Startups get the same tools', 'as giants → big data for everyone.', 'violet'),
    ('Force 5 · AI needs data', 'Machine-learning and AI models are trained on', 'huge, clean, well-governed datasets → quality,', 'lineage and lakehouses matter more than ever.', 'red'),
]
fr2 = []
for i, (h, a, b, c, tone) in enumerate(forces):
    f = ''
    for k in range(5):
        col = ['blue', 'green', 'acc', 'violet', 'red'][k]
        x = 14 + k * 68
        if k == i:
            f += fill(x, 14, 60, 24, col, rx=6) + t(x + 30, 30, f'Force {k + 1}', 8.6, extra=' style="fill:#fff"', bold=True)
        else:
            f += box(x, 14, 60, 24, 'card') + t(x + 30, 30, f'Force {k + 1}', 8.6, 'ink3', bold=True)
    f += t(180, 66, h, 10.5, 'ink', bold=True)
    f += box(20, 80, 320, 84, tone) + t(180, 104, a, 9.2) + t(180, 122, b, 9.2) + t(180, 144, c, 9.2, 'ink', bold=True)
    fr2.append(f)
s2 = anim_one('Real-time scenario 2', 'Five forces that created big data',
              'Big data didn’t appear because someone invented Hadoop. Five changes in the world made it necessary, and each one still shapes how platforms are built.',
              'Why it happened', 'Five forces behind the rise of big data', fr2,
              ['<b>Cheap storage:</b> the cost of a GB of disk fell by more than a million times over about three decades. Companies started keeping every click and log, which created the <b>volume</b>.',
               '<b>Commodity clusters:</b> instead of one fault-tolerant supercomputer, use thousands of cheap servers and let software handle failures. This is the Google/Hadoop insight.',
               '<b>Phones and cheap data:</b> smartphones, and in India the 2016 mobile-data price drop, put crores of people online. Every tap, payment and ride became an event: <b>velocity</b> and <b>variety</b>.',
               '<b>The cloud:</b> renting machines by the minute means a two-person startup can use the same scale as a giant, and pay only for what it uses.',
               '<b>AI:</b> modern models need enormous, clean, well-documented data. That pushes quality, governance and lakehouse tables to the centre.'])

# Scenario 3 (advanced): MapReduce vs Spark on an iterative job
lanes = 'MapReduce', 'Spark'
fr3 = []
def lane(y, steps_done, kind, extra=''):
    out = t(14, y + 14, kind, 9.5, 'acc' if kind == 'Spark' else 'blue', anchor='start', bold=True)
    x = 92
    for k in range(5):
        if k < steps_done:
            out += fill(x, y, 26, 20, 'blue' if kind == 'MapReduce' else 'acc', rx=4) + t(x + 13, y + 14, f'S{k + 1}', 8, extra=' style="fill:#fff"', bold=True)
        else:
            out += box(x, y, 26, 20, 'card', rx=4) + t(x + 13, y + 14, f'S{k + 1}', 8, 'ink3')
        x += 26
        if k < 4:
            if kind == 'MapReduce':
                done = k < steps_done - 1
                out += f'<rect x="{x + 3}" y="{y + 3}" width="20" height="14" rx="3" style="fill:{"#8A94A0" if done else "none"};stroke:#8A94A0"/>'
                out += t(x + 13, y + 30, 'disk', 6.8, 'ink3') if k == 0 else ''
                x += 26
            else:
                out += f'<circle cx="{x + 6}" cy="{y + 10}" r="3" style="fill:{"var(--track)" if k < steps_done - 1 else "var(--line)"}"/>'
                x += 12
    return out + extra
cfg = [
    (1, 1, 'An ML model improves itself in 5 passes over the same data.', 'Both engines start step 1.'),
    (2, 4, 'MapReduce writes every step’s result to HDFS (3 copies)', 'and reads it back for the next step. Spark keeps it in memory.'),
    (3, 5, 'Spark has finished all 5 steps.', 'MapReduce is still on step 3, waiting on disk.'),
    (5, 5, 'MapReduce finishes last. For loops like this, keeping data', 'in memory is often 10–100× faster.'),
    (5, 5, 'A machine dies? Spark knows how each piece was made', '(its lineage) and recomputes only the lost piece.'),
]
for i, (mr, sp, a, b) in enumerate(cfg):
    f = lane(46, mr, 'MapReduce') + lane(104, sp, 'Spark')
    if i == 4:
        f += '<path d="M150 100l12 12M162 100l-12 12" style="stroke:#D64545;stroke-width:2.5"/>' + t(200, 160, 'lost piece of S2 → rebuilt from S1', 8.6, 'red', bold=True)
    f += t(180, 24, 'One iterative job, two engines (5 steps)', 10, 'acc', bold=True)
    f += cap(a, b, 'blue', y=170, h=44)
    fr3.append(f)
s3 = anim_one('Real-time scenario 3 · advanced', 'Why Spark replaced MapReduce for most jobs',
              'Machine learning and graph algorithms repeat the same calculation many times over the same data. Watch the two engines run a 5-step job, and see how Spark still recovers from a failure without saving every step to disk.',
              'Disk between steps vs memory', 'MapReduce writing to disk between steps compared with Spark keeping data in memory', fr3,
              ['An iterative job: each pass improves a model using the result of the previous pass. Both engines start the first step together.',
               '<b>MapReduce</b> writes each step’s output to HDFS, with 3 copies, then reads it back for the next step. <b>Spark</b> keeps the intermediate data in memory across steps.',
               'Spark has finished all five steps while MapReduce is still waiting on disk for step 3.',
               'For iterative work, avoiding the disk round-trips often makes Spark 10–100 times faster. That is why the Spark paper caught on so quickly.',
               'Fault tolerance without saving every step: Spark records the <b>lineage</b> (the recipe used to build each piece of data), so when a machine fails it recomputes only the lost piece from its parent. (Timings are illustrative.)'])

realworld = '''  <p>Three live scenarios: the same business question answered in five eras, the five forces that made big data necessary, and an advanced look at why in-memory processing took over.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>History you can see in today’s job descriptions</h3>
''' + usecase('<rect x="20" y="20" width="80" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="50" text-anchor="middle" font-size="12" font-weight="700" class="s-blue">HDFS</text>',
              '1. Banks and telecom still run Hadoop clusters', 'Many large Indian banks and telecom companies built on-premises Hadoop clusters in the 2010s. They still run HDFS and Hive for regulatory reports and are gradually moving to Spark, cloud or lakehouse platforms. Knowing both worlds is valuable.',
              ['On-prem HDFS + Hive', '*Migration to Spark / cloud', 'Lakehouse']) + usecase(
    '<path d="M20 60h80" style="stroke:var(--track);stroke-width:4"/><circle cx="30" cy="60" r="6" style="fill:var(--track)"/><circle cx="60" cy="60" r="6" style="fill:var(--track)"/><circle cx="90" cy="60" r="6" style="fill:var(--track)"/><text x="60" y="40" text-anchor="middle" font-size="11" font-weight="700" class="s-acc">Kafka</text>',
    '2. Start-ups are born “streaming-first”', 'Food-delivery, ride-hailing and fintech start-ups founded after 2015 usually put Kafka (or a cloud equivalent) at the centre from day one, because their products are real-time.', ['App events', '*Kafka', 'Live features + lake']) + usecase(
    '<rect x="16" y="18" width="88" height="54" rx="6" class="s-soft-acc" style="stroke:var(--track)"/><text x="60" y="42" text-anchor="middle" font-size="10" font-weight="700" class="s-acc">Delta / Iceberg</text><text x="60" y="58" text-anchor="middle" font-size="9" class="s-ink">on S3 / ADLS</text>',
    '3. New platforms are lakehouses', 'Teams building fresh platforms today usually choose cloud object storage with Delta Lake or Iceberg tables and Spark or SQL engines on top, instead of a separate lake and warehouse.', ['Object storage', '*Open table format', 'BI + ML']) + usecase(
    '<circle cx="60" cy="45" r="26" class="s-soft-violet" style="stroke:var(--violet);stroke-width:2"/><text x="60" y="50" text-anchor="middle" font-size="12" font-weight="700" class="s-violet">AI</text>',
    '4. AI raises the bar on data quality', 'Companies training or grounding AI models need well-documented, high-quality, legally collected data. Data engineers with governance and lineage skills are in demand because of this latest shift.', ['Raw data', '*Clean, governed tables', 'AI models'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Why is it called Hadoop?', story)
        + part(2, 'definition', 'Definition', 'How did big data begin?', definition)
        + part(3, 'types', 'Types and ways to use it', 'Five eras of data technology', types)
        + part(4, 'steps', 'Step by step', 'Twenty-five years in six steps', steps)
        + part(5, 'animation', 'See it happen', 'What users saw, and what engineers built', '  <p>Step through the six frames. Left: what ordinary people saw on their screens in each era. Right: what engineers were building behind it.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: the history in action', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Interview · fundamentals', 'Fresher', '“Why was Hadoop created?”',
            'An interviewer opens with: “In two minutes, why was Hadoop created and what problem did it solve?”',
            'do you understand the problem behind the tool, not just its name?',
            '<p>Around 2003 web-scale data no longer fitted on one machine, and scaling up was too expensive and had a ceiling. Google published GFS and MapReduce, showing how to store data as replicated blocks on many cheap machines and process it in parallel with automatic retries. Hadoop (2006) implemented these ideas as open source: <b>HDFS</b> for storage and <b>MapReduce</b> for processing, later <b>YARN</b> for resource management.</p>',
            'listing Hadoop components without saying what problem they solve.')
        + scn('Platform modernisation', '1–3 years', 'An old Hadoop cluster and a cloud proposal',
              'Your company runs a 10-year-old on-premises Hadoop cluster with Hive jobs. Leadership asks whether to move to a cloud lakehouse.',
              'can you weigh history, cost and risk instead of following fashion?',
              '<ul><li>List what runs today: Hive SQL, MapReduce jobs, Spark jobs, downstream reports and their deadlines.</li><li>Compare total cost: hardware refresh, admin staff and licences versus cloud storage and compute.</li><li>Check rules: data that must stay in India (choose an Indian cloud region), security and audit needs.</li><li>Plan in phases: copy data to object storage, convert tables to Parquet/Delta or Iceberg, move Hive SQL to Spark SQL, run both systems in parallel and compare outputs before switching off.</li></ul>',
              '“Hadoop is old, so throw it away tomorrow” or “it works, never touch it”.')
        + scn('System design · reasoning', '1–3 years', 'Why not just use MapReduce today?',
              'A teammate says, “Spark is just faster MapReduce, so the ideas are the same.” The interviewer asks you to agree or disagree.',
              'do you know what Spark actually changed, and what it kept?',
              '<p>Partly agree. Spark keeps the core ideas: partitioned data, parallel tasks, a shuffle for grouping, and re-running failed work. It changed three things: it keeps intermediate data <b>in memory</b> instead of writing to HDFS after every step, it builds a <b>DAG</b> of many steps and optimises the whole plan, and it recovers using <b>lineage</b> instead of replicated intermediate files. It also offers high-level APIs (DataFrames, SQL, streaming, MLlib) instead of hand-written map and reduce functions.</p>',
              'saying they are completely different, or that Spark doesn’t need fault tolerance.')
        + scn('Career · learning plan', 'Fresher', '“Should I still learn Hadoop in 2026?”',
              'A junior asks you whether learning Hadoop is a waste of time now that lakehouses exist.',
              'can you give balanced, practical advice?',
              '<p>Learn the <b>ideas</b> deeply (HDFS blocks and replication, MapReduce, YARN), because Spark, cloud storage and lakehouses are built on them and interviews still ask them. Spend most hands-on time on <b>Spark, SQL, Kafka, a cloud platform and a table format</b>. Many large Indian enterprises still run Hadoop, so knowing it helps with migration projects.</p>',
              'dismissing old tools completely, or spending months on MapReduce Java code.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('body.html and scenarios.html written')
