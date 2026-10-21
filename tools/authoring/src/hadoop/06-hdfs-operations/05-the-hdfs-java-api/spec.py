import os
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = body(HERE)
rd = lambda f: open(os.path.join(HERE, f)).read()

META = dict(
    module='06-hdfs-operations', lesson='05-the-hdfs-java-api', n='6.5',
    module_label='Module 6 · HDFS operations',
    title='The HDFS Java API',
    desc='Use HDFS from your own Java code with the Hadoop FileSystem API: Configuration, FileSystem.get, create, open, getFileStatus, getFileBlockLocations, listStatus, rename and delete, with real output from two programs on a Hadoop 3.5.0 cluster. Counting 300,000 orders in 1.3 s, 403 MB in 5.9 s through one client, a data bug the API won\'t catch, and the same file over WebHDFS with its 307 redirect to a DataNode. Python model of the API, quiz and interview scenarios.',
    og_desc='Every hdfs dfs command is a small Java program. Write your own with the FileSystem API, with real outputs.',
    minutes=26, level='Intermediate',
    lead='The shell is great for people; programs need an API. This lesson writes and runs two Java programs against the lab cluster with the Hadoop FileSystem API: one that writes, reads, inspects, renames and deletes a file, and one that counts items in a big file. Then the same file is read over plain HTTP with WebHDFS. Every output is real.',
    chips=['Real Java programs', 'WebHDFS with curl', 'Runs in your browser (Python)'],
)

RUN = dict(
    heading='The FileSystem API, modelled in Python',
    intro='<p>The Java API can\'t run in your browser, so this Python class copies its shape: <code>create</code>, <code>open</code>, <code>get_file_status</code>, <code>get_file_block_locations</code>, <code>rename</code> and <code>delete</code>, with a NameNode namespace and 128 MB blocks placed on DataNodes. Run it, then try the tasks.</p>',
    code='''BLOCK = 128 * 1024 * 1024

class FileSystem:
    def __init__(self, datanodes):
        self.ns = {}                       # path -> (length, replication, blocks)
        self.dns = datanodes
        self.next_dn = 0

    def create(self, path, data_len, replication=3):
        blocks = []
        for off in range(0, data_len, BLOCK):
            hosts = [self.dns[(self.next_dn + i) % len(self.dns)] for i in range(replication)]
            self.next_dn += 1
            blocks.append((off, min(BLOCK, data_len - off), hosts))
        self.ns[path] = (data_len, replication, blocks)

    def get_file_status(self, path):
        length, rep, blocks = self.ns[path]
        return {"path": path, "len": length, "replication": rep, "blocksize": BLOCK}

    def get_file_block_locations(self, path):
        return self.ns[path][2]

    def rename(self, src, dst):            # returns False instead of raising, like Java
        if src not in self.ns or dst in self.ns:
            return False
        self.ns[dst] = self.ns.pop(src)
        return True

    def delete(self, path):
        return self.ns.pop(path, None) is not None

fs = FileSystem(["datanode-1", "datanode-2", "datanode-3"])
fs.create("/user/hadoop/data/orders_x30.csv", 140_760_270)
print(fs.get_file_status("/user/hadoop/data/orders_x30.csv"))
for off, length, hosts in fs.get_file_block_locations("/user/hadoop/data/orders_x30.csv"):
    print(f"  block at offset {off:,} length {length:,} on {', '.join(hosts)}")
print("rename:", fs.rename("/user/hadoop/data/orders_x30.csv", "/user/hadoop/data/old.csv"))
print("rename again:", fs.rename("/user/hadoop/data/orders_x30.csv", "/user/hadoop/data/old.csv"))
''',
    anno=[
        ('        for off in range(0, data_len, BLOCK):', 'The file is cut into 128 MB blocks; the last one is shorter. The real file gave 134,217,728 + 6,542,542 bytes.'),
        ('    def rename(self, src, dst):            # returns False instead of raising, like Java', 'Java\'s fs.rename() also returns a boolean. The real program printed rename: true. Code that ignores a false silently loses track of files.'),
        ('    def get_file_block_locations(self, path):', 'Only metadata: the NameNode knows the hosts of every block. Schedulers use this to run tasks next to the data.'),
    ],
    tasks=[
        dict(label='1 · Status, blocks, rename', hint='Press <b>Run</b>. Why does the second rename print <code>False</code>?', code=None),
        dict(label='2 · Blocks of other files', hint='<b>Predict first:</b> how many blocks does orders_x90.csv (422,280,810 bytes, shown as 402.7 M by -du -h) have, and how long is the last one?',
             code='''BLOCK = 128 * 1024 * 1024
size = 422_280_810
full, last = divmod(size, BLOCK)
print("blocks:", full + (1 if last else 0), " last block:", f"{last:,}" if last else "full")
'''),
        dict(label='3 · Seek into the middle', hint='An input stream can <code>seek()</code>. Which block and offset inside it does byte 300,000,000 fall in?',
             code='''BLOCK = 128 * 1024 * 1024
pos = 300_000_000
print("block", pos // BLOCK, "offset inside it", f"{pos % BLOCK:,}")
'''),
        dict(label='4 · Count items like ItemCount', hint='The same logic as ItemCount.java on a few lines. Then add a check that skips repeated header lines.',
             code='''lines = ["order_id,item,amount", "1,chai,15", "2,dosa,45", "order_id,item,amount", "3,chai,15"]
counts = {}
for line in lines[1:]:
    item = line.split(",")[1]
    counts[item] = counts.get(item, 0) + 1
print(counts)
'''),
        dict(label='5 · Spot the error', hint='This reads the status of a file that was already renamed. In Java this is a <code>FileNotFoundException</code>. Use the new name.',
             code='''ns = {"/data/old.csv": 140760270}
print(ns["/data/orders_x30.csv"])
''', expect='error'),
    ],
)
RUN['tasks'][0]['code'] = RUN['code']

PCRUN = dict(
    heading='Run it on your PC: Java against HDFS',
    intro='<p>Save these files in the <code>hdfs-lab</code> folder. The namenode container already has Java and the Hadoop jars, so we copy the files in, compile there with <code>javac -cp $(hadoop classpath)</code>, package a jar and run it with <code>hadoop jar</code>. The exact commands are at the end of the first file.</p>',
    items=[
        dict(title='Write, read, inspect, rename, delete', file='HdfsBasics.java',
             cmd=rd('HdfsBasics.java') + '\n// In the hdfs-lab folder:\n//   docker cp HdfsBasics.java lab5-namenode-1:/tmp/\n//   docker cp ItemCount.java lab5-namenode-1:/tmp/\n//   docker exec -it lab5-namenode-1 bash\n// Then inside the container:\n//   cd /tmp\n//   javac -cp $(hadoop classpath) HdfsBasics.java ItemCount.java\n//   jar cf hdfs-demo.jar *.class\n//   hadoop jar hdfs-demo.jar HdfsBasics',
             output='''Connected to: hdfs://namenode
  read: order_id,item,amount
  read: 3001,samosa,18
  read: 3002,chai,15
orders.csv  49 bytes  replication 3  block size 128 MB  owner hadoop
  block at offset 0 length 134,217,728 on ab3b1bedf98a, 46201bb62e68, 264eb9c0f8e2
  block at offset 134,217,728 length 6,542,542 on ab3b1bedf98a, 46201bb62e68, 264eb9c0f8e2
  ls: hdfs://namenode/user/hadoop/api_demo/orders.csv
rename: true
exists after rename: false
delete: true''',
             note='Real output. The hosts are the container IDs of datanode-1, -2 and -3 (yours will differ). orders_x30.csv is canteen_orders.csv repeated 30 times; if you don\'t have it: for i in $(seq 30); do cat canteen_orders.csv; done | hdfs dfs -put - /user/hadoop/data/orders_x30.csv'),
        dict(title='Count orders per item, streaming one file', file='ItemCount.java',
             cmd=rd('ItemCount.java') + '\n// Inside the namenode container, in /tmp:\n//   hadoop jar hdfs-demo.jar ItemCount /user/hadoop/data/canteen_orders.csv\n//   hadoop jar hdfs-demo.jar ItemCount /user/hadoop/data/orders_x90.csv',
             output='''chai      50,170
dosa      49,948
idli      49,984
poha      49,891
samosa    50,021
vada pav  49,986
took 1327 ms in one JVM

chai      4,515,300
dosa      4,495,320
idli      4,498,560
item      89
poha      4,490,190
samosa    4,501,890
vada pav  4,498,740
took 5890 ms in one JVM''',
             note='Real output for the 4.5 MB and the 403 MB file. “item 89” comes from header lines inside the concatenated file: a data bug, not an HDFS one.'),
        dict(title='The same file over HTTP (WebHDFS)', file='webhdfs.sh',
             cmd=rd('webhdfs.sh') + '\n# In the hdfs-lab folder:\n#   docker cp webhdfs.sh lab5-namenode-1:/tmp/\n#   docker exec lab5-namenode-1 bash /tmp/webhdfs.sh',
             output=rd('webhdfs_output.txt').strip(),
             note='Real output. The NameNode answers GETFILESTATUS itself and redirects OPEN (HTTP 307) to a DataNode on port 9864.'),
    ],
)

TRACE = dict(
    heading='Reading a file block by block, as open() does',
    intro='<p>A simplified reader: ask for block locations once, then read each block from its first (nearest) host until the file\'s length is reached.</p>',
    code='''locations = [(0, 100, ["dn-1", "dn-2"]), (100, 100, ["dn-3", "dn-1"]), (200, 40, ["dn-2", "dn-3"])]
pos, served = 0, []
for off, length, hosts in locations:
    served.append((hosts[0], off, off + length))
    pos = off + length
print("read", pos, "bytes:", served)
''',
    notes={1: 'Locations :: One getBlockLocations call returns offsets, lengths and hosts.',
           4: 'Per block :: The stream switches DataNodes at block boundaries; your code just keeps reading.'},
)

WORKED_INTRO = 'Three API questions with numbers: what one JVM saves over shell calls, how fast one client can scan, and how many readers you need. Each runs live and is traced in memory.'
EXAMPLES = [
    dict(level='b', tag='API · JVM start-up', title='API instead of shell calls',
         problem='<p>A backend saves 2,000 small order batches a day. Through <code>hdfs dfs -put</code> each call costs about 1.8 s of JVM start-up; through the API in a running service, about 0.02 s each. How much time is saved per day?</p>',
         inp='2,000 calls · 1.8 s vs 0.02 s',
         approach=['Shell total = calls × 1.8 s.',
                   'API total = calls × 0.02 s.',
                   'Difference in minutes.'],
         code='''calls = 2000
shell, api = calls * 1.8, calls * 0.02
print(f"shell {shell / 60:.0f} min, API {api:.0f} s, saved {(shell - api) / 60:.0f} min per day")
''', notes={2: 'Per call :: The JVM starts once in a service; each API call is just RPCs.'},
         tryit='60 minutes vs 40 seconds. For one-off admin work the shell is fine; for applications use the API.'),
    dict(level='i', tag='Throughput · one client', title='How long does one reader take?',
         problem='<p>ItemCount read 403 MB in 5.89 s. At that speed, how long would one client take for 1 TB, and for 4 TB?</p>',
         inp='402.7 MB in 5.89 s',
         approach=['Speed = MB ÷ seconds.',
                   'Time = size ÷ speed.',
                   'Convert to hours.'],
         code='''speed = 402.7 / 5.89                     # MB/s
for tb in [1, 4]:
    hours = tb * 1024 * 1024 / speed / 3600
    print(f"{tb} TB: {hours:.1f} hours at {speed:.0f} MB/s")
''', notes={1: 'Measured :: Real lab number, one JVM, one stream.'},
         tryit='About 4.3 and 17 hours. One client is limited by one network link and one CPU; that is the problem MapReduce solves.'),
    dict(level='a', tag='Parallelism · blocks', title='How many parallel readers for a 1-hour target?',
         problem='<p>A 4 TB file has 128 MB blocks. If each reader handles whole blocks at 68 MB/s, how many parallel readers are needed to finish within one hour, and how many blocks does each read?</p>',
         inp='4 TB · 128 MB blocks · 68 MB/s · 1 hour',
         approach=['Blocks = size ÷ 128 MB.',
                   'One reader reads 68 × 3600 MB per hour.',
                   'Readers = ceil(size ÷ per-reader capacity); blocks each = blocks ÷ readers.'],
         code='''import math
size_mb = 4 * 1024 * 1024
blocks = size_mb // 128
per_reader = 68 * 3600
readers = math.ceil(size_mb / per_reader)
print(f"{blocks:,} blocks, {readers} readers, about {math.ceil(blocks / readers)} blocks each")
''', notes={4: 'Capacity :: What one reader can do in an hour.'},
         tryit='32,768 blocks, 18 readers. Using getFileBlockLocations, each reader can run on a node that holds its blocks: that is a MapReduce map task.'),
]

QUIZ = mix([
    dict(q='Which call gives you a FileSystem object for the cluster in the configuration?', options=['new FileSystem()', 'FileSystem.get(conf)', 'Path.open()', 'HDFS.connect()'], answer=1,
         why='The scheme of fs.defaultFS (hdfs://) selects DistributedFileSystem. Real: Connected to: hdfs://namenode.'),
    dict(q='What does fs.open(path) return?', options=['A String with the file contents', 'An FSDataInputStream that can seek', 'A list of blocks', 'A FileStatus'], answer=1,
         why='You read it like any Java stream; it fetches block locations and reads from DataNodes.'),
    dict(q='What does fs.rename(src, dst) return if it fails because the destination folder does not exist?', options=['It throws an exception always', 'false', 'null', 'It creates the folder'], answer=1,
         why='Many rename failures just return false: always check the result.'),
    dict(q='Does fs.delete(path, true) move files to the trash?', options=['Yes, always', 'No, it deletes permanently', 'Only for folders', 'Only if replication is 3'], answer=1,
         why='Trash is a shell feature (or use the Trash class explicitly).'),
    dict(q='Which method tells a scheduler where to run tasks near the data?', options=['getFileStatus', 'getFileBlockLocations', 'listStatus', 'getUri'], answer=1,
         why='Real output listed the hosts of both blocks of orders_x30.csv.'),
    dict(q='Why is closing the FileSystem from FileSystem.get() dangerous in a server?', options=['It deletes files', 'The instance is cached and shared, so other code gets “Filesystem closed”', 'It stops the NameNode', 'It is not dangerous'], answer=1,
         why='Use FileSystem.newInstance() if you need your own instance to close.'),
    dict(q='In WebHDFS, what does the NameNode reply to op=OPEN?', options=['The file bytes', 'HTTP 307 redirect to a DataNode', 'HTTP 404', 'A list of blocks in JSON'], answer=1,
         why='Real: HTTP/1.1 307 Temporary Redirect, Location: http://46201bb62e68:9864/...'),
    dict(q='ItemCount printed “item 89” for orders_x90.csv. What is the cause?', options=['HDFS corrupted the file', 'The file contains 89 extra header lines from concatenation', 'A block was missing', 'A Java bug in BufferedReader'], answer=1,
         why='HDFS stores bytes as written; data quality is the program\'s job.'),
])

REVISION = [
    '<code>Configuration</code> → <code>FileSystem.get(conf)</code> → <code>DistributedFileSystem</code> for <code>hdfs://</code>.',
    'Write: <code>create(path, overwrite)</code> → <code>write</code> → <code>close</code> (or <code>hflush</code> to make data visible).',
    'Read: <code>open(path)</code> → seekable stream; reads from DataNodes.',
    'Metadata: <code>getFileStatus</code>, <code>listStatus</code>, <code>listFiles(dir, true)</code>, <code>getFileBlockLocations</code>.',
    '<code>rename</code> and <code>delete</code> return booleans; <code>delete</code> skips the trash.',
    'Lab: 300,000 orders in 1.3 s; 403 MB in 5.9 s (≈68 MB/s) through one client.',
    'WebHDFS: REST on port 9870, OPEN redirects (307) to a DataNode on 9864.',
    'Run with <code>javac -cp $(hadoop classpath)</code> and <code>hadoop jar app.jar Class</code>.',
]
FAQ = [
    ('How do you read a file from HDFS in Java?', 'Create a Configuration, get a FileSystem with FileSystem.get(conf), call fs.open(new Path("/path")) to get an FSDataInputStream, wrap it in a BufferedReader (or copy it with IOUtils.copyBytes), and close the stream. The client gets block locations from the NameNode and reads the bytes directly from DataNodes.'),
    ('How do you write a file to HDFS in Java?', 'Call fs.create(path, overwrite) to get an FSDataOutputStream, write bytes, and close it. Closing completes the file on the NameNode. Use hflush() to make written data visible to readers before closing, and hsync() to also force it to disk on the DataNodes.'),
    ('What is the difference between FileSystem.get() and FileSystem.newInstance()?', 'get() returns a cached instance shared across the JVM for the same scheme, authority and user; closing it affects every user of that instance. newInstance() always returns a new instance that you own and may close.'),
    ('What is WebHDFS?', 'A REST API for HDFS served by the NameNode (port 9870 in Hadoop 3) and DataNodes (port 9864). Metadata operations are answered by the NameNode; for reading and writing data it redirects the client to a DataNode. It lets any language use HDFS over HTTP.'),
    ('How does Spark know where HDFS blocks are?', 'Through the same FileSystem API: getFileBlockLocations (or listFiles with locations) returns the hosts of each block, and the scheduler prefers to run a task on one of those hosts.'),
    ('Can the same Java code access S3?', 'Yes, if the S3A connector is on the classpath and configured: FileSystem.get(URI.create("s3a://bucket/"), conf) returns an S3AFileSystem with the same methods. Some semantics differ (for example rename is a copy on object stores, not an atomic metadata change).'),
]

PRACTICE_INTRO = 'API exercises using the real outputs from the lab programs.'
PROBLEMS = [
    dict(level='easy', title='Bytes in the demo file', stmt='HdfsBasics wrote the header and two order lines (with newline characters). Confirm the 49 bytes it reported.', inp='"order_id,item,amount\\n3001,samosa,18\\n3002,chai,15\\n"',
         code='''data = "order_id,item,amount\\n" + "3001,samosa,18\\n3002,chai,15\\n"
print(len(data.encode("utf-8")), "bytes")
''', explain='49 bytes: 21 + 15 + 13, exactly the length getFileStatus reported.'),
    dict(level='easy', title='Check the total', stmt='Add the six ItemCount results for canteen_orders.csv.', inp='50,170 · 49,948 · 49,984 · 49,891 · 50,021 · 49,986',
         code='''print(sum([50170, 49948, 49984, 49891, 50021, 49986]))
''', explain='300,000 orders: every data line counted once, the header skipped.'),
    dict(level='easy', title='Block lengths', stmt='orders_x30.csv is 140,760,270 bytes. Compute its block lengths with 128 MB blocks.', inp='140,760,270 bytes',
         code='''size, block = 140_760_270, 128 * 1024 * 1024
print([min(block, size - off) for off in range(0, size, block)])
''', explain='[134217728, 6542542]: the two BlockLocations printed by the real program.'),
    dict(level='medium', title='Ratio for x90', stmt='orders_x90.csv is the 300,000-order file 90 times. Check that each item\'s count is exactly 90× and explain “item 89”.', inp='x1 and x90 counts',
         code='''x1 = {"chai": 50170, "dosa": 49948, "idli": 49984, "poha": 49891, "samosa": 50021, "vada pav": 49986}
x90 = {"chai": 4515300, "dosa": 4495320, "idli": 4498560, "poha": 4490190, "samosa": 4501890, "vada pav": 4498740}
print(all(x90[k] == 90 * x1[k] for k in x1), "header lines inside:", 90 - 1)
''', explain='True: every count is exactly 90×. The first header was skipped, the other 89 copies were counted as an item called “item”.'),
    dict(level='medium', title='Parse WebHDFS JSON', stmt='From the real GETFILESTATUS reply, print length, replication, permission and block size in MB.', inp='{"FileStatus":{…}}',
         code='''import json
reply = '{"FileStatus":{"accessTime":1792579946689,"blockSize":134217728,"childrenNum":0,"fileId":16425,"group":"supergroup","length":47,"modificationTime":1792575484677,"owner":"hadoop","pathSuffix":"","permission":"640","replication":3,"storagePolicy":0,"type":"FILE"}}'
st = json.loads(reply)["FileStatus"]
print(st["length"], st["replication"], st["permission"], st["blockSize"] // 2**20, "MB")
''', explain='47 bytes, replication 3, permission 640 (set with chmod in Lesson 6.3), 128 MB blocks.'),
    dict(level='medium', title='Where does the redirect go?', stmt='Extract host, port, offset and NameNode address from the real 307 Location header.', inp='Location: http://46201bb62e68:9864/…',
         code='''from urllib.parse import urlparse, parse_qs
loc = "http://46201bb62e68:9864/webhdfs/v1/user/hadoop/canteen/raw/day1.csv?op=OPEN&user.name=hadoop&namenoderpcaddress=namenode:8020&offset=0"
u = urlparse(loc); q = parse_qs(u.query)
print(u.hostname, u.port, q["offset"][0], q["namenoderpcaddress"][0])
''', explain='DataNode 46201bb62e68 (datanode-2) on port 9864, offset 0, and the NameNode RPC address the DataNode should use.'),
    dict(level='business', title='Service vs shell for an app', stmt='An app team pays Rs 12 per vCPU-hour. Their shell-based uploader uses 1 vCPU fully for 60 minutes a day (mostly JVM start-ups); an API-based version needs 2 minutes. What is the yearly saving, and what else improves?', inp='60 vs 2 min/day · Rs 12/vCPU-hour',
         code='''rate = 12
saved_hours = (60 - 2) / 60 * 365
print(f"Rs {saved_hours * rate:,.0f} per year")
''', explain='About Rs 4,234 a year in compute (illustrative), but the bigger wins are proper exceptions instead of parsing text, and uploads that finish in milliseconds.'),
    dict(level='advanced', title='Locality-aware task plan', stmt='Given block locations (like getFileBlockLocations returns) and 3 worker nodes, assign each block to a worker that holds a replica, keeping the load as even as possible. Print the plan and how many blocks are local.', inp='6 blocks · hosts per block',
         code='''locs = {0: ["dn-1", "dn-2", "dn-3"], 1: ["dn-1", "dn-2", "dn-3"], 2: ["dn-1", "dn-3", "dn-4"],
        3: ["dn-2", "dn-4", "dn-5"], 4: ["dn-1", "dn-5", "dn-2"], 5: ["dn-4", "dn-5", "dn-3"]}
workers = {"dn-1": [], "dn-2": [], "dn-3": []}
for b, hosts in locs.items():
    local = [w for w in workers if w in hosts]
    pick = min(local or workers, key=lambda w: len(workers[w]))
    workers[pick].append((b, "local" if pick in hosts else "remote"))
print(workers)
print("local:", sum(t == "local" for v in workers.values() for _, t in v), "of", len(locs))
''', explain='Every block finds a worker with a local replica here, two blocks each. This is the core idea of MapReduce scheduling (Module 8): move the computation to the data.'),
]

SCN_INTRO = 'API questions check whether you can go beyond the shell and understand what client code really does.'
SCENARIOS = '''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">HDFS · Java</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“Write code to copy a local file to HDFS”</h4>
      <p class="scn__situation">A whiteboard coding question.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> Configuration, FileSystem, Path, closing resources.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li><code>Configuration conf = new Configuration(); FileSystem fs = FileSystem.get(conf);</code></li>
          <li><code>fs.copyFromLocalFile(new Path("orders.csv"), new Path("/user/hadoop/raw/"));</code>, or <code>fs.create()</code> plus <code>IOUtils.copyBytes()</code> from a local input stream.</li>
          <li>Close streams with try-with-resources; mention that the bytes go through the DataNode write pipeline.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Production · bug</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A web service fails with “java.io.IOException: Filesystem closed”</h4>
      <p class="scn__situation">It happens randomly, after some requests finish.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> the FileSystem cache.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>Some code calls <code>fs.close()</code> on an instance from <code>FileSystem.get()</code>, which is cached and shared by all threads.</li>
          <li>Fix: never close the shared instance (close only streams), or use <code>FileSystem.newInstance()</code> where code must own and close its instance.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Design</span><span class="scn__tag scn__tag--level">Experienced</span></div>
      <h4>A Python dashboard must read results from HDFS</h4>
      <p class="scn__situation">No Hadoop installation on the dashboard servers, and a firewall in between.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> WebHDFS vs HttpFS.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>WebHDFS works over HTTP, but OPEN redirects to DataNodes on port 9864, so every DataNode must be reachable.</li>
          <li>Through a firewall, use <b>HttpFS</b>: a gateway that streams the data itself, so only one host and port are opened.</li>
          <li>Keep results small (aggregated by Hive or Spark) so the dashboard never pulls raw data.</li>
        </ul>
      </div></details>
    </article>
    <article class="scn">
      <div class="scn__head"><span class="scn__tag">Performance</span><span class="scn__tag scn__tag--level">Fresher</span></div>
      <h4>“My Java program takes 17 hours to scan 4 TB. Why?”</h4>
      <p class="scn__situation">A single program reads a big file from start to end.</p>
      <p class="scn__look"><b>The interviewer is checking:</b> single client vs parallel processing.</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        <ul>
          <li>One client reads one stream: in our lab about 68 MB/s, so 4 TB ≈ 17 hours.</li>
          <li>HDFS can serve many readers at once. Split the work by blocks (getFileBlockLocations) and run readers on the nodes that hold them: that is MapReduce or Spark.</li>
        </ul>
      </div></details>
    </article>
'''
