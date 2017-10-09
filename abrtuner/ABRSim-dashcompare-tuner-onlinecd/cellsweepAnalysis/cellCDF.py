#!/usr/bin/python

import sys, os
import numpy as np

if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to results file>"
  sys.exit()

lines = open(sys.argv[1]).readlines()

tracePerf = dict()


def parse():
  for l in lines:
    l = l.rstrip()
    name = l.split(" ")[0]
    cellsize = int(l.split(" ")[4]) 
    avgbr = float(l.split(" ")[9])
    rebuf = float(l.split(" ")[12])
    if name not in tracePerf.keys():
      tracePerf[name] = dict()
    if cellsize not in tracePerf[name].keys():
      tracePerf[name][cellsize] = [avgbr, rebuf]
    #print name, cellsize, avgbr, rebuf
    #sys.exit()

def makeCDF():
  cellavgbr = dict()
  cellrebuf = dict()
  for name in tracePerf.keys():
    for cell in sorted(tracePerf[name].keys()):
      if cell not in cellavgbr.keys():
        cellavgbr[cell] = []
      if cell not in cellrebuf.keys():
        cellrebuf[cell] = []
      cellavgbr[cell].append(tracePerf[name][cell][0])
      cellrebuf[cell].append(tracePerf[name][cell][1])
  return cellavgbr, cellrebuf


def printCDF(target):
  for i in range(0, 101):
    print i,
    for cell in sorted(target.keys()):
      print np.percentile(target[cell], i),
    print ""


parse()
cellavgbr, cellrebuf = makeCDF()
printCDF(cellavgbr)
printCDF(cellrebuf)

