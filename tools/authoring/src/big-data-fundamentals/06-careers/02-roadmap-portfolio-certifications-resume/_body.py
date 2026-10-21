import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = box(14, 16, 296, 124, 'red') + t(162, 38, 'Kabir’s resume, version 1', 10, 'red', bold=True)
v1 = ['• Worked on data pipelines using various tools', '• Responsible for Spark jobs', '• Skills: Python, SQL, Spark, Kafka, AWS,', '  Azure, GCP, Hadoop, Hive, Flink, …']
sc += ''.join(t(28, 62 + k * 18, s, 8.8, anchor='start') for k, s in enumerate(v1))
sc += arrow(316, 78, 346, 78, 'ink3', 2)
sc += box(352, 16, 274, 124, 'green') + t(489, 38, 'Version 4', 10, 'green', bold=True)
v4 = ['• Reduced a nightly PySpark job from 3 h', '  to 25 min (skew fix, date partitions)', '• Built an Airflow DAG loading 2 lakh', '  orders a day into Delta tables', '• Project: UPI-style payments pipeline ↗']
sc += ''.join(t(366, 58 + k * 16, s, 8.6, anchor='start') for k, s in enumerate(v4))
scene_svg = scene('A weak resume listing vague duties and many tools, compared with a stronger version with specific results, numbers and a project link.', sc,
                  'Hiring teams look for <tspan font-weight="700" class="s-acc">evidence</tspan>, not lists of tool names.')

story = f'''  <div class="story">
    <p class="narration">Kabir’s internship at TiffinGo ends in three months, and the full-time data engineer role will be open to outside candidates too. His friends have long lists of certificates and courses on their resumes. Kabir has a list of every tool he has heard of, two vague bullet points and no projects outside work.</p>

{scene_svg}

K> Sir, should I do five certifications before the interview? Everyone on LinkedIn has a wall of badges.
A> One good certification can help, Kabir, especially for cloud roles. But what gets you shortlisted is <b>evidence</b>: specific results with numbers, and a project an interviewer can open and run.
R> But freshers don’t have results. What do we write?
A> Projects are your results, Riya. “Built a pipeline that ingests 10 lakh rows, checks quality and serves a dashboard, with tests and an architecture diagram” beats “knows Spark” every time.
K> And what should I learn first? There’s so much.
A> A roadmap in order: foundations first (SQL, Python, Linux, Git, modelling), then distributed processing, orchestration, streaming, one cloud and a lakehouse, with a portfolio project tying it together. Today you’ll build that plan for your own hours, fix your resume bullets with a scoring program, and see what a strong portfolio repository looks like.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Your data engineering career plan at three levels
L1> Getting started (0–3 months)
      <ul>
      <li><b>SQL</b> deeply: joins, GROUP BY, window functions, CTEs, query plans. It is in nearly every data engineering interview.</li>
      <li><b>Python</b> for data: files, JSON, CSV, functions, error handling, pandas basics, writing small scripts.</li>
      <li><b>Linux, Git and the command line:</b> navigating servers, shell scripts, branches, pull requests.</li>
      <li><b>Data modelling:</b> normalisation for transaction systems, star schemas (facts and dimensions) for analytics.</li>
      <li>First small project on GitHub with a clear README.</li>
      </ul>
L2> Becoming job-ready (3–8 months)
      <ul>
      <li><b>Distributed processing:</b> Spark (PySpark DataFrames, partitions, joins, shuffles) and file formats (Parquet).</li>
      <li><b>Orchestration:</b> Airflow DAGs, scheduling, retries, backfills; <b>dbt</b> for SQL transformations and tests.</li>
      <li><b>Streaming basics:</b> Kafka topics, partitions, consumer groups; when to use streaming.</li>
      <li><b>One cloud well:</b> its object storage, managed Spark, warehouse and IAM. Optionally one associate-level certification.</li>
      <li><b>Lakehouse:</b> Delta Lake or Iceberg tables, medallion layers, data quality checks.</li>
      <li>An end-to-end portfolio project; a resume with quantified bullets; active applications.</li>
      </ul>
L3> Growing after you are hired
      <ul>
      <li><b>Depth:</b> Spark tuning, cost optimisation, data modelling at scale, streaming with exactly-once semantics.</li>
      <li><b>Engineering practice:</b> testing, CI/CD for data, infrastructure as code (Terraform), observability, code review.</li>
      <li><b>Ownership:</b> data contracts, governance, on-call, design documents and estimating cost and capacity.</li>
      <li><b>Paths:</b> senior/staff data engineer, analytics engineer, platform or streaming engineer, ML/data platform engineer, data architect, engineering manager.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'A <b>career roadmap</b> for data engineering is an ordered plan of skills, projects and credentials leading to employment and growth in roles that design, build and operate data pipelines and platforms. Core competencies include <b>SQL, programming (usually Python), data modelling, distributed processing, orchestration, streaming, cloud data services and data quality</b>. Employability is demonstrated through a <b>portfolio</b> of documented projects, a <b>resume</b> with measurable achievements, and optionally <b>vendor certifications</b> that validate platform knowledge.',
    'Learn the skills in a sensible order, prove them with projects people can see, write a resume that shows results with numbers, and add a certification only where it helps with the jobs you want.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Portfolio project', 'A complete project you can show: code, README, architecture diagram, sample data and results.'),
    ('ATS', 'Applicant tracking system: software many companies use to store, search and filter applications.'),
    ('Quantified bullet', 'A resume line with an action, a tool and a measurable result (“from 3 h to 25 min”).'),
    ('Associate / professional certification', 'Vendor exams at entry and advanced levels, usually valid for 2–3 years.'),
    ('Referral', 'An employee recommending you for a role; often the most effective way to get an interview.'),
    ('Take-home assignment', 'A small project set by a company during hiring, judged on correctness, clarity and tests.'),
    ('STAR', 'Situation, Task, Action, Result: a structure for answering behavioural questions.'),
    ('Medallion architecture', 'Bronze, silver and gold layers in a lakehouse; a common portfolio project structure.'),
]) + lv + '''
EXAM> Describe a learning path for a data engineer (<b>foundations → processing → orchestration → streaming → cloud → lakehouse → projects</b>), explain why projects and quantified results matter more than tool lists, and name one certification each for <b>AWS, Azure, Google Cloud and Databricks</b>.'''

# ---------------------------------------------------------------- types
types = table(['Certification', 'Provider', 'Level', 'Good for'], [
    ['<b>AWS Certified Data Engineer – Associate</b> (DEA-C01)', 'Amazon Web Services', 'Associate', 'Roles on AWS: S3, Glue, EMR, Redshift, Kinesis'],
    ['<b>Microsoft Certified: Fabric Data Engineer Associate</b> (DP-700)', 'Microsoft', 'Associate', 'Azure / Microsoft Fabric shops (DP-203 was retired in 2025)'],
    ['<b>Google Cloud Professional Data Engineer</b>', 'Google Cloud', 'Professional', 'BigQuery, Dataflow, Pub/Sub, Dataproc roles'],
    ['<b>Databricks Certified Data Engineer Associate</b> / Professional', 'Databricks', 'Associate / Professional', 'Spark and lakehouse roles on any cloud'],
    ['<b>SnowPro Core</b> (then SnowPro Advanced: Data Engineer)', 'Snowflake', 'Core / Advanced', 'Snowflake-based analytics teams'],
    ['<b>Confluent Certified Developer for Apache Kafka</b>', 'Confluent', 'Developer', 'Streaming-heavy roles'],
], minw=680) + '''
  <p class="muted">Exam fees are roughly US$150–200 each as of mid-2026 (DataCamp’s certification guide, July 2026). Names, fees and validity change; always check the provider’s certification page.</p>

  <h3>Four ways to prove your skills</h3>
''' + cards([
    ('Projects', 'End-to-end pipelines on GitHub with README, diagram, tests and results. The strongest evidence for freshers.', 'Most weight'),
    ('Work and internships', 'Quantified achievements: data volumes, time saved, cost cut, errors prevented.', 'Real impact'),
    ('Certifications', 'Validate platform knowledge and help pass resume filters, especially for cloud roles and service companies.', 'Signal'),
    ('Writing and community', 'Blog posts explaining what you built, answers on forums, talks at meetups, open-source contributions.', 'Visibility'),
]) + '''
TIP> Pick the certification that matches the jobs you are applying for (look at 20 job posts first), and take it <b>after</b> you have built something on that platform. Passing is much easier when the services are familiar.'''

# ---------------------------------------------------------------- steps
c1 = '''hours_needed, hours_per_week = 367, 12
weeks = -(-hours_needed // hours_per_week)
print(weeks, "weeks, about", round(weeks / 4.3, 1), "months")'''
c2 = '''bullet = "Reduced a nightly PySpark job from 3 h to 25 min"
print("has a number:", any(ch.isdigit() for ch in bullet))
print("starts with action:", bullet.split()[0] in ("Built", "Reduced", "Designed"))'''
steps = stepper([
    ('Study 20 job posts',
     '<p>Collect 20 data engineer postings for roles you want (product companies, service companies, start-ups) and count the skills that repeat.</p>',
     'In India, SQL, Python, Spark, a cloud, Airflow and data modelling appear in most posts. The posts tell you what to learn and which certification matters.'),
    ('Make a time-boxed plan',
     code('python', 'plan.py', c1, run_code(c1)),
     'Honest hours per week turn a vague goal into a date. Skip what you already know well; spend most time on gaps.'),
    ('Build one end-to-end project',
     '<p>Ingest real data (for example from <code>data.gov.in</code> or a public API), land it raw, clean it with Spark or dbt, run quality checks, orchestrate with Airflow, and serve a small dashboard.</p>',
     'One complete, documented project beats five half-finished notebooks. Interviewers ask about decisions, so write them down in the README.'),
    ('Write quantified resume bullets',
     code('python', 'bullet_check.py', c2, run_code(c2)),
     'Use action + tool + scale + result. Keep the resume to one page as a fresher, with projects above a skills list.'),
    ('Apply with referrals and polish your profiles',
     '<p>Update LinkedIn and GitHub, ask former classmates and colleagues for referrals, apply on job portals and company career pages, and track every application in a sheet.</p>',
     'Referrals and direct messages to hiring managers often get faster replies than portal applications alone.'),
    ('Prepare for interviews',
     '<p>Practise SQL and Python problems, Spark and data-modelling questions, a system design for a pipeline, and STAR stories about your projects. The next lesson has a full question bank.</p>',
     'Most data engineering rounds are SQL, coding, a project deep-dive, design and a behavioural round.'),
])

# ---------------------------------------------------------------- two-view animation: recruiter scan
def page(highlight, note):
    o = box(40, 10, 280, 196, 'card') + t(180, 34, 'KABIR SHAH · Data Engineer (Fresher)', 9, bold=True) + t(180, 48, 'github.com/kabir-de · Pune', 8, 'ink2')
    sections = [('Projects', 66), ('Experience', 106), ('Skills', 146), ('Education & certification', 180)]
    for k, (s, y) in enumerate(sections):
        if k == highlight:
            o += fill(50, y - 11, 260, 30, 'amber', rx=4, opacity=.35)
        o += t(56, y, s, 8.6, 'acc', anchor='start', bold=True)
    o += t(56, 80, '• Payments pipeline: Kafka → Spark → Delta, 10 lakh rows/day', 7.6, anchor='start')
    o += t(56, 120, '• TiffinGo intern: PySpark job 3 h → 25 min', 7.6, anchor='start')
    o += t(56, 160, 'SQL · Python · PySpark · Airflow · AWS', 7.6, anchor='start')
    o += t(56, 194, 'B.Tech CSE · AWS Data Engineer – Associate', 7.6, anchor='start')
    return o + t(180, 218, note, 8, 'ink2')
see = [page(None, 'opened from 180 applications'), page(0, 'eyes go to the projects first'), page(1, 'then the internship result'),
       page(2, 'a short, relevant skills line'), page(3, 'education and one certification'), page(None, 'about 30 seconds: shortlist')]
def think(lines, tone='acc'):
    return ''.join(t(180, 40 + k * 20, s, 9, tone if k == 0 else 'ink2', bold=(k == 0)) for k, s in enumerate(lines))
behind = [
    think(['Filter: search applications', 'for “Spark”, “SQL”, “Airflow”, “AWS”.', 'Kabir’s resume matches the role’s words.', '(An ATS or a human keyword search.)']),
    think(['Is there a real project?', 'A named pipeline with a scale (10 lakh rows/day)', 'and a link they can open.', '✓ evidence, not just claims'], 'green'),
    think(['Is there measurable impact?', '3 h → 25 min shows he understands Spark', 'performance, not just syntax.', '✓ a great interview topic'], 'green'),
    think(['Do the skills match the job?', 'Five relevant tools, no 25-item list.', 'Each one appears in a project or bullet.', '✓ believable']),
    think(['Basic requirements met?', 'Degree and one relevant certification.', 'Nice to have, rarely the deciding factor.', '✓']),
    think(['Decision: shortlist', 'Interview questions already forming:', '“Why Delta?” “How did you fix the skew?”', 'Your resume sets your interview agenda.'], 'green'),
]
see_caps = ['A recruiter opens Kabir’s resume, one of 180 for the role.', 'Her eyes go first to the projects section.', 'Then to the internship result with a number.',
            'A short skills line that matches the job.', 'Education and one certification.', 'About 30 seconds later, Kabir is shortlisted.']
behind_caps = ['Applications are often searched or filtered by keywords from the job description, by an applicant tracking system or simply by a person using search. Matching words get the resume opened.',
               'The first question is whether there is real evidence. A named project with scale and a link is concrete.',
               'Numbers show impact and understanding. A runtime cut from 3 hours to 25 minutes signals real Spark skill.',
               'A short, relevant skills list is believable when each tool also appears in a project or bullet. Long lists of tools invite doubt.',
               'Degree and a relevant certification satisfy basic requirements; they rarely decide alone.',
               'He is shortlisted, and the interviewer’s first questions will come straight from his bullets. Only write what you can explain in depth.']
two = anim_two('Thirty seconds with a recruiter', 'What the recruiter sees, and what she is checking', 'A recruiter scanning Kabir’s one-page resume section by section',
               'The questions a recruiter asks while scanning: keywords, evidence, impact, fit and basics', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: roadmap (real numbers from career_planner.out)
phases = [(1, 6, 'SQL, Python, Linux & Git', 'blue'), (7, 9, 'Data modelling', 'blue'), (10, 15, 'Spark / PySpark', 'acc'), (16, 18, 'Airflow', 'acc'),
          (19, 21, 'Kafka', 'violet'), (22, 26, 'One cloud', 'violet'), (27, 30, 'Lakehouse + dbt', 'green'), (31, 35, 'Portfolio project', 'green')]
def road(n, note1, note2, tone):
    o = t(14, 20, 'Weeks at 12 hours a week (from the planner program)', 8.8, 'ink2', anchor='start')
    scale = 320 / 35
    o += fill(20, 34, 320, 4, 'grey', rx=2)
    for k, (a, b, name, tn) in enumerate(phases):
        x = 20 + (a - 1) * scale
        w = (b - a + 1) * scale - 2
        if k < n:
            o += fill(x, 44 + (k % 2) * 34, w, 24, tn, rx=4, opacity=.85)
            o += t(x + w / 2, 60 + (k % 2) * 34, f'{a}–{b}', 7.6, 'ink', bold=True)
    labels = [p[2] for p in phases[:n]]
    if labels:
        o += t(180, 128, 'now: ' + labels[-1], 9.4, bold=True)
    return o + cap(note1, note2, tone, y=146, h=44)
fr1 = [
    road(2, 'Weeks 1–9: foundations. Kabir is good at SQL and', 'Python already, so he only revises (20 h each).', 'blue'),
    road(4, 'Weeks 10–18: Spark from scratch (70 h),', 'then Airflow for scheduling and retries.', 'acc'),
    road(6, 'Weeks 19–26: Kafka basics and one cloud', '(storage, managed Spark, warehouse, IAM).', 'violet'),
    road(7, 'Weeks 27–30: Delta Lake and dbt,', 'bronze/silver/gold, quality tests.', 'green'),
    road(8, 'Weeks 31–35: one end-to-end project.', 'Total 367 hours, about 8 months.', 'green'),
]
s1 = anim_one('Real-time scenario 1', 'An 8-month roadmap built from Kabir’s own skills',
              'These figures come from the program in “Run it on your PC” below. It skips what Kabir already knows and spreads the rest across 12 hours a week.',
              'Personal roadmap', 'A 35-week learning roadmap from foundations to Spark, Airflow, Kafka, cloud, lakehouse and a portfolio project', fr1,
              ['The planner starts with foundations. Kabir rates himself 2 out of 3 in SQL and Python, so each needs only 20 hours of revision; Linux, Git and data modelling come next.',
               'Spark is new to him and takes the biggest block, 70 hours over six weeks, followed by Airflow.',
               'Kafka basics and one cloud follow. He picks AWS because most posts he collected ask for it.',
               'Then the lakehouse layer: Delta Lake tables, medallion layers and dbt tests.',
               'The last five weeks go to one end-to-end portfolio project that uses everything. In total 367 hours, about 35 weeks or 8 months at 12 hours a week. Change the hours in the program to see your own date.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: rewriting a bullet (scores from career_planner.out)
def bullet(text_lines, score, missing, note1, note2, tone):
    o = box(14, 20, 332, 70, 'card') + ''.join(t(26, 44 + k * 18, s, 9, anchor='start') for k, s in enumerate(text_lines))
    o += t(30, 112, f'score {score}/4', 10, 'green' if score == 4 else ('amber' if score >= 2 else 'red'), anchor='start', bold=True)
    o += t(110, 112, missing, 8.6, 'ink2', anchor='start')
    return o + cap(note1, note2, tone, y=134, h=44)
fr2 = [
    bullet(['Worked on data pipelines using various tools.'], 0, 'missing: verb, tool, number, impact', '“Worked on” and “various tools” say nothing.', 'An interviewer can’t ask anything about it.', 'red'),
    bullet(['Responsible for Spark jobs.'], 1, 'missing: verb, number, impact', 'A tool appears, but “responsible for”', 'is a duty, not an achievement.', 'red'),
    bullet(['Built an Airflow DAG that loads 2 lakh orders a day', 'into Delta tables.'], 3, 'missing: impact', 'Action, tools and scale. Better.', 'What changed because of it?', 'amber'),
    bullet(['Reduced a nightly PySpark job from 3 h to 25 min', 'by fixing skewed joins and partitioning by date.'], 4, 'all four present', 'Action + tool + method + measurable result.', 'Every word can be discussed in an interview.', 'green'),
    bullet(['Reduced a nightly PySpark job from 3 h to 25 min', 'by fixing skewed joins and partitioning by date.'], 4, 'true and explainable?', 'Only write what you did and can explain', 'in depth. Interviewers will dig into it.', 'blue'),
]
s2 = anim_one('Real-time scenario 2', 'One bullet, four versions',
              'The scores come from the program below, which checks each bullet for an action verb, a named tool, a number and an impact. Watch a vague line become an interview magnet.',
              'Resume bullets', 'A resume bullet rewritten from a vague duty to an action with a tool, a number and a result', fr2,
              ['“Worked on data pipelines using various tools” scores 0: no action, no tool, no number, no result.',
               '“Responsible for Spark jobs” names a tool but describes a duty, not something achieved.',
               '“Built an Airflow DAG that loads 2 lakh orders a day into Delta tables” has an action, tools and scale. It is missing the effect.',
               '“Reduced a nightly PySpark job from 3 h to 25 min by fixing skewed joins and partitioning by date” has all four, and tells the interviewer exactly what to ask about.',
               'One rule beats every template: the bullet must be true and you must be able to explain each part in depth, including the trade-offs.'])

# ---------------------------------------------------------------- scenario 3 (advanced): a portfolio repo reviewers trust
items = ['README: problem, architecture diagram, how to run', 'docker-compose: Kafka, Spark, Airflow, MinIO locally', 'pipelines/ with bronze → silver → gold code',
         'tests/ + data quality checks, CI on every push', 'results: dashboard screenshot, data volumes, costs, lessons learnt']
def repo(n, note1, note2, tone):
    o = box(14, 14, 332, 118, 'card') + t(28, 32, 'github.com/kabir-de/payments-lakehouse', 9, 'blue', anchor='start', mono=True)
    for k in range(5):
        on = k < n
        o += t(28, 54 + k * 17, ('✓ ' if on else '○ ') + items[k], 8.4, 'ink' if on else 'ink3', anchor='start')
    return o + cap(note1, note2, tone, y=146, h=44)
fr3 = [
    repo(1, 'The README answers in 1 minute: what problem,', 'what architecture, how to run it, what result.', 'blue'),
    repo(2, 'Anyone can run it locally with one command:', 'docker compose up.', 'blue'),
    repo(3, 'Clear layers, small functions, config separate', 'from code; no secrets committed.', 'acc'),
    repo(4, 'Unit tests and data quality checks run in CI', '(e.g. GitHub Actions) on every push.', 'green'),
    repo(5, 'Results with numbers and honest limitations:', 'the part interviewers love to discuss.', 'green'),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'A portfolio repository a senior engineer would trust',
              'Hiring managers often open a candidate’s main project for two minutes. Watch what turns a folder of notebooks into evidence of professional skill.',
              'Portfolio quality', 'A GitHub repository improving step by step: README, local setup, structured pipelines, tests and CI, and documented results', fr3,
              ['The README states the problem (for example a UPI-style payments analytics pipeline), shows an architecture diagram, and gives exact run instructions and the outcome.',
               'A docker-compose file starts Kafka, Spark, Airflow and MinIO (an S3-compatible store) locally, so a reviewer can run everything with one command.',
               'Code is organised by layer (bronze, silver, gold), with configuration separate from code and no passwords or keys committed.',
               'Unit tests and data quality checks run automatically in CI on every push, showing engineering discipline most fresher projects lack.',
               'Results include a dashboard screenshot, data volumes, run times, rough cloud cost and an honest list of limitations and next steps. These become the best interview conversations.'])

realworld = '''  <p>Three live scenarios: a personal roadmap (numbers from the program below), one resume bullet improving from 0/4 to 4/4, and an advanced look at a portfolio repository that reviewers trust.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Portfolio project ideas with Indian data</h3>
''' + usecase('<rect x="20" y="24" width="80" height="44" rx="8" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="51" text-anchor="middle" font-size="11" font-weight="700" class="s-blue">₹ UPI</text>',
              '1. Payments analytics lakehouse', 'Simulate UPI-style transactions into Kafka, process them with Spark Structured Streaming into Delta tables, flag suspicious patterns and build daily settlement reports.', ['Kafka', '*Spark → Delta', 'Fraud + reports']) + usecase(
    '<rect x="14" y="30" width="92" height="30" rx="6" class="s-soft-green" style="stroke:var(--green)"/><circle cx="34" cy="68" r="6" style="fill:var(--ink3)"/><circle cx="86" cy="68" r="6" style="fill:var(--ink3)"/>',
    '2. Railway or metro performance', 'Use public timetable or delay data, model it as a star schema, load with Airflow daily and show punctuality by route and station.', ['Open data', '*Airflow + dbt', 'Punctuality dashboard']) + usecase(
    '<path d="M20 60 Q40 20 60 46 T100 30" style="fill:none;stroke:var(--violet);stroke-width:3"/>',
    '3. Air quality across cities', 'Collect air-quality readings from public sources (for example data.gov.in), clean and partition by city and date, and alert when levels cross thresholds.', ['API ingest', '*Partitioned Parquet', 'Alerts + trends']) + usecase(
    '<rect x="22" y="26" width="34" height="40" rx="4" class="s-soft-acc" style="stroke:var(--track)"/><rect x="64" y="26" width="34" height="40" rx="4" class="s-soft-acc" style="stroke:var(--track)"/>',
    '4. E-commerce clickstream', 'Generate sale-day clickstream, compute live funnels (view → cart → buy) and hourly product rankings, with batch reprocessing for corrections.', ['Events', '*Streaming + batch', 'Live funnel']) + '''

  <h3>A one-page fresher resume, top to bottom</h3>
''' + table(['Section', 'What to include', 'Avoid'], [
    ['<b>Header</b>', 'Name, target role, city, email, phone, GitHub and LinkedIn links', 'Photos, date of birth, full address'],
    ['<b>Summary (optional, 2 lines)</b>', 'Target role and your strongest evidence', 'Generic “hard-working team player”'],
    ['<b>Projects</b>', '2–3 projects: what, tools, scale, result, link', 'Tutorial copies without your own decisions'],
    ['<b>Experience / internships</b>', 'Quantified bullets: action + tool + scale + result', 'Duties (“responsible for…”)'],
    ['<b>Skills</b>', 'The tools you can discuss in depth, grouped', '25-item lists, skill-level bars'],
    ['<b>Education and certifications</b>', 'Degree, college, year; relevant certifications', 'Unrelated certificates'],
], minw=620) + '''

  <h3>Sources</h3>
  <ul class="muted">
    <li>Certification names, fees and validity: <a href="https://www.datacamp.com/blog/best-data-engineer-certifications" rel="noopener">DataCamp, “Best data engineer certifications”, July 2026</a>; check each provider’s official certification page before booking.</li>
  </ul>'''

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Badges or evidence?', story)
        + part(2, 'definition', 'Definition', 'Roadmap, portfolio, certifications and resume', definition)
        + part(3, 'types', 'Types and ways to use it', 'Certifications and other ways to prove skills', types)
        + part(4, 'steps', 'Step by step', 'From job posts to interviews', steps)
        + part(5, 'animation', 'See it happen', 'A resume in 30 seconds: what the recruiter sees, and what she checks', '  <p>Step through the six frames. Left: Kabir’s resume as the recruiter scans it. Right: the questions in her mind.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: roadmap, resume and portfolio', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Career planning', 'Fresher', '“I have 6 months. What should I learn?”',
            'A final-year student wants a data engineering job in six months and asks for a plan.',
            'can you prioritise ruthlessly?',
            '<ol><li>Weeks 1–6: SQL (windows, CTEs), Python, Git and Linux, data modelling.</li><li>Weeks 7–14: PySpark and Parquet, then Airflow and dbt.</li><li>Weeks 15–18: one cloud’s storage, Spark and warehouse; Kafka basics.</li><li>Weeks 19–24: one end-to-end project, resume, applications and interview practice (SQL daily).</li></ol><p>Skip Hadoop administration, multiple clouds and five certifications; depth in the core beats breadth.</p>',
            'trying to learn every tool on a “roadmap” poster.')
        + scn('Resume', 'Fresher', 'Fix this resume',
              'A resume lists 30 tools, has no projects and says “responsible for data pipelines” for an internship.',
              'can you turn duties into evidence?',
              '<ul><li>Cut skills to tools the candidate can discuss in depth.</li><li>Add 2–3 projects with tools, scale, results and GitHub links, above the skills section.</li><li>Rewrite each bullet as action + tool + scale + result, for example “Automated a daily sales load with Airflow, cutting manual work by 2 hours a day”.</li><li>Keep it to one page and check each line is true and explainable.</li></ul>',
              'adding more tools or decorative design.')
        + scn('Certifications', '1–3 years', 'Which certification first?',
              'An analyst moving into data engineering has budget for one certification and works at a company on Azure.',
              'can you link a certification to real goals?',
              '<p>Start with the platform you use or the jobs you target. On Azure/Microsoft Fabric that is the <b>Fabric Data Engineer Associate (DP-700)</b>; on AWS the <b>AWS Certified Data Engineer – Associate</b>; on Google Cloud the <b>Professional Data Engineer</b>; for Spark/lakehouse roles the <b>Databricks Data Engineer Associate</b>. Take it after building something on that platform, and pair it with a project so the badge has evidence behind it.</p>',
              'choosing the most popular badge without checking job posts.')
        + scn('Interview · behavioural', 'Fresher', '“Tell me about your project.”',
              'The first question in most data engineering interviews.',
              'can you explain your project clearly and honestly in 2 minutes?',
              '<p>Use a clear structure: <b>problem</b> (what and why), <b>architecture</b> (sources → ingestion → storage → processing → serving, with tools), <b>scale</b> (rows, size, frequency), <b>one hard problem</b> you solved and how (STAR), <b>result</b> with numbers, and <b>what you would improve</b>. Be ready for “why this tool and not X?” and “what happens if this fails?”.</p>',
              'reading the tool list or claiming work you didn’t do.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
