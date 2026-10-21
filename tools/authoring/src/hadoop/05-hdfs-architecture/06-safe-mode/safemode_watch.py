# safemode_watch.py: restart the NameNode and follow safe mode until it ends.
# Run in the hdfs-lab folder while the cluster is up.
import json
import re
import subprocess
import time

URL = "http://namenode:9870/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

def nn(*cmd):
    return subprocess.run(["docker", "compose", "exec", "-T", "namenode", *cmd],
                          capture_output=True, text=True).stdout.strip()

def explanation():
    try:
        return json.loads(nn("curl", "-s", URL))["beans"][0]["Safemode"] or "(off)"
    except (ValueError, KeyError, IndexError):
        return "(NameNode not answering yet)"

subprocess.run(["docker", "restart", "lab5-namenode-1"], capture_output=True)
start = time.time()
while time.time() - start < 120:
    state = nn("hdfs", "dfsadmin", "-safemode", "get").splitlines()
    state = state[-1] if state else "(no answer)"
    why = explanation()
    blocks = re.search(r"reported blocks (\d+).*?total blocks (\d+)", why)
    left = re.search(r"in (\d+) seconds", why)
    detail = (f"reported {blocks.group(1)}/{blocks.group(2)} blocks" if blocks else why[:40]) + \
             (f", off in {left.group(1)} s" if left else "")
    print(f"t={time.time() - start:3.0f}s  {state:24} {detail}")
    if "OFF" in state:
        break
    time.sleep(5)
