set term pngcairo size 640, 420 dashed dl 2.0 font ",16"
set output 'pens_qoe_diff_lt300_gt_3000.png'
set xlabel "Percentage improvement achieved by MPC Tuner\n Over Pensieve"
set ylabel 'CDF'
#set yrange [80:100]
set xrange [-20:60]
set key bottom right
set yzeroaxis lt -1
plot 'lt3000/cdf_qoe_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'lt 3000', \
'gt3000/cdf_qoe_percentage_diff_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'gt 3000'

