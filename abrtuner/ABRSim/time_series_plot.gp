set term pngcairo size 960,1280 dashed dl 2.0 font ",16"
#set output 'll.png'
set multiplot layout 4,1
set xlabel "Chunk number (1-49)"
set ylabel "BW (kbps)"
plot "<(sed -n '1,49p' tmp.txt)" u 7:3 with lines lw 2 t 'original', \
"<(sed -n '51,99p' tmp.txt)" u 7:3 with lines lw 2 t 'disc factor = 80%'

set xlabel "Chunk number (1-49)"
set ylabel "Absolute discount factor (kbps)"
plot "<(sed -n '1,49p' tmp.txt)" u 7:11 with lines lw 2 t 'original', \
"<(sed -n '51,99p' tmp.txt)" u 7:11 with lines lw 2 t 'disc factor = 80%'

set xlabel "Chunk number (1-49)"
set ylabel "Buffer (sec)"
#set yrange [0:60]
plot "<(sed -n '1,49p' tmp.txt)" u 7:4 with lines lw 2 t 'original', \
"<(sed -n '51,99p' tmp.txt)" u 7:4 with lines lw 2 t 'disc factor = 80%'


set xlabel "Chunk number (1-49)"
set ylabel "Bitrate (index)"
set yrange [-0.5:5.5]
plot "<(sed -n '1,49p' tmp.txt)" u 7:6 with lines lw 2 t 'original', \
"<(sed -n '51,99p' tmp.txt)" u 7:6 with lines lw 2 t 'disc factor = 80%'

unset multiplot

