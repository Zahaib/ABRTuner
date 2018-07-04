import numpy as np
import sys, subprocess, os
#import pandas as pd
import collections
# from simulation_performance_vector import findMaxConfig
import sys

if len(sys.argv) < 2:
    print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to the output of compare_allconfig_bola.py>"
    sys.exit()

f_vector = sys.argv[1]

# def findMaxConfig(tups):
#     #print tups
#     bsm = -sys.maxint
#     for tup in tups:
#         if bsm < tup[1]:
#             bsm = tup[1]
#     weight =-1000000.0
#     for tup in tups:
#         if tup[1]!=bsm:
#             continue
#         #print tup[0], weight
#         if tup[0] > weight:
#             weight = tup[0]
#         #print tup[0], weight
#     return weight, bsm

# def dominantconfig(configs):
#     old_bitrate = 10000.0
#     old_rebuf = 10000.0
#     configs_dominant = collections.OrderedDict()

#     configs = collections.OrderedDict(sorted(configs.items()))
#     for bit in configs.keys():
#         configs[bit] = collections.OrderedDict(sorted(configs[bit].items()))


#     #for bit in reversed(configs.keys()):
#     #    for rebuf in reversed(configs[bit].keys()):
#     #        print bit, rebuf, configs[bit][rebuf][0]
#     #for bit in reversed(configs.keys()):
#     #    for rebuf in configs[bit].keys():
#     #        print bit, rebuf, configs[bit][rebuf][0]
#     #print ""
#     for bit in reversed(configs.keys()):
#         for rebuf in (configs[bit].keys()):
#             list_p = list()
#             if (float(old_bitrate) > float(bit) and float(old_rebuf) > float(rebuf)) or (float(old_bitrate) == float(bit) and float(old_rebuf) >  float(rebuf)) or (float(old_bitrate) < float(bit) and float(old_rebuf) == float(rebuf)):
#                 old_bitrate = float(bit)
#                 old_rebuf = float(rebuf)
#             #if old_bitrate != 10000 and :
#                 for tup in configs[bit][rebuf]:
#                     list_p.append(tup)
#             if len(list_p) > 0:
#                 configs_dominant[(bit, rebuf)] = list_p
#     #print configs_dominant
#     #for tup in configs_dominant.keys():
#     #    print tup, configs_dominant[tup]
#     #print ""
#     #print "Done to print configs_dominant"
#     for tup in configs_dominant.keys():
#         if tup[1] > 0:
#             continue
#         else:
#             #print configs_dominant[tup]
#             #print findMaxConfig(configs_dominant[tup])
#             #print  tup[0], tup[1], findMaxConfig(configs_dominant[tup])
#             #print ""
#             return tup[0], tup[1], findMaxConfig(configs_dominant[tup])
#             #return configs_dominant[tup][0], configs_dominant[tup][1]
#     #print  tup[0], tup[1], findMaxConfig(configs_dominant[tup])
#     #print "" 
#     return tup[0], tup[1], findMaxConfig(configs_dominant[tup])

def readPerformanceVerctor_multiple():
    bw_step = 100
    std_step = 100
    for i in range(0, 30, 1):
        x =  bw_step+i*100
        y =  std_step+i*100
        #print x,y
        readPerformanceVerctor_input(x,y)


def getBWandStd(path, fileName):
  trace = open(path+fileName, 'r')
  bw=[]
  for inputdata in trace:
    if len(inputdata) < 2:
      continue
    bw.append(float(inputdata.split("\n")[0].split(" ")[1]))
    #x = fileName.split(".")[-2].split("/")[-1].split("_")[1]
    #y = fileName.split(".")[-2].split("/")[-1].split("_")[2]
    # for real group, we need to calculate x and y manually
  x = sum(bw)/len(bw)
  y = np.std(bw, ddof=1)
  return x, y

def readPerformanceVerctor_input(x_, y_):
    #print "reading table"
    bw_step = x_
    std_step = y_
    # path = "/home/zahaib/ABRTuner/abrtuner/trace/synth_trace_for_table/"
    path = ""
    # f_vector = "compare_dash_simulation_result_syn_penseive_video_allconfigs_mpc_4300_fix1010_discount_range100_delayfix_blenfix.txt"
    lines = open(f_vector).readlines()
    performanceVector_all = dict()
    pv_list = dict()
    cnt = 0
    for l in lines:
        #cnt+=1
        #if cnt%1000 == 0:
        #    print cnt
        l = l.replace(",", "").replace(")", "").replace("(", "").replace("\'", "").rstrip().split(" ")
        #print l
        all_avgbr = float(l[1])
        all_rebuf = float(l[2])
        all_bsm = float(l[4])
        filePath = l[0]
        #bw_, std_ = getBWandStd(path, l[0])
        bw_, std_ = getBWandStd(path, filePath)
        #print str(bw_)+" "+str(std_)+" "+str(all_bsm)
        #continue
        if bw_ > 9000: continue
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
    print "dash_syth_bola_gamma_table_"+str(x_)+" = "+str(pv_list)
    #print "low_bw_syth_hyb_table_"+str(x_)+" = "+str(pv_list)
    #print "low_bw_real_ios_hyb_no_abort_conext_table_"+str(x_)+" = "+str(pv_list)
    #print "seg_threshold3_manipulated_drop_120sample_desktop_nsdi_table_"+str(x_)+" = "+str(pv_list)
    return pv_list

readPerformanceVerctor_multiple()
