set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf_compare.png'
set xlabel 'Rebuf ratio'
set ylabel 'CDF'
set yrange [60:100]
plot '../plots_8600/cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'Rebuf 8600', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'Rebuf 4300'
