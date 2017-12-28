f = open("table_selection_test_bw_std_cellsize_desktop.txt",'r')
for s in f:
    temp = s.split(".out ")[1]
    temp = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").replace("\n","").split(" ")
    i=0
    while(i+2<len(temp)):
        print temp[i],temp[i+1], temp[i+2]
        i+=3
