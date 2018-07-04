import os

o = os.listdir("/home/zahaib/ABRTuner/auto_exp/pensieve_total1500_100_0_invertold/")
for i in o:
    s = i.split("_")[0]
    #if s !="total300-100-0-pensieve-pensvid": continue
    if s !="pensieve-pensvid": continue
    print i
    os.system("cp /home/zahaib/ABRTuner/auto_exp/pensieve_total1500_100_0_invertold/"+str(i)+" "+"/home/zahaib/ABRTuner/auto_exp/final_eval_mpctuner_pensieve_lowbw/"+"100-0-"+str(i))
    #print "cp /home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/"+str(i)+" "+"/home/zahaib/ABRTuner/auto_exp/pensieve_default_ourtrain/oritinal-"+str(i)
   
