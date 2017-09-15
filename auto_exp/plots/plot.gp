set term pngcairo dashed dl 2.0 font ",16"
set output 'brCDF.png'
set xlabel 'Avg. br'
set ylabel 'CDF'
set key top left
plot 'cdf_bitrate_tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_bitrate_mpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'RebufCDF.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
set yrange [85:100]
set key bottom right
plot 'cdf_rebuf_tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_rebuf_mpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'brDiffCDF.png'
set xlabel 'BR Diff (%)'
set ylabel 'CDF'
set key top left
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_bitrate_percentage_diff_mpc.txt' u 2:1 with lines lw 3 t 'MPC', \
'cdf_bitrate_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Penseive'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebufDiffCDF.png'
set xlabel 'Rebuf Diff (%)'
set ylabel 'CDF'
set key bottom right
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_rebuf_percentage_diff_mpc.txt' u 2:1 with lines lw 3 t 'MPC', \
'cdf_rebuf_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Penseive'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'QoECDF.png'
set xlabel 'Pensieve style QoE'
set ylabel 'CDF'
set key bottom right
plot 'cdf_qoe_tuner.txt' u 2:1 with lines lw 3 t 'Tuner', \
'cdf_qoe_pensieve.txt' u 2:1 with lines lw 3 t 'Penseive'
