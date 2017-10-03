#!/usr/bin/python

from helpers import *
from chunkMap import *
from config import *
import math
import random
import statistics
import numpy as np
import itertools
# utility function:
# pick the highest bitrate that will not introduce buffering

def getUtilityBitrateDecision_dash(sessionHistory, lastest_chunkid, new_chunkid, bufferlen, margin):
  candidateBitrates = [0,1,2,3,4]
  index_to_bitrate = {0:350,1:600,2:1000,3:2000,4:3000}
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
  if new_chunkid > 63: 
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

def getMPCDecision(bufferlen, bitrate, chunkid, CHUNKSIZE, future_bandwidth, windowSize):
  # VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
  # VIDEO_BIT_RATE_TO_INDEX = {300:0,750:1,1200:2,1850:3,2850:4,4300:5}
  # print bufferlen, bitrate, chunkid, CHUNKSIZE, future_bandwidth, windowSize
  # TOTAL_CHUNKS = 49
  if chunkid + windowSize > 48:
    windowSize = TOTAL_CHUNKS - chunkid

  if windowSize < 0:
    windowSize = 0

  CHUNK_COMBO_OPTIONS = list()
  try:
    for combo in itertools.product([0,1,2,3,4], repeat=windowSize):
      CHUNK_COMBO_OPTIONS.append(combo)
  except ValueError:
    print windowSize, chunkid, TOTAL_CHUNKS
    sys.exit()

  max_reward = -100000000
  best_combo = ()
  start_buffer = bufferlen
  #start = time.time()
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
          # print chunk_quality, download_time, future_bandwidth
          # print size_envivo[chunk_quality][index], ((size_envivo[chunk_quality][index] * 8)/1000.), future_bandwidth
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
      # print combo, reward, curr_rebuffer_time
      if ( reward > max_reward ):
          max_reward = reward
          best_combo = combo
  # send data to html side (first chunk of best combo)
  bitrate = 0 # no combo had reward better than -1000000 (ERROR) so send 0
  if ( best_combo != () ): # some combo was good
      bitrate = best_combo[0]
  return bitrate






def getUtilityBitrateDecision(bufferlen, candidateBitrates, bandwidth, chunkid, CHUNKSIZE, BUFFER_SAFETY_MARGIN, buffering_weight, sessionHistory, chunk_residue, currbitratePlaying, clock, decision_cycle, bwArray, usedBWArray, sessiontimems, oldbw, attempt_id):
  if BUFFER_SAFETY_MARGIN == -1:
    BUFFER_SAFETY_MARGIN = 0.275
  BUFFERING_WEIGHT = buffering_weight
  BITRATE_WEIGHT = 1
  BANDWIDTH_SAFETY_MARGIN = 1.0 
  ret = -1;
  candidateBitrates = sorted(candidateBitrates)
  estBufferingTime = 0
  utility = -1000000
  actualbitrate = 0
  if INDUCE_BW_ERROR:
    est_bandwidth = getTrueBW(clock, bandwidth, SIMULATION_STEP, decision_cycle, bwArray, usedBWArray, sessiontimems)
    #print clock, est_bandwidth
    error = 0.5
    max_est_bw = est_bandwidth + est_bandwidth * error
    min_est_bw = est_bandwidth - est_bandwidth * error
    est_bandwidth_r = random.uniform(min_est_bw, max_est_bw)
    #print clock, est_bandwidth, min_est_bw, max_est_bw, est_bandwidth_r
    #print clock, est_bandwidth
    #print clock + decision_cycle, est_bandwidth
    #oldbw = est_bandwidth
    bandwidth = est_bandwidth_r
  if ESTIMATED_BANDWIDTH_MODE:
    est_bandwidth = estimateSmoothBandwidth(sessionHistory, attempt_id)
    if est_bandwidth != -1:
      bandwidth = est_bandwidth
  if PS_STYLE_BANDWIDTH:
    #bandwidth = interpolateBWPrecisionServerStyle(clock, bufferlen, usedBWArray, bwArray)
    bandwidth  = estimateBWPrecisionServerStyleSessionHistory(clock, bufferlen, usedBWArray, sessionHistory, attempt_id, bwArray)
    #print clock, bandwidth
  # YUN modified
  #bandwidth = est_bandwidth
  remainingSizeOfCurrent = 0
  if CHUNK_AWARE_MODE and currbitratePlaying in sizeDict and chunkid-1 in sizeDict[currbitratePlaying]: remainingSizeOfCurrent = getRealBitrate(currbitratePlaying, chunkid-1, CHUNKSIZE)
  remainingSizeOfCurrent = remainingSizeOfCurrent*(CHUNKSIZE * (1 - chunk_residue))
  for br in candidateBitrates:
# the buffer len you will add: sum of buffer you will download plus current buffer. If current buffer is zero then the
# amount you will add is a function of bandwidth alone. If the bandwidth is zero, then the buffer you have is just the
# current value of the buffer.
    actualbitrate = br
    if CHUNK_AWARE_MODE and br in sizeDict and chunkid in sizeDict[br]: actualbitrate = getRealBitrate(br, chunkid, CHUNKSIZE) #sizeDict[br][chunkid]*8/float(CHUNKSIZE * 1000)
    if NOINTERUPT == True:
      
      estBufferingTime = -1*min(1000*((bufferlen+5)*BUFFER_SAFETY_MARGIN - (remainingSizeOfCurrent + actualbitrate * CHUNKSIZE)/float(bandwidth)),0)   
      #estBufferingTime = -1*min(1000*(bufferlen*BUFFER_SAFETY_MARGIN - actualbitrate * CHUNKSIZE/float(bandwidth)),0)   
      #bufferlengthMs = bufferlen - actualbitrate * CHUNKSIZE/float(bandwidth) + CHUNKSIZE
      #estBufferingTime = 1000 * max(actualbitrate * CHUNKSIZE/float(bandwidth) - bufferlengthMs * BUFFER_SAFETY_MARGIN, 0) # all computation are i
    elif ALLINTERUPT == True:
      bufferlengthMs = bufferlen - actualbitrate * CHUNKSIZE/float(bandwidth) + CHUNKSIZE
      estBufferingTime = 1000 * max(actualbitrate * CHUNKSIZE/float(bandwidth) - bufferlengthMs * BUFFER_SAFETY_MARGIN, 0) # all computation are i
    elif SMARTINTERUPT == True: # still there is some corner case
      if br == currbitratePlaying:
        bufferlengthMs = bufferlen - actualbitrate * (CHUNKSIZE * (1 - chunk_residue))/float(bandwidth) + CHUNKSIZE
        estBufferingTime = 1000 * max(actualbitrate * (CHUNKSIZE * (1 - chunk_residue))/float(bandwidth) - bufferlengthMs * BUFFER_SAFETY_MARGIN, 0) # units: milli-sec
      else:
        estBufferingTime = -1*min(1000*(bufferlen*BUFFER_SAFETY_MARGIN - actualbitrate * CHUNKSIZE/float(bandwidth)),0)   
        #bufferlengthMs = bufferlen - actualbitrate * CHUNKSIZE/float(bandwidth) + CHUNKSIZE
        #estBufferingTime = 1000 * max(actualbitrate * CHUNKSIZE/float(bandwidth) - bufferlengthMs * BUFFER_SAFETY_MARGIN, 0) # all computation are in milli seconds
    #print br, remainingSizeOfCurrent, CHUNKSIZE*actualbitrate, bufferlen, bandwidth, estBufferingTime, estBufferingTime * BUFFERING_WEIGHT + br * BITRATE_WEIGHT 
    if utility < estBufferingTime * BUFFERING_WEIGHT + br * BITRATE_WEIGHT: # and br * BANDWIDTH_SAFETY_MARGIN < bandwidth:
      ret = br
      utility = estBufferingTime * BUFFERING_WEIGHT + br * BITRATE_WEIGHT
  # extremely bad bandwidth case
  if ret == -1:
    ret = candidateBitrates[0]
  return ret

def shouldSwitch(oldABR, ABRChoice, br, chunk_residue, bufferlen, chunkid, sessionHistory, attempt_id, delay, CHUNKSIZE):
  if oldABR == ABRChoice:
    return True
  if CHUNK_AWARE_MODE and br in sizeDict and chunkid in sizeDict[br]: 
    br = getRealBitrate(br, chunkid, CHUNKSIZE)

  bandwidth = estimateSmoothBandwidth(sessionHistory, attempt_id)
  if br * (CHUNKSIZE * (1 - chunk_residue)) / float(bandwidth) < 0.85 * bufferlen + delay / 1000.0:
    return False

  return True  

def estimateSmoothBandwidth_dash(sessionHistory, last_finished_chunkid):
  if len(sessionHistory)==1:
    return 0
  window = 5
  window_start = -1
  window_end = last_finished_chunkid
  cnt=0
  tmpSum = 0.0
  tmpTime = 0.0
  if last_finished_chunkid < 5:
    window_start = 0
  else:
    window_start = last_finished_chunkid+1 - 5

  #print window_start, window_end
  for i in range(window_start, window_end+1):
    tmpSum += float(sessionHistory[i][2])
    tmpTime += float((sessionHistory[i][1] - sessionHistory[i][0]))
  return tmpSum/tmpTime  

def estimateSTD_dash(sessionHistory, last_finished_chunkid):
  if len(sessionHistory)==1:
    return 0
  window = 5
  window_start = -1
  window_end = last_finished_chunkid
  cnt=0
  tmpSum = 0.0
  tmpTime = 0.0
  if last_finished_chunkid < 5:
    window_start = 0
  else:
    window_start = last_finished_chunkid+1 - 5

  #print window_start, window_end
  bw = []
  for i in range(window_start, window_end+1):
    bw.append(float(sessionHistory[i][2])/float((sessionHistory[i][1] - sessionHistory[i][0])))
  if len(bw)==1: return 0
  #print bw
  return np.std(bw, ddof=1)


# function calculates the smoothed bandwidth given the sessionHistory, chunkid
def estimateSmoothBandwidth(sessionHistory, chunkid):
  ret = -1
  if chunkid == 0:
    return ret
  #print sessionHistory
  #print chunkid 
  lookbackWindow = 5
  start = chunkid - 1
  end = max(start - lookbackWindow, -1)
  bw = num = 0
  for i in range(start, end, -1):
    if sessionHistory[i][-1]==False:
      continue
    chunk_start = sessionHistory[i][0]
    chunk_end = sessionHistory[i][1]
    kilobits = sessionHistory[i][2]
    if kilobits == 0.0:
      continue
    bw += kilobits / ((chunk_end - chunk_start) / 1000.0)
    num += 1
  ret = bw / num
  return ret

#function returns smooth bandwidth using the bandwidth logged at every 100msec
def estimateBWFromPlayerVisibleBW(playerVisibleBW, chunk_when_last_chd_ran):
  lookbackwindow = len(playerVisibleBW) - min(51, len(playerVisibleBW) - chunk_when_last_chd_ran)
  bw_since_cp = playerVisibleBW[lookbackwindow:]
  ret = np.mean(bw_since_cp)
  #print ret, chunk_when_last_chd_ran
  return ret


# function estimates the bandwidth given the bufferlen and the previous chunks which have been downloaded
def estimateBandwidth(bufferlen, sessionHistory, chunkid):
  ret = -1
  if chunkid == 0:
    return ret
  elif chunkid == 1:
    return calcBandwidth(sessionHistory, 0)
  
  if bufferlen >= 10.0:
    ret = calcBandwidth(sessionHistory, chunkid - 1)
  else:
    bw1 = calcBandwidth(sessionHistory, chunkid - 1)
    bw2 = calcBandwidth(sessionHistory, chunkid - 2)
    ret = min(bw1, bw2)
  return ret

# function to calculate the bandwidth given the chunkid and sessionHistory
def calcBandwidth(sessionHistory, chunkid):
  chunk_start = sessionHistory[chunkid][0]
  chunk_end = sessionHistory[chunkid][1]
  kilobits = sessionHistory[chunkid][2]
  ret = kilobits / ((chunk_end - chunk_start) / 1000.0)
  return ret

# a mathematical function shaping the behaviour of the ABR
def isWithinBandwidth(br, bw):
  exp = 4.17989 * math.pow(10, -22) * math.pow(br, 6) - 1.19444* math.pow(10,-17) * math.pow(br, 5) + 1.25648 * math.pow(10, -13) * math.pow(br, 4) - 6.28056 * math.pow(10, -10) * math.pow(br, 3) + 1.57631 * math.pow(10, -6) * math.pow(br, 2) - 0.00185333 * br + 1.73095  
  if math.pow(br, exp) < bw:
    return True
  return False

#http://www.wolframalpha.com/input/?i=interpolate+%5B(1000,+0.94),+(2000,+0.96),+(3000,+0.98),+(4000,+0.98),+(5000,+1.05),+(5500,1.13),+(6000,+1.16)
#iteration7
#  exp = 4.17989 * math.pow(10, -22) * math.pow(br, 6) - 1.19444* math.pow(10,-17) * math.pow(br, 5) + 1.25648 * math.pow(10, -13) * math.pow(br, 4) - 6.28056 * math.pow(10, -10) * math.pow(br, 3) + 1.57631 * math.pow(10, -6) * math.pow(br, 2) - 0.00185333 * br + 1.73095

# function returns the bitrate decision given the bufferlen and bandwidth at the heartbeat interval
def getUtilityBitrateDecisionBasic(bufferlen, bitrates, bandwidth, chunkid, CHUNKSIZE):
  WEIGHT = 0
  ret = -1;
  bitrates = sorted(bitrates)
  if bufferlen >= 0 and bufferlen <= 15:
    WEIGHT = 1.15 #1.25 #3 #5 #1.5
  elif bufferlen > 15 and bufferlen <= 35:
    WEIGHT = 0.75 #0.85 #2 #4 #1
  elif bufferlen > 35:
    WEIGHT = 0.5 #0.75 #1 #3 # 0.75

  for br in bitrates:
    if br * WEIGHT <= bandwidth:
      ret = br

  # special case: bandwidth is extremely bad such that no suitable bitrate could be assigned then just return the lowest available bitrate
  if ret == -1:
    ret = bitrates[0]
  return ret

# function returns the bitrate decision given the bufferlen using BBA0 in T.Y paper.
# conf is a dict storing any configuration related stuff, for this case, conf = {'maxbuflen':120, 'r': 45, 'maxRPct':0.9}

def getBitrateBBA0(bufferlen, candidateBitRate, conf):
  maxbuflen = conf['maxbuflen']
  reservoir = conf['r']
  maxRPct = conf['maxRPct']
  # print maxbuflen, reservoir, maxRPct, int(maxbuflen * maxRPct)
  assert (maxbuflen > 30), "too small max player buffer length"
  assert (reservoir < maxbuflen), "initial reservoir is not smaller than max player buffer length"
  assert (maxRPct < 1)
  assert (bufferlen <= maxbuflen), "bufferlen greater than maxbufferlen"

  upperReservoir = int(maxbuflen * maxRPct)

  R_min = candidateBitRate[0]
  R_max = candidateBitRate[-1]

  #print "Rmin=%d, Rmax=%d, reservoir=%d, upperReservoir=%d " % (R_min, R_max, reservoir, upperReservoir)

  # if bufferlen is small, return R_min
  if (bufferlen <=reservoir):
    return R_min
  # if bufferlen is close to full, return R_max
  if (bufferlen >=upperReservoir):
    return R_max

  # linear interpolation of the bufferlen vs bit-rate
  RGap = R_max - R_min
  BGap = upperReservoir - reservoir

  assert (RGap > 100), "R_max and R_min need at least 100kbps gap"
  assert (BGap > 10), "upper reservoir and reservoir need at least 10s gap " + str(reservoir) + " " + str(upperReservoir) + " " + str(maxRPct)

  # based on the slope calc. ideal bit-rate
  RIdeal = R_min + int((bufferlen - reservoir) * RGap * 1.0 / (BGap*1.0))

  #print "RGap = %d, BGap=%d, RIdeal=%d" % (RGap, BGap, RIdeal)

  # find the max rate that is lower than then ideal one.
  for idx in range(len(candidateBitRate)):
    if RIdeal < candidateBitRate[idx]:
      return candidateBitRate[idx-1]


# function returns the bitrate decision given the bufferlen using BBA2 in T.Y paper.
def getBitrateBBA2(bufferlen, candidateBitRate, conf, chunkid, CHUNKSIZE, bitrate, bandwidth, blen_decrease):
  maxbuflen = conf['maxbuflen']
  reservoir = conf['r']
  maxRPct = conf['maxRPct']
  X = conf['xLookahead']
  assert (maxbuflen > 30), "too small max player buffer length"
  assert (reservoir < maxbuflen), "initial reservoir is not smaller than max player buffer length"
  assert (maxRPct < 1)
  assert (bufferlen <= maxbuflen), "bufferlen greater than maxbufferlen"

  # calculate the fallback buffer if the dynamic calculation fails
  upperReservoir = int(maxbuflen * maxRPct)

  R_min = candidateBitRate[0]
  R_max = candidateBitRate[-1]
  # get the dynamic value of the reservoir
  reservoir = dynamicReservoir(bandwidth, chunkid, X, reservoir, CHUNKSIZE, bitrate, candidateBitRate)
  # if bufferlen is small, return R_min
  if (bufferlen <=reservoir):
    return R_min
  # if bufferlen is close to full, return R_max
  if (bufferlen >=upperReservoir):
    return R_max

  # linear interpolation of the bufferlen vs bit-rate
  RGap = R_max - R_min
  BGap = upperReservoir - reservoir

  assert (RGap > 100), "R_max and R_min need at least 100kbps gap"
  assert (BGap > 30), "upper reservoir and reservoir need at least 30s gap"

  # based on the slope calc. ideal bit-rate
  RIdeal = R_min + int((bufferlen - reservoir) * RGap * 1.0 / (BGap*1.0))

  #print "RGap = %d, BGap=%d, RIdeal=%d" % (RGap, BGap, RIdeal)
  interpolatedCandidate = 0
  # find the max rate that is lower than then ideal one.
  for idx in range(len(candidateBitRate)):
    if RIdeal < sizeDict[candidateBitRate[idx]][chunkid]:
      interpolatedCandidate = candidateBitRate[idx-1]
      break
  
  startupCandidate = -1
  threshold = 0.0
  if not blen_decrease:
    if bufferlen >= 0 and bufferlen < int(upperReservoir / 8):
      threshold = 8.0
    elif bufferlen >= int(upperReservoir / 8) and bufferlen < int(upperReservoir / 4):
      threshold = 4.0
    elif bufferlen >= int(upperReservoir / 4) and bufferlen < int(upperReservoir / 1):
      threshold = 2.0
    else:
      return interpolatedCandidate

  if chunkid < len(sizeDict[bitrate]) and CHUNKSIZE / (((sizeDict[bitrate][chunkid] / 1000) * CHUNKSIZE) / float(bandwidth)) > threshold:
    newIndex = candidateBitRate.index(bitrate) + 1
  # calculate the fallback buffer if the dynamic calculation fails
  upperReservoir = int(maxbuflen * maxRPct)

  R_min = candidateBitRate[0]
  R_max = candidateBitRate[-1]
  # get the dynamic value of the reservoir
  reservoir = dynamicReservoir(bandwidth, chunkid, X, reservoir, CHUNKSIZE, bitrate, candidateBitRate)
  #print conf['r'], reservoir
  # if bufferlen is small, return R_min
  if (bufferlen <=reservoir):
    return R_min
  # if bufferlen is close to full, return R_max
  if (bufferlen >=upperReservoir):
    return R_max

  # linear interpolation of the bufferlen vs bit-rate
  RGap = R_max - R_min
  BGap = upperReservoir - reservoir

  assert (RGap > 100), "R_max and R_min need at least 100kbps gap"
  assert (BGap > 30), "upper reservoir and reservoir need at least 30s gap"

  # based on the slope calc. ideal bit-rate
  RIdeal = R_min + int((bufferlen - reservoir) * RGap * 1.0 / (BGap*1.0))

  #print "RGap = %d, BGap=%d, RIdeal=%d" % (RGap, BGap, RIdeal)

  # find the max rate that is lower than then ideal one.
  for idx in range(len(candidateBitRate)):
    if RIdeal < sizeDict[candidateBitRate[idx]][chunkid]:
      return candidateBitRate[idx-1]


# function returns the dynamic value of the reservoir
def dynamicReservoir(bw, chunkid, X, reservoir, CHUNKSIZE, bitrate, candidateBitRate):
  #print chunkid
  if chunkid > len(sizeDict[candidateBitRate[0]]) - X / CHUNKSIZE:
    return reservoir
  bufAdded = 0
  timeAccumulated = 0.0
  while chunkid < len(sizeDict[bitrate]) and ((sizeDict[bitrate][chunkid] / 1000.0) * CHUNKSIZE) / float(bw) + timeAccumulated < X:
    timeAccumulated += ((sizeDict[bitrate][chunkid] / 1000.0) * CHUNKSIZE) / float(bw)
#    print timeAccumulated
    bufAdded += CHUNKSIZE
    chunkid += 1
  #print "bufAdded: " + str(bufAdded) + " X: " + str(X)
  ret = max(X - bufAdded, 2)
  #print "bufAdded: " + str(bufAdded) + " X: " + str(X) + " ret: " + str(ret)
  return ret

# function returns the bitrate decision only on the basis of bandwidth
def getBitrateDecisionBandwidth(bufferlen, bitrates, bandwidth):
  BANDWIDTH_SAFETY_MARGIN = 1.2
  ret = -1;
  for br in bitrates:
    if br * BANDWIDTH_SAFETY_MARGIN <= bandwidth:
      ret = br

  # special case: bandwidth is extremely bad such that no suitable bitrate could be assigned then just return the lowest available bitrate
  if ret == -1:
    ret = bitrates[0]
  return ret


# function return the bitrate decision as a weighted average: a * BW + (1 - a)Avg(nSamples)
def getBitrateWeightedBandwidth(bitrates, BW, nSamples, weight):
  A = weight
  avg_nSamples = 0.0
  count = 0
  ret = -1
  weighted_BW = -1
  if nSamples.count(0) != 5:
    for s in nSamples:
      if s == 0:
        continue
      avg_nSamples += s
      count += 1
    avg_nSamples /= count
    weighted_BW = int(A * avg_nSamples + (1 - A) * BW)
  else:
    weighted_BW = BW

  # print BW, weighted_BW, avg_nSamples

  for br in bitrates:
    if br <= weighted_BW:
      ret = br

  if ret == -1:
    ret = bitrates[0]

  return ret


