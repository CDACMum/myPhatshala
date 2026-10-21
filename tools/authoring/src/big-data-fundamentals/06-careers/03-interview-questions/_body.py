import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
rounds = [('Online test', 'SQL + Python', '60 min', 'blue'), ('Technical 1', 'SQL, Python, Spark', '60 min', 'acc'), ('Technical 2', 'Pipeline design', '60 min', 'violet'),
          ('Manager', 'Project deep-dive', '45 min', 'green'), ('HR', 'Fit and offer', '30 min', 'card')]
sc = ''
for k, (a, b, c, tone) in enumerate(rounds):
    x = 14 + k * 124
    sc += box(x, 30, 112, 92, tone) + t(x + 56, 54, a, 9.6, bold=True) + t(x + 56, 78, b, 8.4, 'ink2') + t(x + 56, 104, c, 8.4, 'ink2')
    if k < 4:
        sc += arrow(x + 113, 76, x + 123, 76, 'ink3', 1.6)
sc += t(320, 18, 'TiffinGo · Data Engineer interview loop', 9.6, 'acc', bold=True)
scene_svg = scene('A typical data engineering interview loop: an online test, two technical rounds on SQL, Spark and pipeline design, a manager round and an HR round.', sc,
                  'Each round tests something different: <tspan font-weight="700" class="s-acc">prepare for all five</tspan>.')

story = f'''  <div class="story">
    <p class="narration">TiffinGo has opened the full-time data engineer role, and Kabir is one of 14 candidates shortlisted. The recruiter emails the loop: an online test, two technical rounds, a manager round and HR, spread over two weeks. Kabir knows the company’s pipelines better than any outsider, but he has never sat a real interview.</p>

{scene_svg}

K> Sir, I’ve worked on these pipelines for months. Why am I nervous about the questions?
A> Because doing and explaining are different skills, Kabir. Interviews test whether you can <b>reason out loud</b>: clarify the question, state assumptions, solve step by step, and discuss trade-offs.
R> Are the questions very different at each company?
A> The wording changes, Riya, but the core is stable: SQL with joins and window functions, Python basics, big data concepts, Spark internals, Kafka, data modelling, pipeline design and your own project. This lesson collects the most common ones with model answers.
K> Should I memorise the answers?
A> Understand them. Interviewers ask follow-ups: “why?”, “what if the data is ten times bigger?”, “what breaks first?” Today you’ll practise SQL questions on real data, watch how an interviewer scores an answer, handle a “why is this Spark job slow?” question and design a pipeline in 45 minutes.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Interview preparation at three levels
L1> Fresher: the must-knows
      <ul>
      <li><b>SQL:</b> joins (inner, left, full, self), GROUP BY with HAVING, subqueries, window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running totals), deduplication.</li>
      <li><b>Python:</b> lists, dicts, sets, string handling, file reading, functions, exceptions, comprehensions, simple algorithms (counting, grouping, sorting).</li>
      <li><b>Concepts:</b> 5 Vs, batch vs streaming, OLTP vs OLAP, ETL vs ELT, data lake vs warehouse vs lakehouse, row vs columnar formats.</li>
      <li><b>Your project:</b> explain it in 2 minutes with architecture, scale, one hard problem and results.</li>
      </ul>
L2> 1–3 years: depth and trade-offs
      <ul>
      <li><b>Spark:</b> driver and executors, lazy evaluation, transformations vs actions, narrow vs wide, shuffles, partitions, broadcast joins, skew, caching, AQE.</li>
      <li><b>Kafka and streaming:</b> topics, partitions, offsets, consumer groups, delivery semantics, watermarks and late data.</li>
      <li><b>Modelling and warehousing:</b> star vs snowflake schema, facts and dimensions, slowly changing dimensions (SCD type 1 and 2), partitioning and clustering.</li>
      <li><b>Pipelines:</b> Airflow DAGs, idempotency, backfills, incremental loads, data quality checks, CDC.</li>
      </ul>
L3> Senior: design and ownership
      <ul>
      <li><b>System design:</b> requirements, estimates, architecture, storage and processing choices, failure handling, cost and governance, in a structured 45 minutes.</li>
      <li><b>Distributed systems:</b> CAP, consistency, replication, exactly-once end to end, schema evolution, small-files problems.</li>
      <li><b>Operations:</b> SLAs, observability, on-call, incident post-mortems, cost optimisation.</li>
      <li><b>Leadership:</b> design reviews, mentoring, disagreeing constructively, data contracts across teams.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>technical interview</b> for data engineering evaluates a candidate’s ability to <b>query and transform data (SQL)</b>, <b>write correct code (usually Python)</b>, explain <b>distributed data processing and storage concepts</b>, <b>design reliable pipelines and platforms</b> under constraints, and communicate decisions. A typical process includes an online assessment, one or more technical rounds, a design round, a project or managerial discussion and a behavioural/HR round, each assessed against a rubric of correctness, depth, trade-off reasoning and communication.',
    'Interviews check whether you can write SQL and Python correctly, explain how big data tools work and why, design a pipeline that won’t break, and talk clearly about your own work. Each round looks at one of these.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Online assessment', 'A timed test (SQL, Python, multiple choice) used to shortlist candidates.'),
    ('Live coding', 'Solving a problem while sharing your screen and explaining your thinking.'),
    ('Design round', 'Designing a pipeline or data platform for a scenario, discussing trade-offs.'),
    ('Rubric', 'The criteria an interviewer scores: correctness, depth, communication, trade-offs.'),
    ('Follow-up', 'A deeper question building on your answer: “what if the data were 10× bigger?”'),
    ('Clarifying question', 'A question you ask before solving, to confirm requirements and edge cases.'),
    ('STAR', 'Situation, Task, Action, Result: structure for behavioural answers.'),
    ('Bar raiser', 'An interviewer from another team whose job is to keep the hiring standard high.'),
]) + lv + '''
EXAM> For any interview question: <b>clarify</b> (inputs, scale, edge cases), <b>state assumptions</b>, answer <b>step by step</b>, give a <b>small example</b>, then add <b>trade-offs or limits</b>. This structure also earns full marks in long-answer exam questions.'''

# ---------------------------------------------------------------- types
types = table(['Round', 'What is tested', 'How to prepare'], [
    ['<b>Online assessment</b>', 'SQL queries, Python problems, MCQs on concepts', 'Daily SQL practice; timed Python problems on lists, dicts, strings'],
    ['<b>Technical: SQL and coding</b>', 'Joins, window functions, deduplication; Python data handling', 'Solve aloud; test with edge cases (NULLs, ties, empty input)'],
    ['<b>Technical: big data concepts</b>', 'Spark internals, Kafka, file formats, partitioning, warehouses', 'Explain each concept with a picture and an example from your project'],
    ['<b>Design round</b>', 'An end-to-end pipeline or platform for a scenario', 'Practise a fixed structure: requirements → estimates → design → failures → cost'],
    ['<b>Project / manager round</b>', 'Ownership, depth, decisions, collaboration', 'Prepare a 2-minute project story and 5 STAR stories'],
    ['<b>HR round</b>', 'Motivation, expectations, notice period, culture fit', 'Research the company; be honest and specific'],
], minw=640) + '''

  <h3>What interviewers score</h3>
''' + cards([
    ('Correctness', 'Does the query or code give the right answer, including edge cases such as NULLs, ties and duplicates?', 'Right'),
    ('Depth', 'Can you explain why it works and what happens underneath (shuffles, partitions, offsets)?', 'Why'),
    ('Trade-offs', 'Do you compare options and pick one for stated reasons (cost, latency, simplicity)?', 'Judgement'),
    ('Communication', 'Do you clarify, think aloud, structure the answer and accept hints well?', 'Clarity'),
]) + '''
TIP> When stuck, say what you know and reason towards the rest: “I haven’t used Iceberg, but it is a table format like Delta, so I’d expect snapshots and ACID commits…”. Interviewers reward honest reasoning far more than confident guessing.'''

# ---------------------------------------------------------------- steps
c1 = '''rows = [("Pune", 900), ("Pune", 450), ("Pune", 320), ("Thane", 610)]
best = {}
for city, amt in rows:
    best[city] = max(best.get(city, 0), amt)
print(best)'''
steps = stepper([
    ('Clarify the question',
     '<p>“Top orders per city: should ties share a rank? Should duplicate rows count once? Any date range?”</p>',
     'Two or three clarifying questions show care and often reveal the edge case the interviewer is waiting for.'),
    ('State assumptions and scale',
     '<p>“I’ll assume order_id is unique after deduplication, and the table has around 10 crore rows partitioned by date.”</p>',
     'Assumptions make your answer checkable and set up good follow-ups.'),
    ('Solve simply first',
     code('python', 'max_per_city.py', c1, run_code(c1)),
     'Get a correct, simple solution, then improve it. A working brute-force answer beats an unfinished clever one.'),
    ('Test with edge cases',
     '<p>Walk through NULL amounts, ties, a city with one order and an empty table. Fix anything that breaks.</p>',
     'Interviewers note whether you test without being asked.'),
    ('Discuss scale and trade-offs',
     '<p>“On 10 crore rows I’d filter by date partition first; in Spark, this window needs a shuffle by city, and a hot city could cause skew.”</p>',
     'Connecting a small answer to big data behaviour is what separates data engineers from general developers.'),
    ('Summarise',
     '<p>End with one sentence: what you did, its complexity or cost, and what you’d do with more time.</p>',
     'A clean summary leaves a strong final impression.'),
])

# ---------------------------------------------------------------- two-view animation: one answer, scored
def bubble(lines, tone='blue'):
    return box(20, 20, 320, 120, tone) + ''.join(t(34, 46 + k * 20, s, 9, anchor='start') for k, s in enumerate(lines))
see = [
    bubble(['Interviewer: “What is a shuffle in Spark,', 'and why should we care?”'], 'card'),
    bubble(['Kabir: “Before I answer, may I relate it to a', 'GROUP BY on our orders table?”']),
    bubble(['“A shuffle moves rows between executors so', 'that rows with the same key end up together.', 'GROUP BY city needs all Pune rows in one place.”']),
    bubble(['“It writes to disk and sends data over the', 'network, so it’s often the slowest stage.', 'In our job it was 70% of the runtime.”']),
    bubble(['“To reduce it: filter and select columns early,', 'broadcast small tables in joins, fix skewed keys,', 'and tune spark.sql.shuffle.partitions or use AQE.”']),
    bubble(['“So: necessary for wide operations, expensive,', 'and the first place I look when a job is slow.”'], 'green'),
]
def rubric(scores, note):
    names = ['Correctness', 'Depth', 'Trade-offs', 'Communication']
    o = ''
    for k, (n, s) in enumerate(zip(names, scores)):
        o += t(30, 44 + k * 26, n, 9, anchor='start') + ''.join(fill(150 + i * 34, 33 + k * 26, 28, 14, 'green' if i < s else 'grey', rx=3) for i in range(4))
    return o + t(180, 160, note, 8.6, 'ink2')
behind = [
    rubric([0, 0, 0, 0], 'A core Spark question. Strong answers relate it to real work.'),
    rubric([0, 0, 0, 2], 'Asking to anchor on an example: good communication.'),
    rubric([3, 1, 0, 2], 'Correct definition with a concrete example.'),
    rubric([3, 3, 0, 3], 'Explains why it is costly, with a real number: depth.'),
    rubric([4, 3, 3, 3], 'Several ways to reduce it, each with a reason: trade-offs.'),
    rubric([4, 4, 3, 4], 'Clear summary. Likely a “strong hire” signal for this question.'),
]
see_caps = ['The interviewer asks a classic: what is a shuffle in Spark, and why care?', 'Kabir asks to explain it through a familiar example.', 'He defines a shuffle using GROUP BY city.',
            'He explains the cost, with a real figure from his internship.', 'He lists ways to reduce shuffles.', 'He ends with a one-line summary.']
behind_caps = ['The interviewer has a rubric with four areas, each scored on a scale.',
               'A short clarifying or framing question already shows good communication.',
               'A correct definition with an example earns most of the correctness score.',
               'Explaining that shuffles hit disk and network, and quoting 70% of runtime from real work, shows depth.',
               'Practical remedies (filter early, broadcast joins, skew handling, partition tuning, adaptive query execution) show judgement.',
               'The summary ties it together. Scores are illustrative, but this is how many structured interviews are assessed.']
two = anim_two('How one answer is scored', 'What Kabir says, and what the interviewer notes', 'Kabir answering “What is a shuffle in Spark?” step by step',
               'An interviewer’s rubric filling up for correctness, depth, trade-offs and communication', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: SQL round (real output from sql_interview.out)
def sqlf(query_lines, result_lines, note1, note2, tone):
    o = box(14, 14, 200, 120, 'card') + ''.join(t(22, 32 + k * 14, s, 7.8, 'blue', anchor='start', mono=True) for k, s in enumerate(query_lines))
    o += box(222, 14, 124, 120, 'green') + t(284, 30, 'result', 8.6, 'green', bold=True) + ''.join(t(230, 48 + k * 15, s, 7.8, anchor='start', mono=True) for k, s in enumerate(result_lines))
    return o + cap(note1, note2, tone, y=146, h=44)
fr1 = [
    sqlf(['-- Top 2 orders per city', '-- Clarify: ties? duplicates?'], [], '“Top 2 orders per city.” Kabir first asks:', 'do ties share a rank? Are there duplicate rows?', 'blue'),
    sqlf(['SELECT DISTINCT order_id,', '  city, amount', 'FROM orders'], ['8 rows → 7', 'O2 was loaded twice'], 'Step 1: remove the duplicate O2 row', 'that a retry loaded twice.', 'amber'),
    sqlf(['DENSE_RANK() OVER (', '  PARTITION BY city', '  ORDER BY amount DESC', ') AS rnk'], ['Pune  O6 900 1', 'Pune  O2 450 2', 'Pune  O1 320 3', 'Thane O3 610 1', 'Thane O5 610 1'], 'Step 2: rank within each city.', 'DENSE_RANK gives ties the same rank.', 'acc'),
    sqlf(['SELECT ... FROM (...)', 'WHERE rnk <= 2', 'ORDER BY city, rnk'], ['Nashik O7 200 1', 'Pune   O6 900 1', 'Pune   O2 450 2', 'Thane  O3 610 1', 'Thane  O5 610 1'], 'Step 3: keep ranks 1 and 2. Thane has a tie,', 'so both 610 orders are rank 1.', 'green'),
    sqlf(['-- ROW_NUMBER: exactly 2', '-- RANK: 1,1,3 (gaps)', '-- DENSE_RANK: 1,1,2'], ['know all three', 'and when to use', 'each one'], 'Follow-up: “What if you used ROW_NUMBER?”', 'Each ranking function treats ties differently.', 'blue'),
]
s1 = anim_one('Real-time scenario 1', 'The SQL round: top 2 orders per city',
              'The results come from the program in “Run it on your PC” below, which runs five classic SQL questions on a small orders table. Watch the most common window-function question solved step by step.',
              'SQL interview', 'Solving top-N per group with deduplication and DENSE_RANK, including ties', fr1,
              ['Before writing SQL, Kabir clarifies two edge cases: how ties should be treated and whether duplicates exist.',
               'The table has the order O2 twice (a retry loaded it twice), so he deduplicates with SELECT DISTINCT. 8 rows become 7.',
               'DENSE_RANK() OVER (PARTITION BY city ORDER BY amount DESC) ranks orders within each city, giving equal amounts the same rank.',
               'Filtering rnk ≤ 2 returns the answer. Thane’s two 610 orders are both rank 1, so Thane returns two rows for rank 1.',
               'A common follow-up: ROW_NUMBER returns exactly two rows per city (breaking ties arbitrarily), RANK leaves gaps (1, 1, 3) and DENSE_RANK doesn’t (1, 1, 2). Knowing the difference is a frequent screening point.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: why is this Spark job slow?
def tasks(durs, note1, note2, tone, hot=None):
    o = t(14, 22, 'Stage 4 tasks (seconds), from the Spark UI', 8.8, 'ink2', anchor='start')
    mx = max(durs)
    for k, d in enumerate(durs):
        w = d / mx * 220
        o += t(30, 44 + k * 13, f'task {k + 1}', 7.6, 'ink2', anchor='start') + fill(80, 36 + k * 13, w, 9, 'red' if k == hot else 'acc', rx=2) + t(86 + w, 44 + k * 13, str(d), 7.4, anchor='start')
    return o + cap(note1, note2, tone, y=150, h=44)
fr2 = [
    tasks([40, 42, 38, 41, 39, 43, 40, 2400], '“The nightly job went from 20 min to an hour.', 'Why?” Kabir opens the Spark UI first.', 'blue'),
    tasks([40, 42, 38, 41, 39, 43, 40, 2400], 'One task takes 2,400 s while others take 40 s.', 'Classic sign of data skew.', 'red', hot=7),
    tasks([40, 42, 38, 41, 39, 43, 40, 2400], 'Check key counts: a test merchant ID has', '30% of all rows, all sent to one partition.', 'red', hot=7),
    tasks([60, 62, 58, 61, 59, 63, 60, 64], 'Fixes: filter test data, salt the hot key, or', 'enable AQE skew-join handling.', 'green'),
    tasks([60, 62, 58, 61, 59, 63, 60, 64], 'Stage now ~64 s. Answer structure: symptom →', 'evidence → cause → fix → prevention.', 'green'),
]
s2 = anim_one('Real-time scenario 2', '“Why is this Spark job slow?”',
              'This is one of the most common data engineering interview questions. Strong candidates don’t guess; they describe how they would find evidence. Watch the reasoning.',
              'Spark troubleshooting', 'Diagnosing a slow Spark stage caused by data skew and fixing it', fr2,
              ['Kabir doesn’t start with guesses like “add more memory”. He says he would open the Spark UI and find the slowest stage.',
               'In that stage, seven tasks take about 40 seconds and one takes 2,400 seconds. One straggler task like this is the classic sign of <b>data skew</b>.',
               'He would check row counts per join or group key and find that a single test merchant ID holds 30% of rows, so one partition does almost all the work.',
               'Fixes: filter out test data, salt the hot key (split it across several partitions), broadcast the smaller table, or enable adaptive query execution’s skew-join handling.',
               'The stage drops to about a minute. The structure is what interviewers want: symptom, evidence, cause, fix, and how to prevent it (a skew alert, data quality checks on test IDs). (Numbers are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): 45-minute design round
phases3 = [('0–5 min', 'Requirements', 'blue'), ('5–10', 'Estimates', 'blue'), ('10–25', 'Architecture', 'acc'), ('25–35', 'Failures', 'violet'), ('35–45', 'Cost', 'green')]
def design(n, note1, note2, tone, inner=''):
    o = ''
    for k, (a, b, tn) in enumerate(phases3):
        x = 14 + k * 67
        o += label_box(x, 14, 62, 40, [a, b.split(' ')[0]], tn if k < n else 'card', 7.8)
    return o + inner + cap(note1, note2, tone, y=146, h=44)
arch = (label_box(14, 74, 56, 34, ['App', 'events'], 'blue', 7.8) + arrow(72, 91, 86, 91, 'ink3', 1.4) + label_box(88, 74, 52, 34, ['Kafka'], 'acc', 8)
        + arrow(142, 91, 156, 91, 'ink3', 1.4) + label_box(158, 74, 60, 34, ['Spark', 'streaming'], 'acc', 7.8) + arrow(220, 91, 234, 91, 'ink3', 1.4)
        + label_box(236, 74, 54, 34, ['Delta', 'lake'], 'green', 7.8) + arrow(292, 91, 300, 91, 'ink3', 1.4) + label_box(302, 74, 44, 34, ['BI'], 'violet', 8))
fr3 = [
    design(1, '“Design real-time order analytics for TiffinGo.”', 'Ask: latency? users? history? correctness needs?', 'blue',
           t(180, 84, 'Dashboard within 1 minute · 3 years history', 9, bold=True) + t(180, 104, 'exact daily revenue for finance · 6 cities', 9, 'ink2')),
    design(2, 'Estimate: 50 lakh orders/day ≈ 58/s avg,', '~300/s peak at lunch; ~5 GB/day of events.', 'blue',
           t(180, 90, '50,00,000 ÷ 86,400 ≈ 58 per second', 9.4, bold=True) + t(180, 110, '× 5 lunch peak ≈ 300 per second', 9, 'ink2')),
    design(3, 'Architecture: events → Kafka → Spark streaming', '→ Delta bronze/silver/gold → dashboards.', 'acc', arch),
    design(4, 'Failures: idempotent writes, checkpoints, late', 'events via watermarks, nightly batch reconciliation.', 'violet', arch),
    design(5, 'Cost and governance: partitions, auto-scaling,', 'PII masking, owners, quality checks. Summarise.', 'green', arch),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'A 45-minute pipeline design round',
              'Design rounds reward structure more than buzzwords. Watch how Kabir spends 45 minutes on a real-time order analytics design.',
              'System design', 'A pipeline design interview moving through requirements, estimates, architecture, failure handling and cost', fr3,
              ['He spends the first five minutes on requirements: dashboard latency under a minute, three years of history, exact revenue for finance, six cities.',
               'Back-of-envelope estimates: 50 lakh orders a day is about 58 per second on average and roughly 300 per second at the lunch peak; about 5 GB of events a day. This rules out over-engineered designs.',
               'The architecture: order events into Kafka, Spark Structured Streaming into Delta Lake bronze, silver and gold tables, with BI dashboards on gold. He explains why each piece is there.',
               'The deep dive covers failures: checkpoints and idempotent writes for exactly-once results, watermarks for late events, and a nightly batch job reconciling totals with the orders database for finance.',
               'He finishes with cost (partitioning, autoscaling, retention), governance (PII masking, owners, quality checks) and a one-minute summary, leaving time for the interviewer’s questions.'])

# ---------------------------------------------------------------- question bank
def bank(title, qa):
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>\n    ' for q, a in qa)
    return f'\n  <h4>{title}</h4>\n  <div class="faq">\n    {items}</div>\n'

qb = bank('SQL', [
    ('Difference between WHERE and HAVING?', 'WHERE filters rows before grouping; HAVING filters groups after aggregation, so it can use aggregates like COUNT(*) > 1.'),
    ('ROW_NUMBER vs RANK vs DENSE_RANK?', 'For ties on 610, 610, 450: ROW_NUMBER gives 1, 2, 3 (arbitrary order for ties); RANK gives 1, 1, 3 (gaps); DENSE_RANK gives 1, 1, 2 (no gaps).'),
    ('How do you remove duplicate rows but keep one?', 'Use ROW_NUMBER() OVER (PARTITION BY the key columns ORDER BY a tiebreaker such as load time DESC) and keep rows where the number is 1; or SELECT DISTINCT when entire rows are identical.'),
    ('INNER vs LEFT vs FULL OUTER JOIN?', 'INNER keeps matching rows only; LEFT keeps all rows from the left table with NULLs where there is no match; FULL OUTER keeps all rows from both sides.'),
    ('What happens to NULLs in COUNT, SUM and joins?', 'COUNT(column) and SUM ignore NULLs, COUNT(*) counts rows; NULL never equals NULL, so NULL keys don’t match in joins unless handled explicitly.'),
    ('How would you find the second highest salary?', 'SELECT MAX(salary) FROM t WHERE salary < (SELECT MAX(salary) FROM t), or DENSE_RANK() and filter rank = 2. Ask how ties should be handled.'),
]) + bank('Python', [
    ('List vs tuple vs set vs dict?', 'List: ordered, mutable. Tuple: ordered, immutable (usable as a dict key). Set: unordered unique items with fast membership. Dict: key-value pairs with fast lookup by key.'),
    ('How do you read a 20 GB file that doesn’t fit in memory?', 'Stream it line by line or in chunks (a for loop over the file, pandas read_csv with chunksize, or pyarrow batches), process each chunk and aggregate; or use Spark or DuckDB.'),
    ('What is a generator and why use it in data pipelines?', 'A function that yields values one at a time with yield, keeping memory low because items are produced lazily, ideal for streaming through large files or API pages.'),
    ('How do you handle errors in a pipeline script?', 'Catch specific exceptions, log context (file, row, ID), retry transient errors with backoff, send bad records to a quarantine location and fail loudly on unexpected errors rather than silently continuing.'),
    ('Count word frequency in a text file.', 'Use collections.Counter over words from each line: Counter(w for line in f for w in line.lower().split()).most_common(10).'),
]) + bank('Big data concepts', [
    ('Explain the 5 Vs.', 'Volume (size), Velocity (speed of arrival), Variety (structured, semi-structured, unstructured), Veracity (quality and trust) and Value (business benefit). Give an example for each from a real system.'),
    ('ETL vs ELT?', 'ETL transforms data before loading into the target; ELT loads raw data first and transforms inside a scalable warehouse or lakehouse, which is common in the cloud because storage is cheap and engines are powerful.'),
    ('Data lake vs data warehouse vs lakehouse?', 'A lake stores raw files of any type cheaply; a warehouse stores structured, modelled data for fast SQL; a lakehouse adds table formats (Delta, Iceberg, Hudi) to lake storage for ACID transactions, schema enforcement and warehouse-like performance.'),
    ('Why are columnar formats like Parquet faster for analytics?', 'Queries read only the needed columns, similar values compress well, and min/max statistics let engines skip row groups, so far less data is read.'),
    ('What is partitioning and what is the small-files problem?', 'Partitioning splits data by a column (often date) so queries skip irrelevant folders. Too many tiny files, from over-partitioning or frequent small writes, slow down listing and reading; fix with compaction and sensible partition choices.'),
    ('Explain the CAP theorem.', 'During a network partition a distributed system must choose between consistency (every read sees the latest write) and availability (every request gets a response). Payments favour consistency; feeds and counters often favour availability.'),
]) + bank('Spark', [
    ('Driver vs executor?', 'The driver plans the job and schedules tasks; executors on worker nodes run tasks on partitions and hold cached data.'),
    ('Transformations vs actions; what is lazy evaluation?', 'Transformations (select, filter, join) build a plan; actions (count, write, collect) trigger execution. Laziness lets Spark optimise the whole plan, for example pushing filters down.'),
    ('Narrow vs wide transformations?', 'Narrow ones (map, filter) work within a partition; wide ones (groupBy, join, distinct) need a shuffle to bring rows with the same key together.'),
    ('repartition vs coalesce?', 'repartition does a full shuffle to any number of partitions with even sizes; coalesce reduces partitions by merging without a full shuffle, cheaper but possibly uneven.'),
    ('What is a broadcast join?', 'Sending a small table to every executor so the big table can be joined without shuffling it. Useful when one side fits comfortably in memory.'),
    ('How do you handle data skew?', 'Find hot keys in the Spark UI and key counts, then filter bad keys, salt hot keys, broadcast the small side, or enable adaptive query execution’s skew handling.'),
    ('cache vs persist?', 'cache stores a DataFrame in memory (default storage level); persist lets you choose levels such as memory and disk. Use it only when the result is reused several times, and unpersist after.'),
]) + bank('Kafka and streaming', [
    ('Topic, partition, offset, consumer group?', 'A topic is a named stream; partitions split it for parallelism and ordering within a partition; an offset is a message’s position; consumers in a group share partitions, so each message is processed by one consumer in the group.'),
    ('At-most-once, at-least-once, exactly-once?', 'At-most-once may lose messages; at-least-once may duplicate them; exactly-once means each message affects results once, achieved with idempotent producers, transactions or idempotent sinks plus checkpoints.'),
    ('What are watermarks?', 'A threshold for how late event-time data may arrive; events older than the watermark are dropped or handled separately so windowed state can be finalised and freed.'),
    ('How does Kafka keep messages in order?', 'Order is guaranteed only within a partition, so events that must stay ordered (for example, for one order ID) use the same key, which maps to the same partition.'),
    ('Batch or streaming for a daily finance report?', 'Batch: it needs complete, reconciled data once a day. Streaming fits fraud alerts or live dashboards where seconds matter.'),
]) + bank('Data modelling and pipelines', [
    ('Star vs snowflake schema?', 'A star schema has a central fact table joined directly to denormalised dimension tables; a snowflake normalises dimensions into more tables. Star is simpler and faster for BI.'),
    ('What is a slowly changing dimension type 2?', 'A dimension that keeps history by inserting a new row with valid_from/valid_to (or is_current) when an attribute such as a customer’s city changes, instead of overwriting it (type 1).'),
    ('What makes a pipeline idempotent?', 'Running it twice for the same input gives the same result: overwrite a date partition or MERGE on keys instead of blindly appending.'),
    ('Full load vs incremental load vs CDC?', 'Full reloads everything; incremental loads only new or changed rows using a watermark column; CDC reads the database’s change log to capture inserts, updates and deletes reliably.'),
    ('What is a backfill?', 'Re-running a pipeline for past dates, for example after a bug fix or a new column. Airflow supports it when tasks are parameterised by date and idempotent.'),
]) + bank('Behavioural and HR', [
    ('Tell me about a time something broke in production.', 'Use STAR: the situation (dashboard 100× wrong), your task, the actions (traced lineage, found a unit change, fixed and backfilled, added a check and a contract) and the result, plus what you learnt.'),
    ('Tell me about a disagreement with a teammate.', 'Show that you listened, used data or a small experiment to decide, and kept the relationship good. Avoid blaming.'),
    ('Why data engineering?', 'Connect a real experience (building a pipeline others relied on) to what you enjoy: reliable systems, scale and enabling decisions.'),
    ('Where do you see yourself in a few years?', 'Be honest and role-related: deeper expertise in streaming or platforms, owning systems end to end, mentoring others.'),
])

realworld = '''  <p>Three live scenarios: a SQL round with real query output (from the program below), a “why is this Spark job slow?” question, and an advanced 45-minute design round. Then a question bank with model answers.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Question bank with model answers</h3>
  <p>Open each question only after answering it aloud yourself. Model answers are short; in an interview, add an example from your own work.</p>
''' + qb

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Five rounds in two weeks', story)
        + part(2, 'definition', 'Definition', 'The data engineering interview', definition)
        + part(3, 'types', 'Types and ways to use it', 'Interview rounds and what they test', types)
        + part(4, 'steps', 'Step by step', 'How to answer any technical question', steps)
        + part(5, 'animation', 'See it happen', 'One answer: what Kabir says, and how it is scored', '  <p>Step through the six frames. Left: Kabir’s answer. Right: the interviewer’s rubric.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios and a question bank', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('SQL · live coding', 'Fresher', '“Find customers who ordered on consecutive days.”',
            'An interviewer gives an orders table (customer, order_date) and asks for customers with orders on two consecutive days.',
            'can you use window functions beyond ranking?',
            '<p>Deduplicate to one row per customer per day, then use <code>LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date)</code> and keep rows where the difference from the previous date is exactly one day. Mention edge cases: several orders on the same day, time zones, and performance (partition by date range on large tables).</p>',
            'self-joining every row with every other row without explaining the cost.')
        + scn('Spark · concepts', '1–3 years', '“Your Spark job fails with OutOfMemory.”',
              'An executor fails with an out-of-memory error during a join.',
              'can you reason from symptoms to causes?',
              '<ul><li>Check the Spark UI: which stage, how large are partitions, is one task much bigger (skew)?</li><li>Look for <code>collect()</code> or <code>toPandas()</code> pulling data to the driver.</li><li>Fixes: more partitions, broadcast only genuinely small tables, salt skewed keys, select fewer columns, avoid caching large unused data, increase executor memory as a last resort.</li></ul>',
              'immediately doubling memory without finding the cause.')
        + scn('System design', '1–3 years', '“Design a daily sales pipeline from 200 stores.”',
              'Each store uploads a CSV of sales every night. Head office needs a dashboard by 7 am.',
              'can you structure a batch design with failure handling?',
              '<ol><li>Requirements: ~200 files a night, sizes, 7 am SLA, late or missing files.</li><li>Land raw files in object storage by date and store (bronze).</li><li>Airflow DAG: sensor for files with a deadline, validation and quality checks, Spark or dbt into silver and gold, idempotent overwrite per date.</li><li>Alerts for missing stores, quarantine for bad files, backfill support.</li><li>Serve gold tables to the dashboard; document owners and definitions.</li></ol>',
              'jumping to Kafka and streaming for a once-a-day requirement.')
        + scn('Behavioural', 'Fresher', '“What is your biggest weakness?”',
              'Asked in many HR and manager rounds.',
              'can you be honest and show growth?',
              '<p>Pick a real, non-critical weakness and show what you are doing about it: “I used to jump into coding before clarifying requirements. After a pipeline I built had to be redone, I now write a one-page design note and confirm it before starting.” Keep it short and specific.</p>',
              'a disguised strength like “I work too hard”.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
