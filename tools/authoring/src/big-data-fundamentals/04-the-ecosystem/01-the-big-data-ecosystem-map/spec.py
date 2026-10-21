import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='01-the-big-data-ecosystem-map', n='4.1',
    module_label='Module 4 · The Ecosystem',
    title='The big data ecosystem map: every tool in its place',
    desc='Make sense of Hadoop, Spark, Kafka, Hive, Airflow and 40 more tools by sorting them into six layers: ingest, store, process, query, visualise and orchestrate. Real-time scenarios (lunch rush, a 2 am failure, moving to the cloud), Beginner to Advanced explanations, Python simulations, quiz and interview scenarios.',
    og_desc='Forty tool names, six jobs. Follow one food order through a real data platform and learn where every big data tool fits.',
    minutes=25, level='Beginner → Advanced',
    lead='Kafka, Spark, Hive, Airflow, Iceberg, BigQuery… the big data world seems to have a new tool every week. This lesson gives you one map that never changes: six jobs that every data platform does. Follow a single food order through all six, watch the platform live at lunch rush and at 2 am, and learn the open-source and cloud names for each job.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios'],
)

RUN = dict(
    heading='Build a tiny data platform in Python',
    intro='<p>Each function below plays the role of one layer. <code>ingest</code> accepts every event like Kafka, <code>store</code> keeps raw copies like a data lake, <code>process</code> cleans like Spark, <code>serve</code> answers a question like a SQL engine, and the last three lines are the orchestrator. Notice how the corrupted event and the wrong data type are handled in <b>process</b>, never by changing the raw copy.</p>',
    code='''import json

raw_events = [
    '{"order": 1, "city": "Pune", "item": "thali", "amount": 120}',
    '{"order": 2, "city": "Mumbai", "item": "biryani", "amount": 250}',
    '{"order": 3, "city": "Pune", "item": "thali", "amount": 120}',
    '{"order": 4, "city": "Pune", "item": "dosa", "amount": "90"}',
    'CORRUPTED###',
]

def ingest(events):                 # like Kafka: accept everything, in order
    print("INGEST :", len(events), "events received")
    return list(events)

def store(events, lake):            # like a data lake: keep the raw copy
    lake["raw/orders"] = events
    print("STORE  :", len(events), "raw events saved")

def process(lake):                  # like Spark: parse, clean, fix types
    clean = []
    for e in lake["raw/orders"]:
        try:
            r = json.loads(e)
        except json.JSONDecodeError:
            continue                # skip broken events (real systems log them)
        r["amount"] = int(r["amount"])
        clean.append(r)
    lake["clean/orders"] = clean
    print("PROCESS:", len(clean), "clean rows")

def serve(lake):                    # like Hive / a warehouse: answer a question
    by_city = {}
    for r in lake["clean/orders"]:
        by_city[r["city"]] = by_city.get(r["city"], 0) + r["amount"]
    print("SERVE  : revenue by city ->", by_city)

# ORCHESTRATE: like Airflow, run each layer in the right order
lake = {}
store(ingest(raw_events), lake)
process(lake)
serve(lake)
''',
    anno=[
        ('lake["raw/orders"] = events', 'The raw copy is saved <b>before</b> cleaning. If the cleaning code has a bug, you fix it and reprocess from raw. That is why lakes keep raw data.'),
        ('except json.JSONDecodeError:', 'One broken event must not stop the platform. The processing layer skips it; real pipelines also write it to an error table for checking.'),
        ('r["amount"] = int(r["amount"])', 'Order 4 sent the amount as text <code>"90"</code>. Fixing types is a typical processing job.'),
        ('store(ingest(raw_events), lake)', 'The last three lines are the <b>orchestrator</b>: they decide the order. Swap <code>process</code> and <code>serve</code> and see what breaks.'),
    ],
    tasks=[
        dict(label='1 · Mini platform', hint='Press <b>Run</b>. Then add a Nashik order and a second corrupted event. Which layer\'s count changes for each?', code=None),
        dict(label='2 · Which layer?', hint='A lookup table from tool to layer. Add <code>"Iceberg"</code>, <code>"Pub/Sub"</code> and <code>"Superset"</code> with the right layers.',
             code='''layer_of = {
    "Kafka": "Ingest", "NiFi": "Ingest", "Kinesis": "Ingest",
    "HDFS": "Store", "S3": "Store", "Cassandra": "Store",
    "Spark": "Process", "Flink": "Process",
    "Hive": "Query", "Trino": "Query", "BigQuery": "Query",
    "Power BI": "Visualise", "Tableau": "Visualise",
    "Airflow": "Orchestrate",
}
for tool in ["Spark", "Kinesis", "BigQuery", "Airflow", "HBase"]:
    print(f"{tool:10} ->", layer_of.get(tool, "?? look it up and add it"))
'''),
        dict(label='3 · DAG order', hint='Airflow runs tasks in <b>dependency order</b>. Python\'s built-in <code>graphlib</code> does the same sorting. Add a task <code>"email_report"</code> that needs <code>"refresh_bi"</code>. Then try making <code>"check_raw"</code> depend on <code>"refresh_bi"</code>: a cycle, which a DAG never allows.',
             code='''from graphlib import TopologicalSorter

needs = {                                  # task: tasks that must finish first
    "spark_job":  {"check_raw"},
    "row_checks": {"spark_job"},
    "load_dw":    {"row_checks"},
    "refresh_bi": {"load_dw"},
    "check_raw":  set(),
}
order = list(TopologicalSorter(needs).static_order())
for step, task in enumerate(order, 1):
    print(step, task)
'''),
        dict(label='4 · Pick a tool', hint='A tiny “architect” function. Add a rule: if the need mentions <code>"schedule"</code>, return Airflow. Try your own questions.',
             code='''def pick(need):
    need = need.lower()
    if "real time" in need or "live" in need:
        return "Stream: Kafka + Flink / Spark Streaming"
    if "sql" in need:
        return "Query: Trino / Hive / a warehouse"
    if "cheap" in need or "raw" in need:
        return "Store: S3 / HDFS (data lake)"
    if "join" in need or "clean" in need:
        return "Process (batch): Spark"
    return "Not sure: which of the six jobs is this?"

for q in ["Live order count per kitchen", "Analysts want SQL on clicks",
          "Keep 5 years of raw logs cheaply", "Clean and join orders nightly"]:
    print(f"{q:36} -> {pick(q)}")
'''),
        dict(label='5 · One layer fails', hint='When a task fails, an orchestrator marks everything downstream as <code>upstream_failed</code> instead of running it on bad data. Change <code>failing</code> to <code>"load_dw"</code>.',
             code='''tasks = ["check_raw", "spark_job", "row_checks", "load_dw", "refresh_bi"]
failing = "spark_job"

status, broken = {}, False
for t in tasks:
    if broken:
        status[t] = "upstream_failed"
    elif t == failing:
        status[t] = "FAILED"
        broken = True
    else:
        status[t] = "success"
for t, s in status.items():
    print(f"{t:11} {s}")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='One pipeline, one line at a time',
    intro='<p>A smaller pipeline: three raw events, a <code>process</code> layer and a <code>serve</code> layer. Watch the <code>lake</code> dictionary gain a <code>"clean"</code> copy while <code>"raw"</code> stays untouched, and watch each layer get its own frame on the stack.</p>',
    code='''events = ["Pune,120", "Mumbai,250", "Pune,90"]

def process(raw):
    rows = []
    for e in raw:
        city, amt = e.split(",")
        rows.append((city, int(amt)))
    return rows

def serve(rows):
    total = {}
    for city, amt in rows:
        total[city] = total.get(city, 0) + amt
    return total

lake = {"raw": events}
lake["clean"] = process(lake["raw"])
print(serve(lake["clean"]))
''',
    notes={1: 'Ingest :: Three events arrive as plain text.',
           15: 'Store :: The lake keeps the raw list under the key <code>"raw"</code>.',
           16: 'Process :: The processing layer reads raw and returns clean tuples.',
           17: 'Serve :: The serving layer answers “revenue by city”.'},
)

WORKED_INTRO = 'Four problems, from first-week intern to platform architect. Each runs live and is traced line by line.'
EXAMPLES = [
    dict(level='b', tag='First week · reading a diagram', title='Sort a stack into layers, and spot the gap',
         problem='<p>Your team\'s platform uses Spark, Kafka, Power BI, S3, Airflow and Hive. Print the tools under each of the six layers, and flag any layer with no tool.</p>',
         inp='stack: Spark, Kafka, Power BI, S3, Airflow, Hive',
         approach=['Keep a lookup table from tool to layer.',
                   'Group the stack into a dictionary of lists with <code>setdefault</code>.',
                   'Print the six layers in order, showing “(missing!)” where a list is empty.'],
         code='''layer_of = {"Kafka": "Ingest", "S3": "Store", "Spark": "Process",
            "Hive": "Query", "Power BI": "Visualise", "Airflow": "Orchestrate"}
stack = ["Spark", "Kafka", "Power BI", "S3", "Airflow", "Hive"]

by_layer = {}
for tool in stack:
    by_layer.setdefault(layer_of[tool], []).append(tool)
for layer in ["Ingest", "Store", "Process", "Query", "Visualise", "Orchestrate"]:
    print(f"{layer:12}", by_layer.get(layer, ["(missing!)"]))
''', notes={5: 'Group :: <code>setdefault</code> creates an empty list the first time a layer is seen.'},
         tryit='Remove <code>"Airflow"</code> from the stack and run again. Who would run the jobs at 2 am now?'),
    dict(level='i', tag='Food delivery · latency', title='When does an order appear on each dashboard?',
         problem='<p>An order can reach a dashboard by two paths. The <b>streaming path</b>: app → Kafka (0.2 s) → Flink (0.5 s) → live dashboard (1 s). The <b>batch path</b>: app → Kafka (0.2 s) → hourly dump to S3 (up to 3,600 s) → nightly Spark job (up to 6 hours) → report (10 minutes). Print the worst-case delay for each.</p>',
         inp='two lists of (stage, seconds)',
         approach=['Write a function that adds up the seconds in a path.',
                   'Call it for both paths.',
                   'Show the result in readable units: seconds and hours.'],
         code='''def delay(path):
    total = 0
    for stage, secs in path:
        total = total + secs
    return total

stream = [("app->Kafka", 0.2), ("Kafka->Flink", 0.5), ("Flink->live", 1.0)]
batch = [("app->Kafka", 0.2), ("Kafka->S3", 3600), ("Spark nightly", 21600), ("report", 600)]
print("Streaming path:", delay(stream), "seconds")
print("Batch path    :", round(delay(batch) / 3600, 1), "hours")
''', notes={7: 'Paths :: Same event, two routes through the ecosystem.'},
         tryit='Change the S3 dump from hourly to every 5 minutes (300 s). Does the batch path become “real time”? Lesson 4.2 explains why not.'),
    dict(level='i', tag='Platform team · orchestration', title='Work out the run order of a DAG by hand',
         problem='<p>Four tasks: <code>ingest</code> needs nothing, <code>clean</code> needs ingest, <code>features</code> needs clean, <code>report</code> needs clean. Find an order that respects every dependency, the way an orchestrator does.</p>',
         inp='needs: clean←ingest, features←clean, report←clean',
         approach=['Repeatedly pick tasks whose requirements are all done.',
                   'Mark them done and add them to the order.',
                   'Stop when every task is done.'],
         code='''needs = {"ingest": [], "clean": ["ingest"],
         "features": ["clean"], "report": ["clean"]}
done, order = set(), []
while len(done) < len(needs):
    for task, reqs in needs.items():
        if task not in done and all(r in done for r in reqs):
            done.add(task)
            order.append(task)
print(order)
''', notes={4: 'Loop :: Keep going until every task has run.'},
         tryit='<code>features</code> and <code>report</code> both only need <code>clean</code>, so an orchestrator can run them <b>at the same time</b>. Add a task <code>email</code> that needs both.'),
    dict(level='a', tag='Cloud migration · architecture', title='Translate an open-source stack to a cloud',
         problem='<p>TiffinGo will move to one cloud. Given the open-source tool for each layer, print the typical managed service on AWS, Azure or Google Cloud.</p>',
         inp='stack per layer + chosen cloud',
         approach=['Store one mapping per cloud: layer → service.',
                   'Keep the current stack as layer → open-source tool.',
                   'Print “open-source → managed” for each layer of the chosen cloud.'],
         code='''current = {"Ingest": "Kafka", "Store": "HDFS", "Process": "Spark",
           "Query": "Hive", "Orchestrate": "Airflow"}
clouds = {
    "aws":   {"Ingest": "Kinesis", "Store": "S3", "Process": "EMR",
              "Query": "Athena", "Orchestrate": "MWAA"},
    "gcp":   {"Ingest": "Pub/Sub", "Store": "Cloud Storage", "Process": "Dataproc",
              "Query": "BigQuery", "Orchestrate": "Cloud Composer"},
}
target = "gcp"
for layer, tool in current.items():
    print(f"{layer:11} {tool:8} -> {clouds[target][layer]}")
''', notes={9: 'Choose :: Only this line changes for a different cloud.'},
         tryit='Add an <code>"azure"</code> entry (Event Hubs, ADLS, Databricks, Synapse, Data Factory) and set <code>target = "azure"</code>.'),
]

QUIZ = [
    dict(q='Beginner: Which layer does Apache Kafka mainly belong to?', options=['Store', 'Ingest (moving events)', 'Visualise', 'Orchestrate'], answer=1,
         why='Kafka is a distributed event log used to <b>ingest</b> and move streams of events between systems.'),
    dict(q='Beginner: Which tool schedules a nightly pipeline and retries failed steps?', options=['Kafka', 'HDFS', 'Airflow', 'Tableau'], answer=2,
         why='<b>Airflow</b> is an orchestrator: it runs DAGs of tasks on a schedule, in dependency order, with retries.'),
    dict(q='Beginner: Where would you keep five years of raw app logs most cheaply?', options=['A data lake on HDFS or object storage', 'Power BI', 'The application database', 'Airflow'], answer=0,
         why='Data lakes on HDFS or object storage (S3, ADLS, GCS) are built for cheap, huge, raw storage.'),
    dict(q='Intermediate: An analyst wants to run SQL directly on Parquet files in the lake. Which tool fits?', options=['Kafka', 'Trino (Presto) or Hive', 'Airflow', 'NiFi'], answer=1,
         why='Query engines like <b>Trino/Presto</b> and <b>Hive</b> run SQL over files stored in the lake.'),
    dict(q='Intermediate: Why does the lake keep the raw copy even after cleaning?', options=['Raw data is faster to query', 'So data can be reprocessed if the cleaning logic was wrong', 'Laws forbid deleting anything', 'Cleaning needs the raw copy to run at all'], answer=1,
         why='Raw data is the source of truth. If a bug is found in processing, you fix the code and reprocess from raw.'),
    dict(q='Intermediate: What is a DAG in Airflow?', options=['A database table', 'A set of tasks with dependencies and no cycles', 'A Kafka topic', 'A type of chart'], answer=1,
         why='A <b>Directed Acyclic Graph</b>: tasks with arrows showing order, and no loops.'),
    dict(q='Advanced: What does “separating storage and compute” mean in modern platforms?', options=['Storing data on paper', 'Data lives in object storage while processing engines start and scale independently', 'Each machine stores data it never processes', 'Running Spark without any storage'], answer=1,
         why='Object storage holds data; Spark, Trino or a warehouse spin up compute only when needed, and each scales on its own.'),
    dict(q='Advanced: Which of these adds database-like transactions and time travel to files in a data lake?', options=['Apache Iceberg / Delta Lake', 'Apache Sqoop', 'Power BI', 'Apache Flume'], answer=0,
         why='Open table formats like <b>Iceberg, Delta Lake and Hudi</b> bring ACID transactions, schema changes and time travel to lakes: the lakehouse.'),
]

REVISION = [
    'Six jobs: <b>Ingest → Store → Process → Query → Visualise</b>, with <b>Orchestrate &amp; govern</b> across all of them.',
    'Ingest: Kafka, NiFi, CDC · Store: HDFS, S3/ADLS/GCS, HBase, Cassandra · Process: Spark, Flink.',
    'Query: Hive, Trino, Spark SQL, Snowflake, BigQuery · Visualise: Power BI, Tableau · Orchestrate: Airflow.',
    '<b>Kafka moves data; Airflow schedules jobs.</b> Don\'t mix them up.',
    'Keep the <b>raw copy</b>; clean in the processing layer; reprocess from raw when logic changes.',
    'Cloud names differ, layers don\'t: Kinesis/Event Hubs/Pub/Sub are all “ingest”.',
    'Advanced: storage–compute separation, open table formats (lakehouse), Kubernetes, governance and lineage.',
]
FAQ = [
    ('Explain the Hadoop / big data ecosystem.', 'A big data platform is built in layers. Ingestion tools (Kafka, Flume, Sqoop, NiFi) bring data in; storage (HDFS, HBase, cloud object storage) keeps it; processing engines (MapReduce, Spark, Flink) transform it in batch or streaming mode; query tools (Hive, Pig historically, Trino) give SQL access; visualisation tools present it; and coordination and scheduling (YARN, ZooKeeper, Oozie/Airflow) manage resources and workflows. Each tool specialises in one layer and they are combined into pipelines.'),
    ('What is the difference between Kafka and Airflow?', 'Kafka is a distributed, durable event log: it moves streams of events continuously from producers to consumers. Airflow is a workflow orchestrator: it schedules and monitors batch tasks (like a Spark job) in dependency order. Kafka carries data; Airflow carries none, it only tells other tools when to run.'),
    ('What is a data pipeline?', 'A sequence of steps that moves data from sources to a useful destination: extract or ingest, store, transform (clean, join, aggregate) and load into a place where it is queried or served. Pipelines can be batch (scheduled) or streaming (continuous).'),
    ('Why do companies use managed cloud services instead of running Hadoop themselves?', 'Managed services remove the work of installing, patching, scaling and monitoring clusters, let compute scale up and down with demand, and separate storage from compute. The trade-offs are cost at large steady scale, less control, and some dependence on one provider.'),
    ('What is the role of orchestration and governance in the ecosystem?', 'Orchestration schedules pipelines, runs tasks in the right order, retries failures and alerts people. Governance makes data trustworthy and safe: catalogues of what data exists, lineage of where it came from, access control, and data-quality checks.'),
]

PRACTICE_INTRO = 'From reading a platform diagram to reasoning like an architect. Problems are marked Easy, Medium, Advanced and Business.'
PROBLEMS = [
    dict(level='easy', title='Count tools per layer', stmt='Count how many tools in the list belong to each layer.', inp='Kafka:Ingest, NiFi:Ingest, S3:Store, Spark:Process, Flink:Process, Hive:Query',
         code='''tools = [("Kafka", "Ingest"), ("NiFi", "Ingest"), ("S3", "Store"),
         ("Spark", "Process"), ("Flink", "Process"), ("Hive", "Query")]
count = {}
for name, layer in tools:
    count[layer] = count.get(layer, 0) + 1
print(count)
''', explain='A dictionary counter: the most-used pattern in data engineering code.'),
    dict(level='easy', title='Total pipeline delay', stmt='Stages take 2, 45, 300 and 30 seconds. Print the total delay in minutes.', inp='[2, 45, 300, 30]',
         code='print(round(sum([2, 45, 300, 30]) / 60, 1), "minutes")\n', explain='377 seconds ≈ 6.3 minutes from source to dashboard.'),
    dict(level='easy', title='Which layers are missing?', stmt='A startup has tools for Ingest, Store and Visualise only. Print the missing layers.', inp='have: Ingest, Store, Visualise',
         code='''all_layers = {"Ingest", "Store", "Process", "Query", "Visualise", "Orchestrate"}
have = {"Ingest", "Store", "Visualise"}
print(sorted(all_layers - have))
''', explain='Set difference gives what is in the first set but not the second.'),
    dict(level='medium', title='Find the bottleneck stage', stmt='Given stage durations, print the slowest stage and its share of the total time.', inp='ingest 5, store 20, spark 900, load 60, refresh 15 (seconds)',
         code='''stages = {"ingest": 5, "store": 20, "spark": 900, "load": 60, "refresh": 15}
slowest = max(stages, key=stages.get)
share = stages[slowest] / sum(stages.values()) * 100
print(slowest, "takes", round(share), "% of the time")
''', explain='Speed up the bottleneck first; improving a 5-second stage changes almost nothing.'),
    dict(level='medium', title='Raw vs Parquet size', stmt='The lake receives 500 GB of raw JSON a day. Converted to compressed Parquet it is about one fifth of the size. Print the yearly size of each in TB.', inp='500 GB/day, ratio 1/5',
         code='''raw_tb = 500 * 365 / 1024
print("Raw JSON    :", round(raw_tb, 1), "TB per year")
print("Parquet     :", round(raw_tb / 5, 1), "TB per year")
''', explain='Columnar, compressed formats are why the processing layer rewrites raw data. More in Lesson 4.3.'),
    dict(level='advanced', title='What must be skipped after a failure?', stmt='Given which tasks depend on which, print every task that cannot run because <code>clean</code> failed (all tasks downstream of it).', inp='clean→features, clean→report, features→model, report→email',
         code='''downstream = {"clean": ["features", "report"], "features": ["model"],
              "report": ["email"], "model": [], "email": []}
to_skip, queue = [], ["clean"]
while queue:
    task = queue.pop(0)
    for nxt in downstream[task]:
        if nxt not in to_skip:
            to_skip.append(nxt)
            queue.append(nxt)
print("Skipped:", to_skip)
''', explain='A breadth-first walk over the DAG: exactly how an orchestrator marks tasks as upstream_failed.'),
    dict(level='advanced', title='Hot and cold storage tiers', stmt='Data is kept 30 days in fast “hot” storage (Rs 2 per GB-month) and then moved to “cold” archive (Rs 0.3 per GB-month) for 1 year. With 100 GB arriving per day, print the monthly cost once the system is full (illustrative prices).', inp='100 GB/day, hot 30 days, cold 365 days',
         code='''hot_gb = 100 * 30
cold_gb = 100 * 365
cost = hot_gb * 2 + cold_gb * 0.3
print("Hot :", hot_gb, "GB")
print("Cold:", cold_gb, "GB")
print("Monthly cost: Rs", round(cost))
''', explain='Most data is cold. Tiering is a standard storage-layer design decision.'),
    dict(level='business', title='Is the dashboard fresh?', stmt='Each dashboard must be updated within its freshness limit (hours). Print which ones are stale.', inp='sales: 5h old, limit 24 · fraud: 2h old, limit 1 · stock: 30h old, limit 24',
         code='''dashboards = {"sales": (5, 24), "fraud": (2, 1), "stock": (30, 24)}
for name, (age, limit) in dashboards.items():
    print(f"{name:6}", "OK" if age <= limit else "STALE")
''', explain='Freshness checks are a governance task: someone must notice before the business does.'),
    dict(level='business', title='Managed or self-hosted?', stmt='Self-hosting needs 2 engineers at Rs 1.5 lakh/month each plus Rs 1 lakh of servers. A managed service costs Rs 3.2 lakh/month and needs 0.5 engineer. Print both monthly costs (illustrative).', inp='as given',
         code='''self_hosted = 2 * 1.5 + 1.0
managed = 3.2 + 0.5 * 1.5
print("Self-hosted: Rs", self_hosted, "lakh")
print("Managed    : Rs", managed, "lakh")
''', explain='People cost often outweighs machine cost. That is why many teams choose managed services despite higher unit prices.'),
]

SCN_INTRO = 'Questions that test whether you understand the ecosystem, not just its names. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
