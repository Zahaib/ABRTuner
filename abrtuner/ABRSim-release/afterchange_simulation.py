# SIMULATION 1.0
import math, sys, collections
from config import *
from helpers import *
from chunkMap import *
from performance_vector import *
from algorithms import *
from simulation_performance_vector import *
import numpy as np
import collections
from collections import deque
import time
from vplayer_state import State
import config
import warnings
warnings.filterwarnings('error')

if TRACE_MODE:
    trace_file = sys.argv[1]
allPerf = collections.OrderedDict()
completionTimeStamps = []
maxQoE = -sys.maxint

switchFlag = False
newBR = 0

lastBlen_decisioncycle = list()
## hyb
dash_zero_buff = 0
if DASH_BUFFER_ADJUST:
  dash_zero_buff = 0.45

#initial_clock = True
#try:
#  a_range_start = float(sys.argv[2])
#except IndexError:
#  a_range_start = 1.0

for initialBSM in [0.25]:
  # for discount in [0, -1]:
  gp = getBolaGP()
  bola_vp = getBolaVP(gp)
  # print >> sys.stderr, gp, bola_vp
  # for bola_gp in np.arange(gp, gp + 0.05, 1.0):
  #for buffer_target_s in np.arange(BUFFER_TARGET_S, BUFFER_TARGET_S + 1, 5):
  # for bola_gp in np.arange(gp - 1.7,gp + 1.5,0.1):
  for bola_gp in np.arange(gp - 1.0,gp + 0.5,0.1):

    #bola_gp = getBolaGP(buffer_target_s)
    #bola_vp = getBolaVP(bola_gp)

    # bola_gp = getBolaGP()
  #for minCellSize in [400]:
  # for windowSize in [1,2,3,4,5,6,7]:
  #for discount in range(-10,201,10):
    #discount = 0
    minCellSize = 900
    max_error = 0
    ###### Change detection variables start ######
    q = deque(maxlen = 2)
    last_chd_interval = 0
    clock_inc = 0
    last_clock_val = 0
    ch_detected = False
    ch_index = 0
    playerVisibleBW = []
    chunk_when_last_chd_ran = -1
    numChunks = -1
    gradual_transition = 0
    additive_inc = 0.0
    ###### Change detection variables end.. ######
    ###### MPC variables start ###################
    discount = 0
    bandwidthEsts = list()
    pastErrors = list()
    change_magnitude = 0
    windowSize = MPC_WINDOWSIZE
    ###### MPC variables end.. ###################
    ###### BOLA variables start ###################
    buffer_target_s = 30
    ###### BOLA variables end.. ###################

    p1_min = initialBSM

    if DEBUG or VERBOSE_DEBUG:
        printHeader()
    upr = -10000000
    bwMap = dict()
    sizeDict = dict()
    usedBWArray = []
    nSamples = collections.deque(5 * [0], 5)
    hbCount = 0
    
    BSM = initialBSM
    upr_h = -10000000
    upr_b = 0.4
    chunk_sched_time_delay = 0.0
    blen_decrease = False
    CHUNKS_DOWNLOADED_old = -1
    BLEN, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, CLOCK, INIT_HB, MID_HB, BR, BW, AVG_SESSION_BITRATE, SWITCH_LOCK, SIMULATION_STEP, ATTEMPT_ID = initSysState()
    candidateBR, jointime, playtimems, sessiontimems, bitrate_groundtruth, bufftimems, BR, bwArray, CHUNKSIZE, TOTAL_CHUNKS = parseSessionStateFromTrace(trace_file)
    
    avgbw, stdbw = getBWStdDev(bwArray)
    newBR = BR
    
    BW = int(getInitBW(bwArray))
    if (jointime < bwArray[0][0]):
        bwArray = insertJoinTimeandInitBW(jointime, BW, bwArray)
    BLEN, CHUNKS_DOWNLOADED, CLOCK, chunk_residue, first_chunk, sessionHistory = bootstrapSim(jointime, BW, BR, CHUNKSIZE)
    # Creating a player state object which keeps track of range of different variables describing the player state.
    # For details see the vplayer_state.py module
    s = State(config, trace_file)

    oldBR = BR
    buffering = False
    sessionFullyDownloaded = False
    numSwitches = 0
    dominantBitrate = dict()
    timeSinceLastDecision = 0
    interval = SIMULATION_STEP
    #BSM = 0.25
    upr_h = -1000
    upr_b = 0.4
    configsUsed = []
    firstRebuf = False
    #ABRChoice = 'HYB'
    lastABR = ''
    chunk_residue = 0.0
    while CLOCK < s.sessiontimems:
        s.playStalled_thisInterval = 0
        s.chd_thisInterval = 0
        s.blenAdded_thisInterval = 0
    
        if  (VERBOSE_DEBUG == True or DEBUG == True) and not s.sessionFullyDownloaded:
            printStats(CLOCK, s.BW, s.BLEN, s.BR, s.oldBR, s.CHUNKS_DOWNLOADED, s.BUFFTIME, s.PLAYTIME, s.chunk_residue)
    
        if CHUNK_DEBUG:
          printStats_chd(CLOCK, s.BW, s.BLEN, 1000, s.BR, s.oldBR, s.CHUNKS_DOWNLOADED, s.BUFFTIME, s.PLAYTIME, s.chunk_residue, s.max_error, s.discount, s.chunk_when_last_chd_ran)

        if s.CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 < 30000 or CLOCK < 30000:
            s.decision_cycle = INIT_HB
        elif s.CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 >= 30000:
            s.decision_cycle = MID_HB
    
        if CLOCK + s.interval > s.sessiontimems:
	    #print "endinterval", interval, CLOCK, sessiontimems
            s.interval = s.sessiontimems - CLOCK
    
        s.chunk_sched_time_delay = max(0, s.chunk_sched_time_delay - s.interval)
        #print "interval: " + str(interval) + " clock: " + str(CLOCK)
    
        s.timeSinceLastDecision += s.interval
    
        CLOCK += s.interval
        if s.SWITCH_LOCK > 0:
            s.SWITCH_LOCK -= s.interval / float(1000)  # add float
    
        if s.BLEN > 0 + s.dash_zero_buff:
            s.buffering = False
    
        if s.buffering and not s.sessionFullyDownloaded:
            s.playStalled_thisInterval = min(timeToDownloadSingleChunk(CHUNKSIZE, s.BR, s.BW, s.chunk_residue, s.CHUNKS_DOWNLOADED),
                                           s.interval / float(1000))  # add float
            if s.playStalled_thisInterval < s.interval / float(1000):  # chunk download so resume
                s.buffering = False
        #print CLOCK, interval, BR, BW, CHUNKS_DOWNLOADED, CHUNKSIZE,  chunk_residue, chunk_sched_time_delay, BLEN, sessionHistory, first_chunk, ATTEMPT_ID
        if not s.sessionFullyDownloaded and s.chunk_sched_time_delay < s.interval:
            #if CHUNKS_DOWNLOADED > 113: exit()
            #window_avg_BW, window_std_BW = getBWFeaturesWeighted(CLOCK, sessionHistory, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED, chunk_residue, BR, CHUNKSIZE)
            #print BR
            s.configsUsed, \
            s.numChunks, \
            s.completionTimeStamps, \
            s.chunk_sched_time_delay, \
            s.sessionHistory, \
            s.BR, \
            s.AVG_SESSION_BITRATE, \
            s.chunk_when_last_chd_ran, \
            s.p1_min, \
            s.gradual_transition, \
            s.additive_inc, \
            s.bandwidthEsts, \
            s.pastErrors, \
            s.change_magnitude, \
            s.discount, \
            s.max_error, \
            bola_gp, \
            s.buffer_target_s  = chunksDownloaded(s.configsUsed, \
                               CLOCK - s.interval, \
                               CLOCK, \
                               s.BR, \
                               s.BW,\
                               s.CHUNKS_DOWNLOADED, \
                               s.CHUNKSIZE,\
                               s.chunk_residue, \
                               s.usedBWArray, \
                               s.bwArray,\
                               s.chunk_sched_time_delay, \
                               s.BLEN, \
                               s.sessionHistory, \
                               s.first_chunk,\
                               s.ATTEMPT_ID,\
                               s.PLAYTIME, \
                               s.AVG_SESSION_BITRATE, \
                               s.minCellSize, \
                               s.BUFFTIME, \
                               s.playerVisibleBW, \
                               s.chunk_when_last_chd_ran, \
                               s.p1_min, \
                               s.gradual_transition, \
                               s.additive_inc, \
                               s.bandwidthEsts, \
                               s.pastErrors, \
                               s.windowSize, \
                               s.change_magnitude, \
                               s.discount, \
                               s.max_error, \
                               bola_gp, \
                               s.bola_vp, \
                               s.buffer_target_s)
            #print numChunks, completionTimeStamps, chunk_sched_time_delay
            s.chd_thisInterval = s.chunk_residue + s.numChunks
    
            if s.playStalled_thisInterval == s.interval / float(1000) and s.chd_thisInterval >= 1.0:
                s.buffering = False
            old_chunk_residue = s.chunk_residue 
            s.chunk_residue = s.chd_thisInterval - int(s.chd_thisInterval)
            if s.BLEN + s.chd_thisInterval * s.CHUNKSIZE >= MAX_BUFFLEN:  # can't download more than the MAX_BUFFLEN
                s.chd_thisInterval = int(MAX_BUFFLEN - s.BLEN) / CHUNKSIZE
                s.chunk_residue = 0
        #s.initial_clock = False
        if s.CHUNKS_DOWNLOADED + int(s.chd_thisInterval) >= math.ceil((s.playtimems) / float(CHUNKSIZE * 1000)):
            s.chd_thisInterval = math.ceil((s.playtimems) / float(CHUNKSIZE * 1000)) - s.CHUNKS_DOWNLOADED
    
        s.clock_inc = CLOCK - s.last_clock_val
        s.last_clock_val = CLOCK
        if s.numChunks > 0:
           s.realBR = getRealBitrate(s.BR, s.CHUNKS_DOWNLOADED, CHUNKSIZE)/float(CHUNKSIZE * 1000)
           if s.chd_thisInterval != 0 and s.numChunks > 0 and int(s.chd_thisInterval) != 1 and s.last_chd_interval != 0 and s.last_chd_interval < s.chd_thisInterval:
             s.q.append((s.realBR * CHUNKSIZE * s.numChunks) / (s.clock_inc / 1000.0))
             if CLOCK % 100 == 0:
               s.playerVisibleBW.append(np.mean(s.q))
        s.last_chd_interval = s.chd_thisInterval



        s.CHUNKS_DOWNLOADED_old = s.CHUNKS_DOWNLOADED
        s.CHUNKS_DOWNLOADED += int(s.chd_thisInterval)
        s.ATTEMPT_ID += int(s.chd_thisInterval)
        if BR in s.dominantBitrate:
            s.dominantBitrate[BR] += int(s.chd_thisInterval)
        else:
            s.dominantBitrate[BR] = int(s.chd_thisInterval)
        #print CHUNKS_DOWNLOADED 
        #if first_chunk and CHUNKS_DOWNLOADED >= 1:
        #    first_chunk = False
        s.blenAdded_thisInterval = int(s.chd_thisInterval) * CHUNKSIZE
    
    
        if not s.buffering and s.BLEN - s.dash_zero_buff >= 0 and s.BLEN - s.dash_zero_buff + s.blenAdded_thisInterval < s.interval / float(
                1000) and not s.sessionFullyDownloaded:
            s.playStalled_thisInterval += (float(s.interval) / float(1000) - (float(s.BLEN) - s.dash_zero_buff + float(s.blenAdded_thisInterval)) )  # add float
            s.buffering = True
            #if first_chunk==True:
            #  playStalled_thisInterval=0
            #print "buffering start: ","time=",CLOCK," playlocation=", PLAYTIME, "bufferlength=",BLEN
    
        if not s.first_chunk and s.playStalled_thisInterval > 0:
          s.firstRebuf = True
        if not s.first_chunk: 
          s.BUFFTIME += float(s.playStalled_thisInterval)
          s.PLAYTIME += float(s.interval) / float(1000) - s.playStalled_thisInterval  # add float

        if s.first_chunk and s.CHUNKS_DOWNLOADED >= 1:
            s.first_chunk = False
        # if float(playStalled_thisInterval) > 0:
        #   print CHUNKS_DOWNLOADED
        #s.PLAYTIME += float(s.interval) / float(1000) - s.playStalled_thisInterval  # add float
        s.lastBlen = s.BLEN
    
        if int(s.chd_thisInterval) >= 1:
            s.lastBlen_decisioncycle.append(s.BLEN)
    
        if s.buffering:
            s.BLEN = 0.0 + s.dash_zero_buff
        elif not s.buffering and s.first_chunk and s.CHUNKS_DOWNLOADED == 0:
            #print "first chunk", interval
            s.BLEN = max(0, float(s.BLEN) - float(s.interval) / float(1000))
        else:
            s.BLEN = max(0, float(s.CHUNKS_DOWNLOADED) * float(s.CHUNKSIZE) - float(s.PLAYTIME))  # else update the bufferlen to take into account the current time step
    
        if s.lastBlen > s.BLEN and s.blen_decrease == False and s.CHUNKS_DOWNLOADED > 1:
            s.blen_decrease = True
        # then take care of the conditional events #########################################################################################################
        #window_avg_BW, window_std_BW = getBWFeatures(CLOCK, sessionHistory, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED)
        if s.CHUNKS_DOWNLOADED >= TOTAL_CHUNKS or s.CHUNKS_DOWNLOADED >= math.ceil((s.playtimems) / float(s.CHUNKSIZE * 1000)):
            s.sessionFullyDownloaded = True
            break
    
        s.oldBR = s.BR

        if NOINTERUPT:
          if s.switchFlag and s.newBR != s.BR:
            pass
          elif s.switchFlag and s.newBR == s.BR:
            s.newBR = s.BR
            s.switchFlag = False
          else:
            s.newBR = s.BR
        else:
          s.newBR = s.BR
        if NOINTERUPT == True:
            if s.timeSinceLastDecision == s.decision_cycle:
                s.timeSinceLastDecision = 0
            #print "\t", old_chunk_residue, chunk_residue, newBR, BR, switchFlag, SWITCH_LOCK
            if ((s.newBR > s.BR and s.SWITCH_LOCK <= 0) or s.newBR < s.BR) and old_chunk_residue > s.chunk_residue:
                #print "switched HERE!!"
                if s.newBR < s.BR and not s.SWITCH_LOCK > 0:
                    s.SWITCH_LOCK = s.LOCK
    	        #sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory, first_chunk, chunk_sched_time_delay, ATTEMPT_ID, False, chunk_residue)
                s.BR = s.newBR
                s.chunk_residue = 0
    	        #ATTEMPT_ID += 1
                if s.switchFlag:
                    s.switchFlag = False
            elif ((s.newBR > s.BR and s.SWITCH_LOCK <= 0) or s.newBR < s.BR) and old_chunk_residue < s.chunk_residue:
                s.switchFlag = True
            
    
        if not s.first_chunk and not s.sessionFullyDownloaded and s.oldBR != s.BR:
            s.numSwitches += 1
    
        s.nSamples.append(s.BW)
        #oldbw = BW
        s.BW = max(interpolateBWInterval(CLOCK, s.usedBWArray, s.bwArray),
                     0.01)  # interpolate bandwidth for the next heartbeat interval
        s.usedBWArray.append(s.BW)  # save the bandwidth used in the session
    
    if s.BLEN > 0:
        s.PLAYTIME += s.BLEN
    AVG_SESSION_BITRATE_sum = s.AVG_SESSION_BITRATE
    s.AVG_SESSION_BITRATE, s.REBUF_RATIO, s.rebuf_groundtruth = generateStats(s.AVG_SESSION_BITRATE, s.BUFFTIME, s.PLAYTIME, s.bufftimems, s.playtimems)
    s.allPerf[str(s.upr) + " " + str(s.initialBSM)] = str(s.AVG_SESSION_BITRATE) + " " + str(s.REBUF_RATIO)+" " + str(s.PLAYTIME)+" " + str(s.BUFFTIME)+" " + str(AVG_SESSION_BITRATE_sum)
    
    print s.trace_file + " initialBSM: "+str(bola_gp)+" minCell: "+str(s.minCellSize)+" QoE: " + str(s.maxQoE) + " avg. bitrate: " + str(s.AVG_SESSION_BITRATE) +  " buf. ratio: " + str(s.REBUF_RATIO) +" playtime: " + str(s.PLAYTIME) +" buftime: " + str(s.BUFFTIME)

