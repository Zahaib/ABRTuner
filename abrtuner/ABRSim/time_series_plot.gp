#set term pngcairo size 960,1280 dashed dl 2.0 font ",16"
#set multiplot layout 4,1
#set xlabel "Chunk number (1-49)"
#set ylabel "BW (kbps)"
#plot "<(sed -n '1,49p' tmp.txt)" u 7:3 with lines lw 2 t 'original', \
#"<(sed -n '51,99p' tmp.txt)" u 7:3 with lines lw 2 t 'disc factor = 80%'
#
#set xlabel "Chunk number (1-49)"
#set ylabel "Absolute discount factor (kbps)"
#plot "<(sed -n '1,49p' tmp.txt)" u 7:11 with lines lw 2 t 'original', \
#"<(sed -n '51,99p' tmp.txt)" u 7:11 with lines lw 2 t 'disc factor = 80%'
#
#set xlabel "Chunk number (1-49)"
#set ylabel "Buffer (sec)"
##set yrange [0:60]
#plot "<(sed -n '1,49p' tmp.txt)" u 7:4 with lines lw 2 t 'original', \
#"<(sed -n '51,99p' tmp.txt)" u 7:4 with lines lw 2 t 'disc factor = 80%'
#
#set xlabel "Chunk number (1-49)"
#set ylabel "Bitrate (index)"
#set yrange [-0.5:5.5]
#plot "<(sed -n '1,49p' tmp.txt)" u 7:6 with lines lw 2 t 'original', \
#"<(sed -n '51,99p' tmp.txt)" u 7:6 with lines lw 2 t 'disc factor = 80%'
#unset multiplot

set term pngcairo size 1280,1280 dashed dl 2.0 font ",16"
set output '1.png'
set multiplot layout 4,1
set title ARG1
#set title 'BW'
set xlabel "Time (sec)"
set ylabel "BW (kbps)"
plot "a.txt" u 1:2 with lines lw 2 t 'tuner mpc', \
"b.txt" u 1:2 with lines lw 2 t 'mpc default'

set title 'Discount factor'
set xlabel "Time (sec)"
set ylabel "Discount factor (%)"
set yrange [0:200]
plot "a.txt" u 1:($11*100) with lines lw 2 t 'tuner mpc', \
"b.txt" u 1:($11*100) with lines lw 2 t 'mpc default'

set title 'Ch pt Detection'
set xlabel "Time (sec)"
set ylabel "Detection index"
set yrange [0:5000]
plot "a.txt" u 1:13 with lines lw 2 t 'tuner mpc'

set title 'Bitrate'
set xlabel "Time (sec)"
set ylabel "Bitrate (0-5)"
set yrange [-0.5:5.5]
plot "a.txt" u 1:6 with lines lw 2 t 'tuner mpc', \
"b.txt" u 1:6 with lines lw 2 t 'mpc default'
unset multiplot
