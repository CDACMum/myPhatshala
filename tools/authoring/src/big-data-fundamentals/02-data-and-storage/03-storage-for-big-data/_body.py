import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..'))
from svgkit import *

# ---------------------------------------------------------------- story
sc = ''
items = [('Block', 'raw disk volume', 'database lives here', 'blue', 14),
         ('File', 'folders and paths', '/team/reports/oct.xlsx', 'violet', 222),
         ('Object', 'bucket + key + metadata', 's3://tiffingo-lake/…', 'green', 430)]
for name, a, b, tone, x in items:
    sc += box(x, 18, 196, 118, tone) + t(x + 98, 40, f'{name} storage', 11, 'ink', bold=True) + t(x + 98, 56, a, 8.8, 'ink2')
    sc += t(x + 98, 124, b, 8.4, 'ink3', mono=True)
sc += ''.join(fill(34 + k * 22, 68, 18, 40, 'blue', rx=2, opacity=.75) for k in range(7))
sc += ''.join(fill(242 + (k % 3) * 52, 66 + (k // 3) * 22, 44, 16, 'violet', rx=3, opacity=.6) for k in range(6))
sc += ''.join(f'<circle cx="{462 + (k % 6) * 26}" cy="{76 + (k // 6) * 24}" r="9" style="fill:var(--green);opacity:.7"/>' for k in range(12))
scene_svg = scene('Three kinds of storage: block storage drawn as disk blocks, file storage as folders, object storage as a big pool of objects with keys.', sc,
                  'Same bytes, three ways to organise them. Big data mostly lives in the <tspan font-weight="700" class="s-acc">third</tspan>.')

story = f'''  <div class="story">
    <p class="narration">Kabir reads TiffinGo’s engineering blog to prepare for his internship. One line stops him: <i>“Our lake holds 2 PB in S3 and we have no file servers at all.”</i> He has always thought of storage as a hard disk with folders. Where do two petabytes go if not on a disk?</p>

{scene_svg}

K> Sir, what is S3? If there are no file servers, where are the folders?
A> S3 is Amazon’s <b>object storage</b>. There are no real folders. You give it a <b>key</b>, like a long name, and some bytes, and it gives the same bytes back when you ask with that key. It looks like folders only because keys contain slashes.
R> Like a cloakroom at a wedding hall? You hand over your bag and get a token?
A> A very good picture, Riya. And the cloakroom is so big that it never fills up, keeps copies of your bag in three buildings, and charges you a few paise per day for it.
K> Then why do we still have normal disks and folders at all?
A> Because each kind of storage is good at different things. Databases need <b>block storage</b> for fast small updates. Teams share documents through <b>file storage</b>. Big data lakes use <b>object storage</b> (or Hadoop’s HDFS) because it is cheap and nearly limitless. Today you’ll see all three, write a file into HDFS, meet the small-files problem and learn why “rename” can be dangerously slow in the cloud.
  </div>'''

# ---------------------------------------------------------------- definition
lv = '''
LEVELS> Storage at three levels
L1> A plot of land, a filing cabinet and a cloakroom
      <ul>
        <li><b>Block storage</b> is an empty plot of land: raw space divided into equal blocks. You (or a database) build whatever structure you want on it. It is fast but sits attached to one machine. Example: your laptop’s SSD, a cloud disk such as Amazon EBS.</li>
        <li><b>File storage</b> is an office filing cabinet: folders inside folders, files with names. Many people can open the same cabinet. Example: a shared office drive (NAS), Google Drive’s folders.</li>
        <li><b>Object storage</b> is a giant cloakroom: hand over an item, get a token (the key). No shelves to manage, almost unlimited space, very cheap. Example: Amazon S3, Azure Blob/ADLS, Google Cloud Storage.</li>
      </ul>
      <p><b>Rule of thumb:</b> databases → block; shared team folders → file; data lakes, backups, photos and videos → object.</p>
L2> How each one is accessed, and where HDFS fits
      <ul>
        <li><b>Block:</b> the operating system sees a raw disk, puts a file system on it, and reads or writes any 4 KB block in place. Lowest latency (sub-millisecond on SSD). Usually one machine at a time.</li>
        <li><b>File:</b> paths like <code>/finance/2026/oct.csv</code>, shared over the network (NFS, SMB). Supports in-place edits, locks and renames. Scaling to billions of files is hard.</li>
        <li><b>Object:</b> a flat namespace of <b>buckets</b> and <b>keys</b>, used over HTTP (<code>PUT</code>, <code>GET</code>, <code>LIST</code>, <code>DELETE</code>). Each object has <b>metadata</b>. Objects are written whole: to change one byte, you upload a new version.</li>
        <li><b>HDFS</b> is a <i>distributed file system</i>: files are split into large blocks (128 MB by default) stored on many DataNodes, usually with 3 copies; a NameNode keeps the directory tree and block locations. It brought storage and compute onto the same machines (data locality).</li>
        <li><b>Today’s default:</b> cloud object storage has largely replaced HDFS for new lakes, because storage and compute can scale and be paid for separately.</li>
      </ul>
L3> Durability, consistency, small files and renames
      <ul>
        <li><b>Durability vs availability:</b> durability is the chance your data is never lost (S3 is designed for 99.999999999%, “eleven nines”); availability is the chance you can read it right now. They are different promises.</li>
        <li><b>Replication vs erasure coding:</b> 3 full copies cost 200% extra space; erasure coding splits data into, say, 6 data pieces plus 3 parity pieces and survives the loss of any 3, for only 50% extra. HDFS 3 and cloud stores use erasure coding for colder data.</li>
        <li><b>Consistency:</b> S3 has offered strong read-after-write consistency since December 2020: a successful write is visible to every reader immediately. Older advice about “eventual consistency” is outdated.</li>
        <li><b>Small files:</b> every object or HDFS file has a fixed cost: a metadata entry (roughly 150 bytes of NameNode memory per file or block), an open request, a listing entry and per-request charges. Millions of tiny files make jobs slow and bills high. Compact to files of roughly 128 MB to 1 GB.</li>
        <li><b>Rename is not cheap on object stores:</b> there are no real directories, so “renaming a folder” means copying and deleting every object under the prefix, which is slow and not atomic. Table formats (Delta Lake, Iceberg) avoid renames by committing through a transaction log.</li>
        <li><b>Lifecycle and tiers:</b> rules move objects automatically from hot to cool, cold and archive tiers as they age, and delete them when retention ends.</li>
      </ul>
/LEVELS
'''
definition = def_block(
    '<b>Block storage</b> divides storage into fixed-size blocks addressed by number and presents them to a server as a raw volume on which a file system or database is built; it offers low latency and in-place updates. <b>File storage</b> organises data as files in a hierarchy of directories accessed by path, often shared over a network (NAS, NFS, SMB). <b>Object storage</b> stores data as immutable objects, each with a unique key and metadata, in a flat namespace of buckets accessed through an HTTP API; it scales to exabytes at low cost and is the usual foundation of cloud data lakes. A <b>distributed file system</b> such as <b>HDFS</b> spreads large files as replicated blocks across a cluster.',
    'Block storage is a raw disk that one computer uses, perfect for databases. File storage is folders and files that a team shares. Object storage is a huge, cheap store where each item has a name (key) and you put or get whole items over the internet. Big data lakes live mostly on object storage, or on Hadoop’s HDFS.') + '''

  <h3>Words you’ll meet in this lesson</h3>
''' + terms([
    ('Volume', 'A block-storage disk attached to a server, such as a cloud disk.'),
    ('NAS', 'Network-attached storage: a file server shared by many computers.'),
    ('Bucket', 'A top-level container in object storage, like <code>tiffingo-lake</code>.'),
    ('Key', 'The full name of an object: <code>orders/date=2026-10-19/part-0.parquet</code>.'),
    ('Prefix', 'The start of a key, used like a folder: <code>orders/date=2026-10-19/</code>.'),
    ('NameNode / DataNode', 'HDFS’s metadata master and the machines that store the actual blocks.'),
    ('Durability', 'The probability that stored data is never lost.'),
    ('Erasure coding', 'Storing data plus parity pieces so lost pieces can be rebuilt, using less space than full copies.'),
]) + '''

  <h3>Typical numbers to reason with (approximate)</h3>
''' + facts([
    ('HDFS block size', '128 MB by default (often 256 MB), stored as 3 replicas'),
    ('Object size limits (S3)', 'single object up to 5 TB; uploads above 5 GB must be split into parts'),
    ('S3 durability', 'designed for 99.999999999% (eleven nines) by storing data across several facilities'),
    ('Good file size for analytics', 'about 128 MB to 1 GB per file; thousands of KB-sized files are a warning sign'),
    ('Storage tiers', 'hot (frequent access) → cool/infrequent → cold → archive (cheapest, retrieval takes minutes to hours)'),
]) + lv + '''
EXAM> Compare <b>block, file and object storage</b> in a table on <b>structure, access method, scalability, latency, cost, update style and examples</b>. Then add HDFS: block size, replication factor 3, NameNode and DataNode roles. These two tables answer most storage questions.'''

# ---------------------------------------------------------------- types
types = cards([
    ('Block storage', 'Raw volumes attached to one server. Fast random reads and writes. Databases, VM disks, Kafka broker disks.', 'Fast · one server'),
    ('File storage', 'Shared folders and files over the network. Familiar paths, locking and edits. Team shares, home directories.', 'Folders · shared'),
    ('Object storage', 'Buckets of objects with keys and metadata over HTTP. Nearly unlimited, cheap, very durable. Lakes, backups, media.', 'Huge · cheap'),
    ('Distributed file system (HDFS)', 'Large files split into replicated blocks across a cluster, processed where they sit. Classic Hadoop platforms.', 'Cluster · local'),
]) + '''

  <h3>Side by side</h3>
''' + table(['', 'Block', 'File', 'Object', 'HDFS'], [
    ['<b>Structure</b>', 'Numbered blocks', 'Folder tree', 'Flat: bucket + key', 'Folder tree over 128 MB blocks'],
    ['<b>Access</b>', 'OS disk calls', 'Paths (NFS, SMB)', 'HTTP API (PUT/GET)', 'HDFS client API'],
    ['<b>Update in place</b>', 'Yes', 'Yes', 'No: rewrite the object', 'Append only'],
    ['<b>Scale</b>', 'One volume, TBs', 'Large, but hard at billions of files', 'Practically unlimited', 'Thousands of nodes'],
    ['<b>Latency</b>', 'Lowest', 'Low', 'Higher (tens of ms per request)', 'Low within the cluster'],
    ['<b>Cost per GB</b>', 'Highest', 'Medium', 'Lowest', 'Hardware you run'],
    ['<b>Typical use</b>', 'Databases', 'Shared documents', 'Data lakes, backups, media', 'On-prem Hadoop lakes'],
    ['<b>Examples</b>', 'Laptop SSD, Amazon EBS, Azure Disk', 'NAS, Amazon EFS, Azure Files', 'Amazon S3, Azure Blob/ADLS Gen2, Google Cloud Storage', 'Apache HDFS'],
], minw=680) + '''
TIP> “Folders” in S3 are an illusion: the console shows <code>orders/</code> because many keys start with that prefix. This is why a <b>key naming scheme</b>, such as <code>orders/date=2026-10-19/part-00001.parquet</code>, is one of the first design decisions in a data lake.'''

# ---------------------------------------------------------------- steps
c1 = '''import math
file_mb, block_mb, replicas = 300, 128, 3
blocks = math.ceil(file_mb / block_mb)
last = file_mb - (blocks - 1) * block_mb
print("Blocks:", blocks, "| last block:", last, "MB")
print("Raw space used:", file_mb * replicas, "MB")'''
c2 = '''bucket = {}
bucket["orders/date=2026-10-19/part-0.parquet"] = b"..."
bucket["orders/date=2026-10-20/part-0.parquet"] = b"..."
bucket["reviews/2026/10/19/O1043.jpg"] = b"..."
prefix = "orders/"
print([k for k in bucket if k.startswith(prefix)])'''
c3 = '''data_tb = 100
print("3 replicas     :", data_tb * 3, "TB raw")
print("Erasure 6 + 3  :", data_tb * (6 + 3) / 6, "TB raw")'''
c4 = '''files, avg_kb = 2_000_000, 40
per_file_ms = 10
print("Total data :", round(files * avg_kb / 1024 / 1024, 1), "GB")
print("Open + list overhead:", round(files * per_file_ms / 1000 / 60), "minutes")'''
steps = stepper([
    ('Block storage: a disk for one server',
     '<p>A PostgreSQL database for TiffinGo’s live orders runs on a cloud disk (block storage). When an order’s status changes, the database rewrites one small block in place, in well under a millisecond.</p>',
     'Fast, in-place, small updates are exactly what databases need. But the disk is attached to one server and is the most expensive storage per GB.'),
    ('File storage: shared folders',
     '<p>The finance team keeps monthly reports in <code>/finance/2026/</code> on a shared drive. Anyone with access can open, edit and rename files by path.</p>',
     'Familiar and convenient for people. At the scale of billions of files and petabytes, managing one giant folder tree becomes slow and costly.'),
    ('HDFS: one 300 MB file becomes blocks',
     code('python', 'hdfs_blocks.py', c1, run_code(c1)),
     'HDFS cuts the file into 128 MB blocks (the last one is smaller), and stores 3 copies of each on different DataNodes. The NameNode remembers which blocks make up the file and where they are.'),
    ('Object storage: keys, not folders',
     code('python', 'keys.py', c2, run_code(c2)),
     'Listing a “folder” is really asking for every key that starts with a prefix. The key naming scheme decides how easily you can find, partition and delete data later.'),
    ('Copies vs erasure coding',
     code('python', 'durability.py', c3, run_code(c3)),
     'Three full copies need 300 TB of disk for 100 TB of data. Erasure coding (6 data + 3 parity pieces) survives losing any 3 pieces and needs only 150 TB. Cloud object stores use techniques like this behind the scenes.'),
    ('The cost of many tiny files',
     code('python', 'small_files.py', c4, run_code(c4)),
     'Only 76 GB of data, yet over five hours of pure overhead just opening and listing two million files one by one (at an illustrative 10 ms each). Compacting them into a few hundred large files makes the overhead disappear.'),
])

# ---------------------------------------------------------------- two-view animation
def phone(title, inner):
    return (f'<rect x="120" y="14" width="120" height="206" rx="16" class="s-board"/><rect x="128" y="30" width="104" height="174" rx="6" class="s-card2"/>'
            + t(180, 46, title, 9.2, bold=True) + inner)
img = lambda x, y, w=72, h=50: fill(x, y, w, h, 'acc', rx=4, opacity=.45) + f'<circle cx="{x + 16}" cy="{y + 14}" r="6" style="fill:var(--track)"/>'
see = [
    phone('Add a photo', img(144, 60) + fill(150, 130, 60, 20, 'acc', rx=10) + t(180, 144, 'UPLOAD', 8, extra=' style="fill:#fff"', bold=True)),
    phone('Uploading…', img(144, 60) + '<rect x="140" y="130" width="80" height="10" rx="4" class="s-card2"/>' + fill(140, 130, 60, 10, 'green') + t(180, 160, '3.1 MB', 8.4, 'ink2')),
    phone('Review posted', img(144, 60) + '<circle cx="180" cy="148" r="12" class="s-soft-green" style="stroke:var(--green);stroke-width:2"/><path d="M174 148l4 4 8-8" style="stroke:var(--green);stroke-width:2.5;fill:none"/>'),
    phone('Annapurna Kitchen', t(180, 62, '★ 4.2 · 1,240 reviews', 8, 'ink2') + img(136, 72, 40, 30) + img(182, 72, 40, 30) + img(136, 110, 40, 30) + img(182, 110, 40, 30)),
    phone('Annapurna Kitchen', img(144, 60) + t(180, 128, 'Riya’s photo', 8.6, 'ink2') + t(180, 146, 'loads in 0.2 s', 8.6, 'green', bold=True)),
    phone('Order history', t(180, 70, 'Oct 2026 · thali', 8.4, 'ink2') + fill(140, 82, 80, 40, 'grey', rx=4) + t(180, 106, 'photo archived', 8, 'ink3') + t(180, 146, 'tap to restore', 8, 'blue')),
]
def az(x, label, on=True, tone='green'):
    return box(x, 120, 100, 56, tone if on else 'card') + t(x + 50, 138, label, 8.6, bold=True) + (''.join(fill(x + 14 + k * 26, 148, 20, 18, tone, rx=3) for k in range(3)) if on else '')
key = 's3://tiffingo-media/reviews/2026/10/19/O1043.jpg'
behind = [
    t(180, 30, 'Phone → upload service', 10, bold=True) + label_box(60, 50, 240, 48, ['HTTPS PUT · 3.1 MB', 'content-type: image/jpeg'], 'blue', 9.4) + t(180, 130, 'The app never talks to a disk or folder.', 9, 'ink2') + t(180, 148, 'It asks the storage service to keep an object.', 9, 'ink2'),
    t(180, 26, 'PUT object', 10, 'acc', bold=True) + box(10, 40, 340, 64, 'card') + t(180, 60, key, 7.8, 'ink', mono=True) + t(180, 80, 'metadata: order=O1043, user=U9, size=3.1 MB', 8.2, 'ink2', mono=True) + t(180, 96, 'etag: 9f2c…a71', 8.2, 'ink3', mono=True) + t(180, 140, 'Key = bucket + full name. The slashes are just characters.', 9, 'ink2'),
    t(180, 26, 'Stored across 3 availability zones', 10, 'green', bold=True) + label_box(130, 44, 100, 40, ['object'], 'acc', 9.4) + arrow(160, 86, 60, 118) + arrow(180, 86, 180, 118) + arrow(200, 86, 300, 118) + az(10, 'Zone A') + az(130, 'Zone B') + az(250, 'Zone C') + t(180, 200, 'Pieces spread so a whole building can fail.', 9, 'ink2'),
    t(180, 26, 'The app database stores only the key', 10, 'blue', bold=True) + box(10, 44, 340, 66, 'card') + ''.join(t(20 + k * 110, 64, h, 8.4, 'ink3', anchor='start', bold=True) for k, h in enumerate(['review_id', 'stars', 'photo_key'])) + ''.join(t(20 + k * 110, 92, v, 8.4, anchor='start', mono=True) for k, v in enumerate(['R88102', '3', 'reviews/…/O1043.jpg'])) + t(180, 140, 'Block storage (database) holds small rows;', 9, 'ink2') + t(180, 156, 'object storage holds the big photo.', 9, 'ink2'),
    t(180, 26, 'GET through a CDN cache', 10, 'green', bold=True) + label_box(10, 60, 90, 44, ['viewer'], 'card', 9) + label_box(135, 60, 90, 44, ['CDN edge', 'Mumbai'], 'green', 9) + label_box(260, 60, 90, 44, ['bucket', 'origin'], 'blue', 9) + arrow(102, 82, 133, 82) + arrow(227, 82, 258, 82, dash=True) + t(180, 136, 'First view fetches from the bucket;', 9, 'ink2') + t(180, 152, 'later views come from a nearby cache.', 9, 'ink2'),
    t(180, 26, 'Lifecycle rule moves it as it ages', 10, 'violet', bold=True) + ''.join(label_box(10 + k * 86, 56, 80, 50, [n, d], tone, 8.8) + (arrow(92 + k * 86, 81, 94 + k * 86, 81) if k < 3 else '') for k, (n, d, tone) in enumerate([('Hot', 'day 0–90', 'acc'), ('Cool', '90 d–1 yr', 'blue'), ('Archive', '1–5 yr', 'violet'), ('Delete', 'after 5 yr', 'card')]))
    + t(180, 140, 'Each step down costs less per GB per month;', 9, 'ink2') + t(180, 156, 'archive takes hours to restore.', 9, 'ink2'),
]
see_caps = ['Riya adds a photo of her thali to a review and taps Upload.',
            'The 3.1 MB photo uploads in a couple of seconds.',
            'Her review is posted with the photo.',
            'Other customers browse the kitchen page with its review photos.',
            'Riya’s photo opens almost instantly for a viewer in Mumbai.',
            'A year later, the photo in her order history is archived and takes a while to restore.']
behind_caps = ['The app sends the bytes to an upload service with an HTTPS <code>PUT</code>. Nobody chooses a disk or a folder.',
               'The photo becomes an <b>object</b>: a key (bucket plus full name), the bytes, and metadata such as order id and size.',
               'Object storage spreads the data across three availability zones (separate buildings), so even losing a whole zone loses nothing.',
               'The app’s database (on block storage) keeps a small row with the photo’s key. Big binary data stays in object storage.',
               'Viewers fetch the photo through a CDN: the first request goes to the bucket, later ones are served from a cache near the viewer.',
               'A lifecycle rule moves the object from hot to cool to archive tiers as it ages, and deletes it when the retention period ends. (Tier timings are an example policy.)']
two = anim_two('One photo in object storage', 'What Riya sees, and what the storage does', 'Riya uploading and viewing a review photo',
               'How object storage stores, serves and ages the photo', see, behind, see_caps, behind_caps)

# ---------------------------------------------------------------- scenario 1: HDFS write
def dn(x, y, label, blocks, dead=False):
    o = box(x, y, 78, 54, 'red' if dead else 'card') + t(x + 39, y + 14, label, 8.4, 'red' if dead else 'ink', bold=True)
    for k, (b, col) in enumerate(blocks):
        o += fill(x + 6 + k * 24, y + 22, 20, 24, col, rx=3) + t(x + 16 + k * 24, y + 38, b, 7.6, extra=' style="fill:#fff"', bold=True)
    return o
C = {'B1': 'blue', 'B2': 'green', 'B3': 'acc'}
layout = {'DN1': ['B1', 'B3'], 'DN2': ['B1', 'B2'], 'DN3': ['B2', 'B3'], 'DN4': ['B1', 'B2', 'B3'][:1] + ['B3']}
layout = {'DN1': ['B1', 'B2'], 'DN2': ['B1', 'B3'], 'DN3': ['B2', 'B3'], 'DN4': ['B1', 'B2', 'B3']}
def cluster(show, dead=None, extra=None):
    o = label_box(130, 8, 100, 34, ['NameNode', 'block map'], 'violet', 8.8)
    for k, d in enumerate(['DN1', 'DN2', 'DN3', 'DN4']):
        bl = [(b, C[b]) for b in layout[d] if b in show]
        if extra and d in extra:
            bl += [(b, C[b]) for b in extra[d]]
        o += dn(8 + k * 88, 54, d, bl, dead == d)
    return o
fr = [
    label_box(14, 16, 110, 60, ['orders.csv', '300 MB'], 'acc', 10) + arrow(126, 46, 150, 46) + ''.join(label_box(156 + k * 64, 22, 56, 48, [b, s], ['blue', 'green', 'acc'][k], 9) for k, (b, s) in enumerate([('B1', '128 MB'), ('B2', '128 MB'), ('B3', '44 MB')]))
    + cap('The client splits the file into 128 MB blocks.', 'The last block uses only the space it needs (44 MB).', 'blue', y=110, h=44),
    cluster(['B1']) + cap('The NameNode picks 3 DataNodes for B1; the client', 'sends it to the first, which forwards it down a pipeline.', 'blue', y=124, h=44),
    cluster(['B1', 'B2', 'B3']) + cap('All 3 blocks stored, each on 3 different DataNodes.', 'The NameNode records which blocks and where.', 'green', y=124, h=44),
    cluster(['B1', 'B2', 'B3'], dead='DN2') + cap('DN2 dies. Its heartbeats stop. B1 and B3', 'now have only 2 copies each.', 'red', y=124, h=44),
    cluster(['B1', 'B2', 'B3'], dead='DN2', extra={'DN3': ['B1'], 'DN1': ['B3']}) + cap('The NameNode copies B1 to DN3 and B3 to DN1.', 'Back to 3 copies, automatically. No data lost.', 'green', y=124, h=44),
]
s1 = anim_one('Real-time scenario 1', 'Writing a 300 MB file into HDFS, and surviving a dead node',
              'Kabir uploads a 300 MB orders file to a small HDFS cluster with four DataNodes. Watch it split into blocks, get copied three times, and heal itself when a machine fails.',
              'HDFS write and recovery', 'A file split into HDFS blocks, replicated on DataNodes, and re-replicated after a failure', fr,
              ['The HDFS client splits the 300 MB file into blocks of 128 MB, 128 MB and 44 MB. A small last block doesn’t waste a full 128 MB.',
               'For each block, the NameNode chooses three DataNodes (on different racks where possible). The client streams the block to the first, which passes it to the second, which passes it to the third: a write pipeline.',
               'All three blocks are stored three times. The NameNode keeps only metadata: which blocks form the file and where each copy is.',
               'DataNode 2 fails. The NameNode notices missing heartbeats and sees that B1 and B3 have only two copies left.',
               'It schedules new copies from the surviving replicas, so every block is back to three copies. Readers never notice. (Placement shown is simplified.)'],
              hid='animated-example')

# ---------------------------------------------------------------- scenario 2: small files
fr2 = [
    t(180, 22, 'A streaming job writes one file per second', 9.6, 'acc', bold=True) + ''.join(fill(14 + (k % 24) * 14, 36 + (k // 24) * 12, 10, 8, 'acc', rx=1, opacity=.7) for k in range(168))
    + cap('Each file ≈ 50 KB. After one day: 86,400 files.', 'After a year: about 3 crore files, only ~1.5 TB in total.', 'amber', y=134, h=44),
    t(180, 22, 'A daily report opens every file', 9.6, 'red', bold=True) + bars([('list files', 70, 'red', 'slow'), ('open each file', 95, 'red', 'slowest'), ('read bytes', 12, 'green', 'fast'), ('compute', 8, 'green', 'fast')], x=120, y=36, w=170, gap=24)
    + cap('Most time is spent listing and opening, not reading.', 'Each object request also adds to the bill.', 'red', y=144, h=44),
    t(180, 22, 'HDFS: the NameNode fills up', 9.6, 'red', bold=True) + label_box(80, 36, 200, 56, ['NameNode RAM', '≈ 150 bytes per file and per block'], 'violet', 9.2)
    + t(180, 112, '3 crore files + 3 crore blocks ≈ 9 GB of RAM', 9, bold=True) + t(180, 128, 'just to remember tiny files.', 9, 'ink2') + cap('Small files hurt HDFS and object stores in different', 'ways, but both get slower and costlier.', 'red', y=144, h=44),
    t(180, 22, 'Fix: compaction', 9.6, 'green', bold=True) + ''.join(fill(14 + (k % 12) * 14, 40 + (k // 12) * 12, 10, 8, 'acc', rx=1, opacity=.7) for k in range(48)) + arrow(186, 64, 216, 64) + ''.join(fill(224 + k * 30, 36, 24, 58, 'green', rx=3) for k in range(4))
    + cap('A nightly job merges each day’s 86,400 files', 'into a few files of 128 MB to 1 GB.', 'green', y=118, h=44),
    t(180, 22, 'After compaction', 9.6, 'green', bold=True) + bars([('files per day', 1, 'green', '86,400 → 1'), ('report time', 8, 'green', 'minutes → seconds'), ('request cost', 2, 'green', 'tiny')], x=110, y=36, w=110, gap=26)
    + cap('Better: write bigger files from the start (micro-batch', 'every few minutes), and let table formats auto-compact.', 'green', y=130, h=44),
]
s2 = anim_one('Real-time scenario 2', 'The small-files problem: 86,400 files a day',
              'A streaming job at TiffinGo saves rider pings every second, one small file each time. The data is tiny; the trouble is the number of files.',
              'Too many files', 'A job writing thousands of tiny files, the slow report that follows, and compaction into large files', fr2,
              ['Writing one 50 KB file per second gives 86,400 files a day and about 3 crore files a year, although the total data is only around 1.5 TB.',
               'A daily report must list and open every file. Most of the time goes into listing and opening, not reading. In object storage every request is also billed.',
               'On HDFS, the NameNode keeps every file and block in memory, roughly 150 bytes each. Crores of tiny files can exhaust its RAM.',
               '<b>Compaction:</b> a scheduled job rewrites each day’s small files into a few large files of 128 MB to 1 GB.',
               'Reports become fast and cheap again. Even better is to avoid the problem: write in micro-batches every few minutes and use table formats that compact automatically. (Numbers are illustrative.)'])

# ---------------------------------------------------------------- scenario 3 (advanced): rename
def lane(y, title, tone, steps_):
    o = t(14, y + 12, title, 9, TXT.get(tone, 's-ink'), anchor='start', bold=True)
    for k, (s, col) in enumerate(steps_):
        o += fill(110 + k * 60, y, 54, 18, col, rx=4) + t(137 + k * 60, y + 13, s, 7.6, extra=' style="fill:#fff"', bold=True)
    return o
fr3 = [
    t(180, 22, 'A Spark job writes 1,000 output files', 9.6, 'acc', bold=True) + box(14, 36, 332, 70, 'card') + t(180, 58, 'out/_temporary/attempt_7/part-0000 … part-0999', 8.6, mono=True) + t(180, 78, 'then “commit” = rename the folder to out/', 8.8, 'ink2') + t(180, 96, '(safe and instant on HDFS)', 8.6, 'green', bold=True)
    + cap('Writers use a temporary folder, then rename it at the end,', 'so readers never see half-written output.', 'blue', y=124, h=44),
    lane(40, 'HDFS', 'green', [('rename', 'green')]) + t(180, 82, 'One metadata change in the NameNode: milliseconds, atomic.', 8.8, 'ink2')
    + cap('On HDFS a directory rename is a single metadata update.', '', 'green', y=124, h=34),
    lane(40, 'Object store', 'red', [('copy 1', 'red'), ('del 1', 'red'), ('copy 2', 'red'), ('del 2', 'red')]) + t(180, 82, '… repeated for all 1,000 objects: minutes', 8.8, 'red', bold=True)
    + cap('No real folders: “rename” = copy + delete', 'for every object. Slow, and billed per request.', 'red', y=124, h=44),
    lane(40, 'Object store', 'red', [('copy 1', 'red'), ('del 1', 'red'), ('crash!', 'red')]) + t(180, 82, 'Readers now see part of the output: 412 of 1,000 files', 8.8, 'red', bold=True)
    + cap('If the job dies mid-rename, output is half moved.', 'Not atomic: readers may get wrong, partial results.', 'red', y=124, h=44),
    box(14, 30, 332, 84, 'green') + t(180, 50, 'Fix: commit without renaming', 9.8, 'green', bold=True) + t(28, 72, '• table formats (Delta Lake, Iceberg, Hudi) write files once,', 8.6, anchor='start') + t(28, 88, '  then add one atomic entry to a transaction log', 8.6, anchor='start') + t(28, 104, '• or use object-store-aware committers (e.g. S3A committers)', 8.6, anchor='start')
    + cap('Readers see either the old version or the new one,', 'never a half-written mix.', 'green', y=128, h=44),
]
s3 = anim_one('Real-time scenario 3 · advanced', 'Why “rename” is dangerous on object storage',
              'Many big data tools were designed for HDFS, where renaming a folder is instant. Moved to cloud object storage unchanged, the same habit becomes slow and unsafe. Here’s why, and what modern platforms do instead.',
              'Committing output safely', 'Comparing a folder rename on HDFS with copy-and-delete on object storage, and the transaction-log fix', fr3,
              ['Classic Spark and Hadoop jobs write output into a temporary folder and, when finished, rename it to its final name. On HDFS this makes results appear all at once.',
               'On HDFS, renaming a directory is one metadata update in the NameNode: instant and atomic.',
               'Object storage has no real directories. Renaming a “folder” means copying every object to a new key and deleting the old one: 1,000 files means thousands of requests and minutes of waiting.',
               'If the job crashes half-way, some files are under the new name and some under the old. Readers can see partial output, which is a correctness problem, not just a speed problem.',
               'Modern platforms avoid renames: table formats write data files once and then commit by adding a single entry to a transaction log, and special committers do the same for plain files. Readers see the old or the new version, never a mix.'])

realworld = '''  <p>Three live scenarios: a file written into HDFS that heals itself after a node failure, the small-files problem and its fix, and an advanced look at why renaming is unsafe on object storage.</p>
  <!--ANIM2-->''' + s1 + s2 + s3 + '''  <!--/ANIM2-->

  <h3>Where each kind of storage is used</h3>
''' + usecase('<rect x="20" y="20" width="80" height="50" rx="6" class="s-soft-blue" style="stroke:var(--blue)"/><text x="60" y="50" text-anchor="middle" font-size="11" font-weight="700" class="s-blue">DB disk</text>',
              '1. Live app databases on block storage', 'Order, payment and user databases run on fast SSD block volumes (for example Amazon EBS or Azure managed disks), often with copies in another zone for safety.', ['App', '*Database on SSD volume', 'Fast updates']) + usecase(
    '<circle cx="40" cy="45" r="16" style="fill:var(--green);opacity:.7"/><circle cx="70" cy="35" r="12" style="fill:var(--green);opacity:.5"/><circle cx="84" cy="60" r="14" style="fill:var(--green);opacity:.6"/>',
    '2. Data lakes on object storage', 'Most modern lakes keep raw and curated data in S3, ADLS Gen2 or Google Cloud Storage, organised by key prefixes such as <code>bronze/orders/date=…/</code>, with Spark, SQL engines and ML reading directly from there.', ['Apps + Kafka', '*Object storage lake', 'Spark · SQL · ML']) + usecase(
    '<rect x="16" y="30" width="22" height="34" rx="3" style="fill:var(--blue)"/><rect x="44" y="30" width="22" height="34" rx="3" style="fill:var(--blue);opacity:.7"/><rect x="72" y="30" width="22" height="34" rx="3" style="fill:var(--blue);opacity:.5"/>',
    '3. On-premises Hadoop clusters with HDFS', 'Banks, telecoms and government departments that must keep data in their own data centres still run HDFS clusters, sometimes alongside an on-prem object store.', ['Core systems', '*HDFS + Hive / Spark', 'Regulatory reports']) + usecase(
    '<rect x="20" y="20" width="80" height="50" rx="6" class="s-soft-violet" style="stroke:var(--violet)"/><text x="60" y="50" text-anchor="middle" font-size="10" font-weight="700" class="s-violet">Archive</text>',
    '4. Backups and compliance archives', 'Old transaction data, call recordings and CCTV footage that must be kept for years go to archive tiers that cost a fraction of hot storage, with lifecycle rules handling the moves.', ['Hot data', '*Lifecycle rules', 'Archive tier'])

body = ('<!-- generated by _body.py -->\n' + part(1, 'story', 'The story', '“2 PB in S3 and no file servers”', story)
        + part(2, 'definition', 'Definition', 'Block, file and object storage', definition)
        + part(3, 'types', 'Types and ways to use it', 'Four kinds of storage compared', types)
        + part(4, 'steps', 'Step by step', 'From one database disk to a petabyte lake', steps)
        + part(5, 'animation', 'See it happen', 'One photo: what Riya sees, and what the storage does', '  <p>Step through the six frames. Left: Riya uploading and viewing a review photo. Right: how object storage stores, serves and ages it.</p>\n' + two)
        + part(6, 'real-world', 'Real-world use', 'Real-time scenarios: storage under load', realworld))
open(os.path.join(HERE, 'body.html'), 'w', encoding='utf-8').write(body)

scen = (scn('Platform design · storage', 'Fresher', 'Where should each kind of data live?',
            'A new fintech app has customer accounts, a stream of transactions, KYC document scans and seven years of history for audits. Where would you store each?',
            'can you match workloads to block, file and object storage?',
            '<ul><li><b>Accounts and live transactions:</b> a relational database on SSD block storage, replicated across zones.</li><li><b>Transaction history for analytics:</b> Parquet tables in object storage (the lake), partitioned by date.</li><li><b>KYC scans:</b> object storage with encryption, restricted access and the object key stored in the database.</li><li><b>Seven-year audit data:</b> lifecycle rules moving old partitions to cool and archive tiers, with deletion after the legal period.</li></ul>',
            'putting scanned documents in database tables, or everything on expensive SSD volumes.')
        + scn('Performance · small files', '1–3 years', 'The report got slower every week',
              'A daily Spark report on a Kafka-fed table took 5 minutes in January and 50 minutes in June. Data volume grew only 20%.',
              'do you suspect the small-files problem and know how to confirm and fix it?',
              '<ol><li>Count files and their average size per partition; you will likely find thousands of KB-sized files per day.</li><li>Check where time goes in the Spark UI: listing and task scheduling for tiny tasks dominate.</li><li>Fix the writer: larger micro-batches, fewer output partitions (<code>coalesce</code>), or a table format with optimised writes.</li><li>Run compaction (for example Delta <code>OPTIMIZE</code>) on old partitions.</li><li>Add a monitor on average file size so it doesn’t creep back.</li></ol>',
              'adding more executors, which only creates even more tiny tasks.')
        + scn('Migration · HDFS to cloud', '1–3 years', 'Our jobs broke after moving to S3',
              'A team copied its Hadoop jobs from HDFS to S3 unchanged. Jobs now run much longer at the commit step, and once a crash left a half-written output folder that a dashboard read.',
              'do you know the semantic differences between HDFS and object storage?',
              '<p>HDFS renames are atomic metadata operations; on S3 a directory rename is copy-plus-delete of every object, slow and not atomic. Use object-store-aware committers (such as the S3A committers) or, better, write through a table format (Delta Lake, Iceberg, Hudi) that commits via a transaction log. Also revisit file sizes, listing-heavy code and data-locality assumptions, since compute and storage are now separate.</p>',
              'blaming S3 performance and adding bigger clusters.')
        + scn('Fundamentals · interview', 'Fresher', '“Explain HDFS architecture”',
              'A standard interview question: describe how HDFS stores a file and handles failures.',
              'can you explain blocks, replication, NameNode and DataNodes clearly?',
              '<p>A file is split into large blocks (128 MB by default). Each block is stored on several DataNodes (replication factor 3 by default, placed on different racks for safety). The <b>NameNode</b> holds the namespace (directories, files) and the mapping of blocks to DataNodes in memory; DataNodes store the blocks and send heartbeats and block reports. On a DataNode failure, the NameNode re-replicates the affected blocks from surviving copies. Clients get block locations from the NameNode and read data directly from DataNodes. For high availability, a standby NameNode takes over if the active one fails.</p>',
              'confusing the NameNode with storage of the actual data.'))
open(os.path.join(HERE, 'scenarios.html'), 'w', encoding='utf-8').write(scen)
print('written')
