import numpy as np
#f = open("compare_all_dash_simulation_result_desktop_8000_penseive_video_allconfigs_hyb_allstat.txt", "r")
f = open("compare_results_mpc_static.txt", "r")

output_br = dict()
output_re = dict()
for data in f:
    data_temp = data.split("))")[1]
    data_temp = data_temp.split(")") 
    #print data_temp
    for i in data_temp:
        if len(i) < 5: continue
        j = i.replace("(","").replace(")","")
        j = j.split(",")
        bsm = float(j[2])
        br = float(j[0])
        re = float(j[1])
        if len(j)!=3: continue
        if float(j[2]) not in output_br.keys():
            output_br[float(j[2])] = list()
            output_re[float(j[2])] = list()
        output_br[bsm].append(br)
        output_re[bsm].append(100*re)

for bsm in output_br.keys():
    #if bsm != 0.53: continue
    #if bsm != 0.25: continue
    #if bsm != 0.77: continue
    #if bsm != 0.73: continue
    print bsm, np.percentile(output_br[bsm], 50), np.percentile(output_re[bsm], 95)
    #for i in range(0,101):
    #    print i, np.percentile(output_br[bsm], i)
    #for i in range(0,101):
    #    print i, np.percentile(output_re[bsm], i)
