# edit_log_report.py: make a few changes in HDFS, then read them back from the NameNode's edit log.
# Run in the hdfs-lab folder while the cluster is up.
import json
import subprocess
import xml.etree.ElementTree as ET

NAME_DIR = "/tmp/hadoop-hadoop/dfs/name/current"

def nn(*cmd):
    return subprocess.run(["docker", "compose", "exec", "-T", "namenode", *cmd],
                          capture_output=True, text=True).stdout

def last_txid():
    url = "http://namenode:9870/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
    info = json.loads(json.loads(nn("curl", "-s", url))["beans"][0]["JournalTransactionInfo"])
    return int(info["LastAppliedOrWrittenTxId"])

before = last_txid()
print("last transaction before our changes:", before)
for cmd in (["hdfs", "dfs", "-mkdir", "-p", "data/demo"],
            ["hdfs", "dfs", "-touchz", "data/demo/order.txt"],
            ["hdfs", "dfs", "-mv", "data/demo/order.txt", "data/demo/order_old.txt"],
            ["hdfs", "dfs", "-rm", "-r", "-skipTrash", "data/demo"]):
    nn(*cmd)

# a checkpoint may have closed the segment meanwhile, so read the newest two edit files
files = nn("bash", "-c", f"ls {NAME_DIR} | grep ^edits_ | tail -2").split()
for f in files:
    nn("hdfs", "oev", "-i", f"{NAME_DIR}/{f}", "-o", "/tmp/edits.xml")
    for rec in ET.fromstring(nn("cat", "/tmp/edits.xml")).iter("RECORD"):
        data = rec.find("DATA")
        txid = int(data.findtext("TXID"))
        path = data.findtext("PATH") or data.findtext("SRC") or ""
        dst = data.findtext("DST")
        if txid > before and path:
            print(f"txid {txid:>4}  {rec.findtext('OPCODE'):15} {path}"
                  + (f" -> {dst}" if dst else "") + f"   [{f}]")
