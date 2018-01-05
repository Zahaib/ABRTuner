#!/usr/bin/python

import sys, os
import numpy as np
import math
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial

VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
BOLA_BITRATES = [br * 1000.0 for br in VIDEO_BIT_RATE]
BOLA_UTILITIES = [math.log(br) for br in BOLA_BITRATES]
MINIMUM_BUFFER_S = 5
BUFFER_TARGET_S = 15

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
  # print >> sys.stderr, gp, Vp
  for i in range(len(BOLA_BITRATES)):
    s = (Vp * (BOLA_UTILITIES[i] + gp) - bufferlen) / BOLA_BITRATES[i]
    if s >= score:
      score = s
      quality = i
  return quality


def getBWFeaturesWeightedPlayerVisible(playerVisibleBW, chunk_when_last_chd_ran):
  lookbackwindow = len(playerVisibleBW) - min(51, len(playerVisibleBW) - chunk_when_last_chd_ran)
  currentstateBWArray = playerVisibleBW[lookbackwindow:]
  return np.mean(currentstateBWArray), np.std(currentstateBWArray)


def onlineCD(chunk_when_last_chd, interval, playerVisibleBW):
  chd_detected = False
  chd_index = chunk_when_last_chd
  # threshold for the amount to samples to consider for change point
  trimThresh = 100
  lenarray = len(playerVisibleBW)
  playerVisibleBW, cutoff = trimPlayerVisibleBW(playerVisibleBW, trimThresh)
  R, maxes = oncd.online_changepoint_detection(np.asanyarray(playerVisibleBW), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
  #interval = 5
  interval = min(interval, len(playerVisibleBW))
  changeArray = R[interval,interval:-1]
  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
    if v > 0.01 and i + cutoff > chunk_when_last_chd and not (i == 0 and chunk_when_last_chd > -1) :
      chd_index = i + cutoff
      chd_detected = True
      print "change detected i = ", i, " cutoff = ", cutoff, " chd_index = ", chd_index, " chunk_when_last_chd =", chunk_when_last_chd, " len = ", lenarray,
      break
  return chd_detected, chd_index

def trimPlayerVisibleBW(playerVisibleBW, thresh):
  ret = []
  cutoff = 0
  lenarray = len(playerVisibleBW)
  if lenarray <= thresh:
    return playerVisibleBW, cutoff
  
  cutoff = lenarray - thresh
  ret = playerVisibleBW[cutoff:]
  return ret, cutoff


def getDynamicconfig_bola(pv_list, bw, std, step):
    bw_step = step
    std_step = step
    ABRAlgo = ''
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    abr_list = list()
    current_list = list()
    count = 0
    if True:
        if bw==-1 and std==-1:
            return 'BOLA', 0.0, 0.0, 0.0
        # if key not in performance vector
        if (bw_cut, std_cut) not in pv_list.keys():
            for i in range(2, 1000, 1):
                count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
                        if (bw_, std_) in pv_list.keys():
                            current_list = current_list + pv_list[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list.keys():
                            current_list = current_list + pv_list[(bw_, std_)]
                if len(current_list)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'BOLA'
                    break
        else:
            current_list = current_list + pv_list[(bw_cut, std_cut)]
            ABRAlgo = 'BOLA'

    if len(current_list)==0:
        return 'BOLA', 0.0, 0.0, 0.0
    if max(current_list) ==-sys.maxint:
        return 'BOLA', 0.0, 0.0, 0.0
    # print >> sys.stderr, ABRAlgo, min(current_list), np.percentile(current_list,50), max(current_list), bw, std
    return ABRAlgo, min(current_list), np.percentile(current_list,50), max(current_list)  