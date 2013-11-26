#
# $Id: surface1.dem,v 1.11 2004/09/17 05:01:12 sfeam Exp $
#


set xlabel "Support"
set ylabel "Confidence"
set zlabel "Time"
set title "Testing time in sec"
set grid
set dgrid 7,8
#set dgrid 30, 30
set pm3d
set hidden3d
splot "graph_input.dat" every ::1 u 1:2:10 notitle with lines

pause -1
