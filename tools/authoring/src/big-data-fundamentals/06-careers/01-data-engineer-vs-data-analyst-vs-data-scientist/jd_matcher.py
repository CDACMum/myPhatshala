# Compare YOUR skills with three typical job descriptions and see the gap.
my_skills = {"python", "sql", "excel", "statistics", "power bi", "git"}

job_descriptions = {
    "Data Analyst": """Strong SQL and Excel. Build dashboards in Power BI or Tableau.
        Basic statistics. Communicate insights to business teams. Python is a plus.""",
    "Data Engineer": """Python and SQL. Build batch and streaming pipelines with Spark and Kafka.
        Orchestrate with Airflow. Cloud (AWS or Azure), Linux, Git, data modelling.""",
    "Data Scientist": """Python, SQL, statistics and machine learning (scikit-learn).
        Feature engineering, experiment design, model evaluation. Git; Spark is a plus.""",
}
vocabulary = ["python", "sql", "excel", "power bi", "tableau", "statistics", "spark", "kafka",
              "airflow", "cloud", "linux", "git", "machine learning", "data modelling",
              "communicate", "dashboards", "feature engineering", "experiment design"]

for role, text in job_descriptions.items():
    text = text.lower()
    wanted = {skill for skill in vocabulary if skill in text}
    have = wanted & my_skills
    missing = sorted(wanted - my_skills)
    score = round(len(have) / len(wanted) * 100)
    print(f"{role:15} match {score:>3}%  ({len(have)}/{len(wanted)} skills)")
    print(f"{'':15} learn next: {', '.join(missing[:4])}")
