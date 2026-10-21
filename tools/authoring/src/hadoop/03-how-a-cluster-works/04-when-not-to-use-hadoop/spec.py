import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='03-how-a-cluster-works', lesson='04-when-not-to-use-hadoop', n='3.4',
    module_label='Module 3 · How one Hadoop cluster works',
    title='When not to use Hadoop',
    desc='When Hadoop is the wrong tool: small data, low-latency OLTP, real-time streaming, frequent updates, small files, iterative work and teams without operations staff, with the better alternative for each (DuckDB, PostgreSQL, cloud warehouses, Kafka and Flink, lakehouse tables), where Hadoop still wins, a decision checklist, cost calculations, quiz and interview scenarios.',
    og_desc='Knowing when to say “not Hadoop” is an expert skill. A checklist, the alternatives, and the cases where Hadoop still wins.',
    minutes=22, level='Beginner → Advanced',
    lead='Hadoop is brilliant for very large, batch, on-premises data with a team to run it, and a poor choice almost everywhere else. This lesson gives you a five-question checklist (size, latency, updates, team, location), the better tool for each case Hadoop handles badly, the situations where Hadoop is still the right answer, and the cost arithmetic behind the decision. Interviewers value this judgement as much as Hadoop knowledge itself.',
    chips=['Decision checklist', 'Runs in your browser (Python)', 'Test your own PC\'s speed'],
)

RUN = dict(
    heading='A tool-recommendation function',
    intro='<p>This function applies the five-question checklist from Part 4 to a workload and recommends a tool. Run it on the three projects from the animation, then try the challenges.</p>',
    code='''def recommend(size_tb, latency_s, updates, ops_team, must_be_onprem):
    if latency_s < 1:
        return "OLTP database or key-value store"
    if latency_s < 60:
        return "Stream processing (Kafka + Flink / Spark Streaming)"
    if size_tb < 1:
        return "One machine: PostgreSQL / DuckDB / pandas"
    if not ops_team and not must_be_onprem:
        return "Managed cloud warehouse or lakehouse"
    if updates:
        return "Lakehouse tables (Iceberg/Delta/Hudi) on Spark"
    return "Hadoop + Spark (batch, distributed)"

projects = {
    "pickle startup": (0.04, 86400, True, False, False),
    "fraud alerts":   (50, 2, False, True, False),
    "telecom CDRs":   (4000, 86400, False, True, True),
}
for name, p in projects.items():
    print(f"{name:15} -> {recommend(*p)}")
''',
    anno=[
        ('def recommend(size_tb, latency_s, updates, ops_team, must_be_onprem):', 'The five questions as parameters: size, how fast answers are needed, whether records change, whether a team can run a cluster, and where the data must live.'),
        ('if latency_s < 1:', 'The order of the checks matters: latency rules out batch tools first, whatever the data size.'),
        ('print(f"{name:15} -> {recommend(*p)}")', '<code>*p</code> unpacks the tuple into the five arguments.'),
    ],
    tasks=[
        dict(label='1 · Three projects', hint='Press <b>Run</b>. Then add <code>"bank risk reports": (300, 3600, False, True, True)</code>.', code=None),
        dict(label='2 · Will it fit in RAM?', hint='<b>Predict first:</b> with an analytical engine needing about 2× the compressed data size in RAM, does 40 GB fit a 64 GB server? Try 400 GB.',
             code='''ram_gb = 64
for data_gb in [10, 40, 400]:
    need = data_gb * 2
    print(f"{data_gb:>4} GB data -> needs ~{need} GB RAM: {'fits' if need <= ram_gb else 'too big for RAM (stream it or scale out)'}")
'''),
        dict(label='3 · Job start-up vs tiny data', hint='A MapReduce job pays a fixed start-up cost (AM, containers). For tiny inputs, the overhead dominates. Find the input size where work time equals start-up time.',
             code='''startup_s = 20          # AM + container launch, roughly
mb_per_s = 100          # one task's processing speed
for mb in [10, 100, 1000, 10000]:
    work = mb / mb_per_s
    print(f"{mb:>6} MB: work {work:6.1f} s vs start-up {startup_s} s")
'''),
        dict(label='4 · Small files and the NameNode', hint='Each file and block costs about 150 bytes each in NameNode memory. Compare 1 crore 10 KB files with the same data in 128 MB files.',
             code='''files = 1_00_00_000
small_mb = files * 2 * 150 / 1024 / 1024
data_mb = files * 10 / 1024
big_files = data_mb / 128
big_mb = big_files * 2 * 150 / 1024 / 1024
print(f"10 KB files : ~{small_mb:,.0f} MB of NameNode heap")
print(f"128 MB files: ~{big_mb:.2f} MB of NameNode heap")
'''),
        dict(label='5 · Spot the error', hint='This check should send real-time workloads to streaming, but the fraud case gets “Hadoop”. Fix the order of the conditions.',
             code='''def recommend(size_tb, latency_s):
    if size_tb > 10:
        return "Hadoop"
    if latency_s < 60:
        return "Streaming"
    return "One machine"

print("fraud alerts ->", recommend(50, 2))
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: how much can one computer do?',
    intro='<p>Before reaching for a cluster, measure a single machine. This program writes 20 lakh fake orders to a CSV file and totals them per item with plain Python on one core. Save it as <code>one_machine.py</code> and run it.</p>',
    items=[
        dict(title='Millions of rows per second, no cluster', file='one_machine.py',
             cmd=open(os.path.join(HERE, 'one_machine.py')).read() + '\n# In a terminal:  python one_machine.py',
             output='''Rows: 2,000,000  File: 35 MB
Write: 2.3 s   Group-by in plain Python: 1.1 s
Top item: vada pav
Rough speed: 1.8 million rows per second on one core''',
             note='Recorded on a small cloud machine with Python 3. Your numbers will differ. Plain Python is the <i>slow</i> option: engines like DuckDB or Polars are typically many times faster and use all cores. At these speeds, a few hundred million rows are a single-machine job.'),
    ],
)

TRACE = dict(
    heading='The checklist, one line at a time',
    intro='<p>Follow one workload (2 TB, answers needed within 2 seconds) through the decision function. Watch which condition decides.</p>',
    code='''def recommend(size_tb, latency_s, ops_team):
    if latency_s < 1:
        return "database"
    if latency_s < 60:
        return "streaming"
    if size_tb < 1:
        return "one machine"
    return "Hadoop + Spark" if ops_team else "cloud warehouse"

print(recommend(2, 2, True))
print(recommend(300, 3600, False))
''',
    notes={4: 'Latency :: Real-time needs are checked before size.'},
)

WORKED_INTRO = 'Three decisions a data team really makes: whether a data set needs a cluster at all, what each option costs over three years, and how to score options fairly. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Analytics · sizing', title='Does this data set need a cluster?',
         problem='<p>For each data set, decide: “one machine” if it is under 1 TB and grows less than 2× a year, otherwise “consider distributed”. Data sets: sales 80 GB (+30%/yr), clickstream 3 TB (+80%/yr), HR records 2 GB (+5%/yr), sensor data 600 GB (+300%/yr).</p>',
         inp='sales 80 GB +30% · clicks 3 TB +80% · HR 2 GB +5% · sensors 600 GB +300%',
         approach=['Convert sizes to TB.',
                   'Check both rules: size and growth.',
                   'Print a verdict for each.'],
         code='''data = {"sales": (0.08, 0.30), "clickstream": (3.0, 0.80),
        "hr": (0.002, 0.05), "sensors": (0.6, 3.00)}
for name, (tb, growth) in data.items():
    small = tb < 1 and growth < 1.0
    verdict = "one machine" if small else "consider distributed"
    print(f"{name:12}: {tb:>6} TB, +{growth:.0%}/yr -> {verdict}")
''', notes={4: 'Rule :: Small now AND not exploding in size.'},
         tryit='Sensors are only 600 GB today but quadruple every year: 2.4 TB, 9.6 TB… Plan for where the data will be, not where it is.'),
    dict(level='i', tag='Finance · TCO', title='3-year cost: own cluster vs cloud warehouse',
         problem='<p>A company has 20 TB and runs reports for 6 hours a day. Option A: an 8-node on-prem cluster at Rs 12 lakh per node, plus Rs 30 lakh per year for 1.5 engineers, power and space. Option B: a cloud warehouse at Rs 2,000 per TB stored per month plus Rs 25,000 per day of query compute. Compare 3-year costs (illustrative prices).</p>',
         inp='A: 8 × 12 L + 30 L/yr · B: 20 TB × Rs 2,000/month + Rs 25,000/day · 3 years',
         approach=['A = hardware once + yearly running cost × 3.',
                   'B = (storage per month × 36) + (compute per day × 365 × 3).',
                   'Compare in lakh.'],
         code='''years = 3
a = 8 * 12 + 30 * years                      # lakh
storage = 20 * 2000 * 12 * years / 1e5        # lakh
compute = 25000 * 365 * years / 1e5           # lakh
b = storage + compute
print(f"A on-prem cluster : Rs {a:.0f} lakh")
print(f"B cloud warehouse : Rs {b:.0f} lakh (storage {storage:.0f} + compute {compute:.0f})")
print("Cheaper:", "A" if a < b else "B")
''', notes={2: 'A :: Hardware bought once, people and power every year.'},
         tryit='Change query compute to Rs 8,000 a day (fewer reports). Which option wins now? The answer depends on usage, which is why you calculate instead of guessing.'),
    dict(level='a', tag='Architecture · decision matrix', title='Score the options with a weighted decision matrix',
         problem='<p>A bank compares three platforms for a 200 TB analytics workload. Criteria weights: cost 0.3, data residency 0.3, team skills 0.2, time to deliver 0.2. Scores (1–5): Hadoop+Spark on-prem (3, 5, 4, 3), cloud warehouse (4, 2, 3, 5), cloud lakehouse (4, 3, 3, 4). Compute weighted totals and pick the winner.</p>',
         inp='weights 0.3/0.3/0.2/0.2 · three options with four scores each',
         approach=['Weighted score = sum of weight × score for each criterion.',
                   'Compute for every option.',
                   'The highest total wins; show all totals so the decision is transparent.'],
         code='''weights = [0.3, 0.3, 0.2, 0.2]          # cost, residency, skills, time
options = {"Hadoop+Spark on-prem": [3, 5, 4, 3],
           "Cloud warehouse": [4, 2, 3, 5],
           "Cloud lakehouse": [4, 3, 3, 4]}
totals = {}
for name, scores in options.items():
    totals[name] = round(sum(w * s for w, s in zip(weights, scores)), 2)
    print(f"{name:22}: {totals[name]}")
print("Choose:", max(totals, key=totals.get))
''', notes={6: 'Score :: <code>zip</code> pairs each weight with its score.'},
         tryit='If the regulator allows an Indian cloud region, residency scores change (warehouse 4, lakehouse 4). Re-run: the decision can flip.'),
]

QUIZ = mix([
    dict(q='A startup has 30 GB of sales data and wants daily reports. The best choice is usually:', options=['A 10-node Hadoop cluster', 'A single database or analytics engine on one machine', 'A supercomputer', 'A streaming system'], answer=1,
         why='30 GB fits easily on one machine. A cluster adds cost and complexity with no benefit.'),
    dict(q='Which requirement rules out Hadoop MapReduce/Hive most clearly?', options=['Scanning 5 years of logs', 'Returning one customer\'s balance in 20 ms', 'Nightly batch reports', 'Storing 2 PB of history'], answer=1,
         why='Millisecond point lookups need an OLTP database or key–value store (or HBase), not batch processing.'),
    dict(q='A fraud system must react within 2 seconds of each payment. Which fits?', options=['Hourly MapReduce jobs', 'Kafka with Flink or Spark Structured Streaming', 'HDFS snapshots', 'A weekly Hive query'], answer=1,
         why='Real-time decisions need stream processing. Batch systems can train the model on history.'),
    dict(q='Why are millions of tiny files bad for HDFS?', options=['HDFS cannot store files under 1 MB', 'Every file and block uses NameNode memory, and each small file becomes a separate task', 'Tiny files are always corrupt', 'They are slower to download'], answer=1,
         why='The small-files problem is a NameNode memory and task-overhead problem. Combine files or use another store.'),
    dict(q='Which situation still favours Hadoop?', options=['A 3-person startup with 50 GB', 'Petabytes that must stay in the company\'s own data centre, with a skilled team', 'A mobile app\'s login database', 'A live cricket score feed'], answer=1,
         why='Huge batch data, data residency and an existing skilled team are where Hadoop remains strong.'),
    dict(q='What does TCO include?', options=['Only the server price', 'Hardware, software, people, power, space and downtime over the system\'s life', 'Only cloud bills', 'Only licence fees'], answer=1,
         why='Total cost of ownership counts everything. Staff to run a cluster is often the biggest item.'),
    dict(q='Records in a table change status many times a day, and analysts need SQL on them. A good modern option is:', options=['Plain files on HDFS', 'Lakehouse table formats such as Iceberg, Delta Lake or Hudi (or a database)', 'MapReduce jobs that rewrite everything hourly', 'Tape backup'], answer=1,
         why='Table formats add updates and deletes on top of files; HDFS files themselves are write-once.'),
    dict(q='Your manager asks “Should we use Hadoop?”. The best first step is:', options=['Say yes, it is industry standard', 'Ask about data size and growth, latency needs, updates, team and data location', 'Say no, Hadoop is dead', 'Buy servers first'], answer=1,
         why='Requirements decide the tool. Asking the five questions makes the answer clear and defensible.'),
])

REVISION = [
    'Hadoop fits: <b>huge</b>, <b>batch</b>, mostly append-only data, run by a <b>skilled team</b>, often <b>on-premises</b>.',
    'Not Hadoop: <b>small data</b> (one machine), <b>ms lookups</b> (database), <b>real time</b> (streaming), <b>frequent updates</b> (DB / table formats).',
    'Also bad: <b>millions of small files</b>, <b>iterative/interactive</b> work on MapReduce, <b>no ops team</b>.',
    'Checklist: size + growth · latency · updates · team · location.',
    'Rough sizes: ≤ tens of GB laptop · ≤ few TB one big server / warehouse · tens of TB+ distributed.',
    'Still wins: petabytes on-prem, data residency, existing investment, shared multi-engine platform.',
    'Modern replacements: Spark (engine), object storage (HDFS), Iceberg/Delta/Hudi (tables), cloud warehouses.',
    'Decide with numbers: TCO over 3 years and a weighted decision matrix.',
]
FAQ = [
    ('What are the limitations of Hadoop?', 'High latency (batch-oriented), unsuitable for real-time processing and point lookups, inefficient with many small files because of NameNode memory and task overhead, write-once files that make updates difficult, slow iterative processing with MapReduce, and considerable operational and security complexity. For small data it is slower and costlier than single-machine tools.'),
    ('When would you not recommend Hadoop?', 'When the data fits comfortably on one machine; when the workload needs millisecond responses or frequent record updates; when results are needed in real time; when data arrives as huge numbers of tiny files; or when the organisation has no team to operate a cluster and can use managed cloud services instead.'),
    ('What are alternatives to Hadoop?', 'For processing: Spark, Flink, Trino. For storage: cloud object storage with table formats (Iceberg, Delta Lake, Hudi). For analytics: cloud data warehouses (BigQuery, Snowflake, Redshift, Synapse) and OLAP engines (ClickHouse, Druid). For small data: PostgreSQL, DuckDB, Polars, pandas. For streams: Kafka with Flink or Spark Structured Streaming.'),
    ('Is Hadoop still worth learning?', 'Yes, as a foundation. Many enterprises still run it, migrations from it are common, and its concepts (distributed storage, replication, data locality, MapReduce, resource management) underlie modern platforms. Knowing its limits is part of knowing it well.'),
    ('How would you decide between Hadoop and a cloud data warehouse?', 'Compare requirements and total cost: data volume and growth, query patterns, latency, data-residency rules, existing skills and investments, and three-year TCO including staff. Steady, very large on-premises workloads with residency rules may favour Hadoop/Spark; smaller teams with variable, SQL-centric workloads often favour a managed warehouse.'),
]

PRACTICE_INTRO = 'Decision and cost exercises. Each one asks you to justify “Hadoop or not?” with numbers.'
PROBLEMS = [
    dict(level='easy', title='Fits on the laptop?', stmt='A laptop has a 1 TB SSD and the data is 120 GB. Will it fit with 50% of the disk kept free?', inp='1 TB SSD · 120 GB · 50% free',
         code='print("Fits:", 120 <= 1024 * 0.5)\n', explain='120 GB is well under 512 GB. No cluster needed to store it.'),
    dict(level='easy', title='Grow the data', stmt='Data is 300 GB and grows 40% a year. How big in 4 years?', inp='300 GB · +40% · 4 years',
         code='print(round(300 * 1.4 ** 4), "GB")\n', explain='About 1,152 GB: crossing 1 TB. Time to plan, not to panic; one big server may still do.'),
    dict(level='easy', title='Classify latency needs', stmt='Classify each response-time need as "OLTP" (< 1 s), "streaming" (< 1 min) or "batch".', inp='[0.05, 5, 3600]',
         code='''for s in [0.05, 5, 3600]:
    print(s, "s ->", "OLTP" if s < 1 else "streaming" if s < 60 else "batch")
''', explain='Only the last one is a natural fit for Hadoop-style batch processing.'),
    dict(level='medium', title='Startup overhead share', stmt='A job has 20 s of fixed start-up and processes 50 MB/s. For inputs of 100 MB, 10 GB and 1 TB, print the share of total time spent on start-up.', inp='20 s · 50 MB/s · [100 MB, 10 GB, 1 TB]',
         code='''for mb in [100, 10 * 1024, 1024 * 1024]:
    work = mb / 50
    print(f"{mb:>8} MB: start-up is {20 / (20 + work):.1%} of the time")
''', explain='For 100 MB, start-up is 91% of the time; for 1 TB it is negligible (a single task here; real jobs split the work). Small jobs are wasteful on batch frameworks.'),
    dict(level='medium', title='Small files combined', stmt='50 lakh sensor files of 20 KB each are combined into 256 MB files. How many files before and after?', inp='50,00,000 × 20 KB · 256 MB',
         code='''import math
files = 50_00_000
total_mb = files * 20 / 1024
print(files, "->", math.ceil(total_mb / 256), "files")
''', explain='About 382 files instead of 50 lakh: thousands of times less NameNode memory and far fewer map tasks.'),
    dict(level='medium', title='Pick by rules', stmt='Write a function that returns "Hadoop" only if size ≥ 10 TB, latency ≥ 1 hour, and there is an ops team; otherwise "something else". Test three cases.', inp='(50, 7200, True) · (5, 7200, True) · (50, 7200, False)',
         code='''def fits(size_tb, latency_s, ops):
    return "Hadoop" if size_tb >= 10 and latency_s >= 3600 and ops else "something else"
for c in [(50, 7200, True), (5, 7200, True), (50, 7200, False)]:
    print(c, "->", fits(*c))
''', explain='All conditions must hold. Missing any one (size, batch latency, team) is a reason to look elsewhere.'),
    dict(level='business', title='Engineers are the biggest cost', stmt='A 10-node cluster costs Rs 1.2 crore in hardware (5-year life). Running it needs 2 engineers at Rs 25 lakh per year each, plus Rs 8 lakh per year for power and space. What share of the yearly cost is people?', inp='Rs 1.2 crore / 5 years · 2 × Rs 25 L · Rs 8 L',
         code='''hardware = 120 / 5
people = 2 * 25
other = 8
total = hardware + people + other
print(f"Yearly: Rs {total:.0f} lakh; people = {people / total:.0%}")
''', explain='People are about 61% of the yearly cost (illustrative figures). For small data, that cost alone outweighs any benefit of a cluster.'),
    dict(level='business', title='Break-even for owning a cluster', stmt='A cloud option costs Rs 1.5 lakh per TB-year of data analysed. An on-prem cluster costs Rs 90 lakh per year whatever the size (up to its capacity). Above how many TB is on-prem cheaper?', inp='Rs 1.5 L per TB-year · Rs 90 L per year fixed',
         code='''import math
print("On-prem cheaper above", math.floor(90 / 1.5) + 1, "TB")
''', explain='Above about 61 TB (illustrative). Below it, pay-per-use wins; well above it and steady, owning hardware can win. Real decisions also weigh residency, skills and flexibility.'),
]

SCN_INTRO = 'Interviewers often test judgement with a “should we use Hadoop?” question. Practise answering with questions, numbers and alternatives.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Startup · architecture</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Our 50 GB database is slow, so let's move to Hadoop”</h4>
      <p class="scn__situation">A startup's PostgreSQL reports take minutes. Someone proposes moving everything to Hadoop “because it's built for big data”.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you diagnose before prescribing, and do you know that 50 GB is not big data?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>50 GB is small. A cluster would add overhead and operations work, and probably be slower for these queries.</li>
          <li>First diagnose: missing indexes, reports running on the live transactional database, poor query design.</li>
          <li>Options: add indexes and summary tables; run reports on a read replica; copy data nightly to DuckDB or a small cloud warehouse for analytics.</li>
          <li>Revisit distributed tools if the data grows to many TB.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> recommending Hadoop because it is “the big data tool”.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Payments · real time</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Use Hive for live fraud alerts?</h4>
      <p class="scn__situation">A payments team stores all transactions in Hive and runs a fraud query every 15 minutes. Fraudsters complete their attacks in under 5 minutes.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you separate real-time and batch needs?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>A 15-minute batch loop can never stop a 5-minute attack. Scoring must happen on each transaction as it arrives.</li>
          <li>Stream transactions through Kafka; score them with Flink or Spark Structured Streaming using features kept in a fast store; block or flag in milliseconds to seconds.</li>
          <li>Keep Hive/Spark on the history to train and evaluate the models nightly, and for investigations.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “Run the Hive query every minute.” Batch start-up and scan costs make that impractical and still too slow.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">IoT · storage</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>The NameNode keeps running out of memory</h4>
      <p class="scn__situation">A smart-meter project writes every reading (a few KB) as its own file into HDFS. After six months the NameNode heap is full and restarts take hours.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you recognise the small-files problem and its fixes?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Hundreds of millions of tiny files mean hundreds of millions of file and block objects in NameNode memory.</li>
          <li>Short term: compact existing files into large Parquet or SequenceFiles per hour/day, and archive old ones (HAR).</li>
          <li>Long term: send readings to Kafka and write large files in batches; or store raw readings in an object store or a time-series database designed for many small writes.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> only increasing the NameNode heap; it delays the problem and makes pauses worse.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Enterprise · strategy</span><span class="scn__tag scn__tag--level">3+ years</span></div>
      <h4>“Should we shut down our Hadoop cluster and move to the cloud?”</h4>
      <p class="scn__situation">A bank runs a 150-node Hadoop cluster with 3 PB. The CIO hears “Hadoop is dead” and asks for a recommendation.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you give a balanced, requirement-driven recommendation?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ol>
          <li><b>Constraints:</b> can this data legally be in a public cloud region? Many banking rules require data to stay in India and under specific controls.</li>
          <li><b>Cost:</b> compare 3–5 year TCO, including migration effort, cloud egress and staff, against hardware refresh costs.</li>
          <li><b>Workloads:</b> which jobs are steady and heavy (cheaper on owned hardware) and which are spiky or new (better in the cloud)?</li>
          <li><b>Path:</b> often a phased or hybrid approach: modernise on-prem (Spark, table formats), move suitable workloads first, keep the rest until hardware refresh.</li>
        </ol>
        <p class="scn__avoid"><b>Avoid:</b> deciding on fashion (“Hadoop is dead”) or on fear of change.</p>
      </div></details>
    </article>'''
