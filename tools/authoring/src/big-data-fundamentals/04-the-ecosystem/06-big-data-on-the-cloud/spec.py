import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='04-the-ecosystem', lesson='06-big-data-on-the-cloud', n='4.6',
    module_label='Module 4 · The Ecosystem',
    title='Big data on the cloud: AWS, Azure and GCP',
    desc='Big data on the cloud explained: IaaS, managed services and serverless, the equivalent big data services on AWS, Azure and Google Cloud (S3, EMR, Glue, Athena, Redshift, Databricks, Synapse/Fabric, BigQuery, Dataproc, Dataflow, Kinesis, Event Hubs, Pub/Sub), India regions, cost meters and FinOps, spot instances, egress, lock-in, security and RBI data residency. Animations and a cloud bill estimator for your PC.',
    og_desc='Build a data platform in a weekend, and see how a ₹50 lakh cloud bill becomes ₹2.4 lakh. Learn the AWS, Azure and GCP big data map.',
    minutes=30, level='Beginner → Advanced',
    lead='The cloud lets a two-person team build a data platform in a weekend, and a careless query rack up lakhs in a day. In this lesson you learn the <b>same building blocks on AWS, Azure and Google Cloud</b>, watch a serverless query scale out and vanish, cut a monthly bill from ₹50 lakh to ₹2.4 lakh, survive a spot machine disappearing mid-job, and see why payment data must stay in Indian regions.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Cloud bill estimator for your PC'],
)

RUN = dict(
    heading='Translate a design between clouds',
    intro='<p>A small dictionary maps each job in a data platform to a service on each cloud. The program prints the same architecture on AWS, Azure and Google Cloud. Then try the challenges: compare scan costs, always-on vs on-demand clusters, spot savings, egress and storage tiers.</p>',
    code='''services = {
    "lake storage":   {"AWS": "S3",         "Azure": "ADLS Gen2",       "GCP": "Cloud Storage"},
    "managed Spark":  {"AWS": "EMR / Glue", "Azure": "Databricks",      "GCP": "Dataproc"},
    "warehouse":      {"AWS": "Redshift",   "Azure": "Synapse/Fabric",  "GCP": "BigQuery"},
    "event stream":   {"AWS": "Kinesis/MSK","Azure": "Event Hubs",      "GCP": "Pub/Sub"},
    "orchestration":  {"AWS": "MWAA",       "Azure": "Data Factory",    "GCP": "Cloud Composer"},
}
design = ["event stream", "lake storage", "managed Spark", "warehouse", "orchestration"]

for cloud in ["AWS", "Azure", "GCP"]:
    print(f"{cloud:5}: " + " -> ".join(services[job][cloud] for job in design))
''',
    anno=[
        ('"lake storage":   {"AWS": "S3",         "Azure": "ADLS Gen2",       "GCP": "Cloud Storage"},', 'Every cloud has the same categories; only the product names differ.'),
        ('design = ["event stream", "lake storage", "managed Spark", "warehouse", "orchestration"]', 'Design in categories first, then pick the product on the chosen cloud.'),
    ],
    tasks=[
        dict(label='1 · Same design, three clouds', hint='Press <b>Run</b>. Add a row <code>"catalog"</code> (Glue Data Catalog, Purview, Dataplex) and put it in the design.', code=None),
        dict(label='2 · Scan cost', hint='A per-TB-scanned engine bills by bytes read. Compare a full-table query with a partition-pruned, two-column query. Prices are illustrative. Try 1,000 queries a day.',
             code='''price_per_tb = 450            # rupees, illustrative
table_tb = 40
queries_per_day = 300
full = table_tb
pruned = table_tb * (1 / 365) * (2 / 20)    # one day of 365, 2 of 20 columns
for name, tb in [("SELECT * on whole table", full), ("one day, 2 columns", pruned)]:
    monthly = tb * price_per_tb * queries_per_day * 30
    print(f"{name:24}: {tb:8.3f} TB/query, Rs {monthly:12,.0f} per month")
'''),
        dict(label='3 · Always on vs on demand', hint='A 20-node cluster at Rs 40 per node-hour. Compare running all day with running only for a 3-hour job. Change the job to 6 hours.',
             code='''nodes, rate, days = 20, 40, 30
for name, hours in [("always on", 24), ("job only", 3)]:
    print(f"{name:9}: Rs {nodes * rate * hours * days:,} per month")
'''),
        dict(label='4 · Spot savings', hint='Spot workers cost much less but some get reclaimed, adding rework. Estimate the effective saving when 10% of work must be redone. Try 30%.',
             code='''on_demand, spot = 40, 12          # rupees per node-hour, illustrative
node_hours = 20 * 3 * 30
rework = 0.10
spot_cost = node_hours * (1 + rework) * spot
print("on-demand:", node_hours * on_demand)
print("spot     :", round(spot_cost))
print(f"saving   : {(1 - spot_cost / (node_hours * on_demand)) * 100:.0f}%")
'''),
        dict(label='5 · Egress (advanced)', hint='Data leaving a region is billed per TB. Compare copying the full 60 TB lake every day with copying only the 0.3 TB of daily changes. Prices are illustrative.',
             code='''egress_per_tb = 7000
for name, tb_per_day in [("full copy daily", 60), ("changes only", 0.3)]:
    print(f"{name:16}: Rs {tb_per_day * 30 * egress_per_tb:,.0f} per month")
'''),
        dict(label='6 · Storage tiers (advanced)', hint='Older partitions move to cheaper tiers. Compute the monthly storage bill for a 3-year lake with 100 GB/day. Prices per TB-month are illustrative.',
             code='''price = {"hot": 1900, "cool": 1000, "archive": 150}
gb_per_day = 100
ages = {"hot": 60, "cool": 365 - 60, "archive": 3 * 365 - 365}   # days of data in each tier
bill = {t: ages[t] * gb_per_day / 1024 * price[t] for t in price}
print({t: f"Rs {v:,.0f}" for t, v in bill.items()})
print("total: Rs", f"{sum(bill.values()):,.0f}", "| all hot would be Rs", f"{3 * 365 * gb_per_day / 1024 * price['hot']:,.0f}")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: estimate and shrink a cloud bill',
    intro='<p>This program estimates the monthly bill of a small cloud data platform (storage, SQL scans, a Spark cluster and data transfer) with illustrative prices, then applies five fixes one by one: columnar files and partitions, auto-shutdown, spot workers and keeping data in region. Change the assumptions at the top and run it again. Save it as <code>cloud_bill.py</code>.</p>',
    items=[
        dict(title='A cloud bill, before and after FinOps', file='cloud_bill.py',
             cmd=open(os.path.join(HERE, 'cloud_bill.py')).read() + '\n# In a terminal:  python cloud_bill.py',
             output=open(os.path.join(HERE, 'cloud_bill.out')).read(),
             note='Recorded from a real run with Python 3.13. The prices are round illustrative numbers, not any provider\'s price list; use your cloud\'s pricing calculator for real estimates. The pattern is what matters: badly laid-out data scanned many times and idle clusters usually dominate the bill.'),
    ],
)

TRACE = dict(
    heading='Adding up a cloud bill, one line at a time',
    intro='<p>Three meters are added: storage, compute and scans. Watch the total grow, and notice which meter dominates.</p>',
    code='''lake_tb, storage_rate = 60, 1900
node_hours, node_rate = 1800, 40
tb_scanned, scan_rate = 240, 450
bill = {}
bill["storage"] = lake_tb * storage_rate
bill["compute"] = node_hours * node_rate
bill["scans"] = tb_scanned * scan_rate
print(bill, sum(bill.values()))
''',
    notes={5: 'Storage :: Paid every month for data at rest.',
           6: 'Compute :: Paid only while machines run.',
           7: 'Scans :: Paid per TB read by serverless SQL: the meter that layout controls.'},
)

WORKED_INTRO = 'Four cloud decisions, from mapping services to estimating a spot-instance plan. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Cloud basics · mapping', title='Find the equivalent service',
         problem='<p>A team moving from AWS to Google Cloud lists the AWS services it uses. Print the Google Cloud equivalent of each.</p>',
         inp='S3, EMR, Redshift, Kinesis, MWAA',
         approach=['Store an AWS → GCP mapping in a dictionary.',
                   'Look up each service.',
                   'Print “no direct match” for anything missing.'],
         code='''aws_to_gcp = {"S3": "Cloud Storage", "EMR": "Dataproc", "Redshift": "BigQuery",
              "Kinesis": "Pub/Sub", "MWAA": "Cloud Composer", "Athena": "BigQuery"}
for svc in ["S3", "EMR", "Redshift", "Kinesis", "MWAA", "QuickSight"]:
    print(f"{svc:10} -> {aws_to_gcp.get(svc, 'no direct match: check docs')}")
''', notes={3: 'Look-up :: <code>get</code> gives a default when the key is missing.'},
         tryit='Add an Azure column for each service and print all three side by side.'),
    dict(level='i', tag='FinOps · scans', title='Cost of a dashboard on a pay-per-scan engine',
         problem='<p>A dashboard has 6 charts, refreshed every 15 minutes during 12 working hours. Each chart scans 25 GB. At an illustrative ₹450 per TB, what does it cost per month (22 working days), and what if refreshed hourly from a small aggregate table scanning 0.5 GB per chart?</p>',
         inp='6 charts, every 15 min × 12 h, 25 GB each, 22 days',
         approach=['Refreshes per day = 12 hours × 4.',
                   'TB per month = charts × refreshes × days × GB ÷ 1024.',
                   'Cost = TB × price.'],
         code='''price = 450
def monthly(charts, per_day, gb, days=22):
    tb = charts * per_day * days * gb / 1024
    return tb, tb * price
for name, per_day, gb in [("every 15 min, raw table", 48, 25), ("hourly, aggregate table", 12, 0.5)]:
    tb, cost = monthly(6, per_day, gb)
    print(f"{name:25}: {tb:7.1f} TB scanned, Rs {cost:10,.0f} per month")
''', notes={3: 'Volume :: Small numbers multiply quickly across charts, refreshes and days.'},
         tryit='Some dashboards stay open on TVs all night. Add 12 more hours of refreshes and see the cost.'),
    dict(level='i', tag='Architecture · provisioned vs serverless', title='When does a fixed cluster beat serverless?',
         problem='<p>Serverless costs ₹450 per TB scanned. A provisioned warehouse costs ₹3 lakh per month regardless of use. Find the break-even monthly scan volume and decide for teams scanning 150 TB and 1,200 TB a month.</p>',
         inp='₹450/TB vs ₹3 lakh/month · 150 TB, 1,200 TB',
         approach=['Break-even TB = fixed cost ÷ price per TB.',
                   'Below it, serverless is cheaper; above it, provisioned is.',
                   'Compare both teams.'],
         code='''per_tb, fixed = 450, 3_00_000
break_even = fixed / per_tb
print(f"break-even: {break_even:.0f} TB per month")
for team, tb in [("marketing", 150), ("data science", 1200)]:
    serverless = tb * per_tb
    choice = "serverless" if serverless < fixed else "provisioned"
    print(f"{team:12}: serverless Rs {serverless:,.0f} vs fixed Rs {fixed:,} -> {choice}")
''', notes={3: 'Break-even :: The scan volume where both options cost the same.'},
         tryit='Usage is spiky: 50 TB most months but 2,000 TB at year end. Which model, or which mix, would you choose?'),
    dict(level='a', tag='Compute planning · spot', title='Plan a spot-heavy Spark cluster',
         problem='<p>A nightly job needs 160 node-hours. On-demand costs ₹40/hour, spot ₹12/hour. History shows 15% of spot node-hours are lost to reclaims and must be redone. The driver and 2 core nodes stay on-demand for the full 4-hour run. Compare all-on-demand with the mixed plan.</p>',
         inp='160 node-hours, ₹40 vs ₹12, 15% rework, 3 on-demand nodes × 4 h',
         approach=['All on-demand: node-hours × ₹40 (the 3 fixed nodes are part of the 160).',
                   'Mixed: 12 on-demand node-hours plus the rest on spot, inflated by 15% rework.',
                   'Compare costs.'],
         code='''total_nh, od, spot, rework = 160, 40, 12, 0.15
fixed_nh = 3 * 4
all_od = total_nh * od
spot_nh = (total_nh - fixed_nh) * (1 + rework)
mixed = fixed_nh * od + spot_nh * spot
print("all on-demand: Rs", all_od)
print("mixed plan   : Rs", round(mixed), f"({spot_nh:.0f} spot node-hours incl. rework)")
print(f"saving       : {(1 - mixed / all_od) * 100:.0f}%")
''', notes={5: 'Rework :: Reclaimed nodes mean some work is done twice.', 6: 'Mixed :: Stable on-demand core plus cheap spot workers.'},
         tryit='During festival weeks spot capacity gets scarce and rework rises to 40%. Is spot still worth it?'),
]

QUIZ = [
    dict(q='Which AWS service is the usual foundation of a data lake?', options=['Amazon EC2', 'Amazon S3', 'Amazon RDS', 'AWS Lambda'], answer=1,
         why='Object storage (Amazon S3; ADLS Gen2 on Azure; Cloud Storage on GCP) holds the lake\'s files.'),
    dict(q='Google BigQuery is best described as:', options=['An object store', 'A serverless cloud data warehouse', 'A message queue', 'A Hadoop cluster'], answer=1,
         why='BigQuery is Google Cloud\'s serverless data warehouse, often billed by data scanned or by reserved capacity.'),
    dict(q='What is the Azure equivalent of Google Pub/Sub or Amazon Kinesis?', options=['Azure Event Hubs', 'Azure Blob Storage', 'Azure Functions', 'Azure DevOps'], answer=0,
         why='Event Hubs is Azure\'s managed event-streaming service (with a Kafka-compatible endpoint).'),
    dict(q='Why does SELECT * on a large table cost so much on serverless SQL engines like Athena or BigQuery on-demand?', options=['They charge per row returned', 'They charge per byte scanned, and SELECT * reads every column', 'They charge per user', 'They block SELECT *'], answer=1,
         why='Billing is by data scanned; select only needed columns, partition, and use columnar formats.'),
    dict(q='What is a spot (or preemptible) instance?', options=['A machine reserved for 3 years', 'Discounted spare capacity that the provider can take back at short notice', 'A machine with a GPU', 'A free machine'], answer=1,
         why='Spot capacity is much cheaper but interruptible, so it suits fault-tolerant batch work like Spark workers.'),
    dict(q='Which cost is often forgotten in cloud designs?', options=['Electricity', 'Egress: data transferred out of a region or cloud', 'Office rent', 'Keyboards'], answer=1,
         why='Moving data out of a region or cloud is billed per GB and can be large for daily full copies.'),
    dict(q='Under the shared responsibility model, who must make sure a storage bucket is not publicly readable?', options=['The cloud provider', 'The customer', 'The internet service provider', 'Nobody'], answer=1,
         why='The provider secures the infrastructure; customers secure their data, permissions and configuration.'),
    dict(q='A fintech wants its payment data lake in a foreign region because it is cheaper. What is the main problem?', options=['Foreign regions are slower', 'Payment-system data must be stored in India under RBI rules', 'Foreign regions don\'t support Parquet', 'There is no problem'], answer=1,
         why='The RBI\'s 2018 direction requires payment-system data to be stored in India, so region choice is a compliance decision.'),
]

REVISION = [
    'Cloud = on-demand, pay-per-use, managed services, elastic; storage and compute separated.',
    'Models: IaaS (VMs) → managed PaaS → serverless → SaaS platforms (Databricks, Snowflake, Confluent).',
    'Map: storage S3 / ADLS Gen2 / Cloud Storage · Spark EMR-Glue / Databricks / Dataproc · warehouse Redshift / Synapse-Fabric / BigQuery.',
    'Streaming Kinesis-MSK / Event Hubs / Pub/Sub · orchestration MWAA / Data Factory / Cloud Composer.',
    'Cost meters: storage, compute, scans, requests, <b>egress</b>. FinOps: tags, budgets, layouts, auto-shutdown, spot.',
    'Spot/preemptible: cheap but reclaimable → stateless, retryable work only.',
    'Security is shared; avoid lock-in with open formats; payment data stays in Indian regions (RBI).',
]
FAQ = [
    ('What are the benefits of cloud computing for big data?', 'Elastic scaling to handle peaks and shrinking afterwards, pay-per-use pricing without large upfront hardware purchases, managed services that remove installation and maintenance work, separation of storage and compute so each scales independently, global regions for low latency and disaster recovery, and fast experimentation with new tools.'),
    ('Compare the big data services of AWS, Azure and GCP.', 'For storage: Amazon S3, Azure Data Lake Storage Gen2/Blob, Google Cloud Storage. Managed Spark/Hadoop: Amazon EMR and AWS Glue, Azure Databricks/Fabric/HDInsight, Google Dataproc. Data warehouses: Amazon Redshift, Azure Synapse Analytics/Microsoft Fabric, Google BigQuery. Streaming: Amazon Kinesis and MSK, Azure Event Hubs, Google Pub/Sub. Orchestration: Amazon MWAA and Step Functions, Azure Data Factory, Google Cloud Composer. Databricks, Snowflake and Confluent run on all three.'),
    ('What is serverless in the context of big data?', 'A model where you submit queries or jobs without choosing or managing servers; the provider allocates capacity automatically and bills by usage, such as per TB scanned (Athena, BigQuery on-demand), per job or per second of processing (serverless Spark, Dataflow). It is convenient for spiky workloads but needs care to control costs.'),
    ('How do you control cloud costs for a data platform?', 'Tag resources by team and project, set budgets and alerts, use columnar formats and partitioning to reduce scans, select only needed columns, build aggregate tables for dashboards, auto-terminate idle clusters and autoscale, use spot capacity for fault-tolerant jobs, apply storage lifecycle tiers, reduce egress, and review the most expensive queries and resources regularly (FinOps).'),
    ('What is vendor lock-in and how can it be reduced?', 'Lock-in is the difficulty and cost of moving away from a provider because your data, code and processes depend on its proprietary services. It can be reduced by keeping data in open formats (Parquet, Delta Lake, Iceberg), using open engines and APIs (Spark, Kafka protocol, Airflow, standard SQL), infrastructure-as-code, and isolating provider-specific code behind clear interfaces.'),
]

PRACTICE_INTRO = 'Cloud cost and design exercises with illustrative prices. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Storage bill', stmt='Store 25 TB at Rs 1,900 per TB-month. Print the monthly cost.', inp='25 TB',
         code='''print(25 * 1900)
''', explain='Storage is billed per GB- or TB-month of data kept.'),
    dict(level='easy', title='Scan cost', stmt='A query scans 300 GB at Rs 450 per TB. Print its cost.', inp='300 GB',
         code='''print(round(300 / 1024 * 450, 2))
''', explain='Convert GB to TB, then multiply by the price.'),
    dict(level='easy', title='Service look-up', stmt='Print the Azure service for event streaming.', inp='event streaming',
         code='''azure = {"storage": "ADLS Gen2", "spark": "Azure Databricks", "event streaming": "Event Hubs"}
print(azure["event streaming"])
''', explain='Event Hubs is Azure\'s managed streaming service.'),
    dict(level='medium', title='Idle cluster waste', stmt='A 12-node cluster at Rs 40/node-hour runs 24 h/day but is busy only 5 h. Print the monthly cost of idle hours.', inp='12 nodes, 19 idle h/day',
         code='''print(12 * 40 * 19 * 30)
''', explain='Auto-termination after a job removes this waste.'),
    dict(level='medium', title='Pruned scan', stmt='A 36 TB table is partitioned into 360 days and has 18 equal columns. A query reads 7 days and 3 columns. Print TB scanned.', inp='36 TB, 7/360 days, 3/18 columns',
         code='''print(round(36 * 7 / 360 * 3 / 18, 3), "TB")
''', explain='Partitions cut rows; columnar storage cuts columns.'),
    dict(level='advanced', title='Spot vs on-demand', stmt='300 node-hours. On-demand Rs 40, spot Rs 12 with 20% rework. Print both costs.', inp='300 nh',
         code='''print("on-demand:", 300 * 40, "| spot:", round(300 * 1.2 * 12))
''', explain='Even with rework, spot is much cheaper for retryable work.'),
    dict(level='advanced', title='Break-even reservation', stmt='On-demand costs Rs 40/hour; a 1-year commitment costs Rs 2,10,000 per node for the year. Above how many hours per year of use is the commitment cheaper?', inp='Rs 40/h vs Rs 2.1 lakh/year',
         code='''hours = 2_10_000 / 40
print(round(hours), "hours per year (", round(hours / 8760 * 100), "% of the year )")
''', explain='Commitments pay off for steady, always-on workloads; on-demand or spot for spiky ones.'),
    dict(level='business', title='Monthly platform estimate', stmt='Storage 50 TB (Rs 1,900/TB), 10 TB scanned per day (Rs 450/TB), a 15-node cluster 4 h/day (Rs 40/node-hour). Print the monthly total in lakh.', inp='as given',
         code='''total = 50 * 1900 + 10 * 30 * 450 + 15 * 4 * 30 * 40
print(f"Rs {total / 1e5:.2f} lakh per month")
''', explain='A first estimate like this belongs in every design document.'),
    dict(level='business', title='Cost per order', stmt='The data platform costs Rs 2.4 lakh per month and the company handles 30 crore orders a month. Print the data-platform cost per 1,000 orders.', inp='Rs 2.4 lakh, 30 crore orders',
         code='''print(f"Rs {2.4e5 / 30e7 * 1000:.2f} per 1,000 orders")
''', explain='Unit cost makes platform spend comparable as the business grows.'),
]

SCN_INTRO = 'Cloud questions from real projects and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
