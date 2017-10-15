#!/bin/bash

while read line; do
  awk '{{sum += $2; sumsq += ($2)^2}} END {printf "%f %f \n", sum/NR, sqrt((sumsq-sum^2/NR)/NR)}' $line
done < $1
