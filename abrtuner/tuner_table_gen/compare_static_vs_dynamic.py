import os, sys
import numpy as np
if len(sys.argv) < 3:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to output of compare_dynamic_all.py>"
  sys.exit()

f_default = open(sys.argv[1])
f_dynamic = open(sys.argv[2])
file_path_allconfig = "/home/yun/simulation/desktop_8000_trace_pen/"
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

default_config = dict()
dynamic_config = dict()
for f in f_default:
    if len(f.split(",")) < 10:
        continue
    fileName = f.split("QoE")[0].split("/")[-1]
    name = fileName.split(" ")[0]

    #bw, std =  getBWandStd(file_path_allconfig, name)
    #if bw > 4300: continue

    out= f.split("\n")[0].split("OrderedDict")[1].replace('\'','').replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(" dominant bitrate:")[0].split(" ")
    # without all state
    step = 4
    # with all state
    step = 7
    default_config[name] = dict()
    for i in range(0,len(out)/step):
        p1 = float(out[i*step])
        p2 = float(out[i*step+1])
        avgbr = float(out[i*step+2])
        rebuf = float(out[i*step+3])
        default_config[name][p2] = (avgbr, rebuf)

for f in f_dynamic:
    session = f.split(" ")[0].split("/")[-1]
    bsm =f.split(" ")[2]
    cell = f.split(" ")[4]
    #bw, std = getBWandStd(file_path_allconfig, session)
    #if bw> 4300: continue
    
    playtime = 1000*float(f.split(" ")[14])
    #bufftime = 1000*(float(f.split(" ")[16])-0.01)
    bufftime = 1000*(float(f.split(" ")[16]))
        #if bufftime == 0.01:
        #  bufftime=0.0
    size = 8*float(f.split(" ")[18])
    if session not in dynamic_config.keys():
        dynamic_config[session] = dict()
    dynamic_config[session][cell] = (size/playtime, 100*bufftime/(playtime+bufftime))

#print dynamic_config

default_avgbr_list = list()
default_rebuf_list = list()
dynamic_avgbr_list = list()
dynamic_rebuf_list = list()
target_cell = 500
target_static = -10



for session in default_config.keys():
    if session not in dynamic_config.keys(): continue
    if target_cell not in dynamic_config[session].keys(): continue
    if target_static not in default_config[session].keys(): continue
    default_avgbr_list.append(default_config[session][target_static][0])    
    default_rebuf_list.append(default_config[session][target_static][1])    
    dynamic_avgbr_list.append(dynamic_config[session][target_cell][0])    
    dynamic_rebuf_list.append(dynamic_config[session][target_cell][1])   

print np.percentile(default_avgbr_list, 50) 
print np.percentile(dynamic_avgbr_list, 50) 
print np.percentile(default_rebuf_list, 95) 
print np.percentile(dynamic_rebuf_list, 95) 
