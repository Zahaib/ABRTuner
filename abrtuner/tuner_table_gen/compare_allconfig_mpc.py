import numpy as np
import sys, subprocess, os
#import pandas as pd
import collections

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

file_allconfig = "mpc_error_results_all_synthetic_traces.txt"
#file_allconfig = "test.txt"
# read ground truth

compare = dict()


# read best performnace 
#allconfig_f = open(file_path_allconfig+file_allconfig, 'r')
allconfig_f = open(file_allconfig, 'r')
sessions_10 = collections.OrderedDict()
default_dict = dict()
cnt=0
for f in allconfig_f:
    cnt+=1
    #print f
    if len(f) < 10:
        continue
    name = f.split(" ")[0]
    #print name
    #break
    #out= f.split("\n")[0].split("OrderedDict")[1].replace('\'','').replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(" dominant bitrate:")[0].split(" ")
    p1 = 1000000 
    p2 = float(f.split(" ")[-1])
    avgbr = float(f.split(" ")[13])
    rebuf = float(f.split(" ")[16])
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
print sessions_10
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
    #if len(compare[session])!=1:
    #    continue
    #else:
    print session,
    print compare[session][0]#, compare[session][1]

