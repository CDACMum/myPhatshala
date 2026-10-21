import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE).replace('{{PLAYGROUND}}', playground(dict(
    title='Same file, different block sizes',
    intro='<p>Upload a <b>1 GB</b> file three times with Block set to <b>64</b>, <b>128</b> and <b>256</b> MB. Compare the block counts in the NameNode metadata tab, then run the job.</p>',
    racks=2, nodes=3, features=['upload', 'job', 'fsck'],
    **{'try': [
        dict(text='Upload 1 GB with <b>64 MB</b> blocks.', on='upload-done'),
        dict(text='Upload 1 GB with <b>128 MB</b> blocks.', on='upload-done'),
        dict(text='Upload 1 GB with <b>256 MB</b> blocks: 16, 8, then 4 blocks for the same data.', on='upload-done'),
        dict(text='Run the job: one map task per block of the input.', on='job-done'),
    ]},
)))

META = dict(
    module='05-hdfs-architecture', lesson='02-blocks', n='5.2',
    module_label='Module 5 · HDFS architecture',
    title='Blocks (and how they differ from splits)',
    desc='HDFS blocks: why files are stored as 128 MB blocks, how the last block uses only its real size, the 1 MB minimum, and why block size is chosen per file. Shown on a real Hadoop 3.5.0 cluster: a record cut across a block boundary, and a MapReduce job whose 5 splits read 70,485 + 67,321 + 65,498 + 65,574 + 31,123 = 300,001 records. Block vs input split, RecordReader rules, Python simulator, quiz and interview scenarios.',
    og_desc='HDFS cuts files by bytes, even mid-record. Splits put the records back together. See both on a real cluster.',
    minutes=26, level='Beginner → Intermediate',
    lead='HDFS stores every file as fixed-size blocks, cut at exact byte counts with no regard for lines or records. MapReduce then divides the work into input splits that follow those blocks but always deliver whole records. This lesson shows both on a real cluster: a canteen order sliced in two by a block boundary, and the job counters proving every order was still read exactly once.',
    chips=['Real block files', 'Hadoop-exact split simulator', 'Cluster Playground'],
)

RUN = dict(
    heading='Cut a file into blocks, then read it in splits',
    intro='<p>This program stores a small CSV in 32-byte “blocks” (as HDFS would with a tiny block size), shows how lines get cut, then reads each split with Hadoop\'s two rules: <i>skip the partial first line unless you are split 0</i> and <i>finish the record that starts inside your split</i>.</p>',
    code='''data = "1001,samosa,18\\n1002,vada pav,20\\n1003,poha,25\\n1004,dosa,45\\n1005,chai,15\\n"
BLOCK = 32
blocks = [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]
for i, b in enumerate(blocks):
    print(f"block {i}: {b!r}")

for i in range(len(blocks)):
    start, end = i * BLOCK, min((i + 1) * BLOCK, len(data))
    pos = start if i == 0 else data.index("\\n", start - 1) + 1
    records = []
    while pos < end:
        nl = data.index("\\n", pos)
        records.append(data[pos:nl])
        pos = nl + 1
    print(f"split {i}: {records}")
''',
    anno=[
        ('blocks = [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]', 'Blocks are cut every 32 characters, wherever that falls. Look for cut-off orders in the output.'),
        ('pos = start if i == 0 else data.index("\\n", start - 1) + 1', 'Rule 1: every split except the first skips to just after the first newline at or after its start (looking one byte back, in case the split starts exactly at a line).'),
        ('while pos < end:', 'Rule 2: a record that <b>starts</b> before the end of the split belongs to it, even if it ends in the next block.'),
    ],
    tasks=[
        dict(label='1 · Blocks vs splits', hint='Press <b>Run</b>. Which orders are cut by block boundaries, and which split reads each of them whole?', code=None),
        dict(label='2 · Change the block size', hint='<b>Predict first:</b> with <code>BLOCK = 20</code>, how many blocks and how many records per split? Every order must still appear exactly once.',
             code='''data = "1001,samosa,18\\n1002,vada pav,20\\n1003,poha,25\\n1004,dosa,45\\n1005,chai,15\\n"
BLOCK = 20
n = (len(data) + BLOCK - 1) // BLOCK
total = 0
for i in range(n):
    start, end = i * BLOCK, min((i + 1) * BLOCK, len(data))
    pos = start if i == 0 else data.index("\\n", start - 1) + 1
    count = 0
    while pos < end:
        pos = data.index("\\n", pos) + 1
        count += 1
    total += count
    print(f"split {i}: {count} record(s)")
print(n, "blocks,", total, "records in total")
'''),
        dict(label='3 · Blocks for a file size', hint='How many blocks, and how big is the last one, for the real 4,692,009-byte file with 1 MB and 128 MB blocks?',
             code='''size = 4_692_009
for block in [1_048_576, 134_217_728]:
    n = -(-size // block)
    last = size - (n - 1) * block
    print(f"block {block:>11,}: {n} block(s), last block {last:,} bytes")
'''),
        dict(label='4 · Why 128 MB?', hint='A disk seeks for 10 ms and reads 150 MB/s. What share of time is spent seeking for blocks of 1, 64, 128 and 256 MB?',
             code='''seek_s, mb_per_s = 0.010, 150
for mb in [1, 64, 128, 256]:
    read_s = mb / mb_per_s
    print(f"{mb:>4} MB block: seeking {seek_s / (seek_s + read_s):.1%} of the time")
'''),
        dict(label='5 · Spot the error', hint='This reader drops a record at every boundary. Compare with Rule 2 in the main program and fix it.',
             code='''data = "a1\\nb22\\nc333\\nd4444\\n"
BLOCK = 6
for i in range(-(-len(data) // BLOCK)):
    start, end = i * BLOCK, min((i + 1) * BLOCK, len(data))
    pos = start if i == 0 else data.index("\\n", start - 1) + 1
    recs = []
    while pos < end:
        nl = data.index("\\n", pos)
        if nl < end:
            recs.append(data[pos:nl])
        pos = nl + 1
    print(i, recs)
'''),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: predict Hadoop\'s split counters exactly',
    intro='<p>This script applies HDFS block cutting and Hadoop\'s <code>LineRecordReader</code> rules to the real <code>canteen_orders.csv</code> (from <code>make_canteen.py</code>, Lesson 4.3) with 1 MB blocks. Save it as <code>blocks_and_splits.py</code> next to the CSV and run it. Then compare with the job counters in Part 4.</p>',
    items=[
        dict(title='Blocks, splits and the cut record, without Hadoop', file='blocks_and_splits.py',
             cmd=open(os.path.join(HERE, 'blocks_and_splits.py')).read() + '\n# In a terminal:\n#   python3 blocks_and_splits.py',
             output='''canteen_orders.csv: 4,692,009 bytes -> 5 blocks of up to 1,048,576 bytes
split 0: bytes       0-1048575  records  70485
split 1: bytes 1048576-2097151  records  67321
split 2: bytes 2097152-3145727  records  65498
split 3: bytes 3145728-4194303  records  65574
split 4: bytes 4194304-4692008  records  31123
record cut by block 0/1: b'71484,poha,2' + b'5\'''',
             note='Every count matches the five “Map input records” counters of the real Hadoop job, and the cut record is the same one found in the block files on the DataNode.'),
    ],
)

TRACE = dict(
    heading='Reading split 1, one line at a time',
    intro='<p>Follow the reader of the <b>second</b> split. Watch how it skips the partial line and where it stops.</p>',
    code='''data = "71483,dosa,45\\n71484,poha,25\\n71485,idli,30\\n"
start, end = 26, len(data)
pos = data.index("\\n", start - 1) + 1
records = []
while pos < end:
    nl = data.index("\\n", pos)
    records.append(data[pos:nl])
    pos = nl + 1
print(records)
''',
    notes={2: 'Boundary :: Byte 26 is inside “71484,poha,25” (between “2” and “5”).',
           3: 'Skip :: Jump past the next newline: the partial record belongs to the previous split.',
           7: 'Read :: Whole records from here on.'},
)

WORKED_INTRO = 'Three block calculations that come up in real projects: how many blocks and map tasks a data set produces, how a block-size change affects the NameNode, and how splits are formed with the 10% slop rule. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Planning · tasks', title='How many map tasks will this job start?',
         problem='<p>A job reads three files: 1 GB, 300 MB and 50 MB, all with 128 MB blocks. How many blocks, and how many map tasks (one per split, splits = blocks by default)?</p>',
         inp='1024 MB · 300 MB · 50 MB · 128 MB blocks',
         approach=['Blocks per file = ceil(size / 128).',
                   'Every file starts its own splits; small files still need one.',
                   'Sum them.'],
         code='''import math
files = {"sales.csv": 1024, "returns.csv": 300, "stores.csv": 50}
total = 0
for name, mb in files.items():
    n = math.ceil(mb / 128)
    total += n
    print(f"{name:12} {mb:>5} MB -> {n} block(s)")
print("map tasks:", total)
''', notes={5: 'Per file :: A 50 MB file still costs a whole map task.'},
         tryit='Replace stores.csv with 500 files of 100 KB. How many map tasks now? Many small files mean many tiny tasks.'),
    dict(level='i', tag='NameNode · objects', title='What does doubling the block size save?',
         problem='<p>A 600 TB data warehouse is stored with 128 MB blocks. How many blocks is that, and how much NameNode heap would 256 MB blocks save, at 150 bytes per block object?</p>',
         inp='600 TB · 128 vs 256 MB · 150 B per block',
         approach=['Blocks = data / block size.',
                   'Heap for blocks = blocks × 150 bytes.',
                   'Difference between the two sizes.'],
         code='''tb_mb = 600 * 1024 * 1024
b128, b256 = tb_mb // 128, tb_mb // 256
saved_gb = (b128 - b256) * 150 / 2**30
print(f"128 MB: {b128:,} blocks   256 MB: {b256:,} blocks")
print(f"heap saved ~{saved_gb:.2f} GB")
''', notes={2: 'Count :: 600 TB in MB divided by block size.'},
         tryit='The saving is modest for big files. The real heap problem is small files (Lesson 7.5), where block size does not help at all.'),
    dict(level='a', tag='MapReduce · splits', title='Form splits with the 10% slop rule',
         problem='<p><code>FileInputFormat</code> keeps cutting full splits while the remaining bytes are more than 1.1 × the split size; whatever remains becomes the last split. Compute the splits for a 270 MB file and a 260 MB file with 128 MB split size.</p>',
         inp='270 MB and 260 MB · split 128 MB · slop 1.1',
         approach=['While remaining / split > 1.1: cut one full split.',
                   'Then the remainder (if any) is one split.',
                   'Compare with a naive ceil(size / 128).'],
         code='''def splits(size, split=128, slop=1.1):
    out, remaining = [], size
    while remaining / split > slop:
        out.append(split)
        remaining -= split
    if remaining:
        out.append(remaining)
    return out
for mb in [270, 260]:
    print(mb, "MB ->", splits(mb))
''', notes={3: 'Slop :: Avoid a tiny last split by allowing the last one to be up to 10% bigger.'},
         tryit='For 260 MB the last split is 132 MB, larger than a block: its map task reads part of a third block. This is real FileInputFormat behaviour.'),
]

QUIZ = mix([
    dict(q='What is the default HDFS block size in Hadoop 3?', options=['64 MB', '128 MB', '256 MB', '1 GB'], answer=1,
         why='dfs.blocksize defaults to 134,217,728 bytes. Hadoop 1 used 64 MB.'),
    dict(q='A 4.5 MB file is stored with a 128 MB block size. How much disk does each replica use?', options=['128 MB', 'About 4.5 MB (plus a small checksum file)', '64 MB', '384 MB'], answer=1,
         why='The real block file was 4,692,009 bytes. Blocks are not padded.'),
    dict(q='Where are blocks cut?', options=['At the end of a line', 'At an exact byte count, even in the middle of a record', 'Wherever the NameNode finds a comma', 'At file boundaries only'], answer=1,
         why='HDFS cuts by bytes. We saw “71484,poha,2” and “5” in two different blocks.'),
    dict(q='What is an input split?', options=['A physical copy of a block', 'A logical piece of input processed by one map task', 'A type of checksum', 'A DataNode folder'], answer=1,
         why='Splits are logical and usually match blocks; one map task per split.'),
    dict(q='Which split reads a record that crosses a block boundary?', options=['Both splits read half each', 'The split in which the record starts', 'The split in which it ends', 'Neither: it is skipped'], answer=1,
         why='The earlier split finishes the record; the next one skips the partial first line.'),
    dict(q='Who decides a file\'s block size?', options=['The NameNode, globally and forever', 'The client writing the file (dfs.blocksize, can be set per file)', 'Each DataNode', 'YARN'], answer=1,
         why='We wrote the same file with 128 MB and 1 MB blocks.'),
    dict(q='Why are HDFS blocks large?', options=['To fit in RAM', 'So disk transfer time dominates seek time, and NameNode metadata stays small', 'Because Java requires it', 'To encrypt data'], answer=1,
         why='Large blocks keep disks streaming and reduce the number of objects.'),
    dict(q='A 10 GB gzip file in HDFS gives how many input splits?', options=['80', '1, because gzip cannot be split', '10', '3'], answer=1,
         why='gzip is not splittable, so one map task must read the whole file.'),
])

REVISION = [
    'Block = <b>physical</b> unit of storage and replication; default <b>128 MB</b> (min 1 MB).',
    'Cut by <b>byte count</b>: records can be split across blocks.',
    'Last block stores only real data (4,692,009-byte file → 4,692,009-byte block file).',
    'Block size is per file, chosen by the writer: <code>-D dfs.blocksize=…</code>.',
    'Split = <b>logical</b> unit of work, one per map task, usually one per block.',
    'RecordReader: skip partial first line (except split 0); finish the record that starts in your split.',
    'Real proof: 5 splits read 70485 + 67321 + 65498 + 65574 + 31123 = 300001 records.',
    'Bigger blocks: less seek overhead, less NameNode memory, fewer tasks. Unsplittable formats (gzip) = 1 split.',
]
FAQ = [
    ('What is a block in HDFS?', 'The unit in which HDFS stores and replicates a file. Files are divided into blocks of dfs.blocksize bytes (128 MB by default); each block is stored on several DataNodes. Only the last block of a file may be smaller, and it uses only the space it needs.'),
    ('Why is the HDFS block size so large?', 'To make reading efficient on disks (the time to transfer a block is much larger than the time to seek to it) and to keep the number of blocks, and so the NameNode\'s memory and the number of tasks, small.'),
    ('What is the difference between a block and an input split?', 'A block is a physical division of a file for storage. An input split is a logical division of the input for processing by one map task. Splits usually match blocks, but the RecordReader makes sure records crossing block boundaries are read whole by exactly one split.'),
    ('Does a small file occupy a full 128 MB block?', 'No. A 1 MB file uses about 1 MB of disk per replica. It does, however, cost one file object and one block object in NameNode memory, which is why many small files are a problem.'),
    ('Can I change the block size of an existing file?', 'Not in place. Block size is fixed when the file is written; to change it, rewrite the file (for example copy it with -D dfs.blocksize=… or with distcp).'),
    ('How many map tasks will my job have?', 'By default one per input split, and splits follow blocks: a 1 GB file with 128 MB blocks gives 8 map tasks. Split size settings, the 10% slop rule, unsplittable compression and combined input formats can change this.'),
]

PRACTICE_INTRO = 'Block and split exercises, several using the exact numbers from the real cluster.'
PROBLEMS = [
    dict(level='easy', title='Blocks for a file', stmt='How many 128 MB blocks does a 1,000 MB file need, and how big is the last block?', inp='1000 MB · 128 MB',
         code='''import math
n = math.ceil(1000 / 128)
print(n, "blocks, last block", 1000 - (n - 1) * 128, "MB")
''', explain='8 blocks: 7 full ones and a last block of 104 MB.'),
    dict(level='easy', title='Check the real numbers', stmt='Verify that 4 blocks of 1,048,576 bytes plus 497,705 bytes equal the file size 4,692,009.', inp='4 × 1,048,576 + 497,705',
         code='print(4 * 1048576 + 497705 == 4692009)\n', explain='True: the fsck lengths add up to the file size exactly.'),
    dict(level='easy', title='Add up the counters', stmt='Add the five real Map input records counters and compare with the file\'s line count (300,001).', inp='70485 · 67321 · 65498 · 65574 · 31123',
         code='print(sum([70485, 67321, 65498, 65574, 31123]))\n', explain='300,001: every line read exactly once, despite five block boundaries.'),
    dict(level='medium', title='Where is byte N?', stmt='For 1 MB blocks, which block contains byte offsets 0, 1,048,575, 1,048,576 and 4,692,008, and at what offset inside the block?', inp='offsets 0 · 1048575 · 1048576 · 4692008',
         code='''B = 1048576
for off in [0, 1048575, 1048576, 4692008]:
    print(off, "-> block", off // B, "offset", off % B)
''', explain='Block = offset // block size, position = offset % block size. Byte 1,048,576 is the first byte of block 1, the “5” of order 71484.'),
    dict(level='medium', title='Splits for many files', stmt='A folder has 20 files of 200 MB and 1,000 files of 2 MB. How many map tasks with one split per block (128 MB)?', inp='20 × 200 MB · 1000 × 2 MB',
         code='''import math
print(20 * math.ceil(200 / 128) + 1000 * math.ceil(2 / 128))
''', explain='40 tasks for the big files and 1,000 for the tiny ones: 1,040 tasks, most of them doing almost nothing.'),
    dict(level='medium', title='Seek share', stmt='With 8 ms seek and 200 MB/s transfer, what block size keeps seeking under 1% of the time?', inp='8 ms · 200 MB/s · 1%',
         code='''seek, rate = 0.008, 200
mb = 1
while seek / (seek + mb / rate) > 0.01:
    mb *= 2
print("about", mb, "MB")
''', explain='About 256 MB (the first power of two that brings seeking under 1%); with 128 MB it is about 1.2%.'),
    dict(level='business', title='Mapper hours wasted', stmt='A nightly job reads 5,000 small files, one map task each. Each task has 3 s of start-up overhead. Merging them into 40 files of 128 MB reduces it to 40 tasks. How many task-hours of overhead are saved per month (30 runs)?', inp='5000 vs 40 tasks · 3 s · 30 runs',
         code='''saved_s = (5000 - 40) * 3 * 30
print(f"{saved_s / 3600:.0f} task-hours per month")
''', explain='About 124 task-hours a month of pure start-up overhead, before counting NameNode load.'),
    dict(level='advanced', title='Record reader for a boundary', stmt='Implement the two RecordReader rules for a list of split boundaries and return records per split for the given text.', inp='"aa\\nbbbb\\ncc\\ndddddd\\ne\\n" · splits at 0, 5, 12',
         code='''data = "aa\\nbbbb\\ncc\\ndddddd\\ne\\n"
bounds = [0, 5, 12, len(data)]
for i in range(len(bounds) - 1):
    start, end = bounds[i], bounds[i + 1]
    pos = start if start == 0 else data.index("\\n", start - 1) + 1
    recs = []
    while pos < end:
        nl = data.index("\\n", pos)
        recs.append(data[pos:nl]); pos = nl + 1
    print(f"split {i} [{start},{end}):", recs)
''', explain='Split 0 gets aa and bbbb (bbbb crosses byte 5), split 1 gets cc and dddddd, split 2 gets e. Each record appears once.'),
]

SCN_INTRO = 'Block and split questions appear in almost every Hadoop interview. Use exact numbers when you can.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · concepts</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“If a line is split across two blocks, is the record corrupted?”</h4>
      <p class="scn__situation">An interviewer draws a CSV row crossing a block boundary.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> block vs split, and the RecordReader.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>The block boundary is purely physical; the bytes are all stored, just in two blocks.</li>
          <li>The map task whose split contains the start of the line reads past its end (possibly from another DataNode) to finish it.</li>
          <li>The next split's reader skips everything up to the first newline. So each record is processed exactly once.</li>
          <li>Real example: order 71484 cut between “2” and “5”; the job still read all 300,001 lines.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Performance · tuning</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>“The job uses only 4 mappers for 1 TB”</h4>
      <p class="scn__situation">A job over 1 TB of logs starts only 4 map tasks and takes hours.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> what controls the number of splits.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>1 TB at 128 MB should give about 8,000 splits, so something prevents splitting.</li>
          <li>Most likely the input is 4 large gzip files (unsplittable). Check the file extensions and the job's “number of splits”.</li>
          <li>Fix: store data in a splittable format (bzip2, or Parquet/ORC with Snappy), or split files at ingestion. Also check any custom InputFormat and split min-size settings.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design · storage</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Choose a block size for a new 2 PB table</h4>
      <p class="scn__situation">A team will write a 2 PB fact table, scanned mostly in full each night.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> trade-offs, not a memorised number.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Large, fully scanned data favours bigger blocks, e.g. 256 MB: half the block objects, longer efficient reads.</li>
          <li>Check parallelism: 2 PB / 256 MB is still about 80 lakh blocks, plenty of tasks.</li>
          <li>Align file format units (Parquet row groups / ORC stripes) with the block size so a task's data sits in one block.</li>
          <li>Keep file sizes large too; block size does not help if writers produce small files.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Storage · basics</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“A 1 KB file wastes 128 MB, right?”</h4>
      <p class="scn__situation">A student claims small files waste disk because each takes a full block.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> what really costs with small files.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>No: a block file is only as big as its data (plus a tiny checksum file). The 4.5 MB file used 4.5 MB per replica, not 128 MB.</li>
          <li>The real cost is metadata: every file and block is an object in NameNode memory, and each small file usually becomes its own map task.</li>
          <li>So small files are a NameNode and scheduling problem, not a disk problem.</li>
        </ul>
      </div></details>
    </article>
'''
