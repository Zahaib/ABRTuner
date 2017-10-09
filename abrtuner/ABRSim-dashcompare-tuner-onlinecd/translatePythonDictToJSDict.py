from low_bw_syth_no_abort_bugfix1224_performance_vector import *
#from testtable import *

dic = ""
print "var syth_sigcomm_desktop_performance_table = {",
#dic+="var syth_sigcomm_desktop_performance_table = {"
for i in range(100, 3100, 100):
    dict_name_backup = "low_bw_syth_hyb_no_abort_bugfix1224_table_"+str(i)
    #dict_name_backup = "test_"+str(i)
    performance_t_backup = (globals()[dict_name_backup])
    dic+=str(i)+":{"
    for k in performance_t_backup:
        dic+="\""+str(k[0])+"-"+str(k[1])+"\":["
        for j in performance_t_backup[k]:
            dic+=str(j)+","
        dic = dic[:-1]
        dic+="]," 
    dic = dic[:-1]

    dic+="},"
dic = dic[:-1]
dic+="}"
print dic


