set term pngcairo dashed dl 2.0 font ",16"
set output 'avgbrCDF.png'
set xlabel "Avg BR"
set ylabel "CDF"
set key top left
plot "<(sed -n '1,101p' cdf.dat)" u 2:1 with lines lw 3 t '100',\
"" u 3:1 with lines lw 3 t '300',\
"" u 4:1 with lines lw 3 t '500',\
"" u 5:1 with lines lw 3 t '700',\
"" u 6:1 with lines lw 3 t '900',\
"" u 7:1 with lines lw 3 t '1100',\
"" u 8:1 with lines lw 3 t '1300',\
"" u 9:1 with lines lw 3 t '1500',\
"" u 10:1 with lines lw 3 t '1700',\
"" u 11:1 with lines lw 3 t '1900',\
"" u 12:1 with lines lw 3 t '2100',\
"" u 13:1 with lines lw 3 t '2300',\
"" u 14:1 with lines lw 3 t '2500',\
"" u 15:1 with lines lw 3 t '2700',\
"" u 16:1 with lines lw 3 t '3000'

reset
set term pngcairo dashed dl 2.0 font ",16"
set output 'rebufCDF.png'
set xlabel "Rebuf"
set ylabel "CDF"
set yrange [75:100]
plot "<(sed -n '102,202p' cdf.dat)" u 2:1 with lines lw 3 t '100',\
"" u 3:1 with lines lw 3 t '300',\
"" u 4:1 with lines lw 3 t '500',\
"" u 5:1 with lines lw 3 t '700',\
"" u 6:1 with lines lw 3 t '900',\
"" u 7:1 with lines lw 3 t '1100',\
"" u 8:1 with lines lw 3 t '1300',\
"" u 9:1 with lines lw 3 t '1500',\
"" u 10:1 with lines lw 3 t '1700',\
"" u 11:1 with lines lw 3 t '1900',\
"" u 12:1 with lines lw 3 t '2100',\
"" u 13:1 with lines lw 3 t '2300',\
"" u 14:1 with lines lw 3 t '2500',\
"" u 15:1 with lines lw 3 t '2700',\
"" u 16:1 with lines lw 3 t '3000'




reset
set term pngcairo size 640,420 font ",16"
set output 'br-rb-candlesticks.png'
set boxwidth 0.2 absolute
set xlabel 'Cell size'
set ylabel 'Avg. Bitrate (Mbps)'
set y2tics nomirror
set ytics nomirror
set y2label 'Rebuf'
set xrange [0:12]
set yrange [1:3]
set key samplen 1
set key top out horizontal
set xtics rotate by 45 offset -1,-1
plot 'brcandles.dat' using 1:4:xticlabels(2) linetype -3 notitle,\
     '' using ($1-0.15):($4/1000):($3/1000):($7/1000):($6/1000) with candlesticks linetype 1 lw 3 title 'Avg. bitrate' whiskerbars,\
     '' using ($1-0.15):($5/1000):($5/1000):($5/1000):($5/1000) with candlesticks linetype -1 lw 3 notitle,\
     'rfcandles.dat' using ($1+0.15):4:3:7:6 with candlesticks linetype 1 lw 3 lc rgb 'green' axes x1y2 title 'Rebuf' whiskerbars,\
     '' using ($1+0.15):5:5:5:5 with candlesticks linetype -1 lw 3 axes x1y2 notitle
