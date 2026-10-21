#!/usr/bin/env bash
# decommission_watch.sh: retire one DataNode safely and watch HDFS copy its blocks away.
# Needs dfs.hosts.exclude=/opt/hadoop/etc/hadoop/dfs.exclude in the NameNode's hdfs-site.xml.
# Run from the hdfs-lab folder:  bash decommission_watch.sh 172.19.0.4
IP=${1:?give the DataNode IP}
NN="docker exec lab5-namenode-1"
status() { $NN hdfs dfsadmin -report 2>/dev/null | grep -m1 -A20 "^Name: $IP:" |
           grep -E "Decommission Status|Num of Blocks" | sed 's/ : /: /' | paste -sd'|' | sed 's/|/,  /'; }
echo "before:  $(status)"
$NN bash -c "echo $IP > /opt/hadoop/etc/hadoop/dfs.exclude"
$NN hdfs dfsadmin -refreshNodes
start=$(date +%s)
while true; do
  s=$(status); echo "t=$(( $(date +%s) - start ))s  $s"
  [[ $s == *"Status: Decommissioned"* ]] && break
  sleep 5
done
$NN bash -c "hdfs fsck / 2>/dev/null | grep -E 'Status:|Under-replicated|Number of data-nodes'"
echo "### recommission"
$NN bash -c "> /opt/hadoop/etc/hadoop/dfs.exclude"
$NN hdfs dfsadmin -refreshNodes
sleep 10; echo "after:   $(status)"
