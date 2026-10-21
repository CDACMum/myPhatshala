#!/usr/bin/env bash
# which_mode.sh: which Hadoop mode is this machine in?
fs=$(hdfs getconf -confKey fs.defaultFS 2>/dev/null)
fw=$(hdfs getconf -confKey mapreduce.framework.name 2>/dev/null)
daemons=$(jps | awk '$2 != "Jps" {print $2}' | sort | tr '\n' ' ')
echo "fs.defaultFS             : $fs"
echo "mapreduce.framework.name : $fw"
echo "daemons on this machine  : ${daemons:-none}"
case "$fs" in
  file:*)                              echo "MODE: standalone (local files, no daemons)" ;;
  hdfs://localhost*|hdfs://127.0.0.1*) echo "MODE: pseudo-distributed (every daemon on this machine)" ;;
  hdfs://*)                            echo "MODE: fully distributed (NameNode at ${fs#hdfs://})" ;;
esac
