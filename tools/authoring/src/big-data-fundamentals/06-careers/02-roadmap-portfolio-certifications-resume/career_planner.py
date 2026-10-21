"""Plan a data engineering learning roadmap from your current skills,
then score resume bullets the way a busy reviewer would."""
import re

# 1) skills: (hours needed from zero, your level 0-3)
skills = {
    "SQL (joins, windows, CTEs)": (60, 2),
    "Python for data": (60, 2),
    "Linux, Git, shell": (25, 1),
    "Data modelling (star schema)": (30, 0),
    "Spark / PySpark": (70, 0),
    "Airflow orchestration": (30, 0),
    "Kafka basics": (30, 0),
    "One cloud (storage, Spark, warehouse)": (50, 0),
    "Lakehouse: Delta / Iceberg, dbt": (40, 0),
    "Portfolio project end to end": (60, 0),
}
HOURS_PER_WEEK = 12
week, plan = 1, []
for skill, (hours, level) in skills.items():
    need = round(hours * (3 - level) / 3)
    if need == 0:
        continue
    weeks = -(-need // HOURS_PER_WEEK)          # ceiling division
    plan.append((week, week + weeks - 1, skill, need))
    week += weeks
print(f"Roadmap at {HOURS_PER_WEEK} hours a week:")
for start, end, skill, need in plan:
    print(f"  weeks {start:2}-{end:2}: {skill:38} ({need} h)")
print(f"Total: {sum(p[3] for p in plan)} hours, about {week - 1} weeks ({(week - 1) / 4.3:.1f} months)")

# 2) resume bullets: action verb + tool + number + impact
VERBS = ("built", "designed", "reduced", "migrated", "automated", "optimised", "optimized", "created", "led", "improved")
TOOLS = ("spark", "pyspark", "airflow", "kafka", "sql", "python", "dbt", "delta", "parquet", "aws", "azure", "gcp", "bigquery", "s3")
def score(bullet):
    b = bullet.lower()
    checks = {
        "action verb": b.split()[0] in VERBS,
        "tool named": any(t in re.findall(r"[a-z0-9]+", b) for t in TOOLS),
        "number": bool(re.search(r"\d", b)),
        "impact": any(w in b for w in ("reduc", "faster", "saving", "cut", "improv", "%", "from")),
    }
    return sum(checks.values()), [k for k, ok in checks.items() if not ok]

bullets = [
    "Worked on data pipelines using various tools.",
    "Responsible for Spark jobs.",
    "Built an Airflow DAG that loads 2 lakh orders a day into Delta tables.",
    "Reduced a nightly PySpark job from 3 h to 25 min by fixing skewed joins and partitioning by date.",
]
print("\nResume bullet scores (out of 4):")
for b in bullets:
    s, missing = score(b)
    print(f"  {s}/4  {b}")
    if missing:
        print(f"        missing: {', '.join(missing)}")
