import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Find the papers\' ideas',
    intro='<p>The NameNode is the GFS master, the DataNodes are the chunkservers, and the job is MapReduce. Spot each idea from the animation.</p>',
    racks=2, nodes=3, features=['upload', 'job', 'fail'],
    preload=[dict(name='nutch_crawl_segment.dat', sizeMB=1024)],
    **{'try': [
        dict(text='<b>One master, many workers:</b> open NameNode metadata. Who knows where every block is?'),
        dict(text='<b>Big chunks, 3 replicas across racks:</b> upload a file with 64 MB blocks (the GFS chunk size), then one with 128 MB.', on='upload-done'),
        dict(text='<b>Map tasks near the data:</b> run the job and check the data-local count in the Event log.', on='job-done'),
        dict(text='<b>Re-execution on failure:</b> run it again and stop a busy node.', on='node-stop'),
    ]},
)))

META = dict(
    module='02-why-hadoop', lesson='02-from-google-s-papers-to-apache-hadoop', n='2.2',
    module_label='Module 2 · Why Hadoop was born',
    title='From Google\'s papers to Apache Hadoop',
    desc='The history of Hadoop: Apache Nutch, Google\'s GFS (2003) and MapReduce (2004) papers, NDFS, the birth of Hadoop in 2006, Yahoo!, the 2008 terabyte sort record, Apache top-level status, releases to 3.5.0 in 2026, and which paper ideas became which Hadoop parts. With animations, a playground, Python you can run, quiz and interview questions.',
    og_desc='Two Google research papers, an open-source search engine and a toy elephant\'s name: how Hadoop was born.',
    minutes=22, level='Beginner → Intermediate',
    lead='Hadoop began as two research papers from Google and an open-source search engine that needed to grow. This lesson follows the story year by year, from Nutch and the GFS and MapReduce papers to Yahoo!, the record-breaking terabyte sort and today\'s releases, and shows exactly which idea in each paper became which part of Hadoop.',
    chips=['Timeline with exact dates', 'Cluster Playground', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='Hadoop\'s history as data',
    intro='<p>A timeline is just a list of (year, event) pairs. This program sorts the milestones, prints them, and works out how long each step took. Then try the challenges, including the famous 2008 sort record.</p>',
    code='''events = [
    (2006, "Hadoop leaves Nutch; Doug Cutting joins Yahoo!"),
    (2003, "Google publishes the GFS paper"),
    (2008, "Hadoop becomes a top-level Apache project"),
    (2004, "Google publishes the MapReduce paper"),
    (2002, "Apache Nutch starts"),
    (2011, "Hadoop 1.0.0 released"),
]

events.sort()
prev = None
for year, what in events:
    gap = f"(+{year - prev} y)" if prev else ""
    print(year, what, gap)
    prev = year
''',
    anno=[
        ('events.sort()', 'Tuples sort by their first item, the year, so the list comes out in time order.'),
        ('for year, what in events:', 'Unpacking: each tuple\'s two parts go into <code>year</code> and <code>what</code>.'),
        ('gap = f"(+{year - prev} y)" if prev else ""', 'A conditional expression: show the gap from the previous event, except for the first one.'),
    ],
    tasks=[
        dict(label='1 · Timeline', hint='Press <b>Run</b>. Add <code>(2013, "Hadoop 2.2.0: YARN")</code> and <code>(2017, "Hadoop 3.0.0")</code>.', code=None),
        dict(label='2 · The 2008 sort record', hint='<b>Predict first:</b> 1 TB sorted by 910 nodes in 209 seconds. How many MB per second did each node handle?',
             code='''tb, nodes, seconds = 1, 910, 209
mb = tb * 1024 * 1024
print(f"Whole cluster: {mb / seconds:,.0f} MB/s")
print(f"Each node    : {mb / seconds / nodes:.1f} MB/s")
'''),
        dict(label='3 · Paper → Hadoop', hint='Look up the Hadoop name for each Google idea. Add <code>"Chubby": "ZooKeeper (similar role)"</code>.',
             code='''google_to_hadoop = {
    "GFS": "HDFS",
    "GFS master": "NameNode",
    "chunkserver": "DataNode",
    "MapReduce": "Hadoop MapReduce",
    "Bigtable": "HBase",
}
for idea in ["chunkserver", "Bigtable", "GFS master"]:
    print(idea, "->", google_to_hadoop[idea])
'''),
        dict(label='4 · Block size over time', hint='How many blocks does a 1 GB file have with the GFS/early-Hadoop 64 MB size, the Hadoop 2+ default of 128 MB, and 256 MB?',
             code='''import math
file_mb = 1024
for block in [64, 128, 256]:
    print(f"{block:>3} MB blocks -> {math.ceil(file_mb / block)} blocks")
'''),
        dict(label='5 · Spot the error', hint='This should print how many years passed between the GFS paper and Hadoop 1.0, but it crashes. Fix the types.',
             expect='error',
             code='''gfs = "2003"
v1 = 2011
print("Years:", v1 - gfs)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

TRACE = dict(
    heading='Building a timeline, one line at a time',
    intro='<p>Watch the list of milestones get sorted, then the loop calculate the gap between each event and the one before it.</p>',
    code='''events = [(2006, "Hadoop"), (2003, "GFS paper"), (2004, "MapReduce paper")]
events.sort()
prev = events[0][0]
for year, what in events:
    print(year, what, "+", year - prev)
    prev = year
''',
    notes={2: 'Sort :: Tuples are compared by their first item (the year).'},
)

WORKED_INTRO = 'Three small problems built on real numbers from Hadoop\'s history: a release table, the sort record, and how block size changed. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='History · releases', title='Years between major releases',
         problem='<p>Given the release years of Hadoop 1.0 (2011), 2.2 (2013), 3.0 (2017) and 3.5 (2026), print how many years each major line came after the previous one.</p>',
         inp='1.0 2011 · 2.2 2013 · 3.0 2017 · 3.5 2026',
         approach=['Store versions and years as a list of pairs.',
                   'Loop from the second item, comparing with the one before it.',
                   'Print the gap.'],
         code='''releases = [("1.0", 2011), ("2.2", 2013), ("3.0", 2017), ("3.5", 2026)]
for i in range(1, len(releases)):
    v, y = releases[i]
    pv, py = releases[i - 1]
    print(f"{pv} -> {v}: {y - py} years")
''', notes={1: 'Data :: Release years from the Apache Hadoop release pages.'},
         tryit='Add 3.3 (2020) and 3.4 (2024) between 3.0 and 3.5. Hadoop now ships smaller releases more often.'),
    dict(level='i', tag='Performance · benchmark', title='What did the 2008 sort record mean per disk?',
         problem='<p>The record cluster had <b>910 nodes</b> with <b>4 disks</b> each and sorted <b>1 TB in 209 s</b>. A sort reads the data and writes it back at least once. Estimate the MB/s each disk handled for reading plus writing.</p>',
         inp='910 nodes × 4 disks · 1 TB · 209 s · read + write',
         approach=['Total bytes moved through disks ≈ 2 × 1 TB (read once, write once).',
                   'Divide by time and by the number of disks.',
                   'Compare with a disk of that era (roughly 50–80 MB/s).'],
         code='''disks = 910 * 4
mb_moved = 2 * 1024 * 1024        # read 1 TB + write 1 TB
per_disk = mb_moved / 209 / disks
print(f"Disks: {disks}")
print(f"Each disk: about {per_disk:.1f} MB/s")
''', notes={2: 'Simplification :: Real sorts also write and read intermediate data, so true disk traffic was higher.'},
         tryit='The disks were not even close to their limit. What else limited the job? (The network: 40 nodes per rack shared 8 Gbps of uplinks.)'),
    dict(level='a', tag='HDFS · design history', title='How did the jump from 64 MB to 128 MB blocks help the NameNode?',
         problem='<p>The NameNode keeps an object for every block in memory (roughly 150 bytes each, a common rule of thumb). For <b>2 PB</b> of data with 3 replicas, compare the number of block objects and the memory needed with 64 MB and 128 MB blocks.</p>',
         inp='2 PB of files · 64 vs 128 MB blocks · ~150 bytes per block object',
         approach=['Blocks = data size ÷ block size (replicas are tracked inside each block object, so count blocks once).',
                   'Memory ≈ blocks × 150 bytes.',
                   'Print both sizes side by side.'],
         code='''pb = 2
data_mb = pb * 1024 * 1024 * 1024
for block_mb in [64, 128]:
    blocks = data_mb / block_mb
    gb = blocks * 150 / 1024**3
    print(f"{block_mb:>3} MB: {blocks / 1e6:.1f} million blocks, ~{gb:.1f} GB of NameNode RAM")
''', notes={3: 'Size :: 2 PB in MB.'},
         tryit='The same 2 PB stored as 1 MB files would need about 2 billion block objects plus as many file objects. That is the small-files problem (Module 7).'),
]

QUIZ = mix([
    dict(q='Which Google paper inspired HDFS?', options=['Bigtable', 'The Google File System (2003)', 'MapReduce (2004)', 'Chubby'], answer=1,
         why='HDFS is modelled on <b>GFS</b>: a master for metadata, many chunk (block) servers, large chunks and replication.'),
    dict(q='Who started the project from which Hadoop came?', options=['Larry Page and Sergey Brin', 'Doug Cutting and Mike Cafarella', 'Linus Torvalds', 'Matei Zaharia'], answer=1,
         why='Doug Cutting and Mike Cafarella started <b>Apache Nutch</b>; its storage and MapReduce code became Hadoop.'),
    dict(q='In which year did Hadoop become a separate project, split out of Nutch?', options=['2003', '2004', '2006', '2011'], answer=2,
         why='In <b>2006</b> the code moved into its own project named Hadoop, around the time Doug Cutting joined Yahoo!.'),
    dict(q='Which Hadoop component plays the role of the GFS master?', options=['DataNode', 'NameNode', 'TaskTracker', 'HBase'], answer=1,
         why='The <b>NameNode</b> holds the namespace and block locations, like the GFS master.'),
    dict(q='Which company invested most heavily in scaling Hadoop in its early years?', options=['Microsoft', 'Yahoo!', 'Oracle', 'IBM'], answer=1,
         why='<b>Yahoo!</b> hired Doug Cutting and ran Hadoop on very large clusters for search, contributing much of the core code.'),
    dict(q='Hive, which lets you query Hadoop data with SQL, was created at:', options=['Google', 'Yahoo!', 'Facebook', 'Cloudera'], answer=2,
         why='Hive was built at <b>Facebook</b> so analysts could use SQL instead of writing Java MapReduce jobs.'),
    dict(q='What did the 2008 terabyte sort record show?', options=['Hadoop could only sort small files', 'Open-source software on commodity servers could beat specialised systems at scale', 'Sorting is impossible on clusters', 'Google used Hadoop'], answer=1,
         why='A 910-node Hadoop cluster sorted 1 TB in 209 seconds, a world record at the time.'),
    dict(q='Where does the name “Hadoop” come from?', options=['An acronym for “High Availability Distributed Object-Oriented Platform”', 'A toy elephant belonging to Doug Cutting\'s son', 'A village in Kerala', 'A Google project code name'], answer=1,
         why='It was the name of his young son\'s toy elephant. It is not an acronym.'),
])

REVISION = [
    '<b>2002</b> Nutch (Cutting, Cafarella) → <b>2003</b> GFS paper → <b>2004</b> MapReduce paper; NDFS in Nutch.',
    '<b>2006</b> Hadoop splits from Nutch (Lucene sub-project); Cutting joins Yahoo!.',
    '<b>Jan 2008</b> top-level Apache project; <b>2008</b> 910 nodes sort 1 TB in 209 s.',
    'Releases: <b>1.0</b> Dec 2011 · <b>2.2</b> (YARN GA) Oct 2013 · <b>3.0</b> Dec 2017 · <b>3.5.0</b> Apr 2026.',
    'GFS master → <b>NameNode</b>; chunkservers → <b>DataNodes</b>; 64 MB chunks → blocks (128 MB since Hadoop 2).',
    'MapReduce paper → Hadoop MapReduce: map, shuffle, reduce, re-execution, backup (speculative) tasks, locality.',
    'Bigtable → <b>HBase</b>; Chubby → similar role as <b>ZooKeeper</b>.',
    'Ecosystem: Hive (Facebook), Pig (Yahoo!), HBase, ZooKeeper, Spark. Distributions: Cloudera, Hortonworks, MapR.',
    'Name: a toy elephant, not an acronym.',
]
FAQ = [
    ('Briefly explain the history of Hadoop.', 'Doug Cutting and Mike Cafarella started Apache Nutch, an open-source web search engine, in 2002. Google published the GFS paper in 2003 and the MapReduce paper in 2004; the Nutch team implemented both (NDFS and MapReduce). In 2006 that code was separated into a new project, Hadoop, and Cutting joined Yahoo!, which invested heavily in it. Hadoop became a top-level Apache project in January 2008, won the terabyte sort benchmark that year, and reached version 1.0 in December 2011, 2.x with YARN in 2013 and 3.0 in 2017.'),
    ('How is HDFS related to GFS?', 'HDFS is an open-source design based on GFS. Both have a single metadata master (GFS master / NameNode) and many storage servers (chunkservers / DataNodes), split files into large chunks or blocks, replicate each chunk (3 by default) across racks, and keep the master out of the data path so clients read data directly from storage servers.'),
    ('What was Yahoo!\'s role in Hadoop?', 'Yahoo! hired Doug Cutting in 2006 and funded a large engineering team to make Hadoop run reliably on thousands of machines for its search and advertising data. Much of Hadoop\'s core code and scalability work came from Yahoo!, and Hortonworks was later spun out of its Hadoop team.'),
    ('What is the Hadoop ecosystem?', 'The set of projects that grew around HDFS and MapReduce/YARN: Hive (SQL), Pig (data-flow scripts), HBase (NoSQL database), ZooKeeper (coordination), Oozie (workflows), Sqoop and Flume (data ingestion), and processing engines such as Tez and Spark. Module 13 covers which are still widely used.'),
    ('Why did Hadoop become popular so quickly?', 'It was free and open source, ran on cheap commodity hardware, was proven at very large scale by Yahoo! and others, solved a problem many companies suddenly had (rapidly growing log and web data), and had a growing ecosystem and commercial support from distribution vendors.'),
]

PRACTICE_INTRO = 'Small programs around Hadoop\'s real history and numbers. The business problems ask the kind of questions a team asked when deciding to adopt it.'
PROBLEMS = [
    dict(level='easy', title='Years from paper to 1.0', stmt='The GFS paper came out in 2003 and Hadoop 1.0 in 2011. How many years apart?', inp='2003 · 2011',
         code='print(2011 - 2003, "years")\n', explain='Eight years from published idea to a 1.0 release, while it was already in heavy production use.'),
    dict(level='easy', title='Records in the sort benchmark', stmt='The terabyte sort used 100-byte records. How many records are in 1 TB (10<sup>12</sup> bytes, as the benchmark defines it)?', inp='10^12 bytes · 100 bytes per record',
         code='print(f"{10**12 // 100:,} records")\n', explain='10 billion records, sorted in 209 seconds: almost 5 crore records per second across the cluster.'),
    dict(level='easy', title='Look up the counterpart', stmt='Using a dictionary, print the open-source counterpart of “GFS” and of “Bigtable”.', inp='{"GFS": "HDFS", "MapReduce": "Hadoop MapReduce", "Bigtable": "HBase"}',
         code='''m = {"GFS": "HDFS", "MapReduce": "Hadoop MapReduce", "Bigtable": "HBase"}
print(m["GFS"], "|", m["Bigtable"])
''', explain='Knowing these three pairs answers a very common viva question.'),
    dict(level='medium', title='Releases per year', stmt='Given a list of release years, count how many releases happened in each year.', inp='[2024, 2024, 2025, 2026, 2024, 2025]',
         code='''years = [2024, 2024, 2025, 2026, 2024, 2025]
count = {}
for y in years:
    count[y] = count.get(y, 0) + 1
print(dict(sorted(count.items())))
''', explain='A frequency count with a dictionary, the same pattern a word-count job uses (Module 8).'),
    dict(level='medium', title='Sort rate per node', stmt='Print the number of 100-byte records each of the 910 nodes sorted per second in the 2008 record (10 billion records in 209 s).', inp='10,000,000,000 records · 209 s · 910 nodes',
         code='''records, seconds, nodes = 10_000_000_000, 209, 910
print(f"{records / seconds / nodes:,.0f} records per node per second")
''', explain='About 52,580 records per node per second, on machines with 8 GB RAM and four SATA disks.'),
    dict(level='medium', title='Which era is a version from?', stmt='Write a function that returns “Hadoop 1 (JobTracker)”, “Hadoop 2 (YARN)” or “Hadoop 3” for a version string like "2.7.3".', inp='["1.2.1", "2.7.3", "3.3.6", "3.5.0"]',
         code='''def era(v):
    major = int(v.split(".")[0])
    return {1: "Hadoop 1 (JobTracker)", 2: "Hadoop 2 (YARN)"}.get(major, "Hadoop 3")

for v in ["1.2.1", "2.7.3", "3.3.6", "3.5.0"]:
    print(v, "->", era(v))
''', explain='Useful when you meet an old cluster: the major version tells you which architecture you are dealing with.'),
    dict(level='business', title='Licence cost avoided', stmt='A company compares a proprietary system at Rs 4 lakh per node per year in licences with open-source Hadoop (no licence) plus Rs 60,000 per node per year for a support subscription. For 50 nodes over 3 years, what is saved?', inp='50 nodes · 3 years · Rs 4 lakh vs Rs 60,000 per node-year',
         code='''nodes, years = 50, 3
proprietary = nodes * years * 4_00_000
open_source = nodes * years * 60_000
print(f"Saved: Rs {(proprietary - open_source) / 1e7:.1f} crore")
''', explain='Rs 5.1 crore over three years (illustrative prices). Open source does not mean zero cost, but the economics drove adoption.'),
    dict(level='business', title='Was the record cluster network-bound?', stmt='The 2008 record cluster had 40 nodes per rack, each with 1 Gbps, and 8 Gbps of uplinks per rack. Print the oversubscription ratio and the uplink share per node when every node sends out of the rack at once.', inp='40 × 1 Gbps · 8 Gbps uplinks',
         code='''down, up = 40 * 1, 8
print(f"Oversubscription: {down / up:.0f} : 1")
print(f"Each node gets {up / 40 * 1000:.0f} Mbps when all send at once")
''', explain='5 : 1. During the shuffle of a sort, almost all data crosses racks, so the uplinks, not the disks, set the pace. The lesson from Module 1 was already true in 2008.'),
]

SCN_INTRO = 'History questions in interviews are usually about understanding, not memorising dates. These show how to turn the story into a strong answer.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Tell me how Hadoop started.”</h4>
      <p class="scn__situation">An interviewer opens with this to see how you explain things. You have one minute.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> can you tell a clear, correct story and connect it to the design?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <p>“Around 2003–04 Google published two papers describing how it stored and processed the web: GFS and MapReduce. Doug Cutting and Mike Cafarella were building Nutch, an open-source search engine that had the same scaling problem, so they implemented those designs. In 2006 that code became its own project, Hadoop, and Yahoo! invested heavily to run it on thousands of machines. That's why HDFS looks like GFS (a NameNode master, DataNodes, big blocks, three replicas) and why Hadoop MapReduce follows the paper's map–shuffle–reduce model with automatic re-execution.”</p>
        <p class="scn__avoid"><b>Avoid:</b> saying “Google created Hadoop.” Google published ideas; Hadoop was written by the open-source community.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Platform team · legacy</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>You inherit a Hadoop 2.7 cluster</h4>
      <p class="scn__situation">On your first day you find the company runs Hadoop 2.7, released around 2015–16, on Java 7. Your manager asks what you think.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you know the version history well enough to see the risks of very old releases?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The 2.7 line is long out of active maintenance, so it no longer receives security fixes or bug fixes.</li>
          <li>Java 7 is far out of support, and Hadoop 3 needs at least Java 8; newer 3.x lines support newer Java versions.</li>
          <li>Missing features: erasure coding, multiple standby NameNodes, improved cloud connectors and many performance fixes (Lesson 2.4).</li>
          <li>Propose an upgrade plan: inventory jobs and dependencies, test on a staging cluster, upgrade Java, then HDFS and YARN with a rollback plan, or consider migrating to a supported distribution or cloud service.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> “It works, leave it.” Unsupported software is a security risk.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Architecture · open source</span><span class="scn__tag scn__tag--level">1–3 years</span></div>
      <h4>Why did an open-source copy beat the original?</h4>
      <p class="scn__situation">The interviewer asks: “Google's internal systems were years ahead. Why did Hadoop, not Google's code, become the industry standard?”</p>
      <p class="scn__look"><b>The interviewer is checking:</b> do you understand how open-source ecosystems grow?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Google's code was internal and tied to its own infrastructure; nobody else could use it.</li>
          <li>Hadoop was free (Apache licence), ran on ordinary servers, and many companies improved the same code base, so it got better fast.</li>
          <li>An ecosystem (Hive, HBase, Pig, later Spark) and commercial support (Cloudera, Hortonworks, MapR) made it practical for enterprises.</li>
          <li>Neutral governance at the Apache Software Foundation let competitors collaborate.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> claiming Hadoop was technically superior to Google's systems; the advantage was openness and ecosystem.</p>
      </div></details>
    </article>

    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Any company · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Does HDFS still use 64 MB blocks?”</h4>
      <p class="scn__situation">You mention blocks while explaining HDFS, and the interviewer asks what the default block size is, and why it changed.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> are you up to date, and do you know why block size matters?</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Early Hadoop used 64 MB, like the 64 MB chunks of GFS. Since Hadoop 2 the default is <b>128 MB</b> (<code>dfs.blocksize</code>); many clusters use 256 MB for big files.</li>
          <li>Bigger blocks mean fewer block objects in NameNode memory and fewer, longer map tasks (less scheduling overhead). Disks also got faster, so a 128 MB read still takes only about a second.</li>
          <li>Too big a block reduces parallelism for medium-sized files.</li>
        </ul>
        <p class="scn__avoid"><b>Avoid:</b> quoting 64 MB as today's default.</p>
      </div></details>
    </article>'''
