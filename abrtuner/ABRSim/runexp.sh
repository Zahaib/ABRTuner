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

> out_performance.txt
while read line; do
        echo $line
	python simulation.py $line  > tmp.txt
        echo $line >> out_performance.txt
        tl_1=$(grep 'initialBSM' tmp.txt | cut -d ' ' -f8-13 | head -n 1 | sed ':a;N;$!ba;s/\n/ /g' | sed "s/ /-/g")
        tl_2=$(grep 'initialBSM' tmp.txt | cut -d ' ' -f8-13 | tail -n 1 | sed ':a;N;$!ba;s/\n/ /g' | sed "s/ /-/g")
        tl="TUNER:"$tl_1"++++MPC:"$tl_2
        #echo $tl
        echo $tl >> out_performance.txt
        sed -i '$ d' tmp.txt
        lines=$(wc -l < tmp.txt)
        endfirst=$(grep -n "initialBSM" tmp.txt | cut -f1 -d:)
        headcond=$((endfirst-1))
        tailcond=$((lines-endfirst))
        #echo $lines, $endfirst, $headcond, $tailcond
        head -n $headcond tmp.txt > a.txt
        tail -n $tailcond tmp.txt > b.txt
        #gnuplot -e "set output '1.png'" time_series_plot.gp
        echo $tl
        a="asdf_adfai_asdfa_adf_asdf_asdf asdf asdf asdfasdf asdf asdf asdf asdf"
        gnuplot -c time_series_plot.gp $tl
        name=$(echo $line | cut -d\/ -f1 --complement)
        mv 1.png time_series2/$name.png
done < $1
