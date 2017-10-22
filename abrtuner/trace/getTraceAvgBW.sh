#!/bin/bash

dir=$(echo $1 | cut -d/ -f1)
dir=$dir"/"
#echo $dir

limit=500

ls $dir* | while read line; do
  avgbw=$(awk '{ total += $2 } END { print total/NR }'  $line)
  comp=$(echo "$avgbw<$limit" | bc)
  if [ $comp -eq 1 ]; then
    echo $line, $avgbw
  fi
done
