# heartbeat_watch.py: freeze one DataNode and watch the NameNode's view of it
# change from live to stale to dead. Run in the hdfs-lab folder.
import json
import subprocess
import time

DN = "lab5-datanode-4"
URL = "http://namenode:9870/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def nn_view(host):
    info = json.loads(sh("docker", "compose", "exec", "-T", "namenode", "curl", "-s", URL))["beans"][0]
    for state in ("LiveNodes", "DeadNodes"):
        for name, node in json.loads(info[state]).items():
            if name.startswith(host):
                return state[:-5].lower(), node["lastContact"]
    return "unknown", None

host = sh("docker", "inspect", "-f", "{{.Config.Hostname}}", DN).strip()
sh("docker", "pause", DN)                      # the process freezes: no more heartbeats
start = time.time()
try:
    while time.time() - start < 80:
        time.sleep(8)
        state, last = nn_view(host)
        print(f"t={time.time() - start:3.0f}s  NameNode says: {state:5} lastContact={last}s")
finally:
    sh("docker", "unpause", DN)
time.sleep(6)
print("after unpause:", nn_view(host))
