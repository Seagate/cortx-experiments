set terminal pngcairo size 1024,768
set output datafile.".png"

stats datafile using 1:(column(-2)) nooutput

plot for [idx=1:STATS_blocks] datafile index (idx-1) using 1:(STATS_blocks + 1- column(-2)):yticlabel(3) with lines lw 6 notitle, for [idx=1:STATS_blocks] datafile index (idx-1) using 1:(STATS_blocks + 1 - column(-2)):2 with labels left point pt 8 rotate by 90 notitle

set terminal x11 size 1024,768
set output

set lmargin 15

replot

pause -1
