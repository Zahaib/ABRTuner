#!/usr/bin/python

import sys, os
import numpy as np
from tuner_lookup_tables import *
from dash_syn_simulation_hyb_pen_performance_table_8600 import *
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial

size_envivo = {0:[181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270],
1:[450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954],
2:[668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450],
3:[1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850],
4:[1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412],
5:[2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658]
}


def getUtilityBitrateDecision_dash(est_bandwidth, new_chunkid, bufferlen, margin):
  candidateBitrates = [0,1,2,3,4,5]
  index_to_bitrate = {0:300,1:750,2:1200,3:1850,4:2850,5:4300}
  BUFFER_SAFETY_MARGIN = margin
  #BUFFERING_WEIGHT = -100000000.0
  BUFFERING_WEIGHT = 8600
  BITRATE_WEIGHT = 1
  tempbitrate = -1
  tempquality = 0
  utility = -100000000.0
  #print sessionHistory, lastest_chunkid, new_chunkid
  estBufferingTime = 0.0
  # est_bandwidth = estimateSmoothBandwidth_dash(sessionHistory, lastest_chunkid)
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
      print "change detected i = ", i, " cutoff = ", cutoff, " chd_index = ", chd_index, " chunk_when_last_chd =", chunk_when_last_chd, " len = ", lenarray
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
  if bw > 9000:
    return 'HYB', 0.97, 0.97, 0.97, 5, 5, 5, 0.4, 0.4, 0.4
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
