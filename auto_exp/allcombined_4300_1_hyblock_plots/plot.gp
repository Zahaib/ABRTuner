set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'avgbr.png'
set xlabel 'Avg. Bitrate (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:2500]
set key bottom right
set xtics 1000
plot 'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines dt 2 lw 4 t 'RobustMPC', \
'cdf_bitrate_online-tuner.txt' u 2:1 with lines dt 1 lw 4 t 'HYB+ABRTuner'

reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'rebuf.png'
set xlabel 'Rebuf. Ratio (%)'
set ylabel 'CDF(Perc. of sessions)'
set xrange [0:5]
set yrange [60:100]
set key bottom right
plot 'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines dt 2 lw 4 t 'RobustMPC', \
'cdf_rebuf_online-tuner.txt' u 2:1 with lines dt 1 lw 4 t 'HYB+ABRTuner'


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'change.png'
set xlabel 'Avg. per chunk change (kbps)'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [0:1000]
plot 'cdf_change_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_change_robustmpc.txt' u 2:1 with lines dt 2 lw 4 t 'RobustMPC', \
'cdf_change_online-tuner.txt' u 2:1 with lines dt 1 lw 4 t 'HYB+ABRTuner'


reset
set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
set output 'qoe.png'
set xlabel 'Average QoE per chunk'
set ylabel 'CDF(Perc. of sessions)'
set key bottom right
set xrange [-0.5:2.5]
plot 'cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines dt 5 lw 4 t 'Pensieve', \
'cdf_qoe_robustmpc.txt' u 2:1 with lines dt 2 lw 4 t 'RobustMPC', \
'cdf_qoe_online-tuner.txt' u 2:1 with lines dt 1 lw 4 t 'HYB+ABRTuner'



#reset
#set term pngcairo size 640, 420 dashed dl 0.15 font ",16"
#set output 'diff.png'
#set xlabel '(c) Perc Diff. in Rebuf. Ratio over HYB (%)'
#set ylabel 'CDF(Perc. of sessions)'
#set x2tics nomirror
#set x2label 'Perc. Diff in Avg. Bitrate over HYB (%)'
#set xrange [-0.5:0.5]
#set x2range [-10:10]
#set key top left
#set key samplen 1
#plot 'cdf_rebuf_percentage_diff_hyb.txt' u 2:1 with lines axes x1y1 dt 5 lw 4 lc rgb 'blue' t 'Rebuf. Ratio', \
#'cdf_bitrate_percentage_diff_hyb.txt' u 2:1 with lines axes x2y1 dt 1 lw 4 lc rgb 'red' t 'Avg. Bitrate'
#
