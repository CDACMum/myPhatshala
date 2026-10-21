# write_trace.py: upload a file from datanode-1 with client debug logging,
# then summarise what the write pipeline did. Run in the hdfs-lab folder.
import re
import subprocess

LOG4J = """log4j.rootLogger=WARN, err
log4j.appender.err=org.apache.log4j.ConsoleAppender
log4j.appender.err.Target=System.err
log4j.appender.err.layout=org.apache.log4j.PatternLayout
log4j.appender.err.layout.ConversionPattern=%d{HH:mm:ss,SSS} %m%n
log4j.logger.org.apache.hadoop.hdfs.DataStreamer=DEBUG
"""
CLIENT = "lab5-datanode-1"           # a DataNode, so replica 1 is written locally

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

sh(f"docker exec -i {CLIENT} bash -c 'cat > /tmp/w.properties' <<'X'\n{LOG4J}X")
sh(f"docker exec {CLIENT} bash -c 'for i in $(seq 30); do cat /tmp/canteen_orders.csv; done > /tmp/orders_x30.csv'")
log = sh(f"docker exec {CLIENT} bash -c 'HADOOP_CLIENT_OPTS=-Dlog4j.configuration=file:/tmp/w.properties "
         f"hdfs dfs -put -f /tmp/orders_x30.csv /user/hadoop/data/orders_x30.csv'").stderr

ip_to_name = {}
for n in sh("docker ps --format '{{.Names}}'").stdout.split():
    ip = sh("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + n).stdout.strip()
    ip_to_name[ip] = n.replace("lab5-", "")

for m in re.finditer(r"pipeline = \[(.*?)\]\], (blk_\d+)", log):
    ips = re.findall(r"(\d+\.\d+\.\d+\.\d+):9866", m.group(1))
    print(m.group(2), "pipeline:", " -> ".join(ip_to_name.get(ip, ip) for ip in ips))
packets = len(re.findall(r"sending packet seqno", log))
acks = len(re.findall(r"reply: SUCCESS reply: SUCCESS reply: SUCCESS", log))
first = re.search(r"seqno: 0 offsetInBlock: 0 lastPacketInBlock: false lastByteOffsetInBlock: (\d+)", log)
times = re.findall(r"^(\d\d:\d\d:\d\d,\d+)", log, re.M)
print(f"packets sent: {packets}, acknowledged by all 3 DataNodes: {acks}")
print(f"data bytes per full packet: {first.group(1)}")
print(f"first log line {times[0]}, last {times[-1]}")
