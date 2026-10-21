import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)

META = dict(
    module='06-hdfs-operations', lesson='03-hdfs-shell-commands', n='6.3',
    module_label='Module 6 · HDFS operations',
    title='HDFS shell commands',
    desc='The everyday hdfs dfs commands with real Hadoop 3.5.0 outputs: mkdir, put, ls, cat, du, df, count, cp, mv, appendToFile, getmerge, chmod, test, find, stat, setrep and rm. Why mv of a 403 MB file takes 1.9 s but cp takes 5.6 s, why trash is off by default, what the two du columns mean, and the errors you will meet. Python shell simulator, quiz and interview scenarios.',
    og_desc='Linux file commands, with a twist: some only touch the NameNode, some move every byte. Real outputs from a real cluster.',
    minutes=26, level='Beginner',
    lead='You will use hdfs dfs every day. This lesson runs the important commands on a real cluster and shows their exact output, then explains what each one does behind the screen: which commands only change the NameNode\'s metadata and finish instantly, which ones read and write data through DataNodes, and which defaults (like trash being off) catch people out.',
    chips=['Real command outputs', 'cp vs mv timed', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='A tiny HDFS shell in Python',
    intro='<p>This program keeps a namespace in a dictionary (path → size and replication) and implements <code>ls</code>, <code>mv</code>, <code>du</code> and <code>rm</code>, counting which ones would touch DataNodes. Run it, then try the tasks.</p>',
    code='''ns = {"/user/hadoop/raw/mon.csv": (47, 3), "/user/hadoop/raw/tue.csv": (34, 3)}
datanode_bytes = 0

def ls(folder):
    for path, (size, rep) in sorted(ns.items()):
        if path.startswith(folder + "/"):
            print(f"-rw-r--r--  {rep} hadoop {size:>6} {path}")

def mv(src, dst):                 # metadata only: no bytes move
    ns[dst] = ns.pop(src)

def cp(src, dst):                 # reads and writes every byte
    global datanode_bytes
    size, rep = ns[src]
    datanode_bytes += size + size * rep
    ns[dst] = (size, rep)

def du(folder):
    files = [v for p, v in ns.items() if p.startswith(folder + "/")]
    print(sum(s for s, r in files), sum(s * r for s, r in files), folder)

cp("/user/hadoop/raw/mon.csv", "/user/hadoop/mon_backup.csv")
mv("/user/hadoop/mon_backup.csv", "/user/hadoop/archive_mon.csv")
ls("/user/hadoop/raw")
du("/user/hadoop")
print("bytes through DataNodes:", datanode_bytes)
''',
    anno=[
        ('def mv(src, dst):                 # metadata only: no bytes move', 'A rename only changes the key in the namespace. That is why -mv of 403 MB took 1.863 s, mostly Java start-up.'),
        ('datanode_bytes += size + size * rep', 'cp reads the file once and writes it again with 3 replicas: 47 + 141 bytes here.'),
        ('print(sum(s for s, r in files), sum(s * r for s, r in files), folder)', 'The two du columns: data size and raw space with replicas. Real output: 81 243 for the shell_lab folder before the copy.'),
    ],
    tasks=[
        dict(label='1 · Copy, move, list', hint='Press <b>Run</b>. The du line should say 128 384: three files (47 + 34 + 47).', code=None),
        dict(label='2 · The real du numbers', hint='<b>Predict first:</b> the lab printed <code>81  243</code> for two files of 47 and 34 bytes with replication 3. Check it.',
             code='''sizes = [47, 34]
print(sum(sizes), sum(sizes) * 3)
'''),
        dict(label='3 · setrep changes the second column', hint='After <code>-setrep 2</code> on archive_mon.csv (47 bytes), what does <code>du</code> show for the three files?',
             code='''files = {"mon.csv": (47, 3), "tue.csv": (34, 3), "archive_mon.csv": (47, 2)}
print(sum(s for s, r in files.values()), sum(s * r for s, r in files.values()))
'''),
        dict(label='4 · Trash path', hint='With trash on, <code>-rm</code> moves a file to <code>.Trash/Current</code> plus its full path. Build the trash path for any file.',
             code='''def trash_path(path, user="hadoop"):
    return f"/user/{user}/.Trash/Current{path}"

print(trash_path("/user/hadoop/shell_lab/archive_mon.csv"))
'''),
        dict(label='5 · Spot the error', hint='This mv crashes because the source does not exist, like <code>mv: `…\': No such file or directory</code>. Fix the path.',
             code='''ns = {"/user/hadoop/raw/mon.csv": 47}
ns["/user/hadoop/archive.csv"] = ns.pop("/user/hadoop/raw/monday.csv")
print(ns)
''', expect='error'),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: a shell workout',
    intro='<p>This script creates two small CSV files and runs 14 everyday commands on a practice folder, printing each command before its output. Save it as <code>shell_lab.sh</code> in the <code>hdfs-lab</code> folder, copy it into the namenode container and run it.</p>',
    items=[
        dict(title='Fourteen commands, one folder', file='shell_lab.sh',
             cmd=open(os.path.join(HERE, 'shell_lab.sh')).read() + '\n# In the hdfs-lab folder:\n#   docker cp shell_lab.sh lab5-namenode-1:/tmp/\n#   docker exec lab5-namenode-1 bash /tmp/shell_lab.sh',
             output=open('/home/claude/lab5/tx_shelllab.txt').read().strip() if os.path.exists('/home/claude/lab5/tx_shelllab.txt') else '',
             note='Real output from the lab cluster. Dates differ on your run. Note: CONTENT_SIZE 128 = 47 + 34 + 47, DIR_COUNT 2 counts shell_lab itself and raw, and the trash message proves the file can still be restored.'),
    ],
)

TRACE = dict(
    heading='Publishing results with one rename',
    intro='<p>Follow a job that writes part files into a temporary folder and publishes them with a single move: readers see either nothing or everything.</p>',
    code='''ns = {}
for i in range(3):
    ns[f"out/_tmp/part-0000{i}"] = 100 + i
visible = [p for p in ns if p.startswith("out/final/")]
print("before mv, visible:", visible)
ns = {p.replace("out/_tmp/", "out/final/"): s for p, s in ns.items()}
visible = [p for p in ns if p.startswith("out/final/")]
print("after mv, visible:", len(visible), "files")
''',
    notes={3: 'Write :: The job writes its part files under _tmp; nobody reads there.',
           6: 'Rename :: One -mv of the folder renames everything in a single NameNode operation.'},
)

WORKED_INTRO = 'Three shell questions with numbers: how much JVM start-up costs in a loop, how big a folder really is on disk, and how much setrep can free. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='Scripting · cost', title='Is a loop of hdfs dfs calls slow?',
         problem='<p>A script checks 600 files with one <code>hdfs dfs -test -e</code> each. Each call costs about 1.8 s of JVM start-up (measured in the lab). How long does the loop take, versus one <code>-ls -R</code> of the folder (one call) and checking the names in the output?</p>',
         inp='600 calls · 1.8 s each',
         approach=['Loop time = calls × start-up time.',
                   'One listing = one start-up.',
                   'Compare.'],
         code='''calls, startup = 600, 1.8
print(f"loop: {calls * startup / 60:.0f} minutes, one listing: {startup} s")
''', notes={2: 'JVM :: Most of each call is Java starting, not HDFS work.'},
         tryit='18 minutes vs about 2 seconds. For many small checks use one listing, the Java API or WebHDFS.'),
    dict(level='i', tag='Capacity · du', title='How much disk does the data folder really use?',
         problem='<p>The lab printed <code>948.6 M  2.8 G  /user/hadoop/data</code>. The files are 4.5 M, 4.5 M, 134.2 M, 402.7 M and 402.7 M with replication 3. Recompute both columns.</p>',
         inp='five files · replication 3',
         approach=['First column = sum of file sizes.',
                   'Second = sum × replication.',
                   'Convert MB to GB by dividing by 1024.'],
         code='''sizes = [4.5, 4.5, 134.2, 402.7, 402.7]
data = sum(sizes)
print(f"{data:.1f} M   {data * 3 / 1024:.1f} G")
''', notes={2: 'Logical :: What you think of as the folder size.'},
         tryit='Capacity planning uses the second column: 1 TB of data costs 3 TB of disk at replication 3.'),
    dict(level='a', tag='Cost · setrep', title='How much space does setrep 2 on old data free?',
         problem='<p>A cluster has 600 TB of data at replication 3. Data older than 90 days is 70% of it and rarely read. If we <code>-setrep 2</code> the old data, how much raw disk is freed, and what is the risk?</p>',
         inp='600 TB · 70% old · 3 → 2',
         approach=['Raw before = 600 × 3.',
                   'Raw after = old × 2 + new × 3.',
                   'Difference is the saving; risk: only one spare copy.'],
         code='''data, old_share = 600, 0.70
before = data * 3
after = data * old_share * 2 + data * (1 - old_share) * 3
print(f"raw before {before:.0f} TB, after {after:.0f} TB, freed {before - after:.0f} TB")
''', notes={3: 'Mix :: Only the old part changes replication.'},
         tryit='420 TB freed. Erasure coding (Lesson 7.3) gets similar savings with better durability.'),
]

QUIZ = mix([
    dict(q='Which command creates a folder and any missing parents?', options=['hdfs dfs -mkdir', 'hdfs dfs -mkdir -p', 'hdfs dfs -touchz', 'hdfs dfs -put -p'], answer=1,
         why='Without -p, a missing parent or an existing folder causes an error.'),
    dict(q='Why did -mv of a 403 MB file take about the same time as -rm?', options=['Both are cached', 'Both only change NameNode metadata; the time is mostly JVM start-up', 'mv deletes the file first', 'The file was small'], answer=1,
         why='Real: mv 1.863 s, rm 1.830 s, cp 5.615 s.'),
    dict(q='hdfs dfs -du -s -h printed "81  243". What is 243?', options=['Block count', 'Space used including 3 replicas', 'Free space', 'Number of files'], answer=1,
         why='81 bytes of data × 3 replicas.'),
    dict(q='What is the default value of fs.trash.interval?', options=['1440', '60', '0 (trash off)', '360'], answer=2,
         why='hdfs getconf -confKey fs.trash.interval printed 0 on the lab.'),
    dict(q='Where does a file go when deleted with trash enabled?', options=['/tmp', '/user/<name>/.Trash/Current/<full path>', 'It is deleted at once', 'The NameNode backup'], answer=1,
         why='Real: Moved … to trash at: …/.Trash/Current/user/hadoop/shell_lab/archive_mon.csv'),
    dict(q='What does -getmerge do?', options=['Merges two HDFS folders', 'Concatenates the files of an HDFS folder into one local file', 'Joins CSVs by key', 'Merges small blocks'], answer=1,
         why='It just concatenates bytes, so headers repeat.'),
    dict(q='How does a script know whether a path exists?', options=['Parse -ls output only', 'Use hdfs dfs -test -e and check the exit code', 'Use -cat', 'It cannot'], answer=1,
         why='Real: exists: 0 for day1.csv, exists: 1 for day9.csv.'),
    dict(q='For copying 5 TB between folders, the better tool is:', options=['hdfs dfs -cp', 'hadoop distcp', 'hdfs dfs -getmerge', 'hdfs dfs -mv'], answer=1,
         why='-cp streams everything through one client; distcp runs a parallel job.'),
])

REVISION = [
    'Syntax: <code>hdfs dfs [-D prop=value] -command [options] paths</code>; relative paths start at <code>/user/&lt;name&gt;</code>.',
    'Metadata only (instant): <code>-ls -mkdir -mv -rm -chmod -count -du -stat -test</code>.',
    'Data commands (time ∝ size): <code>-put -get -cat -cp -getmerge -appendToFile</code>.',
    'Lab: <code>cp</code> 5.615 s vs <code>mv</code> 1.863 s vs <code>rm</code> 1.830 s on 403 MB.',
    '<code>-du</code>: data size, raw size with replicas (81 / 243).',
    'Trash is <b>off</b> by default (<code>fs.trash.interval=0</code>); with it on, files go to <code>.Trash/Current</code>.',
    'Errors: <code>File exists</code> (use <code>-p</code> / <code>-f</code>), <code>No such file or directory</code>.',
    'Scripts: use <code>-test</code> exit codes; quote globs; avoid thousands of separate calls.',
]
FAQ = [
    ('What is the difference between hadoop fs and hdfs dfs?', 'They run the same FsShell. hadoop fs works with any file system Hadoop supports (HDFS, local, S3, ADLS…), and hdfs dfs is the conventional name when working with HDFS. hadoop dfs is an old deprecated form.'),
    ('How do I copy a file from local disk to HDFS?', 'hdfs dfs -put localfile /hdfs/path/ (or -copyFromLocal). Use -f to overwrite an existing file. To move instead of copy, -moveFromLocal deletes the local file after upload.'),
    ('Why is hdfs dfs -mv so fast?', 'A move or rename within HDFS only changes the path in the NameNode namespace; no block data is copied. Its time is dominated by the client JVM start-up, so it is the same for a tiny or a huge file.'),
    ('How do I recover a deleted file?', 'Only if trash was enabled (fs.trash.interval &gt; 0) and the file was not deleted with -skipTrash: move it back from /user/&lt;name&gt;/.Trash/Current/&lt;original path&gt;. Otherwise restore from a snapshot or backup if one exists.'),
    ('What do the columns of hdfs dfs -du mean?', 'First: the size of the data. Second: the disk space consumed including all replicas. Then the path. With -s you get one total line for the folder, and -h prints human-readable units.'),
    ('How do I change the replication factor of existing files?', 'hdfs dfs -setrep N path (folders apply to all files inside). The NameNode updates the metadata immediately and schedules extra copies or deletions; -w waits until the actual replica count matches.'),
]

PRACTICE_INTRO = 'Shell exercises using the real outputs from the lab.'
PROBLEMS = [
    dict(level='easy', title='Parse an ls line', stmt='From a real <code>-ls</code> line, extract permissions, replication, size and file name.', inp='-rw-r--r--   3 hadoop supergroup         47 2026-10-21 09:54 /user/hadoop/shell_lab/raw/mon.csv',
         code='''line = "-rw-r--r--   3 hadoop supergroup         47 2026-10-21 09:54 /user/hadoop/shell_lab/raw/mon.csv"
f = line.split()
print(f[0], int(f[1]), int(f[4]), f[7].rsplit("/", 1)[1])
''', explain='-rw-r--r--, replication 3, 47 bytes, mon.csv. Split on whitespace; field 1 is replication (or - for folders).'),
    dict(level='easy', title='Count lines after getmerge', stmt='mon.csv has 3 lines, tue.csv has 2. How many lines does getmerge produce, and how many are headers?', inp='3 + 2 lines',
         code='''files = {"mon.csv": 3, "tue.csv": 2}
print("lines:", sum(files.values()), " headers:", len(files))
''', explain='5 lines (the real wc -l printed 5 week.csv), of which 2 are header lines.'),
    dict(level='easy', title='Octal permissions', stmt='Convert chmod 640 into the rwx string that -ls shows.', inp='640',
         code='''def rwx(mode):
    return "".join(("r" if d & 4 else "-") + ("w" if d & 2 else "-") + ("x" if d & 1 else "-") for d in map(int, mode))
print("-" + rwx("640"))
''', explain='-rw-r-----, exactly what the real -ls showed after hdfs dfs -chmod 640 day1.csv.'),
    dict(level='medium', title='Remove repeated headers', stmt='After getmerge, keep only the first header line.', inp='merged lines with header repeated',
         code='''merged = ["order_id,item,amount", "4001,idli,30", "4002,chai,15", "order_id,item,amount", "4003,dosa,45"]
clean = merged[:1] + [l for l in merged[1:] if l != merged[0]]
print("\\n".join(clean))
''', explain='4 lines remain: one header and three orders. Do this before handing a file to Excel.'),
    dict(level='medium', title='Check count -v', stmt='The real <code>-count -v</code> printed 2 dirs, 3 files, 128 bytes for shell_lab. Rebuild those numbers from the paths.', inp='shell_lab, raw, 3 files (47, 34, 47)',
         code='''paths = {"shell_lab/": None, "shell_lab/raw/": None, "shell_lab/raw/mon.csv": 47,
         "shell_lab/raw/tue.csv": 34, "shell_lab/archive_mon.csv": 47}
dirs = sum(v is None for v in paths.values())
files = [v for v in paths.values() if v is not None]
print(dirs, len(files), sum(files))
''', explain='2 3 128: the folder itself counts as a directory.'),
    dict(level='medium', title='Time a cleanup script', stmt='A cleanup script runs 120 separate <code>hdfs dfs -rm</code> calls at 1.83 s each. Rewritten as one call with 120 paths, it takes about 3 s. How much time is saved per run and per month (one run a day)?', inp='120 × 1.83 s vs 3 s · 30 runs',
         code='''loop, single = 120 * 1.83, 3
print(f"per run {loop - single:.0f} s saved, per month {(loop - single) * 30 / 3600:.1f} hours")
''', explain='About 217 s per run and 1.8 hours a month: -rm accepts many paths (and globs) in one call.'),
    dict(level='business', title='Cost of no trash', stmt='A team deletes data by mistake about 4 times a year. Without trash, each restore from backup takes 2 engineers × 6 hours at Rs 1,500/hour. With trash (1 day), each takes 15 minutes of one engineer. What does enabling trash save per year?', inp='4 incidents · Rs 1,500/hour',
         code='''rate = 1500
without = 4 * 2 * 6 * rate
with_trash = 4 * 0.25 * rate
print(f"Rs {without - with_trash:,.0f} per year")
''', explain='Rs 70,500 per year (illustrative), and some deletions cannot be restored at all without trash or snapshots.'),
    dict(level='advanced', title='Mini FsShell', stmt='Implement <code>mkdir -p</code>, <code>put</code> (fail if the file exists unless <code>-f</code>), and <code>rm</code> with optional trash on a dictionary namespace. Print the messages like the real shell.', inp='commands list',
         code='''ns, trash_on = {"/user/hadoop": "dir"}, True

def mkdir_p(p):
    parts = p.strip("/").split("/")
    for i in range(1, len(parts) + 1):
        ns.setdefault("/" + "/".join(parts[:i]), "dir")

def put(p, size, force=False):
    if p in ns and not force:
        print(f"put: `{p}': File exists"); return
    ns[p] = size

def rm(p):
    if trash_on:
        t = "/user/hadoop/.Trash/Current" + p
        ns[t] = ns.pop(p); print(f"Moved: '{p}' to trash at: {t}")
    else:
        del ns[p]; print("Deleted", p)

mkdir_p("/user/hadoop/lab/raw"); put("/user/hadoop/lab/raw/a.csv", 47)
put("/user/hadoop/lab/raw/a.csv", 50); put("/user/hadoop/lab/raw/a.csv", 50, force=True)
rm("/user/hadoop/lab/raw/a.csv")
print(sorted(p for p in ns if ns[p] != "dir"))
''', explain='The second put prints File exists, the -f put overwrites, and rm moves the file to .Trash/Current with its full path, which is all that is left as a file.'),
]

SCN_INTRO = 'Shell questions check practical habits: safe deletes, fast scripts and knowing what each command really costs.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · basics</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Name ten HDFS commands you use”</h4>
      <p class="scn__situation">The most common first question on HDFS.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> real usage, not a memorised list.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Group them: list/size (<code>-ls</code>, <code>-du -s -h</code>, <code>-count</code>), transfer (<code>-put</code>, <code>-get</code>, <code>-getmerge</code>), read (<code>-cat</code>, <code>-tail</code>), change (<code>-mkdir -p</code>, <code>-mv</code>, <code>-cp</code>, <code>-rm -r</code>), attributes (<code>-chmod</code>, <code>-setrep</code>).</li>
          <li>Add one detail that shows experience: du's second column includes replicas; mv is metadata-only; trash is off by default.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Operations · safety</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>Someone ran hdfs dfs -rm -r on a production folder</h4>
      <p class="scn__situation">A colleague deleted yesterday's processed data by mistake and asks you to bring it back.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> trash, snapshots and prevention.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Check <code>.Trash/Current</code> of the user who ran it; if it is there, <code>-mv</code> it back.</li>
          <li>If trash was off or <code>-skipTrash</code> was used, restore from a snapshot (<code>.snapshot</code>) or reprocess from raw data.</li>
          <li>Prevent: enable <code>fs.trash.interval</code>, snapshot important folders, restrict write permissions on production paths.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Scripting · performance</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A housekeeping script takes 40 minutes</h4>
      <p class="scn__situation">It loops over 1,300 paths, calling hdfs dfs -test and -rm for each.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> JVM start-up cost.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Each call starts a JVM (about 1.8 s): 1,300 × 2 calls ≈ 40 minutes, almost all start-up.</li>
          <li>List once (<code>-ls -R</code> or <code>-find</code>), decide in the script, then pass many paths or a glob to one <code>-rm</code>.</li>
          <li>For complex logic, use the Java API or Python with WebHDFS in a single process.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Pipelines · correctness</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>Reports sometimes read half-written output</h4>
      <p class="scn__situation">A dashboard reads a folder while the nightly job is still writing to it.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> atomic rename.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Write to a temporary folder first, then publish with one <code>-mv</code>; a rename is atomic in the NameNode.</li>
          <li>Also have readers wait for a <code>_SUCCESS</code> marker (<code>-test -e</code>).</li>
        </ul>
      </div></details>
    </article>
'''
