import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
def mini_phone(x, title, big, small, tone):
    return (f'<rect x="{x}" y="14" width="96" height="126" rx="12" class="s-board"/><rect x="{x + 6}" y="26" width="84" height="104" rx="5" class="s-card2"/>'
            + t(x + 48, 42, title, 8.6, bold=True) + t(x + 48, 76, big, 13, tone, bold=True) + t(x + 48, 98, small, 7.8, 'ink2'))
sc = mini_phone(14, 'Riya’s phone', '♥ 1,024', 'likes on her reel', 'red') + mini_phone(120, 'Meera, Delhi', '♥ 1,021', 'same reel, same time', 'red')
sc += t(117, 154, 'different numbers: nobody minds', 8.6, 'ink2')
sc += mini_phone(410, 'UPI · Riya', '₹ 2,350', 'balance', 'green') + mini_phone(516, 'UPI · bank', '₹ 2,350', 'must always match', 'green')
sc += t(513, 154, 'different numbers: unacceptable', 8.6, 'ink2')
sc += t(320, 70, 'vs', 16, 'ink3', bold=True)
scene_svg = scene('Two phones showing different like counts for the same reel, and two screens that must always show the same bank balance.', '<g transform="translate(0,-6)">' + sc + '</g>',
                  '')
scene_svg = scene_svg.replace('<text x="320" y="158" text-anchor="middle" font-size="10.5" class="s-ink2"></text>', '')

story = f'''  <div class="story">
    <p class="narration">Riya posts a reel. On her phone it shows 1,024 likes; at the same moment her cousin Meera in Delhi sees 1,021 on the same reel. Neither of them cares. Five minutes later Riya pays ₹500 by UPI, and the app says <i>“Payment pending, please don’t retry”</i> for ten long seconds.</p>

{scene_svg}

R> Sir, why can Instagram show two different numbers for my likes, but my bank won’t even let me pay until it is sure?
A> Because both are distributed systems, with copies of data in many places, and both face the same unavoidable choice. When the network between copies breaks, a system can either stay <b>available</b> and risk different answers, or stay <b>consistent</b> and refuse some requests.
K> That’s the CAP theorem! Consistency, Availability, Partition tolerance: pick two?
A> That’s the popular slogan, Kabir, and it’s slightly misleading. Networks <i>will</i> break sometimes, so partition tolerance isn’t optional. The real choice is: <b>when a partition happens</b>, do you give up consistency or availability? Likes choose availability. Money chooses consistency.
R> And when the network is fine?
A> Then there is a quieter trade-off between <b>speed</b> and consistency, called PACELC. Today you’ll see both, merge a shopping cart after a split, and learn the ladder of consistency models from “eventual” to “strong”.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> CAP and consistency at three levels
L1> Two bank branches and a broken phone line
      <p>Imagine one bank account managed by two branches that phone each other after every transaction. One day the phone line breaks.</p>
      <ul>
        <li><b>Choose consistency:</b> both branches refuse withdrawals until the line is fixed. No mistakes, but customers are turned away (not available).</li>
        <li><b>Choose availability:</b> both branches keep serving customers. Nobody is turned away, but the two branches may now disagree about the balance (not consistent), and someone could withdraw the same money twice.</li>
      </ul>
      <p>Banks choose consistency for balances. Social apps choose availability for likes and views. Both are correct for their data.</p>
L2> CP and AP systems, and common myths
      <ul>
        <li><b>C (consistency)</b> in CAP means <i>linearizability</i>: every read sees the latest successful write, as if there were one copy. <b>A (availability)</b> means every request to a working node gets a non-error response. <b>P (partition tolerance)</b> means the system keeps operating when messages between nodes are lost.</li>
        <li><b>CP examples:</b> ZooKeeper, etcd, HBase, MongoDB with majority reads and writes, most relational databases with synchronous replication. In a partition, the minority side refuses requests.</li>
        <li><b>AP examples:</b> Cassandra and DynamoDB-style stores at low consistency levels, DNS, many caches. In a partition, every side answers, and copies reconcile later (<b>eventual consistency</b>).</li>
        <li><b>Myth 1:</b> “pick any two”. A distributed system can’t give up P, so “CA” really means “not distributed” (or “stops working during a partition”).</li>
        <li><b>Myth 2:</b> the choice is fixed for a whole system. Many databases let you choose per query (Cassandra consistency levels, DynamoDB strongly consistent reads).</li>
      </ul>
L3> PACELC, the consistency ladder and conflict resolution
      <ul>
        <li><b>PACELC</b> (Daniel Abadi): if there is a <b>P</b>artition, choose <b>A</b> or <b>C</b>; <b>E</b>lse, choose <b>L</b>atency or <b>C</b>onsistency. Strong consistency needs coordination even on good days, which costs round trips, especially across regions.</li>
        <li><b>Consistency ladder</b> (strongest to weakest): <i>linearizable</i> (real-time order, one copy illusion) → <i>sequential</i> (one agreed order) → <i>causal</i> (cause before effect, e.g. a reply never appears before its comment) → <i>session guarantees</i> (read-your-writes, monotonic reads) → <i>eventual</i> (copies converge if writes stop).</li>
        <li><b>Conflict resolution in AP systems:</b> last-write-wins (simple, but silently drops concurrent updates and depends on clocks), version vectors (detect concurrent versions and keep both), and <b>CRDTs</b> (data types like counters and sets designed to merge automatically and correctly).</li>
        <li><b>Global strong consistency:</b> Google Spanner uses tightly synchronised clocks (TrueTime) and consensus to offer linearizable transactions across regions, at the cost of commit latency.</li>
        <li><b>Design rule:</b> decide consistency <i>per piece of data</i>: balances, inventory counts and seat bookings need strong guarantees; likes, views, recommendations and analytics can be eventual.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    'The <b>CAP theorem</b> (conjectured by Eric Brewer in 2000 and proved by Seth Gilbert and Nancy Lynch in 2002) states that a distributed data store cannot simultaneously guarantee <b>Consistency</b> (every read receives the most recent write, i.e. linearizability), <b>Availability</b> (every request to a non-failing node receives a response) and <b>Partition tolerance</b> (the system continues to operate despite lost messages between nodes). Since network partitions cannot be ruled out, a system must choose, during a partition, between consistency (CP) and availability (AP). <b>Consistency models</b> describe the guarantees a system gives about the order and visibility of reads and writes, from strong (linearizable) to eventual consistency.',
    'When copies of data are on different machines and the network between them breaks, a system has two choices: keep answering (and possibly give different answers on each side), or refuse some requests until it can be sure every answer is correct. It can’t do both. Banks refuse; social media keeps answering.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Network partition', 'A failure where some nodes can’t communicate with others, though each may still be running.'),
    ('Linearizability', 'The strongest consistency: the system behaves as if there were one copy, and reads see the latest completed write.'),
    ('Eventual consistency', 'If no new writes happen, all copies eventually become the same.'),
    ('CP system', 'Stays consistent during a partition by refusing requests on the minority side.'),
    ('AP system', 'Stays available during a partition, allowing copies to differ for a while.'),
    ('PACELC', 'Extension of CAP: without partitions, there is still a latency vs consistency trade-off.'),
    ('Causal consistency', 'Effects are never seen before their causes.'),
    ('CRDT', 'Conflict-free replicated data type: a structure that merges concurrent updates automatically.'),
]) + '''

  <h3>Where common systems sit (default settings)</h3>
''' + facts([
    ('CP-leaning', 'ZooKeeper, etcd, HBase, Google Spanner, MongoDB (majority read/write concern), relational databases with synchronous replicas'),
    ('AP-leaning', 'Cassandra and ScyllaDB (consistency level ONE), Amazon Dynamo-style stores, Riak, CouchDB, DNS, CDN caches'),
    ('Tunable per request', 'Cassandra (ONE, QUORUM, ALL), DynamoDB (eventually or strongly consistent reads), MongoDB (read and write concerns)'),
]) + lv + '''
EXAM> State the CAP theorem with all three properties defined, explain why <b>P is unavoidable</b> so the real choice is <b>C or A during a partition</b>, and give one CP and one AP example with a reason (bank balance vs social media likes). Mention <b>eventual consistency</b> and, for extra marks, <b>PACELC</b>.'''

# ---------------------------------------------------------------- types
types = cards([
    ('CP: consistent under partition', 'The side without a majority stops serving. Answers are always correct, but some users see errors. Payments, inventory, leader election, config stores.', 'Correct or nothing'),
    ('AP: available under partition', 'Every side keeps serving and copies reconcile later. Users always get an answer, but it may be stale or conflict. Feeds, likes, carts, DNS.', 'Answer always'),
    ('Tunable', 'The client chooses per request: fast, eventually consistent reads for a feed; strongly consistent reads for checkout.', 'Per query'),
]) + '''

  <h3>The consistency ladder</h3>
''' + table(['Model', 'Guarantee', 'Example where it matters', 'Cost'], [
    ['<b>Linearizable (strong)</b>', 'Reads see the latest completed write, in real-time order', 'Bank balance, seat booking, unique usernames', 'Highest (coordination on every operation)'],
    ['<b>Sequential</b>', 'Everyone sees operations in one agreed order', 'Replicated logs', 'High'],
    ['<b>Causal</b>', 'Causes are seen before effects', 'Comment threads, chat replies', 'Medium'],
    ['<b>Read-your-writes / monotonic</b>', 'You see your own changes; reads never go backwards', 'Profile edits, order status', 'Low'],
    ['<b>Eventual</b>', 'Copies converge when writes stop', 'Like counts, view counts, recommendations', 'Lowest'],
], minw=640) + '''
TIP> Don’t ask “is our system CP or AP?”; ask “for <i>this</i> data, what is worse during a network fault: showing an error or showing a possibly wrong answer?” The answer is usually different for balances, carts and like counts in the same app.'''

# ---------------------------------------------------------------- steps
c1 = '''replicas = {"A": 100, "B": 100, "C": 100}
groups = [{"A"}, {"B", "C"}]           # the network splits
majority = len(replicas) // 2 + 1
for g in groups:
    print(sorted(g), "has majority" if len(g) >= majority else "minority")'''
c2 = '''def cp_write(group, value, replicas, majority=2):
    if len(group) < majority:
        return "error: try again later"
    for n in group:
        replicas[n] = value
    return "ok"
r = {"A": 100, "B": 100, "C": 100}
print("via A:", cp_write({"A"}, 40, r), "| via B:", cp_write({"B", "C"}, 70, r), "|", r)'''
c3 = '''r = {"A": 100, "B": 100, "C": 100}
r["A"] = 40                      # AP: A accepts a write on its side
r["B"] = r["C"] = 70             # B accepts a different write on the other side
print("A answers", r["A"], "| B answers", r["B"], "-> both available, inconsistent")'''
c4 = '''N, W, R = 3, 2, 2
print("R + W > N:", R + W > N, "-> every read overlaps the latest write")
print("survives 1 node down for reads and writes:", N - W >= 1 and N - R >= 1)'''
steps = stepper([
    ('Three copies, then the network splits',
     code('python', 'partition.py', c1, run_code(c1)),
     'A network fault separates A from B and C. Every node is still running; they just can’t talk. This is a <b>partition</b>, and in a big cluster it is a matter of when, not if.'),
    ('CP: the minority refuses',
     code('python', 'cp.py', c2, run_code(c2)),
     'Only the side with a majority may accept writes (and serve strongly consistent reads). Clients talking to A get errors, but no one ever sees two different balances.'),
    ('AP: both sides answer',
     code('python', 'ap.py', c3, run_code(c3)),
     'Every request succeeds, but the two sides now disagree. When the network heals, the system must reconcile the two values, and some updates may need special merging.'),
    ('Quorums: consistency you can tune',
     code('python', 'quorum.py', c4, run_code(c4)),
     'In leaderless stores like Cassandra, choosing W and R per query moves you along the scale: W = R = 1 is fast and AP-like; R + W &gt; N gives strongly consistent reads while still tolerating one failed node.'),
    ('When the network is fine: latency vs consistency',
     '<p>Even without failures, a strongly consistent write must wait for a majority to confirm. If replicas are in Mumbai, Singapore and Frankfurt, that wait is one long network round trip.</p>',
     'This is the “ELC” in <b>PACELC</b>: else, choose latency or consistency. Many systems keep strongly consistent data in one region and replicate asynchronously elsewhere.'),
    ('Decide per piece of data',
     '<p>In one food-delivery app: wallet balance → strong; restaurant stock of a limited dish → strong; cart → eventual with merge; ratings and view counts → eventual.</p>',
     'Good designs mix models. The skill is matching each kind of data to the weakest guarantee that is still correct for the business.'),
])

# ---------------------------------------------------------------- two-view animation
def ph(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
see = [
    ph('Riya’s reel', fill(140, 58, 80, 70, 'acc', rx=4, opacity=.35) + t(180, 150, '♥ 1,024', 12, 'red', bold=True) + t(180, 172, 'she taps like: instant', 8.2, 'ink2')),
    ph('Meera · Delhi', fill(140, 58, 80, 70, 'acc', rx=4, opacity=.35) + t(180, 150, '♥ 1,021', 12, 'red', bold=True) + t(180, 172, 'a few likes behind', 8.2, 'ink2')),
    ph('Everyone', fill(140, 58, 80, 70, 'acc', rx=4, opacity=.35) + t(180, 150, '♥ 1,025', 12, 'red', bold=True) + t(180, 172, 'same number for all', 8.2, 'green')),
    ph('UPI', t(180, 74, 'Pay ₹500 to', 9) + t(180, 90, 'Kirana Store', 9, bold=True) + fill(144, 120, 72, 22, 'acc', rx=11) + t(180, 135, 'PAY', 8.4, extra=' style="fill:#fff"', bold=True)),
    ph('UPI', '<circle cx="180" cy="94" r="18" style="fill:none;stroke:#E0A100;stroke-width:3;stroke-dasharray:22 8"/>' + t(180, 136, 'Payment pending', 9, 'acc', bold=True) + t(180, 152, 'please don’t retry', 8, 'ink2')),
    ph('UPI', '<circle cx="180" cy="94" r="18" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M172 94l5 5 10-10" style="stroke:var(--green);stroke-width:2.5;fill:none"/>' + t(180, 136, 'Paid ₹500', 9.4, 'green', bold=True) + t(180, 152, 'balance ₹1,850, correct', 8, 'ink2')),
]
def regions(a, b, c, link_ok=True, title='', tone_a='card', tone_bc='card'):
    o = t(180, 22, title, 9.6, bold=True)
    o += label_box(20, 50, 110, 50, ['Mumbai', a], tone_a, 9.4) + label_box(230, 40, 110, 44, ['Delhi', b], tone_bc, 9) + label_box(230, 100, 110, 44, ['Chennai', c], tone_bc, 9)
    if link_ok:
        o += arrow(132, 72, 228, 62, 'ink3', 1.4, dash=True) + arrow(132, 80, 228, 118, 'ink3', 1.4, dash=True)
    else:
        o += '<path d="M180 36V160" style="stroke:#D64545;stroke-width:3;stroke-dasharray:6 4"/>'
    return o
behind = [
    regions('♥ 1,024', '♥ 1,021', '♥ 1,021', title='Likes: AP, eventually consistent', tone_a='green') + t(180, 190, 'The like is written locally and replicated later.', 9, 'ink2'),
    regions('♥ 1,024', '♥ 1,021', '♥ 1,021', title='Delhi is a few likes behind', tone_bc='amber') + t(180, 190, 'Stale by a second or two. No harm done.', 9, 'ink2'),
    regions('♥ 1,025', '♥ 1,025', '♥ 1,025', title='Copies converge', tone_a='green', tone_bc='green') + t(180, 190, 'When updates settle, every copy agrees: eventual consistency.', 9, 'ink2'),
    regions('₹2,350', '₹2,350', '₹2,350', title='Balance: CP, strongly consistent', tone_a='blue', tone_bc='blue') + t(180, 190, 'A debit must be agreed by a majority before it counts.', 9, 'ink2'),
    regions('₹2,350', '₹2,350', '₹2,350', link_ok=False, title='Link to Mumbai breaks mid-payment', tone_a='red', tone_bc='blue') + t(180, 190, 'Mumbai (minority) refuses to confirm alone: “pending”.', 9, 'ink2'),
    regions('₹1,850', '₹1,850', '₹1,850', title='Majority confirms the debit once', tone_a='green', tone_bc='green') + t(180, 190, 'Exactly one debit, the same balance everywhere.', 9, 'ink2'),
]
see_caps = ['Riya likes her own reel; the count jumps to 1,024 instantly.',
            'Meera in Delhi sees 1,021 on the same reel at the same moment.',
            'A little later everyone sees the same count, 1,025.',
            'Riya pays ₹500 to the kirana store by UPI.',
            'The app shows “payment pending, please don’t retry” for a few seconds.',
            'The payment succeeds and her balance is exactly right.']
behind_caps = ['Likes use an <b>AP</b> design: the write is accepted by the nearest copy and replicated to others in the background.',
               'Delhi’s copy hasn’t received the latest likes yet, so it shows a slightly older number. Nobody is harmed by this.',
               'Once updates stop for a moment, all copies converge on the same value: <b>eventual consistency</b>.',
               'Balances use a <b>CP</b> design: a debit counts only when a majority of copies agree, so there is one true balance.',
               'A network fault cuts Mumbai off. Rather than risk confirming a debit the others don’t know about, the minority side refuses and the app shows “pending”: less available, never wrong.',
               'Once the majority confirms, the debit is applied exactly once, and every copy shows ₹1,850. (Regions and timings are illustrative.)']
two = anim_two('AP likes, CP money', 'What Riya sees, and what the copies do', 'Riya seeing like counts and making a UPI payment',
               'Copies in three regions handling likes with eventual consistency and payments with strong consistency', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: same partition, CP vs AP
def split(mode, stage):
    o = '<path d="M180 36V150" style="stroke:#D64545;stroke-width:3;stroke-dasharray:6 4"/>' if 1 <= stage <= 3 else ''
    if mode == 'CP':
        a = {0: ('Rs 100', 'card'), 1: ('Rs 100', 'card'), 2: ('refuses', 'red'), 3: ('refuses', 'red'), 4: ('Rs 70', 'green')}[stage]
        bc = {0: 'Rs 100', 1: 'Rs 100', 2: 'Rs 70', 3: 'Rs 70', 4: 'Rs 70'}[stage]
    else:
        a = {0: ('♥ 1,000', 'card'), 1: ('♥ 1,000', 'card'), 2: ('♥ 1,003', 'amber'), 3: ('♥ 1,003', 'amber'), 4: ('♥ 1,008', 'green')}[stage]
        bc = {0: '♥ 1,000', 1: '♥ 1,000', 2: '♥ 1,005', 3: '♥ 1,005', 4: '♥ 1,008'}[stage]
    o += label_box(20, 56, 110, 50, ['Node A', a[0]], a[1], 9.4)
    o += label_box(230, 40, 110, 40, ['Node B', bc], 'green' if stage >= 2 else 'card', 8.8) + label_box(230, 90, 110, 40, ['Node C', bc], 'green' if stage >= 2 else 'card', 8.8)
    return o
fr1 = [
    split('CP', 1) + t(180, 22, 'Network splits: {A} | {B, C}', 9.6, 'red', bold=True) + cap('Same failure, two designs. First: a CP bank balance.', '', 'card', y=160, h=34),
    split('CP', 2) + t(180, 22, 'CP: A has no majority → refuses', 9.6, 'acc', bold=True) + cap('B and C (2 of 3) accept a debit to Rs 70.', 'Users routed to A get an error. Nobody sees a wrong balance.', 'blue', y=156, h=44),
    split('AP', 2) + t(180, 22, 'AP like counter: both sides accept', 9.6, 'acc', bold=True) + cap('3 likes arrive at A, 5 at B. Everyone gets a response,', 'but A says 1,003 and B says 1,005.', 'amber', y=156, h=44),
    split('AP', 3) + t(180, 22, 'Network heals: how to merge?', 9.6, 'acc', bold=True) + cap('Last-write-wins would keep 1,005: A’s 3 likes vanish.', 'Silent data loss.', 'red', y=156, h=44),
    split('AP', 4) + t(180, 22, 'CRDT counter: add both sides’ increments', 9.6, 'green', bold=True) + cap('1,000 + 3 + 5 = 1,008. Every like kept.', 'AP done right needs data types that merge safely.', 'green', y=156, h=44),
]
s1 = anim_one('Real-time scenario 1', 'One network split, two designs',
              'A three-node cluster loses its network link to node A. Watch a CP bank balance and an AP like counter react to exactly the same failure. (These are the numbers from the program in “Run it on your PC”.)',
              'CP vs AP during a partition', 'Three nodes split by a network partition, handled first with CP and then with AP', fr1,
              ['The network splits node A from B and C. All three are still running.',
               '<b>CP balance:</b> A is alone, not a majority, so it refuses requests. B and C, a majority, accept a debit to ₹70. Some users see errors, but nobody ever sees two different balances.',
               '<b>AP like counter:</b> both sides keep accepting likes: 3 arrive at A and 5 at B. Every user gets an answer, but the two sides disagree.',
               'When the network heals, the copies must be merged. A naive last-write-wins rule keeps B\'s 1,005 and silently drops A\'s 3 likes.',
               'A <b>CRDT counter</b> stores each node’s increments separately and adds them: 1,008, with nothing lost. AP systems need merge rules designed for the data.'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: cart merge (Dynamo style)
def cart(x, title, items, tone='card'):
    return box(x, 40, 150, 100, tone) + t(x + 75, 58, title, 9.2, bold=True) + ''.join(t(x + 14, 80 + k * 16, ('• ' + it), 8.6, anchor='start') for k, it in enumerate(items))
fr2 = [
    cart(14, 'Replica 1', ['thali']) + cart(196, 'Replica 2', ['thali']) + t(180, 24, 'Riya’s cart, copied on two replicas', 9.6, bold=True) + cap('Carts are AP: adding an item must never fail.', '', 'card', y=156, h=34),
    cart(14, 'Replica 1', ['thali', 'lassi'], 'amber') + cart(196, 'Replica 2', ['thali', 'gulab jamun'], 'amber') + '<path d="M180 36V146" style="stroke:#D64545;stroke-width:3;stroke-dasharray:6 4"/>' + t(180, 24, 'Partition: phone and laptop hit different replicas', 9.2, 'red', bold=True)
    + cap('She adds lassi on her phone and gulab jamun on her laptop.', 'Both writes succeed on different replicas.', 'amber', y=156, h=44),
    cart(105, 'Merged cart', ['thali', 'lassi', 'gulab jamun'], 'green') + t(180, 24, 'Healed: merge = union of both carts', 9.6, 'green', bold=True) + cap('Union keeps every addition. Nothing she added is lost.', '', 'green', y=156, h=34),
    cart(105, 'Merged cart', ['thali', 'lassi', 'gulab jamun'], 'red') + t(180, 24, 'But: she had removed lassi on one side', 9.6, 'red', bold=True) + cap('A plain union brings deleted items back (“zombie” items).', 'Amazon’s Dynamo paper describes exactly this.', 'red', y=156, h=44),
    cart(105, 'Merged cart', ['thali', 'gulab jamun'], 'green') + t(180, 24, 'Fix: track adds and removes separately', 9.6, 'green', bold=True) + cap('An OR-Set CRDT records each add and remove with an id,', 'so a remove beats the add it saw. The cart merges correctly.', 'green', y=156, h=44),
]
s2 = anim_one('Real-time scenario 2', 'Merging a shopping cart after a split',
              'Shopping carts are a classic AP example: it is better to always accept “add to cart” than to show an error during a sale. Watch what merging two diverged carts really involves.',
              'AP merge done right', 'Two replicas of a cart diverging during a partition and being merged', fr2,
              ['Riya’s cart is stored on two replicas. Adding to the cart must always work, so the cart is designed to be available.',
               'During a partition her phone and her laptop reach different replicas. She adds a lassi on one and a gulab jamun on the other. Both writes succeed.',
               'When the network heals, the simplest merge is the <b>union</b> of both carts, which keeps every item she added.',
               'But if she had removed the lassi on one side, a plain union would bring it back. Amazon’s Dynamo paper reported this “deleted item reappears” effect.',
               'The fix is a smarter data type: an <b>OR-Set</b> CRDT tags each add and remove, so a remove cancels exactly the adds it had seen. The merged cart is correct without any coordination.'])

# ---------------------------------------------------------------- scenario 3 (advanced): PACELC latency
def lat(rows, note1, note2, tone):
    return t(14, 22, 'write latency (illustrative)', 9, 'ink2', anchor='start') + bars(rows, x=150, y=32, w=150, gap=24) + cap(note1, note2, tone, y=140, h=44)
fr3 = [
    label_box(14, 40, 100, 44, ['Mumbai'], 'acc', 9.6) + label_box(130, 40, 100, 44, ['Singapore'], 'blue', 9.6) + label_box(246, 40, 100, 44, ['Frankfurt'], 'violet', 9.6)
    + t(180, 24, 'Three replicas in three regions', 9.6, bold=True) + t(180, 110, 'round trip Mumbai–Singapore ≈ 60 ms · Mumbai–Frankfurt ≈ 120 ms', 8.4, 'ink2')
    + cap('No partition today. Every link works.', 'What does consistency cost?', 'card', y=140, h=44),
    lat([('async (local only)', 3, 'green', '≈ 2 ms')], 'Async: confirm after the local write.', 'Fastest, but other regions may lag (and lose data in a crash).', 'green'),
    lat([('async (local only)', 3, 'green', '≈ 2 ms'), ('majority (2 of 3)', 50, 'acc', '≈ 60 ms')], 'Strong: wait for a majority. Mumbai + Singapore', 'must agree: one long round trip on every write.', 'blue'),
    lat([('async (local only)', 3, 'green', '≈ 2 ms'), ('majority (2 of 3)', 50, 'acc', '≈ 60 ms'), ('all 3 replicas', 100, 'red', '≈ 120 ms')], 'Waiting for all three adds Frankfurt’s distance', 'and fails if any one region is down.', 'red'),
    lat([('wallet: majority', 50, 'acc', '≈ 60 ms'), ('likes: async', 3, 'green', '≈ 2 ms'), ('cart: local + merge', 3, 'green', '≈ 2 ms')], 'PACELC choice per data: pay latency only where', 'correctness truly needs it.', 'green'),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'PACELC: consistency costs time even on good days',
              'CAP talks only about partitions. But most of the time the network is fine, and there is still a trade-off: every strongly consistent write must wait for other replicas. Watch the latency of one write with replicas in three regions.',
              'Latency vs consistency', 'Write latency bars for asynchronous, majority and all-replica writes across regions', fr3,
              ['Replicas are in Mumbai, Singapore and Frankfurt. There is no failure. Network round trips are roughly 60 ms to Singapore and 120 ms to Frankfurt.',
               '<b>Asynchronous:</b> the write is confirmed after the local copy is saved, about 2 ms. Other regions catch up later.',
               '<b>Majority:</b> a strongly consistent write needs two of three replicas, so Mumbai waits for Singapore: about 60 ms on every write.',
               '<b>All replicas:</b> waiting for Frankfurt too pushes it to about 120 ms, and any single region being down blocks writes.',
               'So, per PACELC: <b>else</b> (no partition) choose <b>latency</b> or <b>consistency</b>. Pay the latency only for data like wallets; keep likes and carts fast. (Latencies are illustrative.)'])

realworld = '''  <p>Three live scenarios: the same network split handled by a CP and an AP design (real numbers), a shopping cart merged after a split, and an advanced look at the latency cost of consistency across regions.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Consistency choices in real products</h3>
''' + usecase('<rect x="20" y="20" width="80" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="50" text-anchor="middle" font-size="12" font-weight="700" class="s-blue">₹ ledger</text>',
              '1. Payments and wallets: strong consistency', 'UPI and wallet systems treat balances as strongly consistent: a debit is confirmed only once, and during uncertainty the payment stays “pending” and is later settled or reversed rather than guessed.', ['Debit request', '*Majority / transaction', 'One true balance']) + usecase(
    '<text x="60" y="54" text-anchor="middle" font-size="20" class="s-red">♥</text><text x="88" y="54" text-anchor="middle" font-size="10" class="s-ink">1.2k</text>',
    '2. Social counters and feeds: eventual', 'Likes, views and follower counts are counted on many servers and merged in the background. Showing 1,021 instead of 1,024 for a second is a fine trade for never failing a tap.', ['Tap ♥', '*Local write, async merge', 'Converges']) + usecase(
    '<rect x="20" y="22" width="34" height="46" rx="4" class="s-soft-acc" style="stroke:var(--track)"/><rect x="66" y="22" width="34" height="46" rx="4" class="s-soft-acc" style="stroke:var(--track)"/><text x="60" y="82" text-anchor="middle" font-size="9" class="s-ink">seat 14B</text>',
    '3. Ticket and seat booking: strong for the seat', 'Train, flight and cinema booking must never sell one seat twice, so the final seat assignment is strongly consistent, even though seat-availability views shown while browsing may be slightly stale.', ['Browse (stale OK)', '*Lock / confirm seat', 'One owner']) + usecase(
    '<circle cx="60" cy="45" r="26" style="fill:none;stroke:var(--green);stroke-width:4"/><text x="60" y="50" text-anchor="middle" font-size="10" font-weight="700" class="s-green">etcd</text>',
    '4. Cluster coordination: CP stores', 'Kubernetes stores cluster state in etcd and Kafka uses KRaft (formerly ZooKeeper): small CP stores based on consensus, where being correct about “who is leader” matters more than answering during a split.', ['Leader election', '*Raft consensus', 'Exactly one leader'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', 'Why can likes disagree, but my bank balance can’t?', story)
        + part(2, 'definition', 'Definition', 'The CAP theorem and consistency models', definition)
        + part(3, 'types', 'Types and ways to use it', 'CP, AP and the consistency ladder', types)
        + part(4, 'steps', 'Step by step', 'A partition, handled two ways', steps)
        + part(5, 'animation', 'See it happen', 'Likes and a payment: what Riya sees, and what the copies do', '  <p>Step through the six frames. Left: Riya’s reel likes and a UPI payment. Right: copies in three regions, eventually consistent for likes and strongly consistent for money.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: choosing consistency', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('System design · consistency', 'Fresher', 'Which parts of a food app need strong consistency?',
            'For a food-delivery app, decide the consistency level for: wallet balance, cart, restaurant ratings, “only 5 left” limited-dish stock, and order status shown to the customer.',
            'can you choose consistency per piece of data with reasons?',
            '<ul><li><b>Wallet:</b> strong (never double-spend).</li><li><b>Limited stock:</b> strong at checkout (never oversell); browsing can show a slightly stale count.</li><li><b>Cart:</b> eventual/available, with a correct merge.</li><li><b>Ratings:</b> eventual.</li><li><b>Order status:</b> read-your-writes and monotonic reads per user (status never goes backwards), not necessarily global linearizability.</li></ul>',
            'labelling the whole app “CP” or “AP”.')
        + scn('Distributed DB · Cassandra', '1–3 years', 'Users sometimes see old profile data',
              'A Cassandra cluster with replication factor 3 uses consistency level ONE for reads and writes. Users occasionally see their old profile after updating it.',
              'do you understand tunable consistency and its trade-offs?',
              '<p>With W = 1 and R = 1, R + W = 2 is not greater than N = 3, so a read can hit a replica that hasn’t received the write. Use QUORUM for both (2 + 2 &gt; 3) on profile reads and writes, accepting slightly higher latency, or LOCAL_QUORUM in multi-datacentre setups. Keep ONE for data where staleness is harmless. Make sure clocks are synchronised, since Cassandra resolves conflicts by timestamp (last-write-wins).</p>',
              'switching everything to ALL, which fails whenever any replica is down.')
        + scn('Architecture · multi-region', '3+ years', 'Go active-active in two regions?',
              'Leadership wants the app to accept writes in both Mumbai and Hyderabad at the same time, so a regional outage causes no downtime.',
              'do you see the consistency consequences of multi-leader designs?',
              '<p>Active-active means concurrent writes to the same data in both regions, so conflicts are certain during network issues. For each entity decide: can it be partitioned by region (each user’s data has a home region), can it merge automatically (counters, sets via CRDTs), or must it be strongly consistent (wallet, inventory), which then needs a single leader or consensus with cross-region latency on every write. Often the answer is active-active for most data plus a single-region leader for money, with fast failover.</p>',
              'promising zero downtime and strong consistency everywhere without discussing the latency or conflicts.')
        + scn('Fundamentals · interview', 'Fresher', '“Explain the CAP theorem”',
              'The classic question. Many candidates answer “pick any two of three”.',
              'can you explain it precisely and correct the myth?',
              '<p>In a distributed system, when a network partition happens, you must choose between consistency (every read returns the latest write) and availability (every request gets a non-error response). Partitions can’t be prevented, so partition tolerance is required, and “CA” only applies to non-distributed systems. Example: a bank ledger chooses consistency and refuses some requests during a partition; a like counter chooses availability and reconciles later. Without partitions, PACELC adds a latency vs consistency trade-off, and many databases let you tune consistency per query.</p>',
              'saying “Cassandra is AP, MongoDB is CP, done” without explaining what is traded and when.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
