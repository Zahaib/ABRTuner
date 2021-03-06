#!/usr/bin/python

import os, sys
import numpy as np

if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to result file>"
  sys.exit()

lines = open(sys.argv[1]).readlines()

result = dict()

for l in lines:
  l = l.rstrip()
  row = l.split(" ")
  name = row[0].split("/")[-1]
  if name not in result.keys():
    result[name] = dict()
    result[name]['best_disc'] = -1
    result[name]['default_perf'] = -1
    result[name]['best_avgbr'] = -1
    result[name]['best_rebuf'] = 1.0
    result[name]['avgbw'] = -1.0
    result[name]['stdbw'] = -1.0
  win = int(row[6])
  avgbr = float(row[13])
  rebuf = float(row[16])
  disc = int(row[-1])
  avgbw = float(name.split("_")[1])
  stdbw = float(name.split("_")[2].split(".")[0])
  try:
    cv = stdbw / avgbw
  except ZeroDivisionError:
    cv = 0
  if disc < 0:
    result[name]['default_perf'] = [avgbr, rebuf, avgbw, stdbw]
  if avgbr > result[name]['best_avgbr'] and rebuf <= result[name]['best_rebuf'] or avgbr >= result[name]['best_avgbr'] and rebuf < result[name]['best_rebuf']:
    result[name]['best_disc'] = disc
    result[name]['best_avgbr'] = avgbr
    result[name]['best_rebuf'] = rebuf
    result[name]['avgbw'] = avgbw
    result[name]['stdbw'] = stdbw

for name in result.keys():
  try:
    print name,  float(result[name]['avgbw']), float(result[name]['stdbw']), result[name]['stdbw'] / float(result[name]['avgbw']), result[name]['best_disc']
  except ZeroDivisionError:
    print name,  float(result[name]['avgbw']), float(result[name]['stdbw']), 0, result[name]['best_disc']

#avgbr_diff = list()
#rebuf_diff = list()
#for name in result.keys():
#  mpc_def = result[name]['default_perf']
#  avgbr_per_diff = ((result[name]['best_avgbr'] - mpc_def[0]) / mpc_def[0]) * 100
#  rebuf_per_diff = (mpc_def[1] - result[name]['best_rebuf']) * 100
#  avgbr_diff.append(avgbr_per_diff)
#  rebuf_diff.append(rebuf_per_diff)
#
#f_out = open('avgbr_rebuff_percentage_diff.dat', 'w')
#for i in range(0,101):
#  f_out.write(str(i) + " " +  str(np.percentile(avgbr_diff, i)) + " " + str(np.percentile(rebuf_diff,i)) + "\n")
#f_out.close()
#
