#!/bin/bash


#for i in `ls ../pensieve/sim/cooked_traces/*`; do
  #echo $i
#  awk '{sum += $2 * 1000; sumsq += ($2*1000)^2} END {printf "%f %f \n", sum/NR, sqrt((sumsq-sum^2/NR)/NR)}' < $i
#done

> lt_3000_raw.txt

for i in `ls trace_500_pen/*`; do
  #echo $i
  #awk '{sum += $2; sumsq += ($2)^2} END {printf "%f %f \n", sum/NR, sqrt((sumsq-sum^2/NR)/NR)}' < $i
  a=$(awk '{avg += $2} END {printf "%f \n", avg/NR}' < $i)
  #echo $a

  if (( $(bc <<< "$a > 5000") ))
  then
      fn=$(echo $i | cut -d/ -f1 --complement | cut -d. -f1)
      fn_dict=$(echo $i | cut -d/ -f1 --complement | cut -d. -f1 | cut -d_ -f4-5 | sed 's/_//g')
      #echo $fn, $fn_dict
      #echo \'$fn_dict\'
      #cat $i >> lt_3000_raw.txt
      echo $i, $a
      #cp tuner_pensieve_mpc_results/*$fn* tuner_pensieve_mpc_results_3000/
  fi

done
