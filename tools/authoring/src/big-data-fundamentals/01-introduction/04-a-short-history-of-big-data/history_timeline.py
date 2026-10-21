"""Print the big data timeline as a text chart, grouped by era.
Change BORN to your birth year to see how old you were at each milestone."""
BORN = 2006
NOW = 2026

milestones = [
    (1997, "Term 'big data' used by NASA researchers", "Before Hadoop"),
    (2001, "Doug Laney describes the 3 Vs", "Before Hadoop"),
    (2003, "Google File System paper", "Google papers"),
    (2004, "MapReduce paper", "Google papers"),
    (2006, "Bigtable paper; Hadoop starts; Amazon S3", "Google papers"),
    (2008, "Hadoop top-level Apache project; Hive, Cassandra", "Ecosystem"),
    (2011, "Kafka open-sourced by LinkedIn", "Ecosystem"),
    (2014, "Spark 1.0, Apache top-level project", "Ecosystem"),
    (2016, "UPI launched; cheap 4G in India", "Cloud and mobile"),
    (2019, "Delta Lake open-sourced", "Lakehouse"),
    (2023, "India's DPDP Act passed", "Lakehouse"),
]

era = None
for year, event, group in milestones:
    if group != era:
        era = group
        print(f"\n== {era} ==")
    age = year - BORN
    when = f"you were {age}" if age >= 0 else f"{-age} years before you were born"
    bar = "#" * ((year - 1995) // 2)
    print(f"{year} {bar:<16} {event}  ({when})")

span = milestones[-1][0] - milestones[0][0]
print(f"\n{len(milestones)} milestones over {span} years; {NOW - 2003} years since the GFS paper.")
