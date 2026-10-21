import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Store, process, survive',
    intro='<p>This cluster already runs Hadoop. Use it to tick off the four requirements from Part 2, one by one.</p>',
    racks=2, nodes=3, features=['upload', 'job', 'fail'],
    **{'try': [
        dict(text='<b>Store data bigger than one machine:</b> upload a 2 GB file. Its blocks are spread over all six nodes.', on='upload-done'),
        dict(text='<b>Process it in parallel:</b> run the job. One map task per block, many at the same time.', on='job-done'),
        dict(text='<b>Survive failures:</b> run it again and stop a busy node. The job still succeeds.', on='node-stop'),
        dict(text='<b>Simple programming:</b> notice you never chose where blocks go or which node runs which task. The framework did.'),
    ]},
)))

META = dict(
    module='02-why-hadoop', lesson='01-the-problem-hadoop-solved', n='2.1',
    module_label='Module 2 · Why Hadoop was born',
    title='The problem Hadoop solved (and is Hadoop still relevant?)',
    desc='The web-scale data problem of the early 2000s: storing and processing data bigger than any machine, cheaply and reliably. Why databases, SANs, supercomputers and home-grown scripts did not fit, the four requirements Hadoop meets, and an honest look at Hadoop\'s place in 2026. With animations, a playground, Python you can run, quiz and interview scenarios.',
    og_desc='Store it, process it, survive failures, keep it simple: the four problems Hadoop solved, and why it still matters in 2026.',
    minutes=24, level='Beginner → Intermediate',
    lead='Around 2003, web companies had a problem no existing tool could solve: data far bigger than any computer, which had to be stored, processed in parallel and kept safe on thousands of cheap machines that broke all the time. This lesson pins that problem down precisely, compares the tools of the time, and shows the four requirements Hadoop was designed to meet. It ends with an honest answer to the question every student asks: is Hadoop still worth learning?',
    chips=['Cluster Playground', 'Runs in your browser (Python)', 'Honest 2026 view'],
)

RUN = dict(
    heading='Manual sharding, and why it hurts',
    intro='<p>Before Hadoop, teams split data across machines with their own rules. This program spreads 10,000 URLs over 4 machines with a hash, then counts how many URLs would have to move if a fifth machine is added. Then try the challenges.</p>',
    code='''import zlib

def machine_for(url, machines):
    return zlib.crc32(url.encode()) % machines

urls = [f"https://site{i}.in/page" for i in range(10000)]
before = {u: machine_for(u, 4) for u in urls}
after = {u: machine_for(u, 5) for u in urls}

moved = sum(1 for u in urls if before[u] != after[u])
print("URLs per machine (4):", [list(before.values()).count(m) for m in range(4)])
print(f"Adding a 5th machine moves {moved} of {len(urls)} URLs ({moved / len(urls):.0%})")
''',
    anno=[
        ('zlib.crc32(url.encode()) % machines', 'A hash turns the URL into a number; <code>% machines</code> picks a machine. The same URL always lands on the same machine.'),
        ('before = {u: machine_for(u, 4) for u in urls}', 'A dictionary comprehension: for each URL, which of 4 machines owns it.'),
        ('moved = sum(1 for u in urls if before[u] != after[u])', 'Count URLs whose owner changes when there are 5 machines instead of 4.'),
    ],
    tasks=[
        dict(label='1 · Shard and grow', hint='Press <b>Run</b>. About 4 in 5 URLs move. Change 5 to 8: how many move when you double the machines?', code=None),
        dict(label='2 · How big is the web crawl?', hint='<b>Predict first:</b> 200 crore pages of 100 KB each. Is that closer to 2 TB, 20 TB or 200 TB?',
             code='''pages = 200_00_00_000        # 200 crore
kb_each = 100
tb = pages * kb_each / 1024**3
print(f"{tb:,.0f} TB of pages")
print(f"Disks of 4 TB needed (one copy): {tb / 4:,.0f}")
'''),
        dict(label='3 · A job with no fault tolerance', hint='A job runs on N machines for 10 hours. Each machine has a 0.2% chance of failing in those 10 hours. Without fault tolerance, one failure kills the job. Try N = 1000.',
             code='''p_fail = 0.002
for n in [1, 10, 100, 500]:
    p_ok = (1 - p_fail) ** n
    print(f"{n:>4} machines: job survives {p_ok:.0%} of the time")
'''),
        dict(label='4 · Plumbing vs logic', hint='Count lines in a typical home-made pipeline. What share is the actual business logic?',
             code='''lines = {"parse page + count words": 50, "split data over machines": 300,
         "start and monitor workers": 400, "retry failed parts": 600,
         "merge results": 250, "move data when adding machines": 400}
logic = lines["parse page + count words"]
total = sum(lines.values())
print(f"Logic: {logic} of {total} lines ({logic / total:.0%})")
'''),
        dict(label='5 · Spot the error', hint='This was meant to show which machine owns each URL, but it crashes. Read the error, then fix the call.',
             expect='error',
             code='''import zlib
def machine_for(url, machines):
    return zlib.crc32(url) % machines
print(machine_for("https://iitb.ac.in", 4))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Hash sharding, one line at a time',
    intro='<p>Watch three URLs being assigned to machines with a hash, first with 4 machines and then with 5. See which ones change owner.</p>',
    code='''import zlib

def owner(url, n):
    return zlib.crc32(url.encode()) % n

for url in ["iitb.ac.in", "coep.org.in", "nitk.ac.in"]:
    a, b = owner(url, 4), owner(url, 5)
    print(url, a, "->", b, "moved" if a != b else "stays")
''',
    notes={3: 'Rule :: The whole sharding scheme is this one line, and every program must use it.'},
)

WORKED_INTRO = 'Three calculations that explain why Hadoop had to exist: how big the data was, how likely a long job was to fail, and how much a bigger cluster would cost without one. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Web search · capacity', title='How many machines just to store the crawl?',
         problem='<p>A search engine has <b>80 crore pages</b> of about <b>60 KB</b> each, and wants <b>3 copies</b> for safety. Each machine in 2005 has <b>4 disks of 250 GB</b>. How many machines are needed just for storage?</p>',
         inp='80 crore pages × 60 KB · ×3 · 4 × 250 GB per machine',
         approach=['Total size = pages × KB, converted to GB.',
                   'Multiply by 3 copies.',
                   'Divide by GB per machine and round up.'],
         code='''import math
pages = 80_00_00_000
gb = pages * 60 / 1024 / 1024
raw_gb = gb * 3
per_machine = 4 * 250
print(f"Data: {gb:,.0f} GB, with copies: {raw_gb:,.0f} GB")
print("Machines:", math.ceil(raw_gb / per_machine))
''', notes={3: 'Size :: KB → GB is ÷ 1024 ÷ 1024.'},
         tryit='Disks in 2026 are often 16 TB or more. Change <code>per_machine</code> to 12 × 16000 GB. The same crawl now fits on a handful of machines; but today\'s data is far bigger too.'),
    dict(level='i', tag='Reliability · long jobs', title='How often does a 1,000-machine job fail without fault tolerance?',
         problem='<p>An indexing job runs on <b>1,000 machines</b> for <b>8 hours</b>. Each machine has about a <b>4%</b> chance of failing in a year. Without automatic recovery, any failure kills the job. What is the chance the job completes?</p>',
         inp='1,000 machines · 8 hours · 4% per year',
         approach=['Chance one machine fails during the job = 4% × (8 hours ÷ hours in a year).',
                   'Chance all 1,000 survive = (1 − p)<sup>1000</sup>.',
                   'Compare with a job that can retry: it almost always finishes.'],
         code='''p_year = 0.04
p_job = p_year * 8 / (365 * 24)
p_all_ok = (1 - p_job) ** 1000
print(f"One machine fails during the job: {p_job:.5%}")
print(f"Job completes with no failures  : {p_all_ok:.1%}")
''', notes={2: 'Scale :: 8 hours is a small slice of a year.'},
         tryit='Make the job run for 48 hours on 4,000 machines: it now completes only about 42% of the time. Real pipelines run many such jobs every day, so without automatic recovery something would fail daily. This is why fault tolerance was a requirement, not a luxury.'),
    dict(level='a', tag='IT budget · cost', title='Scale-up storage vs a commodity cluster',
         problem='<p>A company must store <b>500 TB</b>. Option A: an enterprise storage array at <b>Rs 40,000 per usable TB</b>. Option B: commodity servers with raw disk at <b>Rs 2,500 per TB</b>, using HDFS with 3 copies and 25% headroom, plus <b>Rs 20 lakh</b> for setup and staff training. Compare the costs. (Prices are illustrative.)</p>',
         inp='500 TB · A: Rs 40,000/TB · B: Rs 2,500/TB raw, ×3 ÷ 0.75 + Rs 20 lakh',
         approach=['A = 500 × 40,000.',
                   'B raw TB = 500 × 3 ÷ 0.75; cost = raw × 2,500 + 20 lakh.',
                   'Print both in lakh rupees and the ratio.'],
         code='''tb = 500
a = tb * 40_000
raw = tb * 3 / 0.75
b = raw * 2_500 + 20_00_000
print(f"A (storage array) : Rs {a / 1e5:,.0f} lakh")
print(f"B (Hadoop cluster): Rs {b / 1e5:,.0f} lakh for {raw:,.0f} TB raw")
print(f"A costs {a / b:.1f} times more")
''', notes={4: 'Raw :: 3 copies and 25% free space: 2,000 TB of cheap disk.'},
         tryit='B also gives you hundreds of CPU cores next to the data for processing; A gives storage only. That difference, not just the price, is why Hadoop spread.'),
]

QUIZ = mix([
    dict(q='What was the main problem that led to Hadoop?', options=['Making websites look better', 'Storing and processing data far bigger than one machine, cheaply and reliably', 'Replacing all relational databases', 'Speeding up mobile phones'], answer=1,
         why='Web-scale data needed distributed storage, parallel processing and fault tolerance on commodity hardware.'),
    dict(q='Which component gives Hadoop scalable storage?', options=['YARN', 'HDFS', 'Hive', 'ZooKeeper'], answer=1,
         why='<b>HDFS</b> splits files into blocks and stores replicated copies across many nodes.'),
    dict(q='Why was central SAN/NAS storage a poor fit for web-scale processing?', options=['It cannot store files', 'Every server pulled data over the network from one place, so the network became the bottleneck, and it was expensive at petabyte scale', 'It only works on Windows', 'It has no disks'], answer=1,
         why='Central storage separates data from compute; at scale, moving data to the CPUs is the bottleneck. Hadoop moves computation to the data.'),
    dict(q='What is the main weakness of manual (hash) sharding with “hash % N”?', options=['It spreads data unevenly', 'Changing N moves most of the data, and failures must be handled by hand', 'It is slower than one disk', 'It only works for numbers'], answer=1,
         why='Going from 4 to 5 machines moves about 80% of keys with modulo hashing, and there are no automatic copies or retries.'),
    dict(q='Which design bet did Hadoop make?', options=['Low latency for small random reads', 'High throughput for large sequential reads, write once and read many', 'Every machine must be highly reliable', 'Data must be in tables before storage'], answer=1,
         why='Hadoop optimises for reading large files fast in bulk, and files are written once rather than edited in place.'),
    dict(q='Which statement about Hadoop in 2026 is most accurate?', options=['Nobody uses it anymore', 'It is used everywhere for every workload', 'Many enterprises still run HDFS/YARN/Hive, MapReduce is largely replaced by Spark, and its ideas underpin modern platforms', 'It only runs on mainframes'], answer=2,
         why='Hadoop is a mature foundation: still running in many companies, partly replaced for new projects, and conceptually behind most big data tools.'),
    dict(q='Why does Hadoop ask you to write only a map and a reduce function?', options=['Because Java cannot do more', 'A restricted model lets the framework split, schedule, move and retry work automatically', 'To make jobs shorter to type', 'Because SQL is not allowed'], answer=1,
         why='By limiting the shape of a job, the framework can parallelise and recover it without the programmer\'s help.'),
    dict(q='What is Hadoop NOT designed for?', options=['Batch processing of huge files', 'Low-latency queries on many tiny records, like an online banking app', 'Storing years of logs', 'Running on commodity servers'], answer=1,
         why='Hadoop is built for throughput, not millisecond responses. Transaction systems use databases; interactive analytics use other engines.'),
])

REVISION = [
    'Early 2000s: web-scale data, far bigger than any machine, on cheap hardware that fails often.',
    'Four requirements: <b>scalable storage</b>, <b>parallel processing</b>, <b>fault tolerance</b>, <b>simple programming</b>. Plus low cost.',
    'Hadoop\'s answers: <b>HDFS</b>, <b>MapReduce</b>, replication + retries, map/reduce functions; <b>YARN</b> from Hadoop 2.',
    'RDBMS: scale up, costly, needs tables. SAN: network bottleneck. MPI: programmer handles failures. Scripts: manual repair.',
    'Manual hash sharding: changing N moves most data; no copies, no retries.',
    'Design bets: throughput over latency, write once read many, move code to data, failure is normal.',
    'Not for: low-latency lookups, many tiny files, fast iterative jobs.',
    '2026: still running widely; MapReduce mostly replaced by Spark; concepts power modern platforms; migrations need Hadoop skills.',
]
FAQ = [
    ('What is Hadoop and what problem does it solve?', 'Apache Hadoop is an open-source framework for storing and processing very large data sets on clusters of commodity computers. It solves the problem of data that is too large for one machine: HDFS stores it reliably across many nodes, MapReduce (and other engines on YARN) process it in parallel near the data, and failures are handled automatically, so developers only write the processing logic.'),
    ('Why couldn\'t traditional databases handle big data?', 'They mostly scale up on one large server, become very expensive per TB, need data to be modelled into tables before loading, and are optimised for transactions and indexed queries rather than scanning petabytes of raw, semi-structured data. Hadoop scales out on cheap hardware and stores raw data first (schema-on-read).'),
    ('What does “write once, read many” mean in HDFS?', 'Files are written once (and may be appended to), but not modified in the middle. Most big data workloads write data once and then read it many times for analysis. This simplifies replication and consistency and allows very high read throughput.'),
    ('Is Hadoop dead?', 'No, but its role has changed. Many enterprises still run HDFS, YARN and Hive, especially on-premises. Classic MapReduce has largely been replaced by Spark and Tez, and new cloud projects often use object storage and managed services instead of HDFS. The core ideas (blocks, replication, data locality, distributed processing) are used by almost every modern data platform, and migrations from Hadoop are common projects.'),
    ('What are the limitations of Hadoop?', 'High latency (batch, not interactive), poor handling of many small files (NameNode memory), MapReduce writes intermediate results to disk which makes iterative algorithms slow, operational complexity, and security that must be configured separately (Kerberos, Ranger). Later tools such as Spark, Hive LLAP/Impala and cloud warehouses address several of these.'),
]

PRACTICE_INTRO = 'Small calculations and programs about scale, sharding and failure: the reasons Hadoop exists. The business problems are the arguments teams really had before adopting it.'
PROBLEMS = [
    dict(level='easy', title='How long to read the crawl?', stmt='A 400 TB crawl is read by one machine at 200 MB/s. How many days does one full read take?', inp='400 TB · 200 MB/s',
         code='print(round(400 * 1024 * 1024 / 200 / 86400, 1), "days")\n', explain='About 24 days for one pass. Rebuilding a search index weekly is impossible on one machine.'),
    dict(level='easy', title='Same read on 1,000 machines', stmt='The same 400 TB is spread over 1,000 machines, each reading its share at 200 MB/s. How many minutes?', inp='400 TB · 1000 × 200 MB/s',
         code='print(round(400 * 1024 * 1024 / (1000 * 200) / 60, 1), "minutes")\n', explain='About 35 minutes. Parallel reading is the heart of Hadoop.'),
    dict(level='easy', title='Which machine owns the key?', stmt='Using <code>zlib.crc32(key.encode()) % 3</code>, print which of 3 machines owns each of the keys "pune", "delhi", "goa".', inp='["pune", "delhi", "goa"] · 3 machines',
         code='''import zlib
for k in ["pune", "delhi", "goa"]:
    print(k, "->", zlib.crc32(k.encode()) % 3)
''', explain='Deterministic: the same key always goes to the same machine. That is the good part of hashing.'),
    dict(level='medium', title='Share of keys that move', stmt='For 20,000 keys, compute the share that change machine when going from 10 to 11 machines with modulo hashing.', inp='keys k0…k19999 · 10 → 11 machines',
         code='''import zlib
keys = [f"k{i}" for i in range(20000)]
moved = sum(1 for k in keys if zlib.crc32(k.encode()) % 10 != zlib.crc32(k.encode()) % 11)
print(f"{moved / len(keys):.0%} of keys move")
''', explain='About 91%. Adding just one machine to ten moves almost everything. HDFS avoids this: the NameNode tracks each block\'s location individually, so adding nodes moves nothing until you choose to balance.'),
    dict(level='medium', title='Chance of a failure during the job', stmt='A job uses 3,000 machines for 24 hours. Each machine fails with probability 3% per year. What is the chance that at least one fails during the job?', inp='3000 machines · 24 h · 3%/year',
         code='''p = 0.03 * 24 / (365 * 24)
print(f"{1 - (1 - p) ** 3000:.1%}")
''', explain='About 22%: roughly one run in five hits a failure. Without automatic recovery, each of those runs fails entirely and starts again.'),
    dict(level='medium', title='Schema-on-read in miniature', stmt='Raw log lines are stored as they are. Only when reading, parse them into (city, amount) and sum per city, skipping broken lines.', inp='["Pune,240", "Delhi,120", "bad line", "Pune,60"]',
         code='''raw = ["Pune,240", "Delhi,120", "bad line", "Pune,60"]
totals = {}
for line in raw:
    parts = line.split(",")
    if len(parts) != 2 or not parts[1].isdigit():
        continue
    totals[parts[0]] = totals.get(parts[0], 0) + int(parts[1])
print(totals)
''', explain='Hadoop stores data first and applies structure when reading (schema-on-read). A database would reject the bad line at load time (schema-on-write).'),
    dict(level='business', title='When does the storage array become too expensive?', stmt='Data starts at 50 TB and doubles every year. A storage array costs Rs 40,000 per TB; the company\'s budget for it is Rs 5 crore. In which year does the array exceed the budget?', inp='50 TB · ×2 per year · Rs 40,000/TB · budget Rs 5 crore',
         code='''tb, year = 50, 0
while tb * 40_000 <= 5_00_00_000:
    tb *= 2
    year += 1
print("Year", year, ":", tb, "TB costs Rs", tb * 40_000 / 10**7, "crore")
''', explain='In year 5 (1,600 TB = Rs 6.4 crore). With exponential growth, scale-up storage stops being affordable within a few years. This calculation drove many companies to Hadoop.'),
    dict(level='business', title='Developer time saved by a framework', stmt='Each new data job needs about 2,000 lines of distribution code without a framework, and 0 with Hadoop. A developer writes about 100 tested lines a day and costs Rs 6,000 a day. The team builds 15 jobs a year. How much does the framework save per year?', inp='2000 lines/job · 100 lines/day · Rs 6,000/day · 15 jobs',
         code='''days_per_job = 2000 / 100
saving = days_per_job * 6000 * 15
print(f"Saved: {days_per_job * 15:.0f} developer-days = Rs {saving / 1e5:.0f} lakh a year")
''', explain='300 developer-days a year (illustrative numbers), before counting the bugs avoided. Frameworks pay for themselves in people\'s time.'),
]

SCN_INTRO = 'Questions interviewers ask to check that you understand why Hadoop exists, and where it fits today.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Why do we need Hadoop when we have Oracle?”</h4>
      <p class="scn__situation">The interviewer works at a bank that uses Oracle for its core systems. She asks why a bank would also run a Hadoop cluster.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you see Hadoop and databases as complementary, with different strengths?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Oracle</b> runs the core banking transactions: many small reads and writes, strict consistency, millisecond responses. Hadoop is not built for that.</li>
          <li><b>Hadoop</b> holds years of raw data from many systems (transactions, logs, call-centre notes, app clicks) cheaply, and runs large batch analytics: risk models, fraud features, regulatory reports.</li>
          <li>Moving that history and analytics load off the database saves expensive database capacity and lets analysts work on raw data.</li>
          <li>Data typically flows from the databases into Hadoop (and results flow back) through ingestion pipelines.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid saying:</b> “Hadoop replaces Oracle.”</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Career · honesty</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Isn't Hadoop outdated? Why did you learn it?”</h4>
      <p class="scn__situation">A startup interviewer who uses only cloud tools asks this, half-teasing.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you have a balanced, informed view of the ecosystem, rather than defending or dismissing it blindly?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Agree partly: classic MapReduce is rarely used for new work, and many new platforms use cloud object storage and Spark or warehouse engines.</li>
          <li>But HDFS, YARN and Hive still run in many large companies, and migrations from them are active projects.</li>
          <li>More importantly, Hadoop taught you the fundamentals that every tool relies on: partitioning data into blocks, replication, data locality, shuffles, master–worker scheduling and failure handling. That makes Spark, cloud warehouses and lakehouse tables easier to understand and tune.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> claiming Hadoop is the best choice for everything, or saying you learned it only because the syllabus required it.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">E-commerce · architecture</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Should this workload go to Hadoop?</h4>
      <p class="scn__situation">Three requests arrive: (a) the app needs to show a user's last 10 orders in under 100 ms; (b) analysts want to scan 3 years of clickstream to find drop-off patterns; (c) a dashboard needs results refreshed every 5 seconds. Which belong on a Hadoop cluster?</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you match workloads to Hadoop's design (high throughput batch) and spot the ones that don't fit?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>(a) No:</b> low-latency lookups of small records belong in a database or key–value store (or HBase, which runs on HDFS but is a different tool).</li>
          <li><b>(b) Yes:</b> scanning years of raw data in parallel is exactly Hadoop's job (with Hive or Spark on YARN).</li>
          <li><b>(c) Mostly no:</b> 5-second refreshes need stream processing (Kafka + Flink/Spark Streaming) or a real-time analytics database. Hadoop can hold the history behind it.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “Put everything in Hadoop.”</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · design</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>“Let's write our own distributed storage. It's just splitting files.”</h4>
      <p class="scn__situation">A confident teammate proposes a home-made system: split big files across servers with a hash of the filename, and a cron job to copy them for backup.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know the hard problems that frameworks like HDFS already solve?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><b>Growth:</b> hashing by N means adding servers moves most data; HDFS tracks each block's location and moves nothing unless asked.</li>
          <li><b>Failures:</b> detecting dead nodes, knowing which data lost copies, re-copying in the right order, avoiding false alarms.</li>
          <li><b>Correctness:</b> partial writes, corruption (checksums), consistent metadata, concurrent readers and writers.</li>
          <li><b>Locality and scheduling:</b> processing next to the data needs integration with the compute layer.</li>
          <li>All of this is years of work; HDFS has been hardened on thousands of clusters. Build only what is truly unique to the business.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> a flat “never build anything”. The point is knowing the true cost.</p>
      </div></details>
    </article>'''
