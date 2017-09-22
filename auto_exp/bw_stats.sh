#!/bin/bash


for i in `ls ../pensieve/sim/cooked_traces/*`; do
  #echo $i
  awk '{sum += $2 * 1000; sumsq += ($2*1000)^2} END {printf "%f %f \n", sum/NR, sqrt((sumsq-sum^2/NR)/NR)}' < $i
done


