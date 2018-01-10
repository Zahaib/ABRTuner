set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 600, 400 
set output 'pm3d.25.png'
set border 895 front lt black linewidth 1.000 dashtype solid
set grid nopolar
set grid xtics nomxtics ytics nomytics noztics nomztics nortics nomrtics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set grid layerdefault   lt 0 linecolor 0 linewidth 0.500,  lt 0 linecolor 0 linewidth 0.500
set style line 100  linecolor rgb "#f0e442"  linewidth 0.500 dashtype solid pointtype 5 pointsize default #pointinterval 0 pointnumber 0
set view map scale 1
set samples 11, 11
set isosamples 11, 11
unset surface 
set style data pm3d
set style function pm3d
set xyplane relative 0
set nomcbtics
set title "Datafile with different nb of points in scans; pm3d flush begin" 
set xlabel "X LABEL" 
set ylabel "Y LABEL" 
set lmargin  0
set pm3d implicit at b
set pm3d scansforward
## Last datafile plotted: "triangle.dat"
splot 'triangle.dat'
