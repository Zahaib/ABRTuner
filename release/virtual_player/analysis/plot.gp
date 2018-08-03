set term pngcairo dashed dl 2.0 font ",16"
set output 'br.png'
set xlabel 'Avgbr'
set ylabel 'CDF'
set key top left
plot "<(python mpc_analysis.py ../results_mpc_trace_500_pen.txt)" u 2:1 with lines lw 3 t 'win=1', \
"" u 3:1 with lines lw 3 t 'win=2', \
"" u 4:1 with lines lw 3 t 'win=3', \
"" u 5:1 with lines lw 3 t 'win=4', \
"" u 6:1 with lines lw 3 t 'win=5', \
"" u 7:1 with lines lw 3 t 'win=6', \
"" u 8:1 with lines lw 3 t 'win=7'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebuf.png'
set xlabel 'Rebuf'
set ylabel 'CDF'
set yrange[80:100]
set key bottom right
plot "<(python mpc_analysis.py ../results_mpc_trace_500_pen.txt)" u 9:1 with lines lw 3 t 'win=1', \
"" u 10:1 with lines lw 3 t 'win=2', \
"" u 11:1 with lines lw 3 t 'win=3', \
"" u 12:1 with lines lw 3 t 'win=4', \
"" u 13:1 with lines lw 3 t 'win=5', \
"" u 14:1 with lines lw 3 t 'win=6', \
"" u 15:1 with lines lw 3 t 'win=7'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'change.png'
set xlabel 'Per chunk change'
set ylabel 'CDF'
plot "<(python mpc_analysis.py ../results_mpc_trace_500_pen.txt)" u 16:1 with lines lw 3 t 'win=1', \
"" u 17:1 with lines lw 3 t 'win=2', \
"" u 18:1 with lines lw 3 t 'win=3', \
"" u 19:1 with lines lw 3 t 'win=4', \
"" u 20:1 with lines lw 3 t 'win=5', \
"" u 21:1 with lines lw 3 t 'win=6', \
"" u 22:1 with lines lw 3 t 'win=7'


reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_br_CDF.png'
set xlabel 'BR (Kbps)'
set ylabel 'Frac. of sessions'
plot "cdf_bola_oncd_min_5_target_30_notbufferleveladjusted.txt" u 2:1 with lines lw 3 t 'BOLA'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_rebuf_CDF.png'
set xlabel 'Rebuf Ratio'
set ylabel 'Frac. of sessions'
set yrange[80:100]
plot "cdf_bola_oncd_min_5_target_30_notbufferleveladjusted.txt" u 3:1 with lines lw 3 t 'BOLA'
