set term pngcairo size 640,1280 dashed dl 2.0 font ",16"
set output 'std_compare.png'
set multiplot layout 3,1
set xlabel 'Lookahead Window Size'
set ylabel 'Avg. BR'
set title 'Avgbw = 3000, stdev = 0'
set boxwidth 0.5
set xrange [0:8]
set yrange [2820:2920]
plot "zero_std.dat" u 7:14:xtic(7) with boxes notitle

set title 'Avgbw = 3000, stdev = 247'
set boxwidth 0.5
set xrange [0:8]
set yrange [2820:2920]
plot "247_std.dat" u 7:14:xtic(7) with boxes notitle

set title 'Avgbw = 3000, stdev = 1835'
set boxwidth 0.5
set xrange [0:8]
set yrange [3000:3200]
plot "1835_std.dat" u 7:14:xtic(7) with boxes notitle
unset multiplot

reset
set term pngcairo size 640,1280 dashed dl 2.0 font ",16"
set output 'bw_compare.png'
set multiplot layout 3,1
set xlabel 'Time (sec)'
set ylabel 'BW (kbps)'
set title 'Avgbw = 3000, stdev = 0'
set yrange [0:9000]
set xrange[0:210]
plot "16716_3000_0.txt" u ($1/1000):2 with lines lw 3 notitle

set title 'Avgbw = 3000, stdev = 247'
set yrange [0:9000]
set xrange[0:210]
plot "16707_3000_247.txt" u ($1/1000):2 with lines lw 3 notitle

set title 'Avgbw = 3000, stdev = 1835'
set yrange [0:9000]
set xrange[0:210]
plot "16772_3000_1835.txt" u ($1/1000):2 with lines lw 3 notitle
unset multiplot

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window5_bestdiscount.png'
set title 'Lookahead windowsize = 5'
set xlabel 'Coefficient of Variation of BW'
set ylabel 'Best Discount Percentage'
plot "<(python discount_factor.py results_focused_filelist_window=5.txt)" u 4:5 with points pt 3 ps 2 lw 3 notitle

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window1_bestdiscount.png'
set title 'Lookahead windowsize = 1'
set xlabel 'Coefficient of Variation of BW'
set ylabel 'Best Discount Percentage'
plot "<(python discount_factor.py results_focused_filelist_window=1.txt)" u 4:5 with points pt 3 ps 2 lw 3 notitle

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window5_bestdiscount_10gap.png'
set title 'Lookahead windowsize = 5'
set xlabel 'Coefficient of Variation of BW'
set ylabel 'Best Discount Percentage'
plot "<(python discount_factor.py results_focused_filelist_window5_gap10.txt)" u 4:5 with points pt 3 ps 2 lw 3 notitle

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window5_bestdiscount_10gap_avgbw_stdbw.png'
set title 'Lookahead windowsize = 5'
set xlabel 'Avg BW'
set ylabel 'StdBW'
plot "<(python discount_factor.py results_focused_filelist_window5_gap10.txt)" u 2:3:5 with points pt 3 ps 2 lw 3 palette notitle

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window5_bestdiscount_5gap_avgbw_stdbw.png'
set title 'Lookahead windowsize = 5'
set xlabel 'Avg BW'
set ylabel 'StdBW'
plot "<(python discount_factor.py results_focused_filelist_window5_gap5.txt)" u 2:3:5 with points pt 3 ps 2 lw 3 palette notitle

reset
set term pngcairo size 640,480 dashed dl 2.0 font ",16"
set output 'window1_bestdiscount_10gap.png'
set title 'Lookahead windowsize = 1'
set xlabel 'Coefficient of Variation of BW'
set ylabel 'Best Discount Percentage'
plot "<(python discount_factor.py results_focused_filelist_window1_gap10.txt)" u 4:5 with points pt 3 ps 2 lw 3 notitle
