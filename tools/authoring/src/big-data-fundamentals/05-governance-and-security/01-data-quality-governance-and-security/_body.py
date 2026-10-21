import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = box(14, 16, 290, 124, 'red') + t(159, 38, 'Monday 9:30 am · revenue dashboard', 9.6, 'red', bold=True)
sc += t(159, 76, 'Yesterday: ₹38.6 crore', 15, 'red', bold=True) + t(159, 100, '(usual: ₹38.6 lakh)', 9.4, 'ink2') + t(159, 124, 'CEO forwards it: “Is this real?”', 8.8, 'ink2')
sc += t(327, 84, '+', 18, 'ink3', bold=True)
sc += box(350, 16, 276, 124, 'amber') + t(488, 38, 'Same week, a second problem', 9.6, 'amber', bold=True)
sc += t(364, 64, '• a shared sheet has 2 lakh customer', 8.8, anchor='start') + t(364, 80, '   phone numbers, open to “anyone', 8.8, anchor='start') + t(364, 96, '   with the link”', 8.8, anchor='start') + t(364, 120, '• found by a vendor, not by us', 8.8, 'red', anchor='start')
scene_svg = scene('A revenue dashboard showing 38.6 crore instead of the usual 38.6 lakh, and a spreadsheet of customer phone numbers shared publicly.', sc,
                  'Wrong data and leaked data are <tspan font-weight="700" class="s-acc">both big data failures</tspan>.')

story = f'''  <div class="story">
    <p class="narration">On Monday morning TiffinGo’s revenue dashboard shows ₹38.6 crore for Sunday, a hundred times the usual figure. The CEO forwards it to the whole leadership group with one line: “Is this real?” By noon Kabir finds the cause: the payments team started sending amounts in paise instead of rupees, and nothing in the pipeline checked. On Wednesday a vendor reports that a spreadsheet with two lakh customer phone numbers is open to anyone with the link.</p>

{scene_svg}

K> Sir, the pipeline didn’t fail. Every job was green. That’s what scares me.
A> That’s the lesson, Kabir. A pipeline can run perfectly and still deliver wrong data. <b>Data quality</b> checks catch that. And knowing who owns each table, where it came from and who may see it is <b>governance</b>.
R> And the phone numbers? That sounds like a security problem, not a data one.
A> It’s both, Riya. Personal data needs protection by design: masking, access control, encryption, audit logs. In India the <b>Digital Personal Data Protection Act, 2023</b> also makes it a legal duty, with penalties of up to ₹250 crore.
K> So quality, governance, security and privacy are four separate jobs?
A> Four sides of one promise: the right data, correct, to the right people, used lawfully. Today you’ll build a quality gate, trace a broken number to its source, mask personal data, and handle a deletion request and a breach the DPDP way.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Quality, governance and security at three levels
L1> Trustworthy data, simply
      <ul>
      <li><b>Data quality</b> means the data is correct and usable: no missing values where needed, no duplicates, sensible ranges, delivered on time.</li>
      <li><b>Governance</b> means clear rules: who owns each dataset, what each column means, who may use it, how long it is kept.</li>
      <li><b>Security</b> means only allowed people and programs can read or change data, and every access is logged.</li>
      <li><b>Privacy</b> means personal data (name, phone, email, location, payments) is collected with consent, used only for the stated purpose and deleted when no longer needed.</li>
      </ul>
L2> How teams put it into practice
      <ul>
      <li><b>Quality dimensions:</b> accuracy, completeness, consistency, timeliness (freshness), validity (format and range) and uniqueness.</li>
      <li><b>Quality checks in pipelines:</b> tests on every load (row counts, nulls, ranges, uniqueness, referential integrity), with bad rows quarantined and the pipeline stopped above a threshold. Tools: Great Expectations, dbt tests, Soda, Deequ, Delta Live Tables expectations.</li>
      <li><b>Governance tools:</b> a <b>data catalog</b> (what exists, owner, meaning), <b>lineage</b> (where data came from and where it goes), <b>classification</b> (tagging PII and sensitive columns) and data contracts between producers and consumers.</li>
      <li><b>Security controls:</b> role-based access (RBAC), column masking and row-level filters, encryption at rest and in transit, secrets in a vault, private networks, audit logs.</li>
      </ul>
L3> Privacy law, observability and hard problems
      <ul>
      <li><b>DPDP Act, 2023 (India):</b> data principals (people) and data fiduciaries (companies); consent that is free, specific and informed, with notice; purpose limitation; rights to access, correction and erasure; reasonable security safeguards; breach notification to the Data Protection Board and affected people; extra duties for children’s data and for Significant Data Fiduciaries.</li>
      <li><b>Erasure at big data scale:</b> deleting one person from a lake means deleting from tables, derived tables, caches, ML features and eventually backups. Table formats (Delta, Iceberg, Hudi) support row-level deletes; pseudonymous keys and separate PII stores make it manageable.</li>
      <li><b>Pseudonymisation vs anonymisation:</b> replacing an email with a salted hash is pseudonymisation (still personal data if it can be linked back); true anonymisation is hard because combinations of columns can re-identify people.</li>
      <li><b>Data observability:</b> monitoring freshness, volume, schema and distribution changes automatically, with alerts, rather than relying only on hand-written tests.</li>
      <li><b>Data mesh and contracts:</b> domain teams own their data products, publish schemas and SLAs as contracts, and breaking changes are caught before deployment.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Data quality</b> is the degree to which data is fit for its intended use, measured along dimensions such as accuracy, completeness, consistency, timeliness, validity and uniqueness. <b>Data governance</b> is the set of roles, policies, standards and processes that ensure data is managed as an asset: ownership and stewardship, metadata and catalogs, lineage, classification, retention and access policies. <b>Data security</b> protects data against unauthorised access, modification and loss through identity and access management, encryption, network controls, monitoring and auditing. <b>Data privacy</b> governs the lawful processing of personal data, in India under the <b>Digital Personal Data Protection Act, 2023</b> and the DPDP Rules, 2025.',
    'Quality: is the data correct? Governance: who owns it, what does it mean, who may use it? Security: is it locked so only the right people can reach it? Privacy: are we using people’s personal data fairly, with their permission, and as the law requires?') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('PII', 'Personally identifiable information: data that identifies a person, such as name, phone, email, Aadhaar or address.'),
    ('Data owner / steward', 'The owner is accountable for a dataset; the steward manages its definitions and quality day to day.'),
    ('Data catalog', 'A searchable inventory of datasets with owners, descriptions, schemas, tags and usage.'),
    ('Lineage', 'The path data takes from sources through transformations to reports and models.'),
    ('Quarantine', 'Holding bad rows aside for review instead of loading them into trusted tables.'),
    ('Masking', 'Hiding part or all of a value (XXXXXX8843) for users who don’t need the full value.'),
    ('Pseudonymisation', 'Replacing identifiers with tokens or salted hashes so data can be joined without exposing identity.'),
    ('Data fiduciary / principal', 'Under DPDP: the organisation deciding how personal data is processed / the person the data is about.'),
]) + '''

  <h3>DPDP Act and Rules: the key facts (as of October 2026)</h3>
''' + facts([
    ('Law and rules', 'Digital Personal Data Protection Act, 2023; DPDP Rules, 2025 notified in November 2025, with phased implementation'),
    ('Timeline', 'Data Protection Board set up first; consent-manager provisions from about November 2026; most obligations from about May 2027 (the government has consulted on shortening this for large companies)'),
    ('Breach', 'Inform the Data Protection Board and affected people without delay; a detailed report to the Board within 72 hours'),
    ('Penalties', 'Up to ₹250 crore for failing to take reasonable security safeguards; up to ₹200 crore for not notifying a breach or for children’s-data violations'),
]) + '''
  <p class="muted">This is a learning summary, not legal advice. Check the current Act, Rules and notifications on meity.gov.in before making compliance decisions.</p>
''' + lv + '''
EXAM> List the <b>six data quality dimensions</b> with an example each, define <b>data governance</b> and its components (<b>ownership, catalog, lineage, classification, policies</b>), and name the main rights of a data principal and duties of a data fiduciary under the <b>DPDP Act, 2023</b>.'''

# ---------------------------------------------------------------- types
types = table(['Dimension', 'Question it answers', 'Example check at TiffinGo'], [
    ['<b>Accuracy</b>', 'Does the value match reality?', 'Order amounts agree with payment-gateway settlement totals'],
    ['<b>Completeness</b>', 'Is anything missing?', 'City is never empty; yesterday has orders from every city'],
    ['<b>Consistency</b>', 'Do systems agree with each other?', 'Order count in the lake equals the count in the orders database'],
    ['<b>Timeliness</b>', 'Is it fresh enough?', 'Yesterday’s gold table is ready by 6:00 am'],
    ['<b>Validity</b>', 'Is it in the right format and range?', 'Phone is 10 digits starting 6–9; amount between ₹1 and ₹50,000'],
    ['<b>Uniqueness</b>', 'Are there duplicates?', 'Each order_id appears exactly once'],
], minw=600) + '''

  <h3>Four pillars of trustworthy data</h3>
''' + cards([
    ('Quality', 'Tests and monitors on every pipeline: row counts, nulls, ranges, uniqueness, freshness, reconciliation with source systems.', 'Correct'),
    ('Governance', 'Owners and stewards, a catalog with business definitions, lineage, classification tags, retention rules and data contracts.', 'Understood'),
    ('Security', 'Least-privilege access, masking and row filters, encryption, secrets management, private networks, audit logs.', 'Protected'),
    ('Privacy', 'Consent and notice, purpose limitation, minimisation, rights requests (access, correction, erasure), breach handling under DPDP.', 'Lawful'),
]) + '''
TIP> A cheap rule that saves careers: <b>never publish a table you haven’t tested</b>, and <b>never copy personal data to a place that is less protected than its source</b> (a laptop, a shared sheet, a test environment).'''

# ---------------------------------------------------------------- steps
c1 = '''rows = [120, 450, -150, 300, 0, 99000]
bad = [r for r in rows if not 1 <= r <= 50_000]
print("bad:", bad, f"-> {len(bad) / len(rows):.0%} failed")'''
c2 = '''phone = "9876543210"
print("masked:", "XXXXXX" + phone[-4:])'''
steps = stepper([
    ('Classify the data',
     '<p>Kabir tags every column in the catalog: <code>phone</code>, <code>email</code>, <code>address</code> as <b>PII</b>; <code>amount</code> as <b>financial</b>; <code>city</code> as <b>internal</b>.</p>',
     'You can’t protect what you haven’t labelled. Tags drive masking, access policies and retention automatically.'),
    ('Write quality rules with the owner',
     code('python', 'range_check.py', c1, run_code(c1)),
     'Rules come from business meaning, so the data owner signs off: “amount between ₹1 and ₹50,000”, “one row per order”, “ready by 6 am”.'),
    ('Gate the pipeline',
     '<p>Checks run after every load. Bad rows go to a quarantine table; if more than 2% fail, the pipeline stops and alerts the owner instead of publishing.</p>',
     'A stopped pipeline with an alert is far better than a confident wrong dashboard.'),
    ('Mask and restrict',
     code('python', 'mask.py', c2, run_code(c2)),
     'Analysts get masked phones and pseudonymous customer keys; only the support tool can see full numbers, and every lookup is logged.'),
    ('Record lineage and ownership',
     '<p>Each table in the catalog shows its owner, description, upstream sources and downstream dashboards, captured automatically from pipeline code where possible.</p>',
     'When a number looks wrong, lineage turns hours of guessing into minutes of tracing.'),
    ('Plan for rights and breaches',
     '<p>A runbook says how to find and delete one customer everywhere, how long each table is kept, and who notifies the Data Protection Board and customers if a breach happens.</p>',
     'DPDP turns these from good ideas into legal duties with deadlines.'),
])

# ---------------------------------------------------------------- two-view animation: tracing the wrong number
def dash(val, note, tone='red'):
    return (box(30, 24, 300, 160, 'card') + t(180, 48, 'Revenue · Sunday', 10, bold=True) + t(180, 98, val, 20, tone, bold=True) + t(180, 132, note, 9, 'ink2'))
see = [
    dash('₹38.6 crore', 'usual Sunday: about ₹38.6 lakh'),
    dash('₹38.6 crore', 'Kabir opens the table’s lineage'),
    dash('₹38.6 crore', 'upstream: payments.orders'),
    dash('₹38.6 crore', 'schema change found: amount in paise'),
    dash('₹38.6 lakh', 'fixed and backfilled', 'green'),
    dash('₹38.6 lakh', 'a new check now guards this table', 'green'),
]
def lin(active, red=None, note=''):
    names = [('payments.orders', 14), ('bronze.orders', 102), ('silver.orders', 190), ('gold.revenue', 278)]
    o = ''
    for k, (n, x) in enumerate(names):
        tone = 'red' if red == k else ('acc' if k in active else 'card')
        o += label_box(x, 40, 76, 40, n.split('.'), tone, 8.2)
        if k < 3:
            o += arrow(x + 78, 60, x + 86, 60, 'ink3', 1.6)
    return o + t(180, 112, note, 8.6, 'ink2')
behind = [
    lin([3], 3, 'gold.revenue is 100× too high. All jobs were green.') + t(180, 128, 'No check looked at the values.', 8.6, 'red'),
    lin([2, 3], None, 'Lineage in the catalog shows upstream tables.') + t(180, 128, 'silver.orders sums match gold: not the bug.', 8.6, 'ink2'),
    lin([0, 1], None, 'bronze is a raw copy of payments.orders.') + t(180, 128, 'Median amount jumped from 320 to 32,000.', 8.6, 'red', bold=True),
    lin([0], 0, 'Payments team changed amount to paise on Saturday.') + t(180, 128, 'No data contract, so no one was told.', 8.6, 'red'),
    lin([0, 1, 2, 3], None, 'silver now divides by 100 for new rows;') + t(180, 128, 'Saturday–Sunday partitions are reprocessed.', 8.6, 'green'),
    lin([0, 1, 2, 3], None, 'New: contract on amount unit + range check') + t(180, 128, '(median between ₹100 and ₹2,000) before publish.', 8.6, 'green'),
]
see_caps = ['The dashboard shows ₹38.6 crore for Sunday, about 100 times normal.', 'Kabir opens the gold table in the catalog and clicks Lineage.', 'He follows it upstream to the payments team’s orders table.',
            'The cause: a schema change on Saturday sent amounts in paise.', 'After the fix and backfill, Sunday shows ₹38.6 lakh.', 'A new quality check and a data contract protect the table from now on.']
behind_caps = ['Every job succeeded, so no alert fired. Pipeline monitoring checks that jobs ran, not that values make sense.',
               'The catalog’s lineage graph shows gold.revenue is built from silver.orders, which is built from bronze.orders. The sums agree between silver and gold, so the transformation is not the problem.',
               'Comparing distributions shows the median order amount jumped from about 320 to 32,000 on Saturday, already in the raw bronze copy.',
               'The payments team switched the amount field to paise (a common way to avoid decimals) without telling consumers. There was no data contract or schema review.',
               'Kabir converts new rows in silver and reprocesses the affected date partitions, so history is correct again.',
               'Two protections are added: a data contract with the payments team specifying the unit, and a distribution check that stops publishing if the median amount leaves its normal range.']
two = anim_two('Tracing a wrong number with lineage', 'What Kabir sees, and how the data moved', 'Kabir debugging a revenue dashboard that is 100 times too high',
               'A lineage graph from the payments table through bronze, silver and gold, revealing a schema change in paise', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: quality gate (real numbers from quality_guard.out)
fails = [('amount is positive', 40), ('order_id unique', 30), ('city present', 25), ('phone 10 digits', 15)]
def gate(n, note1, note2, tone, extra=''):
    o = t(14, 22, 'Batch of 10,030 order rows', 9, 'ink2', anchor='start')
    rows = [(a, b / 40 * 100, 'red', str(b)) for a, b in fails[:n]]
    o += bars(rows, x=150, y=32, w=140, gap=20) if rows else t(180, 70, 'running checks…', 10, 'ink2')
    return o + extra + cap(note1, note2, tone, y=150, h=44)
fr1 = [
    gate(0, 'A nightly batch arrives: 10,030 rows of orders.', 'Four checks run before anything is published.', 'blue'),
    gate(2, '40 negative amounts and 30 duplicate order IDs', '(the same order sent twice by a retry).', 'red'),
    gate(4, '25 missing cities, 15 invalid phone numbers.', 'Each failing row goes to a quarantine table.', 'red'),
    gate(4, '9,920 rows pass, 110 quarantined:', 'failure rate 1.10%, below the 2% threshold.', 'amber'),
    gate(4, 'Decision: PUBLISH the good rows, alert the owner', 'about the 110 quarantined rows to review.', 'green'),
]
s1 = anim_one('Real-time scenario 1', 'A quality gate catches 110 bad rows',
              'These figures come from the program in “Run it on your PC” below. Watch a nightly batch pass through four checks before it is allowed into trusted tables.',
              'Quality gate', 'A batch of orders checked for negative amounts, duplicates, missing cities and invalid phones, with bad rows quarantined', fr1,
              ['A nightly batch of 10,030 order rows lands in the lake. Before it reaches analysts, four rules run.',
               'The amount check finds 40 negative values and the uniqueness check finds 30 orders sent twice, a common side effect of retries.',
               'The completeness check finds 25 rows with no city and the validity check finds 15 phones that are not 10-digit Indian mobile numbers. Failing rows are written to a quarantine table, not deleted.',
               'In total 9,920 rows pass and 110 are quarantined, a failure rate of 1.10%.',
               'Because the rate is below the agreed 2% threshold, the good rows are published and the data owner is alerted to fix the source. Above 2%, the pipeline would stop entirely.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: same table, three roles
def view(role, cols, note1, note2, tone, query=None, heads=('name', 'phone', 'city', 'orders')):
    o = t(180, 22, query or f'SELECT * FROM customers  — as {role}', 9.2, 'blue', mono=True)
    for k, h in enumerate(heads):
        o += t(40 + k * 82, 46, h, 8.8, bold=True, anchor='start')
    for r, row in enumerate(cols):
        for k, v in enumerate(row):
            o += t(40 + k * 82, 66 + r * 18, v, 8.6, 'ink2' if 'X' in v or '█' in v else 'ink', anchor='start', mono=True)
    return o + cap(note1, note2, tone, y=126, h=44)
full = [['Asha P', '9876543210', 'Pune', '14'], ['Ravi K', '9123456780', 'Thane', '3']]
masked = [['█████', 'XXXXXX3210', 'Pune', '14'], ['█████', 'XXXXXX6780', 'Thane', '3']]
fr2 = [
    view('support agent', full, 'Support needs the full phone to call about a', 'late order. Every lookup is written to an audit log.', 'blue'),
    view('analyst', masked, 'Analysts see the same table with names hidden', 'and phones masked: enough for city trends.', 'green'),
    view('analyst (Pune)', [masked[0]], 'A row-level filter also limits the Pune city team', 'to Pune customers only.', 'green'),
    view('', [],  'Export of PII to a laptop or shared sheet is', 'blocked by policy. Wednesday’s leak can’t repeat.', 'red',
         query='EXPORT customers TO shared_sheet  — as intern', heads=()) + t(180, 70, '✗ Denied: table has PII-tagged columns', 10, 'red', bold=True) + t(180, 92, 'Request access with a reason, or export a masked view.', 8.6, 'ink2'),
    view('', [['support_17', 'customers', '42', '11:02'], ['analyst_3', 'customers', '3,910', '02:14']], 'Audit logs show who read which PII and when,', 'so unusual access can be spotted and investigated.', 'amber',
         query='SELECT * FROM audit_log  — as security team', heads=('user', 'table', 'rows', 'time')),
]
s2 = anim_one('Real-time scenario 2', 'One table, different views for different roles',
              'Instead of making copies with columns removed, modern platforms apply masking and row filters when the query runs, based on who is asking. Watch the same query return different results.',
              'Access control and masking', 'The same customers table returned in full to support, masked to analysts, filtered by city, blocked for export, and logged for audit', fr2,
              ['A support agent sees full phone numbers, because calling customers is their job. Each lookup is recorded in an audit log.',
               'An analyst running the same query sees names hidden and phones masked. Column masking policies apply automatically based on the user’s role and the column’s PII tag.',
               'A row-level filter limits the Pune team to Pune customers: least privilege for rows as well as columns.',
               'Policies block exporting PII columns to unmanaged places such as laptops or public sheets, the exact cause of Wednesday’s leak.',
               'Audit logs record who read which sensitive data and when. The second row stands out: one analyst account read 3,910 customer rows at 2:14 am, which the security team investigates.'])

# ---------------------------------------------------------------- scenario 3 (advanced): DPDP erasure and breach
def place(states, note1, note2, tone, title):
    labels = ['orders (lake)', 'features (ML)', 'CRM export', 'backups']
    o = t(180, 20, title, 9.4, bold=True)
    for k, (lab, st) in enumerate(zip(labels, states)):
        x = 14 + k * 84
        tn = {'has': 'amber', 'del': 'green', 'exp': 'blue', 'leak': 'red', 'lock': 'green'}[st]
        sub = {'has': 'has data', 'del': 'deleted', 'exp': 'expires 35 d', 'leak': 'exposed', 'lock': 'access closed'}[st]
        o += label_box(x, 34, 78, 46, [lab, sub], tn, 8.2)
    return o + cap(note1, note2, tone, y=100, h=44)
fr3 = [
    place(['has'] * 4, 'Asha withdraws consent and asks TiffinGo to', 'erase her data. Where does it live?', 'blue', 'Erasure request: customer key 97c8…'),
    place(['del', 'has', 'has', 'has'], 'Lake table: row-level DELETE by customer key', '(Delta/Iceberg), then old file versions vacuumed.', 'amber', 'Erasure request: customer key 97c8…'),
    place(['del', 'del', 'del', 'exp'], 'Features and the CRM export are cleaned; backups', 'expire on schedule and are not restored for her.', 'green', 'Erasure request: customer key 97c8…'),
    place(['has', 'has', 'leak', 'has'], 'Later: a misconfigured CRM export is found', 'publicly readable. A personal data breach.', 'red', 'Breach: 2 lakh phone numbers exposed'),
    place(['has', 'has', 'lock', 'has'], 'Close access, investigate, inform the Board and', 'affected people; detailed report within 72 hours.', 'amber', 'Breach: 2 lakh phone numbers exposed'),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'An erasure request and a breach under the DPDP Act',
              'Privacy law turns data engineering choices into deadlines. Watch how a well-governed lake handles a customer’s erasure request, and what must happen when a breach is found.',
              'DPDP in a data platform', 'Deleting one customer across lake tables, ML features, exports and backups, then responding to a data breach', fr3,
              ['A customer withdraws consent and asks for her data to be erased. Because the platform uses a pseudonymous customer key and a catalog with PII tags, the team can list every place her data lives.',
               'Lake tables in Delta Lake or Iceberg support row-level deletes by key. Old file versions that still contain the row are removed by vacuum or snapshot expiry after the retention window.',
               'Derived ML features and exported copies are deleted too. Backups usually can’t be edited, so they expire on a fixed schedule and are never restored for erased customers. The request and its completion are logged.',
               'Separately, a CRM export bucket is found to be publicly readable with two lakh phone numbers. That is a personal data breach.',
               'The team closes access, investigates scope and cause, and under the DPDP Rules informs the Data Protection Board and affected people without delay, with a detailed report to the Board within 72 hours. Penalties for failing to protect or notify can reach ₹200–250 crore. (Learning summary, not legal advice.)'])

realworld = '''  <p>Three live scenarios: a quality gate on a real batch (numbers from the program below), one table seen through different roles, and an advanced look at erasure requests and breaches under the DPDP Act.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Where you’ll see this at work</h3>
''' + usecase('<rect x="20" y="22" width="80" height="48" rx="8" class="s-soft-green" style="stroke:var(--green)"/><path d="M38 46l10 10 20-20" style="fill:none;stroke:var(--green);stroke-width:4"/>',
              '1. Quality checks in every pipeline', 'Data teams add tests (dbt tests, Great Expectations, Soda, Deequ) to each model and stop publishing on failure. Data observability tools watch freshness, volume and schema automatically.', ['Load', '*Tests + thresholds', 'Publish or stop']) + usecase(
    '<circle cx="34" cy="46" r="12" style="fill:var(--blue);opacity:.6"/><circle cx="86" cy="30" r="10" style="fill:var(--blue);opacity:.4"/><circle cx="86" cy="62" r="10" style="fill:var(--blue);opacity:.4"/><path d="M46 46L76 30M46 46L76 62" style="stroke:var(--ink3);stroke-width:2"/>',
    '2. Catalogs and lineage', 'Unity Catalog, AWS Glue Data Catalog with Lake Formation, Microsoft Purview, Google Dataplex, DataHub and OpenMetadata record owners, descriptions, PII tags and lineage.', ['Pipelines', '*Catalog + lineage', 'Find, trust, debug']) + usecase(
    '<rect x="40" y="36" width="40" height="34" rx="4" class="s-soft-acc" style="stroke:var(--track)"/><path d="M48 36v-8a12 12 0 0 1 24 0v8" style="fill:none;stroke:var(--track);stroke-width:3"/>',
    '3. Banks, fintech and health', 'Regulated sectors combine RBI, SEBI or sector rules with DPDP: tokenised card data, data localisation, strict access reviews and long audit trails.', ['Sensitive data', '*Encrypt, mask, audit', 'Regulator-ready']) + usecase(
    '<rect x="24" y="24" width="72" height="44" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="51" text-anchor="middle" font-size="11" font-weight="700" class="s-blue">DPDP</text>',
    '4. Consumer apps preparing for DPDP', 'Indian apps are building consent records, purpose tags, deletion workflows across lakes and backups, and breach-response runbooks before the main obligations apply.', ['Consent + notice', '*Purpose + retention', 'Erasure + breach plan']) + '''

  <h3>Sources</h3>
  <ul class="muted">
    <li>DPDP Rules timelines, breach reporting and penalties: <a href="https://uniqus.com/digital-personal-data-protection-act-timelines/" rel="noopener">Uniqus, November 2025</a>; Government of India explainer on the DPDP Rules, <a href="https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf" rel="noopener">PIB, November 2025</a>.</li>
    <li>Proposal to shorten compliance timelines: <a href="https://ssrana.in/articles/meity-plans-to-cut-short-dpdp-compliance-timeline-and-notify-cross-border-restrictions-for-sdfs/" rel="noopener">S.S. Rana &amp; Co.</a>, 2026.</li>
  </ul>'''

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Every job was green', story)
        + part(2, 'definition', 'Definition', 'Data quality, governance, security and privacy', definition)
        + part(3, 'types', 'Types and ways to use it', 'Six quality dimensions and four pillars', types)
        + part(4, 'steps', 'Step by step', 'Making a dataset trustworthy', steps)
        + part(5, 'animation', 'See it happen', 'A wrong number: what Kabir sees, and where it came from', '  <p>Step through the six frames. Left: the dashboard Kabir is debugging. Right: the lineage graph that leads him to the cause.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: quality gate, access and privacy law', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Data quality', 'Fresher', 'The dashboard shows 100× revenue',
            'A revenue dashboard suddenly shows a figure about 100 times higher than usual. All pipeline jobs succeeded.',
            'can you debug a data issue systematically?',
            '<ol><li>Confirm the symptom and its start date; tell stakeholders you are investigating.</li><li>Follow lineage upstream, comparing counts and sums at each layer to find where values change.</li><li>Check for schema or unit changes (rupees to paise), duplicates, or join explosions.</li><li>Fix the transformation and backfill affected partitions.</li><li>Prevent recurrence: range/distribution checks, a data contract with the source team, and alerts.</li></ol>',
            'patching the dashboard number by hand.')
        + scn('Security', '1–3 years', 'Analysts need customer data, safely',
              'Analysts want access to the customers table, which includes names, phones and addresses.',
              'do you apply least privilege without blocking useful work?',
              '<ul><li>Classify columns and tag PII in the catalog.</li><li>Give analysts a view or policy with names removed, phones masked and a pseudonymous customer key for joins.</li><li>Use row-level filters where teams should see only their region.</li><li>Keep full access for the few roles that need it, with audit logs and periodic access reviews.</li><li>Block exports of PII to unmanaged locations.</li></ul>',
              'giving everyone full access “just for now”, or refusing access entirely.')
        + scn('Privacy · DPDP', '1–3 years', 'Delete one customer from the lake',
              'A customer withdraws consent and asks for erasure. Their data is in raw files, Delta tables, ML features and nightly backups.',
              'do you understand erasure at big data scale?',
              '<p>Use the catalog and a pseudonymous key to find all locations. Run row-level deletes on table-format tables (Delta, Iceberg, Hudi), rewrite or expire raw files, vacuum old versions after the retention window, delete derived features and exports, and let immutable backups expire on schedule without restoring erased customers. Record the request and completion. Design ahead: keep PII in few places, separate it from event data, and use keys that make deletion cheap.</p>',
              'saying “data lakes are append-only, so we can’t delete”.')
        + scn('Fundamentals · interview', 'Fresher', '“What is data governance?”',
              'A common interview and exam question.',
              'can you define it with concrete components and tools?',
              '<p>Data governance is the framework of roles, policies and processes that keeps data <b>accurate, understood, secure and used lawfully</b>. Components: ownership and stewardship, a data catalog with business definitions, lineage, classification of sensitive data, quality rules and monitoring, access policies, retention and deletion rules, and compliance with laws such as India’s DPDP Act. Tools include Unity Catalog, Purview, Dataplex, Glue Data Catalog with Lake Formation, DataHub and OpenMetadata.</p>',
              'describing governance only as “security”.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
