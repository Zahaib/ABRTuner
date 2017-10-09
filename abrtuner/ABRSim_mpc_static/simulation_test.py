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

#readPerformanceVerctor()
#exit()

#1 = 5 sec
#3 = 20sec
window_mode = 3
#0 : min
#1 : median
#2 : max
pick_mode = 0

if TRACE_MODE:
    traceFile = sys.argv[1]
debugcount = 0
debugcountP = 0
debugcountN = 0
if DATABRICKS_MODE:
    singleSession[['timestampms', 'bandwidth']] = singleSession[['timestampms', 'bandwidth']].astype(int)
    sessionwise = singleSession.groupby(['clientid', 'clientsessionid'])

#sys.stderr.write("running file: " + traceFile + "\n")
allPerf = collections.OrderedDict()
NUM_SESSIONS = 0
percentageErrorBitrate = []
percentageErrorRebuf = []
avgbitratePrecision = []
rebufPrecision = []
avgbitrateGroundTruth = []
rebufGroundTruth = []
avgbwSessions = []
stdbwSessions = []
completionTimeStamps = []
maxQoE = -sys.maxint
optimal_A = 0
optimal_bitrate = 0
optimal_rebuf = 0
optimal_domBR = 0
AVG_SESSION_BITRATE = 0

#list_a = [0.01, 0.05, 0.1, 0.15, 0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
list_a = [0.53]

switchFlag = False
old_chunk_resudue = 0.0
newBR = 0

lastBlen_decisioncycle = list()
b_ratioList = list()
upr_end = 1.0
## hyb
try:
  a_range_start = float(sys.argv[2])
except IndexError:
  a_range_start = 1.0

for upri in range(10, 11, 1):
  upr = upri * -100
  #for A in np.arange(a_range_start,1.01,0.04):
  #for A in np.arange(0.01,a_range_start + 0.01,0.04):
  for A in list_a:

## bb
#for upr in np.arange(0.1, upr_end, 0.05):
  #for A in np.arange(1,int(upr * conf['maxbuflen']) - 10,5):


    oldbw = 0
    if DEBUG:
        printHeader()
    bwMap = dict()
    sizeDict = dict()
    usedBWArray = []
    bitratesPlayed = dict()
    nSamples = collections.deque(5 * [0], 5)
    hbCount = 0
    
    #try:
    #  BSM = float(bestconf[sys.argv[1]])
    #except KeyError:
    #  BSM = 0.25
    BSM = A
    BSM_old = BSM
    BSM1 = BSM
    BSM2 = BSM
    #BSM_old = 0.25
    #BSM = 0.25
    #BSM_1 = 0.25
    #BSM_2 = 0.25
    upr_h = -1000
    upr_b = 0.4
    chunk_sched_time_delay = 0.0
    blen_decrease = False
    BLEN, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, CLOCK, INIT_HB, MID_HB, BR, BW, AVG_SESSION_BITRATE, SWITCH_LOCK, SIMULATION_STEP, ATTEMPT_ID = initSysState()
    if DATABRICKS_MODE:
        group2 = group1.sort("timestampms")
        candidateBR, jointime, playtimems, sessiontimems, bitrate_groundtruth, bufftimems, BR, bwArray, CHUNKSIZE, TOTAL_CHUNKS = parseSessionState(
            group2)
    elif TRACE_MODE:
        candidateBR, jointime, playtimems, sessiontimems, bitrate_groundtruth, bufftimems, BR, bwArray, CHUNKSIZE, TOTAL_CHUNKS = parseSessionStateFromTrace(
            traceFile)
    if VALIDATION_MODE:
        bwArray = bwArray[0::2]
    if AVERAGE_BANDWIDTH_MODE:
        bwArray = validationBWMap(bwArray)
    
    avgbw, stdbw = getBWStdDev(bwArray)
    newBR = BR
    
    BW = int(getInitBW(bwArray))
    if (jointime < bwArray[0][0]):
        bwArray = insertJoinTimeandInitBW(jointime, BW, bwArray)
    BLEN, CHUNKS_DOWNLOADED, CLOCK, chunk_residue, first_chunk, sessionHistory = bootstrapSim(jointime, BW, BR, CHUNKSIZE)
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
    _sample = 0
    configsUsed = []
    firstRebuf = False
    ABRChoice = 'HYB'
    lastABR = ''
    while CLOCK < sessiontimems:
        playStalled_thisInterval = 0
        chd_thisInterval = 0
        blenAdded_thisInterval = 0
    
        if VERBOSE_DEBUG == True or DEBUG == True and timeSinceLastDecision == 0:
            printStats(CLOCK, BW, BLEN, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue)
    
        if CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 < 30000 or CLOCK < 30000:
            decision_cycle = INIT_HB
        elif CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 >= 30000:
            decision_cycle = MID_HB
    
        if CLOCK + interval > sessiontimems:
	    #print "endinterval", interval, CLOCK, sessiontimems
            interval = sessiontimems - CLOCK
    
        chunk_sched_time_delay = max(0, chunk_sched_time_delay - interval)
    #    print "interval: " + str(interval) + " clock: " + str(CLOCK)
    
        timeSinceLastDecision += interval
    
        CLOCK += interval
        if SWITCH_LOCK > 0:
            SWITCH_LOCK -= interval / float(1000)  # add float
    
        if BLEN > 0:
            buffering = False
    
        if buffering and not sessionFullyDownloaded:
            playStalled_thisInterval = min(timeToDownloadSingleChunk(CHUNKSIZE, BR, BW, chunk_residue, CHUNKS_DOWNLOADED),
                                           interval / float(1000))  # add float
            if playStalled_thisInterval < interval / float(1000):  # chunk download so resume
                buffering = False
    
        if not sessionFullyDownloaded and chunk_sched_time_delay < interval:
            numChunks, completionTimeStamps, chunk_sched_time_delay, sessionHistory = chunksDownloaded(CLOCK - interval, CLOCK, BR, BW,
                                                                                       CHUNKS_DOWNLOADED, CHUNKSIZE,
                                                                                       chunk_residue, usedBWArray, bwArray,
                                                                                       chunk_sched_time_delay, BLEN, sessionHistory, first_chunk,
                                                                                       ATTEMPT_ID)
            chd_thisInterval = chunk_residue + numChunks
    #        if int(chd_thisInterval) >= 1 and chunk_sched_time_delay < interval:
    #            chunk_sched_time_delay = getRandomDelay(BR, CHUNKS_DOWNLOADED, CHUNKSIZE, BLEN)
    
            if playStalled_thisInterval == interval / float(1000) and chd_thisInterval >= 1.0:
                buffering = False
            old_chunk_residue = chunk_residue 
            #print chunk_residue
            chunk_residue = chd_thisInterval - int(chd_thisInterval)
            #print chunk_residue
            if BLEN + chd_thisInterval * CHUNKSIZE >= MAX_BUFFLEN:  # can't download more than the MAX_BUFFLEN
                chd_thisInterval = int(MAX_BUFFLEN - BLEN) / CHUNKSIZE
                chunk_residue = 0
    
        if CHUNKS_DOWNLOADED + int(chd_thisInterval) >= math.ceil((playtimems) / float(CHUNKSIZE * 1000)):
            chd_thisInterval = math.ceil((playtimems) / float(CHUNKSIZE * 1000)) - CHUNKS_DOWNLOADED
    
        #if int(chd_thisInterval) == 1:
        #    sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory, first_chunk,
        #                                          chunk_sched_time_delay)
    
        CHUNKS_DOWNLOADED += int(chd_thisInterval)
        ATTEMPT_ID += int(chd_thisInterval)
        if BR in dominantBitrate:
            dominantBitrate[BR] += int(chd_thisInterval)
        else:
            dominantBitrate[BR] = int(chd_thisInterval)
    
        if first_chunk and CHUNKS_DOWNLOADED >= 1:
            first_chunk = False
        blenAdded_thisInterval = int(chd_thisInterval) * CHUNKSIZE
    
        if CHUNKS_DOWNLOADED <= math.ceil((playtimems) / float(
                        CHUNKSIZE * 1000)) and not sessionFullyDownloaded:  # check the equal to sign in less than equal to
            AVG_SESSION_BITRATE += int(chd_thisInterval) * BR * CHUNKSIZE
    
        if CHUNKS_DOWNLOADED >= TOTAL_CHUNKS or CHUNKS_DOWNLOADED >= math.ceil((playtimems) / float(CHUNKSIZE * 1000)):
            sessionFullyDownloaded = True
    
        if not buffering and BLEN >= 0 and BLEN + blenAdded_thisInterval < interval / float(
                1000) and not sessionFullyDownloaded:
            playStalled_thisInterval += (float(interval) / float(1000) - float(BLEN) - float(blenAdded_thisInterval))  # add float
            buffering = True
    
        if not first_chunk and playStalled_thisInterval > 0:
          firstRebuf = True
        BUFFTIME += float(playStalled_thisInterval)
        PLAYTIME += float(interval) / float(1000) - playStalled_thisInterval  # add float
        lastBlen = BLEN
    
        # for last blen in each decision cycle
        #if not first_chunk and not sessionFullyDownloaded and timeSinceLastDecision == decision_cycle:
        #    lastBlen_decisioncycle.append(BLEN)
    
        if int(chd_thisInterval) >= 1:
            lastBlen_decisioncycle.append(BLEN)
    
        if buffering:
            BLEN = 0.0
        elif not buffering and first_chunk and CHUNKS_DOWNLOADED == 0:
            BLEN = max(0, float(BLEN) - float(interval) / float(1000))
        else:
            BLEN = max(0,
                       float(CHUNKS_DOWNLOADED) * float(CHUNKSIZE) - float(PLAYTIME))  # else update the bufferlen to take into account the current time step
    
        if lastBlen > BLEN and blen_decrease == False and CHUNKS_DOWNLOADED > 1:
            blen_decrease = True
        # then take care of the conditional events #########################################################################################################
        #window_avg_BW, window_std_BW = getBWFeatures(CLOCK, sessionHistory, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED)
    
        if DYNAMIC_BSM:
            BSM = getDynamicBSM(nSamples, hbCount, BSM)
        oldBR = BR
        if not first_chunk and not sessionFullyDownloaded and timeSinceLastDecision == decision_cycle:
            #window_avg_BW, window_std_BW = getBWFeaturesWeighted(CLOCK, sessionHistory, ATTEMPT_ID, window_mode, CHUNKS_DOWNLOADED, chunk_residue, BR, CHUNKSIZE)
            hbCount += 1
            #timeP, timeN, bwP, bwN = findNearestTimeStampsAndBandwidths(CLOCK, usedBWArray, bwArray)
            #bwArray[i][0] bwArray[i][1]
            #_sample = bwArray.index((timeP, bwP))
            b_ratio =1        
            if EXPERIMENT_MODE == True and hbCount > 5 and _sample >= 1:
    	        lastABR = ABRChoice
                #ABRChoice = getABRChoice(BB_or_HYB_THROW, window_avg_BW, window_std_BW)    
                b_ratio = 0.0
    
                #if  lastBlen_decisioncycle[-2]==0 and lastBlen_decisioncycle[-1] !=0:
                #    b_ratio = 0.1
                #elif lastBlen_decisioncycle[-2]==0 or lastBlen_decisioncycle[-1] ==0:
                #    b_ratio=0.0
                #else:
                #    b_ratio = float(lastBlen_decisioncycle[-1]) / float(lastBlen_decisioncycle[-2])
                #b_ratioList.append(b_ratio)
    
                #BSM_c, BSM_1, BSM_2 = getDynamicconfig(hyb_throwing_table, window_avg_BW, window_std_BW, pick_mode) # performance_vector_10800_zerogap_min
    	    #ABRChoice, p1_min, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_combine(hyb_throwing_table, bb_agg_lwr, bb_agg_upr, BB_or_HYB_THROW, window_avg_BW, window_std_BW, COMBINATION_ABR)
    	        #ABRChoice, p1_min, p1_median, p1_max, p2_min, p2_median, p2_max,p3_min, p3_median, p3_max = getDynamicconfig_combine(hyb_throwing_table_300, bb_agg_lwr_300, bb_agg_upr_300, BB_or_HYB_THROW_300, window_avg_BW, window_std_BW, COMBINATION_ABR)
                #if ABRChoice == 'HYB':
                #    upr_h = -1000
                #    A = A*0.75+p2_min*0.25
                #    upr_b = upr_b*0.75+p3_min*0.25
                #    BSM = BSM*0.75+p1_min*0.25
                #else:
                #    A = A*0.75+p2_min*0.25
                #    upr_b = upr_b*0.75+p3_min*0.25
    	        #    if int(upr_b * conf['maxbuflen']) - A <= 10: upr_b = (A + 11) / float(conf['maxbuflen'])
                #    BSM = BSM*0.75+p1_min*0.25
            if (COMBINATION_ABR and ABRChoice == 'HYB') or UTILITY_BITRATE_SELECTION:# and firstRebuf == False:
    	    #print 'using HYB'
                #configsUsed.append((CLOCK/1000.0, 'HYB', BW, int(window_avg_BW), int(window_std_BW), round(BSM,2), round(chunk_residue,2), round(BLEN,2), CHUNKS_DOWNLOADED, BR, round(BUFFTIME,2)))
                buffering_weight = upr
                newBR = getUtilityBitrateDecision(BLEN, candidateBR, BW, CHUNKS_DOWNLOADED, CHUNKSIZE, BSM,
                                                  buffering_weight, sessionHistory, chunk_residue, BR, CLOCK,
                                                  decision_cycle, bwArray, usedBWArray, sessiontimems, oldbw, ATTEMPT_ID)
            elif (COMBINATION_ABR and ABRChoice == 'BB') or BUFFERLEN_UTILITY:
    	    #print 'using BB'
    	    #A_min, A_med, A_max = getDynamicconfigBB_lower(bb_agg_lwr, window_avg_BW, window_std_BW, pick_mode)
    	    #upr_min, upr_med, upr_max = getDynamicconfigBB_upper(bb_agg_upr, window_avg_BW, window_std_BW, pick_mode)
    	    #upr = upr_min
    	    #A = A_min
    
    	        configsUsed.append((CLOCK/1000.0, 'BB', BW, int(window_avg_BW), int(window_std_BW), round(A,2), round(upr_b,2), round(chunk_residue,2), round(BLEN,2), CHUNKS_DOWNLOADED, BR, round(BUFFTIME,2)))
    	        conf['r'] = A
    	        conf['maxRPct'] = upr_b
                newBR = getBitrateBBA0(BLEN, candidateBR, conf)
            elif BUFFERLEN_BBA1_UTILITY:
                newBR = getBitrateBBA1(BLEN, candidateBR, conf, CHUNKS_DOWNLOADED, CHUNKSIZE, BR, BW)
            elif BUFFERLEN_BBA2_UTILITY:
                newBR = getBitrateBBA2(BLEN, candidateBR, conf, CHUNKS_DOWNLOADED, CHUNKSIZE, BR, BW, blen_decrease)
            elif BANDWIDTH_UTILITY:
                newBR = getBitrateDecisionBandwidth(BLEN, candidateBR, BW)
            elif WEIGHTED_BANDWIDTH:
                newBR = getBitrateWeightedBandwidth(candidateBR, BW, nSamples, 0.35)  # last parameter is the weight
            else:
                newBR = getBitrateDecision(BLEN, candidateBR, BW)
        else:
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
            #if (newBR > BR and SWITCH_LOCK <= 0) or newBR < BR: # and shouldSwitch(lastABR, ABRChoice, BR, chunk_residue, BLEN, CHUNKS_DOWNLOADED, sessionHistory, ATTEMPT_ID, chunk_sched_time_delay, CHUNKSIZE):
            if (newBR != BR): # and shouldSwitch(lastABR, ABRChoice, BR, chunk_residue, BLEN, CHUNKS_DOWNLOADED, sessionHistory, ATTEMPT_ID, chunk_sched_time_delay, CHUNKSIZE):
    	#print "decision made at: " + str(configsUsed[-1])
                if newBR < BR and not SWITCH_LOCK > 0:
                    SWITCH_LOCK = LOCK
            # update the start time of the chunk, since we have switched and this is a new chunk
    	        sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory, first_chunk, chunk_sched_time_delay, ATTEMPT_ID, False, chunk_residue)
                BR = newBR
                chunk_residue = 0
    	        ATTEMPT_ID += 1
            #sessionHistory[CHUNKS_DOWNLOADED][0] = CLOCK + max(0,chunk_sched_time_delay - SIMULATION_STEP)
        elif NOINTERUPT == True:
            if timeSinceLastDecision == decision_cycle:
                timeSinceLastDecision = 0
            #print "\t", old_chunk_residue, chunk_residue, newBR, BR, switchFlag, SWITCH_LOCK
            if (newBR!=BR) and old_chunk_residue > chunk_residue:
                #print "switched HERE!!"
                if newBR < BR and not SWITCH_LOCK > 0:
                    SWITCH_LOCK = LOCK
    	        sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory, first_chunk, chunk_sched_time_delay, ATTEMPT_ID, False, chunk_residue)
                BR = newBR
                chunk_residue = 0
    	        ATTEMPT_ID += 1
                if switchFlag:
                    switchFlag = False
            elif (newBR!=BR) and old_chunk_residue < chunk_residue:
                switchFlag = True
            
    
        if not first_chunk and not sessionFullyDownloaded and oldBR != BR:
            numSwitches += 1
    
        nSamples.append(BW)
        oldbw = BW
        BW = max(interpolateBWInterval(CLOCK, usedBWArray, bwArray),
                     0.01)  # interpolate bandwidth for the next heartbeat interval
        usedBWArray.append(BW)  # save the bandwidth used in the session
    
    if BLEN > 0:
        PLAYTIME += BLEN

    AVG_SESSION_BITRATE, REBUF_RATIO, rebuf_groundtruth = generateStats(AVG_SESSION_BITRATE, BUFFTIME, PLAYTIME, bufftimems, playtimems)
    allPerf[str(upr) + " " + str(A)] = str(AVG_SESSION_BITRATE) + " " + str(REBUF_RATIO)
    
print traceFile + " QoE: " + str(maxQoE) + " avg. bitrate: " + str(optimal_bitrate) +  " buf. ratio: " + str(optimal_rebuf) + " optimal A: " + str(optimal_A) + " mapping: " + str(allPerf)
#print traceFile + " QoE: " + str(maxQoE) + " avg. bitrate: " + str(optimal_bitrate) +  " buf. ratio: " + str(optimal_rebuf) + " optimal A: " + str(optimal_A) + " mapping: "
#for kk in allPerf.keys():
#    print kk, allPerf[kk]


#print AVG_SESSION_BITRATE, REBUF_RATIO
#print sessionHistory
#maxQoE = 1000
#print traceFile + " QoE: " + str(maxQoE) + " avg. bitrate: " + str(AVG_SESSION_BITRATE) +  " buf. ratio: " + str(REBUF_RATIO) + " configs used: " + str(configsUsed) #+ " bitrates: " + str(dominantBitrate)
#print traceFile + " QoE: " + str(maxQoE) + " avg. bitrate: " + str(AVG_SESSION_BITRATE) +  " buf. ratio: " + str(REBUF_RATIO) + " configs used: " #+ " bitrates: " + str(dominantBitrate)
#for i in configsUsed:
#    print i
#print sessionHistory

#for i in range(0,20):
#  print str(round(sessionHistory[i][0],1)) + "\t\t\t" + str(round(sessionHistory[i][1],1)) + "\t\t\t" + str(sessionHistory[i][2]) + "\t\t\t" + str((sessionHistory[i][2] * 1000.0) / (sessionHistory[i][1] - sessionHistory[i][0]))
