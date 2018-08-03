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

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    output,errors = p.communicate()
    print 'OUTPUT: ' + output
    if p.returncode:
        raise Exception(errors)
    return str(output)

#file_path = "/Users/ynam/emulation/automation/dash_mobile_trace_out_bandwidth/"
file_path = "/home/zahaib/convivaProj/convivaData/precisionserver_history_clientIp_time_day_low_bw/"
file_names = os.listdir(file_path)

for file_name in file_names:
    print file_name
    if file_name==".DS_Store": continue
    name = file_name.split("_bandwidth")[0]
    cmd = "python simulation.py "+ file_path+file_name+" > " +name+"_simulator_out_withoutgap.txt"
    #print run_cmd
    pid_out = run_cmd(cmd)
