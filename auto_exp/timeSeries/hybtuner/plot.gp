set term pngcairo size 640,640 dashed dl 0.1 font ",16"
set output 'hyb_vs_hybtuner.png'
set multiplot layout 3,1

set ylabel 'BW (Mbps)'
set xrange [41:48]
set yrange [0.8:2.2]
set ytics 0.4
set key samplen 1
set datafile separator '\t'
set arrow from 44, graph 0 to 44,graph 1 nohead lw 3 dt 2
set label "change point\ndetected" at 44.5,1.3 tc rgb 'red'
set arrow from 45, graph 0.4 to 44.1, graph 0.75 lw 3
plot 'online2.txt' u 3:7 with lines dt 2 lw 3 lc rgb 'red' t 'Bandwidth', \

unset label
unset arrow
set ytics nomirror
set yrange [0:1]
set xrange [41:48]
#set xlabel 'Chunk number'
set ylabel 'Beta'
set key top left
set arrow from 44, graph 0 to 44,graph 1 nohead lw 3 dt 2
set label "HYBTuner adapts beta" at 44.5, 0.9 tc rgb 'red'
set arrow from 45, graph 0.8 to 44.1, graph 0.6 lw 3
plot 'hyb2.txt' u 3:6 with lines lw 3 axes x1y1 t 'HYB', \
'online2.txt' u 3:6 with lines lw 3 dt 2 axes x1y1 t 'HYBTuner'

unset label
unset arrow
set yrange [0:4.4]
set xrange [41:48]
set ylabel 'Bitrate (Mbps)'
set xlabel 'Chunk Number'
set key top left
set key samplen 1
set ytics 1.1
set arrow from 44, graph 0 to 44,graph 1 nohead lw 3 dt 2
set label "HYBTuner switches up" at 44.5, 3.7 tc rgb 'red'
set arrow from 44.7, graph 0.7 to 44.9, graph 0.22 lw 3
plot 'hyb2.txt' u 3:($5/1000) with lines lw 3 axes x1y1 t 'HYB', \
'online2.txt' u 3:($5/1000) with lines lw 3 dt 2 axes x1y1 t 'HYBTuner'
unset multiplot 


#reset
#set term pngcairo size 640,640 dashed dl 0.1 font ",16"
#set output 'badqoe_instance_noappend.png'
#set multiplot layout 3,1
#
#set ylabel 'BW (Mbps)'
#set xrange [0:200]
#set ytics nomirror
#set y2tics nomirror
##set y2label 'BW Mbps'
#set yrange [3.6:4.4]
#set y2range [3.6:4.4]
#set ytics 0.2
#set y2tics 0.2
#set key samplen 1
#plot 'bw_emulated.txt' u 1:2 with lines dt 2 lw 3 lc rgb 'red' t 'Bandwidth'
#
#set y2tics nomirror
#set ytics nomirror
#set y2range [0:4.5]
#set yrange [0:15]
#set xrange [0:200]
#set y2tics 1
##set xlabel 'Time (sec)'
#set ylabel 'Buffer (sec)'
#set y2label 'Bitrate (Mbps)'
#set key samplen 1
#set ytics 3
#plot 'robust_noappend_timeline.txt' u 2:4 with lines lw 3 axes x1y1 t 'bufferlen', \
#'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 t 'bitrate'
#
#set y2tics nomirror
#set ytics nomirror
#set y2range [0:4.5]
#set yrange [0:15]
#set xrange [0:200]
#set y2tics 1
#set xlabel 'Time (sec)'
#set ylabel 'Buffer (sec)'
#set y2label 'Bitrate (Mbps)'
#plot 'online-tuner_noappend_timeline.txt' u 2:4 with lines lw 3 axes x1y1 notitle, \
#'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 notitle
#unset multiplot
#
#reset
#set term pngcairo size 640,480 dashed dl 0.1 font ",16"
#set output 'pensieve.png'
#set y2tics nomirror
#set ytics nomirror
#set y2range [0:4.5]
#set yrange [0:30]
#set xrange [0:200]
#set y2tics 1
##set xlabel 'Time (sec)'
#set ylabel 'Buffer (sec)'
#set y2label 'Bitrate (Mbps)'
#set key samplen 1
#set ytics 3
#plot 'pensieve_timeline.txt' u 2:4 with lines lw 3 axes x1y1 t 'bufferlen', \
#'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 t 'bitrate'
#
#reset
#set term pngcairo size 640, 480 dashed dl 0.1 font ",16"
#set output 'switchlock.png'
#set y2tics nomirror
#set ytics nomirror
#set y2range [0:4.5]
#set yrange [0:30]
#set xrange [0:200]
#set y2tics 1
#set xlabel 'Time (sec)'
#set ylabel 'Buffer (sec)'
#set y2label 'Bitrate (Mbps)'
#plot 'switchlock_timeline.txt' u 2:4 with lines lw 3 axes x1y1 notitle, \
#'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 notitle
#
