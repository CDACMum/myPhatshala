import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

MODULES = [('1', 'Introduction', '5 Vs · one computer is not enough · distributed basics · history', 4, 'blue'),
           ('2', 'Data and storage', 'data types · file formats · storage · NoSQL', 4, 'blue'),
           ('3', 'Distributed systems', 'scale out · partitioning · replication · CAP', 4, 'acc'),
           ('4', 'The ecosystem', 'Hadoop · Spark · Kafka · lakehouse · pipelines · cloud · India scale', 7, 'acc'),
           ('5', 'Governance', 'quality · governance · security · DPDP', 1, 'violet'),
           ('6', 'Careers', 'roles · roadmap · resume · interviews', 3, 'green'),
           ('7', 'Capstone', 'mini pipeline · final test', 2, 'green')]

# ---------------------------------------------------------------- story
sc = ''
for k, (n, name, _, cnt, tone) in enumerate(MODULES):
    x = 14 + k * 88
    sc += box(x, 26, 82, 96, tone) + t(x + 41, 50, f'Module {n}', 8.6, 'ink2') + t(x + 41, 72, name.split(' ')[0], 9.4, bold=True)
    sc += t(x + 41, 88, ' '.join(name.split(' ')[1:]), 8.4, bold=True) + t(x + 41, 110, f'{cnt} lesson' + ('s' if cnt > 1 else ''), 8.2, 'ink2')
scene_svg = scene('Seven modules of Big Data Fundamentals: introduction, data and storage, distributed systems, the ecosystem, governance, careers and the capstone, 25 lessons in all.', sc,
                  '25 lessons, one course: <tspan font-weight="700" class="s-acc">time to bring it all together</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Riya’s semester exam in Big Data is next week. Kabir has just received his full-time offer from TiffinGo, and the first thing he does is call Riya to help her revise. Arjun Sir joins them for one last session.</p>

{scene_svg}

R> Sir, there’s so much. 5 Vs, CAP, Spark, Kafka, Parquet, DPDP… where do I even start?
A> With the map, Riya. Every lesson answers one of four questions: <b>what</b> is big data, <b>how</b> do we store and spread it, <b>which tools</b> process it, and <b>how</b> do we keep it trustworthy and useful. If you can place each topic on that map, you can write any answer.
K> In my interviews, they never asked definitions alone. Always “why” and “what if”.
A> Exams reward the same thing in long answers: a definition, a diagram, an example and a trade-off. Today you get a one-page cheat sheet, the 2-mark and 5-mark answer patterns, a 50-mark practice paper you can regenerate on your PC, and a final test across the whole course.
R> And if I score well on the final test?
A> Then you’re ready, for the exam and for Kabir’s kind of interviews.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Revision at three levels
L1> Remember the core
      <ul>
      <li><b>Big data:</b> 5 Vs; why one machine fails (disk speed, memory, single point of failure); scale out.</li>
      <li><b>Data:</b> structured, semi-structured, unstructured; CSV, JSON, Avro, Parquet, ORC; files, blocks, objects; NoSQL types.</li>
      <li><b>Systems:</b> partitioning, replication (factor 3), CAP, consistency levels.</li>
      <li><b>Tools:</b> HDFS, YARN, MapReduce, Hive, Spark, Kafka, lakehouse; Airflow; AWS/Azure/GCP equivalents.</li>
      </ul>
L2> Explain and compare
      <ul>
      <li>Row vs columnar; lake vs warehouse vs lakehouse; batch vs streaming; ETL vs ELT; MapReduce vs Spark.</li>
      <li>Scale up vs scale out; leader-follower vs leaderless replication; strong vs eventual consistency.</li>
      <li>Mod-N hashing vs consistent hashing; provisioned vs serverless cloud.</li>
      <li>Six data quality dimensions; governance components; DPDP rights and duties.</li>
      </ul>
L3> Apply and design
      <ul>
      <li>Estimate load: totals → per second → peak; storage with replication and retention.</li>
      <li>Design a pipeline: requirements, ingestion, bronze/silver/gold, orchestration, quality, idempotency, cost and governance.</li>
      <li>Diagnose: skew, small files, wrong numbers (lineage), duplicates (idempotency), cost spikes (scans, idle clusters).</li>
      <li>Case studies: UPI, IRCTC Tatkal, live cricket streaming, sale days.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Big Data Fundamentals</b> covers the characteristics of data sets too large, fast or varied for a single traditional system (<b>volume, velocity, variety, veracity, value</b>); the storage formats and databases suited to them; the <b>distributed-systems</b> principles of scaling out, partitioning, replication and consistency; the <b>ecosystem</b> of processing and streaming tools (Hadoop, Spark, Kafka, lakehouse table formats, orchestration, cloud services); the practices of <b>data quality, governance, security and privacy</b>; and the roles and skills of data professionals, applied in an end-to-end pipeline.',
    'Big data is data too big, fast or messy for one computer. We spread it across many machines, store it in efficient formats, process it with tools like Spark and Kafka, keep it correct, safe and lawful, and turn it into useful answers.') + '''

  <h3>The course on one page</h3>
''' + table(['Module', 'Lessons', 'Must remember'], [[f'<b>{n}. {name}</b>', str(cnt), keys] for n, name, keys, cnt, _ in MODULES], minw=600) + lv + '''
EXAM> A full-marks long answer has five parts: <b>definition</b> (1–2 lines), <b>diagram</b> (labelled), <b>explanation</b> (points, not paragraphs), <b>example</b> (preferably Indian and with numbers) and <b>advantages/limitations or a comparison table</b>. Underline key terms.'''

# ---------------------------------------------------------------- types: cheat sheet
types = '''  <h3>Cheat sheet: numbers and units</h3>
''' + table(['Unit or fact', 'Value', 'Use it for'], [
    ['1 KB → MB → GB → TB → PB', '× 1,000 each step (decimal); 1,024 in binary units', 'Storage estimates'],
    ['1 lakh / 1 crore', '1,00,000 / 1,00,00,000 (100 lakh)', 'Indian figures in answers'],
    ['Seconds in a day', '86,400', 'Daily totals → per second'],
    ['HDFS default block / replication', '128 MB / 3 copies', 'Hadoop questions'],
    ['Replicas for quorum', 'R + W > N (e.g. N=3, W=2, R=2)', 'Consistency questions'],
    ['UPI (Sept 2026)', '24.07 billion transactions ≈ 9,300 per second on average', 'Velocity and scale examples'],
    ['IRCTC peak', '37,410 tickets in one minute (Aug 2025)', 'Peak load examples'],
    ['DPDP breach report', 'Detailed report to the Board within 72 hours', 'Privacy questions'],
], minw=600) + '''

  <h3>Cheat sheet: comparisons examiners love</h3>
''' + table(['Compare', 'First', 'Second'], [
    ['<b>Scale up vs scale out</b>', 'Bigger machine; simple; hard ceiling; single point of failure', 'More machines; near-linear growth; needs distribution and fault tolerance'],
    ['<b>Row vs columnar</b>', 'CSV, Avro: good for writing whole records', 'Parquet, ORC: good for reading few columns of many rows'],
    ['<b>Lake vs warehouse</b>', 'Raw files, any type, cheap, schema-on-read', 'Modelled tables, SQL, fast, schema-on-write'],
    ['<b>Batch vs streaming</b>', 'Bounded data, scheduled, minutes to hours', 'Unbounded events, continuous, milliseconds to seconds'],
    ['<b>MapReduce vs Spark</b>', 'Disk between every step, Java-heavy', 'In-memory DAG execution, SQL/Python APIs, much faster for iterative work'],
    ['<b>CP vs AP</b>', 'Refuse or delay to stay consistent (payments)', 'Answer with possibly stale data (feeds, carts)'],
    ['<b>ETL vs ELT</b>', 'Transform before loading', 'Load raw, transform inside the warehouse/lakehouse'],
], minw=640) + '''
TIP> Before the exam, redraw five diagrams from memory: <b>HDFS (NameNode, DataNodes, replicas)</b>, <b>Spark (driver, executors, stages)</b>, <b>Kafka (producers, partitions, consumer groups)</b>, <b>consistent hashing ring</b> and <b>bronze-silver-gold pipeline</b>. Diagrams earn marks quickly.'''

# ---------------------------------------------------------------- steps
c1 = '''day1, day3, day7 = "learn", "recall", "recall again"
for d, task in [(1, day1), (3, day3), (7, day7)]:
    print(f"day {d}: {task}")'''
steps = stepper([
    ('Map before memorising',
     '<p>Write the seven modules on one page and, under each, the lessons and three key words from memory. Fill gaps from the cheat sheet.</p>',
     'A mental map makes every answer easier to place and connect.'),
    ('Practise recall, not rereading',
     code('python', 'spaced.py', c1, run_code(c1)),
     'Testing yourself after a gap (day 1, day 3, day 7) builds memory far better than rereading notes.'),
    ('Use answer patterns',
     '<p>2 marks: definition + one example or point. 5 marks: definition, diagram, 3–4 points, example. 10 marks: add comparison table, case study, advantages and limitations.</p>',
     'Patterns stop you writing too much for small questions and too little for big ones.'),
    ('Take a timed paper',
     '<p>Generate a paper with the program in “Run it on your PC”, write answers in 2 hours, then check against the lessons.</p>',
     'Timing matters: about 22 minutes per 10 marks leaves 10 minutes to revise.'),
    ('Fix weak areas',
     '<p>Note every question you struggled with, revisit that lesson’s Revision and FAQ sections, and redo its quiz.</p>',
     'Targeted revision on weak lessons gives the biggest improvement per hour.'),
    ('Final test',
     '<p>Take the 25-question final test on this page. Aim for 20 or more; review explanations for every mistake.</p>',
     'It samples every module, so your score shows where you stand overall.'),
])

# ---------------------------------------------------------------- two-view animation: writing a 5-mark answer
def sheet(lines, note):
    o = box(20, 12, 320, 190, 'card') + t(34, 32, 'Q. Explain the CAP theorem.  [5]', 9, 'acc', anchor='start', bold=True)
    for k, s in enumerate(lines):
        o += t(34, 54 + k * 17, s, 8.4, anchor='start')
    return o + t(180, 216, note, 8.2, 'ink2')
A = ['1. CAP: in a distributed system, during a network', '   partition you can keep Consistency or Availability.',
     '2. [diagram: two nodes, broken link, client]', '3. C: every read sees the latest write.', '   A: every request gets a response. P: tolerate splits.',
     '4. e.g. UPI balance → CP; Instagram likes → AP.', '5. No partition → can have both; PACELC adds latency.']
see = [sheet(A[:0], 'Riya reads the question: 5 marks.'), sheet(A[:2], 'Starts with a crisp definition.'), sheet(A[:3], 'Adds a labelled diagram.'),
       sheet(A[:5], 'Explains each letter in short points.'), sheet(A[:6], 'Gives real Indian examples.'), sheet(A[:7], 'Ends with a limitation / extension.')]
def scheme(got, note):
    items = [('Definition', 1), ('Diagram', 1), ('Explanation of C, A, P', 1), ('Examples', 1), ('Limitation / insight', 1)]
    o = t(180, 26, 'Examiner’s marking scheme', 9.6, 'acc', bold=True)
    for k, (n, m) in enumerate(items):
        ok = k < got
        o += t(40, 54 + k * 22, ('✓ ' if ok else '○ ') + n, 9, 'green' if ok else 'ink3', anchor='start') + t(320, 54 + k * 22, f'{m if ok else 0}/{m}', 9, 'green' if ok else 'ink3', anchor='end', bold=True)
    return o + t(180, 180, f'Total so far: {got}/5', 10, 'green' if got == 5 else 'ink', bold=True) + t(180, 200, note, 8.4, 'ink2')
behind = [scheme(0, 'Five marks usually means five distinct points.'), scheme(1, 'A correct one-line definition: 1 mark.'), scheme(2, 'A labelled diagram: 1 mark, quickly earned.'),
          scheme(3, 'Clear meaning of each property: 1 mark.'), scheme(4, 'Concrete examples show understanding: 1 mark.'), scheme(5, 'An insight beyond the basics: the final mark.')]
see_caps = ['Riya reads a 5-mark question on the CAP theorem.', 'She writes a precise definition first.', 'She draws a small labelled diagram of a network partition.',
            'She explains C, A and P in short points.', 'She adds examples: UPI balances (CP) and social-media likes (AP).', 'She finishes with a limitation and the PACELC extension.']
behind_caps = ['Marking schemes for 5-mark questions typically look for about five distinct elements.',
               'A precise definition earns the first mark.', 'A diagram earns a mark in seconds and makes the answer easy to check.',
               'Explaining each property separately earns the explanation mark.', 'Real examples prove understanding rather than memorising.',
               'A limitation or extension (no partition means both are possible; PACELC adds the latency vs consistency trade-off) earns the last mark. Schemes vary by university; this is a typical pattern.']
two = anim_two('Writing a 5-mark answer', 'What Riya writes, and how it is marked', 'Riya writing a five-mark answer on the CAP theorem point by point',
               'An examiner’s marking scheme filling up mark by mark', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: course map recap
def cmap(n, note1, note2, tone):
    o = ''
    for k, (num, name, keys, cnt, tn) in enumerate(MODULES):
        y = 14 + k * 17
        on = k < n
        o += fill(14, y, 14, 13, tn if on else 'grey', rx=3) + t(36, y + 10, f'{num}. {name}', 8.4, 'ink' if on else 'ink3', anchor='start', bold=on)
        if on:
            o += t(150, y + 10, keys[:44] + ('…' if len(keys) > 44 else ''), 7.4, 'ink2', anchor='start')
    return o + cap(note1, note2, tone, y=146, h=44)
fr1 = [
    cmap(2, 'What is big data, and how is it stored?', 'Modules 1–2: 5 Vs, formats, storage, NoSQL.', 'blue'),
    cmap(3, 'How do we spread it over many machines?', 'Module 3: scale out, partition, replicate, CAP.', 'acc'),
    cmap(4, 'Which tools process it?', 'Module 4: Hadoop, Spark, Kafka, lakehouse, cloud.', 'acc'),
    cmap(5, 'How do we keep it trustworthy and lawful?', 'Module 5: quality, governance, security, DPDP.', 'violet'),
    cmap(7, 'How do you use it in a career?', 'Modules 6–7: roles, interviews, capstone.', 'green'),
]
s1 = anim_one('Real-time scenario 1', 'The whole course in four questions',
              'Every lesson answers one of four questions. Watch the modules light up as each question is answered; use this map as the skeleton of your revision.',
              'Course map', 'Seven course modules grouped under four questions: what and where, how to spread, which tools, how to trust, then careers', fr1,
              ['Modules 1 and 2 answer “what is big data and where does it live?”: the 5 Vs, limits of one computer, data types, file formats, storage systems and NoSQL databases.',
               'Module 3 answers “how do we spread it over many machines?”: scaling out, partitioning and sharding, replication and the CAP theorem.',
               'Module 4 answers “which tools process it?”: Hadoop, Spark, Kafka, lakehouses, pipelines and orchestration, the cloud, and Indian-scale case studies.',
               'Module 5 answers “how do we keep it trustworthy and lawful?”: data quality, governance, security and the DPDP Act.',
               'Modules 6 and 7 turn it into a career: roles, roadmap, interviews, and a capstone pipeline you built yourself.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: estimation question
def est(lines, note1, note2, tone):
    o = box(14, 14, 332, 118, 'card') + t(28, 34, 'Q. A platform handles 24 billion payments a month.', 8.8, 'acc', anchor='start', bold=True) + t(28, 50, '   Estimate average TPS, peak TPS and yearly storage.  [5]', 8.8, 'acc', anchor='start', bold=True)
    for k, s in enumerate(lines):
        o += t(28, 72 + k * 15, s, 8.4, anchor='start', mono=True)
    return o + cap(note1, note2, tone, y=146, h=44)
E = ['avg = 24e9 / (30 × 86,400) ≈ 9,300 TPS', 'peak (assume 4×) ≈ 37,000 TPS', 'storage = 24e9 × 12 × 1 KB ≈ 288 TB/yr', '× 3 replicas ≈ 864 TB/yr ≈ 0.9 PB']
fr2 = [
    est([], 'Estimation questions appear in exams and', 'interviews. First, write the formula.', 'blue'),
    est(E[:1], 'Monthly total ÷ seconds in a month', '≈ 9,300 transactions per second.', 'acc'),
    est(E[:2], 'State an assumption for the peak (4×):', 'design for about 37,000 TPS.', 'acc'),
    est(E[:3], 'Assume 1 KB per transaction record:', 'about 288 TB a year.', 'violet'),
    est(E[:4], 'With 3 replicas: about 0.9 PB a year.', 'Assumptions stated = full marks.', 'green'),
]
s2 = anim_one('Real-time scenario 2', 'An estimation question, solved for full marks',
              'Numbers questions reward clear steps and stated assumptions more than exact answers. Watch one solved line by line, using UPI-scale figures.',
              'Estimation', 'Converting 24 billion monthly payments into average TPS, peak TPS and yearly storage with replication', fr2,
              ['Start by writing what you will compute and how: totals → per second → peak → storage.',
               '24 billion ÷ (30 × 86,400 seconds) ≈ 9,300 transactions per second on average.',
               'Peaks are higher. State an assumption (4× the average) and design for about 37,000 TPS.',
               'Assume each transaction record is about 1 KB: 24 billion × 12 months × 1 KB ≈ 288 TB a year.',
               'With a replication factor of 3, about 864 TB, or roughly 0.9 PB, a year. Each assumption is written down, so the examiner can follow and award marks even if their numbers differ.'])

# ---------------------------------------------------------------- scenario 3 (advanced): one case, all modules
case = [('Scale', '1', 'blue'), ('Store, cache', '2', 'blue'), ('Shard, replicate', '3', 'acc'), ('Kafka, Spark', '4', 'acc'), ('Quality, DPDP', '5', 'violet')]
def caseframe(n, note1, note2, tone):
    o = t(180, 20, 'Case: a railway booking platform on Tatkal day', 9.4, bold=True)
    for k, (a, m, tn) in enumerate(case[:n]):
        x = 14 + k * 67
        o += label_box(x, 34, 62, 56, [f'Module {m}'] + a.split(', ') if ', ' in a else [f'Module {m}', a], tn, 7.6)
    return o + cap(note1, note2, tone, y=110, h=44)
fr3 = [
    caseframe(1, 'Start with scale: 37,410 tickets per minute ≈ 624/s', 'at peak; crores of searches (Module 1).', 'blue'),
    caseframe(2, 'Bookings in a strongly consistent store; logs as', 'Parquet in the lake; cache for availability (2).', 'blue'),
    caseframe(3, 'Partition by train and date; replicate across zones;', 'seats need CP, search results can be AP (3).', 'acc'),
    caseframe(4, 'Events to Kafka; Spark for demand forecasts and bot', 'detection; waiting room in front of booking (4).', 'acc'),
    caseframe(5, 'Quality checks on bookings; passenger data protected', 'under DPDP; masked for analysts (5).', 'violet'),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'One 10-mark case, every module',
              'The best long answers pull ideas from across the course. Watch a railway booking case answered module by module, the structure that earns top marks.',
              'Integrated case answer', 'A Tatkal-day booking platform answered using ideas from all five technical modules', fr3,
              ['Begin with scale from published numbers: 37,410 tickets in one minute is about 624 per second at peak, with far more searches. This shows volume and velocity (Module 1).',
               'Choose storage: bookings in a strongly consistent transactional store, logs and history as Parquet in a lake, and a cache for seat availability pages (Module 2).',
               'Spread the load: partition by train and date, replicate across zones; seat allocation needs consistency (CP), while search results can be slightly stale (AP) (Module 3).',
               'Process: booking and search events flow into Kafka; Spark builds demand forecasts and detects bots; a waiting room protects the booking system at 10 am (Module 4).',
               'Trust: quality checks on booking data, passenger personal data protected under the DPDP Act, masked for analysts, with breach plans (Module 5). Add a diagram and a limitations paragraph for full marks.'])

# ---------------------------------------------------------------- question banks
def bank(title, qa):
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>\n    ' for q, a in qa)
    return f'\n  <h4>{title}</h4>\n  <div class="faq">\n    {items}</div>\n'

two_mark = bank('2-mark questions with model answers', [
    ('Define big data.', 'Data sets whose volume, velocity or variety exceed the capacity of traditional single-machine systems to store and process them in acceptable time, requiring distributed storage and processing.'),
    ('What is veracity?', 'The quality and trustworthiness of data: accuracy, completeness and consistency. Example: duplicate or fake transactions reduce veracity.'),
    ('Differentiate structured and semi-structured data.', 'Structured data has a fixed schema of rows and columns (a bank table); semi-structured data has tags or keys but a flexible schema (JSON, XML).'),
    ('What is a NameNode?', 'The HDFS master that stores the file system metadata (file names, block locations) and coordinates DataNodes, which store the actual blocks.'),
    ('What is schema-on-read?', 'The schema is applied when data is read rather than when it is written, as in data lakes; allows storing raw data first.'),
    ('What is a partition key?', 'The column whose value decides which partition or shard a row belongs to, for example customer_id or date.'),
    ('What is eventual consistency?', 'If no new updates occur, all replicas eventually converge to the same value; reads may briefly return stale data.'),
    ('What is a DAG in Spark or Airflow?', 'A directed acyclic graph of steps with dependencies and no cycles; Spark uses it for stages of computation, Airflow for task order.'),
    ('What is a Kafka offset?', 'The sequential position of a message within a partition, used by consumers to track what they have read.'),
    ('What is the lakehouse?', 'An architecture combining low-cost lake storage with warehouse features (ACID transactions, schemas, fast SQL) using table formats such as Delta Lake, Iceberg or Hudi.'),
    ('What is egress in cloud billing?', 'Charges for data transferred out of a cloud region or out of the cloud, often a hidden cost.'),
    ('Who is a data fiduciary under the DPDP Act?', 'The person or organisation that determines the purpose and means of processing personal data.'),
])
five_mark = bank('5-mark questions with answer outlines', [
    ('Explain the 5 Vs of big data with examples.', 'Define each V in one line with an Indian example: volume (UPI billions a month), velocity (live cricket concurrency), variety (text, images, logs), veracity (fake reviews, duplicates), value (fraud detection, recommendations). Add a small diagram of the five Vs.'),
    ('Why is one computer not enough for big data?', 'Disk read speed limits (hours to scan TBs), memory limits, CPU limits, single point of failure, cost of very large machines. Solution: split data and work across many machines (parallelism) with replication. Include a calculation, e.g. 10 TB at 200 MB/s ≈ 14 hours vs 100 machines ≈ 8 minutes.'),
    ('Compare CSV, JSON, Avro, Parquet and ORC.', 'Table with: row/columnar, schema, compression, splittable, best use. CSV/JSON human-readable but large; Avro row-based with schema, good for streaming and Kafka; Parquet/ORC columnar, compressed, best for analytics.'),
    ('Explain replication strategies.', 'Leader-follower (writes to leader, followers copy; sync vs async), multi-leader, leaderless with quorums (R + W > N). Benefits: availability, durability, read scaling; issues: lag, conflicts, failover. Diagram.'),
    ('Explain Spark architecture.', 'Driver, cluster manager, executors; jobs, stages, tasks; lazy evaluation and DAG; narrow vs wide transformations and shuffles; in-memory processing. Diagram with driver and executors.'),
    ('Explain Kafka architecture.', 'Producers, brokers, topics, partitions, offsets, replication, consumer groups; ordering per partition; retention; use cases like UPI events or order tracking. Diagram.'),
    ('Explain cloud service models for big data with AWS/Azure/GCP examples.', 'IaaS, managed PaaS, serverless, SaaS; examples: S3/ADLS/GCS, EMR/Databricks/Dataproc, Redshift/Synapse/BigQuery; benefits and concerns (cost, lock-in, residency).'),
    ('Explain the DPDP Act, 2023 from a data engineer’s point of view.', 'Fiduciary and principal; consent and notice; purpose limitation; rights (access, correction, erasure); security safeguards; breach notification within 72 hours to the Board; penalties up to ₹250 crore; engineering impacts: PII tagging, masking, deletion workflows, audit logs.'),
])

realworld = '''  <p>Three live scenarios: the course map in four questions, an estimation question solved for full marks, and an advanced case answered with every module. Then exam question banks with model answers.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Exam question bank</h3>
  <p>Answer each aloud or on paper before opening the model answer. Long answers should follow the five-part pattern: definition, diagram, explanation, example, limitations.</p>
''' + two_mark + five_mark + '''
  <h4>10-mark questions to practise</h4>
  <ul>
    <li>Design a data pipeline for a food-delivery company’s daily revenue dashboard (use your capstone).</li>
    <li>Explain how a platform like IRCTC handles the Tatkal spike, with calculations (Lesson 4.7).</li>
    <li>Describe the Hadoop ecosystem and compare it with Spark and the modern lakehouse.</li>
    <li>Explain partitioning, replication and consistency in distributed databases with diagrams.</li>
    <li>Explain data quality, governance and security for a big data platform, including the DPDP Act.</li>
  </ul>'''

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'One last session', story)
        + part(2, 'definition', 'Definition', 'Big Data Fundamentals in one page', definition)
        + part(3, 'types', 'Types and ways to use it', 'Cheat sheet: numbers and comparisons', types)
        + part(4, 'steps', 'Step by step', 'A revision plan that works', steps)
        + part(5, 'animation', 'See it happen', 'A 5-mark answer: what Riya writes, and how it is marked', '  <p>Step through the six frames. Left: Riya’s answer sheet. Right: the examiner’s marking scheme.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios and exam question banks', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Exam strategy', 'Fresher', 'Ten minutes left, two questions to go',
            'In the exam you have 10 minutes left and one 5-mark and one 10-mark question unanswered.',
            'can you maximise marks under time pressure?',
            '<p>Attempt both in outline form: for each, a one-line definition, a quick labelled diagram and 3–4 bullet points with an example. Partial structured answers earn marks; a blank page earns none. Spend roughly 4 minutes on the 5-mark and 6 on the 10-mark question.</p>',
            'perfecting one answer and leaving the other blank.')
        + scn('Concept check', 'Fresher', '“Is Hadoop dead?”',
              'A viva examiner or interviewer asks whether Hadoop is still relevant.',
              'can you give a nuanced, current answer?',
              '<p>Hadoop MapReduce is rarely chosen for new projects; Spark and cloud services have replaced it. But Hadoop’s ideas live on everywhere: distributed storage with replication (HDFS → object storage), resource management (YARN → Kubernetes and cloud schedulers), Hive’s metastore and table concepts (→ catalogs and lakehouse formats). Many enterprises still run Hadoop clusters and are migrating them to cloud lakehouses.</p>',
              'a simple yes or no.')
        + scn('Integration', '1–3 years', '“Which single idea from this course matters most?”',
              'A reflective viva or interview question.',
              'can you connect concepts?',
              '<p>A strong answer picks one idea and links it across the course, for example <b>partitioning</b>: it decides how data is spread across machines (Module 3), how Parquet folders are laid out and queries prune data (Modules 2 and 4), how Kafka scales and orders events (Module 4), how cloud scan costs fall (Module 4.6), how pipelines stay idempotent by overwriting a partition (capstone), and where skew comes from (interviews).</p>',
              'listing tools without connecting them.')
        + scn('Next steps', 'Fresher', '“I finished the course. What now?”',
              'You have completed Big Data Fundamentals.',
              'do you have a plan to keep growing?',
              '<p>Publish your capstone on GitHub with a README; extend it with PySpark, Delta Lake and Airflow; pick one cloud and build the same pipeline there; follow the roadmap from Lesson 6.2; practise SQL daily and use Lesson 6.3 for interviews. Then go deeper in the next courses of the Big Data Engineering track.</p>',
              'stopping at the certificate of completion.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
