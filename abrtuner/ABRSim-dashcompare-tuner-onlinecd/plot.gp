set term png
set output 'bw.png'

plot 'out.txt' u 1:2 with linespoints t 'BW', 'out2.txt' u ($1/1000):2 with linespoints t 'Orig', 'out3.txt' u ($1/1000):2 with linespoints t 'Est'
