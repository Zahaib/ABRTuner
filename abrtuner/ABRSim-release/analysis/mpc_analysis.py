#!/usr/bin/python

import os, sys
import numpy as np

if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to results file>"
  sys.exit()

lines = open(sys.argv[1]).readlines()

results = dict()

for l in lines:
  l = l.rstrip()
  row = l.split(" ")
  fn = row[0].split("/")[-1]
  win = int(row[6])
  avgbr = float(row[13])
  rebuf = float(row[16])
  change = float(row[8])
  if win not in results.keys():
    results[win] = dict()
    results[win]['name'] = list()
    results[win]['avgbr'] = list()
    results[win]['rebuf'] = list()
    results[win]['change'] = list()
  results[win]['name'].append(fn)
  results[win]['avgbr'].append(avgbr)
  results[win]['rebuf'].append(rebuf)
  results[win]['change'].append(change)


for i in range(0,101):
  print i,
  for win in sorted(results.keys()):
    print round(np.percentile(results[win]['avgbr'], i), 2),

  for win in sorted(results.keys()):
    print round(np.percentile(results[win]['rebuf'], i), 2),

  for win in sorted(results.keys()):
    print round(np.percentile(results[win]['change'], i), 2),
  print ""

  


