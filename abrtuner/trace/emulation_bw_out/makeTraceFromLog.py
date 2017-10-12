#!/usr/bin/python

import os, sys
import numpy as np
import math

if len(sys.argv) < 3:
  print >> sys.stderr, "Incorrect usage:\nUsage: python " + sys.argv[0] + " <path to log file> <path to store traces>"
  sys.exit()

lines = open(sys.argv[1]).readlines()
outpath = sys.argv[2].rstrip('/') + "/"

def roundup_1000(x):
  return int(math.ceil(x / 1000.0)) * 1000

def write_file(trace_num, bw_l, ts_l):
  f_out = open(outpath+str(trace_num)+"_emulated.txt", "w")
  for i in range(0, len(bw_l)):
    curr_ts = roundup_1000(ts_l[i])
    if i < len(bw_l) - 1:
      next_ts = roundup_1000(ts_l[i+1])
      for ts_1000 in np.arange(curr_ts, next_ts, 1000.0):
        f_out.write(str(ts_1000) + " " + str(bw_l[i]) + "\n")
    elif i == len(bw_l) - 1:
      for ts_1000 in np.arange(curr_ts, curr_ts + 5001.0, 1000.0):
        f_out.write(str(ts_1000) + " " + str(bw_l[i]) + "\n")
  f_out.close()


trace_num = 1
bw_l = list()
ts_l = list()
new_trace = True
prev_ts = 0
for i, l in enumerate(lines):
  if l in ['\n', '\r\n'] or i == len(lines) - 1:
    trace_num += 1
    write_file(trace_num, bw_l, ts_l)
    if i < len(lines) - 1:
      ts_l = list()
      bw_l = list()
    new_trace = True
  else:
    l = l.rstrip()
    row = l.split("\t")
    ts = float(row[0])
    bw = (float(row[4]) * 8) / float(row[5])
    if new_trace:
      ts_l.append(0)
      bw_l.append(bw)
      new_trace = False
      prev_ts = ts
    else:
      ts_l.append(int((ts - prev_ts) * 1000))
      bw_l.append(bw)
    #prev_ts = ts
  
  
