# LIST OF HELPER FUNCTIONS
import numpy as np
import random, sys
import traceback
import inspect
from algorithms import *
from config import *
from chunkMap import *
#from low_bw_syth_no_abort_bugfix1224_performance_vector import *
from dash_syn_simulation_hyb_performance_table import *
from mpc_performancetable_syn import *
from simulation_performance_vector import *
from dash_syn_simulation_mpc_pen_performance_table_4300 import *
from dash_syn_simulation_mpc_pen_performance_table_4300_fix1010 import *
from dash_syn_bola_gamma_table_min_10_target_30_simbufferadjust import *
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial
#from __future__ import print_function
import timeit

def onlineCD(sessionHistory, chunk_when_last_chd, interval, playerVisibleBW):
  chd_detected = False
  chd_index = chunk_when_last_chd
  trimThresh = 1000
  lenarray = len(playerVisibleBW)
  playerVisibleBW, cutoff = trimPlayerVisibleBW(playerVisibleBW, trimThresh)
  R, maxes = oncd.online_changepoint_detection(np.asanyarray(playerVisibleBW), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
  interval = min(interval, len(playerVisibleBW))
  changeArray = R[interval,interval:-1]
  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
    if v > 0.01 and i + cutoff > chunk_when_last_chd and not (i == 0 and chunk_when_last_chd > -1):
      chd_index = i + cutoff
      chd_detected = True
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


# function returns the most dominant bitrate played, if two are dominant it returns the bigger of two
def getDominant(dominantBitrate):
  ret = 0
  maxFreq = -sys.maxint
  for b in sorted(dominantBitrate.keys()):
    if maxFreq <= dominantBitrate[b]:
      ret = b
      maxFreq = dominantBitrate[b]
  return ret, maxFreq, sum(dominantBitrate.values())


# function returns the initial bandwidth using the jointime of the session
def printPercentile(target):
  for i in range (0,101):
    print str(i/float(100)) + "\t" + str(np.percentile(target, i))
    
def getInitBWCalculated(init_br, jointime, chunksize):
  return int(init_br * chunksize / float(jointime) * 1000)

def getInitBW(bwArray):
  return bwArray[0][1]

# function generates the final stats
def generateStats(AVG_SESSION_BITRATE, BUFFTIME, PLAYTIME, bufftimems, playtimems):
  AVG_SESSION_BITRATE = (8*AVG_SESSION_BITRATE/float(PLAYTIME)/1000) # add float
  REBUF_RATIO = round(BUFFTIME/float(BUFFTIME + PLAYTIME),3)
  rebuf_groundtruth = round(bufftimems/float(bufftimems + playtimems),3)
  
  return AVG_SESSION_BITRATE, REBUF_RATIO, rebuf_groundtruth

# update session history because a chunk just finished downloading
def updateSessionHistory(bitrate, clock, chunkid, CHUNKSIZE, sessionHistory, first_chunk, time_residue, attempt_id, completed, chunk_residue):
  #print "update sessionshistory"
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid] * 8
  
  time_residue = max(0, time_residue - SIMULATION_STEP)

  if first_chunk:
    size = bitrate * CHUNKSIZE * (1 - 1.25/5.0)
  elif completed == False:
    size = bitrate * CHUNKSIZE * chunk_residue
  else:
    size = bitrate * CHUNKSIZE
  sessionHistory[attempt_id].append(clock)
  sessionHistory[attempt_id].append(bitrate)
  sessionHistory[attempt_id].append(chunkid)
  sessionHistory[attempt_id].append(completed)
  sessionHistory[attempt_id + 1] = [clock  + time_residue]
  return sessionHistory

# getBWFeaturesWeighted with player visible BW
def getBWFeaturesWeightedPlayerVisible(playerVisibleBW, chunk_when_last_chd_ran):
  lookbackwindow = len(playerVisibleBW) - min(51, len(playerVisibleBW) - chunk_when_last_chd_ran)
  currentstateBWArray = playerVisibleBW[lookbackwindow:]
  return np.mean(currentstateBWArray), np.std(currentstateBWArray)

# inserts the jointime and bandwidth as an additional timestamp and bandwidth  
def insertJoinTimeandInitBW(ts, bw, bwArray):
  t = []
  t.append(ts)
  b = []
  b.append(bw)
  row = zip(t,b)
  bwArray = row + bwArray
  return bwArray

# funtion returns the time it will take to download a single chunk whether downloading a new chunk or finishing up a partial chunk
def timeToDownloadSingleChunk(CHUNKSIZE, bitrate, BW, chunk_residue, chunkid):
  if BW == 0:
    return 1000000 # one thousand seconds, very large number
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid] * 8
  return round((bitrate  - bitrate  * chunk_residue)/float(BW),2)

# function returns the remaining time to finish the download of the chunk
def timeRemainingFinishChunk(chunk_residue, bitrate, bandwidth, chunkid, chunksize):
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    bitrate = size_envivo[bitrate][chunkid]*8

  #bandwidth = bandwidth / 2.0
  ret = (1 - chunk_residue) * ((bitrate ) / float(bandwidth))
  return ret

# function returns the past 5 BW samples
def getPastFiveBW(sessionHistory, chunkid):
  past_five = list()
  start = max(chunkid - 5 + 1, 0)
  for i in range(start, chunkid + 1):
    bw_sample = (sessionHistory[i][2] / 8) / (float(sessionHistory[i][1] - sessionHistory[i][0])) / 1000.0 # KBytes/ms or MBytes/sec
    past_five.append(bw_sample)
  return past_five

# function returns the BW needed by MPC
def getMPCBW(sessionHistory, bandwidthEsts, pastErrors, chunkid, discount):
  curr_error = 0
  if len(bandwidthEsts) > 0:
    last_chunk_bw = (sessionHistory[chunkid][2] / 8) / float(sessionHistory[chunkid][1] - sessionHistory[chunkid][0]) / 1000.0 # KBytes/ms or MBytes/sec
    curr_error = abs(bandwidthEsts[-1] - last_chunk_bw) / float(last_chunk_bw)
  pastErrors.append(curr_error)
  past_five = getPastFiveBW(sessionHistory, chunkid)
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
    max_error = discount / 100.0
    future_bandwidth = harmonic_bandwidth/(1+max_error)
  future_bandwidth = future_bandwidth * 8 * 1000.0 # converted to kbps 

  return future_bandwidth, max_error, bandwidthEsts, pastErrors

def chunksDownloaded(s, param, time_prev):
  # declaring local variables which do not need to be updated in the state
  chunk_count = 0.0
  time_residue_this_interval = 0.0
  completion_time_stamps = []
  bitrate = s.BR
  bitrate_at_interval_start = bitrate
  bitrate_at_interval_end = bitrate
  next_chunk_bitrate = -2
  time_curr, chunkid, bandwidth, attempt_id = s.CLOCK, s.CHUNKS_DOWNLOADED, s.BW, s.ATTEMPT_ID

  if CHUNK_AWARE_MODE:
    bitrate = getRealBitrate(bitrate_at_interval_start, chunkid, CHUNKSIZE)
  # first add the residue time from the previous interval
  time_prev += s.chunk_sched_time_delay
  time2FinishResidueChunk = (((1 - s.chunk_residue) * bitrate)/float(bandwidth))
  time2DownloadFullChunk = (bitrate /float(bandwidth))
  # if there is a residue chunk from the last interval, then handle it first
  if s.chunk_residue > 0 and time_prev + time2FinishResidueChunk <= time_curr:
    chunk_count +=  1 - s.chunk_residue
    completionTime = time_prev + time2FinishResidueChunk
    completion_time_stamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, s.BLEN)
    time_prev += time2FinishResidueChunk + nextChunkDelay
    ## update sessionHistory here, since a chunk finished download
    s.sessionHistory = updateSessionHistory(bitrate_at_interval_start, completionTime, chunkid, CHUNKSIZE, s.sessionHistory, s.first_chunk,
                                              nextChunkDelay, attempt_id, True, s.chunk_residue)
    if TRUE_AVG_BITRATE:
      # true bitrate using chunksize
      s.AVG_SESSION_BITRATE+=size_envivo[bitrate_at_interval_start][chunkid]
    else:
      # label bitrate
      s.AVG_SESSION_BITRATE+=(VIDEO_BIT_RATE[bitrate_at_interval_start] * CHUNKSIZE * 1000.0) / 8.0

    est_bandwidth = est_std = 0
    # if online change point detection is enabled, run the change detection and find the configuration
    if ONCD:
      # CD_INTERVAL is window size for change detection, defined in config
      ch_detected, ch_index = onlineCD(s.sessionHistory, s.chunk_when_last_chd_ran, CD_INTERVAL, s.playerVisibleBW)
      est_bandwidth, est_std = getBWFeaturesWeightedPlayerVisible(s.playerVisibleBW, ch_index)
      if ch_detected:
        s.chunk_when_last_chd_ran = ch_index
        s.gradual_transition = nsteps
        if HYB_ABR:
          dict_name_backup = "dash_syth_hyb_table_"+str(minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, p1_min, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_self(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = p1_min
        elif MPC_ABR:
          dict_name_backup = "mpc_dash_syth_hyb_pen_table_4300_fix1010_"+str(minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, disc_min, disc_median, disc_max = getDynamicconfig_mpc(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = disc_median
        elif BOLA_ABR:
          dict_name_backup = "dash_syth_bola_gamma_table_"+str(minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, bola_gp_min, bola_gp_median, bola_gp_max = getDynamicconfig_bola(performance_t, est_bandwidth, est_std, s.minCellSize)
          param = bola_gp_max

    active_abr = ""
    if MPC_ABR:
      future_bandwidth, s.max_error, s.bandwidthEsts, s.pastErrors = getMPCBW(s.sessionHistory, s.bandwidthEsts, s.pastErrors, chunkid, param)
      bitrateMPC = getMPCDecision(s.BLEN, bitrate_at_interval_start, chunkid, CHUNKSIZE, future_bandwidth, s.windowSize)
      bitrate_at_interval_end = bitrateMPC
      active_abr = "MPC"
    elif HYB_ABR:
      bitrateDASH = getUtilityBitrateDecision_dash(s.sessionHistory, chunkid, chunkid+1, s.BLEN+CHUNKSIZE, param)
      bitrate_at_interval_end = bitrateDASH
      active_abr = "HYB"
    elif BOLA_ABR:
      bitrateBOLA = getBOLADecision(s.BLEN + CHUNKSIZE, param, s.bola_vp)
      bitrate_at_interval_end = bitrateBOLA
      active_abr = "BOLA"

    s.change_magnitude += abs(VIDEO_BIT_RATE[bitrate_at_interval_end] - VIDEO_BIT_RATE[bitrate_at_interval_start])
    chunkid+=1

    # Selecting the bitrate after adding the delay.
    s.configsUsed.append((time_curr/1000.0, active_abr, bandwidth, int(est_bandwidth), int(est_std), param, round(s.chunk_residue,2), round(s.BLEN,2), chunkid-1, bitrate_at_interval_end, round(s.BUFFTIME,2)))
    # residue chunk is complete so now move to next chunkid and get the actual bitrate of the next chunk
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrate_at_interval_end, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, s.usedBWArray, s.bwArray),0.01)
    attempt_id += 1
    time2DownloadFullChunk = (bitrate /float(bandwidth))
     
  # loop untill chunks can be downloaded in the interval, after each download add random delay
  while time_prev + time2DownloadFullChunk <= time_curr:
    chunk_count += 1
    completionTime = time_prev + time2DownloadFullChunk
    completion_time_stamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, s.BLEN)
    time_prev += time2DownloadFullChunk + nextChunkDelay
    ## update sessionHistory here, since a chunk finished download
    s.sessionHistory = updateSessionHistory(bitrate_at_interval_end, completionTime, chunkid, CHUNKSIZE, s.sessionHistory, s.first_chunk,
                                              nextChunkDelay, attempt_id, True, s.chunk_residue)
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrate_at_interval_end, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, s.usedBWArray, s.bwArray),0.01)
    chunkid += 1
    attempt_id += 1
    time2DownloadFullChunk = (bitrate /float(bandwidth))
  # if there is still some time left, download the partial chunk  
  if time_prev < time_curr:
    chunk_count += bandwidth/(float(bitrate)) * (time_curr - time_prev)
  # if the delay was enough to make time_prev greater than time_curr then we need to transfer over the remaining delay to next interval
  if time_prev >= time_curr:
    time_residue_this_interval = time_prev - time_curr
  s.numChunks = chunk_count
  s.chunk_sched_time_delay = time_residue_this_interval
  s.BR = bitrate_at_interval_end
  if bitrate_at_interval_start != bitrate_at_interval_end:
    s.oldBR = bitrate_at_interval_start
  return s, param


# function returns the number of chunks downloaded during the heartbeat interval and uses delay
#def chunksDownloaded(configsUsed, time_prev, time_curr, bitrate, bandwidth, chunkid, CHUNKSIZE, chunk_residue, usedBWArray, bwArray, time_residue, BLEN, sessionHistory, first_chunk, attempt_id,PLAYTIME,AVG_SESSION_BITRATE, minCellSize, BUFFTIME, playerVisibleBW, chunk_when_last_chd_ran, p1_min, gradual_transition, additive_inc, bandwidthEsts, pastErrors, windowSize, change_magnitude, discount, max_error, bola_gp, bola_vp, buffer_target_s):
#  chunkCount = 0.0
#  time_residue_thisInterval = 0.0
#  completionTimeStamps = []
#  bitrateAtIntervalStart = bitrate
#  next_chunk_bitrate = -2
#  if bandwidth == 0.0:
#    return chunkCount, completionTimeStamps, time_residue_thisInterval
#
#  if CHUNK_AWARE_MODE:
#    bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
#  # first add the residue time from the previous interval
#  time_prev += time_residue
#  time2FinishResidueChunk = (((1 - chunk_residue) * bitrate)/float(bandwidth))
#  time2DownloadFullChunk = (bitrate /float(bandwidth))
#  # if there is a residue chunk from the last interval, then handle it first
#  if chunk_residue > 0 and time_prev + time2FinishResidueChunk <= time_curr:
#    chunkCount +=  1 - chunk_residue
#    completionTime = time_prev + time2FinishResidueChunk
#    completionTimeStamps.append(completionTime)
#    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN)
#    time_prev += time2FinishResidueChunk + nextChunkDelay
#    ## update sessionHistory here, since a chunk finished download
#    sessionHistory = updateSessionHistory(bitrateAtIntervalStart, completionTime, chunkid, CHUNKSIZE, sessionHistory, first_chunk,
#                                              nextChunkDelay, attempt_id, True, chunk_residue)
#    if TRUE_AVG_BITRATE:
#      # true bitrate using chunksize
#      AVG_SESSION_BITRATE+=size_envivo[bitrateAtIntervalStart][chunkid]
#    else:
#      # label bitrate
#      AVG_SESSION_BITRATE+=(VIDEO_BIT_RATE[bitrateAtIntervalStart] * CHUNKSIZE * 1000.0) / 8.0
#
#    est_bandwidth = est_std = 0
#    # just a hacky way to adjust ONCD for time series experiments
#    if discount < 0:
#      config.ONCD = True
#
#    if ONCD:
#      CDinterval = 5
#      ch_detected, ch_index = onlineCD(sessionHistory, chunk_when_last_chd_ran, CDinterval, playerVisibleBW)
#      est_bandwidth, est_std = getBWFeaturesWeightedPlayerVisible(playerVisibleBW, ch_index)
#      nsteps = 2.0
#      p1_min_new = 0.0
#      if ch_detected:
#        chunk_when_last_chd_ran = ch_index
#        gradual_transition = nsteps
#        #print time_curr/1000.0,est_bandwidth, est_std, chunk_when_last_chd_ran
#        if HYB_ABR:
#          dict_name_backup = "dash_syth_hyb_table_"+str(minCellSize)
#          performance_t = (globals()[dict_name_backup])
#          ABRChoice, p1_min_new, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_self(performance_t, est_bandwidth, est_std, minCellSize)
#
#          additive_inc = (p1_min_new - p1_min) / nsteps
#          if gradual_transition > 0:
#            p1_min += additive_inc
#            gradual_transition -= 1
#        elif MPC_ABR:
#          dict_name_backup = "mpc_dash_syth_hyb_pen_table_4300_fix1010_"+str(minCellSize)
#          performance_t = (globals()[dict_name_backup])
#          ABRChoice, disc_min, disc_median, disc_max = getDynamicconfig_mpc(performance_t, est_bandwidth, est_std, minCellSize)
#          discount = disc_median
#        elif BOLA_ABR:
#          dict_name_backup = "dash_syth_bola_gamma_table_"+str(minCellSize)
#          performance_t = (globals()[dict_name_backup])
#          ABRChoice, bola_gp_min, bola_gp_median, bola_gp_max = getDynamicconfig_bola(performance_t, est_bandwidth, est_std, minCellSize)
#          bola_gp = bola_gp_max
#
#    
#    ######## MPC code
#    future_bandwidth, max_error, bandwidthEsts, pastErrors = getMPCBW(sessionHistory, bandwidthEsts, pastErrors, chunkid, discount)
#    bitrateMPC = getMPCDecision(BLEN, bitrateAtIntervalStart, chunkid, CHUNKSIZE, future_bandwidth, windowSize)
#    ######## MPC code
#    bitrateBOLA = getBOLADecision(BLEN + CHUNKSIZE, bola_gp, bola_vp)
#    # TODO
#    # Do We need to select bitrate before or after the delay??
#    bitrateDASH = getUtilityBitrateDecision_dash(sessionHistory, chunkid, chunkid+1, BLEN+CHUNKSIZE, p1_min)
#    chunkid+=1
#    
#
#    ############ MPC bitrate ############
#    change_magnitude += abs(VIDEO_BIT_RATE[bitrateMPC] - VIDEO_BIT_RATE[bitrateAtIntervalStart])
#    active_abr = ""
#    if MPC_ABR:
#      bitrateAtIntervalStart = bitrateMPC
#      active_abr = "MPC"
#    elif HYB_ABR:
#      bitrateAtIntervalStart = bitrateDASH
#      active_abr = "HYB"
#    elif BOLA_ABR:
#      bitrateAtIntervalStart = bitrateBOLA
#      active_abr = "BOLA"
#
#    ############ MPC bitrate ############
#
#    configsUsed.append((time_curr/1000.0, active_abr, bandwidth, int(est_bandwidth), int(est_std), discount, round(chunk_residue,2), round(BLEN,2), chunkid-1, bitrateAtIntervalStart, round(BUFFTIME,2)))
#    # residue chunk is complete so now move to next chunkid and get the actual bitrate of the next chunk
#    if CHUNK_AWARE_MODE:
#      bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
#    bandwidth = max(interpolateBWInterval(time_prev, usedBWArray, bwArray),0.01)
#    attempt_id += 1
#    time2DownloadFullChunk = (bitrate /float(bandwidth))
#     
#  # loop untill chunks can be downloaded in the interval, after each download add random delay
#  while time_prev + time2DownloadFullChunk <= time_curr:
#    chunkCount += 1
#    completionTime = time_prev + time2DownloadFullChunk
#    completionTimeStamps.append(completionTime)
#    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN)
#    time_prev += time2DownloadFullChunk + nextChunkDelay
#    ## update sessionHistory here, since a chunk finished download
#    sessionHistory = updateSessionHistory(bitrateAtIntervalStart, completionTime, chunkid, CHUNKSIZE, sessionHistory, first_chunk,
#                                              nextChunkDelay, attempt_id, True, chunk_residue)
#    if CHUNK_AWARE_MODE:
#      bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
#    bandwidth = max(interpolateBWInterval(time_prev, usedBWArray, bwArray),0.01)
#    chunkid += 1
#    attempt_id += 1
#    time2DownloadFullChunk = (bitrate /float(bandwidth))
#  # if there is still some time left, download the partial chunk  
#  if time_prev < time_curr:
#    chunkCount += bandwidth/(float(bitrate)) * (time_curr - time_prev)
#  # if the delay was enough to make time_prev greater than time_curr then we need to transfer over the remaining delay to next interval
#  if time_prev >= time_curr:
#    time_residue_thisInterval = time_prev - time_curr
#  return configsUsed, \
#         chunkCount, \
#         completionTimeStamps, \
#         time_residue_thisInterval, \
#         sessionHistory,\
#         bitrateAtIntervalStart,\
#         AVG_SESSION_BITRATE, \
#         chunk_when_last_chd_ran, \
#         p1_min, \
#         gradual_transition, \
#         additive_inc, \
#         bandwidthEsts, \
#         pastErrors, \
#         change_magnitude, \
#         discount, \
#         max_error, \
#         bola_gp, \
#         buffer_target_s


def getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN):
  return 87
  chunksizeBytes = getChunkSizeBytes(bitrate, chunkid, CHUNKSIZE)
  zero = 0.0
  five = 0.00002 * chunksizeBytes + 34.8
  twentyfive = 0.0003 * chunksizeBytes - 107.71
  fifty = 0.0007 * chunksizeBytes - 287.3
  seventyfive = 0.0009 * chunksizeBytes - 239.42
  lower = min(five, BLEN * 1000)
  upper = max(min(twentyfive, BLEN * 1000),0)
  #if upper < 0:
  #  upper = 0
  #if lower == upper:
  #  return 0
  #return random.randint(int(zero), int(upper))
  #return twentyfive
  #print chunksizeBytes, upper
  return upper

# function return the actual size of a chunk in bits
def getChunkSizeBytes(bitrate, chunkid, CHUNKSIZE):
  ret = (bitrate * CHUNKSIZE * 1000) / 8
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    ret = size_envivo[bitrate][chunkid]
  return ret

# function returns the actual bitrate of the label bitrate and the specific chunk
def getRealBitrate(bitrate, chunkid, CHUNKSIZE):
  ret = bitrate
  #print bitrate, chunkid
  if CHUNK_AWARE_MODE and bitrate in size_envivo and chunkid <len(size_envivo[bitrate]):
    ret = size_envivo[bitrate][chunkid]*8
  return ret

# function return the actual size of a chunk in bits
def getChunkSizeBits(bitrate, chunkid, CHUNKSIZE):
  ret = bitrate * CHUNKSIZE * 1000
  if CHUNK_AWARE_MODE and bitrate in size_envivo:
    ret = size_envivo[bitrate][chunkid] * 8
  return ret
  
# function returns interpolated bandwidth at the time of the heartbeat
def interpolateBWInterval(time_heartbeat, usedBWArray, bwArray):
  if time_heartbeat == bwArray[-1][0]:
    return bwArray[-1][1]
  time_prev, time_next, bw_prev, bw_next = findNearestTimeStampsAndBandwidths(time_heartbeat, usedBWArray, bwArray) # time_prev < time_heartbeat < time_next
  intervalLength = time_next - time_prev
#   if time_heartbeat > time_next:
#     return (bw_prev + bw_next)/2
  # print time_prev, time_next, bw_prev, bw_next
  try:
    aa = int((intervalLength - (time_heartbeat - time_prev))/float(intervalLength) * bw_prev + (intervalLength - (time_next - time_heartbeat))/float(intervalLength) * bw_next)
  except ZeroDivisionError:
    print >> sys.stderr, "Divide by zero error, exiting..." + sys.argv[1], time_heartbeat, time_prev, time_next, inspect.stack()[1][3]
    sys.exit()
  return int((intervalLength - (time_heartbeat - time_prev))/float(intervalLength) * bw_prev + (intervalLength - (time_next - time_heartbeat))/float(intervalLength) * bw_next)

def estimateBWPrecisionServerStyleSessionHistory(time_heartbeat, BLEN, usedBWArray, sessionHistory, chunkid, bwArray):  
  #print chunkid, sessionHistory
  if chunkid - 2 not in sessionHistory.keys() and chunkid - 1 in sessionHistory.keys():
    return sessionHistory[chunkid - 1][2] / (float(sessionHistory[chunkid - 1][1] - sessionHistory[chunkid - 1][0]) / 1000.0)
  
  if chunkid - 2 not in sessionHistory.keys() and chunkid - 1 not in sessionHistory.keys():
    return interpolateBWInterval(time_heartbeat, usedBWArray, bwArray)

  start_1 = sessionHistory[chunkid - 1][0]
  end_1 = sessionHistory[chunkid - 1][1]
  size_1 = sessionHistory[chunkid - 1][2]
  bw_1 = size_1 / (float(end_1 - start_1) / 1000.0)

  start_2 = sessionHistory[chunkid - 2][0]
  end_2 = sessionHistory[chunkid - 2][1]
  size_2 = sessionHistory[chunkid - 2][2]
  bw_2 = size_1 / (float(end_2 - start_2) / 1000.0)
  #if time_prev_prev == 0:
  #  return interpolateBWInterval(time_heartbeat, usedBWArray)
  if BLEN < 10:
    return min(bw_1, bw_2)

  return (bw_1 + bw_2)/2

# function returns the nearest timestamps and bandwidths to the heartbeat timestamp
def findNearestTimeStampsAndBandwidths(time_heartbeat, usedBWArray, bwArray):
  time_prev, time_next, bw_prev, bw_next = 0, 0, 0, 0
  if len(usedBWArray) > 1 and time_heartbeat > bwArray[len(bwArray) - 1][0]:
    bw_next = pickRandomFromUsedBW(usedBWArray)
    time_next = time_heartbeat
  for i in range(0, len(bwArray)):
    if bwArray[i][0] < time_heartbeat:
      time_prev = bwArray[i][0]
      bw_prev = bwArray[i][1]
  for i in range(len(bwArray) - 1, -1, -1):
    if bwArray[i][0] > time_heartbeat:
      time_next = bwArray[i][0]
      bw_next = bwArray[i][1]
  return time_prev, time_next, bw_prev, bw_next

# function just returns a bandwidth randomly form the second half of the session
def pickRandomFromUsedBW(usedBWArray):
  return usedBWArray[random.randint(len(usedBWArray)/2 ,len(usedBWArray) - 1)]
  

# function to get the best value of the Buffer Safety Margin
def getDynamicBSM(nSamples, hbCount, BSM): 
  if hbCount < 5:
    return 0.25
  stdbw = []
  if nSamples.count(0) != 5:
    for s in nSamples:
      if s == 0:
        continue
      stdbw.append(s)
  CV = np.std(stdbw) / np.mean(stdbw)
  BUFFER_SAFETY_MARGIN = 0.0
  if hbCount % 5 != 0:
    return BSM
  if hbCount != 0 and hbCount % 5 == 0:
    if CV >= 0 and CV < 0.1:
      BUFFER_SAFETY_MARGIN = 0.85
    elif CV >= 0.1 and CV < 0.2:
      BUFFER_SAFETY_MARGIN = 0.65
    elif CV >= 0.2 and CV < 0.3:
      BUFFER_SAFETY_MARGIN = 0.45
    elif CV >= 0.3 and CV < 0.4:
      BUFFER_SAFETY_MARGIN = 0.35
    else:
      BUFFER_SAFETY_MARGIN = 0.20
  return BUFFER_SAFETY_MARGIN

def getTrueBW(clock, currBW, stepsize, decision_cycle, bwArray, usedBWArray, sessiontimeFromTrace):
  ret = currBW
  num = 1.0
  for c in range(clock + stepsize, int(min(clock + decision_cycle + stepsize, sessiontimeFromTrace)), stepsize):
    ret += interpolateBWInterval(c, usedBWArray, bwArray)
    num += 1.0

  return ret / num 
