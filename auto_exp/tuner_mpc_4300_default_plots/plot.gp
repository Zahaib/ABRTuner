set term pngcairo dashed dl 2.0 font ",16"
set output 'tuner_better_rebuf.png'
set xrange [0:9000]
set yrange [0:5000]
set xlabel 'Avg BW'
set ylabel 'Stdev'
set title 'Rebuf'
plot "<(bash getTraceAvgBWStdev.sh mpc_tuner_worse_rebuf.txt)" u 1:2 with points ps 2 lw 2 t 'Tuner worse', \
"<(bash getTraceAvgBWStdev.sh mpc_tuner_better_rebuf.txt)" u 1:2 with points ps 2 lw 2 t 'Tuner better'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'tuner_better_bitrate.png'
set xrange [0:9000]
set yrange [0:5000]
set xlabel 'Avg BW'
set ylabel 'Stdev'
set title 'Bitrate'
plot "<(bash getTraceAvgBWStdev.sh mpc_tuner_worse_bitrate.txt)" u 1:2 with points ps 2 lw 2 t 'Tuner worse', \
"<(bash getTraceAvgBWStdev.sh mpc_tuner_better_bitrate.txt)" u 1:2 with points ps 2 lw 2 t 'Tuner better'
