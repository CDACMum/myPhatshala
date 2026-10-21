import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-careers', lesson='01-data-engineer-vs-data-analyst-vs-data-scientist', n='6.1',
    module_label='Module 6 · Careers',
    title='Data engineer vs data analyst vs data scientist',
    desc='Data engineer, data analyst and data scientist compared: what each does, skills and tools, a day in the life, career paths, adjacent roles (analytics engineer, ML engineer), indicative 2026 salary ranges in India, and how to choose. Beginner to Advanced, real-time scenarios, Python tools to test your fit, quiz and interview questions.',
    og_desc='Three data careers, one platform. See a real day for each role, compare skills and growth paths, and run a program that matches your skills to job descriptions.',
    minutes=25, level='Beginner → Advanced',
    lead='All three job posts ask for SQL and Python, yet the jobs are very different. The <b>data engineer</b> makes sure data arrives correct and on time, the <b>data analyst</b> explains what happened, and the <b>data scientist</b> predicts what will happen next. Follow all three through one working day, watch them handle a live incident, compare their skills and career paths, and find out which role your skills match today.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Skill matcher for your PC'],
)

RUN = dict(
    heading='Which role fits you? A tiny quiz engine',
    intro='<p>Each statement adds points to one or more roles. Change the <code>answers</code> to match yourself (True if the statement describes you) and run it. Then try the challenges: classify real job-description lines, find your skill gap, and plan a team.</p>',
    code='''statements = {
    "I enjoy building things that run automatically every night": {"engineer": 2},
    "I like explaining numbers to people in simple words":        {"analyst": 2},
    "Statistics and probability interest me":                     {"scientist": 2, "analyst": 1},
    "I like fixing things when they break":                       {"engineer": 2},
    "I enjoy making charts and dashboards":                       {"analyst": 2},
    "I want to predict the future from past data":                {"scientist": 2},
    "Linux, servers and cloud sound exciting":                    {"engineer": 2},
    "I like running experiments to test ideas":                   {"scientist": 2},
}
answers = [True, False, False, True, False, True, True, False]   # change these!

scores = {"engineer": 0, "analyst": 0, "scientist": 0}
for (statement, points), yes in zip(statements.items(), answers):
    if yes:
        for role, p in points.items():
            scores[role] += p

for role, s in sorted(scores.items(), key=lambda x: -x[1]):
    print(f"{role:9} {'#' * s} {s}")
print("Best match today:", max(scores, key=scores.get))
''',
    anno=[
        ('statements = {...}', 'A dictionary of dictionaries: each statement maps to the roles it points towards and how strongly.'),
        ('zip(statements.items(), answers)', '<code>zip</code> pairs each statement with your True/False answer, in order.'),
        ("'#' * s", 'Multiplying a string repeats it: a quick text bar chart.'),
        ('max(scores, key=scores.get)', 'The role with the highest score. A match today is not destiny; skills change with learning.'),
    ],
    tasks=[
        dict(label='1 · Role quiz', hint='Press <b>Run</b>, then change the <code>answers</code> to describe yourself honestly. Add a statement of your own, like “I enjoy writing SQL queries” worth 1 point for all three roles.', code=None),
        dict(label='2 · Read a job post', hint='This classifies lines from a job post by counting role keywords. Paste lines from a real job post you found and see which role it really is, whatever its title says.',
             code='''keywords = {
    "engineer": ["pipeline", "spark", "kafka", "airflow", "etl", "cloud", "streaming"],
    "analyst": ["dashboard", "power bi", "tableau", "excel", "report", "stakeholder"],
    "scientist": ["machine learning", "model", "statistics", "a/b test", "prediction"],
}
job_post = """Build ETL pipelines with Spark and Airflow on cloud.
Create reports for stakeholders. Exposure to streaming with Kafka.""".lower()

counts = {role: sum(job_post.count(k) for k in words) for role, words in keywords.items()}
print(counts)
print("This post is mostly a", max(counts, key=counts.get), "role")
'''),
        dict(label='3 · Skill gap', hint='Set operations show what you already have and what to learn next. Change <code>target</code> to "scientist" or "analyst".',
             code='''needed = {
    "engineer": {"python", "sql", "spark", "airflow", "kafka", "linux", "cloud", "git"},
    "analyst": {"sql", "excel", "power bi", "statistics", "communication"},
    "scientist": {"python", "sql", "statistics", "machine learning", "git", "pandas"},
}
my_skills = {"python", "sql", "excel", "git"}
target = "engineer"

have = needed[target] & my_skills
gap = needed[target] - my_skills
print(f"For {target}: you have {len(have)}/{len(needed[target])}")
print("Learn next:", sorted(gap))
'''),
        dict(label='4 · Plan a team (advanced)', hint='A startup estimates weekly work hours by type. How many people of each role does it need (40 hours/week each)? Change the hours as the company grows.',
             code='''import math
weekly_hours = {"pipelines & platform": 70, "reports & dashboards": 55, "models & experiments": 30}
role_for = {"pipelines & platform": "engineer", "reports & dashboards": "analyst",
            "models & experiments": "scientist"}

team = {}
for work, hours in weekly_hours.items():
    team[role_for[work]] = math.ceil(hours / 40)
print(team, "| total people:", sum(team.values()))
'''),
        dict(label='5 · Learning plan', hint='A 12-week plan from a list of topics with estimated weeks. Reorder the topics for your target role, or change the weekly study hours.',
             code='''plan = [("SQL (joins, group by, windows)", 3), ("Python + pandas", 3),
        ("Spark basics", 2), ("Airflow + one cloud", 2), ("Portfolio project", 2)]
week = 1
for topic, weeks in plan:
    print(f"Weeks {week:>2}-{week + weeks - 1:>2}: {topic}")
    week += weeks
print("Total:", week - 1, "weeks")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: match your skills to job descriptions',
    intro='<p>Put your real skills in <code>my_skills</code>, paste real job descriptions you find online into <code>job_descriptions</code>, and run. The program shows how well you match each one and which skills to learn next. Save it as <code>jd_matcher.py</code>.</p>',
    items=[
        dict(title='How close are you to each role?', file='jd_matcher.py',
             cmd=open(os.path.join(HERE, 'jd_matcher.py')).read() + '\n# In a terminal:  python jd_matcher.py',
             output=open(os.path.join(HERE, 'jd_matcher.out')).read(),
             note='Recorded from a real run with the sample skills and job descriptions above; your output will match until you change them. A keyword match is a rough guide: real job posts use different words for the same skill, so extend the vocabulary list as you read more posts.'),
    ],
)

TRACE = dict(
    heading='The role quiz, one line at a time',
    intro='<p>A shorter quiz with three statements. Watch the <code>scores</code> dictionary change only when an answer is True, and watch the inner loop add points to each role a statement mentions.</p>',
    code='''statements = [({"engineer": 2}, True),
              ({"analyst": 2}, False),
              ({"scientist": 2, "analyst": 1}, True)]
scores = {"engineer": 0, "analyst": 0, "scientist": 0}
for points, yes in statements:
    if yes:
        for role, p in points.items():
            scores[role] = scores[role] + p
print(scores)
print("Best match:", max(scores, key=scores.get))
''',
    notes={1: 'Answers :: Each item pairs the points a statement gives with your answer.',
           4: 'Scores :: Everyone starts at zero.',
           (6, 2): 'Skip :: This statement does not describe you, so no points are added.',
           10: 'Result :: The highest score is today\'s best match.'},
)

WORKED_INTRO = 'Four career problems: recognising the work, reading job posts, closing a skill gap and planning a team. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Self-check · roles', title='Whose job is this task?',
         problem='<p>Assign each everyday task to the role that usually owns it.</p>',
         inp='fix a failed nightly load · build a sales dashboard · predict next week\'s demand · add a Kafka topic · explain a drop in KPIs · design an A/B test',
         approach=['Map each task to its owner with a dictionary.',
                   'Group tasks by role.',
                   'Print each role with its tasks.'],
         code='''owner = {"fix a failed nightly load": "engineer", "build a sales dashboard": "analyst",
         "predict next week's demand": "scientist", "add a Kafka topic": "engineer",
         "explain a drop in KPIs": "analyst", "design an A/B test": "scientist"}
by_role = {}
for task, role in owner.items():
    by_role.setdefault(role, []).append(task)
for role, tasks in by_role.items():
    print(f"{role:9}:", "; ".join(tasks))
''', notes={4: 'Group :: A dictionary of lists, one list per role.'},
         tryit='Add “write a SQL query”. Who owns it? (All three!) How would you represent a task with several owners?'),
    dict(level='i', tag='Job search · reading posts', title='Score a job post by role keywords',
         problem='<p>A post titled “Data Analyst” says: <i>Build ETL pipelines in Spark, schedule with Airflow, create one Power BI report.</i> Count keywords for each role to see what the job really is.</p>',
         inp='the job post text',
         approach=['Keep a keyword list per role.',
                   'Count how many keywords from each list appear in the lower-cased post.',
                   'The highest count suggests the real role.'],
         code='''post = "Build ETL pipelines in Spark, schedule with Airflow, create one Power BI report.".lower()
words = {"engineer": ["etl", "pipeline", "spark", "airflow"],
         "analyst": ["power bi", "report", "dashboard"],
         "scientist": ["model", "machine learning", "statistics"]}
score = {}
for role, kws in words.items():
    score[role] = sum(1 for k in kws if k in post)
print(score)
print("Title says analyst; work says", max(score, key=score.get))
''', notes={6: 'Count :: <code>k in post</code> checks whether each keyword appears.'},
         tryit='Titles are often misleading. Try the post: “Data Scientist: build Tableau dashboards and Excel reports.”'),
    dict(level='i', tag='Career plan · skill gap', title='What should I learn first?',
         problem='<p>Your target is data engineering. Each missing skill has a priority (how often it appears in job posts, out of 10). List missing skills, highest priority first.</p>',
         inp='needed with priorities; you have python, sql, git',
         approach=['Store needed skills with priorities in a dictionary.',
                   'Keep only those not in your skills set.',
                   'Sort by priority, highest first.'],
         code='''needed = {"python": 10, "sql": 10, "spark": 8, "airflow": 7, "cloud": 8, "kafka": 6, "git": 7}
have = {"python", "sql", "git"}
missing = {s: p for s, p in needed.items() if s not in have}
for skill, p in sorted(missing.items(), key=lambda x: -x[1]):
    print(f"{skill:8} priority {p}")
''', notes={3: 'Gap :: A dictionary comprehension keeps only missing skills.'},
         tryit='Change <code>have</code> to include “spark” and “cloud”. What becomes your next step?'),
    dict(level='a', tag='Startup · team design', title='How many people of each role?',
         problem='<p>A startup expects these weekly hours: pipelines 95, dashboards 60, models 25. One person works 40 hours a week. Startups with less than a full role of work often combine roles. Show the full-time headcount and any leftover hours.</p>',
         inp='pipelines 95 h, dashboards 60 h, models 25 h',
         approach=['Full-time people = hours // 40.',
                   'Leftover hours = hours % 40, which may be combined into a mixed role.',
                   'Print both for each type of work.'],
         code='''work = {"engineer": 95, "analyst": 60, "scientist": 25}
leftover_total = 0
for role, hours in work.items():
    full, left = divmod(hours, 40)
    leftover_total += left
    print(f"{role:9}: {full} full-time + {left} h left over")
print("Combined leftover hours:", leftover_total, "-> about", round(leftover_total / 40, 1), "more people")
''', notes={4: 'Split :: <code>divmod</code> gives full people and leftover hours in one step.'},
         tryit='The 25 hours of modelling work don\'t justify a full scientist yet. Would you hire an analyst with statistics skills instead?'),
]

QUIZ = [
    dict(q='Beginner: Who mainly builds and maintains data pipelines?', options=['Data analyst', 'Data engineer', 'Data scientist', 'HR manager'], answer=1,
         why='Data engineers build the systems that collect, transform and deliver data.'),
    dict(q='Beginner: “Why did sales drop last Friday?” is mainly a question for the…', options=['Data analyst', 'Data engineer', 'Network administrator', 'UI designer'], answer=0,
         why='Explaining what happened and why is the analyst\'s core work.'),
    dict(q='Beginner: Which role most often builds predictive models?', options=['Data analyst', 'Data scientist', 'Database administrator', 'Web developer'], answer=1,
         why='Data scientists use statistics and machine learning to predict outcomes.'),
    dict(q='Intermediate: Which skill is used daily by all three roles?', options=['Kafka administration', 'SQL', 'Deep learning', 'Graphic design'], answer=1,
         why='SQL is the shared language of data work.'),
    dict(q='Intermediate: Power BI and Tableau are most associated with…', options=['Data engineers', 'Data analysts', 'ML engineers', 'Cloud architects'], answer=1,
         why='They are business-intelligence tools for dashboards and reports, the analyst\'s main deliverables.'),
    dict(q='Intermediate: A dashboard is empty because last night\'s load failed. Who usually fixes it first?', options=['Data scientist', 'Data engineer', 'Business head', 'Marketing'], answer=1,
         why='Pipeline failures are owned by data engineering.'),
    dict(q='Advanced: Which role puts a data scientist\'s model into production and keeps it running?', options=['BI developer', 'ML engineer', 'Data analyst', 'Data steward'], answer=1,
         why='ML engineers specialise in deploying, monitoring and retraining models.'),
    dict(q='Advanced: An analytics engineer mainly…', options=['Designs mobile apps', 'Builds clean, tested data models in the warehouse (often with SQL and dbt)', 'Trains deep learning models', 'Manages office networks'], answer=1,
         why='Analytics engineers sit between analysts and engineers, modelling warehouse data so it can be trusted.'),
]

REVISION = [
    '<b>Engineer</b>: is the data there, correct, on time? → pipelines, lakes, warehouses.',
    '<b>Analyst</b>: what happened and why? → SQL, dashboards, insights.',
    '<b>Scientist</b>: what will happen and what should we do? → models, experiments.',
    'All three use <b>SQL</b>, Git and clear communication; they depend on one another.',
    'In between: <b>analytics engineer</b> (analyst↔engineer), <b>ML engineer</b> (scientist↔engineer), <b>data architect</b>.',
    'Careers move: analyst → analytics/data engineer; analyst → scientist; developer → data engineer.',
    'Pay varies widely by company type, city and skills; check current listings. A real project beats a list of certificates.',
]
FAQ = [
    ('Differentiate the roles of data engineer, data analyst and data scientist.', 'A data engineer builds and maintains the infrastructure and pipelines that deliver reliable data. A data analyst queries and visualises that data to explain business performance and support decisions. A data scientist applies statistics and machine learning to predict outcomes and design experiments. Engineers enable the work of the other two; analysts and scientists turn data into decisions.'),
    ('Why do you want to be a data engineer rather than a data scientist?', 'A good answer is honest and specific: for example, “I enjoy building systems that run reliably and at scale, I like debugging pipelines and working with distributed tools like Spark and Kafka, and I want my work to enable every analyst and scientist in the company.” Back it with a project you built.'),
    ('What skills does a fresher need for a data analyst role?', 'Strong SQL (joins, group by, window functions), Excel, one BI tool (Power BI or Tableau), basic statistics (averages, percentages, distributions), and the ability to explain findings clearly. Basic Python is a plus. A portfolio dashboard with clear insights helps a lot.'),
    ('Can a data analyst become a data engineer or data scientist?', 'Yes, and it is common. Towards engineering: deepen Python, learn data modelling, Spark, Airflow, a cloud platform and Git, often via an analytics-engineer role. Towards science: deepen statistics, learn machine learning with Python, and practise experiments on real problems.'),
    ('What is the difference between a data scientist and an ML engineer?', 'A data scientist explores data, builds and evaluates models, and interprets results. An ML engineer takes models to production: building serving systems, feature pipelines, monitoring and retraining at scale. In smaller companies one person may do both.'),
]

PRACTICE_INTRO = 'Career-flavoured coding exercises. The last two are planning decisions a data team lead makes.'
PROBLEMS = [
    dict(level='easy', title='Count tasks per role', stmt='Count how many tasks each role has in the list.', inp='engineer, analyst, engineer, scientist, analyst, engineer',
         code='''tasks = ["engineer", "analyst", "engineer", "scientist", "analyst", "engineer"]
counts = {}
for r in tasks:
    counts[r] = counts.get(r, 0) + 1
print(counts)
''', explain='The dictionary counter pattern, again. You will use it in every data role.'),
    dict(level='easy', title='Shared skills', stmt='Print the skills common to both job posts.', inp='analyst: sql, excel, power bi · engineer: sql, python, spark',
         code='''analyst = {"sql", "excel", "power bi"}
engineer = {"sql", "python", "spark"}
print("Common:", analyst & engineer)
''', explain='Set intersection (&): SQL is the overlap.'),
    dict(level='easy', title='Match percentage', stmt='A job needs 8 skills and you have 5 of them. Print your match as a percentage.', inp='5 of 8',
         code='print(round(5 / 8 * 100), "% match")\n', explain='A simple, honest progress measure for job preparation.'),
    dict(level='medium', title='Missing skills', stmt='Print the skills a data scientist post needs that you don\'t have yet, in alphabetical order.', inp='needs: python, sql, statistics, machine learning · have: python, sql',
         code='''needs = {"python", "sql", "statistics", "machine learning"}
have = {"python", "sql"}
print(sorted(needs - have))
''', explain='Set difference (−) shows the gap; <code>sorted</code> makes the output stable.'),
    dict(level='medium', title='Title vs content', stmt='Given keyword counts from a post, print whether the title matches the content.', inp='title analyst · counts engineer 4, analyst 1, scientist 0',
         code='''title = "analyst"
counts = {"engineer": 4, "analyst": 1, "scientist": 0}
real = max(counts, key=counts.get)
print("Matches title" if real == title else f"Real role: {real}")
''', explain='Read job descriptions, not just titles; companies use titles differently.'),
    dict(level='advanced', title='Rank roles for a profile', stmt='Given your skill depth (1–5) and each role\'s required depth, score each role as the sum of the smaller of the two values, and rank the roles.', inp='you: sql 4, python 3, stats 4, cloud 1',
         code='''me = {"sql": 4, "python": 3, "stats": 4, "cloud": 1}
roles = {"engineer": {"sql": 4, "python": 4, "stats": 1, "cloud": 4},
         "analyst": {"sql": 5, "python": 2, "stats": 3, "cloud": 1},
         "scientist": {"sql": 3, "python": 5, "stats": 5, "cloud": 2}}
fit = {r: sum(min(me[s], need) for s, need in req.items()) for r, req in roles.items()}
for r, f in sorted(fit.items(), key=lambda x: -x[1]):
    print(r, f)
''', explain='Using <code>min</code> means extra depth beyond what the role needs doesn\'t add points.'),
    dict(level='advanced', title='Weeks to job-ready', stmt='Each missing skill takes a number of weeks; you study 10 hours a week and each week of the estimate assumes 10 hours. If you can study 15 hours, how many weeks will the plan take?', inp='spark 3, airflow 2, cloud 3, kafka 2 (weeks at 10 h)',
         code='''plan = {"spark": 3, "airflow": 2, "cloud": 3, "kafka": 2}
hours_needed = sum(plan.values()) * 10
print(round(hours_needed / 15, 1), "weeks at 15 hours a week")
''', explain='Convert to hours first, then divide by your real weekly capacity.'),
    dict(level='business', title='First data hire', stmt='A startup has 3 data needs with weekly hours: dashboards 30, pipelines 25, models 5. Print which role should be hired first (the one with most hours).', inp='dashboards 30, pipelines 25, models 5',
         code='''needs = {"analyst": 30, "engineer": 25, "scientist": 5}
print("Hire first:", max(needs, key=needs.get))
''', explain='Many startups hire an analyst or analytics engineer first, and a scientist only when there is enough clean data to model.'),
    dict(level='business', title='Team cost (illustrative)', stmt='Monthly cost per person: analyst Rs 60,000, engineer Rs 90,000, scientist Rs 1,10,000 (illustrative). Print the cost of a team of 2 analysts, 2 engineers and 1 scientist.', inp='2 · 2 · 1',
         code='''cost = {"analyst": 60000, "engineer": 90000, "scientist": 110000}
team = {"analyst": 2, "engineer": 2, "scientist": 1}
print("Monthly team cost: Rs", sum(cost[r] * n for r, n in team.items()))
''', explain='Team planning combines workload and cost; the numbers are examples only.'),
]

SCN_INTRO = 'Career and teamwork questions asked in data interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
