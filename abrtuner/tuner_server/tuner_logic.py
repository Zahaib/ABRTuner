#!/usr/bin/python

import sys, os
import numpy as np
from tuner_lookup_tables import *
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial

def getUtilityBitrateDecision_dash(sessionHistory, lastest_chunkid, new_chunkid, bufferlen, margin):
  candidateBitrates = [0,1,2,3,4,5]
  index_to_bitrate = {0:300,1:750,2:1200,3:1850,4:2850,5:4300}
  BUFFER_SAFETY_MARGIN = margin
  BUFFERING_WEIGHT = -100000000.0
  BITRATE_WEIGHT = 1
  tempbitrate = -1
  tempquality = 0
  utility = -100000000.0
  #print sessionHistory, lastest_chunkid, new_chunkid
  estBufferingTime = 0.0
  est_bandwidth = estimateSmoothBandwidth_dash(sessionHistory, lastest_chunkid)
  #print est_bandwidth
  if new_chunkid > 48:
    #exit()
    return new_chunkid;
  for br in candidateBitrates:
    size = size_envivo[br][new_chunkid]
    estBufferingTime = -1*min(((float(bufferlen))*BUFFER_SAFETY_MARGIN - (float(size)*8)/(est_bandwidth*1000)),0)
    if utility < estBufferingTime * BUFFERING_WEIGHT + index_to_bitrate[br] * BITRATE_WEIGHT:
      tempbitrate = index_to_bitrate[br]
      tempquality = br
      utility = estBufferingTime * BUFFERING_WEIGHT + index_to_bitrate[br] * BITRATE_WEIGHT
    #print bufferlen,est_bandwidth,br,new_chunkid,size_envivo[br][new_chunkid],estBufferingTime
  return tempquality


# getBWFeaturesWeighted with player visible BW
def getBWFeaturesWeightedPlayerVisible(playerVisibleBW, chunk_when_last_chd_ran):
  lookbackwindow = len(playerVisibleBW) - min(51, len(playerVisibleBW) - chunk_when_last_chd_ran)
  currentstateBWArray = playerVisibleBW[lookbackwindow:]
  return np.mean(currentstateBWArray), np.std(currentstateBWArray)


def onlineCD(sessionHistory, chunk_when_last_chd, interval, playerVisibleBW):
  chd_detected = False
  chd_index = chunk_when_last_chd
  R, maxes = oncd.online_changepoint_detection(np.asanyarray(playerVisibleBW), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
  #interval = 5
  interval = min(interval, len(playerVisibleBW))
  changeArray = R[interval,interval:-1]
  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
    if v > 0.01 and i > chunk_when_last_chd:
      chd_index = i
      chd_detected = True
      break
  return chd_detected, chd_index

def getDynamicconfig_self(pv_list_hyb, bw, std, step):
  bw_step = step
  std_step = step
  ABRAlgo = ''
  bw_cut =int(float(bw)/bw_step)*bw_step
  std_cut = int(float(std)/std_step)*std_step
  abr_list = list()
  current_list_1 = list()
  current_list_2 = list()
  current_list_bb_1 = list()
  current_list_bb_2 = list()
  current_list_hyb = list()
  count = 0
  if True:
    if bw==-1 and std==-1:
      return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
    if (bw_cut, std_cut) not in pv_list_hyb.keys():
      for i in range(2, 1000, 1):
        count += 1
        for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
          for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
            if (bw_, std_) in pv_list_hyb.keys():
              current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
        for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
          for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
            if (bw_, std_) in pv_list_hyb.keys():
              current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
        for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
          for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
            if (bw_, std_) in pv_list_hyb.keys():
              current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
        if len(current_list_hyb)==0:
          continue
        else:# len(abr_list)>0 and 'BB' not in abr_list:
          ABRAlgo = 'HYB'
          #print "HYB", bw_cut, std_cut, count, sys.argv[1]
          break
    else:
      current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
      ABRAlgo = 'HYB'
  if len(current_list_hyb)==0:
    return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
  return ABRAlgo, min(current_list_hyb), np.percentile(current_list_hyb,10), max(current_list_hyb), 0,0,0,0,0,0
