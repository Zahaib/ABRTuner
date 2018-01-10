#!/usr/bin/python
import sys, os
import math
import numpy as np

VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
VIDEO_BIT_RATE_TO_INDEX = {300:0,750:1,1200:2,1850:3,2850:4,4300:5}
CHUNKSIZE = 4.0

### BOLA settings
MINIMUM_BUFFER_S = 5 #10 # BOLA should never add artificial delays if buffer is less than MINIMUM_BUFFER_S. Orig val: 10
BUFFER_TARGET_S = 15# If Schedule Controller does not allow buffer level to reach BUFFER_TARGET_S, this can be a virtual buffer level. Orig val: 30
BOLA_BITRATES = [br * 1000.0 for br in VIDEO_BIT_RATE]
BOLA_UTILITIES = [math.log(br) for br in BOLA_BITRATES]

def getBolaGP():
  gp = 1 - BOLA_UTILITIES[0] + (BOLA_UTILITIES[-1] - BOLA_UTILITIES[0]) / (BUFFER_TARGET_S / MINIMUM_BUFFER_S - 1)
  return gp
   
def getBolaVP(BOLA_GP):
  vp = MINIMUM_BUFFER_S / (BOLA_UTILITIES[0] + BOLA_GP - 1)   
  return vp

def getBOLADecision(bufferlen, gp, Vp):
  # Vp = getBolaVP(gp)
  quality = None
  score = -sys.maxint
  #print >> sys.stderr , gp, Vp
  #gp = -10.9458907969
  for i in range(len(BOLA_BITRATES)):
    s = (Vp * (BOLA_UTILITIES[i] + gp) - bufferlen) / BOLA_BITRATES[i]
    if s >= score:
      score = s
      quality = i
  return quality

bola_gp = getBolaGP()
bola_vp = getBolaVP(bola_gp)
tmp_buff = BUFFER_TARGET_S
tmp_min = MINIMUM_BUFFER_S

print "buf\tgp\tvp\t15\t20\t25\t30\t35\t40\t45\t50\t55\t60\t10-30"
for i in np.arange(0, 36, 0.5):
  BUFFER_TARGET_S = tmp_buff
  MINIMUM_BUFFER_S = tmp_min
  bola_br = []
  for j in range(10):
    bola_gp = getBolaGP()
    bola_vp = getBolaVP(bola_gp)
    br = getBOLADecision(i, bola_gp, bola_vp)
    bola_br.append(VIDEO_BIT_RATE[br])
    BUFFER_TARGET_S += 5
  BUFFER_TARGET_S = 30
  MINIMUM_BUFFER_S = 10
  bola_gp = getBolaGP()
  bola_vp = getBolaVP(bola_gp)
  br_10_30 = getBOLADecision(i, bola_gp, bola_vp)
  bola_br.append(VIDEO_BIT_RATE[br_10_30])
  print str(i) + "\t" + str(round(bola_gp, 2)) + "\t" + str(round(bola_vp, 2)) + "\t" + '\t'.join([str(br) for br in bola_br])
  #print i, round(bola_gp, 2), round(bola_vp, 2), bola_br, VIDEO_BIT_RATE[bola_br], VIDEO_BIT_RATE[bola_br_1], VIDEO_BIT_RATE[bola_br_2], VIDEO_BIT_RATE[bola_br_3], VIDEO_BIT_RATE[bola_br_4], VIDEO_BIT_RATE[bola_br_5], VIDEO_BIT_RATE[bola_br_6]
