# rack_check.py: does every block follow the rack-aware placement rules?
# Run in the hdfs-lab folder while the cluster is up.
import re
import subprocess
from collections import Counter

cmd = ["docker", "compose", "exec", "-T", "namenode",
       "hdfs", "fsck", "/user/hadoop/data", "-files", "-blocks", "-racks"]
out = subprocess.run(cmd, capture_output=True, text=True).stdout

for line in out.splitlines():
    m = re.search(r"(blk_\d+)_\d+ len=(\d+).*\[(.*)\]", line)
    if not m:
        continue
    blk, racks = m.group(1), re.findall(r"(/rack\d+)/", m.group(3))
    per_rack = Counter(racks)
    ok = len(per_rack) >= 2 and max(per_rack.values()) <= 2
    print(f"{blk}: {dict(per_rack)}  {'OK' if ok else 'CHECK'}")
