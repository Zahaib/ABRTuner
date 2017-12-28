import math, sys, collections
import numpy as np
import collections
import statistics

def getBWandStd_seg(path, fileName):
  trace = open(path+fileName, 'r')
  bw=[]
  for inputdata in trace:
    if len(inputdata) < 3:
      continue
    if float(inputdata.split("\n")[0].split(" ")[0]) > 375000:
      break
    bw.append(float(inputdata.split("\n")[0].split(" ")[1]))
    #x = fileName.split(".")[-2].split("/")[-1].split("_")[1]
    #y = fileName.split(".")[-2].split("/")[-1].split("_")[2]
    # for real group, we need to calculate x and y manually
  x = sum(bw)/len(bw)
  y = np.std(bw, ddof=1)
  return x, y, len(bw)

def getBWandStd(path, fileName):
  trace = open(path+fileName, 'r')
  bw=[]
  for inputdata in trace:
    if len(inputdata) < 3:
      continue
    bw.append(float(inputdata.split("\n")[0].split(" ")[1]))
    #x = fileName.split(".")[-2].split("/")[-1].split("_")[1]
    #y = fileName.split(".")[-2].split("/")[-1].split("_")[2]
    # for real group, we need to calculate x and y manually
  x = sum(bw)/len(bw)
  y = np.std(bw, ddof=1)
  return x, y, len(bw)



path_seg = "/home/zahaib/zahaibVM/convivaProj/convivaData/segment_traces_10_extend/"
path_syn =  "/home/zahaib/zahaibVM/convivaProj/convivaData/fit_trace_0_7500_0_15000/"
best_seg = "comparison_segment10_desktop_vod_allconfig_default_25_50_75_nsdi.txt"
best_syn = "comparison_10800_allconfig_default_25_50_75_bugfix1224.txt"

f_best_syn = open(best_syn, 'r')
temp = list()
for i in f_best_syn:
  if len(i.split(" ")) < 10: continue
  name = i.split(" ")[0]
  best = float(i.split(" ")[10].replace(")",""))
  bw, std, l = getBWandStd(path_syn, name)
  #print i
  #print bw, std, name, l, best
  #break
  if bw > 3000 and bw < 3500 and std < 1000 and std>500:
    temp.append(best)
  if bw > 3000 and bw < 3500 and std < 1000 and std>500 and best < 0.75:
    print name, bw, std, l, best

print len(temp)
print max(temp)
print np.percentile(temp, 90)
print np.percentile(temp, 50)
print np.percentile(temp, 10)
print min(temp)
