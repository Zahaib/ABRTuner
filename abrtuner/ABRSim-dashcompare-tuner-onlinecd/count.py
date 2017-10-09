#!/usr/bin/python

import numpy as np 
import sys

if len(sys.argv) < 3:
  print >> sys.stderr, "Incorrect Usage...\nUsage: python " + sys.argv[0] + " <path to bw-std file> <binsize>"
  sys.exit()

def printPercentile(target):
  for i in range(90,100,1):
    print str(i) + " " + str(np.percentile(target, i))

h = sys.argv[1]
binsize = int(sys.argv[2])
lines = open(h).readlines()
count = dict()
#binsize = 1000
cv = [] 
for l in lines:
  l = l.rstrip()
  bw = float(l.split(" ")[0])
  std = float(l.split(" ")[1])
  bw_10k = int(bw) / binsize
  std_10k = int(std) / binsize

  if bw < binsize:
    cv.append(std/bw)
  if bw_10k in count.keys():
    count[bw_10k] += 1
  else:
    count[bw_10k] = 1


print "total: " + str(sum(count.values())) + " actual count: " + str(count)
printPercentile(cv)
#print np.percentile(cv, 50), np.percentile(cv, 75), np.percentile(cv, 95)
