import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='05-governance-and-security', lesson='01-data-quality-governance-and-security', n='5.1',
    module_label='Module 5 · Governance and Security',
    title='Data quality, governance, security and the DPDP Act',
    desc='Data quality dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), quality checks and quarantine in pipelines, data governance (ownership, catalogs, lineage, classification, data contracts), security (RBAC, masking, row filters, encryption, audit logs) and privacy under India\'s Digital Personal Data Protection Act 2023 and DPDP Rules 2025: consent, erasure, breach notification and penalties. Animations and a data-quality gate for your PC.',
    og_desc='Every job was green, and the dashboard was 100× wrong. Learn data quality checks, lineage, masking and the DPDP Act.',
    minutes=30, level='Beginner → Advanced',
    lead='A pipeline can run perfectly and still publish wrong numbers, and a single shared sheet can leak lakhs of phone numbers. In this lesson you learn the <b>six data quality dimensions</b>, build a <b>quality gate</b> that quarantines bad rows, trace a 100× revenue error with <b>lineage</b>, see one table masked differently for each role, and handle an erasure request and a breach under India’s <b>DPDP Act</b>.',
    chips=['Runs in your browser (Python)', '3 real-time scenarios', 'Quality gate for your PC'],
)

RUN = dict(
    heading='Write your first data quality checks',
    intro='<p>A few order rows are checked against rules for validity, completeness and uniqueness. Rows that fail are quarantined with the reason. Then try the challenges: freshness, reconciliation, masking, pseudonymous keys and a publish threshold.</p>',
    code='''orders = [
    {"id": "O1", "city": "Pune",   "amount": 320},
    {"id": "O2", "city": "",       "amount": 150},
    {"id": "O3", "city": "Thane",  "amount": -40},
    {"id": "O1", "city": "Pune",   "amount": 320},
    {"id": "O4", "city": "Mumbai", "amount": 610},
]
seen, good, quarantine = set(), [], []
for o in orders:
    reasons = []
    if not o["city"]:
        reasons.append("missing city")
    if o["amount"] <= 0:
        reasons.append("amount not positive")
    if o["id"] in seen:
        reasons.append("duplicate id")
    seen.add(o["id"])
    (quarantine if reasons else good).append((o["id"], reasons))

print("good      :", [i for i, _ in good])
print("quarantine:", quarantine)
''',
    anno=[
        ('    if not o["city"]:', 'Completeness: a required field is empty.'),
        ('    if o["id"] in seen:', 'Uniqueness: the same order arrived twice.'),
    ],
    tasks=[
        dict(label='1 · Three checks', hint='Press <b>Run</b>. Add a validity rule: amounts above 50,000 are suspicious. Add a row to test it.', code=None),
        dict(label='2 · Freshness', hint='The gold table must be updated by 6:00 am. Compare the last update time with the deadline. Try 05:40.',
             code='''from datetime import datetime
deadline = datetime(2026, 10, 20, 6, 0)
last_update = datetime(2026, 10, 20, 6, 47)
late = (last_update - deadline).total_seconds() / 60
print("FRESH" if late <= 0 else f"STALE by {late:.0f} minutes")
'''),
        dict(label='3 · Reconciliation', hint='Consistency: compare counts and totals between the source database and the lake. Change one number and see which check fails.',
             code='''source = {"rows": 48_210, "total": 1_54_32_890}
lake   = {"rows": 48_210, "total": 1_54_31_640}
for k in source:
    diff = lake[k] - source[k]
    print(f"{k:5}: source {source[k]:,} lake {lake[k]:,}", "OK" if diff == 0 else f"MISMATCH ({diff:+,})")
'''),
        dict(label='4 · Masking', hint='Mask phones and emails for analysts. Keep the email domain. Add a masked Aadhaar showing only the last 4 digits.',
             code='''def mask_phone(p):
    return "X" * 6 + p[-4:]
def mask_email(e):
    name, domain = e.split("@")
    return name[0] + "***@" + domain
print(mask_phone("9876543210"), mask_email("asha.patil@example.com"))
'''),
        dict(label='5 · Pseudonymous keys (advanced)', hint='A salted hash gives the same key for the same email, so tables can be joined without the email. Change the salt and see every key change.',
             code='''import hashlib
SALT = "from-a-secrets-vault"
def key(email):
    return hashlib.sha256((SALT + email.lower()).encode()).hexdigest()[:12]
print(key("Asha@example.com"))
print(key("asha@example.com"))   # same person, same key
print(key("ravi@example.com"))
'''),
        dict(label='6 · Publish threshold (advanced)', hint='Publish only if fewer than 2% of rows fail. Try 600 failures.',
             code='''total, failed, limit = 25_000, 380, 0.02
rate = failed / total
print(f"failure rate {rate:.2%}:", "PUBLISH, alert owner" if rate < limit else "STOP pipeline, page on-call")
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a quality gate with privacy masking',
    intro='<p>This program creates a batch of 10,030 orders with realistic problems (negative amounts, missing cities, invalid phones, duplicates), runs four quality checks, quarantines failing rows, decides whether to publish, and writes a clean CSV where emails become pseudonymous keys and phones are masked. Save it as <code>quality_guard.py</code>.</p>',
    items=[
        dict(title='Check, quarantine, mask, publish', file='quality_guard.py',
             cmd=open(os.path.join(HERE, 'quality_guard.py')).read() + '\n# In a terminal:  python quality_guard.py',
             output=open(os.path.join(HERE, 'quality_guard.out')).read(),
             note='Recorded from a real run with Python 3.13 (only the standard library). The data is generated with a fixed random seed, so you will get the same counts. In production the salt would come from a secrets manager, and tools such as Great Expectations, dbt tests or Soda would run the checks.'),
    ],
)

TRACE = dict(
    heading='A quality check, one row at a time',
    intro='<p>Four amounts are checked against a valid range. Watch the pass and fail lists fill up.</p>',
    code='''amounts = [320, -40, 610, 99000]
passed, failed = [], []
for a in amounts:
    if 1 <= a <= 50_000:
        passed.append(a)
    else:
        failed.append(a)
print("passed", passed, "failed", failed)
''',
    notes={4: 'Rule :: Validity: the amount must be in a sensible range.',
           7: 'Quarantine :: Failing values are kept aside for review, not thrown away.'},
)

WORKED_INTRO = 'Four data-quality and privacy tasks from a real platform. Each runs live and is traced.'
EXAMPLES = [
    dict(level='b', tag='Quality · completeness', title='Percentage of missing values per column',
         problem='<p>Count how many values are missing in each column of a small customer table, as a percentage.</p>',
         inp='4 rows with name, city, phone',
         approach=['For each column, count values that are empty or None.',
                   'Divide by the number of rows.',
                   'Print as a percentage.'],
         code='''rows = [{"name": "Asha", "city": "Pune", "phone": "9876543210"},
        {"name": "Ravi", "city": "", "phone": None},
        {"name": "", "city": "Thane", "phone": "9123456780"},
        {"name": "Meera", "city": "", "phone": "9988776655"}]
for col in ["name", "city", "phone"]:
    missing = sum(1 for r in rows if not r[col])
    print(f"{col:5}: {missing / len(rows):.0%} missing")
''', notes={6: 'Count :: Empty strings and None both count as missing.'},
         tryit='Set a rule: fail the batch if any required column is more than 10% missing.'),
    dict(level='i', tag='Quality · distribution', title='Catch the rupees-to-paise bug',
         problem='<p>Compare today’s median order amount with the last 7 days. Flag it if it is more than 3 times higher or lower than the 7-day median.</p>',
         inp='7 daily medians and today’s median',
         approach=['Compute the median of the last 7 daily medians.',
                   'Ratio = today ÷ baseline.',
                   'Flag if ratio > 3 or < 1/3.'],
         code='''from statistics import median
history = [318, 325, 330, 312, 340, 322, 319]
today = 32_150
baseline = median(history)
ratio = today / baseline
flag = ratio > 3 or ratio < 1 / 3
print(f"baseline {baseline}, today {today}, ratio {ratio:.0f}x ->", "ALERT" if flag else "ok")
''', notes={4: 'Baseline :: The median is robust to one unusual day.', 6: 'Check :: Big jumps up or down are suspicious.'},
         tryit='Today’s median is 290. Does it alert? What ratio would a rupees-to-thousands bug produce?'),
    dict(level='i', tag='Governance · catalog', title='Find every column tagged as PII',
         problem='<p>A small catalog maps tables to columns and tags. List every PII column, grouped by table, so the privacy team knows where personal data lives.</p>',
         inp='catalog dictionary',
         approach=['Loop over tables and their columns.',
                   'Keep columns whose tags include “pii”.',
                   'Print table: columns.'],
         code='''catalog = {
    "customers": {"name": ["pii"], "phone": ["pii"], "city": []},
    "orders": {"order_id": [], "customer_key": ["pseudonym"], "amount": ["financial"]},
    "support_tickets": {"email": ["pii"], "message": ["pii", "free-text"]},
}
for table, cols in catalog.items():
    pii = [c for c, tags in cols.items() if "pii" in tags]
    if pii:
        print(f"{table}: {pii}")
''', notes={6: 'Filter :: Tags drive masking and deletion, so they must be complete.'},
         tryit='Add a check that warns about columns named like “phone” or “email” that are missing the pii tag.'),
    dict(level='a', tag='Privacy · erasure', title='Erase one customer across tables',
         problem='<p>A customer’s pseudonymous key must be removed from three tables. Delete matching rows, count deletions per table and record an audit entry.</p>',
         inp='tables keyed by customer_key, key "97c8"',
         approach=['For each table, keep rows whose key is different.',
                   'Count how many were removed.',
                   'Append an audit record with the counts.'],
         code='''tables = {
    "orders": [("97c8", 320), ("a1b2", 150), ("97c8", 610)],
    "features": [("97c8", 0.82), ("a1b2", 0.31)],
    "crm_export": [("a1b2", "Thane")],
}
target, audit = "97c8", {}
for name, rows in tables.items():
    kept = [r for r in rows if r[0] != target]
    audit[name] = len(rows) - len(kept)
    tables[name] = kept
print("deleted:", audit, "| remaining orders:", tables["orders"])
''', notes={7: 'Delete :: Keep every row that is not the target customer.', 8: 'Audit :: Record what was erased, for proof of compliance.'},
         tryit='Backups can’t be edited. Add a “backups” entry that records the expiry date instead of deleting.'),
]

QUIZ = [
    dict(q='Each order_id should appear exactly once, but some appear twice. Which quality dimension is violated?', options=['Timeliness', 'Uniqueness', 'Accuracy', 'Completeness'], answer=1,
         why='Duplicates violate uniqueness; they often come from retries or reloading the same file.'),
    dict(q='The gold table is ready at 9 am, but dashboards need it by 6 am. Which dimension is this?', options=['Validity', 'Consistency', 'Timeliness', 'Uniqueness'], answer=2,
         why='Timeliness (freshness) is whether data is available when it is needed.'),
    dict(q='All pipeline jobs succeed, but revenue is 100× too high. What would have caught it?', options=['More CPU', 'A value or distribution check on the amount column', 'A faster scheduler', 'Bigger partitions'], answer=1,
         why='Job monitoring checks that jobs ran; data quality checks check that values make sense.'),
    dict(q='What does data lineage show?', options=['Who is logged in', 'Where data came from and which tables and reports depend on it', 'The cost of a query', 'The size of a file'], answer=1,
         why='Lineage traces data from sources through transformations to consumers, which speeds up debugging and impact analysis.'),
    dict(q='Analysts see phone numbers as XXXXXX3210 while support agents see the full number. This is:', options=['Encryption at rest', 'Role-based column masking', 'Partitioning', 'Replication'], answer=1,
         why='Masking policies show different values depending on the user\'s role.'),
    dict(q='Replacing an email with a salted hash so tables can still be joined is called:', options=['Anonymisation', 'Pseudonymisation', 'Compression', 'Normalisation'], answer=1,
         why='It can still be linked back with the salt or other data, so it remains personal data, but it reduces exposure.'),
    dict(q='Under the DPDP Act, 2023, the company that decides why and how personal data is processed is called the:', options=['Data principal', 'Data fiduciary', 'Data steward', 'Consent manager'], answer=1,
         why='The data principal is the person; the data fiduciary is the organisation deciding the purpose and means of processing.'),
    dict(q='Under the DPDP Rules, 2025, what is the deadline for a detailed breach report to the Data Protection Board?', options=['7 days', '30 days', '72 hours', 'No deadline'], answer=2,
         why='Intimation is required without delay, with a detailed report within 72 hours.'),
]

REVISION = [
    'Six quality dimensions: accuracy, completeness, consistency, timeliness, validity, uniqueness.',
    'Gate pipelines: test every load, quarantine bad rows, stop above a threshold, alert the owner.',
    'Green jobs ≠ correct data: add range, distribution and reconciliation checks.',
    'Governance = owners/stewards, catalog, lineage, classification (PII tags), contracts, retention.',
    'Security = least privilege (RBAC), masking, row filters, encryption, secrets vault, audit logs.',
    'Pseudonymisation (salted hash) ≠ anonymisation; deletion in lakes via Delta/Iceberg/Hudi deletes + vacuum.',
    'DPDP 2023 + Rules 2025: consent, purpose limits, erasure, safeguards, breach report within 72 h, penalties up to ₹250 crore.',
]
FAQ = [
    ('What are the dimensions of data quality?', 'The commonly used dimensions are accuracy (values match reality), completeness (no missing required data), consistency (systems and tables agree), timeliness (data is fresh when needed), validity (values follow formats, types and ranges) and uniqueness (no unintended duplicates). Some frameworks add integrity, relevance and accessibility.'),
    ('What is the difference between data governance and data management?', 'Data governance sets the rules, roles and accountability: who owns data, what policies apply, how quality and access are decided. Data management is the day-to-day execution: building pipelines, storing, securing, cleaning and delivering data according to those rules.'),
    ('How do you implement data quality checks in a pipeline?', 'Define rules with data owners, then run automated tests after each load: schema, row counts, nulls, ranges, uniqueness, referential integrity, freshness and reconciliation with source totals. Quarantine failing rows, stop publishing above a threshold, alert the owner and track quality metrics over time. Tools include dbt tests, Great Expectations, Soda, Deequ and Delta Live Tables expectations.'),
    ('What is the DPDP Act and how does it affect data engineers?', 'The Digital Personal Data Protection Act, 2023 is India\'s law on processing digital personal data, made operational by the DPDP Rules, 2025 with phased timelines. It requires notice and consent, purpose limitation, data minimisation, reasonable security safeguards, honouring rights such as erasure, breach notification and extra care for children\'s data. For data engineers this means tagging PII, limiting copies, masking, access controls, retention and deletion workflows across lakes and backups, audit logs and breach-response plans.'),
    ('How do you delete personal data from a data lake?', 'Locate all copies using a catalog and a consistent customer key, run row-level deletes on tables stored in formats such as Delta Lake, Apache Iceberg or Hudi, remove old file versions with vacuum or snapshot expiry, delete derived tables, features and exports, and let immutable backups expire on a defined schedule without restoring erased records. Record the request and completion for audit.'),
]

PRACTICE_INTRO = 'Data-quality, masking and privacy exercises. The last two are business tasks.'
PROBLEMS = [
    dict(level='easy', title='Count nulls', stmt='Count the None values in [12, None, 7, None, 3].', inp='list',
         code='''print([12, None, 7, None, 3].count(None))
''', explain='Completeness checks start with counting missing values.'),
    dict(level='easy', title='Find duplicates', stmt='Print the IDs that appear more than once in ["a", "b", "a", "c", "b", "a"].', inp='list of IDs',
         code='''from collections import Counter
print([k for k, v in Counter(["a", "b", "a", "c", "b", "a"]).items() if v > 1])
''', explain='Uniqueness check: count occurrences per key.'),
    dict(level='easy', title='Mask a phone', stmt='Print 9876543210 with only the last 4 digits visible.', inp='9876543210',
         code='''p = "9876543210"
print("X" * 6 + p[-4:])
''', explain='Masking keeps enough to recognise a number without exposing it.'),
    dict(level='medium', title='Validate phones', stmt='Print which of ["9876543210", "12345", "6123456789", "5123456789"] are valid Indian mobile numbers (10 digits, starting 6–9).', inp='4 strings',
         code='''import re
print([p for p in ["9876543210", "12345", "6123456789", "5123456789"] if re.fullmatch(r"[6-9]\\d{9}", p)])
''', explain='A regular expression expresses the validity rule precisely.'),
    dict(level='medium', title='Reconcile totals', stmt='Source total Rs 15,43,289; lake total Rs 15,43,164. Print the difference and whether it is within Rs 100.', inp='two totals',
         code='''d = 15_43_164 - 15_43_289
print(d, "OK" if abs(d) <= 100 else "MISMATCH")
''', explain='Consistency checks compare systems; tolerances must be agreed with the owner.'),
    dict(level='advanced', title='Pseudonymous key', stmt='Print the first 10 hex characters of SHA-256 of "salt" + "asha@example.com".', inp='email',
         code='''import hashlib
print(hashlib.sha256(("salt" + "asha@example.com").encode()).hexdigest()[:10])
''', explain='The same input always gives the same key, so joins still work.'),
    dict(level='advanced', title='Retention check', stmt='Partitions older than 365 days must be deleted. Given ages [12, 400, 365, 800, 90], print those to delete.', inp='ages in days',
         code='''print([a for a in [12, 400, 365, 800, 90] if a > 365])
''', explain='Retention rules limit how long personal data is kept.'),
    dict(level='business', title='Cost of bad data', stmt='Each wrongly refunded order costs Rs 240. Duplicates caused 1,850 wrong refunds last month. Print the loss and the yearly loss.', inp='1,850 × Rs 240',
         code='''m = 1_850 * 240
print(f"Rs {m:,} per month, Rs {m * 12:,} per year")
''', explain='Putting a rupee value on quality issues helps prioritise fixes.'),
    dict(level='business', title='Quality score', stmt='A table passed 46 of 50 checks this week. Print the quality score and whether it meets the 95% target.', inp='46/50',
         code='''s = 46 / 50
print(f"{s:.0%}", "meets target" if s >= 0.95 else "below target")
''', explain='A simple score per table makes quality visible to owners.'),
]

SCN_INTRO = 'Quality, security and privacy questions from real projects and interviews. Decide your answer first, then open the model answer.'
SCENARIOS = open(os.path.join(HERE, 'scenarios.html'), encoding='utf-8').read()
