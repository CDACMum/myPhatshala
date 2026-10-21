#!/usr/bin/env bash
# webhdfs.sh: the same file system over plain HTTP (REST). No Java, no Hadoop client needed.
# Run inside the namenode container:  bash webhdfs.sh
NN=http://namenode:9870/webhdfs/v1
F=/user/hadoop/canteen/raw/day1.csv
echo "--- GETFILESTATUS (metadata, answered by the NameNode)"
curl -s "$NN$F?op=GETFILESTATUS&user.name=hadoop"; echo
echo "--- OPEN without following redirects"
curl -s -i "$NN$F?op=OPEN&user.name=hadoop" | grep -iE "^HTTP|^Location"
echo "--- OPEN, following the redirect to the DataNode (-L)"
curl -s -L "$NN$F?op=OPEN&user.name=hadoop"
