#i LIST OF HELPER FUNCTIONS
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
import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial
#from __future__ import print_function
import timeit
#def eprint(*args, **kwargs):
#  print(*args, file=sys.stderr, **kwargs)

def onlineCD(sessionHistory, chunk_when_last_chd, interval, playerVisibleBW):
  chd_detected = False
  chd_index = chunk_when_last_chd
  trimThresh = 1000
  lenarray = len(playerVisibleBW)
  playerVisibleBW, cutoff = trimPlayerVisibleBW(playerVisibleBW, trimThresh)
  R, maxes = oncd.online_changepoint_detection(np.asanyarray(playerVisibleBW), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
  #interval = 5
  interval = min(interval, len(playerVisibleBW))
  changeArray = R[interval,interval:-1]
  #for i ,v in list(enumerate(changeArray)):
  #  if v > 0.01:
  #    print "loop",i + cutoff, playerVisibleBW[i], v
  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
   # if v > 0.01 and i > chunk_when_last_chd:
   #   chd_index = i
   #   chd_detected = True
   #   print chd_index, chd_detected
   #   break
    #print changeArray

  #for i,v in list(enumerate(changeArray)): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
    if v > 0.01 and i + cutoff > chunk_when_last_chd and not (i == 0 and chunk_when_last_chd > -1):
      chd_index = i + cutoff
      chd_detected = True
      #print chd_index, chd_detected, cutoff
      break
  #print chd_detected, chd_index
  return chd_detected, chd_index


#def onlineCD(chunk_when_last_chd, interval, playerVisibleBW):
#  chd_detected = False
#  chd_index = chunk_when_last_chd
#  # threshold for the amount to samples to consider for change point
#  trimThresh = 100
#  lenarray = len(playerVisibleBW)
#  playerVisibleBW, cutoff = trimPlayerVisibleBW(playerVisibleBW, trimThresh)
#  R, maxes = oncd.online_changepoint_detection(np.asanyarray(playerVisibleBW), partial(oncd.constant_hazard, 250), oncd.StudentT(0.1,0.01,1,0))
#  #interval = 5
#  interval = min(interval, len(playerVisibleBW))
#  changeArray = R[interval,interval:-1]
#  for i,v in reversed(list(enumerate(changeArray))): #reversed(list(enumerate(changeArray))): # enumerate(changeArray):
#    if v > 0.01 and i + cutoff > chunk_when_last_chd and not (i == 0 and chunk_when_last_chd > -1) :
#      chd_index = i + cutoff
#      chd_detected = True
#      print "change detected i = ", i, " cutoff = ", cutoff, " chd_index = ", chd_index, " chunk_when_last_chd =", chunk_when_last_chd, " len = ", lenarray
#      break
#  return chd_detected, chd_index

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

# function prints a print header
def printHeader():
  print "\nSession joined..." #+ str(group2.irow(0)["clientid"]) + ", " + str(group2.irow(0)["clientsessionid"])
  print "TIME" + "\t" + "BW" + "\t" + "BLEN" + "\t" + "OBR" + "\t" + "BR" + "\t" + "CHKS" + "\t" + "RSDU" + "\t" + "BUFF" + "\t" + "PLAY"

# function prints current session status
def printStats(CANONICAL_TIME, BW, BLEN, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue):
  print str(round(CANONICAL_TIME/1000.0,2)) + "\t" + str(round(BW,2)) + "\t" + str(round(BLEN,2)) + "\t" + str(oldBR) + "\t" + str(BR) + "\t" + str(CHUNKS_DOWNLOADED) + "\t" + str(round(chunk_residue,2)) + "\t" + str(round(BUFFTIME,2)) + "\t" + str(round(PLAYTIME,2))

def printStats_chd(time_curr, bandwidth, BLEN, future_bandwidth, oldBR, BR, chunkid, BUFFTIME, PLAYTIME, chunk_residue, max_error, discount, chunk_when_last_chd_ran):
  print str(round(time_curr/1000.0,2)) + "\t" + str(round(bandwidth,2)) + "\t" + str(round(future_bandwidth, 2)) + "\t" + str(round(BLEN,2)) + "\t" + str(oldBR) + "\t" + str(BR) + "\t" + str(chunkid) + "\t" + str(round(chunk_residue,2)) + "\t" + str(round(BUFFTIME,2)) + "\t" + str(round(PLAYTIME,2)) + "\t" + str(round(max_error,4)) + "\t" + str(discount) + "\t" + str(chunk_when_last_chd_ran)

# function initializes the state variables
def initSysState():
  BLEN = 0
  CHUNKS_DOWNLOADED = 0
  BUFFTIME = 0
  PLAYTIME = 0
  CANONICAL_TIME = 0
  INIT_HB = 50
  MID_HB = 50
  BR = 0
  BW = 0
  AVG_SESSION_BITRATE = 0
  SWITCH_LOCK = 0
  ATTEMPT_ID = 0
  return BLEN, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, CANONICAL_TIME, INIT_HB, MID_HB, BR, BW, AVG_SESSION_BITRATE, SWITCH_LOCK, SIMULATION_STEP, ATTEMPT_ID

# function bootstraps the simulation, some of the functionality is same as the initSysState, check duplication
def bootstrapSim(jointime, BW, BR, CHUNKSIZE):
  sessionHistory = dict()
  BLEN = 0
  CHUNKS_DOWNLOADED = int(BLEN / CHUNKSIZE)
  CLOCK = jointime
  chunk_residue = 0#BLEN / CHUNKSIZE % 1
  sessionHistory[0] = [jointime]
  #print chunk_residue, CHUNKS_DOWNLOADED 
  if BLEN < CHUNKSIZE:
    first_chunk = True
  elif BLEN >= CHUNKSIZE:
    first_chunk = False
  return BLEN, CHUNKS_DOWNLOADED, CLOCK, chunk_residue, first_chunk, sessionHistory  

# just a bunch of sanity checks to ensure input is right
def isSane(bwArray, BR, stdbw, avgbw, size_envivo):
  sanity = True
  if any(bw[1] < 0 for bw in bwArray):
    if DEBUG: print "Bad bandwidth value in bwArry, exiting..."
    sanity = False
  if any(ts[0] < 0 for ts in bwArray):
    if DEBUG: print "Bad timestamp value in bwArry, exiting..."
    sanity = False
  if any(bw[0] < 0 for bw in bwArray):
    if DEBUG: print "Bad bandwidth map, exiting..."
    sanity = False
  if BR == -1:
    if DEBUG: print "Bad init bitrate, exiting..."
    sanity = False
  # filter sessions which have avgbw less than 200kbps or greater than 250mbps
  # if avgbw < 200 or avgbw > 250000:
  #   if DEBUG: print "Bad bandwidth reported, exiting..."
  #   sanity = False
  # filter sessions for which not enough samples are available  
  if len(bwArray) < 3:
    if DEBUG: print "Not enough session information, exiting..."
    sanity = False
    # filter sessions which have too much bandwidth variation    
  #if stdbw/float(avgbw) <= 1: 
  #  if DEBUG: print "Bad bandwidth deviation, exiting..."
  #  sanity = False
  # if BR not in size_envivo.keys():
  #   if DEBUG: print "Bad BR reported, exiting..."
  #   sanity = False

  return sanity      

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
 # if completed == False:
 #   sessionHistory[attempt_id][1] = clock
 #   size = bitrate * CHUNKSIZE * chunk_residue
 #   sessionHistory[attempt_id].append(size)
 #   sessionHistory[attempt_id].append(chunkid)
 #   sessionHistory[attempt_id].append(completed)
 #   sessionHistory[attempt_id + 1] = [clock + time_residue]
 #   return sessionHistory

  if first_chunk:
    size = bitrate * CHUNKSIZE * (1 - 1.25/5.0)
  elif completed == False:
    size = bitrate * CHUNKSIZE * chunk_residue
  else:
    size = bitrate * CHUNKSIZE
  #print "time_residue: " + str(time_residue)
  #time_residue = max(0, time_residue - SIMULATION_STEP)
  sessionHistory[attempt_id].append(clock)
  sessionHistory[attempt_id].append(bitrate)
  sessionHistory[attempt_id].append(chunkid)
  sessionHistory[attempt_id].append(completed)
  sessionHistory[attempt_id + 1] = [clock  + time_residue]
  #if time_residue == 0:
  #print sessionHistory
  return sessionHistory

# this function returns the average and std dev of bandwidth computed from a time window
def getBWFeatures(CLOCK, sessionHistory, attempt_id, mode, chunkid):
  sample_width = 10
  if mode == 0:
    w_size = CLOCK
  elif mode == 1:
    w_size = 5000
  elif mode == 2:
    w_size = 10000
  elif mode == 3:
    w_size = 20000
  elif mode == 4:
    w_size = 30000

  start_id = attempt_id
  if CLOCK >= w_size:
    while start_id > 0 and sessionHistory[start_id][0] > CLOCK - w_size:
      start_id -= 1
  elif CLOCK < w_size:
    start_id = 0
  bw = []
  for i in range(start_id, attempt_id):
    for j in range(0, int(sessionHistory[i][1] - sessionHistory[i][0]) / sample_width):
      if sessionHistory[i][2] == 0.0:
        continue
      bw.append(sessionHistory[i][2] / ((sessionHistory[i][1] - sessionHistory[i][0]) / 1000.0))
  #print "len(bw): " + str(len(bw)) 
  if len(bw) == 0:
    return -1, -1
  return np.average(bw), np.std(bw)


def getBWFeaturesWeighted(CLOCK, sessionHistory, attempt_id, mode, chunkid, chunk_residue, bitrate, CHUNKSIZE):
  sample_width = 10
  if mode == 0:
    w_size = CLOCK
  elif mode == 1:
    w_size = 5000
  elif mode == 2:
    w_size = 10000
  elif mode == 3:
    w_size = 20000
  elif mode == 4:
    w_size = 30000
  print CHUNKSIZE, bitrate, chunkid, attempt_id
  norm_sum = dict()
  try:
    sessionHistory[attempt_id][1]
    start_id = attempt_id
  except IndexError:
    start_id = attempt_id - 1
  #if chunk_residue > 0.0:
  #  start_id = attempt_id - 1
  #else:
  #  start_id = attempt_id
  if CLOCK < w_size:
    w_size = CLOCK
  while start_id >= 0 and sessionHistory[start_id][0] >= CLOCK - w_size:
    if sessionHistory[start_id][2] == 0.0:
      norm_sum[start_id] = 0.0
    else:
      norm_sum[start_id] = (w_size - (CLOCK - sessionHistory[start_id][1])) ** 2
    #print start_id
    start_id -= 1
  if chunk_residue > 0.0:
    norm_sum[attempt_id] = w_size ** 2

  start_id = attempt_id
  if CLOCK >= w_size:
    while start_id > 0 and sessionHistory[start_id - 1][0] >= CLOCK - w_size:
      start_id -= 1
  elif CLOCK < w_size:
    start_id = 0
  print "starting: " + str(start_id)
  bw = []
  bw_weighted = 0
  # first account for the current chunk being downloaded
  print chunk_residue
  if chunk_residue > 0.0:
    total_curr_kbs = 0
    if CHUNK_AWARE_MODE and bitrate in size_envivo:
      total_curr_kbs = size_envivo[bitrate][chunkid] /1000.0
    else:
      total_curr_kbs = bitrate * CHUNKSIZE
    kbs_down = chunk_residue * total_curr_kbs
    print "kbs_down: " + str(kbs_down)
    bw_weighted += norm_sum[attempt_id] / float(sum(norm_sum.values())) * kbs_down / ((CLOCK - sessionHistory[attempt_id][0]) / 1000.0)
    print bw_weighted, kbs_down, norm_sum[attempt_id],  sum(norm_sum.values()), ((CLOCK - sessionHistory[attempt_id][0]) / 1000.0)
    for j in range(0, int(CLOCK - sessionHistory[attempt_id][0]) / sample_width):
      bw.append(kbs_down / ((CLOCK - sessionHistory[attempt_id][0]) / 1000.0))

  for i in range(start_id, attempt_id):
    if norm_sum[i] != 0:
      bw_weighted += norm_sum[i] / float(sum(norm_sum.values())) * sessionHistory[i][2] / ((sessionHistory[i][1] - sessionHistory[i][0]) / 1000.0)
    else:
      bw_weighted += 0
      #print >> sys.stderr,chunk_residue, CLOCK, norm_sum, norm_sum.values(), sessionHistory[i][1], sessionHistory[i][0], sys.argv[1] 
    for j in range(0, int(sessionHistory[i][1] - sessionHistory[i][0]) / sample_width):
      if sessionHistory[i][2] == 0.0:
        continue
      bw.append(sessionHistory[i][2] / ((sessionHistory[i][1] - sessionHistory[i][0]) / 1000.0))

  if len(bw) == 0:
    return -1, -1
  #print norm_sum, bw_weighted, np.std(bw), CLOCK, attempt_id, chunk_residue
  return bw_weighted, np.std(bw)


# getBWFeaturesWeighted with player visible BW
def getBWFeaturesWeightedPlayerVisible(playerVisibleBW, chunk_when_last_chd_ran):
  lookbackwindow = len(playerVisibleBW) - min(51, len(playerVisibleBW) - chunk_when_last_chd_ran)
  #try:
  currentstateBWArray = playerVisibleBW[lookbackwindow:]
  #except IndexError:
    #print chunk_when_last_chd_ran, len(playerVisibleBW)
    #sys.exit()
  #print lookbackwindow, np.mean(currentstateBWArray), np.std(currentstateBWArray)
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

# function returns the amount of time spent in rebuffering
def getStall(ch_d, completionTimeStamps, bufferlen, intervalStart, interval, CHUNKSIZE):
  if ch_d != len(completionTimeStamps):
    return False,0
  if ch_d == 0 and bufferlen < interval :
    return True, interval - bufferlen
  if bufferlen > interval:
    return False, 0
  stall = 0
  ts_minus1 = intervalStart
  for i in range(ch_d):
#     if i < len(completionTimeStamps):
    if bufferlen < interval and (completionTimeStamps[i] - ts_minus1)/float(1000) > bufferlen:
      stall += (completionTimeStamps[i]  - ts_minus1)/float(1000) - bufferlen
      bufferlen = CHUNKSIZE + max(0, bufferlen - (completionTimeStamps[i] - ts_minus1)/float(1000))
    elif bufferlen < interval and (completionTimeStamps[i] - ts_minus1)/float(1000) < bufferlen:
      bufferlen = bufferlen - (completionTimeStamps[i] - ts_minus1)/float(1000) + CHUNKSIZE
    else:
      bufferlen = bufferlen - (completionTimeStamps[i] - ts_minus1)/float(1000) + CHUNKSIZE
    ts_minus1 = completionTimeStamps[i]
      
  if len(completionTimeStamps) > 0 and (completionTimeStamps[-1] - intervalStart)/float(1000) + bufferlen < interval:
    stall += interval - (completionTimeStamps[-1] - intervalStart)/float(1000) - bufferlen
    return True, round(stall,2)
  return False, round(stall,2)

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

#def chunksDownloaded(time_prev, time_curr, bitrate, bandwidth, chunkid, CHUNKSIZE, chunk_residue, usedBWArray, bwArray, time_residue, BLEN, sessionHistory, first_chunk, attempt_id):
# function returns the past 5 BW samples
def getPastFiveBW(sessionHistory, chunkid):
  past_five = list()
  start = max(chunkid - 5 + 1, 0)
  # print start, chunkid, len(sessionHistory.keys()), sessionHistory[len(sessionHistory.keys()) - 1]
  for i in range(start, chunkid + 1):
    bw_sample = (sessionHistory[i][2] / 8) / (float(sessionHistory[i][1] - sessionHistory[i][0])) / 1000.0 # KBytes/ms or MBytes/sec
    past_five.append(bw_sample)
  return past_five

# function returns the BW needed by MPC
def getMPCBW(sessionHistory, bandwidthEsts, pastErrors, chunkid, discount):
  #print discount
  curr_error = 0
  if len(bandwidthEsts) > 0:
    last_chunk_bw = (sessionHistory[chunkid][2] / 8) / float(sessionHistory[chunkid][1] - sessionHistory[chunkid][0]) / 1000.0 # KBytes/ms or MBytes/sec
    curr_error = abs(bandwidthEsts[-1] - last_chunk_bw) / float(last_chunk_bw)
  pastErrors.append(curr_error)
  # print chunkid, len(bandwidthEsts), len(sessionHistory)
  past_five = getPastFiveBW(sessionHistory, chunkid)
  # print past_five
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
  # print chunkid, future_bandwidth, harmonic_bandwidth, max_error
  # print future_bandwidth, max_error #, bandwidthEsts, pastErrors
  # print chunkid, harmonic_bandwidth* 8 * 1000.0, discount, future_bandwidth

  return future_bandwidth, max_error, bandwidthEsts, pastErrors



# function returns the number of chunks downloaded during the heartbeat interval and uses delay
def chunksDownloaded(configsUsed, time_prev, time_curr, bitrate, bandwidth, chunkid, CHUNKSIZE, chunk_residue, usedBWArray, bwArray, time_residue, BLEN, sessionHistory, first_chunk, attempt_id,PLAYTIME,AVG_SESSION_BITRATE, margin, minCellSize, BUFFTIME, playerVisibleBW, chunk_when_last_chd_ran, p1_min, gradual_transition, additive_inc, bandwidthEsts, pastErrors, windowSize, change_magnitude, discount, max_error):
  chunkCount = 0.0
  time_residue_thisInterval = 0.0
  completionTimeStamps = []
  bitrateAtIntervalStart = bitrate
  next_chunk_bitrate = -2
  if bandwidth == 0.0:
    return chunkCount, completionTimeStamps, time_residue_thisInterval

  if CHUNK_AWARE_MODE:
    bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
    #print bitrate
  # first add the residue time from the previous interval
  time_prev += time_residue
  #bandwidth_i = max(interpolateBWInterval(time_prev, usedBWArray, bwArray),0.01)
  time2FinishResidueChunk = (((1 - chunk_residue) * bitrate)/float(bandwidth))
  time2DownloadFullChunk = (bitrate /float(bandwidth))
  #print "time to remain ", time2FinishResidueChunk
  # if there is a residue chunk from the last interval, then handle it first
  if chunk_residue > 0 and time_prev + time2FinishResidueChunk <= time_curr:
    #print "we finish this chunk in this time", chunkid
    chunkCount +=  1 - chunk_residue
    completionTime = time_prev + time2FinishResidueChunk
    completionTimeStamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN)
    time_prev += time2FinishResidueChunk + nextChunkDelay
    ## update sessionHistory here, since a chunk finished download
    sessionHistory = updateSessionHistory(bitrateAtIntervalStart, completionTime, chunkid, CHUNKSIZE, sessionHistory, first_chunk,
                                              nextChunkDelay, attempt_id, True, chunk_residue)
    #print "id=",chunkid,"quality=",bitrateAtIntervalStart,"start=",sessionHistory[chunkid][0],"end=",sessionHistory[chunkid][1],"bufferlength=",BLEN+CHUNKSIZE,"currentPlaylocation=",PLAYTIME
    if TRUE_AVG_BITRATE:
      # true bitrate using chunksize
      AVG_SESSION_BITRATE+=size_envivo[bitrateAtIntervalStart][chunkid]
    else:
      # label bitrate
      AVG_SESSION_BITRATE+=(VIDEO_BIT_RATE[bitrateAtIntervalStart] * CHUNKSIZE * 1000.0) / 8.0
    #est_bandwidth = estimateSmoothBandwidth_dash(sessionHistory, chunkid)
    #est_std = estimateSTD_dash(sessionHistory, chunkid)

    est_bandwidth = est_std = 0
    ONCD = True
    # just a hacky way to adjust ONCD for time series experiments
    if discount < 0:
      ONCD = False

    if ONCD:
      CDinterval = 5
      ch_detected, ch_index = onlineCD(sessionHistory, chunk_when_last_chd_ran, CDinterval, playerVisibleBW)
      est_bandwidth, est_std = getBWFeaturesWeightedPlayerVisible(playerVisibleBW, ch_index)
      #if ch_detected:
      #  print time_curr, ch_index, len(playerVisibleBW), " new state = ", est_bandwidth, est_std
      #additive_inc = 0.0
      nsteps = 2.0
      p1_min_new = 0.0
      if ch_detected:
        chunk_when_last_chd_ran = ch_index
        gradual_transition = nsteps
        #print time_curr/1000.0,est_bandwidth, est_std, chunk_when_last_chd_ran
        if HYB_ABR:
          dict_name_backup = "dash_syth_hyb_table_"+str(minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, p1_min_new, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_self(performance_t, est_bandwidth, est_std, minCellSize)

          additive_inc = (p1_min_new - p1_min) / nsteps
          if gradual_transition > 0:
            p1_min += additive_inc
            gradual_transition -= 1
        elif MPC_ABR:
          dict_name_backup = "mpc_dash_syth_hyb_pen_table_4300_fix1010_"+str(minCellSize)
          performance_t = (globals()[dict_name_backup])
          ABRChoice, disc_min, disc_median, disc_max = getDynamicconfig_mpc(performance_t, est_bandwidth, est_std, minCellSize)
          discount = disc_median
          #print discount, disc_min, disc_median, disc_max
        #print time_curr, p1_min - additive_inc, p1_min, p1_min_new, additive_inc
    
    ######## MPC code
    future_bandwidth, max_error, bandwidthEsts, pastErrors = getMPCBW(sessionHistory, bandwidthEsts, pastErrors, chunkid, discount)
    bitrateMPC = getMPCDecision(BLEN, bitrateAtIntervalStart, chunkid, CHUNKSIZE, future_bandwidth, windowSize)
    ######## MPC code
    #print BLEN
    # print "chunkid ", chunkid, " bitrate selected: ", bitrateMPC
    # TODO
    # Do We need to select bitrate before or after the delay??
    #print "Bitrate selection for next chunk!"
    bitrateAtIntervalStart1 = getUtilityBitrateDecision_dash(sessionHistory, chunkid, chunkid+1, BLEN+CHUNKSIZE, margin)
    # bitrateAtIntervalStart 
    bitrateDASH = getUtilityBitrateDecision_dash(sessionHistory, chunkid, chunkid+1, BLEN+CHUNKSIZE, p1_min)
    # print bitrateAtIntervalStart
    #print chunkid, p1_min
    chunkid+=1
    
    #if CHUNK_DEBUG == True:
    #  printStats_chd(time_curr, bandwidth, BLEN, future_bandwidth, bitrateAtIntervalStart, bitrateMPC, chunkid, BUFFTIME, PLAYTIME, chunk_residue, max_error * 100, discount)

    ############ MPC bitrate ############
    # bitrateAtIntervalStart = bitrateMPC
    change_magnitude += abs(VIDEO_BIT_RATE[bitrateMPC] - VIDEO_BIT_RATE[bitrateAtIntervalStart])
    if MPC_ABR:
      bitrateAtIntervalStart = bitrateMPC
    elif HYB_ABR:
      bitrateAtIntervalStart = bitrateDASH
      

    ############ MPC bitrate ############

    configsUsed.append((time_curr/1000.0, 'MPC', bandwidth, int(est_bandwidth), int(est_std), discount, round(chunk_residue,2), round(BLEN,2), chunkid-1, bitrateAtIntervalStart, round(BUFFTIME,2)))
    #print bitrateAtIntervalStart, bitrateAtIntervalStart1
    #if chunkid==64:
    #  #print "return"
    #  return chunkCount, completionTimeStamps, time_residue_thisInterval, sessionHistory,bitrateAtIntervalStart,AVG_SESSION_BITRATE
    #else:
    #  print bitrateAtIntervalStart, chunkid-1, size_envivo[bitrateAtIntervalStart][chunkid-1]
    #  AVG_SESSION_BITRATE+=size_envivo[bitrateAtIntervalStart][chunkid-1]
    # residue chunk is complete so now move to next chunkid and get the actual bitrate of the next chunk
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, usedBWArray, bwArray),0.01)
    attempt_id += 1
    #print "finished chunk: " + str(chunkid - 1) + " finish time: " + str(completionTime)  
    time2DownloadFullChunk = (bitrate /float(bandwidth))
     
  # loop untill chunks can be downloaded in the interval, after each download add random delay
  #print time_prev, time2DownloadFullChunk, time_curr
  while time_prev + time2DownloadFullChunk <= time_curr:
    chunkCount += 1
    completionTime = time_prev + time2DownloadFullChunk
    completionTimeStamps.append(completionTime)
    nextChunkDelay = getRandomDelay(bitrate, chunkid, CHUNKSIZE, BLEN)
    time_prev += time2DownloadFullChunk + nextChunkDelay
    ## update sessionHistory here, since a chunk finished download
    sessionHistory = updateSessionHistory(bitrateAtIntervalStart, completionTime, chunkid, CHUNKSIZE, sessionHistory, first_chunk,
                                              nextChunkDelay, attempt_id, True, chunk_residue)
    if CHUNK_AWARE_MODE:
      bitrate = getRealBitrate(bitrateAtIntervalStart, chunkid, CHUNKSIZE)
    bandwidth = max(interpolateBWInterval(time_prev, usedBWArray, bwArray),0.01)
    chunkid += 1
    attempt_id += 1
    time2DownloadFullChunk = (bitrate /float(bandwidth))
  # if there is still some time left, download the partial chunk  
  if time_prev < time_curr:
    chunkCount += bandwidth/(float(bitrate)) * (time_curr - time_prev)
    #if chunk_residue >= 0.985 or chunk_residue == 0.0:
    #  print "started chunk: " + str(chunkid) + " time_prev: " + str(time_prev) + " time_curr: " + str(time_curr) + " chunk_residue: " + str(chunk_residue)
  # if the delay was enough to make time_prev greater than time_curr then we need to transfer over the remaining delay to next interval
  if time_prev >= time_curr:
    time_residue_thisInterval = time_prev - time_curr
  return configsUsed, \
         chunkCount, \
         completionTimeStamps, \
         time_residue_thisInterval, \
         sessionHistory,\
         bitrateAtIntervalStart,\
         AVG_SESSION_BITRATE, \
         chunk_when_last_chd_ran, \
         p1_min, \
         gradual_transition, \
         additive_inc, \
         bandwidthEsts, \
         pastErrors, \
         change_magnitude, \
         discount, \
         max_error


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
  
# return the average and standard deviation of the session bandwidth
def getBWStdDev(bwArray):
  bwMat = np.array(bwArray)
  return np.around(np.average(bwMat[:,1]),2), np.around(np.std(bwMat[:,1]),2)
        
# function intializes session state
def parseSessionState(group):
  ret = []
  ts = []
  bw = []
  for i in group.irow(0)["candidatebitrates"].split(","):
    ret.append(int(i))
  for j in range(0, group.shape[0]):
    ts.append(group.irow(j)["timestampms"])
    bw.append(group.irow(j)["bandwidth"])
  return ret, int(group.irow(0)["jointimems"]), int(group.irow(0)["playtimems"]), int(group.irow(0)["sessiontimems"]), int(group.irow(0)["lifeaveragebitratekbps"]), int(group.irow(0)["bufftimems"]), int(group.irow(0)["init_br"]), zip(ts,bw), int(group.irow(0)["chunkDuration"]), len(size_envivo[ret[0]]) #10 , 75 # 

# function intializes session state
def parseSessionStateFromTrace(filename):
  ts, bw = [], []
  init_br = 0
  #bitrates = [1002, 1434, 2738, 3585, 4661, 5885] # candidate bitrates are in kbps, you can change these to suite your values
  #bitrates = [0, 1, 2, 3, 4] # candidate bitrates are in kbps, you can change these to suite your values
  #bitrates = [1183, 1620, 2332, 3463, 4994]
  bitrates = range(0, NUM_BITRATES)
  try:  
    ls = open(filename).readlines()
    for l in ls:
      if l in ['\n', '\r\n']:
	continue
      try:
        ts.append(float(l.split("\t")[0]))
        bw.append(float(l.split("\t")[1]))
      except ValueError:
        ts.append(float(l.split(" ")[0]))
        bw.append(float(l.split(" ")[1]))

  except IOError:
    print("Incorrect filepath: " + str(filename) + " no such file found...")
    sys.exit()

  try:
    init_br = int(float(ls[-1].rstrip("\n").split(" ")[9]))
  except (IndexError, ValueError):
    init_br = bitrates[0]

  # now write the code to read the trace file, following is a sample ts and bw array
  #ts = [0, 1000, 2000, 3000, 4000, 5000, 6000]
  #bw = [179981.99099548874, 203036.0, 209348.0, 198828.0000000001, 209348.0, 203036.0, 209348.0]    
  try:
    totalTraceTime = ts[-1] # read this value as the last time stamp in the file
  except IndexError:
    print >> sys.stderr, sys.argv[1]
    sys.exit()
  chunkDuration = CHUNKSIZE
  jointimems = 0 #ts[0] + 1
  total_chunks = TOTAL_CHUNKS
  #init_br = bitrates[0]
  return bitrates, jointimems, totalTraceTime, totalTraceTime + jointimems, 1, 1, init_br, zip(ts,bw), chunkDuration, total_chunks #10 , 75 # 

def parseSessionStateFromTrace_p(filename, s_id):
  ts, bw = [], []
  init_br = 0
  bitrates = [1002, 1434, 2738, 3585, 4661, 5885] # candidate bitrates are in kbps, you can change these to suite your values

  try:
    ls = open(filename).readlines()
    for l in ls:
      if l in ['\n', '\r\n']:
        continue
      ts.append(float(l.split(" ")[0]))
      bw.append(float(l.split(" ")[1]))
  except IOError:
    print("Incorrect filepath: " + str(filename) + " no such file found...")
    sys.exit()

  try:
    init_br = int(float(ls[-1].rstrip("\n").split(" ")[9]))
  except (IndexError, ValueError):
    init_br = bitrates[0]

  ts = ts[0:s_id]
  bw = bw[0:s_id]
  # now write the code to read the trace file, following is a sample ts and bw array
  #ts = [0, 1000, 2000, 3000, 4000, 5000, 6000]
  #bw = [179981.99099548874, 203036.0, 209348.0, 198828.0000000001, 209348.0, 203036.0, 209348.0]
  try:
    totalTraceTime = ts[-1] # read this value as the last time stamp in the file
  except IndexError:
    sys.stderr.write("Error reading file: " + filename + "\n")
    sys.exit()
  chunkDuration = 5
  jointimems = 0 #ts[0] + 1

  return bitrates, jointimems, totalTraceTime, totalTraceTime + jointimems, 1, 1, init_br, zip(ts,bw), chunkDuration, sys.maxint #10 , 75 # 

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

#def interpolateBWPrecisionServerStyle(time_heartbeat, BLEN, usedBWArray, bwArray):
#  time_prev, time_next, bw_prev, _ = findNearestTimeStampsAndBandwidths(time_heartbeat, usedBWArray, bwArray) # time_prev < time_heartbeat < time_next
#  time_prev_prev, time_next_next, bw_prev_prev, _ = findNearestTimeStampsAndBandwidths(time_prev, usedBWArray, bwArray) # time_prev < time_heartbeat < time_next
#  if time_prev_prev == 0:
#    return interpolateBWInterval(time_heartbeat, usedBWArray, bwArray) 
#  if BLEN < 10:
#    return min(bw_prev, bw_prev_prev)
#  
#  return (bw_prev + bw_prev_prev)/2

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
#   if len(usedBWArray) < 4:
#     return -1
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

# returns a bwArray of average of bandwidth at every 10 second interval
def validationBWMap(bwArray):
  ts = []
  bw = []
  avg, count, index, i = 0, 0, 0, 0
  last = bwArray[len(bwArray) - 1][0] % 10000
  while i < len(bwArray) and bwArray[i][0] <= bwArray[-1][0] - last:
    while i < len(bwArray) and bwArray[i][0] > index * 10000 and bwArray[i][0] <= index * 10000 + 10000:
      avg += bwArray[i][1] # simple average
      i += 1
      count += 1

    index += 1
    if count > 0:
      ts.append(index * 10000)
      bw.append(round(avg/int(count),2))
      avg = 0
      count = 0
  
  # if the last sample is missing, just average for the end using three samples and append
  if i < len(bwArray) - 1:
    j = len(bwArray) - 1
    while j < len(bwArray) and bwArray[-1][0] - bwArray[j][0] < 10000 and count < 3:
      avg += bwArray[j][1]
      count += 1
      j -= 1
    ts.append(bwArray[-1][0])
    bw.append(round(avg/int(count),2))
  
  return zip(ts,bw)

def getTrueBW(clock, currBW, stepsize, decision_cycle, bwArray, usedBWArray, sessiontimeFromTrace):
  ret = currBW
  num = 1.0
  for c in range(clock + stepsize, int(min(clock + decision_cycle + stepsize, sessiontimeFromTrace)), stepsize):
    ret += interpolateBWInterval(c, usedBWArray, bwArray)
    num += 1.0

  return ret / num 
