set term pngcairo size 640,640 dashed dl 0.1 font ",16"
set output 'hyb_vs_hybtuner.png'
set multiplot layout 3,1

set ylabel 'BW (Mbps)'
set xrange [1:50]
#set yrange [1.0:1.9]
set ytics 0.5
set key samplen 1
set datafile separator '\t'
set arrow from 28.9, graph 0 to 28.9,graph 1 nohead lw 3 dt 2
set label "change point\ndetected" at 10.0,2.0 tc rgb 'red'
set arrow from 24.5, graph 0.4 to 28.3, graph 0.45 lw 3
plot 'mpct-185.txt' u 2:7 with lines dt 2 lw 3 lc rgb 'red' t 'Bandwidth', \

unset label
unset arrow
set ytics nomirror
set yrange [0:200]
set xrange [1:50]
#set xlabel 'Chunk number'
set ylabel 'BW discount factor'
set ytics 50
set key top left
set arrow from 28.9, graph 0 to 28.9,graph 1 nohead lw 3 dt 2
set label "HYBTuner\nadapts discount" at 32.5, 175 tc rgb 'red'
set arrow from 32, graph 0.9 to 29.1, graph 0.55 lw 3
plot 'rob-185.txt' u 2:6 with lines lw 3 axes x1y1 t 'RobustMPC', \
'mpct-185.txt' u 2:6 with lines lw 3 dt 2 axes x1y1 t 'MPC+ABRTuner'

unset label
unset arrow
set yrange [0:25]
set xrange [1:50]
set ylabel 'Buffer (sec)'
set xlabel 'Chunk Number'
set key top left
set key samplen 1
set ytics 6
#set arrow from 44, graph 0 to 44,graph 1 nohead lw 3 dt 2
set label "RobustMPC rebuffers" at 30.0, 22.0 tc rgb 'red'
set arrow from 44.7, graph 0.7 to 44.9, graph 0.12 lw 3
plot 'rob-185.txt' u 2:4 with lines lw 3 axes x1y1 notitle 'RobustMPC', \
'mpct-185.txt' u 2:4 with lines lw 3 axes x1y1 notitle 'MPC+ABRTuner'


#unset label
#unset arrow
#set yrange [0:6]
#set xrange [1:50]
#set ylabel 'Bitrate (sec)'
#set xlabel 'Chunk Number'
#set key top left
#set key samplen 1
#set ytics 6
#set arrow from 44, graph 0 to 44,graph 1 nohead lw 3 dt 2
#set label "HYBTuner switches up" at 44.5, 3.7 tc rgb 'red'
#set arrow from 44.7, graph 0.7 to 44.9, graph 0.22 lw 3
#plot 'rob-185.txt' u 2:($5/1000) with lines lw 3 axes x1y1 t 'HYB', \
#'mpct-185.txt' u 2:($5/1000) with lines lw 3 dt 2 axes x1y1 t 'HYBTuner'
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
