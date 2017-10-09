#!/usr/bin/python

import sys, os
import numpy as np
from mpc_lookup_table_4300 import *
# from dash_syn_simulation_hyb_pen_performance_table_8600 import *
import bayesian_changepoint_detection.online_changepoint_detection as oncd
import itertools
from functools import partial


size_envivo = {0:[181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270],
1:[450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954],
2:[668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450],
3:[1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850],
4:[1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412],
5:[2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658]
}

NUM_BITRATES = 6
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
TOTAL_VIDEO_CHUNKS = 48
REBUF_PENALTY = 8.6 #4.3  # 1 sec rebuffering -> this number of Mbps
SMOOTH_PENALTY = 0.0


def getMPCDecision(bufferlen, bitrate, chunkid, future_bandwidth):
  # print bufferlen, bitrate, chunkid, CHUNKSIZE, future_bandwidth, windowSize
  windowSize = 5
  if chunkid + windowSize > TOTAL_VIDEO_CHUNKS:
    windowSize = TOTAL_VIDEO_CHUNKS - chunkid

  if windowSize < 0:
    windowSize = 0

  CHUNK_COMBO_OPTIONS = list()
  for combo in itertools.product(range(NUM_BITRATES), repeat=windowSize):
    CHUNK_COMBO_OPTIONS.append(combo)

  max_reward = -100000000
  best_combo = ()
  start_buffer = bufferlen
  for full_combo in CHUNK_COMBO_OPTIONS:
      combo = full_combo[0:windowSize]
      # print combo
      # calculate total rebuffer time for this combination (start with start_buffer and subtract
      # each download time and add 2 seconds in that order)
      curr_rebuffer_time = 0
      curr_buffer = start_buffer
      bitrate_sum = 0
      smoothness_diffs = 0
      last_quality = bitrate #VIDEO_BIT_RATE_TO_INDEX[bitrate]
      for position in range(0, len(combo)):
          chunk_quality = combo[position]
          index = chunkid + position + 1 # e.g., if last chunk is 3, then first iter is 3+0+1=4
          download_time = ((size_envivo[chunk_quality][index] * 8)/1000.)/future_bandwidth # this is Kb/Kb/s --> seconds
          if ( curr_buffer < download_time ):
              curr_rebuffer_time += (download_time - curr_buffer)
              curr_buffer = 0
          else:
              curr_buffer -= download_time
          curr_buffer += 4
          
          # linear reward
          bitrate_sum += VIDEO_BIT_RATE[chunk_quality]
          smoothness_diffs += abs(VIDEO_BIT_RATE[chunk_quality] - VIDEO_BIT_RATE[last_quality])

          last_quality = chunk_quality
      # compute reward for this combination (one reward per 5-chunk combo)
      # bitrates are in Mbits/s, rebuffer in seconds, and smoothness_diffs in Mbits/s
      
      # linear reward 
      reward = (bitrate_sum/1000.0) - (REBUF_PENALTY * curr_rebuffer_time) - (SMOOTH_PENALTY * smoothness_diffs/1000.0)
      #print combo, reward, future_bandwidth, curr_rebuffer_time
      if ( reward > max_reward ):
          max_reward = reward
          best_combo = combo
  # send data to html side (first chunk of best combo)
  bitrate = 0 # no combo had reward better than -1000000 (ERROR) so send 0
  if ( best_combo != () ): # some combo was good
      bitrate = best_combo[0]
  #print "bitrate selected: ", bitrate
  return bitrate



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
      print "change detected i = ", i, " chd_index = ", chd_index, " chunk_when_last_chd =", chunk_when_last_chd, " len = ", lenarray
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

def getDynamicconfig_mpc(pv_list_hyb, bw, std, step):
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
            return 'MPC', 0.0, 0.0, 0.0
        # if key not in performance vector
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
                if len(current_list_hyb)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'MPC'
                    break
        else:
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'MPC'

    if len(current_list_hyb)==0:
        return 'MPC', 0.0, 0.0, 0.0
    if max(current_list_hyb) ==-1.0:
        return 'MPC', 0.0, 0.0, 0.0
    return ABRAlgo, min(current_list_hyb), np.percentile(current_list_hyb,50), max(current_list_hyb)

def getPastFiveBW(chunkBWSamples, chunkid):
  past_five = list()
  start = max(chunkid - 5 + 1, 0)
  # print start, chunkid, len(sessionHistory.keys()), sessionHistory[len(sessionHistory.keys()) - 1]
  for i in range(start, chunkid + 1):
    bw_sample =  (chunkBWSamples[i] / 8) / 1000.0 # KBytes/ms or MBytes/sec
    past_five.append(bw_sample)
  return past_five

# function returns the BW needed by MPC
def getMPCBW(chunkBWSamples, bandwidthEsts, pastErrors, chunkid, discount):
  #print discount
  curr_error = 0
  if len(bandwidthEsts) > 0:
    last_chunk_bw = (chunkBWSamples[-1] / 8) / 1000.0 # KBytes/ms or MBytes/sec
    curr_error = abs(bandwidthEsts[-1] - last_chunk_bw)
  pastErrors.append(curr_error)
  past_five = getPastFiveBW(chunkBWSamples, chunkid)
  bandwidth_sum = 0
  for past_val in past_five:
      bandwidth_sum += (1/float(past_val))
  harmonic_bandwidth = 1.0/(bandwidth_sum/len(past_five))
  bandwidthEsts.append(harmonic_bandwidth)

  max_error = 0

  if discount < 0:
  #### Original code start ####
    error_pos = -5
    if ( len(pastErrors) < 5 ):
      error_pos = -len(pastErrors)
    max_error = float(max(pastErrors[error_pos:]))
    future_bandwidth = harmonic_bandwidth/(1+max_error)
  #### Original code end.. ####
  else:
    max_error = harmonic_bandwidth * (discount / 100.0)
    future_bandwidth = harmonic_bandwidth/(1+max_error)
  future_bandwidth = future_bandwidth * 8 * 1000.0 # converted to kbps 

  return future_bandwidth, bandwidthEsts, pastErrors            

