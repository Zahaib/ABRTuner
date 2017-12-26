#!/usr/bin/python

import os, sys
import numpy as np
sys.path.append('../')


if len(sys.argv) < 2:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to file>"
  sys.exit()

file_name = sys.argv[1]

log_lines = list()
log_conf = dict()
if len(sys.argv) == 3:
  log_lines = open(sys.argv[2]).readlines()
  for l in log_lines:
    l = l.rstrip()
    row = l.split("\t")
    chunk = int(row[1])
    conf = float(row[-1])
    if chunk not in log_conf.keys():
      log_conf[chunk] = conf
else:
  a = range(0,49)
  log_conf = dict.fromkeys(a,0.25)

lines = open(file_name).readlines()

size_Envivio = {5:[2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658],4:[1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412],3:[1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850],2:[668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450],1:[450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954], 0:[181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270]}

print(file_name)
video_to_index = {6:0, 5:1, 4:2, 3:3, 2:4, 1:5}
index_to_bitrate = {0:300,1:750,2:1200,3:1850,4:2850,5:4300}
scheme = file_name.split("_")[0]
name = file_name.split("_")[4] + file_name.split("_")[5]
chunks_dash = dict()
buffering_dash = []
quality = 0
ID = 0
first = True
last_quality = 0
bw = 0
for line in lines:
    line = line.replace("\n","").replace(",","").replace("\"","")
    chunk  = line.split(" ")[4:]

    if "chunk" in chunk[0]:
        temp1 = int(chunk[2].split("video")[1].split("/")[0])
        last_quality = quality
        quality = video_to_index[temp1]
        ID = int(chunk[2].split("/")[-1].split(".")[0])
        size = size_Envivio[quality][ID-1]
        start = float(chunk[3].split("=")[-1]) / 1000.0
        end = float(chunk[5].split("=")[-1]) / 1000.0
        bufferlen = float(chunk[7].split("=")[-1])
        play = float(chunk[6].split("=")[-1])
        chunks_dash[ID] = dict()
        chunks_dash[ID]["start"] = start
        chunks_dash[ID]["end"] = end
        chunks_dash[ID]["bufferlen"] = bufferlen
        chunks_dash[ID]["play"] = play
        chunks_dash[ID]["bitrate"] = index_to_bitrate[quality]
        bw = ((size * 8) / 1000000.0) / (end - start)
#        print start, bw
#        print end, bw
        print 'downloaded' + '\t' + \
              str(round(end,1)) + '\t' + \
              str(ID) + '\t' + \
              str(max(round(bufferlen,2) - 4.0,0)) + '\t' + \
              str(index_to_bitrate[last_quality]) + '\t' + \
              str(log_conf[ID-1]) + '\t' + \
              str(bw)
        print 'appended' + '\t' + \
              str(round(end,1)) + '\t' + \
              str(ID) + '\t' + \
              str(round(bufferlen,2)) + '\t' + \
              str(index_to_bitrate[quality]) + '\t' + \
              str(log_conf[ID-1]) + '\t' + \
              str(bw)

 
    if "buffering" in chunk[0]:
        if first:
          first = False
          continue
        start = float(chunk[4].split("=")[-1])/1000.0
        end = float(chunk[5].split("=")[-1])/1000.0
        play = float(chunk[7].split("=")[-1])
        bufferlen = float(chunk[8].split("=")[-1])-4
        buffering_dash.append([start,play,bufferlen,end])
        print 'rebuf_start' + '\t' + \
              str(round(start,1)) + '\t' + \
              str(ID) + '\t' + \
              str(0) + '\t' + \
              str(index_to_bitrate[quality]) + '\t' + \
              str(log_conf[ID-1]) + '\t' + \
              str(bw)







#        print 'rebuf_end' + '\t' + \
#              str(round(end,1)) + '\t' + \
#              str(ID) + '\t' + \
#              str(round(bufferlen,2) + 4) + '\t' + \
#              str(index_to_bitrate[quality])




#