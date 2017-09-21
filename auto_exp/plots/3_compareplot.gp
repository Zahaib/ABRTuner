
set term pngcairo dashed dl 2.0 font ",16"
set output 'brCDF.png'
set xlabel 'Avg. br'
set ylabel 'CDF'
set key top left
plot 'cdf_bitrate_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'RebufCDF.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
set yrange [85:100]
set key bottom right
plot 'cdf_rebuf_online-tuner.txt' u 2:1 with lines lw 3 t 'ABRTuner', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC' , \
'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'brDiffCDF.png'
set xlabel 'BR Diff (%)'
set ylabel 'CDF'
set key top left
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_bitrate_percentage_diff_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC', \
'cdf_bitrate_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Penseive'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebufDiffCDF.png'
set xlabel 'Rebuf Diff (%)'
set ylabel 'CDF'
set key bottom right
set yzeroaxis lt 1 lw 3 lc rgb 'black'
plot 'cdf_rebuf_percentage_diff_robustmpc.txt' u 2:1 with lines lw 3 t 'MPC', \
'cdf_rebuf_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Penseive'
