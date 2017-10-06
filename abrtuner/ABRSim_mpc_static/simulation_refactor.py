# SIMULATION 1.0
import math, sys, collections
from config import *
from helpers import *
from chunkMap import *
from algorithms import *
import numpy as np
import collections

if TRACE_MODE:
    traceFile = sys.argv[1]
debugcount = 0
debugcountP = 0
debugcountN = 0
if DATABRICKS_MODE:
    singleSession[['timestampms', 'bandwidth']] = singleSession[['timestampms', 'bandwidth']].astype(int)
    sessionwise = singleSession.groupby(['clientid', 'clientsessionid'])

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
upr_end = 0
A_end = 0
allPerf = collections.OrderedDict()
if BUFFERLEN_UTILITY == False:
    upr_end = 0.271
else:
    upr_end = 1.0
if BUFFERLEN_BBA1_UTILITY == True or BUFFERLEN_BBA2_UTILITY == True:
    A_end = 0.02
else:
    A_end = 1.01

utilities = [-500, -750, -1000, -2000, -3000, -4000, -5000, -6000, -7000, -8000, -10000]

oldbw = 0
if DEBUG:
    printHeader()
bwMap = dict()
sizeDict = dict()
usedBWArray = []
bitratesPlayed = dict()
nSamples = collections.deque(5 * [0], 5)
hbCount = 0
BSM = -1.0
chunk_sched_time_delay = 0.0
blen_decrease = False
BLEN, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, CLOCK, INIT_HB, MID_HB, BR, BW, AVG_SESSION_BITRATE, SWITCH_LOCK, SIMULATION_STEP = initSysState()
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
A = 0.25
upr = 10000
while CLOCK < sessiontimems:
    playStalled_thisInterval = 0
    chd_thisInterval = 0
    blenAdded_thisInterval = 0

    if CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 < 30000 or CLOCK < 30000:
        decision_cycle = INIT_HB
    elif CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 >= 30000:
        decision_cycle = MID_HB

    if CLOCK + interval > sessiontimems:
        interval = sessiontimems - CLOCK

    chunk_sched_time_delay = max(0, chunk_sched_time_delay - interval)

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
        numChunks, completionTimeStamps, chunk_sched_time_delay = chunksDownloaded(CLOCK - interval, CLOCK, BR, BW,
                                                                                   CHUNKS_DOWNLOADED, CHUNKSIZE,
                                                                                   chunk_residue, usedBWArray, bwArray,
                                                                                   chunk_sched_time_delay, BLEN)
        chd_thisInterval = chunk_residue + numChunks
        if int(chd_thisInterval) >= 1 and chunk_sched_time_delay < interval:
            chunk_sched_time_delay = getRandomDelay(BR, CHUNKS_DOWNLOADED, CHUNKSIZE, BLEN)

        if playStalled_thisInterval == interval / float(1000) and chd_thisInterval >= 1.0:
            buffering = False

        chunk_residue = chd_thisInterval - int(chd_thisInterval)
        if BLEN + chd_thisInterval * CHUNKSIZE >= MAX_BUFFLEN:  # can't download more than the MAX_BUFFLEN
            chd_thisInterval = int(MAX_BUFFLEN - BLEN) / CHUNKSIZE
            chunk_residue = 0

    if CHUNKS_DOWNLOADED + int(chd_thisInterval) >= math.ceil((playtimems) / float(CHUNKSIZE * 1000)):
        chd_thisInterval = math.ceil((playtimems) / float(CHUNKSIZE * 1000)) - CHUNKS_DOWNLOADED

    if int(chd_thisInterval) == 1:
        sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory, first_chunk,
                                              chunk_sched_time_delay)

    CHUNKS_DOWNLOADED += int(chd_thisInterval)

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
        playStalled_thisInterval += (interval / float(1000) - BLEN - blenAdded_thisInterval)  # add float
        buffering = True

    BUFFTIME += playStalled_thisInterval
    PLAYTIME += interval / float(1000) - playStalled_thisInterval  # add float
    lastBlen = BLEN

    if buffering:
        BLEN = 0
    elif not buffering and first_chunk and CHUNKS_DOWNLOADED == 0:
        BLEN = max(0, BLEN - interval / float(1000))
    else:
        BLEN = max(0,
                   CHUNKS_DOWNLOADED * CHUNKSIZE - PLAYTIME)  # else update the bufferlen to take into account the current time step

    if lastBlen > BLEN and blen_decrease == False and CHUNKS_DOWNLOADED > 1:
        blen_decrease = True
    # then take care of the conditional events #########################################################################################################
    BSM = A
    if DYNAMIC_BSM:
        BSM = getDynamicBSM(nSamples, hbCount, BSM)
    oldBR = BR
    if not first_chunk and not sessionFullyDownloaded and timeSinceLastDecision == decision_cycle:
        if UTILITY_BITRATE_SELECTION:
            buffering_weight = upr
            newBR = getUtilityBitrateDecision(BLEN, candidateBR, BW, CHUNKS_DOWNLOADED, CHUNKSIZE, BSM,
                                              buffering_weight, sessionHistory, chunk_residue, BR, CLOCK,
                                              decision_cycle, bwArray, usedBWArray, sessiontimems, oldbw)
        elif BUFFERLEN_UTILITY:
            conf['r'] = A
            conf['maxRPct'] = upr
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
        newBR = BR

    if timeSinceLastDecision == decision_cycle:
        timeSinceLastDecision = 0
    if (newBR > BR and SWITCH_LOCK <= 0) or newBR < BR:
        if newBR < BR and not SWITCH_LOCK > 0:
            SWITCH_LOCK = LOCK
        BR = newBR
        chunk_residue = 0

    if not first_chunk and not sessionFullyDownloaded and oldBR != BR:
        numSwitches += 1

    nSamples.append(BW)
    oldbw = BW
    if PS_STYLE_BANDWIDTH:
        BW = interpolateBWPrecisionServerStyle(CLOCK, BLEN, usedBWArray)
    else:
        BW = max(interpolateBWInterval(CLOCK, usedBWArray, bwArray),
                 0.01)  # interpolate bandwidth for the next heartbeat interval
    usedBWArray.append(BW)  # save the bandwidth used in the session
    hbCount += 1

if BLEN > 0:
    PLAYTIME += BLEN

AVG_SESSION_BITRATE, REBUF_RATIO, rebuf_groundtruth = generateStats(AVG_SESSION_BITRATE, BUFFTIME, PLAYTIME, bufftimems,
                                                                    playtimems)

allPerf[str(upr) + " " + str(A)] = str(AVG_SESSION_BITRATE) + " " + str(REBUF_RATIO)
print allPerf
