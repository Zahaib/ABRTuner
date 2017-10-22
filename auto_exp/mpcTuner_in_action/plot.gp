set term pngcairo size 640,960 dashed dl 0.1 font ",16"
set output 'badqoe_instance.png'
set multiplot layout 4,1

set ylabel 'BW (Mbps)'
set xrange [0:180]
set ytics nomirror
set y2tics nomirror
#set y2label 'BW Mbps'
set yrange [0.4:3.4]
set y2range [0.4:3.4]
set ytics 0.5
set y2tics 0.5
set key samplen 1
plot 'bw_emulated.txt' u 1:2 with lines dt 2 lw 3 lc rgb 'red' t 'Bandwidth'


set ylabel 'discount'
set xrange [0:180]
set ytics nomirror
set y2tics nomirror
set y2label 'change'
set yrange [0:100]
set y2range [0:1]
set ytics 20
set y2tics 1
set key samplen 1
plot 'change_detection.txt' u 1:2 with lines axes x1y2 dt 1 lw 3 t 'change point', \
'' u 1:3 with lines axes x1y1 dt 2 lw 3 t 'discount'

set y2tics nomirror
set ytics nomirror
set y2range [0:4.5]
set yrange [0:40]
set xrange [0:190]
set y2tics 1
#set xlabel 'Time (sec)'
set ylabel 'Buffer (sec)'
set y2label 'Bitrate (Mbps)'
set key samplen 1
set ytics 10
plot 'robust_timeline.txt' u 2:4 with lines lw 3 axes x1y1 t 'bufferlen', \
'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 t 'bitrate'

set y2tics nomirror
set ytics nomirror
set y2range [0:4.5]
set yrange [0:40]
set xrange [0:190]
set y2tics 1
set xlabel 'Time (sec)'
set ylabel 'Buffer (sec)'
set y2label 'Bitrate (Mbps)'
plot 'mpc-tuner_timeline.txt' u 2:4 with lines lw 3 axes x1y1 notitle, \
'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 notitle
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
