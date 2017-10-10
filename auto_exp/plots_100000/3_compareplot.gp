set term pngcairo dashed dl 2.0 font ",16"
set output 'brCDF.png'
set xlabel 'Avg. br'
set ylabel 'CDF'
set key top left
plot 'cdf_bitrate_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

#plot '../plots/cdf_bitrate_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
#'../plots/cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
#'../plots/cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
#'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'RebufCDF.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
set yrange [80:100]
set key bottom right
set xrange[0:6]
plot 'cdf_rebuf_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

#plot '../plots/cdf_rebuf_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
#'../plots/cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
#'../plots/cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
#'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'changeCDF.png'
set xlabel 'Average bitrate change (kbps)'
set ylabel 'CDF'
#set yrange [85:100]
set key bottom right
plot 'cdf_change_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_change_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC', \

#plot '../plots/cdf_change_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
#'../plots/cdf_change_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
#'../plots/cdf_change_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
#'cdf_change_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC', \

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'qoeCDF.png'
set xlabel 'QoE'
set ylabel 'CDF'
set key bottom right
set xrange[-0.25:4.3]
plot 'cdf_qoe_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_qoe_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

#plot '../plots/cdf_qoe_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
#'../plots/cdf_qoe_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
#'../plots/cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
#'cdf_qoe_robustmpc.txt' u 2:1 with lines lw 3 t '100000 MPC'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'brDiffCDF.png'
set xlabel 'BR Diff (%)'
set ylabel 'CDF'
set key top left
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_bitrate_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

#plot '../plots/cdf_bitrate_percentage_diff_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC', \
#'../plots/cdf_bitrate_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lt 3 lw 3 t 'Penseive', \
#'cdf_bitrate_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebufDiffCDF.png'
set xlabel 'Rebuf Diff (%)'
set ylabel 'CDF'
set key bottom right
set yzeroaxis lt 1 lw 3 lc rgb 'black'
set xrange [-2:8]
plot 'cdf_rebuf_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

#plot '../plots/cdf_rebuf_percentage_diff_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC', \
#'../plots/cdf_rebuf_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lt 3 lw 3 t 'Penseive', \
#'cdf_rebuf_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'changeDiffCDF.png'
set xlabel 'Change Diff (%)'
set ylabel 'CDF'
set key top left
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_change_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

#plot '../plots/cdf_change_percentage_diff_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC', \
#'../plots/cdf_change_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lt 3 lw 3 t 'Penseive', \
#'cdf_change_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'qoeDiffCDF.png'
set xlabel 'QoE Diff (%)'
set ylabel 'CDF'
set key bottom right
set yzeroaxis lt 1 lw 3 lc rgb 'black'
set xrange [-50:50]
plot 'cdf_qoe_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000'

#plot '../plots/cdf_qoe_percentage_diff_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC', \
#'../plots/cdf_qoe_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lt 3 lw 3 t 'Penseive', \
#'cdf_qoe_percentage_diff_robustmpc.txt' u 2:1 with lines lt 4 lw 3 t 'MPC-100000', \


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'mpcRebuff.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
set key bottom right
set yrange [80:100]
plot 'cdf_rebuf_robustmpc.txt' u 2:1 with lines lt 1 lw 3 t 'MPC-100000', \
'../plots_8600/cdf_rebuf_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC 8600', \
'../plots_4300/cdf_rebuf_robustmpc.txt' u 2:1 with lines lt 3 lw 3 t 'MPC 4300'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'mpcBitrate.png'
set xlabel 'Bitrate'
set ylabel 'CDF'
set key bottom right
plot 'cdf_bitrate_robustmpc.txt' u 2:1 with lines lt 1 lw 3 t 'MPC-100000', \
'../plots_8600/cdf_bitrate_robustmpc.txt' u 2:1 with lines lt 2 lw 3 t 'MPC 8600', \
'../plots_4300/cdf_bitrate_robustmpc.txt' u 2:1 with lines lt 3 lw 3 t 'MPC 4300'
