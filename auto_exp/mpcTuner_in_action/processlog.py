#!/usr/bin/python

import os, sys
import numpy as np

if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to log file>"
  sys.exit()

lines = open(sys.argv[1]).readlines()

start_time = 0
for i, l in enumerate(lines):
  l = l.strip()
  row = l.split('\t')
  if i == 0:
    start_time = int(row[5])
  change = -1
  if float(row[7]) > 0.0:
    change = 1
  curr_time = int(row[6])
  config = float(row[15])
  time_since_start = (curr_time - start_time) / 1000.0
  #print time_since_start, change, config
  if change == 1:
    print time_since_start - 0.001, 0, config
    print time_since_start, change, config
    print time_since_start + 0.001, 0, config
  else:
    print time_since_start, change,config
  
