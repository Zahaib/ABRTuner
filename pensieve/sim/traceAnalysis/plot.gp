set term pngcairo dashed dl 2.0 font ",16"
set output 'trace-analysis.png'
set xlabel 'BW (Mbps)'
set ylabel 'CDF'
plot 'cdf_cooked_trace_raw.txt' u ($2*1000):1 with lines lw 3 t 'Pensieve training', \
'cdf_cooked_test_trace_raw.txt' u ($2*1000):1 with lines lw 3 t 'Pensieve test', \
'cdf_lt_3000_pen_trace.txt' u 2:1 with lines lw 3 t 'Conviva < 3K'
