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

if TRACE_MODE:
    traceFile = sys.argv[1]
allPerf = collections.OrderedDict()
completionTimeStamps = []
maxQoE = -sys.maxint
starttt = time.time()

switchFlag = False
newBR = 0

lastBlen_decisioncycle = list()
## hyb
dash_zero_buff = 0
if DASH_BUFFER_ADJUST:
  dash_zero_buff = 0.45

initial_clock = True
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
  for bola_gp in np.arange(gp - 1.5,gp,0.1):

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
    player_visible_bw = []
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
    used_bw_array = []
    nSamples = collections.deque(5 * [0], 5)
    hbCount = 0
    
    BSM = initialBSM
    upr_h = -10000000
    upr_b = 0.4
    chunk_sched_time_delay = 0.0
    blen_decrease = False
    CHUNKS_DOWNLOADED_old = -1
    BLEN, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, CLOCK, INIT_HB, MID_HB, BR, BW, AVG_SESSION_BITRATE, SWITCH_LOCK, SIMULATION_STEP, ATTEMPT_ID = initSysState()
    candidateBR, jointime, playtimems, sessiontimems, bitrate_groundtruth, bufftimems, BR, bw_array, CHUNKSIZE, TOTAL_CHUNKS = parseSessionStateFromTrace(traceFile)
    
    avgbw, stdbw = getBWStdDev(bw_array)
    newBR = BR
    
    BW = int(getInitBW(bw_array))
    if (jointime < bw_array[0][0]):
        bw_array = insertJoinTimeandInitBW(jointime, BW, bw_array)
    BLEN, CHUNKS_DOWNLOADED, CLOCK, chunk_residue, first_chunk, session_history = bootstrapSim(jointime, BW, BR, CHUNKSIZE)
    # Creating a player state object which keeps track of range of different variables describing the player state.
    # For details see the vplayer_state.py module
    s = State(config, traceFile)

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
    while CLOCK < sessiontimems:
        playStalled_thisInterval = 0
        chd_thisInterval = 0
        blenAdded_thisInterval = 0

	#if CLOCK < 300:
        #	print "TOP", CLOCK, chunk_residue, numChunks
    
        if (VERBOSE_DEBUG == True or DEBUG == True) and not sessionFullyDownloaded:
            printStats(CLOCK, BW, BLEN, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue)
    
        if CHUNK_DEBUG:
          printStats_chd(CLOCK, BW, BLEN, 1000, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue, max_error, discount, chunk_when_last_chd_ran)

        if CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 < 30000 or CLOCK < 30000:
            decision_cycle = INIT_HB
        elif CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 >= 30000:
            decision_cycle = MID_HB
    
        if CLOCK + interval > sessiontimems:
	    #print "endinterval", interval, CLOCK, sessiontimems
            interval = sessiontimems - CLOCK
    
        chunk_sched_time_delay = max(0, chunk_sched_time_delay - interval)
        #print "interval: " + str(interval) + " clock: " + str(CLOCK)
    
        timeSinceLastDecision += interval
    
        CLOCK += interval
        if SWITCH_LOCK > 0:
            SWITCH_LOCK -= interval / float(1000)  # add float
    
        if BLEN > 0 + dash_zero_buff:
            buffering = False
    
        if buffering and not sessionFullyDownloaded:
            playStalled_thisInterval = min(timeToDownloadSingleChunk(CHUNKSIZE, BR, BW, chunk_residue, CHUNKS_DOWNLOADED),
                                           interval / float(1000))  # add float
            if playStalled_thisInterval < interval / float(1000):  # chunk download so resume
                buffering = False
        if not sessionFullyDownloaded and chunk_sched_time_delay < interval: # and initial_clock == False:
            #if CHUNKS_DOWNLOADED > 113: exit()
            #window_avg_BW, window_std_BW = getBWFeaturesWeighted(CLOCK, session_history, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED, chunk_residue, BR, CHUNKSIZE)
            #print BR
            configsUsed, \
            numChunks, \
            completionTimeStamps, \
            chunk_sched_time_delay, \
            session_history, \
            BR, \
            AVG_SESSION_BITRATE, \
            chunk_when_last_chd_ran, \
            p1_min, \
            gradual_transition, \
            additive_inc, \
            bandwidthEsts, \
            pastErrors, \
            change_magnitude, \
            discount, \
            max_error, \
            bola_gp, \
            buffer_target_s  = chunksDownloaded(configsUsed, \
                               CLOCK - interval, \
                               CLOCK, \
                               BR, \
                               BW,\
                               CHUNKS_DOWNLOADED, \
                               CHUNKSIZE,\
                               chunk_residue, \
                               used_bw_array, \
                               bw_array,\
                               chunk_sched_time_delay, \
                               BLEN, \
                               session_history, \
                               first_chunk,\
                               ATTEMPT_ID,\
                               PLAYTIME, \
                               AVG_SESSION_BITRATE, \
                               minCellSize, \
                               BUFFTIME, \
                               player_visible_bw, \
                               chunk_when_last_chd_ran, \
                               p1_min, \
                               gradual_transition, \
                               additive_inc, \
                               bandwidthEsts, \
                               pastErrors, \
                               windowSize, \
                               change_magnitude, \
                               discount, \
                               max_error, \
                               bola_gp, \
                               bola_vp, \
                               buffer_target_s)
            #print numChunks, completionTimeStamps, chunk_sched_time_delay
            chd_thisInterval = chunk_residue + numChunks
    #        if int(chd_thisInterval) >= 1 and chunk_sched_time_delay < interval:
    #            chunk_sched_time_delay = getRandomDelay(BR, CHUNKS_DOWNLOADED, CHUNKSIZE, BLEN)
    
            if playStalled_thisInterval == interval / float(1000) and chd_thisInterval >= 1.0:
                buffering = False
            old_chunk_residue = chunk_residue 
            chunk_residue = chd_thisInterval - int(chd_thisInterval)
            if BLEN + chd_thisInterval * CHUNKSIZE >= MAX_BUFFLEN:  # can't download more than the MAX_BUFFLEN
                chd_thisInterval = int(MAX_BUFFLEN - BLEN) / CHUNKSIZE
                chunk_residue = 0
        #initial_clock = False
        if CHUNKS_DOWNLOADED + int(chd_thisInterval) >= math.ceil((playtimems) / float(CHUNKSIZE * 1000)):
            chd_thisInterval = math.ceil((playtimems) / float(CHUNKSIZE * 1000)) - CHUNKS_DOWNLOADED
    
        clock_inc = CLOCK - last_clock_val
        last_clock_val = CLOCK
        if numChunks > 0:
           realBR = getRealBitrate(BR, CHUNKS_DOWNLOADED, CHUNKSIZE)/float(CHUNKSIZE * 1000)
           if chd_thisInterval != 0 and numChunks > 0 and int(chd_thisInterval) != 1 and last_chd_interval != 0 and last_chd_interval < chd_thisInterval:
             #print CLOCK, CHUNKS_DOWNLOADED,round(last_chd_interval,2),round(chd_thisInterval,2), realBR, CHUNKSIZE, numChunks, clock_inc, (realBR * CHUNKSIZE * numChunks) / (clock_inc / 1000.0)
             q.append((realBR * CHUNKSIZE * numChunks) / (clock_inc / 1000.0))
             if CLOCK % 100 == 0:
               player_visible_bw.append(np.mean(q))
        last_chd_interval = chd_thisInterval



        CHUNKS_DOWNLOADED_old = CHUNKS_DOWNLOADED
        CHUNKS_DOWNLOADED += int(chd_thisInterval)
        ATTEMPT_ID += int(chd_thisInterval)
        if BR in dominantBitrate:
            dominantBitrate[BR] += int(chd_thisInterval)
        else:
            dominantBitrate[BR] = int(chd_thisInterval)
        #print CHUNKS_DOWNLOADED 
        #if first_chunk and CHUNKS_DOWNLOADED >= 1:
        #    first_chunk = False
        blenAdded_thisInterval = int(chd_thisInterval) * CHUNKSIZE
    
    
        if not buffering and BLEN - dash_zero_buff >= 0 and BLEN - dash_zero_buff + blenAdded_thisInterval < interval / float(
                1000) and not sessionFullyDownloaded:
            playStalled_thisInterval += (float(interval) / float(1000) - (float(BLEN) - dash_zero_buff + float(blenAdded_thisInterval)) )  # add float
            buffering = True
            #if first_chunk==True:
            #  playStalled_thisInterval=0
            #print "buffering start: ","time=",CLOCK," playlocation=", PLAYTIME, "bufferlength=",BLEN
    
        if not first_chunk and playStalled_thisInterval > 0:
          firstRebuf = True
        if not first_chunk: 
          BUFFTIME += float(playStalled_thisInterval)
          PLAYTIME += float(interval) / float(1000) - playStalled_thisInterval  # add float

        if first_chunk and CHUNKS_DOWNLOADED >= 1:
            first_chunk = False
        # if float(playStalled_thisInterval) > 0:
        #   print CHUNKS_DOWNLOADED
        #PLAYTIME += float(interval) / float(1000) - playStalled_thisInterval  # add float
        lastBlen = BLEN
    
        if int(chd_thisInterval) >= 1:
            lastBlen_decisioncycle.append(BLEN)
    
        if buffering:
            BLEN = 0.0 + dash_zero_buff
        elif not buffering and first_chunk and CHUNKS_DOWNLOADED == 0:
            #print "first chunk", interval
            BLEN = max(0, float(BLEN) - float(interval) / float(1000))
        else:
            BLEN = max(0, float(CHUNKS_DOWNLOADED) * float(CHUNKSIZE) - float(PLAYTIME))  # else update the bufferlen to take into account the current time step
    
        if lastBlen > BLEN and blen_decrease == False and CHUNKS_DOWNLOADED > 1:
            blen_decrease = True
        # then take care of the conditional events #########################################################################################################
        #window_avg_BW, window_std_BW = getBWFeatures(CLOCK, session_history, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED)
        if CHUNKS_DOWNLOADED >= TOTAL_CHUNKS or CHUNKS_DOWNLOADED >= math.ceil((playtimems) / float(CHUNKSIZE * 1000)):
            sessionFullyDownloaded = True
            break
    
        #if DYNAMIC_BSM:
        #    BSM = getDynamicBSM(nSamples, hbCount, BSM)
        oldBR = BR

        if NOINTERUPT:
          if switchFlag and newBR!=BR:
            newBR = newBR
            BR = BR
          elif switchFlag and newBR==BR:
            newBR = BR
            switchFlag = False
          else:
            newBR = BR
        else:
          newBR = BR
        if ALLINTERUPT == True or SMARTINTERUPT==True: 
            if timeSinceLastDecision == decision_cycle:
                timeSinceLastDecision = 0
            if (newBR > BR and SWITCH_LOCK <= 0) or newBR < BR: # and shouldSwitch(lastABR, ABRChoice, BR, chunk_residue, BLEN, CHUNKS_DOWNLOADED, session_history, ATTEMPT_ID, chunk_sched_time_delay, CHUNKSIZE):
    	#print "decision made at: " + str(configsUsed[-1])
                if newBR < BR and not SWITCH_LOCK > 0:
                    SWITCH_LOCK = LOCK
            # update the start time of the chunk, since we have switched and this is a new chunk
    	        #session_history = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, session_history, first_chunk, chunk_sched_time_delay, ATTEMPT_ID, False, chunk_residue)
                BR = newBR
                chunk_residue = 0
    	        #ATTEMPT_ID += 1
            #session_history[CHUNKS_DOWNLOADED][0] = CLOCK + max(0,chunk_sched_time_delay - SIMULATION_STEP)
        elif NOINTERUPT == True:
            if timeSinceLastDecision == decision_cycle:
                timeSinceLastDecision = 0
            #print "\t", old_chunk_residue, chunk_residue, newBR, BR, switchFlag, SWITCH_LOCK
            if ((newBR > BR and SWITCH_LOCK <= 0) or newBR < BR) and old_chunk_residue > chunk_residue:
                #print "switched HERE!!"
                if newBR < BR and not SWITCH_LOCK > 0:
                    SWITCH_LOCK = LOCK
    	        #session_history = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, session_history, first_chunk, chunk_sched_time_delay, ATTEMPT_ID, False, chunk_residue)
                BR = newBR
                chunk_residue = 0
    	        #ATTEMPT_ID += 1
                if switchFlag:
                    switchFlag = False
            elif ((newBR > BR and SWITCH_LOCK <= 0) or newBR < BR) and old_chunk_residue < chunk_residue:
                switchFlag = True
            
    
        if not first_chunk and not sessionFullyDownloaded and oldBR != BR:
            numSwitches += 1
    
        nSamples.append(BW)
        #oldbw = BW
        BW = max(interpolateBWInterval(CLOCK, used_bw_array, bw_array),
                     0.01)  # interpolate bandwidth for the next heartbeat interval
        used_bw_array.append(BW)  # save the bandwidth used in the session
	#if CLOCK < 300:
        # 	print "BOT", CLOCK, chunk_residue, numChunks, "\n"
    
    if BLEN > 0:
        PLAYTIME += BLEN
    AVG_SESSION_BITRATE_sum = AVG_SESSION_BITRATE
    AVG_SESSION_BITRATE, REBUF_RATIO, rebuf_groundtruth = generateStats(AVG_SESSION_BITRATE, BUFFTIME, PLAYTIME, bufftimems, playtimems)
    allPerf[str(upr) + " " + str(initialBSM)] = str(AVG_SESSION_BITRATE) + " " + str(REBUF_RATIO)+" " + str(PLAYTIME)+" " + str(BUFFTIME)+" " + str(AVG_SESSION_BITRATE_sum)
    
    print traceFile + " initialBSM: "+str(bola_gp)+" minCell: "+str(minCellSize)+" QoE: " + str(maxQoE) + " avg. bitrate: " + str(AVG_SESSION_BITRATE) +  " buf. ratio: " + str(REBUF_RATIO) +" playtime: " + str(PLAYTIME) +" buftime: " + str(BUFFTIME)

#end = time.time()
#print(end - starttt)
