import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = ''
tiles = [('UPI', '80 crore+', 'payments a day', 'blue'), ('IRCTC', '37,410', 'tickets in one minute', 'green'),
         ('Live cricket', '5.9 crore', 'watching at once', 'acc'), ('Sale day', 'crores', 'of product page views', 'violet')]
for k, (a, b, c, tone) in enumerate(tiles):
    x = 14 + k * 154
    sc += box(x, 20, 144, 112, tone) + t(x + 72, 44, a, 10, tone, bold=True) + t(x + 72, 80, b, 15, bold=True) + t(x + 72, 104, c, 8.6, 'ink2')
scene_svg = scene('Four Indian systems at huge scale: UPI with over 80 crore payments a day, IRCTC with 37,410 tickets in one minute, live cricket with 5.9 crore concurrent viewers, and online sale days with crores of page views.', sc,
                  'India runs some of the <tspan font-weight="700" class="s-acc">largest real-time systems in the world</tspan>.')

story = f'''  <div class="story">
    <p class="narration">It is 9:59 am. Kabir has two browser tabs open: the IRCTC Tatkal page for his mother’s ticket home, and the TiffinGo dashboard, where lunch orders are about to spike. At 10:00 both pages slow down. He books the ticket after a short wait in a queue, pays by UPI in two seconds, and opens the cricket stream on his phone during lunch, where crores of people are watching the same over.</p>

{scene_svg}

K> Sir, our app struggles with a few thousand lunch orders a minute. How does UPI handle 80 crore payments a day? How does IRCTC survive Tatkal?
A> They use the same ideas you’ve learnt in this course, at a bigger size: partitioning, replication, queues, caches, streams and lakes. Today we’ll open up four Indian systems and see which ideas carry the weight.
R> Do we know exactly how they’re built inside?
A> Good question, Riya. Only partly. NPCI, IRCTC and the streaming and e-commerce companies publish some numbers and talks, but not their full designs. So we’ll be careful: published figures are marked with sources, and the rest is the standard pattern any engineer would use for that problem.
K> So I can learn to design for crores of users by studying these four?
A> Yes. And you’ll do the arithmetic yourself: turning “80 crore a day” into requests per second, peaks and terabytes is the first skill interviewers check.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> India-scale systems at three levels
L1> What “India scale” means
      <ul>
      <li><b>Many users at the same moment:</b> Tatkal at 10 am, the last over of a final, midnight sale launches. The problem is the <i>peak</i>, not the daily average.</li>
      <li><b>Every request matters:</b> a lost payment or a double-booked berth is a serious failure, so correctness is as important as speed.</li>
      <li><b>Huge variety of devices and networks:</b> cheap phones, 2G to 5G, many languages. Systems must be light and tolerant of slow connections.</li>
      <li><b>All of it creates data:</b> each payment, booking and video second becomes an event for fraud checks, dashboards, recommendations and reports.</li>
      </ul>
L2> The patterns behind each system
      <ul>
      <li><b>UPI:</b> a central switch (NPCI) routes requests between payment apps and banks; it is an online transaction system that needs strong consistency for money, with streaming fraud checks beside it.</li>
      <li><b>IRCTC:</b> a short, extreme peak; standard answers are waiting rooms, rate limits, caching of read-heavy pages (availability, fares), and a carefully protected seat-allocation core.</li>
      <li><b>Live streaming:</b> video is cut into small segments and pushed through CDNs (servers close to viewers), with adaptive bitrate; event data streams into analytics for ads and quality.</li>
      <li><b>E-commerce sales:</b> catalogue and search served from caches and search clusters, inventory and orders sharded and protected, clickstream into Kafka and a lakehouse for real-time dashboards and recommendations.</li>
      </ul>
L3> Design trade-offs at peak
      <ul>
      <li><b>Peak-to-average ratio:</b> design capacity for the peak (often several times the average) plus headroom; pre-scale for known events instead of relying only on autoscaling, which may react too slowly.</li>
      <li><b>Backpressure and load shedding:</b> admit at a safe rate (queues, tokens), degrade gracefully (turn off recommendations before checkout), and fail fast instead of piling up timeouts.</li>
      <li><b>Consistency where it matters:</b> money and seats need strong consistency and idempotency (a retried payment must not debit twice); counters, views and recommendations can be eventually consistent.</li>
      <li><b>Hot keys:</b> one train, one match or one product can overload a single partition; caching, request coalescing and splitting hot keys spread the load.</li>
      <li><b>Data platform behind it:</b> every event goes to streams (for fraud, live dashboards) and to the lake (for reconciliation, reports, ML), often under data-residency rules.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Large-scale systems</b> serve very high numbers of users and transactions with strict requirements on <b>throughput</b>, <b>latency</b>, <b>availability</b> and <b>correctness</b>. Designing them involves estimating load (average and <b>peak</b> requests per second, data volume), and applying distributed-systems techniques: horizontal scaling, partitioning, replication, caching, <b>content delivery networks</b>, asynchronous messaging, rate limiting and load shedding, together with streaming and batch data platforms that capture every event for monitoring, fraud detection, analytics and audit.',
    'A system is at India scale when crores of people use it, often at the same moment. To survive, it spreads work over many machines, keeps copies, answers repeated questions from caches, makes people wait in fair queues during rushes, and records every action as data for later analysis.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('TPS / RPS', 'Transactions or requests per second: the basic unit of load.'),
    ('Peak-to-average ratio', 'How many times busier the busiest second is than the average second.'),
    ('Concurrency', 'How many users or requests are active at the same moment.'),
    ('CDN', 'Content delivery network: servers near users that cache and deliver content such as video segments.'),
    ('Waiting room', 'A queue in front of a system that admits users at a rate the system can handle.'),
    ('Idempotency', 'Doing the same request twice has the same effect as doing it once (no double debit).'),
    ('Hot key', 'A single key (train, match, product) receiving a disproportionate share of traffic.'),
    ('Load shedding', 'Deliberately rejecting or simplifying some work to protect the core under overload.'),
]) + '''

  <h3>Published figures used in this lesson</h3>
''' + facts([
    ('UPI, September 2026', '24.07 billion transactions worth ₹29.37 lakh crore; about 80.2 crore a day on average (August 2026 set the record at 24.51 billion)'),
    ('IRCTC', 'peak of 37,410 tickets booked in one minute (16 Aug 2025); record 18.4 lakh tickets in a day (19 Aug 2025); about 89% of reserved tickets booked online'),
    ('Live streaming', '5.9 crore peak concurrent viewers on Disney+ Hotstar for the 2023 ICC World Cup final, India vs Australia'),
]) + '''
  <p class="muted">Sources are listed at the end of the Real-world use section. Internal designs of these systems are not fully public: the architecture shown here is the standard pattern for each problem, not a confirmed blueprint.</p>
''' + lv + '''
EXAM> For a case study, give <b>scale figures</b> (with source and date), convert them to <b>TPS at average and peak</b>, then explain the techniques used: <b>horizontal scaling, partitioning, replication, caching/CDN, queues and rate limiting</b>, and how events flow to a <b>streaming and batch analytics</b> platform.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Payments: UPI', 'Short, critical transactions between apps and banks via a central switch. Needs strong consistency, idempotency and fraud checks within the payment flow.', 'Money'),
    ('Booking rush: IRCTC', 'Huge spikes at fixed times (Tatkal opens at 10 am for AC classes and 11 am for non-AC). Limited inventory, so fairness and no double-booking matter.', 'Spikes'),
    ('Live streaming: cricket', 'Crores watch the same content at the same moment. Read-only, so CDNs and caching carry the load; the challenge is bandwidth and sudden joins.', 'Bandwidth'),
    ('E-commerce sales', 'Midnight launches with huge browsing, cart and checkout traffic, limited stock of hot deals, and real-time dashboards for the business.', 'Mixed'),
]) + '''

  <h3>Which big data ideas carry each system</h3>
''' + table(['System', 'Main challenge', 'Key techniques', 'Data platform behind it'], [
    ['<b>UPI</b>', 'Correct money movement at thousands of TPS, high availability', 'Central switch, partitioned and replicated transaction stores, idempotent request IDs, timeouts and reversals', 'Streaming fraud and risk scoring; daily settlement and reconciliation; regulatory reports'],
    ['<b>IRCTC</b>', 'A very short, extreme peak on limited seats', 'Waiting room and rate limiting, cached availability and fares, protected seat-allocation core, captcha and bot controls', 'Booking and search logs for demand forecasting, fraud (bots, agents) and capacity planning'],
    ['<b>Live cricket</b>', 'Crores of concurrent viewers joining in minutes', 'Segmented video, adaptive bitrate, multi-CDN, pre-scaling before key moments, graceful degradation', 'Playback events streamed for quality of experience and ads; concurrency dashboards'],
    ['<b>Sale day</b>', 'Browsing, carts and checkout spike; hot products', 'Caching catalogue and search, sharded inventory and orders, queues for order processing, feature flags to switch off extras', 'Clickstream into Kafka and a lakehouse; live sales dashboards; recommendations and pricing'],
], minw=720) + '''
TIP> Every one of these systems separates the <b>critical path</b> (pay, book, play, order) from <b>everything else</b> (analytics, recommendations, notifications). Under pressure, the extras are queued or switched off so the critical path survives.'''

# ---------------------------------------------------------------- steps
c1 = '''per_month = 24.07e9
per_day = per_month / 30
print(f"{per_day / 1e7:.1f} crore a day")
print(f"{per_day / 86_400:,.0f} per second on average")'''
c2 = '''avg_tps = 9_286
for ratio in [2, 3, 5]:
    print(f"peak x{ratio}: {avg_tps * ratio:,} TPS")'''
c3 = '''tps, bytes_per_event = 9_286, 1_000
gb_per_day = tps * 86_400 * bytes_per_event / 1e9
print(f"{gb_per_day:,.0f} GB of events a day, {gb_per_day * 365 / 1e3:,.0f} TB a year")'''
steps = stepper([
    ('Start from a published number',
     code('python', 'per_second.py', c1, run_code(c1)),
     'Monthly or daily totals sound huge, but systems are designed in requests per second. 24 billion a month is about 9,300 per second on average.'),
    ('Estimate the peak',
     code('python', 'peak.py', c2, run_code(c2)),
     'Traffic is not flat: evenings, salary days, festivals and sale launches are much busier. Designers use a peak-to-average ratio from history and add headroom on top.'),
    ('Find the critical path',
     '<p>For UPI: app → switch → payer bank → payee bank → confirmations. For IRCTC: search → availability → seat allocation → payment. Only these steps must succeed in real time.</p>',
     'Everything else (rewards, notifications, analytics) can be asynchronous through queues, so it never slows the critical path.'),
    ('Spread and protect the load',
     '<p>Partition data and traffic (by account, train, region), replicate for failures, cache what is read often, and put a queue or rate limiter in front of anything that can be overwhelmed.</p>',
     'These are the Module 3 ideas: scale out, shard, replicate, choose consistency per data type.'),
    ('Size the data platform',
     code('python', 'event_volume.py', c3, run_code(c3)),
     'Each transaction creates events for fraud checks, dashboards and audit. Even small events add up to terabytes a year, before replication and logs.'),
    ('Rehearse the big day',
     '<p>Load-test at the expected peak plus margin, pre-scale capacity before the event, prepare switches to turn off non-essential features, and watch live dashboards during the event.</p>',
     'Known peaks (Tatkal, a final, a sale) are planned like launches, with game days and runbooks, not left to chance.'),
])

# ---------------------------------------------------------------- two-view animation: one UPI payment
def phone(title, inner):
    return ('<rect x="110" y="10" width="140" height="196" rx="16" class="s-board"/><rect x="118" y="26" width="124" height="166" rx="6" class="s-card2"/>' + t(180, 44, title, 9, bold=True) + inner)
see = [
    phone('Scan & pay', t(180, 80, 'Sharma Tiffins', 9.4, bold=True) + t(180, 108, '₹ 120', 16, bold=True) + t(180, 150, 'Pay ▶', 10, 'acc', bold=True)),
    phone('Enter UPI PIN', t(180, 96, '● ● ● ●', 14, bold=True) + t(180, 140, 'PIN stays on the phone,', 8, 'ink2') + t(180, 154, 'encrypted', 8, 'ink2')),
    phone('Processing', t(180, 104, 'Please wait…', 9.4, 'ink2') + t(180, 124, 'about 1 second', 8.6, 'ink2')),
    phone('Processing', t(180, 104, 'Please wait…', 9.4, 'ink2') + t(180, 124, 'still under 2 seconds', 8.6, 'ink2')),
    phone('Paid', t(180, 96, '✓', 26, 'green', bold=True) + t(180, 126, '₹120 paid', 10, 'green', bold=True) + t(180, 144, 'Ref 6123…', 8, 'ink2')),
    phone('Done', t(180, 92, 'Shop speaker:', 9, 'ink2') + t(180, 112, '“₹120 received”', 9.6, bold=True) + t(180, 150, 'SMS from bank', 8.6, 'ink2')),
]
def flow(active, note):
    nodes = [('Payer app', 18, 'blue'), ('NPCI switch', 108, 'acc'), ('Payer bank', 198, 'violet'), ('Payee bank', 288, 'green')]
    o = ''
    for k, (n, x, tone) in enumerate(nodes):
        o += label_box(x - 4, 40, 64, 40, n.split(' ', 1) if ' ' in n else [n], tone if k in active else 'card', 8.4)
    return o + t(180, 112, note, 8.6, 'ink2')
behind = [
    flow([0], 'The app builds a request with a unique transaction ID.') + t(180, 128, 'The ID makes retries safe (idempotency).', 8.6, 'ink2'),
    flow([0, 1], 'Request + encrypted PIN goes to the NPCI UPI switch,') + t(180, 128, 'which routes by the payer’s bank handle.', 8.6, 'ink2'),
    flow([1, 2], 'Payer bank verifies the PIN and balance,') + t(180, 128, 'debits ₹120 and replies to the switch.', 8.6, 'ink2'),
    flow([1, 3], 'Switch asks the payee bank to credit ₹120.') + t(180, 128, 'If credit fails, the debit is reversed.', 8.6, 'red'),
    flow([0, 1, 2, 3], 'Confirmations flow back to both apps.') + t(180, 128, 'One of ~9,300 payments that second, on average.', 8.6, 'acc', bold=True),
    flow([1], 'Every step was logged as events:') + t(180, 128, 'fraud scoring, dashboards, settlement, disputes.', 8.6, 'ink2'),
]
see_caps = ['Riya scans the tiffin shop’s QR code and taps Pay for ₹120.', 'She enters her UPI PIN.', 'The app shows “Processing”.', 'Still processing, under two seconds so far.',
            'Payment successful, with a reference number.', 'The shop’s speaker announces the payment and her bank sends an SMS.']
behind_caps = ['Her UPI app creates a payment request with a unique transaction ID, so a network retry can never debit her twice.',
               'The request, with the PIN encrypted, goes to NPCI’s UPI switch, which routes it to Riya’s bank based on her UPI handle.',
               'Riya’s bank checks the PIN and balance and debits ₹120, then responds to the switch.',
               'The switch sends a credit request to the shop’s bank. If the credit fails or times out, the debit is reversed: money must never vanish.',
               'Confirmations go back to both sides. This is one of roughly 9,300 UPI payments in an average second in September 2026, and many more at peak.',
               'Every step is recorded. These events feed fraud and risk models, live monitoring, daily settlement between banks and dispute handling. (Simplified flow; real UPI has more checks and messages.)']
two = anim_two('One UPI payment', 'What Riya sees, and what happens behind', 'Riya paying ₹120 by UPI on her phone',
               'A UPI payment request going from the app to the NPCI switch, the payer bank and the payee bank, and back', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: waiting room (real numbers from indian_scale.out)
def room(waiting, admitted, note1, note2, tone, server_load='250/s'):
    dots = round(waiting / 320)
    o = box(14, 24, 150, 110, 'amber') + t(89, 42, 'Waiting room', 9.4, 'amber', bold=True)
    for i in range(min(dots, 48)):
        o += fill(24 + (i % 12) * 11, 54 + (i // 12) * 14, 8, 10, 'amber', rx=2, opacity=.7)
    o += t(89, 126, f'{waiting:,} waiting' if waiting else 'empty', 8.6, bold=True)
    o += arrow(168, 78, 206, 78, 'green', 2) + t(187, 68, server_load, 8.4, 'green', bold=True)
    o += box(210, 24, 136, 110, 'green') + t(278, 42, 'Booking system', 9.4, 'green', bold=True) + t(278, 80, f'{admitted:,}', 14, bold=True) + t(278, 98, 'users admitted', 8.6, 'ink2')
    return o + cap(note1, note2, tone, y=146, h=44)
fr1 = [
    room(0, 0, '9:59:59. The booking system can safely take', 'about 250 users a second (illustrative).', 'blue'),
    room(3_750, 3_750, '10:00:15. Users arrive far faster than 250/s.', 'Extra arrivals wait in the queue, not on the servers.', 'amber'),
    room(15_000, 15_000, '10:01:00. 30,000 users have arrived in one minute.', 'Admitted so far: 15,000; the rest see their place.', 'amber'),
    room(7_500, 22_500, '10:01:30. Arrivals have stopped; the queue drains', 'at a steady 250 per second.', 'amber'),
    room(0, 30_000, '10:02:00. Everyone admitted after 120 s.', 'Median wait 30 s, worst 60 s, servers never overloaded.', 'green'),
]
s1 = anim_one('Real-time scenario 1', 'Tatkal at 10 am: a waiting room protects the booking system',
              'These figures come from the program in “Run it on your PC” below: 30,000 users arrive in one minute, but the booking system admits only 250 per second. Watch the queue absorb the spike.',
              'Virtual waiting room', 'A waiting room queue absorbing 30,000 users arriving in one minute and admitting 250 per second to the booking system', fr1,
              ['Just before 10 am the booking system is ready. Load tests say it can safely handle about 250 users entering the booking flow per second (an illustrative number).',
               'At 10:00 thousands arrive every second. Instead of letting them all hit the servers (which would make everything time out), a waiting room queues them and admits 250 per second.',
               'After one minute 30,000 users have arrived. Half have been admitted; the rest see a progress message with their position.',
               'No new users arrive after the first minute, and the queue drains at a steady 250 per second.',
               'Everyone is admitted after 120 seconds. The median user waited 30 seconds and the unluckiest 60, while the booking servers never saw more than 250 users a second. A fair, predictable wait beats a crash.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: UPI peak with idempotent retry
def bank(state, note1, note2, tone):
    o = label_box(14, 34, 80, 44, ['Payer app', 'txn 7781'], 'blue', 8.6) + label_box(140, 34, 80, 44, ['Switch'], 'acc', 9) + label_box(266, 34, 80, 44, ['Payer bank', state], 'violet', 8.6)
    o += arrow(96, 56, 138, 56, 'ink3', 2) + arrow(222, 56, 264, 56, 'ink3', 2)
    return o + cap(note1, note2, tone, y=120, h=44)
fr2 = [
    bank('balance ₹5,000', 'Salary day evening: traffic is several times', 'the average. A ₹500 request leaves the app.', 'blue'),
    bank('debited ₹500', 'The bank debits ₹500, but its reply is delayed', 'by a congested network link.', 'amber'),
    bank('debited ₹500', 'The app times out and retries with', 'the SAME transaction ID 7781.', 'amber'),
    bank('already done', 'The bank sees ID 7781 was already processed', 'and returns the earlier result. No second debit.', 'green'),
    bank('balance ₹4,500', 'Exactly one debit. Idempotency turns', '“retry” from dangerous into safe.', 'green'),
]
s2 = anim_one('Real-time scenario 2', 'A retry at peak must not debit twice',
              'At peak, slow links and timeouts are normal. Watch how a unique transaction ID makes a retry safe, which is the core reason payment systems can scale out without losing money.',
              'Idempotent payments', 'A UPI payment retried after a timeout, with the bank recognising the same transaction ID and not debiting twice', fr2,
              ['It is a salary-day evening and traffic is far above average. A ₹500 request with transaction ID 7781 goes from the app through the switch to the bank.',
               'The bank debits ₹500, but its response is delayed by congestion somewhere on the path.',
               'The app (or switch) times out and retries the request, carrying the same transaction ID.',
               'The bank stores processed IDs; it recognises 7781 and returns the earlier result instead of debiting again.',
               'The user is charged exactly once. In real UPI, status-check and reversal flows plus daily reconciliation catch any remaining mismatch. Idempotency keys are a standard pattern in every payment system.'])

# ---------------------------------------------------------------- scenario 3 (advanced): live cricket spike
def cdn(viewers, note1, note2, tone, edges=4, hot=False):
    o = label_box(14, 50, 80, 44, ['Origin', 'encoder'], 'violet', 8.6)
    for k in range(edges):
        y = 16 + k * (120 // edges)
        o += arrow(96, 72, 150, y + 11, 'ink3', 1.4) + label_box(152, y, 70, 22, [f'CDN edge {k + 1}'], 'red' if hot and k == 0 else 'green', 8)
    o += t(290, 50, viewers, 13, bold=True) + t(290, 70, 'concurrent', 8.6, 'ink2') + t(290, 84, 'viewers', 8.6, 'ink2')
    return o + cap(note1, note2, tone, y=146, h=44)
fr3 = [
    cdn('1.5 cr', 'Match starts: video cut into 2–6 s segments,', 'each in several bitrates, cached at CDN edges.', 'blue'),
    cdn('3 cr', 'Pre-scaled for the chase: extra edge capacity', 'and several CDN providers booked in advance.', 'blue', edges=5),
    cdn('5.9 cr', 'Last overs of the 2023 World Cup final:', '5.9 crore watching at once (published peak).', 'acc', edges=5, hot=True),
    cdn('5.9 cr', 'Edge 1 is overloaded: viewers are steered to other', 'edges; players drop to a lower bitrate, not freeze.', 'amber', edges=5, hot=True),
    cdn('5.9 cr', 'Playback events stream into analytics:', 'concurrency, buffering, ad delivery, live.', 'green', edges=5),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Crores join the same match in minutes',
              'Live streaming is the opposite of payments: everyone reads the same data. The hard parts are bandwidth, sudden joins and keeping quality up. Watch the standard design at work.',
              'Live streaming at peak', 'A live cricket stream served through an origin and multiple CDN edges as concurrent viewers rise to 5.9 crore', fr3,
              ['The live video is encoded into short segments (a few seconds each) at several qualities. Edge servers of content delivery networks cache segments close to viewers, so the origin serves each segment only a few times.',
               'Big moments are predictable, so capacity is reserved in advance across more than one CDN, instead of waiting for autoscaling to react.',
               'In the 2023 ICC World Cup final, Disney+ Hotstar reported a peak of 5.9 crore concurrent viewers. At even 2.5 Mbps each, that is roughly 148 Tbps of video (our program’s estimate), which only a wide CDN footprint can deliver.',
               'If one edge or network is overloaded, traffic is steered elsewhere and adaptive bitrate lowers quality instead of freezing. Non-essential features (comments, extra stats) can be switched off.',
               'Every player sends events (start, buffering, bitrate changes, ad views) into a streaming pipeline, powering live concurrency dashboards, quality alerts and ad billing, and later the lake for analysis.'])

realworld = '''  <p>Three live scenarios: the Tatkal waiting room (real numbers from the program below), a payment retry at peak that must not debit twice, and an advanced look at serving crores of live cricket viewers.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Four systems, four lessons</h3>
''' + usecase('<rect x="20" y="24" width="80" height="44" rx="8" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="51" text-anchor="middle" font-size="12" font-weight="700" class="s-blue">UPI</text>',
              '1. UPI: correctness at thousands of TPS', 'A central switch connects hundreds of banks and many payment apps. Each payment is small but must be exactly-once in effect; streams of events feed fraud checks and settlement.', ['App', '*NPCI switch', 'Banks + settlement']) + usecase(
    '<rect x="14" y="30" width="92" height="30" rx="6" class="s-soft-green" style="stroke:var(--green)"/><circle cx="34" cy="68" r="6" style="fill:var(--ink3)"/><circle cx="86" cy="68" r="6" style="fill:var(--ink3)"/>',
    '2. IRCTC: survive a fixed-time rush', 'Tatkal creates a predictable spike on limited seats. Waiting rooms, caching of availability, bot controls and a protected booking core keep it fair; IRCTC has announced upgrades for higher booking rates.', ['Users at 10 am', '*Queue + rate limit', 'Seat allocation']) + usecase(
    '<path d="M30 25 L95 45 L30 65 Z" style="fill:var(--acc);opacity:.7"/>',
    '3. Live cricket: bandwidth and sudden joins', 'Segmented video and multi-CDN delivery serve crores of identical reads. Playback events stream into analytics for quality and ad billing.', ['Encoder', '*Multi-CDN edges', 'Crores of phones']) + usecase(
    '<rect x="22" y="26" width="34" height="40" rx="4" class="s-soft-acc" style="stroke:var(--track)"/><rect x="64" y="26" width="34" height="40" rx="4" class="s-soft-acc" style="stroke:var(--track)"/>',
    '4. Sale days: protect checkout', 'E-commerce sales (such as Flipkart’s Big Billion Days and Amazon’s Great Indian Festival) cache the catalogue, shard inventory and orders, queue order processing and switch off extras, while clickstream feeds live dashboards.', ['Browse (cached)', '*Cart + checkout', 'Orders queue']) + '''

  <h3>Sources for the figures</h3>
  <ul class="muted">
    <li>UPI monthly volumes (August and September 2026): NPCI data as reported by <a href="https://startuptalky.com/india-upi-transactions-september-2026/" rel="noopener">StartupTalky, September 2026</a> and <a href="https://startuptalky.com/india-upi-transactions-august-2026-record-volume/" rel="noopener">StartupTalky, August 2026</a>.</li>
    <li>5.9 crore concurrent viewers, 2023 World Cup final: <a href="https://www.exchange4media.com/digital-news/india-aus-final-wc-match-peak-concurrency-touches-59-crore-131034.html" rel="noopener">exchange4media, November 2023</a>.</li>
    <li>IRCTC peaks (37,410 tickets per minute; 18.4 lakh tickets in a day) and online share: Indian Railways figures as reported by IANS and Free Press Journal (2025–26); planned upgrade to over 1 lakh bookings a minute reported by Outlook Money, August 2026.</li>
    <li>Figures are as published; check the latest NPCI and IRCTC releases before quoting them.</li>
  </ul>'''

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', '10:00 am in India', story)
        + part(2, 'definition', 'Definition', 'Big data at Indian scale', definition)
        + part(3, 'types', 'Types and ways to use it', 'Payments, booking rushes, live streaming and sale days', types)
        + part(4, 'steps', 'Step by step', 'From a headline number to a design', steps)
        + part(5, 'animation', 'See it happen', 'One UPI payment: what Riya sees, and what happens behind', '  <p>Step through the six frames. Left: Riya paying a tiffin shop. Right: a simplified view of the request moving through the UPI network.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: rush, retry and live stream', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('System design · estimation', 'Fresher', '“Estimate the load on UPI”',
            'An interviewer says: UPI handles about 24 billion transactions a month. Estimate average and peak TPS and daily event data.',
            'can you turn a headline number into engineering numbers, stating assumptions?',
            '<ol><li>Per day: 24 billion ÷ 30 ≈ 80 crore.</li><li>Average TPS: 80 crore ÷ 86,400 ≈ 9,300.</li><li>Peak: assume 3–5× average at busy hours and festivals → roughly 30,000–45,000 TPS to design for, plus headroom.</li><li>Events: if each transaction produces ~10 events of ~1 KB across systems, that is ~8 TB a day before replication.</li><li>State assumptions clearly and say how you would validate them (published peak figures, traffic history).</li></ol>',
            'giving one number with no assumptions, or designing only for the average.')
        + scn('System design · peaks', '1–3 years', 'Design for Tatkal-style rush hour',
              'Your company runs a ticket sale that opens at a fixed time; last year the site crashed in the first minute.',
              'do you know how to protect a system from a predictable spike?',
              '<ul><li>Estimate peak arrivals from last year and load-test above that.</li><li>Put a <b>virtual waiting room</b> and rate limits in front of the booking flow.</li><li>Cache read-heavy pages (availability, fares) and serve static content from a CDN.</li><li>Pre-scale capacity before opening time; don’t rely only on autoscaling.</li><li>Protect inventory with strong consistency and short seat holds; stop bots with captcha and limits.</li><li>Prepare switches to turn off non-essential features; watch live dashboards.</li></ul>',
              'just adding more servers to the database.')
        + scn('Payments · correctness', '1–3 years', 'A customer was charged twice',
              'During a peak, a few customers were debited twice for one order after network timeouts.',
              'do you understand idempotency and reconciliation?',
              '<p>Retries after a timeout re-sent the payment as a <i>new</i> request. Fix: generate an <b>idempotency key</b> (unique transaction ID) on the client, send it with every retry, and store processed keys on the server so a repeat returns the original result. Add a status-check call before retrying, automatic reversal for failed flows, and a daily <b>reconciliation</b> job comparing your records with the bank or gateway settlement files to catch and refund mismatches.</p>',
              'removing retries entirely, which turns network blips into failed payments.')
        + scn('Case study · interview', 'Fresher', '“How does Hotstar handle crores of live viewers?”',
              'A common case-study question for data and platform roles.',
              'can you explain the standard pattern honestly, without claiming insider knowledge?',
              '<p>Explain that internal details are only partly public, then describe the standard design: video encoded into short segments at multiple bitrates (adaptive streaming), cached and delivered by multiple CDNs close to viewers, origin protected by caching, capacity pre-provisioned before big matches, graceful degradation (lower bitrate, switch off extras) and player events streamed into analytics for concurrency, quality and ad billing. Quote a published figure with source, such as the 5.9 crore concurrent peak in the 2023 World Cup final.</p>',
              'inventing exact server counts or claiming to know their internal architecture.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
