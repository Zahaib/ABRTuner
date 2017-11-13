set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'avgbr.png'
set xlabel 'Avg. Bitrate (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:4300]
set key bottom right
set xtics 1000
plot 'cdf_bitrate_original-pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve provided model', \
'cdf_bitrate_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'Our trained model with their set', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines dt 1 lw 4 t 'RobustMPC', \
'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines dt 6 lw 4 lt rgb 'red' t 'Our trained model with our set(all)', \

reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'rebuf.png'
set xlabel 'Rebuf. Ratio (%)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:5]
set yrange [70:100]
set key bottom right
plot 'cdf_rebuf_original-pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve provided model', \
'cdf_rebuf_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'Our trained model with their set', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines dt 1 lw 4 t 'RobustMPC', \
'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines dt 6 lw 4 lt rgb 'red' t 'Our trained model with our set(all)', \


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'change.png'
set xlabel 'Avg. per chunk change (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [0:800]
plot 'cdf_change_original-pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve provided model', \
'cdf_change_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'Our trained model with their set', \
'cdf_change_robustmpc.txt' u 2:1 with lines dt 1 lw 4 t 'RobustMPC', \
'cdf_change_pensieve-pensvid.txt' u 2:1 with lines dt 6 lw 4 lt rgb 'red' t 'Our trained model with our set(all)', \


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'qoe.png'
set xlabel 'Average QoE per chunk'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [-0.5:4.5]
plot 'cdf_qoe_original-pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve provided model', \
'cdf_qoe_ourtrain-pensieve-pensvid.txt' u 2:1 with lines dt 2 lw 4 t 'Our trained model with their set', \
'cdf_qoe_robustmpc.txt' u 2:1 with lines dt 1 lw 4 t 'RobustMPC', \
'cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines dt 6 lw 4 lt rgb 'red' t 'Our trained model with our set(all)', \


