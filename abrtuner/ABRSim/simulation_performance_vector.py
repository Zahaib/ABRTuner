# SIMULATION 1.0
import math, sys, collections
from config import *
from helpers import *
from chunkMap import *
from algorithms import *
import numpy as np
import collections
import statistics

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
    #if combination == True:
    if True:
        if bw==-1 and std==-1:
            return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
        # if key not in performance vector
        if (bw_cut, std_cut) not in pv_list_hyb.keys():
            for i in range(2, 1000, 1):
                count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step + std_step, std_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            #abr_list = abr_list + ABRs[(bw_, std_)]
                            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            #abr_list = abr_list + ABRs[(bw_, std_)]
                            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(current_list_hyb)==0:
                    continue
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'HYB'
                    #print "HYB", bw_cut, std_cut, count, sys.argv[1]
                    break
        else:
            #abr_list = ABRs[(bw_cut, std_cut)]
            #current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_cut, std_cut)]
            #current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_cut, std_cut)]
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'HYB'


    #if combination ==True:
    if len(current_list_hyb)==0:
        return 'HYB', 0.25, 0.25, 0.25, 5, 5, 5, 0.4, 0.4, 0.4
    #return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), 0,0,0,0,0,0
    return ABRAlgo, min(current_list_hyb), np.percentile(current_list_hyb,10), max(current_list_hyb), 0,0,0,0,0,0

def getBWandStd(path, fileName):
  trace = open(path+fileName, 'r')
  bw=[]
  for inputdata in trace:
    if len(inputdata) < 5:
      continue
    bw.append(float(inputdata.split("\n")[0].split(" ")[1]))
    #x = fileName.split(".")[-2].split("/")[-1].split("_")[1]
    #y = fileName.split(".")[-2].split("/")[-1].split("_")[2]
    # for real group, we need to calculate x and y manually
  x = sum(bw)/len(bw)
  y = np.std(bw, ddof=1)
  return x, y


def readPerformanceVerctor():
    #print "reading table"
    bw_step = 100
    std_step = 100
    path = "/home/zahaib/convivaProj/convivaData/fit_trace_0_7500_0_15000/"
    f_vector = "comparison_result_10800_allconfigonly_uppergap.txt"
    lines = open(f_vector).readlines()
    performanceVector_all = dict()
    pv_list = dict()
    cnt = 0
    for l in lines:
        #cnt+=1
        #if cnt%1000 == 0:
        #    print cnt
        l = l.replace(",", "").replace(")", "").replace("(", "").replace("\'", "").rstrip().split(" ")
        #grnd_avgbr = float(l[1])
        #grnd_rebuf = float(l[2])
        sim_avgbr = float(l[1])
        sim_rebuf = float(l[2])
        all_avgbr = float(l[3])
        all_rebuf = float(l[4])
        all_bsm = float(l[6])
        bw_, std_ = getBWandStd(path, l[0])
        performanceVector_all[(int(bw_), int(std_))] = all_bsm

#    pv_list = dict()
#    for key in performanceVector_all.keys():
#        bw = key[0]
#        std = key[1]
        #bsm = performanceVector_all[key]
        bw_cut =int(bw_/bw_step)*bw_step
        std_cut = int(std_/std_step)*std_step
        if (bw_cut, std_cut) not in pv_list.keys():
            pv_list[(bw_cut, std_cut)] = list()

        pv_list[(bw_cut, std_cut)].append(all_bsm)
    #print "reading table done"
    print pv_list
    return pv_list

def getABRChoice(BB_or_HYB, bw, std):
    bw_step = 100
    std_step = 100
    if bw == -1 and std == -1:
        return 'HYB'
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in BB_or_HYB.keys():
        #print bw_cut, std_cut
        #return 'HYB'
        if bw_cut < 10000 and float(std) / float(bw) > 0.70:
            return 'BB'
        else:
            return getNearestABR(BB_or_HYB, bw_cut, std_cut, bw_step, std_step)
    #print >> sys.stderr, 'here'
    if 'BB' in BB_or_HYB[bw_cut, std_cut]:
        return 'BB'
    return 'HYB'

def getNearestABR(pv_list, bw_cut, std_cut, bw_step, std_step):
  for i in range(2, 4, 1):
    for bw in range(bw_cut - (i - 1) * bw_step, bw_cut + i * bw_step, bw_step):
      for std in range(std_cut - (i - 1) * std_step, std_cut + i * std_step, std_step):
        if bw == bw_cut and std == std_cut or (bw, std) not in pv_list.keys():
          continue
        if 'BB' in pv_list[bw, std]:
          return 'BB'
  return 'HYB'   
      


def getDynamicconfig_combine(pv_list_hyb, pv_list_bb_1, pv_list_bb_2, ABRs, bw, std, combination):
    bw_step = 300
    std_step = 300
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
    if combination == True:
        if bw==-1 and std==-1:
            return 'BB', 5, 5, 5, 0.4, 0.4, 0.4
        # if key not in performance vector
        if (bw_cut, std_cut) not in ABRs.keys():
            for i in range(2, 1000, 1):
	        count += 1
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step, std_step):
                        if (bw_, std_) in ABRs.keys():
                            abr_list = abr_list + ABRs[(bw_, std_)]
                            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in ABRs.keys():
                            abr_list = abr_list + ABRs[(bw_, std_)]
                            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_, std_)]
                            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_, std_)]
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(abr_list)==0:
                    continue
                elif len(abr_list)>0 and 'BB' in abr_list:
                    ABRAlgo = 'BB'
		    #print "BB", bw_cut, std_cut, count, sys.argv[1]
                    break
                else:# len(abr_list)>0 and 'BB' not in abr_list:
                    ABRAlgo = 'HYB'
		    #print "HYB", bw_cut, std_cut, count, sys.argv[1]
                    break
        else:
            abr_list = ABRs[(bw_cut, std_cut)]
            current_list_bb_1 = current_list_bb_1 + pv_list_bb_1[(bw_cut, std_cut)]
            current_list_bb_2 = current_list_bb_2 + pv_list_bb_2[(bw_cut, std_cut)]
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            if 'BB' in abr_list:
                ABRAlgo = 'BB'
            else: 
                ABRAlgo = 'HYB'
        
    else:
        if bw==-1 and std==-1:
            return 'HYB', 0.25, 0.25, 0.25, 0.25, 0.25, 0.25
        if (bw_cut, std_cut) not in pv_list_hyb.keys():
            for i in range(2, 1000, 1):
                for bw_ in [bw_cut - (i - 1) * bw_step, bw_cut + (i-1) * bw_step]:
                    for std_ in range(std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step, std_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                for std_ in [std_cut - (i - 1) * std_step, std_cut + (i-1) * std_step]:
                    for bw_ in range(bw_cut - (i - 2) * bw_step, bw_cut + (i-1) * bw_step, bw_step):
                        if (bw_, std_) in pv_list_hyb.keys():
                            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_, std_)]
                if len(current_list_hyb)==0:
                    continue
                else:
                    ABRAlgo = 'HYB'
                    break
        else:
            current_list_hyb = current_list_hyb + pv_list_hyb[(bw_cut, std_cut)]
            ABRAlgo = 'HYB'
    if combination ==True:    
        return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), min(current_list_bb_1), statistics.median(current_list_bb_1), max(current_list_bb_1), min(current_list_bb_2), statistics.median(current_list_bb_2), max(current_list_bb_2)
    else:
        return ABRAlgo, min(current_list_hyb), statistics.median(current_list_hyb), max(current_list_hyb), 0,0,0,0,0,0
       
#mode 0 : min
#mode 1 : median
#mode 2 : max
def getDynamicconfig(pv_list, bw, std, mode):    
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 0.25, 0.25, 0.25
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 0.97, 0.97, 0.97
        elif float(bw) < 500:
            return 0.01, 0.01, 0.01
        elif float(std)*2 > float(bw):
            return 0.01, 0.01, 0.01
        else:
            return 0.25, 0.25, 0.25
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 0.97, 0.97, 0.97
        elif float(bw) < 500:
            return 0.01, 0.01, 0.01
        elif float(std) > float(bw)*2:
            return 0.1, 0.01, 0.01
        else:
            return 0.25, 0.25, 0.25
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
        else:
            return 0.25, 0.25, 0.25
    return 0.25, 0.25, 0.25


def getDynamicconfigBB_lower(pv_list, bw, std, mode):
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 5, 5, 5
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 1, 1, 1
        elif float(bw) < 500:
            return 75, 75, 75
        elif float(std)*2 > float(bw):
            return 75, 75, 75
        else:
            return 5, 5, 5
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 1, 1, 1
        elif float(bw) < 500:
            return 75, 75, 75
        elif float(std) > float(bw)*2:
            return 75, 75, 75
        else:
            return 5, 5, 5
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
    return 5, 5, 5

def getDynamicconfigBB_upper(pv_list, bw, std, mode):
    bw_step = 100
    std_step = 100
    if bw==-1 and std==-1:
        return 0.4, 0.4, 0.4
    bw_cut =int(float(bw)/bw_step)*bw_step
    std_cut = int(float(std)/std_step)*std_step
    if (bw_cut, std_cut) not in pv_list.keys():
        if float(bw) > 10000:
            return 0.33, 0.33, 0.33
        elif float(bw) < 500:
            return 0.9, 0.9, 0.9
        elif float(std)*2 > float(bw):
            return 0.9, 0.9, 0.9
        else:
            return 0.4, 0.4, 0.4
    current_list = pv_list[(bw_cut, std_cut)]
    if len(current_list)==0:
        if float(bw) > 12000:
            return 0.33, 0.33, 0.33
        elif float(bw) < 500:
            return 0.9, 0.9, 0.9
        elif float(std) > float(bw)*2:
            return 0.9, 0.9, 0.9
        else:
            return 0.4, 0.4, 0.4
    else:
        if mode ==0:
            return min(current_list), statistics.median(current_list), max(current_list)
        elif mode ==1:
            return statistics.median(current_list), min(current_list), max(current_list)
        elif mode == 2:
            return max(current_list), statistics.median(current_list), min(current_list)
    return 0.4, 0.4, 0.4

def findMaxConfig(tups):
    #print tups
    bsm = -1.0
    for tup in tups:
        if bsm < tup[1]:
            bsm = tup[1]
    weight =-1000000.0
    for tup in tups:
        if tup[1]!=bsm:
            continue
        #print tup[0], weight
        if tup[0] > weight:
            weight = tup[0]
        #print tup[0], weight
    return weight, bsm



def dominantconfig(configs):
    #print configs
    old_bitrate = 10000.0
    old_rebuf = 10000.0
    configs_dominant = collections.OrderedDict()

    configs = collections.OrderedDict(sorted(configs.items()))
    for bit in configs.keys():
        configs[bit] = collections.OrderedDict(sorted(configs[bit].items()))

    for bit in reversed(configs.keys()):
        for rebuf in reversed(configs[bit].keys()):
            list_p = list()
            if float(old_bitrate) > float(bit) and float(old_rebuf) > float(rebuf):
                old_bitrate = float(bit)
                old_rebuf = float(rebuf)
                for tup in configs[bit][rebuf]:
                    list_p.append(tup)
            if len(list_p) > 0:
                configs_dominant[(bit, rebuf)] = list_p

    for tup in configs_dominant.keys():
        if tup[1] > 0:
            continue
        else:
            return findMaxConfig(configs_dominant[tup])
    return findMaxConfig(configs_dominant[tup])


def performance_vector(sample, filename):
    traceFile = filename
    numSamples = len(open(traceFile).readlines())

    allPerf = collections.OrderedDict()

    for upri in range(1, 41, 10):
        upr = upri * -100
        for A in np.arange(0.01, 1.01, 0.04):

            oldbw = 0
            #if DEBUG:
            #    printHeader()
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
            candidateBR, jointime, playtimems, sessiontimems, bitrate_groundtruth, bufftimems, BR, bwArray, CHUNKSIZE, TOTAL_CHUNKS = parseSessionStateFromTrace(
                traceFile)

            #print "per: " + str(sample) + " " + str(len(bwArray))
            avgbw, stdbw = getBWStdDev(bwArray)

            BW = int(getInitBW(bwArray))
            if (jointime < bwArray[0][0]):
                bwArray = insertJoinTimeandInitBW(jointime, BW, bwArray)

            BLEN, CHUNKS_DOWNLOADED, CLOCK, chunk_residue, first_chunk, sessionHistory = bootstrapSim(jointime, BW, BR,
                                                                                                      CHUNKSIZE)
            oldBR = BR
            buffering = False
            sessionFullyDownloaded = False
            numSwitches = 0
            dominantBitrate = dict()
            timeSinceLastDecision = 0
            interval = SIMULATION_STEP
	    endTime = bwArray[sample][0]
            while CLOCK < endTime:
                playStalled_thisInterval = 0
                chd_thisInterval = 0

                #if VERBOSE_DEBUG == True or DEBUG == True and timeSinceLastDecision == 0:
                #    printStats(CLOCK, BW, BLEN, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue)

                if CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 < 30000 or CLOCK < 30000:
                    decision_cycle = INIT_HB
                elif CHUNKS_DOWNLOADED * CHUNKSIZE * 1000 >= 30000:
                    decision_cycle = MID_HB

                if CLOCK + interval > sessiontimems:
                    interval = sessiontimems - CLOCK
		#print "interval: " + str(interval) + " clock: " + str(CLOCK)
                chunk_sched_time_delay = max(0, chunk_sched_time_delay - interval)

                timeSinceLastDecision += interval

                CLOCK += interval
                if SWITCH_LOCK > 0:
                    SWITCH_LOCK -= interval / float(1000)  # add float

                if BLEN > 0:
                    buffering = False

                if buffering and not sessionFullyDownloaded:
                    playStalled_thisInterval = min(
                        timeToDownloadSingleChunk(CHUNKSIZE, BR, BW, chunk_residue, CHUNKS_DOWNLOADED),
                        interval / float(1000))  # add float
                    if playStalled_thisInterval < interval / float(1000):  # chunk download so resume
                        buffering = False

                if not sessionFullyDownloaded and chunk_sched_time_delay < interval:
                    numChunks, completionTimeStamps, chunk_sched_time_delay, sessionHistory = chunksDownloaded(CLOCK - interval, CLOCK,
                                                                                               BR, BW,
                                                                                               CHUNKS_DOWNLOADED,
                                                                                               CHUNKSIZE, chunk_residue,
                                                                                               usedBWArray, bwArray,
                                                                                               chunk_sched_time_delay,
                                                                                               BLEN, sessionHistory, first_chunk)
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

                #if int(chd_thisInterval) == 1:
                #    sessionHistory = updateSessionHistory(BR, CLOCK, CHUNKS_DOWNLOADED, CHUNKSIZE, sessionHistory,
                #                                          first_chunk, chunk_sched_time_delay)

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

                if CHUNKS_DOWNLOADED >= TOTAL_CHUNKS or CHUNKS_DOWNLOADED >= math.ceil(
                                (playtimems) / float(CHUNKSIZE * 1000)):
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
                        newBR = getBitrateBBA2(BLEN, candidateBR, conf, CHUNKS_DOWNLOADED, CHUNKSIZE, BR, BW,
                                               blen_decrease)
                    elif BANDWIDTH_UTILITY:
                        newBR = getBitrateDecisionBandwidth(BLEN, candidateBR, BW)
                    elif WEIGHTED_BANDWIDTH:
                        newBR = getBitrateWeightedBandwidth(candidateBR, BW, nSamples,
                                                            0.35)  # last parameter is the weight
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
                #if PS_STYLE_BANDWIDTH:
                #    BW = interpolateBWPrecisionServerStyle(CLOCK, BLEN, usedBWArray, bwArray)
                #else:
	#	if CLOCK == bwArray[-1][0]:
	#	    BW = bwArray[-1][1]
	#	else:
                BW = max(interpolateBWInterval(CLOCK, usedBWArray, bwArray),
                             0.01)  # interpolate bandwidth for the next heartbeat interval
                usedBWArray.append(BW)  # save the bandwidth used in the session
                hbCount += 1

            # print status after finishing
            #if DEBUG:
            #    printStats(CLOCK, BW, BLEN, BR, oldBR, CHUNKS_DOWNLOADED, BUFFTIME, PLAYTIME, chunk_residue)

            if BLEN > 0:
                PLAYTIME += BLEN

            AVG_SESSION_BITRATE, REBUF_RATIO, rebuf_groundtruth = generateStats(AVG_SESSION_BITRATE, BUFFTIME, PLAYTIME,
                                                                                bufftimems, playtimems)
            #print upr, A, AVG_SESSION_BITRATE   

            if float(AVG_SESSION_BITRATE) not in allPerf.keys():
                allPerf[float(AVG_SESSION_BITRATE)] = collections.OrderedDict()
            if float(REBUF_RATIO) not in allPerf[float(AVG_SESSION_BITRATE)].keys():
                #allPerf[float(AVG_SESSION_BITRATE)][float(REBUF_RATIO)] = collections.OrderedDict()
                allPerf[float(AVG_SESSION_BITRATE)][float(REBUF_RATIO)] = list()
            allPerf[float(AVG_SESSION_BITRATE)][float(REBUF_RATIO)].append((float(upr), float(A)))

    return dominantconfig(allPerf)
