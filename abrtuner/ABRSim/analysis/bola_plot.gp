
reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_br_CDF.png'
set xlabel 'BR (Kbps)'
set ylabel 'Frac. of sessions'
set key top left
plot "cdf_bola_oncd_min_5_target_30.txt" u 2:1 with lines lw 3 t 'BOLA+Tuner min', \
"cdf_bola_oncd_median_min_5_target_30.txt" u 2:1 with lines lw 3 t 'BOLA+Tuner med', \
"cdf_bola_static_min_5_target_30.txt" u 2:1 with lines lw 3 t 'BOLA'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_rebuf_CDF.png'
set xlabel 'Rebuf Ratio'
set ylabel 'Frac. of sessions'
set yrange[80:100]
set key bottom right
plot "cdf_bola_oncd_min_5_target_30.txt" u 3:1 with lines lw 3 t 'BOLA+Tuner min', \
"cdf_bola_oncd_median_min_5_target_30.txt" u 3:1 with lines lw 3 t 'BOLA+Tuner med', \
"cdf_bola_static_min_5_target_30.txt" u 3:1 with lines lw 3 t 'BOLA'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_br_CDF.png'
set xlabel 'BR (Kbps)'
set ylabel 'Frac. of sessions'
plot "cdf_bola_static_min_5_target_15_notbufferleveladjusted.txt" u 2:1 with lines lw 3 t 'BOLA sim', \
"cdf_bola_oncd_min_5_target_15_notbufferleveladjusted.txt" u 2:1 with lines lw 3 t 'BOLA Tuner'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_rebuf_CDF.png'
set xlabel 'Rebuf Ratio'
set ylabel 'Frac. of sessions'
set yrange[80:100]
plot "cdf_bola_static_min_5_target_15_notbufferleveladjusted.txt" u ($3 * 100):1 with lines lw 3 t 'BOLA sim', \
"cdf_bola_oncd_min_5_target_15_notbufferleveladjusted.txt" u ($3 * 100):1 with lines lw 3 t 'BOLA Tuner'



reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_br_10_30_CDF.png'
set xlabel 'BR (Kbps)'
set ylabel 'Frac. of sessions'
plot "cdf_bola_static_min_10_target_30_simbufferadjust.txt" u 2:1 with lines lw 3 t 'BOLA default', \
"cdf_bola_oncd_min_10_target_30_simbufferadjust.txt" u 2:1 with lines lw 3 t 'BOLA Tuner'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'bola_rebuf_10_30_CDF.png'
set xlabel 'Rebuf Ratio'
set ylabel 'Frac. of sessions'
set yrange[80:100]
plot "cdf_bola_static_min_10_target_30_simbufferadjust.txt" u ($3 * 100):1 with lines lw 3 t 'BOLA default', \
"cdf_bola_oncd_min_10_target_30_simbufferadjust.txt" u ($3 * 100):1 with lines lw 3 t 'BOLA Tuner'
