import os
import numpy as np
import sys
import bandwidth_profile

#size_Envivio = {0:[207189,219272,134208,204651,164461,230942,136746,150366,193697,193362,189146,153391,195591,177177,190923,155030,185660,164741,179442,131632,198676,115285,148044,181978,200708,177663,176815,109489,203211,196841,161524,151656,182521,172804,211407,171710,170866,178753,175461,184494,154382,206330,175870,178679,173567,172998,189473,172737,163181,181882,186151,164281,172026,173011,162488,201781,176856,137099,57015,234214,172494,184405,61936,43268,81580], 1:[361158,370284,246858,357922,264156,371586,241808,270621,327839,334864,313171,253682,348331,319047,311275,282933,308899,289234,307870,207573,354546,208087,305510,364291,331480,298846,298034,195290,327636,354076,261457,272419,344053,307537,344697,301834,261403,332467,324205,276260,260969,357539,301214,320538,292593,290952,325914,285965,266844,327707,308757,271734,313780,284833,295589,331270,307411,224531,94934,385537,306688,310705,95847,78651,162260], 2:[604139,577615,418531,555427,469238,614632,393715,428426,594788,527047,460827,500774,621760,556545,476734,417508,552639,462442,552256,303234,522859,337637,471941,598737,560588,487684,479873,284277,564825,546935,394056,442514,610493,523364,574457,499175,412705,586327,560284,476697,408166,570011,502061,569274,444948,507586,525450,541979,391886,539537,506089,408110,515570,462132,574826,523754,572621,344553,157240,610010,460871,480012,169331,126490,236234], 3:[1184008,1123706,854424,1150093,902304,1237428,763515,840707,1279590,930828,996858,950867,1285933,1049248,984261,876058,1054391,875132,996451,660126,1032091,626844,949274,1197901,1001670,994288,925341,623084,977347,1184694,766276,834528,1285071,1017030,1080835,1078945,788728,1165402,1123991,937434,804808,1178153,922947,1175468,903392,970351,1094905,931644,854957,1179875,978233,794797,1073857,942081,1074761,1033448,1181202,660582,297985,1188866,910001,974311,314327,221329,445973], 4:[1680951,1637558,1371111,1684293,1400042,1792609,1213669,1191552,1888982,1381292,1593129,1384566,1918298,1605664,1356382,1278860,1580165,1315506,1642869,928190,1416000,865548,1284104,1692271,1504744,1484004,1405086,891371,1401736,1743545,1084561,1099310,1789869,1675658,1636106,1492615,1200522,1787763,1690817,1459339,1250444,1691788,1403315,1732710,1270067,1514363,1615320,1507682,1260622,1784654,1352160,1115913,1637646,1546975,1637443,1475444,1616179,1113960,466635,1727956,1316739,1373312,458410,320487,573826]}
#
size_Envivio = {5:[2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658],4:[1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412],3:[1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850],2:[668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450],1:[450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954], 0:[181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270]}


if len(sys.argv) < 6:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to log dir> <path to output dir> <num_schemes> <reference scheme> <bw limit>"
  sys.exit()

num_schemes = int(sys.argv[3])
ref_scheme = sys.argv[4]
bw_limit = int(sys.argv[5])

if ref_scheme not in ['hyb', 'online-tuner', 'robustmpc', 'mpc-tuner', 'bola', 'bola-tuner']:
	print >> sys.stderr, "ref_scheme needs to be one of " + ['hyb', 'online-tuner', 'robustmpc', 'mpc-tuner', 'bola', 'bola-tuner']
	sys.exit()
#Envivio
#video_to_index = {5:0, 4:1, 3:2, 2:3, 1:4}
video_to_index = {6:0, 5:1, 4:2, 3:3, 2:4, 1:5}
index_to_bitrate = {0:300,1:750,2:1200,3:1850,4:2850,5:4300}
num_chunks_video = 49
set_to_use = set()

if bw_limit == 1:
    set_to_use = bandwidth_profile.lt_1000
elif bw_limit == 2:
    set_to_use = bandwidth_profile.lt_2000
elif bw_limit == 3:
    set_to_use = bandwidth_profile.lt_3000
elif bw_limit == 4:
    set_to_use = bandwidth_profile.lt_4000
elif bw_limit == 5:
    set_to_use = bandwidth_profile.lt_4500
elif bw_limit == 6:
    set_to_use = bandwidth_profile.lt_6000
elif bw_limit == 33:
    set_to_use = bandwidth_profile.gt_3000    
elif bw_limit == 44:
    set_to_use = bandwidth_profile.gt_4000
elif bw_limit == 55:
    set_to_use = bandwidth_profile.gt_5000
elif bw_limit == 66:
    set_to_use = bandwidth_profile.gt_6000
elif bw_limit == 77:
    set_to_use = bandwidth_profile.gt_7000
elif bw_limit == 88:
    set_to_use = bandwidth_profile.gt_8000
else:
    set_to_use = bandwidth_profile.lt_15000


#log_path = "/home/zahaib/zahaibVM/convivaProj/automation_zahaib/trace_500_out/"
log_path = sys.argv[1].rstrip("/") + "/"
output_dir = sys.argv[2].rstrip("/") + "/"
rebuf_penalty = 4.3 #4.3
change_penalty = 1.0 #1
file_names = os.listdir(log_path)
dash_QoE = dict()
average_QoE = dict()
file_name_dict = dict()
rebuf_impacted = set()
bitrate_pdf = dict()
name_to_actualfilename = dict()
for file_name in file_names:
    if "DS_" in file_name: continue
    print(file_name)
    fname = "_".join(file_name.split("_")[1:6]) + ".txt"
    if fname not in file_name_dict.keys():
      file_name_dict[fname] = dict()
    scheme = file_name.split("_")[0]
    name = file_name.split("_")[4] + file_name.split("_")[5]
    name_to_actualfilename[name] = fname
    if name not in set_to_use:
        continue
    if scheme not in bitrate_pdf:
        bitrate_pdf[scheme] = dict.fromkeys(range(6), 0)
    #name = '_'.join(file_name.split(" ")[1:])
    #continue    
    f = open(log_path+file_name,"r")
    #continue
    chunks_dash = dict()
    buffering_dash = []
    last_quality = 0
    total_quality_change_events = 0
    total_quality_change = 0
    total_quality_change_log = 0.0
    for line in f:
        #print line
        line = line.replace("\n","").replace(",","").replace("\"","")
        #print line
        chunk  = line.split(" ")[4:]
        #print chunk
        
        if "chunk" in chunk[0]:
            #print chunk[2]
            temp1 = int(chunk[2].split("video")[1].split("/")[0])
            #print temp1, video_to_index[temp1]
            quality = video_to_index[temp1]
            bitrate_pdf[scheme][quality] += 1
            ID = int(chunk[2].split("/")[-1].split(".")[0])
            # print quality, ID
            size = size_Envivio[quality][ID-1]
            #print quality, ID, size
            
            start = float(chunk[3].split("=")[-1])
            #start = float(chunk[4].split("=")[-1])
            end = float(chunk[5].split("=")[-1])
            bufferlen = float(chunk[7].split("=")[-1])
            play = float(chunk[6].split("=")[-1])
            chunks_dash[ID] = dict()
            #chunks_dash[ID]["bitrate"] = bitrate
            chunks_dash[ID]["size"] = size
            chunks_dash[ID]["start"] = start
            chunks_dash[ID]["end"] = end
            chunks_dash[ID]["bufferlen"] = bufferlen
            chunks_dash[ID]["play"] = play
            chunks_dash[ID]["bitrate"] = index_to_bitrate[quality]
            if ID == 1:
                last_quality = quality
            else:
                if quality != last_quality:
                    total_quality_change_events += 1
                    total_quality_change += abs(index_to_bitrate[last_quality] - index_to_bitrate[quality])
                    total_quality_change_log += abs(np.log(index_to_bitrate[quality] / float(index_to_bitrate[0])) - \
                                                np.log(index_to_bitrate[last_quality] / float(index_to_bitrate[0]))) 
                    last_quality = quality

            #if file_name=="desktop_dash_trace_4_out_txt": print chunks_dash[ID]
        if "buffering" in chunk[0]:
            start = float(chunk[4].split("=")[-1])/1000.0
            end = float(chunk[5].split("=")[-1])/1000.0
            play = float(chunk[7].split("=")[-1])
            bufferlen = float(chunk[8].split("=")[-1])-4
            buffering_dash.append([start,play,bufferlen,end])
            #print buffering_dash[-1], buffering_dash[-1][3]-buffering_dash[-1][0]
        #break
    # print chunks_dash
    buffering_dash = buffering_dash[1:]
    total_size = 0.0
    total_size_log = 0.0
    total_time = 0.0
    total_buffering = 0.0

    # print len(buffering_dash), len(chunks_dash.keys()), buffering_dash

    print ("total quality change events=", total_quality_change_events, "total_quality_change=", total_quality_change)
    for i in buffering_dash:
        total_buffering+=((i[3]-i[0]))
    print ("total buffering events=", len(buffering_dash), "total buffering time=",total_buffering)
    # for i in range(1,len(chunks_dash) + 1):
    #     total_size+=chunks_dash[i]["size"]
    # avgBitrate = round((total_size*8/(4.0*len(chunks_dash)))/1000.0,2)

    for i in range(1, len(chunks_dash) + 1):
    	total_size += chunks_dash[i]["bitrate"]
        total_size_log += np.log(chunks_dash[i]["bitrate"] / float(index_to_bitrate[0]))

    avgBitrate = round(total_size / float(len(chunks_dash)) ,2)

    print ("total bitrate=", total_size)

    rebufRatio = total_buffering/(4.0*len(chunks_dash)+total_buffering)
    QoE = (total_size / 1000.0 - rebuf_penalty * total_buffering - change_penalty * (total_quality_change / 1000.0)) / float(len(chunks_dash))
    QoE_log = (total_size_log - rebuf_penalty * total_buffering - change_penalty * total_quality_change_log) / float(len(chunks_dash))

    print ("avgBitrate=", avgBitrate, "rebufRatio=", rebufRatio, "QoE=", QoE)    	

    #dash_QoE[file_name] = (avgBitrate,rebufRatio, len(chunks_dash))
    print name, scheme
    # if name not in average_QoE.keys():
    #     average_QoE[name] = dict()
    if name not in dash_QoE.keys():
        dash_QoE[name] = dict()
    if scheme == "robustmpc" and rebufRatio > 0 and name not in rebuf_impacted:
        rebuf_impacted.add(name)
    #if scheme not in dash_QoE[name].keys():
    dash_QoE[name][scheme] = (avgBitrate,rebufRatio, len(chunks_dash), QoE, total_quality_change/float(len(chunks_dash)), QoE_log)
    # average_QoE[name][scheme] = (avgBitrate - rebuf_penalty * rebufRatio * 100)

    file_name_dict[fname][scheme] = (avgBitrate,rebufRatio, len(chunks_dash), QoE, total_quality_change/float(num_chunks_video))
    print (len(chunks_dash))
    print ("")

bitrate_cdf = dict()
rebuf_cdf = dict()
qoe_cdf = dict()
change_cdf = dict()
qoelog_cdf = dict()

bitrate_cdf_ri = dict()
rebuf_cdf_ri = dict()
qoe_cdf_ri = dict()
change_cdf_ri = dict()

bitrate_per_cdf = dict()
rebuf_per_cdf = dict()
qoe_per_cdf = dict()
change_per_cdf = dict()
qoelog_per_cdf = dict()

for i in dash_QoE.keys():
    if len(dash_QoE[i]) != num_schemes:
        continue
    for ii in dash_QoE[i].keys():
        if ii not in bitrate_cdf.keys():
            bitrate_cdf[ii] = []
        if ii not in rebuf_cdf.keys():
            rebuf_cdf[ii] = []
        if ii not in qoe_cdf.keys():
            qoe_cdf[ii] = []            
        if ii not in change_cdf.keys():
            change_cdf[ii] = []            
        if ii not in qoelog_cdf.keys():
            qoelog_cdf[ii] = []

        if ii not in bitrate_cdf_ri.keys():
            bitrate_cdf_ri[ii] = []
        if ii not in rebuf_cdf_ri.keys():
            rebuf_cdf_ri[ii] = []
        if ii not in qoe_cdf_ri.keys():
            qoe_cdf_ri[ii] = []
        if ii not in change_cdf_ri.keys():
            change_cdf_ri[ii] = []


        if ii != ref_scheme and ii not in rebuf_per_cdf.keys():
            rebuf_per_cdf[ii] = []
        if ii != ref_scheme and ii not in bitrate_per_cdf.keys():
            bitrate_per_cdf[ii] = []
        if ii != ref_scheme and ii not in qoe_per_cdf.keys():
            qoe_per_cdf[ii] = []
        if ii != ref_scheme and ii not in change_per_cdf.keys():
            change_per_cdf[ii] = []
        if ii != ref_scheme and ii not in qoelog_per_cdf.keys():
            qoelog_per_cdf[ii] = []

        bitrate_cdf[ii].append(float(dash_QoE[i][ii][0]))
        rebuf_cdf[ii].append(100*float(dash_QoE[i][ii][1]))
        qoe_cdf[ii].append(float(dash_QoE[i][ii][3]))
        change_cdf[ii].append(float(dash_QoE[i][ii][4]))
        qoelog_cdf[ii].append(float(dash_QoE[i][ii][5]))

        #if i == '291022':
        #if float(dash_QoE[i][ii][1]) < float(dash_QoE[i]['robustmpc'][1]) and dash_QoE[i][ii][3] < dash_QoE[i]['robustmpc'][3]:
          #print >> sys.stderr, i, ii, dash_QoE[i][ii]
          #print >> sys.stderr, i, ii, dash_QoE[i][ii][3], dash_QoE[i]['robustmpc'][3], dash_QoE[i][ii][1] * 100.0, dash_QoE[i]['robustmpc'][1] * 100.0



        if i in rebuf_impacted:
          #if i == '291022':
          #if float(dash_QoE[i][ii][1]) < float(dash_QoE[i]['robustmpc'][1]) and dash_QoE[i][ii][3] < dash_QoE[i]['robustmpc'][3]:
            #print >> sys.stderr, i, ii, dash_QoE[i][ii], dash_QoE[i]['robustmpc']
            #cprint >> sys.stderr, i, ii, dash_QoE[i][ii][3], dash_QoE[i]['robustmpc'][3], dash_QoE[i][ii][1] * 100.0, dash_QoE[i]['robustmpc'][1] * 100.0
          bitrate_cdf_ri[ii].append(float(dash_QoE[i][ii][0]))
          rebuf_cdf_ri[ii].append(100*float(dash_QoE[i][ii][1]))
          qoe_cdf_ri[ii].append(float(dash_QoE[i][ii][3]))
          change_cdf_ri[ii].append(float(dash_QoE[i][ii][4]))

        if ii != ref_scheme:
            bitrate_per_cdf[ii].append(100*(float(dash_QoE[i][ref_scheme][0]) - float(dash_QoE[i][ii][0]))/float(dash_QoE[i][ii][0]))
            rebuf_per_cdf[ii].append(100*(float(dash_QoE[i][ii][1]) - float(dash_QoE[i][ref_scheme][1])))
            try:
              # qoe_diff = 100*(float(dash_QoE[i][ref_scheme][3]) - float(dash_QoE[i][ii][3]))/abs(float(dash_QoE[i][ii][3]))
              # if ii == "robustmpc" and qoe_diff < 0:
              #   print name_to_actualfilename[i], qoe_diff
              qoe_per_cdf[ii].append(100*(float(dash_QoE[i][ref_scheme][3]) - float(dash_QoE[i][ii][3]))/abs(float(dash_QoE[i][ii][3])))
            except ZeroDivisionError:
              qoe_per_cdf[ii].append(0)
            #if 100*(float(dash_QoE[i]["online-tuner"][3]) - float(dash_QoE[i][ii][3]))/float(dash_QoE[i][ii][3]) < -30:
            #    print >> sys.stderr, i, dash_QoE[i]["online-tuner"][3], dash_QoE[i][ii][3], float(dash_QoE[i]["online-tuner"][3]) - float(dash_QoE[i][ii][3])
            if float(dash_QoE[i][ii][4]) == 0:
                change_per_cdf[ii].append(100*(float(dash_QoE[i][ii][4]) - float(dash_QoE[i][ref_scheme][4]))/0.01)
            else:	
                change_per_cdf[ii].append(100*(float(dash_QoE[i][ii][4]) - float(dash_QoE[i][ref_scheme][4]))/float(dash_QoE[i][ii][4]))

for sh in bitrate_cdf.keys():
    f_out = open(output_dir + "/cdf_bitrate_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(bitrate_cdf[sh], i))+"\n")
    f_out.close()
for sh in rebuf_cdf.keys():
    f_out = open(output_dir +"/cdf_rebuf_"+str(sh)+".txt",'w')
    for i in np.arange(0,100.01, 0.1):
        f_out.write(str(i)+" "+str(np.percentile(rebuf_cdf[sh], i))+"\n")
    f_out.close()
for sh in qoe_cdf.keys():
    f_out = open(output_dir +"/cdf_qoe_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(qoe_cdf[sh], i))+"\n")
    f_out.close()
for sh in change_cdf.keys():
    f_out = open(output_dir +"/cdf_change_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(change_cdf[sh], i))+"\n")
    f_out.close()

#for sh in bitrate_cdf_ri.keys():
#    f_out = open(output_dir + "/cdf_bitrate_ri_"+str(sh)+".txt",'w')
#    for i in range(0,101):
#        f_out.write(str(i)+" "+str(np.percentile(bitrate_cdf_ri[sh], i))+"\n")
#    f_out.close()
#for sh in rebuf_cdf_ri.keys():
#    f_out = open(output_dir +"/cdf_rebuf_ri_"+str(sh)+".txt",'w')
#    for i in np.arange(0,100.01, 0.1):
#        f_out.write(str(i)+" "+str(np.percentile(rebuf_cdf_ri[sh], i))+"\n")
#    f_out.close()
#for sh in qoe_cdf_ri.keys():
#    f_out = open(output_dir +"/cdf_qoe_ri"+str(sh)+".txt",'w')
#    for i in range(0,101):
#        f_out.write(str(i)+" "+str(np.percentile(qoe_cdf_ri[sh], i))+"\n")
#    f_out.close()
#for sh in change_cdf_ri.keys():
#    f_out = open(output_dir +"/cdf_change_ri_"+str(sh)+".txt",'w')
#    for i in range(0,101):
#        f_out.write(str(i)+" "+str(np.percentile(change_cdf_ri[sh], i))+"\n")
#    f_out.close()




for sh in bitrate_per_cdf.keys():
    f_out = open(output_dir +"/cdf_bitrate_percentage_diff_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(bitrate_per_cdf[sh], i))+"\n")
    f_out.close()
for sh in rebuf_per_cdf.keys():
    f_out = open(output_dir + "/cdf_rebuf_percentage_diff_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(rebuf_per_cdf[sh], i))+"\n")
    f_out.close()
for sh in qoe_per_cdf.keys():
    f_out = open(output_dir + "/cdf_qoe_percentage_diff_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(qoe_per_cdf[sh], i))+"\n")
    f_out.close()
for sh in change_per_cdf.keys():
    f_out = open(output_dir + "/cdf_change_percentage_diff_"+str(sh)+".txt",'w')
    for i in range(0,101):
        f_out.write(str(i)+" "+str(np.percentile(change_per_cdf[sh], i))+"\n")
    f_out.close()

print "\navg. bitrate"
for sh in bitrate_cdf.keys():
  print sh, np.mean(bitrate_cdf[sh]), np.std(bitrate_cdf[sh]), np.percentile(bitrate_cdf[sh], 50), len(bitrate_cdf[sh])

print "\nrebuf"
for sh in rebuf_cdf.keys():
  print sh, np.mean(rebuf_cdf[sh]),np.std(rebuf_cdf[sh]), np.percentile(rebuf_cdf[sh], 50), np.mean(rebuf_cdf[sh]) * rebuf_penalty, len(rebuf_cdf[sh])

print "\nchange"
for sh in change_cdf.keys():
  print sh, np.mean(change_cdf[sh]),np.std(change_cdf[sh]), np.percentile(change_cdf[sh], 50), np.mean(change_cdf[sh]) * change_penalty, len(change_cdf[sh])

print "\nQoE"
for sh in qoe_cdf.keys():
  print sh, np.mean(qoe_cdf[sh]), np.std(qoe_cdf[sh]), np.percentile(qoe_cdf[sh], 50), np.mean(qoe_cdf[sh]), len(qoe_cdf[sh])

print ""
for scheme in sorted(bitrate_pdf.keys()):
  if scheme == "online-tuner":
    print "online-tuner",
  elif scheme == "pensieve-pensvid":
    print "pensieve",
  else:
    print scheme, 
  for br in sorted(bitrate_pdf[scheme]):
    print round((bitrate_pdf[scheme][br] / float(sum(bitrate_pdf[scheme].values()))) * 100, 2),
  print ""
#print bitrate_pdf
# log reward
# log_bit_rate = np.log(VIDEO_BIT_RATE[chunk_quality] / float(VIDEO_BIT_RATE[0]))
# log_last_bit_rate = np.log(VIDEO_BIT_RATE[last_quality] / float(VIDEO_BIT_RATE[0]))
# bitrate_sum += log_bit_rate
# smoothness_diffs += abs(log_bit_rate - log_last_bit_rate)
# reward = (bitrate_sum) - (4.3*curr_rebuffer_time) - (smoothness_diffs)

# --log reward--
# log_bit_rate = np.log(VIDEO_BIT_RATE[post_data['lastquality']] / float(VIDEO_BIT_RATE[0]))   
# log_last_bit_rate = np.log(self.input_dict['last_bit_rate'] / float(VIDEO_BIT_RATE[0]))

# reward = log_bit_rate \
#          - 4.3 * rebuffer_time / M_IN_K \
#          - SMOOTH_PENALTY * np.abs(log_bit_rate - log_last_bit_rate)


