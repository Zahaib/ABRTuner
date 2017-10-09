set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf_compare.png'
set xlabel 'Rebuf ratio'
set ylabel 'CDF'
set yrange [60:100]
set xrange [0:12]
plot '../plots_8600/cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'Rebuf 8600', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'Rebuf 4300'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'avgbr_compare.png'
set xlabel 'Avg. bitrate'
set ylabel 'CDF'
plot '../plots_8600/cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t '8600', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t '4300'

