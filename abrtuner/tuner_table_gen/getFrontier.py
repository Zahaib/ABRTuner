import os, sys
#f = open("hybrid_dynamic_vod_min_wire_all_parce_detail.txt", 'r')
##f = open("hybrid_dynamic_vod_min_mobile_all_parce_detail.txt", 'r')
#f = open("hybrid_dynamic_live_min_wire_all_parce_detail.txt", 'r')
#f = open("low_bw_result_dynamic_hyb_desktop_conext_frontier_parce.txt", 'r')
#f = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_table_previous_online_25_frontir_parse.txt", 'r')
#f = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_threshold1_manipulated_drop_60sample_table_previous_online_10per_frontier_parse.txt", 'r')
#f = open("low_bw_result_dynamic_hyb_desktop_nsid_seg_threshold1_manipulated_drop_60sample_table_previous_online_10per_backuptable_fronter_parse.txt", 'r')
#f = open("hybrid_dynamic_live_min_wire_all_parce.txt", 'r')
#f = open("low_bw_result_dynamic_hyb_desktop_nsid_previous_graph_again_frontier_parse.txt", 'r')
#f = open("hybrid_dynamic_vod_min_mobile_all_parce.txt", 'r')
#f = open("bb_dynamic_vod_min_wire_all_parce_detail.txt", 'r')
if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to output of compare_dynamic_all.py>"
  sys.exit()

f = open(sys.argv[1])

import collections
config = dict()
for i in f:
    i = i.replace("\n","").split(" ")
    #print i
    if len(i)<3:
        continue
    #print i
    #if float(i[0]) < 0.25 or float(i[0]) > 0.77:
    #if float(i[0]) > 0.7:# or float(i[0]) > 0.77:
    #    continue
    #if float(i[10]) > 7:
    #if float(i[0]) > 0.7:# or float(i[0]) > 0.77:
    #    continue
    #
    #aggreg bitrate and rebuf
    #config[float(i[2])]=dict()
    #config[float(i[2])][100*float(i[3])]=((i[0],i[1]))
    # avg bitrate and rebuf
    #config[float(i[5])]=dict()
    #config[float(i[5])][float(i[6])]=((i[0],i[1]))
    # median bitrate and 90%tilerebuf
    config[float(i[7])]=dict()
    config[float(i[7])][float(i[10])]=((i[0],i[1]))
    #config[float(i[7])][float(i[11])]=((i[0],i[1]))
    # avg bitrate and 90%tilerebuf
    #config[float(i[5])]=dict()
    #config[float(i[5])][float(i[10])]=((i[0],i[1]))
    # avg bitrate and fraction
    #config[float(i[5])]=dict()
    #config[float(i[5])][float(i[4])]=((i[0],i[1]))
    # median bitrate and fraction
    #config[float(i[7])]=dict()
    #config[float(i[7])][float(i[4])]=((i[0],i[1]))
    config_sort = collections.OrderedDict(sorted(config.items()))
   
pre = -1
for i in reversed(config_sort.keys()):
    if pre==-1:
        pre = config_sort[i].keys()[-1]
        #print config_sort[i][config_sort[i].keys()[-1]][0], config_sort[i][config_sort[i].keys()[-1]][1], i, config_sort[i].keys()[-1]
        #print i, config_sort[i].keys()[-1]
    else:
        if config_sort[i].keys()[-1] > pre:
            #print i, config_sort[i].keys()[-1]
            continue
        else:
            pre = config_sort[i].keys()[-1]
            #print config_sort[i][config_sort[i].keys()[-1]][0], config_sort[i][config_sort[i].keys()[-1]][1], i, config_sort[i].keys()[-1]
            print config_sort[i][config_sort[i].keys()[-1]][1], i, config_sort[i].keys()[-1]
