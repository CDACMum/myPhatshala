import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = box(14, 16, 250, 124, 'red') + t(139, 38, 'Cloud bill · October', 10, 'red', bold=True)
rows = [('Object storage', '₹1.1 L'), ('Serverless SQL scans', '₹43.2 L'), ('Spark cluster', '₹5.8 L'), ('Data transfer out', '₹0.3 L')]
sc += ''.join(t(28, 62 + k * 16, a, 8.8, anchor='start') + t(250, 62 + k * 16, b, 8.8, 'red' if 'SQL' in a else 'ink', anchor='end', bold=True) for k, (a, b) in enumerate(rows))
sc += t(139, 132, 'Total ₹50.5 lakh', 10, 'red', bold=True)
sc += arrow(272, 78, 312, 78, 'ink3', 2) + t(292, 66, 'fix', 8.6, 'ink3')
sc += box(320, 16, 306, 124, 'green') + t(473, 38, 'Same platform, after a week of fixes', 10, 'green', bold=True)
fixes = ['Parquet + date partitions + no SELECT *', 'cluster runs only for the nightly job', 'spot workers, data kept in region']
sc += ''.join(t(334, 64 + k * 18, '✓ ' + f, 8.8, anchor='start') for k, f in enumerate(fixes))
sc += t(473, 132, 'Total ₹2.4 lakh', 10, 'green', bold=True)
scene_svg = scene('A cloud bill of 50.5 lakh rupees, mostly from SQL scans, reduced to 2.4 lakh after partitioning, auto-shutdown, spot workers and keeping data in region.', sc,
                  'The cloud makes big data <tspan font-weight="700" class="s-acc">easy to start and easy to overspend</tspan>.')

story = f'''  <div class="story">
    <p class="narration">TiffinGo has no data centre at all: everything runs on a public cloud. In his second month Kabir builds a small analytics setup in a weekend: files in object storage, a serverless SQL engine on top, and a Spark cluster for the nightly job. The analysts love it. Then the October bill arrives: ₹50 lakh, mostly from one line, “SQL scans”.</p>

{scene_svg}

K> Sir, it took me two days to build what used to take a team months. How did it also cost ₹50 lakh?
A> Because in the cloud you pay for what you <i>use</i>, and serverless SQL charges for every terabyte a query reads. Analysts ran <code>SELECT *</code> on 40 TB of uncompressed CSV, hundreds of times a day. The cluster also ran all night and all day, though the job needs three hours.
R> So the cloud is expensive?
A> No, Riya. The cloud is <i>honest</i>: it bills exactly what you do. With good file layouts, clusters that switch off and cheaper spare capacity, the same platform cost ₹2.4 lakh a month.
K> And all those service names, S3, EMR, Glue, BigQuery, Databricks? It feels like learning three languages.
A> It’s mostly one language with three accents. Every cloud has object storage, managed Spark, a warehouse, a streaming service and an orchestrator. Today you’ll learn the map once, then see a bill shrink, a spot instance disappear mid-job, and why payment data must stay in Indian regions.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Big data on the cloud at three levels
L1> Renting instead of buying
      <ul>
        <li><b>Buying servers</b> is like buying a car: big cost up front, it sits idle most of the day, and you maintain it.</li>
        <li><b>The cloud</b> is like a ride-hailing app: book exactly the size you need, for as long as you need, and pay per use. Need 200 cars for one hour? Possible.</li>
        <li><b>Managed services</b> mean someone else runs the engine: you get storage, Spark, SQL and Kafka-like streaming as ready services, not machines to install.</li>
        <li><b>Regions</b> are the cities where the cloud has data centres. Indian companies usually choose Mumbai, Hyderabad, Pune, Chennai or Delhi regions.</li>
      </ul>
L2> The same building blocks on every cloud
      <ul>
        <li><b>Storage:</b> object storage is the foundation of every cloud lake (S3, ADLS Gen2, Cloud Storage).</li>
        <li><b>Processing:</b> managed Spark (EMR, Databricks, Dataproc), serverless ETL (Glue), or Apache Beam pipelines (Dataflow).</li>
        <li><b>SQL:</b> warehouses (Redshift, Synapse/Fabric, BigQuery, Snowflake) and serverless SQL directly over lake files (Athena, BigQuery external tables).</li>
        <li><b>Streaming:</b> managed event streams (Kinesis, MSK, Event Hubs, Pub/Sub, Confluent Cloud).</li>
        <li><b>Orchestration and governance:</b> managed Airflow (MWAA, Cloud Composer), Data Factory, Step Functions; catalogs (Glue Data Catalog, Unity Catalog, Purview, Dataplex).</li>
        <li><b>Provisioned vs serverless:</b> provisioned means you choose and pay for machines by the hour; serverless means you just submit work and pay per query, job or data processed.</li>
      </ul>
L3> Cost, lock-in, security and data residency
      <ul>
        <li><b>The four meters:</b> storage (per GB-month), compute (per node-hour or per TB scanned), requests (per thousand API calls) and <b>egress</b> (data leaving a region or cloud, often the hidden cost).</li>
        <li><b>FinOps habits:</b> tag every resource with an owner, set budgets and alerts, partition and use columnar formats, auto-terminate idle clusters, autoscale, and use <b>spot / preemptible</b> capacity (much cheaper, but the cloud can take it back at short notice) for fault-tolerant work.</li>
        <li><b>Lock-in:</b> proprietary services are convenient but hard to leave. Open formats (Parquet, Delta Lake, Iceberg) and open engines (Spark, Kafka APIs, Airflow) keep options open.</li>
        <li><b>Shared responsibility:</b> the provider secures the data centres and services; you secure your data: least-privilege IAM roles, encryption, private network endpoints, no public buckets.</li>
        <li><b>Data residency:</b> Indian rules (for example the RBI’s 2018 requirement to store payment-system data in India) and company policies decide which regions data may live in; disaster recovery is often set up across two Indian regions.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Cloud computing</b> provides on-demand access to computing resources (storage, compute, networking and managed software services) over the internet, billed by usage. For big data, public clouds such as <b>Amazon Web Services (AWS)</b>, <b>Microsoft Azure</b> and <b>Google Cloud Platform (GCP)</b> offer managed object storage, distributed processing, data warehouses, streaming and orchestration services that scale elastically. Service models range from <b>IaaS</b> (virtual machines you manage) through <b>PaaS / managed services</b> to <b>serverless</b> offerings billed per query or job, with storage and compute typically <b>separated</b>.',
    'Instead of buying and running your own servers, you rent storage and processing from a cloud company and pay only for what you use. Each cloud offers ready-made services for storing lake data, running Spark, querying with SQL and handling streams, so a small team can build a big data platform in days.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Region / availability zone', 'A region is a geographic area with data centres (for example Mumbai); a zone is one isolated data centre group within it.'),
    ('IaaS / PaaS / SaaS', 'Rent machines / rent a managed platform / rent finished software.'),
    ('Serverless', 'No servers to choose or manage; you pay per query, per job or per data processed.'),
    ('Managed service', 'The provider installs, patches, scales and backs up the software for you.'),
    ('Egress', 'Data transferred out of a cloud region or out of the cloud; usually charged per GB.'),
    ('Spot / preemptible instance', 'Spare capacity sold at a deep discount that the provider can reclaim at short notice.'),
    ('FinOps', 'The practice of managing cloud costs: visibility, budgets, ownership and optimisation.'),
    ('Shared responsibility', 'The provider secures the cloud; the customer secures what they put in it.'),
]) + '''

  <h3>India regions (2026)</h3>
''' + facts([
    ('AWS', 'Asia Pacific (Mumbai) and Asia Pacific (Hyderabad)'),
    ('Microsoft Azure', 'Central India (Pune), South India (Chennai), West India (Mumbai) and additional regions with partners'),
    ('Google Cloud', 'asia-south1 (Mumbai) and asia-south2 (Delhi)'),
]) + '''
  <p class="muted">Region lists and service names change. Always check the provider’s current documentation before designing.</p>
''' + lv + '''
EXAM> Explain the advantages of cloud for big data (<b>elasticity, pay-per-use, managed services, separation of storage and compute, global reach</b>) and the concerns (<b>cost control, lock-in, security, data residency</b>). Add a mapping table of equivalent services on AWS, Azure and GCP for storage, processing, warehouse and streaming.'''

# ---------------------------------------------------------------- types
types = cards([
    ('IaaS: virtual machines', 'You rent VMs and install Hadoop, Spark or Kafka yourself. Most control, most work. Used for special needs or lift-and-shift migrations.', 'You run it'),
    ('Managed platforms (PaaS)', 'Managed Spark clusters, managed Kafka, managed Airflow. You choose sizes; the provider runs the software.', 'They run it'),
    ('Serverless', 'Submit SQL or a job; capacity appears and disappears automatically. Billed per TB scanned, per job or per second of use.', 'No servers'),
    ('SaaS data platforms', 'Snowflake, Databricks, Confluent Cloud: run on any major cloud, billed by usage, with their own consoles.', 'Multi-cloud'),
]) + '''

  <h3>The same job, three clouds</h3>
''' + table(['Job', 'AWS', 'Microsoft Azure', 'Google Cloud'], [
    ['<b>Lake storage</b>', 'Amazon S3', 'ADLS Gen2 / Blob Storage (OneLake in Fabric)', 'Cloud Storage'],
    ['<b>Managed Spark / Hadoop</b>', 'Amazon EMR, AWS Glue (Spark)', 'Azure Databricks, Fabric Spark, HDInsight', 'Dataproc'],
    ['<b>Data warehouse</b>', 'Amazon Redshift', 'Synapse Analytics / Fabric Warehouse', 'BigQuery'],
    ['<b>SQL directly on lake files</b>', 'Amazon Athena', 'Synapse serverless SQL / Fabric', 'BigQuery external & BigLake tables'],
    ['<b>Event streaming</b>', 'Kinesis, Amazon MSK (Kafka)', 'Event Hubs (Kafka-compatible)', 'Pub/Sub, Managed Kafka'],
    ['<b>Stream processing</b>', 'Managed Service for Apache Flink, Glue streaming', 'Stream Analytics, Databricks', 'Dataflow (Apache Beam)'],
    ['<b>Orchestration</b>', 'MWAA (Airflow), Step Functions', 'Data Factory, Fabric pipelines', 'Cloud Composer (Airflow), Workflows'],
    ['<b>Catalog / governance</b>', 'Glue Data Catalog, Lake Formation', 'Microsoft Purview, Unity Catalog', 'Dataplex, Data Catalog'],
    ['<b>Machine learning</b>', 'SageMaker', 'Azure Machine Learning', 'Vertex AI'],
], minw=720) + '''
  <p class="muted">Databricks, Snowflake and Confluent run on all three clouds. Names are as of 2026 and may change.</p>
TIP> Learn the <b>categories</b>, not the brand names. If you know “object storage + managed Spark + warehouse + streaming + orchestrator + catalog” and how they connect, you can work on any cloud after a week of reading its documentation.'''

# ---------------------------------------------------------------- steps
c1 = '''lake_tb, scan_fraction = 40, 0.01
price_per_tb = 450       # illustrative rupees per TB scanned
print("SELECT * (whole table):", lake_tb * price_per_tb, "rupees per query")
print("one day, 2 columns    :", lake_tb * scan_fraction * price_per_tb, "rupees per query")'''
c2 = '''nodes, rate = 20, 40       # node-hours at illustrative Rs 40
print("always on :", nodes * 24 * 30 * rate, "rupees/month")
print("3 h a day :", nodes * 3 * 30 * rate, "rupees/month")'''
steps = stepper([
    ('Pick a region and create the lake bucket',
     '<p>Kabir creates a bucket in the Mumbai region with folders by zone: <code>bronze/</code>, <code>silver/</code>, <code>gold/</code>, versioning on, encryption on, public access blocked.</p>',
     'The region decides latency, price and legal residency. Security settings are your job under the shared-responsibility model.'),
    ('Stream app events into the lake',
     '<p>App events flow into a managed stream (Kinesis, MSK, Event Hubs or Pub/Sub) and a delivery service writes them to <code>bronze/</code> every few minutes as compressed files.</p>',
     'No Kafka brokers to patch. The trade-off: you pay per shard, partition or GB, and you accept the provider’s limits.'),
    ('Catalog the tables',
     '<p>A crawler or a table format registers the files as tables (schema, partitions, location) in a catalog so SQL engines and Spark can find them by name.</p>',
     'The catalog is what turns a bucket of files into a lake people can query, and where access permissions are managed.'),
    ('Transform with managed Spark',
     code('python', 'cluster_cost.py', c2, run_code(c2)),
     'A managed Spark cluster (EMR, Databricks, Dataproc) or a serverless Spark job builds silver and gold tables. Starting it only for the job instead of leaving it on is the easiest big saving.'),
    ('Query with serverless SQL, carefully',
     code('python', 'scan_cost.py', c1, run_code(c1)),
     'Per-TB-scanned engines reward Parquet, partitions and selecting only needed columns. The same question can cost a hundred times less with a good layout.'),
    ('Watch the bill like a metric',
     '<p>Every resource is tagged with a team and project; a budget alert fires at 80% of the monthly limit; a weekly report shows the most expensive queries and idle resources.</p>',
     'In the cloud, cost is an engineering metric, just like latency and errors. Teams that watch it daily rarely get bill shocks.'),
])

# ---------------------------------------------------------------- two-view animation
def laptop(title, inner):
    return ('<rect x="40" y="20" width="280" height="168" rx="10" class="s-board"/><rect x="50" y="32" width="260" height="144" rx="4" class="s-card2"/><path d="M24 198h312l-12 14H36z" style="fill:#2B3A34"/>' + t(180, 48, title, 9.4, bold=True) + inner)
sql = t(60, 72, "SELECT city, SUM(amount)", 8.6, 'blue', anchor='start', mono=True) + t(60, 86, "FROM gold.orders", 8.6, 'blue', anchor='start', mono=True) + t(60, 100, "WHERE day = '2026-10-19'", 8.6, 'blue', anchor='start', mono=True) + t(60, 114, "GROUP BY city", 8.6, 'blue', anchor='start', mono=True)
see = [
    laptop('Query editor', sql + t(180, 150, 'Run ▶', 9.4, 'acc', bold=True)),
    laptop('Query editor', sql + t(180, 150, 'Queued… 1 s', 9, 'ink2')),
    laptop('Query editor', sql + t(180, 150, 'Running… 6 s', 9, 'ink2')),
    laptop('Results', ''.join(t(80, 74 + k * 16, c, 8.6, anchor='start') + t(280, 74 + k * 16, v, 8.6, anchor='end', bold=True) for k, (c, v) in enumerate([('Pune', '₹38.4 L'), ('Mumbai', '₹35.1 L'), ('Thane', '₹9.8 L'), ('Nashik', '₹4.2 L')])) + t(180, 150, '4 rows · 9 s', 9, 'green', bold=True)),
    laptop('Results', t(180, 92, 'Data scanned: 14 GB', 10, bold=True) + t(180, 112, 'Cost ≈ ₹6', 10, 'green', bold=True) + t(180, 150, 'shown under every query', 8.6, 'ink2')),
    laptop('Workspace', t(180, 96, 'Idle', 12, 'ink2', bold=True) + t(180, 120, 'nothing running, nothing billed', 9, 'green')),
]
def workers(n, tone='green'):
    o = ''
    for i in range(n):
        o += fill(20 + (i % 20) * 16, 120 + (i // 20) * 14, 12, 10, tone, rx=2)
    return o
behind = [
    label_box(120, 30, 120, 44, ['SQL engine', 'serverless'], 'acc', 9.6) + t(180, 110, 'No cluster is running yet.', 9, 'ink2') + t(180, 128, 'The query is just text sent to the service.', 9, 'ink2'),
    label_box(120, 30, 120, 44, ['planner'], 'acc', 9.6) + t(180, 96, 'Reads the catalog: table location, partitions, schema.', 8.8, 'ink2') + t(180, 112, 'Only partition day=2026-10-19 matches.', 8.8, 'green', bold=True),
    label_box(120, 20, 120, 40, ['workers start'], 'acc', 9.4) + t(180, 80, '200 workers read Parquet files from object storage', 8.8, 'ink2') + t(180, 96, '(only the city and amount columns)', 8.8, 'ink2') + workers(80),
    label_box(120, 20, 120, 40, ['aggregate'], 'acc', 9.4) + t(180, 80, 'Partial sums are combined into 4 result rows.', 8.8, 'ink2') + workers(80, 'blue'),
    label_box(60, 30, 240, 50, ['Meter: 14 GB scanned', '× ₹450 per TB (illustrative) ≈ ₹6'], 'blue', 9.4) + t(180, 112, 'Billed per byte read, not per second of compute.', 8.8, 'ink2'),
    label_box(60, 30, 240, 50, ['workers released', 'storage stays (₹ per GB-month)'], 'green', 9.4) + t(180, 112, 'Compute exists only while queries run.', 8.8, 'ink2') + t(180, 128, 'Storage and compute are separate.', 8.8, 'ink2'),
]
see_caps = ['Kabir writes a query for yesterday’s revenue by city and presses Run.', 'It is queued for about a second.', 'Running for a few seconds.', 'Four result rows appear after 9 seconds.',
            'Under the result: 14 GB scanned, cost about ₹6.', 'Afterwards the workspace is idle, and nothing is being billed for compute.']
behind_caps = ['There is no cluster waiting: the serverless SQL service receives the query text.',
               'The planner reads the catalog and finds that only one date partition can match.',
               'The service starts about 200 workers for a few seconds; each reads part of the Parquet files from object storage, only the two needed columns.',
               'Partial results are combined into four rows.',
               'The bill is based on bytes scanned: 14 GB at an illustrative ₹450 per TB is about ₹6.',
               'Workers are released immediately. Only the stored data keeps costing money, which is the separation of storage and compute in action. (Numbers are illustrative.)']
two = anim_two('Serverless SQL on a cloud lake', 'What Kabir sees, and what the cloud does', 'Kabir running a SQL query in a cloud query editor',
               'A serverless SQL engine planning, starting workers, scanning lake files and billing per data scanned', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: the bill (real numbers from cloud_bill.out)
steps_bill = [('Naive', 50.5), ('+ Parquet & partitions', 8.3), ('+ auto-shutdown', 3.3), ('+ spot workers', 2.8), ('+ no egress', 2.4)]
def billbars(n):
    rows = []
    for k, (name, v) in enumerate(steps_bill):
        if k < n:
            rows.append((name, v / 50.5 * 100, 'red' if k == 0 else 'green', f'₹{v} L'))
    return t(14, 22, 'Monthly bill (₹ lakh, illustrative prices)', 9, 'ink2', anchor='start') + bars(rows, x=150, y=32, w=150, gap=22)
fr1 = [
    billbars(1) + cap('CSV files, SELECT * all day, cluster always on.', '“SQL scans” alone: ₹43.2 lakh.', 'red', y=152, h=44),
    billbars(2) + cap('Parquet + date partitions + only needed columns:', 'each query scans 0.02 TB instead of 0.8 TB.', 'green', y=152, h=44),
    billbars(3) + cap('Start the Spark cluster for the 3-hour job only,', 'instead of 24 hours a day.', 'green', y=152, h=44),
    billbars(4) + cap('Run workers on spot capacity, about 70% cheaper here.', 'Spark retries any task on a reclaimed node.', 'green', y=152, h=44),
    billbars(5) + cap('Stop copying data out of the region every day.', 'Result: 95% lower bill, same dashboards.', 'green', y=152, h=44),
]
s1 = anim_one('Real-time scenario 1', 'From ₹50 lakh to ₹2.4 lakh a month',
              'These figures come from the program in “Run it on your PC” below, with illustrative prices. Watch each fix shrink TiffinGo’s monthly bill.',
              'FinOps in five steps', 'A monthly cloud bill shrinking as layout, shutdown, spot and egress fixes are applied', fr1,
              ['The first version stores CSV, lets analysts run <code>SELECT *</code> hundreds of times a day on a pay-per-scan engine, and keeps a 20-node cluster running all day. Scans alone cost ₹43 lakh.',
               'Rewriting to Parquet, partitioning by date and selecting only needed columns cuts the data each query reads by 40 times. The bill falls to ₹8.3 lakh.',
               'The Spark cluster is started only for the 3-hour nightly job and terminated afterwards: ₹3.3 lakh.',
               'Workers run on spot capacity, which is much cheaper; if the cloud reclaims a node, Spark simply re-runs its tasks: ₹2.8 lakh.',
               'A daily copy of data to another region is stopped, removing egress charges: ₹2.4 lakh, a 95% saving with the same results. (Prices are illustrative, not a real price list.)'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: spot node reclaimed
def spot(states, note1, note2, tone):
    o = label_box(14, 30, 90, 46, ['driver', 'on-demand'], 'blue', 9)
    for k, st in enumerate(states):
        x = 120 + (k % 4) * 58
        y = 24 + (k // 4) * 52
        lab, tn = {'run': ('spot', 'green'), 'gone': ('reclaimed', 'red'), 'new': ('new spot', 'amber'), 'done': ('done', 'green')}[st]
        o += label_box(x, y, 52, 44, [f'W{k + 1}', lab], tn, 8.4)
    return o + cap(note1, note2, tone, y=140, h=44)
fr2 = [
    spot(['run'] * 8, 'Nightly Spark job: driver on a regular machine,', '8 workers on spot capacity at a big discount.', 'blue'),
    spot(['run', 'run', 'gone', 'run', 'run', 'run', 'run', 'run'], 'The cloud needs capacity back: W3 gets a short', 'warning, then is reclaimed mid-job.', 'red'),
    spot(['run', 'run', 'gone', 'run', 'run', 'run', 'run', 'run'], 'Spark notices the lost executor and re-runs W3’s', 'tasks on the other workers (lineage, Lesson 1.4).', 'amber'),
    spot(['run', 'run', 'new', 'run', 'run', 'run', 'run', 'run'], 'The cluster manager requests a replacement node', 'to keep the job on schedule.', 'amber'),
    spot(['done'] * 8, 'The job finishes about 6 minutes late,', 'at a fraction of the on-demand price.', 'green'),
]
s2 = anim_one('Real-time scenario 2', 'A spot worker disappears in the middle of the job',
              'Spot (or preemptible) machines are spare cloud capacity at a deep discount, with one catch: the provider can take them back at short notice. Watch why they suit Spark batch jobs.',
              'Spot capacity', 'A Spark cluster losing one spot worker and recovering by re-running its tasks', fr2,
              ['The nightly job runs with the driver on a normal on-demand machine and eight workers on spot capacity.',
               'The cloud needs its capacity back. Worker 3 gets a short warning (typically a couple of minutes or less) and is taken away.',
               'Spark detects the lost executor and re-runs the tasks that worker was handling on the remaining workers, recomputing any lost data from its lineage.',
               'The cluster manager asks for a replacement node, often trying a different machine type or zone.',
               'The job finishes a few minutes late but costs far less. Rule of thumb: spot for stateless, retryable work (Spark workers, batch); on-demand for drivers, databases and anything that can’t be interrupted.'])

# ---------------------------------------------------------------- scenario 3 (advanced): residency, DR, egress, lock-in
fr3 = [
    label_box(20, 40, 140, 56, ['Mumbai region', 'payments lake (primary)'], 'green', 9.2) + label_box(200, 40, 140, 56, ['Singapore region', 'cheaper this month?'], 'card', 9.2)
    + arrow(162, 68, 198, 68, 'red', 2) + t(180, 24, 'Proposal: move payment data to Singapore', 9.4, 'red', bold=True) + cap('Not allowed: payment-system data must be stored', 'in India (RBI, 2018). Region choice is a legal decision.', 'red', y=120, h=44),
    label_box(20, 40, 140, 56, ['Mumbai region', 'primary'], 'green', 9.2) + label_box(200, 40, 140, 56, ['Hyderabad region', 'disaster recovery'], 'blue', 9.2)
    + arrow(162, 68, 198, 68, 'ink3', 2, dash=True) + t(180, 24, 'Disaster recovery inside India', 9.4, 'green', bold=True) + cap('Async replication to a second Indian region.', 'If one region fails, switch over without leaving India.', 'green', y=120, h=44),
    label_box(20, 40, 140, 56, ['Cloud A lake', '60 TB'], 'green', 9.2) + label_box(200, 40, 140, 56, ['Other cloud / office', 'daily full copy'], 'card', 9.2)
    + arrow(162, 68, 198, 68, 'red', 2) + t(180, 24, 'The hidden meter: egress', 9.4, 'red', bold=True) + cap('Moving data OUT of a region or cloud is billed per GB.', 'Copy only what is needed, incrementally, and compress it.', 'amber', y=120, h=44),
    box(14, 30, 332, 80, 'card') + t(180, 50, 'Avoiding lock-in', 9.8, 'acc', bold=True) + t(28, 72, '• open table formats: Parquet + Delta Lake / Iceberg', 8.6, anchor='start') + t(28, 90, '• open engines and APIs: Spark, Kafka protocol, Airflow, SQL', 8.6, anchor='start')
    + cap('Proprietary services are fine, but keep the data itself', 'in open formats so it can move later.', 'blue', y=124, h=44),
    box(14, 30, 332, 84, 'green') + t(180, 50, 'Security checklist', 9.8, 'green', bold=True) + t(28, 70, '• no public buckets · encryption at rest and in transit', 8.6, anchor='start') + t(28, 86, '• least-privilege roles · private endpoints · audit logs', 8.6, anchor='start') + t(28, 102, '• keys managed in a KMS, rotated', 8.6, anchor='start')
    + cap('The provider secures the cloud; you secure your data.', '', 'green', y=128, h=34),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Where may the data live? Residency, DR, egress and lock-in',
              'Choosing a cloud region is not only about price and speed. Watch four decisions an Indian fintech data team must get right before writing any pipeline.',
              'Region and risk decisions', 'Cloud regions for an Indian fintech: residency, disaster recovery, egress and lock-in', fr3,
              ['Someone proposes moving the payments lake to a cheaper foreign region. For payment-system data this is not allowed: the RBI’s 2018 direction requires it to be stored only in India. Regions are a compliance decision.',
               'Disaster recovery is therefore set up across two Indian regions, for example Mumbai and Hyderabad, with asynchronous replication and a rehearsed switch-over.',
               'Data leaving a region or cloud is charged per GB (<b>egress</b>). A daily full copy of 60 TB elsewhere is expensive; copy incrementally and only what is needed.',
               'To avoid being locked in, keep the data in open formats (Parquet with Delta Lake or Iceberg) and prefer open engines and APIs, even when using managed services.',
               'Security is shared: the provider protects the infrastructure, while the team must block public access, encrypt data, use least-privilege roles and private endpoints, and keep audit logs.'])

realworld = '''  <p>Three live scenarios: a monthly bill cut by 95% (real numbers from the program below), a spot worker reclaimed mid-job, and an advanced look at data residency, disaster recovery, egress and lock-in.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>How Indian companies use the cloud for data</h3>
''' + usecase('<circle cx="40" cy="45" r="16" style="fill:var(--green);opacity:.7"/><circle cx="68" cy="34" r="12" style="fill:var(--green);opacity:.5"/><circle cx="82" cy="58" r="14" style="fill:var(--green);opacity:.6"/>',
              '1. Start-ups: cloud-native from day one', 'Food, travel, ed-tech and fintech start-ups build lakes on object storage with managed Spark or a SaaS platform, a cloud warehouse for BI and managed Kafka, without owning a single server.', ['Apps', '*Managed cloud services', 'Dashboards + ML']) + usecase(
    '<rect x="14" y="20" width="40" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><rect x="66" y="20" width="40" height="50" rx="6" class="s-soft-green" style="stroke:var(--green)"/><path d="M54 45h12" style="stroke:var(--ink);stroke-width:2"/>',
    '2. Banks and insurers: hybrid', 'Regulated companies often keep core systems on premises and use cloud regions in India for analytics, ML and customer apps, with strict controls on what data moves where.', ['Core banking (on-prem)', '*Controlled transfer', 'Cloud analytics in India']) + usecase(
    '<rect x="20" y="20" width="80" height="50" rx="6" class="s-soft-acc" style="stroke:var(--track)"/><text x="60" y="50" text-anchor="middle" font-size="11" font-weight="700" class="s-acc">₹ budget</text>',
    '3. FinOps teams', 'Larger companies run FinOps practices: tagging, monthly cost reviews per team, rightsizing, spot usage targets and alerts on expensive queries, because cloud spend can rival salaries.', ['Usage data', '*Tags + budgets + reviews', 'Lower unit cost']) + usecase(
    '<path d="M20 60 Q40 20 60 46 T100 30" style="fill:none;stroke:var(--violet);stroke-width:3"/>',
    '4. Hadoop to cloud migrations', 'Many enterprises are moving older on-premises Hadoop clusters to cloud lakehouses: data copied to object storage, Hive tables converted to Delta or Iceberg, jobs moved to managed Spark.', ['On-prem HDFS', '*Copy + convert', 'Cloud lakehouse'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'A ₹50 lakh surprise', story)
        + part(2, 'definition', 'Definition', 'Big data on the cloud', definition)
        + part(3, 'types', 'Types and ways to use it', 'Service models and the AWS, Azure and GCP map', types)
        + part(4, 'steps', 'Step by step', 'Building a small cloud data platform', steps)
        + part(5, 'animation', 'See it happen', 'One serverless query: what Kabir sees, and what the cloud does', '  <p>Step through the six frames. Left: Kabir running a query. Right: how a serverless engine plans, scales out, bills and disappears.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: cost, capacity and compliance', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Cloud architecture', 'Fresher', 'Design a small analytics platform on a cloud',
            'A start-up wants daily dashboards from app events and its PostgreSQL database, on any one cloud, with a tiny team.',
            'can you assemble the standard building blocks and justify them?',
            '<ul><li><b>Ingest:</b> app events to a managed stream, delivered to object storage; database changes extracted nightly (or with change data capture).</li><li><b>Store:</b> object storage lake with bronze/silver/gold zones, Parquet with Delta Lake or Iceberg, in an Indian region.</li><li><b>Process:</b> serverless or managed Spark jobs, or SQL/dbt in a cloud warehouse.</li><li><b>Serve:</b> warehouse or serverless SQL for BI dashboards.</li><li><b>Orchestrate:</b> managed Airflow.</li><li><b>Govern and secure:</b> catalog, IAM roles, encryption, budgets and tags from day one.</li></ul>',
            'listing ten services without explaining how data flows or what it costs.')
        + scn('FinOps · cost', '1–3 years', 'The query bill tripled this month',
              'Serverless SQL costs tripled. Data volume grew only 10%.',
              'can you investigate and fix cloud cost problems?',
              '<ol><li>Find the top queries by bytes scanned and who ran them (query history, cost reports by tag).</li><li>Look for <code>SELECT *</code>, missing partition filters, dashboards refreshing every minute and new unpartitioned tables.</li><li>Fix the layout: Parquet, partitions, clustering; create small aggregate tables for dashboards.</li><li>Add guardrails: per-user or per-workgroup scan limits, required partition filters, budget alerts.</li><li>Share a weekly cost report with teams.</li></ol>',
              'switching to a bigger fixed cluster without finding what changed.')
        + scn('Compliance · data residency', '1–3 years', 'Can we use a cheaper overseas region?',
              'A fintech’s finance team notices that an overseas region is cheaper and asks to move the payments analytics lake there.',
              'do you know that region choice is a compliance decision?',
              '<p>Payment-system data in India must be stored in India under the RBI’s 2018 direction on storage of payment system data, and other data may have contractual or DPDP-related obligations. Keep the lake in Indian regions, use a second Indian region for disaster recovery, and reduce cost through layout, lifecycle tiers, reserved or committed-use discounts and spot capacity instead. Involve the compliance team before moving any regulated data.</p>',
              'deciding on price alone.')
        + scn('Fundamentals · interview', 'Fresher', '“What are the advantages and risks of cloud for big data?”',
              'A common question in data engineering interviews.',
              'can you give a balanced answer with examples?',
              '<p><b>Advantages:</b> elasticity (scale up for peaks and down afterwards), pay-per-use, managed services that save operations work, separation of storage and compute, global regions, fast experimentation. <b>Risks:</b> uncontrolled costs (scans, idle clusters, egress), vendor lock-in, security misconfiguration (public buckets, broad permissions), data-residency rules, and dependence on provider outages. Mitigations: FinOps practices, open formats, least-privilege security, region planning and multi-zone designs.</p>',
              'saying only “the cloud is cheaper”.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
