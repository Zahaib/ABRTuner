import numpy as np
import sys, subprocess, os
#import pandas as pd
import collections


def findMaxConfig(tups):
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

def findMaxConfig_bb(tups):
    lower = -1000000.0
    for tup in tups:
        if lower < tup[1]:
            lower = tup[1]
    upper =1000000.0
    for tup in tups:
        if tup[1]!=lower:
            continue
        #print tup[0], weight
        if tup[0] < upper:
            upper = tup[0]
        #print tup[0], weight
    return lower, upper


def dominantconfig(configs):
    old_bitrate = 10000.0
    old_rebuf = 10000.0
    configs_dominant = collections.OrderedDict()

    configs = collections.OrderedDict(sorted(configs.items()))
    for bit in configs.keys():
        configs[bit] = collections.OrderedDict(sorted(configs[bit].items()))


    #for bit in reversed(configs.keys()):
    #    for rebuf in reversed(configs[bit].keys()):
    #        print bit, rebuf, configs[bit][rebuf][0]
    #for bit in reversed(configs.keys()):
    #    for rebuf in configs[bit].keys():
    #        print bit, rebuf, configs[bit][rebuf][0]
    #print ""
    for bit in reversed(configs.keys()):
        for rebuf in (configs[bit].keys()):
            list_p = list()
            if (float(old_bitrate) > float(bit) and float(old_rebuf) > float(rebuf)) or (float(old_bitrate) == float(bit) and float(old_rebuf) >  float(rebuf)) or (float(old_bitrate) < float(bit) and float(old_rebuf) == float(rebuf)):
                old_bitrate = float(bit)
                old_rebuf = float(rebuf)
            #if old_bitrate != 10000 and :
                for tup in configs[bit][rebuf]:
                    list_p.append(tup)
            if len(list_p) > 0:
                configs_dominant[(bit, rebuf)] = list_p
    #print configs_dominant
    #for tup in configs_dominant.keys():
    #    print tup, configs_dominant[tup]
    #print ""
    #print "Done to print configs_dominant"
    for tup in configs_dominant.keys():
        if tup[1] > 0:
            continue
        else:
            #print configs_dominant[tup]
            #print findMaxConfig(configs_dominant[tup])
            #print  tup[0], tup[1], findMaxConfig(configs_dominant[tup])
            #print ""
            return tup[0], tup[1], findMaxConfig(configs_dominant[tup])
            #return configs_dominant[tup][0], configs_dominant[tup][1]
    #print  tup[0], tup[1], findMaxConfig(configs_dominant[tup])
    #print "" 
    return tup[0], tup[1], findMaxConfig(configs_dominant[tup])

file_path_allconfig = "/home/zahaib/zahaibVM/convivaProj/ABRSim-allconfigs/"
file_path_allconfig = "/home/zahaib/zahaibVM/convivaProj/ABRSim-dashcompare-allconfig/"
#file_path_allconfig = "/home/zahaib/convivaProj/ABRSim-bw-prediction-yun-test/"
#file_allconfig = "low_bw_allconfigs_hyb.txt"
#file_allconfig = "10800_result_fix_gap_allconfig.txt"
#file_allconfig = "10800_result_allconfig_no_abort.txt"
#file_allconfig = "10800_allconfigs_hyb_no_abort_bugfix_1224.txt"
#file_allconfig = "10800_allconfigs_hyb_no_abort_bugfix_1224_live30sec.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_live30sec.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224.txt"
file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_allstat_fix.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_allstat_fix_5linetest.txt"
#file_allconfig = "ios_allconfigs.txt"
file_allconfig = "ios_allconfigs_allstat_fix.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_interupt.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_interupt_no_lock.txt"
#file_allconfig = "testt.txt"
file_allconfig = "segments_10_desktop_allconfigs_hyb_allstat.txt"
file_allconfig = "segment_trace_threshold_0.3_drop_25sample_2min_desktop_allconfigs_hyb_allstat.txt"
file_allconfig = "segment_trace_threshold_0.1_manipulate1sec_drop60samples_desktop_allconfigs_hyb_allstat.txt"
file_allconfig = "segment_trace_threshold_0.3_manipulate1sec_drop120samples_desktop_allconfigs_hyb_allstat.txt"
file_allconfig = "dash_simulation_result_desktop_allconfigs_hyb_allstat.txt"
file_allconfig = "dash_simulation_result_syn_allconfigs_hyb_allstat.txt"
file_allconfig = "dash_simulation_result_syn_penseive_video_allconfigs_bb_allstat.txt"
# read ground truth

compare = dict()


# read best performnace 
#allconfig_f = open(file_path_allconfig+file_allconfig, 'r')
allconfig_f = open(file_allconfig, 'r')
sessions_10 = collections.OrderedDict()
default_dict25 = dict()
default_dict50 = dict()
default_dict75 = dict()
cnt=0
for f in allconfig_f:
    cnt+=1
    #if cnt%5000==0:
    #    print cnt
    #group = f.split("QoE")[0].split("/")[-2]
    #print group
    #print f
    if len(f.split(",")) < 10:
        continue
    fileName = f.split("QoE")[0].split("/")[-1]
    name = fileName.split(" ")[0]
    #print name
    #break
    out= f.split("\n")[0].split("OrderedDict")[1].replace('\'','').replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(" dominant bitrate:")[0].split(" ")
    #print out, len(out)
    # without all state
    step = 4
    # with all state
    step = 7
    for i in range(0,len(out)/step):
        p1 = float(out[i*step])
        p2 = float(out[i*step+1])
        avgbr = float(out[i*step+2])
        rebuf = float(out[i*step+3])
        #print p1, p2, avgbr, rebuf, name
        if p2==5:
        #if p1 ==0.5 and p2==41:
            #print p1, p2, avgbr, rebuf, name
            default_dict25[name.split(" ")[0]] = (avgbr, rebuf)
        #if p1 ==-1000 and p2==0.53:
        if p2==50:
            default_dict50[name.split(" ")[0]] = (avgbr, rebuf)
        #if p1 ==-1000 and p2==0.77:
        if p2==100:
            default_dict75[name.split(" ")[0]] = (avgbr, rebuf)
        if name not in sessions_10.keys():
            sessions_10[name] = collections.OrderedDict()
        if avgbr not in sessions_10[name].keys():
            sessions_10[name][avgbr] = collections.OrderedDict()
        if rebuf not in sessions_10[name][avgbr].keys():
            sessions_10[name][avgbr][rebuf] = list()
        sessions_10[name][avgbr][rebuf].append((p1, p2))

for fileName in sessions_10.keys():
    sessions_10[fileName] = collections.OrderedDict(sorted(sessions_10[fileName].items()))
for fileName in sessions_10.keys():
    for bit in sessions_10[fileName].keys():
        sessions_10[fileName][bit] = collections.OrderedDict(sorted(sessions_10[fileName][bit].items()))

for session in sessions_10.keys():
    #print session
    #print sessions_10[session]
    if session not in compare.keys():
        compare[session] = []
    compare[session].append(dominantconfig(sessions_10[session]))
"""
f_dynamic = open(file_path_dynamic+file_dynamic,'r')
for f in f_dynamic:
    session = f.split(" ")[0].split("/")[-1]
    br = f.split(" ")[5]
    buff = f.split(" ")[8]
    #print session, br, buff
    #break
    compare[session].append((br, buff))
"""
for session in compare.keys():
    if len(compare[session])!=1:
        continue
    else:
        print session, 
        print default_dict25[session], 
        print default_dict50[session], 
        print default_dict75[session], 
        print compare[session][0]#, compare[session][1]

