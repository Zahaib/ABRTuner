#!/usr/bin/python

import numpy as np
import os, sys

if len(sys.argv) < 2:
	print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to simulation output results>"
	sys.exit()

lines = open(sys.argv[1]).readlines()

AVGBR, REBUF = [], []

index_to_bitrate = {0:300,1:750,2:1200,3:1850,4:2850,5:4300}


for l in lines:
	l = l.rstrip()
	row = l.split(" ")
	fn = row[0]
	avgbr = float(row[9])
	rebuf = float(row[12])
	AVGBR.append(avgbr)
	REBUF.append(rebuf)	



for i in range(101):
	print i, round(np.percentile(AVGBR, i),4), round(np.percentile(REBUF, i),4)
