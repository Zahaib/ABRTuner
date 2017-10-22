set term pngcairo dashed dl 2.0 font ",16"
set output 'avg_br.png'
set xlabel 'Avg br'
set ylabel 'CDF'
set key top left
plot 'cdf_bitrate_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
'cdf_bitrate_online-tuner.txt' u 2:1 with lines lw 3 t 'Tuner', \
'cdf_bitrate_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC'

set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
plot 'cdf_rebuf_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
'cdf_rebuf_online-tuner.txt' u 2:1 with lines lw 3 t 'Tuner', \
'cdf_rebuf_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC'

set term pngcairo dashed dl 2.0 font ",16"
set output 'change.png'
set xlabel 'Per chunk average change'
set ylabel 'CDF'
plot 'cdf_change_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve', \
'cdf_change_online-tuner.txt' u 2:1 with lines lw 3 t 'Tuner', \
'cdf_change_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC'

set term pngcairo dashed dl 2.0 font ",16"
set output 'qoe.png'
set xlabel 'Avg br'
set ylabel 'CDF'
set xrange [0:5]
set key top left
plot 'cdf_qoe_online-tuner.txt' u 2:1 with lines lw 3 t 'Tuner', \
'cdf_qoe_robustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_qoe_pensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'
