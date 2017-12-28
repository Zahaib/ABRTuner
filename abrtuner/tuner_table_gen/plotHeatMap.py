#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os, sys

if len(sys.argv) < 2:
	print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to output of compare_allconfig.py>"
	sys.exit()

lines = open(sys.argv[1]).readlines()


def getBwStd(fn):
	lines = open(fn)
	BW = []
	for l in lines:
		l = l.rstrip()
		row = l.split(" ")
		bw = float(row[-1])
		BW.append(bw)
	return np.mean(BW), np.std(BW)


BW, STD, PARAM = np.array([]), np.array([]), np.array([])

for l in lines:
	l = l.rstrip()
	l = l.replace("(", "").replace(")", "").replace(",", "")
	row = l.split(" ")
	fn = row[0]
	param = row[-1]
	bw, std = getBwStd(fn)
	BW = np.append(BW, bw)
	STD = np.append(STD, std)
	PARAM = np.append(PARAM, param)

	# print bw, std, param


# create x-y points to be used in heatmap
# xi = np.linspace(BW.min(),BW.max(),500)
# yi = np.linspace(STD.min(),STD.max(),500)
xi = np.linspace(BW.min(),8000,5000)
yi = np.linspace(STD.min(),6000,5000)


# Z is a matrix of x-y values
zi = griddata((BW, STD), PARAM, (xi[None,:], yi[:,None]), method='cubic')

# I control the range of my colorbar by removing data 
# outside of my range of interest
zmin = -11.5
zmax = -1
zi[(zi<zmin) | (zi>zmax)] = None

# Create the contour plot
CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
                  vmax=zmax, vmin=zmin)
plt.colorbar()  
plt.show()