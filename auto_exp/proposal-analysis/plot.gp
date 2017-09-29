set term pngcairo dashed dl 0.15 font ",16"
set output "xput_needed_vs_available.png"
set xlabel "Relative throughput increase \n needed to avoid rebuffering"
set ylabel "Cummulative fraction of sessions \n (chunks) with rebuffering"
set key bottom right
plot 'cdf_session_delta_xput.txt' u 2:($1/100) with lines lw 4 dashtype 1 t 'Per session', \
'cdf_chunk_delta_xput.txt' u 2:($1/100) with lines lw 4 dashtype 2 t 'Per chunk'

