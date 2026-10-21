#!/bin/bash
# Rack topology script: Hadoop passes IP addresses, we print one rack per argument.
for host in "$@"; do
  name=$(getent hosts "$host" | awk '{print $2}')
  n=$(echo "$name" | grep -o 'datanode-[0-9]*' | grep -o '[0-9]*$')
  if [ -z "$n" ]; then echo "/default-rack"
  elif [ "$n" -le 2 ]; then echo "/rack1"
  else echo "/rack2"; fi
done
