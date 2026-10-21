#!/usr/bin/env bash
# shell_lab.sh: practise the everyday hdfs dfs commands on a small folder.
# Run inside the namenode container:  bash shell_lab.sh
set -e
run() { echo "\$ $*"; eval "$@"; echo; }
cd /tmp
printf 'order_id,item,amount\n4001,idli,30\n4002,chai,15\n' > mon.csv
printf 'order_id,item,amount\n4003,dosa,45\n' > tue.csv
D=/user/hadoop/shell_lab

run "hdfs dfs -rm -r -f -skipTrash $D > /dev/null"
run "hdfs dfs -mkdir -p $D/raw"
run "hdfs dfs -put mon.csv tue.csv $D/raw/"
run "hdfs dfs -ls $D/raw"
run "hdfs dfs -cat $D/raw/mon.csv"
run "hdfs dfs -du -s -h $D"
run "hdfs dfs -cp $D/raw/mon.csv $D/mon_backup.csv"
run "hdfs dfs -mv $D/mon_backup.csv $D/archive_mon.csv"
run "hdfs dfs -getmerge $D/raw week.csv && wc -l week.csv"
run "hdfs dfs -setrep -w 2 $D/archive_mon.csv"
run "hdfs dfs -stat '%n %r %b' $D/archive_mon.csv"
run "hdfs dfs -count -v $D"
run "hdfs dfs -D fs.trash.interval=60 -rm $D/archive_mon.csv"
run "hdfs dfs -ls -R $D"
