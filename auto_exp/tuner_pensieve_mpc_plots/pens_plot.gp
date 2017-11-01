set term pngcair dashed dl 2.0 font ",16"
set output 'pens_avgbr.png'
set xlabel 'Avg. BR (kbps)'
set ylabel 'CDF'
plot 'lt3000/cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'lt 3000', \
'gt3000/cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'gt 3000'

reset
set term pngcair dashed dl 2.0 font ",16"
set output 'pens_rebuf.png'
set xlabel 'Rebuf Ratio'
set ylabel 'CDF'
set yrange [80:100]
set xrange [0:8]
plot 'lt3000/cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'lt 3000', \
'gt3000/cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'gt 3000'

reset
set term pngcair dashed dl 2.0 font ",16"
set output 'pens_change.png'
set xlabel 'Avg. per chunk change magnitude'
set ylabel 'CDF'
plot 'lt3000/cdf_change_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'lt 3000', \
'gt3000/cdf_change_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'gt 3000'

reset
set term pngcair dashed dl 2.0 font ",16"
set output 'pens_qoe.png'
set xlabel 'QoE'
set ylabel 'CDF'
set xrange [-0.5:4.3]
plot 'lt3000/cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'lt 3000', \
'gt3000/cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'gt 3000'
