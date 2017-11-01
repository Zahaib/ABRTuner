set term pngcairo dashed dl 2.0 font ",16"
set output 'avgbr_compare.png'
set xlabel 'Avg. bitrate'
set ylabel 'CDF'
set key top left
plot 'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_bitrate_mpc-tuner.txt' u 2:1 with lines lw 3 t 'Tuner MPC', \
'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf_compare.png'
set xlabel 'Rebuf ratio'
set ylabel 'CDF'
set yrange [60:100]
set xrange [0:6]
set key bottom right
plot 'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_rebuf_mpc-tuner.txt' u 2:1 with lines lw 3 t 'Tuner MPC', \
'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'qoe_compare.png'
set xlabel 'QoE'
set ylabel 'CDF'
set yrange [0:100]
set xrange [0:4.2]
set key bottom right
plot 'cdf_qoe_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_qoe_mpc-tuner.txt' u 2:1 with lines lw 3 t 'Tuner MPC', \
'cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'change_compare.png'
set xlabel 'Average change magnitude per chunk'
set ylabel 'CDF'
#set yrange [80:100]
#set xrange [-0.5:4.3]
set key bottom right
plot 'cdf_change_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_change_mpc-tuner.txt' u 2:1 with lines lw 3 t 'Tuner MPC', \
'cdf_change_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'qoe_percentage_improvement.png'
set xlabel 'Percentage improvement achieved by MPC Tuner'
set ylabel 'CDF'
#set yrange [80:100]
set xrange [-20:60]
set key bottom right
set yzeroaxis lt -1
plot 'cdf_qoe_percentage_diff_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_qoe_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'qoe_percentage_improvement_mpctuner_lt_3000_and_full.png'
set xlabel 'Percentage improvement achieved by MPC Tuner'
set ylabel 'CDF'
#set yrange [80:100]
set xrange [-20:60]
set key bottom right
set yzeroaxis lt -1
plot 'cdf_qoe_percentage_diff_robustmpc.txt' u 2:1 with lines lw 3 t '100-9000Kbps BW', \
'cdf_qoe_percentage_diff_robustmpc_lt3000.txt' u 2:1 with lines lw 3 t '< 3000Kbps BW'
