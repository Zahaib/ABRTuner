set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf_compare.png'
set xlabel 'Rebuf ratio'
set ylabel 'CDF'
set yrange [60:100]
set xrange [0:12]
plot 'cdf_rebuf_online-tuner.txt' u 2:1 with lines lw 3 t 'HYB+Tuner', \
'cdf_rebuf_hyb.txt' u 2:1 with lines lw 3 t 'HYB'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'avgbr_compare.png'
set xlabel 'Avg. bitrate'
set ylabel 'CDF'
plot 'cdf_bitrate_online-tuner.txt' u 2:1 with lines lw 3 t 'HYB+Tuner', \
'cdf_bitrate_hyb.txt' u 2:1 with lines lw 3 t 'HYB'

