import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-careers', lesson='02-roadmap-portfolio-certifications-resume', n='6.2',
    module_label='Module 6 · Careers',
    title='Data engineering roadmap, portfolio, certifications and resume',
    desc='A practical data engineering career plan for India: a skills roadmap from SQL and Python to Spark, Airflow, Kafka, cloud and lakehouse, portfolio project ideas with Indian data, how to build a GitHub repository reviewers trust, which certifications to choose (AWS DEA-C01, Microsoft DP-700, Google Professional Data Engineer, Databricks, Snowflake, Confluent), and how to write a one-page resume with quantified bullets. Animations and a roadmap planner and resume-bullet scorer for your PC.',
    og_desc='Badges or evidence? Build your data engineering roadmap, a portfolio project and a resume that gets shortlisted.',
    minutes=30, level='Beginner → Advanced',
    lead='Long lists of tools and badges rarely get anyone hired. Projects with numbers do. In this lesson you build a <b>roadmap from your own skills and hours</b>, choose the <b>certification</b> that matches the jobs you want, design a <b>portfolio project</b> reviewers trust, and rewrite resume bullets from vague duties into results, with a program that scores them.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Roadmap planner for your PC'],
)

RUN = dict(
    heading='Plan your roadmap from your own skills',
    intro='<p>Rate yourself from 0 to 3 in each skill. The program works out the hours you still need and the weeks it will take at your pace. Then try the challenges: job-post keyword counts, bullet checks, application tracking and certification choices.</p>',
    code='''skills = {            # skill: (hours from zero, your level 0-3)
    "SQL": (60, 2),
    "Python": (60, 2),
    "Spark": (70, 0),
    "Airflow": (30, 0),
    "Cloud": (50, 1),
    "Project": (60, 0),
}
hours_per_week = 10
total = 0
for skill, (hours, level) in skills.items():
    need = round(hours * (3 - level) / 3)
    total += need
    print(f"{skill:8}: {need:3} h")
print(f"total {total} h -> {total / hours_per_week:.0f} weeks at {hours_per_week} h/week")
''',
    anno=[
        ('    need = round(hours * (3 - level) / 3)', 'Level 3 means nothing left to learn; level 0 means the full hours.'),
        ('hours_per_week = 10', 'Be honest: a plan based on real hours gives a real date.'),
    ],
    tasks=[
        dict(label='1 · Your plan', hint='Press <b>Run</b>. Change the levels to your own, and try 6 and 15 hours a week.', code=None),
        dict(label='2 · Count skills in job posts', hint='Paste skills from job posts you collect. The most common ones are what to learn first.',
             code='''from collections import Counter
posts = [["SQL", "Python", "Spark", "AWS"], ["SQL", "Airflow", "Spark", "Azure"],
         ["SQL", "Python", "Kafka", "Spark"], ["SQL", "dbt", "Snowflake", "Python"],
         ["Python", "Spark", "AWS", "Airflow"]]
print(Counter(s for p in posts for s in p).most_common(5))
'''),
        dict(label='3 · Check a resume bullet', hint='Does the bullet start with an action and contain a number? Try your own bullets.',
             code='''verbs = ("Built", "Reduced", "Designed", "Automated", "Migrated", "Improved")
for b in ["Responsible for ETL jobs", "Automated daily sales load with Airflow, saving 2 hours a day"]:
    ok_verb = b.split()[0] in verbs
    ok_num = any(c.isdigit() for c in b)
    print(f"{b[:45]:45} verb={ok_verb} number={ok_num}")
'''),
        dict(label='4 · Application tracker', hint='Track applications and see your reply rate by channel. Which channel should you use more?',
             code='''apps = [("referral", True), ("portal", False), ("portal", False), ("referral", True),
        ("portal", True), ("career page", False), ("referral", False), ("portal", False)]
for ch in sorted({c for c, _ in apps}):
    replies = [r for c, r in apps if c == ch]
    print(f"{ch:12}: {sum(replies)}/{len(replies)} replies")
'''),
        dict(label='5 · Pick a certification (advanced)', hint='Score certifications by how often their platform appears in your job posts. Change the counts to match your posts.',
             code='''platform_counts = {"AWS": 9, "Azure": 6, "GCP": 2, "Databricks": 7, "Snowflake": 3}
certs = {"AWS": "AWS Certified Data Engineer - Associate", "Azure": "Fabric Data Engineer Associate (DP-700)",
         "GCP": "Professional Data Engineer", "Databricks": "Databricks Data Engineer Associate",
         "Snowflake": "SnowPro Core"}
best = max(platform_counts, key=platform_counts.get)
print("most requested:", best, "->", certs[best])
'''),
        dict(label='6 · Portfolio checklist (advanced)', hint='Score your project repository. Mark what you have and see what to add next.',
             code='''have = {"README with diagram": True, "one-command setup": False, "tests": True,
        "CI": False, "data quality checks": True, "results with numbers": False}
done = sum(have.values())
print(f"{done}/{len(have)} done; next:", [k for k, v in have.items() if not v])
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: roadmap planner and resume-bullet scorer',
    intro='<p>This program plans a 10-skill data engineering roadmap from your self-ratings and weekly hours, then scores resume bullets for an action verb, a named tool, a number and an impact. Edit the levels, hours and bullets to your own and run it again. Save it as <code>career_planner.py</code>.</p>',
    items=[
        dict(title='Your weeks, and your bullets', file='career_planner.py',
             cmd=open(os.path.join(HERE, 'career_planner.py')).read() + '\n# In a terminal:  python career_planner.py',
             output=open(os.path.join(HERE, 'career_planner.out')).read(),
             note='Recorded from a real run with Python 3.13 (standard library only). The hour estimates are rough guides for focused study; adjust them to your pace. The bullet scorer is a simple checklist, not a replacement for feedback from an experienced engineer.'),
    ],
)

TRACE = dict(
    heading='Turning skills into weeks',
    intro='<p>Three skills with your current level are converted into hours still needed and a running week count.</p>',
    code='''plan = [("SQL", 60, 2), ("Spark", 70, 0), ("Airflow", 30, 1)]
per_week = 10
week = 0
for skill, hours, level in plan:
    need = hours * (3 - level) // 3
    week += -(-need // per_week)
    print(skill, need, "h, done by week", week)
''',
    notes={5: 'Gap :: Only the part you don’t know yet.', 6: 'Weeks :: Ceiling division: 25 hours at 10 a week needs 3 weeks.'},
)

WORKED_INTRO = 'Four career-planning calculations. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Planning · dates', title='When will I be job-ready?',
         problem='<p>Kabir needs 367 hours of study and can do 12 hours a week, starting on 1 November 2026. On which date does he finish?</p>',
         inp='367 hours, 12 h/week, start 2026-11-01',
         approach=['Weeks = ceiling of hours ÷ hours per week.',
                   'Add that many weeks to the start date.',
                   'Print the date.'],
         code='''from datetime import date, timedelta
weeks = -(-367 // 12)
finish = date(2026, 11, 1) + timedelta(weeks=weeks)
print(weeks, "weeks -> finish on", finish)
''', notes={2: 'Ceiling :: A partial week still counts as a week.'},
         tryit='What date if he manages 15 hours a week? And 8?'),
    dict(level='i', tag='Job search · keywords', title='Skills your resume is missing',
         problem='<p>Compare the skills in a job description with the skills on a resume. Print what matches and what is missing.</p>',
         inp='job skills set, resume skills set',
         approach=['Store both as sets.',
                   'Intersection = matching skills.',
                   'Difference = skills to add (only if you really have them) or learn.'],
         code='''job = {"sql", "python", "spark", "airflow", "aws", "data modelling"}
resume = {"sql", "python", "pandas", "spark", "excel"}
print("match  :", sorted(job & resume))
print("missing:", sorted(job - resume))
print(f"coverage: {len(job & resume) / len(job):.0%}")
''', notes={3: 'Intersection :: Words both share.', 4: 'Difference :: What the job wants that the resume lacks.'},
         tryit='Add a second job post and find skills missing in both.'),
    dict(level='i', tag='Resume · scoring', title='Rank bullets by strength',
         problem='<p>Score each bullet: +1 action verb, +1 number, +1 named tool. Print bullets from strongest to weakest.</p>',
         inp='3 bullets',
         approach=['Write a score function with three checks.',
                   'Sort bullets by score, highest first.',
                   'Rewrite the weakest first.'],
         code='''verbs, tools = {"built", "reduced", "automated"}, {"spark", "airflow", "sql", "kafka"}
def score(b):
    w = b.lower().replace(",", "").split()
    return (w[0] in verbs) + any(c.isdigit() for c in b) + bool(tools & set(w))
bullets = ["Helped team with reports", "Built Kafka consumer for 5k events/s", "Automated SQL checks"]
for b in sorted(bullets, key=score, reverse=True):
    print(score(b), b)
''', notes={4: 'Score :: True counts as 1 when added.'},
         tryit='Add a fourth check for impact words like “reduced”, “saved” or “%”.'),
    dict(level='a', tag='Job search · funnel', title='How many applications do I need?',
         problem='<p>From past data: 12% of applications get a recruiter call, 45% of calls reach a technical round, 30% of technical rounds lead to an offer. How many applications for an expected 2 offers? How does that change if referrals double the call rate?</p>',
         inp='12% → 45% → 30%, target 2 offers',
         approach=['Offer rate per application = product of the stage rates.',
                   'Applications = target ÷ offer rate, rounded up.',
                   'Repeat with a 24% call rate.'],
         code='''import math
def needed(call, tech=0.45, offer=0.30, target=2):
    rate = call * tech * offer
    return rate, math.ceil(target / rate)
for name, call in [("portals only", 0.12), ("with referrals", 0.24)]:
    rate, apps = needed(call)
    print(f"{name:15}: {rate:.2%} per application -> {apps} applications")
''', notes={3: 'Funnel :: Each stage keeps only a fraction of candidates.'},
         tryit='Improving your technical round from 45% to 60% through practice: how many applications now?'),
]

QUIZ = [
    dict(q='For a fresher data engineer, what usually carries the most weight on a resume?', options=['A long list of tools', 'Many certificates', 'Documented projects with clear results and links', 'A colourful design'], answer=2,
         why='Projects are evidence; interviewers can open them and ask about decisions.'),
    dict(q='Which skill appears in almost every data engineering interview?', options=['Photoshop', 'SQL', 'Assembly language', 'Mobile app development'], answer=1,
         why='SQL (joins, aggregation, window functions) is tested in nearly every data engineering hiring process.'),
    dict(q='Which bullet is strongest?', options=['Responsible for ETL pipelines', 'Worked with Spark and other tools', 'Reduced a PySpark job from 3 h to 25 min by fixing skewed joins', 'Hard-working and passionate about data'], answer=2,
         why='It has an action, a tool, a method and a measurable result.'),
    dict(q='Microsoft’s current data engineering certification for Fabric is:', options=['DP-203', 'DP-700', 'AZ-900', 'PL-300'], answer=1,
         why='DP-700 (Fabric Data Engineer Associate); DP-203 was retired in 2025. PL-300 is for Power BI analysts.'),
    dict(q='What is the AWS associate-level data engineering exam?', options=['AWS Certified Data Engineer – Associate (DEA-C01)', 'AWS Cloud Practitioner', 'AWS Big Data Specialty', 'AWS Developer – Professional'], answer=0,
         why='DEA-C01 replaced the older Big Data / Data Analytics specialty exams.'),
    dict(q='When is the best time to take a platform certification?', options=['Before learning anything', 'After building something on that platform, when it matches target jobs', 'Only after 10 years', 'Never'], answer=1,
         why='Hands-on experience makes the exam easier and the certificate meaningful.'),
    dict(q='Which makes a portfolio repository most trustworthy?', options=['Many notebooks with no README', 'A README with architecture and run steps, one-command setup, tests and results', 'Only screenshots', 'A very long commit history of typo fixes'], answer=1,
         why='Reviewers want to understand, run and trust the project quickly.'),
    dict(q='What does STAR stand for in behavioural interviews?', options=['Skill, Tool, Attitude, Result', 'Situation, Task, Action, Result', 'Start, Test, Analyse, Repeat', 'Story, Theory, Answer, Review'], answer=1,
         why='A clear structure for describing what you did and what happened.'),
]

REVISION = [
    'Roadmap: SQL, Python, Linux/Git, modelling → Spark → Airflow/dbt → Kafka → one cloud → lakehouse → project.',
    'Study 20 job posts first; learn what repeats; plan with honest hours per week.',
    'Evidence beats lists: 2–3 end-to-end projects with README, diagram, tests, results and links.',
    'Bullets = action + tool + scale + result; one page; only what you can explain in depth.',
    'Certs: AWS DEA-C01 · Microsoft DP-700 (DP-203 retired) · Google Professional Data Engineer · Databricks · SnowPro · Confluent.',
    'Take a certification after hands-on work on that platform, matched to target jobs.',
    'Apply with referrals, track a funnel, prepare SQL, coding, design and STAR stories.',
]
FAQ = [
    ('How do I become a data engineer as a fresher in India?', 'Learn SQL and Python thoroughly, then data modelling, Spark, an orchestrator such as Airflow, the basics of Kafka and one cloud platform. Build two or three end-to-end projects on GitHub with clear documentation, write a one-page resume with quantified bullets, apply through referrals, job portals and company career pages, and practise SQL, coding and pipeline design questions.'),
    ('Which certification is best for data engineers?', 'The best one matches the jobs you target: AWS Certified Data Engineer – Associate for AWS roles, Microsoft Certified: Fabric Data Engineer Associate (DP-700) for Azure and Fabric, Google Cloud Professional Data Engineer for GCP, and Databricks Certified Data Engineer Associate for Spark and lakehouse roles. Certifications help most when combined with projects on the same platform.'),
    ('What projects should a data engineer have in a portfolio?', 'End-to-end projects that ingest real or realistic data, store it in layers (bronze, silver, gold), transform it with Spark or dbt, run data quality checks, are orchestrated by Airflow, and serve results in a dashboard or table. Include a README with problem, architecture diagram, run instructions, results and limitations; add tests and CI if possible. Examples: payments streaming with Kafka and Spark, public transport punctuality, air quality monitoring, e-commerce clickstream funnels.'),
    ('How long does it take to become a data engineer?', 'With prior programming knowledge, a focused learner studying 10–15 hours a week can usually become job-ready in about 6–9 months; full-time study can shorten that. The time depends on your starting skills, so plan from an honest self-assessment and measure progress with finished projects.'),
    ('How should a data engineer write a resume?', 'Keep it to one page for freshers, with a header including GitHub and LinkedIn links, projects near the top, and bullets written as action plus tool plus scale plus result. List only tools you can discuss in depth, add relevant certifications, avoid duties and generic adjectives, and tailor keywords to each job description truthfully.'),
]

PRACTICE_INTRO = 'Small career-planning programs. The last two are business-style tasks.'
PROBLEMS = [
    dict(level='easy', title='Hours to weeks', stmt='You need 120 hours and study 9 hours a week. Print the number of weeks (round up).', inp='120 h, 9 h/week',
         code='''print(-(-120 // 9))
''', explain='Ceiling division: -(-a // b).'),
    dict(level='easy', title='Most common skill', stmt='Print the most common skill in ["SQL", "Spark", "SQL", "Python", "SQL", "Spark"].', inp='list',
         code='''from collections import Counter
print(Counter(["SQL", "Spark", "SQL", "Python", "SQL", "Spark"]).most_common(1))
''', explain='Counting skills across job posts shows what to learn first.'),
    dict(level='easy', title='Has a number?', stmt='Print whether "Built 3 Airflow DAGs" contains a digit.', inp='bullet',
         code='''print(any(c.isdigit() for c in "Built 3 Airflow DAGs"))
''', explain='Numbers make bullets concrete.'),
    dict(level='medium', title='Skill coverage', stmt='Job needs {sql, python, spark, aws}; you have {sql, python, excel}. Print coverage as a percentage.', inp='two sets',
         code='''job, me = {"sql", "python", "spark", "aws"}, {"sql", "python", "excel"}
print(f"{len(job & me) / len(job):.0%}")
''', explain='Set intersection finds matching skills.'),
    dict(level='medium', title='Reply rate', stmt='You sent 40 applications and got 6 replies. Print the reply rate.', inp='6/40',
         code='''print(f"{6 / 40:.0%}")
''', explain='Track your funnel to see what works.'),
    dict(level='advanced', title='Funnel offers', stmt='60 applications, 15% calls, 50% pass technical, 35% offers. Print expected offers.', inp='as given',
         code='''print(round(60 * 0.15 * 0.50 * 0.35, 2))
''', explain='Multiply through each stage of the funnel.'),
    dict(level='advanced', title='Weakest bullet', stmt='Scores {"A": 2, "B": 4, "C": 1}. Print the bullet to rewrite first.', inp='dict',
         code='''s = {"A": 2, "B": 4, "C": 1}
print(min(s, key=s.get))
''', explain='Improve the weakest evidence first.'),
    dict(level='business', title='Certification return', stmt='A certification costs US$150 (about Rs 13,000) and 40 hours of study. If it raises your interview rate from 10% to 13% across 50 applications, print the extra interviews expected.', inp='50 apps, 10% → 13%',
         code='''print(round(50 * (0.13 - 0.10), 1), "extra interviews")
''', explain='Weigh the cost of a credential against what it actually changes.'),
    dict(level='business', title='Study budget', stmt='You can study 2 hours on weekdays and 5 hours on weekend days. Print hours per week and weeks for a 367-hour plan.', inp='2×5 + 5×2',
         code='''h = 2 * 5 + 5 * 2
print(h, "h/week,", -(-367 // h), "weeks")
''', explain='A realistic weekly budget turns a plan into a date.'),
]

SCN_INTRO = 'Career questions students and early-career engineers ask. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
