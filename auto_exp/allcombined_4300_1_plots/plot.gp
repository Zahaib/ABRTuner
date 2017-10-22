set term pngcairo dashed dl 2.0 font ",16"
set output 'qoe_ri.png'
set xlabel 'QoE of Rebuf Impacted Sessions'
set ylabel 'CDF'
plot 'cdf_qoe_rirobustmpc.txt' u 2:1 with lines lw 3 t 'RobustMPC', \
'cdf_qoe_rionline-tuner.txt' u 2:1 with lines lw 3 t 'HYBTuner', \
'cdf_qoe_ripensieve-pensvid.txt' u 2:1 with lines lw 3 t 'Pensieve'
