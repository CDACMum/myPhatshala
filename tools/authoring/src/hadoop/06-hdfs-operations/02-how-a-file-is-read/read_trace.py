# read_trace.py: read the same file from two different clients and show
# which DataNode served each block. Run in the hdfs-lab folder.
import re
import subprocess

LOG4J = """log4j.rootLogger=WARN, err
log4j.appender.err=org.apache.log4j.ConsoleAppender
log4j.appender.err.Target=System.err
log4j.appender.err.layout=org.apache.log4j.PatternLayout
log4j.appender.err.layout.ConversionPattern=%m%n
log4j.logger.org.apache.hadoop.hdfs.DFSClient=DEBUG
"""
FILE = "/user/hadoop/data/canteen_1mb.csv"

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

names = {}
for n in sh("docker ps --format '{{.Names}}'").stdout.split():
    ip = sh("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + n).stdout.strip()
    names[ip] = n.replace("lab5-", "")

fsck = sh(f"docker compose exec -T namenode hdfs fsck {FILE} -files -blocks -locations").stdout
for i, line in enumerate(l for l in fsck.splitlines() if "blk_" in l):
    hosts = re.findall(r"(\d+\.\d+\.\d+\.\d+):9866", line)
    print(f"block {i} replicas on: {', '.join(names[h] for h in hosts)}")

for client in ["lab5-namenode-1", "lab5-datanode-2"]:
    sh(f"docker exec -i {client} bash -c 'cat > /tmp/r.properties' <<'X'\n{LOG4J}X")
    err = sh(f"docker exec {client} bash -c 'HADOOP_CLIENT_OPTS=-Dlog4j.configuration=file:/tmp/r.properties "
             f"hdfs dfs -cat {FILE} > /dev/null'").stderr
    served = re.findall(r"Connecting to datanode (\d+\.\d+\.\d+\.\d+):9866", err)
    print(f"client {client.replace('lab5-', ''):11} read from: {', '.join(names[s] for s in served)}")
