#!/usr/bin/env bash
# where_is_my_file.sh: show the real block files behind one HDFS file
# usage: bash where_is_my_file.sh /user/hadoop/data/canteen_orders.csv
file=$1
docker compose exec -T namenode hdfs fsck "$file" -files -blocks -locations 2>/dev/null |
  grep -o 'blk_[0-9]*_[0-9]* len=[0-9]*\|[0-9.]*:9866' | while read -r item; do
    case "$item" in
      blk_*) blk=$(echo "$item" | cut -d_ -f1-2); echo "$item";;
      *) ip=${item%:9866}
         c=$(docker ps --format '{{.Names}}' | while read n; do
               docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} $n" "$n"; done |
             awk -v ip="$ip" '$1==ip {print $2}')
         path=$(docker exec "$c" find /tmp/hadoop-hadoop/dfs/data -name "$blk" 2>/dev/null)
         size=$(docker exec "$c" stat -c %s "$path")
         echo "   on $c  ($ip)  file size $size bytes";;
    esac
  done
