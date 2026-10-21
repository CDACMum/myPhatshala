"""Generate a 50-mark Big Data Fundamentals practice paper.
Change SEED for a new paper; set SHOW_KEY = True to print answer hints."""
import random

SEED = 2026
SHOW_KEY = False
BANK = {
    2: [("Define big data using the 5 Vs.", "Volume, velocity, variety, veracity, value; one line each"),
        ("What is horizontal scaling?", "Add more machines (scale out) vs a bigger machine"),
        ("Differentiate OLTP and OLAP.", "Transactions, row-wise, many small writes vs analytics, columnar, large scans"),
        ("What is a data lake?", "Cheap storage of raw files of any type, schema-on-read"),
        ("What is replication factor?", "Number of copies of each block or partition, e.g. 3"),
        ("Name two NoSQL database types with an example each.", "Key-value: Redis; document: MongoDB; wide-column: Cassandra; graph: Neo4j"),
        ("Why is Parquet faster than CSV for analytics?", "Columnar, compressed, column pruning and statistics"),
        ("What is a Kafka consumer group?", "Consumers sharing a topic's partitions; each message to one consumer in the group"),
        ("What is idempotency in pipelines?", "Re-running gives the same result; overwrite or MERGE"),
        ("State one right of a data principal under the DPDP Act.", "Access, correction, erasure, grievance redressal, nominate"),
        ("What is a shuffle in Spark?", "Moving rows across executors so equal keys meet; costly disk + network"),
        ("Expand HDFS and YARN.", "Hadoop Distributed File System; Yet Another Resource Negotiator")],
    5: [("Explain the CAP theorem with one CP and one AP example.", "Definitions, partition forces a choice, payments CP, feeds/counters AP"),
        ("Compare row and columnar file formats with examples.", "CSV/Avro vs Parquet/ORC; access pattern, compression, schema"),
        ("Explain partitioning and sharding. How does consistent hashing help?", "Split data by key; mod-N moves most keys; ring moves ~1/N"),
        ("Describe the Hadoop ecosystem components and their roles.", "HDFS, YARN, MapReduce, Hive, HBase, Sqoop/Flume, Oozie; Spark"),
        ("Compare data warehouse, data lake and lakehouse.", "Schema, cost, users, ACID, examples, when to use"),
        ("Explain batch vs stream processing with Indian examples.", "Daily settlement vs UPI fraud checks; latency, tools"),
        ("What are the six data quality dimensions? Give a check for each.", "Accuracy, completeness, consistency, timeliness, validity, uniqueness"),
        ("Explain the medallion architecture.", "Bronze raw, silver clean, gold business; quality and reprocessing")],
    10: [("Design a data pipeline for a food-delivery company's daily revenue dashboard.", "Requirements, estimates, ingest, bronze/silver/gold, Airflow, quality, idempotency, cost, governance"),
         ("Explain how a system like IRCTC Tatkal can handle a sudden spike. Include calculations.", "Peak TPS from published figures, waiting room, caching, rate limits, consistency for seats, data platform"),
         ("Explain big data on the cloud: services, cost meters and data residency.", "AWS/Azure/GCP map, serverless vs provisioned, FinOps, egress, RBI residency"),
         ("Describe replication and consistency in distributed databases with diagrams.", "Leader-follower, quorum R+W>N, failover, eventual vs strong consistency")],
}
PLAN = [(2, 5, "Section A: answer all (2 marks each)"),
        (5, 4, "Section B: answer all (5 marks each)"),
        (10, 2, "Section C: answer both (10 marks each)")]

rnd = random.Random(SEED)
total, qn = 0, 1
print(f"BIG DATA FUNDAMENTALS · PRACTICE PAPER (seed {SEED})   Time: 2 hours   Max marks: 50\n")
for marks, count, title in PLAN:
    print(title)
    for q, hint in rnd.sample(BANK[marks], count):
        print(f"  Q{qn}. {q}  [{marks}]")
        if SHOW_KEY:
            print(f"       key: {hint}")
        total += marks
        qn += 1
    print()
print(f"Total: {total} marks · {qn - 1} questions")
print(f"Suggested time: {(2 * 60 - 10) * 10 // total} min per 10 marks, plus 10 min to revise")
