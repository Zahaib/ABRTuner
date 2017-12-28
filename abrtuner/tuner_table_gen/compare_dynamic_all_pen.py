import numpy as np
import sys, subprocess, os
#import pandas as pd
import collections

# Zahaib: edited the script to take file as input argument
if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to raw result file>"
  sys.exit()

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


def printPercentile_f(target, string):
  f = open(string+".txt",'w')
  for i in np.arange(0,100.5, 0.5):
    #print str(i) + " " + str(np.percentile(target, i))
    f.write(str(i) + " " + str(np.percentile(target, i))+"\n")
  #print "\n"
  f.close()


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


def dominantconfig_qoe(configs):
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
    #print "Done to print configs_dominant"
    config_list = []
    qoe = -100000000
    bitrate =-1
    rebuf = -1
    for tup in configs_dominant.keys():
        qoe_c = float(tup[0])-200*tup[1]*100
        if qoe_c > qoe:
            config_list = configs_dominant[tup]
            qoe = qoe_c
            bitrate = tup[0]
            rebuf = tup[1]
        #print tup, bitrate, rebuf, qoe
    #print bitrate, rebuf, findMaxConfig(config_list)
    #print ""
    return bitrate, rebuf, findMaxConfig(config_list)


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

file_path_allconfig = "/home/zahaib/convivaProj/ABRSim-allconfigs/"
#file_path_allconfig = "/home/zahaib/convivaProj/ABRSim-allconfigs_bb_upper/"
#file_path_allconfig = "/home/zahaib/convivaProj/ABRSim-bw-prediction-yun-test/"
#file_allconfig = "low_bw_allconfigs_hyb.txt"
#file_allconfig = "10800_result_fix_gap_allconfig.txt"
#file_allconfig = "10800_result_allconfig_no_abort.txt"
#file_allconfig = "10800_allconfigs_hyb_no_abort_bugfix_1224.txt"
#file_allconfig = "10800_allconfigs_hyb_no_abort_bugfix_1224_live30sec.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_live30sec.txt"
file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_allstat.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_live30sec_allstat.txt"
#file_allconfig = "low_bw_result_allconfig_no_abort_bb_allstat_20lower.txt"
#file_allconfig = "low_bw_result_allconfig_no_abort_bb_allstat_test.txt"
#file_allconfig = "ios_allconfigs_allstat.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_abort_bugfix_1224_allstat.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_interupt.txt"
#file_allconfig = "low_bw_allconfigs_hyb_no_interupt_no_lock.txt"
#file_allconfig = "testt.txt"
#file_allconfig = "1441_result_allconfig_bb.txt"

#file_path_dynamic = "/home/zahaib/convivaProj/ABRSim-experiment-2/"
#file_dynamic = "10session-hello-dynamic-everyhb.txt"

#file_path_dynamic = "/home/zahaib/convivaProj/ABRSim-nearest-neighbour-yun-auto/"
#file_path_dynamic = "/home/zahaib/convivaProj/ABRSim-nearest-neighbour-yun-bb/"
#file_path_dynamic = "/home/zahaib/convivaProj/ABRSim-nearest-neighbour-yun-auto-test/"
file_path_dynamic = "/home/zahaib/convivaProj/ABRSim-nearest-neighbour-yun-auto-onlinecd-trigger"
#file_dynamic = "hybrid_dynamic_vod_min_wire_all.txt"
#file_dynamic = "hybrid_dynamic_vod_min_wire_53.txt"
#file_dynamic = "hybrid_dynamic_live_min_wire_all.txt"
#file_dynamic = "bb_dynamic_vod_min_wire_3.txt"
#file_dynamic = "1441_result_dynamic_bb_300_max.txt"
#file_dynamic = "low_bw_result_dynamic_hyb_desktop_conext_test.txt"
file_dynamic = "reference_chd.txt"


file_data = "/home/zahaib/convivaProj/convivaData/precisionserver_history_clientIp_time_day_low_bw/"
file_list = "precisionserver_history_low_bw_filelist.txt"

#file_data = "/home/zahaib/convivaProj/convivaData/precisionserver_ios/"
#file_list = "precisionserver_ios_filelist.txt"

#file_data = "/home/zahaib/convivaProj/aggregated_state/"
#file_list = "precisionserver_ios_filelist_nobad.txt"


#file_data = "/home/zahaib/convivaProj/convivaData/fit_trace_0_7500_0_15000/"
#file_list = "10800-filelist.txt"

#file_data = "/home/zahaib/convivaProj/ABRSim-nearest-neighbour-yun-auto-onlinecd-trigger"
#file_list = "onlinecd_exps_from_precisionserver_history_low_bw_filelist.txt"

# read ground truth

#compare = dict()

#f_list = open(file_path_allconfig+file_list, 'r')
#f_list = open(file_data+file_list, 'r')
#for ff in f_list:
#    session= ff.strip().split("/")[-1]
    #session = file_data + "/" + session
    #print session
#    compare[session] = list()
    #fff = open(file_data+ff.strip().split("/")[-1], 'r')
    #for line in fff:
    #    gt= line.split(" ")
    #    compare[session].append((float(gt[7]), float(gt[8])))
    #    break

#print "done to make dic"

# print ground trught
#for key in compare.keys():
#    print key, compare[key][0]

# read best performnace 
#allconfig_f = open(file_path_allconfig+file_allconfig, 'r')
#sessions_10 = collections.OrderedDict()
#default_dict25 = dict()
#default_dict50 = dict()
#default_dict75 = dict()
#cnt=0
#default25_playtime = []
#default50_playtime = []
#default75_playtime = []
#default25_rebuftime = []
#default50_rebuftime = []
#default75_rebuftime = []
#default25_size = []
#default50_size = []
#default75_size = []
#best_playtime = []
#best_rebuftime = []
#best_size = []
#
#sessions = dict()
#configs_dict = dict()
#cntt=0
#for f in allconfig_f:
#    #if cnt%5000==0:
#    #    print cnt
#    #group = f.split("QoE")[0].split("/")[-2]
#    #print group
#    #print f
# 
#    if len(f.split(",")) < 10:
#        continue
#    fileName = f.split("QoE")[0].split("/")[-1]
#    name = fileName.split(" ")[0]
#    #print name
#    if name not in compare.keys():
#        continue
#    #break
#    out= f.split("\n")[0].split("OrderedDict")[1].replace('\'','').replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(" dominant bitrate:")[0].split(" ")
#    #print out, len(out)
#    sessions[name] = dict()
#    for i in range(0,len(out)/7):
#        p1 = float(out[i*7])
#        p2 = float(out[i*7+1])
#        avgbr = float(out[i*7+2])
#        rebuf = float(out[i*7+3])
#        play = float(out[i*7+4])
#        rebuftime = float(out[i*7+5])
#        size = float(out[i*7+6])
#        if p2 not in configs_dict.keys():
#            configs_dict[p2] = []
#        configs_dict[p2].append((play, rebuftime, size))
#        sessions[name][p1] = (avgbr, rebuf, play, rebuftime, size)
#        if name not in sessions_10.keys():
#            sessions_10[name] = collections.OrderedDict()
#        if avgbr not in sessions_10[name].keys():
#            sessions_10[name][avgbr] = collections.OrderedDict()
#        if rebuf not in sessions_10[name][avgbr].keys():
#            sessions_10[name][avgbr][rebuf] = list()
#        sessions_10[name][avgbr][rebuf].append((p1, p2))
#print "1"
#for fileName in sessions_10.keys():
#    sessions_10[fileName] = collections.OrderedDict(sorted(sessions_10[fileName].items()))
#for fileName in sessions_10.keys():
#    for bit in sessions_10[fileName].keys():
#        sessions_10[fileName][bit] = collections.OrderedDict(sorted(sessions_10[fileName][bit].items()))
#print "2"
#for session in sessions_10.keys():
#    #print session
#    #print sessions_10[session]
#    compare[session].append(dominantconfig(sessions_10[session]))
#    if session not in sessions.keys():
#        continue
#    #print compare[session][0][2][0]
#    #print sessions[session][compare[session][0][2][0]]
#    #play = sessions[session][compare[session][0][2][1]][2]
#    #rebuftime = sessions[session][compare[session][0][2][1]][3]
#    #size = sessions[session][compare[session][0][2][1]][4]
#    #best_playtime.append(play)
#    #best_rebuftime.append(rebuftime)
#    #best_size.append(size)
#print "3"
configs_dict = dict()

#f_dynamic = open(file_path_dynamic+file_dynamic,'r')

#f_dynamic = open("hybrid_dynamic_vod_max_wire_until17.txt",'r')
#f_dynamic = open("bb_dynamic_vod_min_wire_all.txt",'r')
#f_dynamic = open("dynamic_desktop_vod_17_1400.txt",'r')
#f_dynamic = open("dynamic_mobile_vod_41_900.txt",'r')
#f_dynamic = open("dynamic_desktop_live_13_1300.txt",'r')
#f_dynamic = open("mpc_mobile_vod.txt",'r')
#f_dynamic = open("dynamic_all.txt",'r')
#f_dynamic = open("ios_41_1500.txt",'r')

#f_dynamic = open("low_bw_result_dynamic_hyb_desktop_conext.txt",'r')
#f_dynamic = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_table_previous_online_25.txt",'r')
#f_dynamic = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_threshold1_manipulated_drop_60sample_table_previous_online_10per.txt",'r')
#f_dynamic = open("low_bw_result_dynamic_hyb_desktop_nsid_previous_graph_again.txt",'r')
#f_dynamic = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_threshold1_manipulated_drop_60sample_table_previous_online_10per_backuptable.txt",'r')

#f_dynamic = open("/home/zahaib/zahaibVM/convivaProj/ABRSim-nearest-neighbour-yun-auto-onlinecd-trigger-periodic/trigger_5.txt",'r')
#ex= open("dynamic_example_33_1200.txt", 'w')
f_dynamic = open(sys.argv[1], "r")
file_path_allconfig = "/home/yun/simulation/desktop_8000_trace_pen/"
total = 0
for f in f_dynamic:
    session = f.split(" ")[0].split("/")[-1]
    #temp = f.split(" ")
    #for i in temp:
    #    print i
    #break
    total+=1
    #if total%1000000==0:
    #    print total
    bw, std =  getBWandStd(file_path_allconfig, session)
    if bw > 4300: continue 
    bsm =f.split(" ")[2]
    cell = f.split(" ")[4]
    length = f.split("configs used:")[1]
    length_temp = length.split("), (")
    #print f
    #for kkk in length_temp:
    #    print kkk
    playtime_pen = length_temp[-1].split(",")[-2]
    playtime_pen = 4*(float(playtime_pen))
    if playtime_pen == 0.0:
        continue 
    #print f.split(" ")
    #print f.split(" ")[9],f.split(" ")[11],f.split(" ")[13]
    try:
        #playtime = 1000*float(f.split(" ")[14])
        playtime = 1000*float(playtime_pen)
        bufftime = 1000*(float(f.split(" ")[16]))
        #if bufftime == 0.01:
        #  bufftime=0.0
        size = 8*float(f.split(" ")[18])
    except:
        continue
        playtime = 1000*float(f.split(" ")[10])
        bufftime = float(f.split(" ")[12])
        size = 8*float(f.split(" ")[14])
    #if bsm==0.33 and cell==1200:
    #    ex.write(str(f.split(" ")[0].split("/")[-1])+" "+str(playtime)+" "+str(bufftime)+" "+str(size)+"\n")
    if bsm not in configs_dict.keys():
        configs_dict[bsm] = dict()
    if cell not in configs_dict[bsm].keys():
        configs_dict[bsm][cell] = []
    #print f
    #print bsm, cell, playtime, bufftime, size
    #break
    configs_dict[bsm][cell].append((playtime, bufftime,size))
    #print session, br, buff
    #break
    #compare[session].append((br, buff))
#print "done parcing"
total = 0
for b in configs_dict.keys():
    for c in configs_dict[b].keys():
        playtime = []
        bufftime = []
        avgbr = []
        avgrebuf = []
        size = []
        rebufcnt=0

        for li in configs_dict[b][c]:
            playtime.append(li[0])
            bufftime.append(li[1])
            avgbr.append(li[2]/li[0])
            avgrebuf.append(100*li[1]/(li[1]+li[0]))
            size.append(li[2])
            if li[1] > 0.0:
                rebufcnt+=1
        print b,c, 
        print sum(size)/sum(playtime), 
        print sum(bufftime)/(sum(bufftime)+sum(playtime)), 
        print float(rebufcnt)/len(bufftime)*100, 
        print float(sum(avgbr))/len(avgbr), 
        print float(sum(avgrebuf)/len(avgrebuf)), 
        print np.percentile(avgbr, 50), np.percentile(avgrebuf, 80), np.percentile(avgrebuf, 85), np.percentile(avgrebuf, 90),  np.percentile(avgrebuf, 95), len(size)
        #if b == 0.25 and c==1500:
        #printPercentile_f(avgbr,"dynamic_mobile_br_41_900")
        #printPercentile_f(avgrebuf,"dynamic_mobile_rebuf_41_900")
        #if b == 0.37 and c==1100:
        #    printPercentile_f(avgbr, "dynamic_br_37_1100_detail")
        #    printPercentile_f(avgrebuf, "dynamic_rebuf_37_1100_detail")
        #if b == 0.33 and c==1200:
        #    printPercentile_f(avgbr, "dynamic_br_33_1200_detail")
        #    printPercentile_f(avgrebuf, "dynamic_rebuf_33_1200_detail")
        #if b == 0.41 and c==1200:
        #    printPercentile_f(avgbr, "dynamic_br_41_1200_detail")
        #    printPercentile_f(avgrebuf, "dynamic_rebuf_41_1200_detail")
            
        

#for con in configs_dict.keys():
#    playtime = []
#    bufftime = []
#    size = []
#    for li in configs_dict[con]:
#        playtime.append(li[0])
#        bufftime.append(li[1])
#        size.append(li[2])
#    print con, sum(size)/sum(playtime), sum(bufftime)/(sum(bufftime)+sum(playtime))
#print sum(default25_size)/sum(default25_playtime), sum(default25_rebuftime)/(sum(default25_rebuftime)+sum(default25_playtime))
#print sum(default50_size)/sum(default50_playtime), sum(default50_rebuftime)/(sum(default50_rebuftime)+sum(default50_playtime))
#print sum(default75_size)/sum(default75_playtime), sum(default75_rebuftime)/(sum(default75_rebuftime)+sum(default75_playtime))
#print sum(best_size)/sum(best_playtime), sum(best_rebuftime)/(sum(best_rebuftime)+sum(best_playtime))
#for session in compare.keys():
#    if len(compare[session])!=1:
#        continue
#    else:
#        print session, default_dict25[session], default_dict50[session], default_dict75[session], compare[session][0]#, compare[session][1]

