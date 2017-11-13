import os

o = os.listdir("/home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/")
for i in o:
    s = i.split("_")[0]
    if s !="pensieve-pensvid": continue
    print i
    os.system("cp /home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/"+str(i)+" "+"/home/zahaib/ABRTuner/auto_exp/pensieve_ourtrace_250/original-"+str(i))
    #print "cp /home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/"+str(i)+" "+"/home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/oritinal-"+str(i)
   
