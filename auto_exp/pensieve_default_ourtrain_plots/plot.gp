set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'avgbr.png'
set xlabel 'Avg. Bitrate (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:4300]
set key bottom right
set xtics 1000
plot 'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_bitrate_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'OurTrain', \

reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'rebuf.png'
set xlabel 'Rebuf. Ratio (%)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:5]
set yrange [90:100]
set key bottom right
plot 'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_rebuf_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'OurTrain', \


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'change.png'
set xlabel 'Avg. per chunk change (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [0:1000]
plot 'cdf_change_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_change_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'OurTrain', \


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'qoe.png'
set xlabel 'Average QoE per chunk'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [-0.5:4.5]
plot 'cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_qoe_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'OurTrain', \


