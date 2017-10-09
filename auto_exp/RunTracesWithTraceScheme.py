#!/usr/bin/python
import sys
import os
import random
import math
import subprocess
from optparse import OptionParser
import time
from datetime import datetime
import httplib
from os import walk
import time
import shlex

if len(sys.argv) < 3:
  print >> sys.stderr, "Incorrect usage...\nUsage: python " + sys.argv[0] + " <path to trace dir> <path to output dir>"
  sys.exit()
#from service import Service

#flag = False
#URLs = []
#scavenged_configs = list()

#if(len(sys.argv) == 1):
#    sys.exit("Missing file with list of URLs")
#else:
#    URLFile = sys.argv[1]


#usage = " %prog <URL list file path>"
#parser = OptionParser(usage=usage)

# blocking
def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    output,errors = p.communicate()
    print 'OUTPUT: ' + output
    if p.returncode:
        raise Exception(errors)
    return str(output)

# non-blocking
def run_process(cmd):
    process = subprocess.Popen(cmd, shell=True)
    return process
     
def KillUnwantedProcesses(plist):
    #pidL = []
    #for p in plist:
    #    print p
    #    cmd = "sudo ps -ef | grep " + p + " | grep -v grep | awk '{print $2}'"
    #    pid = run_cmd(cmd)
    #    print 'INKILLUNWANED :' + pid.split('\n')[0]
    #    pidL.append(pid.split('\n')[0])
    #    
    #for ids in pidL:
    #    cmd = "sudo kill -2 " + ids
    #    print cmd
    #    res = run_cmd(cmd)
    #    print 'Killed ' + str(ids)
    for p in plist:
        if(p.find("web-page-replay") > 0):
            cmd = "sudo pkill -2 -f " + p
        elif(p.find("chrome") > 0):
            cmd = "sudo pkill -9 -f " + p
        elif(p.find("apache2") > 0):
            cmd = "sudo service apache2 restart"
        else:
            cmd = "sudo pkill -9 -f " + p
        print cmd
        res = subprocess.call(cmd, shell=True)
        print 'Killed : ' + p
        time.sleep(5)
        #if(p.find("apache2") > 0):
        #    time.sleep(10)


import random
START = 0
END = 20
DURATION = 0.5
MIN_ = 800
MAX_ = 6400

def KillProcesses():
	cmd = "killall -9 node"
	subprocess.call(cmd, shell=True)
	cmd = "killall -9 \"chrome\""
	subprocess.call(cmd, shell=True)

def traceGenerator(start, end, min_, max_, duration,sessionid):
	temp = []
	mean = (min_+max_)/2
	std = mean*2
	for i in range(start, int(end/duration)):
		bw = random.randint(min_,max_)
		bw = 0
		while bw<min_ or bw>max_:
			bw = int(random.gauss(mean, std))
		#print random.gauss(mean, std)
		#print ""
		temp.append(bw)
	print len(temp)
	return temp

def traceToFile (trace, START, END, DURATION,sessionid):
	f = open("trace.txt", "w")
	time = 0
	interval = int(DURATION*60*1000)
	for i in trace:
		for ii in range(0, interval, 100):
			f.write(str(time)+" "+str(i)+"\n")
			time+=100
	f.close()

# dash, mpc, hyb, tuner, pensieve-pensvid, online-tuner, robustmpc
schemes = ["online-tuner"]
#trace_path = "/Users/ynam/emulation/automation/dash_mobile_trace/"
#trace_path_out = "/Users/ynam/emulation/automation/dash_mobile_trace_out/"
#trace_path = "/Users/ynam/emulation/compareWithMPC/compare_trace/"
#trace_path = "/Users/ynam/emulation/compareWithMPC/test_zahaib/"
#trace_path = "trace_500_pen/"
#outdir = "output/"
trace_path = sys.argv[1].rstrip("/") + "/"
outdir = sys.argv[2].rstrip("/") + "/"

def main():
    f_trace = os.listdir(trace_path)
    for i in f_trace:
        for scheme in schemes:
            print scheme
            trace = trace_path+i
            print trace
            output_temp = str(scheme)+"_"+str(i.split(".")[0])+"_out_txt"
            print output_temp
            complete_temp = []
            out_complete_list = os.listdir(outdir)
            for ff in out_complete_list:
                ff_temp = ff.split("/")[-1]
                fff = open(outdir+ff)
                if len(fff.read()) > 10:
                    complete_temp.append(ff_temp)

            if output_temp in complete_temp:
                print "already there"
                continue
            KillProcesses()
            time.sleep(5)
            chrome_start_cmd = "/usr/bin/google-chrome --disable-extensions --disable-component-extensions-with-background-pages --disk-cache-size=1 --enable-logging --v=1 --remote-debugging-port=9222"
            pid2 = subprocess.Popen(shlex.split(chrome_start_cmd), shell=False)
            time.sleep(5)
            script_cmd = "node /home/zahaib/ABRTuner/auto_exp/chrome_automationWithTraceScheme.js " + str(trace) +" "+str(scheme)
            print script_cmd
            pid = run_cmd(script_cmd)
            print "Copy Output"
            # check the path for chrome output log for Linux
            copy_output_cmd = "grep \"Yun Final\" ~/.config/google-chrome/chrome_debug.log > " + outdir + output_temp
            try:
                pid_out = run_cmd(copy_output_cmd)
            except:
                print "error in copy"
            print "done", trace
            print ""
        KillProcesses()
main()


