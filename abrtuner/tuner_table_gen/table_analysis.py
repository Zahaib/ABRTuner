import numpy as np
from low_bw_syth_no_abort_bugfix1224_performance_vector import *
#from table_seg10_desktop_vod_hyb_no_abort_nsdi import *
from table_seg_threshold1_manipulated_drop_60sample_desktop_nsdi import *

syth = low_bw_syth_hyb_no_abort_bugfix1224_table_100
seg = seg_threshold1_manipulated_drop_60sample_desktop_nsdi_table_100

var = 1000
#print len(syth)
for key in syth.keys():
    #print key
    if key not in seg.keys():
        #print key[0], key[1]
        adf=0
    else:
        #if float(np.percentile(seg[key], 10)) - float(min(syth[key]))<0:
        #    print key[0], key[1]
        #elif float(np.percentile(seg[key], 10)) - float(min(syth[key]))==0:
        #    print key[0], key[1], 0
        #elif float(np.percentile(seg[key], 10)) - float(min(syth[key]))<0:
        #    print key[0], key[1], -1

        if float(np.percentile(seg[key], 10)) - float(min(syth[key]))<0:
            print key[0], key[1], -float(np.percentile(seg[key], 10)) + float(min(syth[key]))
#f = open("bar_syth_500.txt", "w")
#for i in range(500, 6500, 500):
#    if (i,var) in syth.keys():
#        #print i, var, len(syth[(i, var)])
#        temp = syth[(i, var)]
#        #print i, min(temp), np.percentile(temp, 10), np.percentile(temp, 50), np.percentile(temp, 90), max(temp)
#ff = open("bar_seg_500.txt", "w")
#for i in range(500, 6500, 500):
#    if (i,var) in seg.keys():
#        #print i, var, len(seg[(i, var)])
#        temp = seg[(i, var)]
#        print i, min(temp), np.percentile(temp, 10), np.percentile(temp, 50), np.percentile(temp, 90), max(temp)
