#!/bin/bash

#sed -i 's/nsteps = 2.0/nsteps = 3.0/g' helpers.py
#parallel -a dash_generated_trace_filelist.txt -j 48 python simulation.py >> v2-3steps-converge.txt
#
#sed -i 's/nsteps = 3.0/nsteps = 4.0/g' helpers.py
#parallel -a dash_generated_trace_filelist.txt -j 48 python simulation.py >> v2-4steps-converge.txt
#
#sed -i 's/nsteps = 4.0/nsteps = 5.0/g' helpers.py
#parallel -a dash_generated_trace_filelist.txt -j 48 python simulation.py >> v2-5steps-converge.txt
#
#sed -i 's/nsteps = 5.0/nsteps = 6.0/g' helpers.py
#parallel -a dash_generated_trace_filelist.txt -j 48 python simulation.py >> v2-6steps-converge.txt

while read line; do
        echo $line
	python simulation.py $line | sed '$ d' > tmp.txt
        gnuplot -e "set output '1.png'" time_series_plot.gp
        name=$(echo $line | cut -d\/ -f1 --complement)
        mv 1.png time_series/$name.png
done < $1
