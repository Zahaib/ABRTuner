#set term pngcairo size 640,640 dashed dl 0.1 font ",16"
#set output 'badqoe_instance.png'
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
#plot 'robust_timeline.txt' u 2:4 with lines lw 3 axes x1y1 t 'bufferlen', \
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
#plot 'online-tuner_timeline.txt' u 2:4 with lines lw 3 axes x1y1 notitle, \
#'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 notitle
#unset multiplot 
#
#
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

reset
set term pngcairo size 640,480 dashed dl 0.1 font ",16"
set output 'pensieve.png'
set title 'Pensieve'
set y2tics nomirror
set ytics nomirror
set y2range [0:4.5]
set yrange [0:30]
set xrange [0:30]
set y2tics 1
#set xlabel 'Time (sec)'
set ylabel 'Buffer (sec)'
set y2label 'Bitrate (Mbps)'
set key samplen 1
set ytics 3
plot 'pens-53.txt' u 2:4 with lines lw 3 axes x1y1 t 'bufferlen', \
'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 t 'bitrate'

reset
set term pngcairo size 640, 480 dashed dl 0.1 font ",16"
set output 'robustmpc.png'
set title 'RobustMPC'
set y2tics nomirror
set ytics nomirror
set y2range [0:4.5]
set yrange [0:30]
set xrange [0:30]
set y2tics 1
set ylabel 'Buffer (sec)'
set y2label 'Bitrate (Mbps)'
plot 'rob-53.txt' u 2:4 with lines lw 3 axes x1y1 notitle, \
'' u 2:($5/1000) with lines lw 3 dt 2 axes x1y2 notitle

