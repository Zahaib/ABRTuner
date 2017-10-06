reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'percentage_diff.png'
set xlabel 'Percentage difference'
set ylabel 'CDF'
plot 'avgbr_rebuff_percentage_diff.dat' u 2:1 with lines lw 3 t 'Avgbr %age diff', \
'avgbr_rebuff_percentage_diff.dat' u 3:1 with lines lw 3 t 'Rebuf %age diff'
