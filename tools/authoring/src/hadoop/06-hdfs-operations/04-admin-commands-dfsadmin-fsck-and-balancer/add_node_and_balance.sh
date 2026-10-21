#!/usr/bin/env bash
# add_node_and_balance.sh: add a new, empty DataNode with its own small disk, then run the balancer.
# Run from the hdfs-lab folder (compose project "lab5", network lab5_default).
NN="docker exec lab5-namenode-1"
show() {
  $NN hdfs dfsadmin -report 2>/dev/null |
    awk '/^Name:/{ip=$2; sub(":9866","",ip)} /^DFS Used%/{if(ip) printf "  %-12s used %6s\n", ip, $3; ip=""}'
}
echo "### 1. Start datanode-6 with a 1.5 GB disk of its own (a RAM disk)"
docker run -d --name lab5-datanode-6 --hostname datanode-6 --network lab5_default \
  --env-file config --tmpfs /tmp/hadoop-hadoop:size=1536m,mode=1777 \
  apache/hadoop:3.5.0 hdfs datanode > /dev/null
sleep 25; show
echo "### 2. Balancer, threshold 5%"
$NN hdfs balancer -threshold 5 2>&1 |
  grep -E "underutilized|Need to move|Decided to move|Successfully moved|Out of space|^[A-Z][a-z]{2} [0-9]+, |No block|Iteration#" |
  sed -E 's/^2026-[0-9-]+ ([0-9:]+) (INFO|WARN)  [A-Za-z]+:[0-9]+ - /\1 /; s/java.io.IOException: Got error.*(Out of space)/  ... \1/; s/:9866:DISK//g' | cut -c1-150
echo "### 3. After"
show
